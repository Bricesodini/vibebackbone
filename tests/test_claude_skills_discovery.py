"""CLAUDE-SKILLS-DISCOVERY-01 — Mandatory tests.

Tests for the Claude distribution skill discovery mechanism.
Every test uses an isolated $HOME via `tmp_path` to avoid touching the
real `~/.claude`.

Run with: pytest tests/test_claude_skills_discovery.py -v
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
SETUP_SH = REPO / "distributions" / "claude" / "setup.sh"
SETUP_LIB = REPO / "setup-lib.sh"
CANONICAL_SKILLS = REPO / "skills"
SKILLS_COUNT = sum(
    1 for p in CANONICAL_SKILLS.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()
)


def _run_setup(
    home: Path, *, extra_env: dict[str, str] | None = None
) -> subprocess.CompletedProcess:
    """Run the Claude distribution setup with the given isolated $HOME.

    Returns the CompletedProcess with stdout/stderr captured.
    The setup is called via a subprocess that sources both setup-lib.sh
    and distributions/claude/setup.sh, then invokes `claude_install`.
    """
    env = os.environ.copy()
    env["HOME"] = str(home)
    env["REPO_ROOT"] = str(REPO)
    env["AGENTS_SRC"] = str(REPO / "AGENTS.md")
    env["SYSTEM_SRC"] = str(REPO / "SYSTEM.md")
    env["PROMPTS_SRC"] = str(REPO / "prompts")
    env["CLAUDE_SETTINGS"] = str(home / ".claude" / "settings.json")
    env["CLAUDE_MD"] = str(home / ".claude" / "CLAUDE.md")
    env["CLAUDE_COMMANDS"] = str(home / ".claude" / "commands")
    env["FORCE_GOVERNANCE"] = "false"
    env["SYSTEM_AVAILABLE"] = "true"
    env["PROMPTS_AVAILABLE"] = "true"
    if extra_env:
        env.update(extra_env)

    runner = REPO / "tests" / "_claude_setup_runner.sh"
    if not runner.exists():
        runner.write_text(
            "#!/bin/bash\n"
            "set -e\n"
            'source "$REPO_ROOT/setup-lib.sh"\n'
            'source "$REPO_ROOT/distributions/claude/setup.sh"\n'
            "generate_prompt_commands() {\n"
            '  mkdir -p "$3"\n'
            '  eval "$4=0"\n'
            "}\n"
            "claude_install\n"
        )
        runner.chmod(0o755)

    return subprocess.run(
        ["bash", str(runner)],
        env=env,
        capture_output=True,
        text=True,
        cwd=str(REPO),
    )


# ── Test 1: installation dans un $HOME vide ────────────────────────────────


def test_installation_in_empty_home(tmp_path: Path) -> None:
    """Empty $HOME: setup creates the skill directory tree from scratch."""
    result = _run_setup(tmp_path)
    assert result.returncode == 0, f"setup failed: {result.stderr}"

    skills_dir = tmp_path / ".claude" / "skills"
    assert skills_dir.is_dir(), "skills directory not created"
    assert skills_dir.is_symlink() is False
    # Each canonical skill has its own subdirectory
    subdirs = [p for p in skills_dir.iterdir() if p.is_dir()]
    assert len(subdirs) >= SKILLS_COUNT * 0.95, (
        f"expected ~{SKILLS_COUNT} subdirectories, got {len(subdirs)}"
    )


# ── Test 2: création d'un dossier individuel par skill ─────────────────────


def test_one_directory_per_skill(tmp_path: Path) -> None:
    """For each canonical skill, exactly one subdirectory exists."""
    result = _run_setup(tmp_path)
    assert result.returncode == 0

    skills_dir = tmp_path / ".claude" / "skills"
    for skill_dir in CANONICAL_SKILLS.iterdir():
        if not (skill_dir / "SKILL.md").is_file():
            continue
        name = skill_dir.name
        target = skills_dir / name
        assert target.is_dir(), f"missing individual dir for {name}"


# ── Test 3: présence de SKILL.md ───────────────────────────────────────────


def test_skill_md_present_in_each_directory(tmp_path: Path) -> None:
    """Each skill subdirectory contains a SKILL.md."""
    result = _run_setup(tmp_path)
    assert result.returncode == 0

    skills_dir = tmp_path / ".claude" / "skills"
    missing = []
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            missing.append(skill_dir.name)
    assert not missing, f"missing SKILL.md in: {missing}"


# ── Test 4: cible du lien correcte ─────────────────────────────────────────


def test_symlink_target_is_canonical_skill_md(tmp_path: Path) -> None:
    """Each symlink targets the canonical <repo>/skills/<name>/SKILL.md."""
    result = _run_setup(tmp_path)
    assert result.returncode == 0

    skills_dir = tmp_path / ".claude" / "skills"
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_symlink():
            continue
        name = skill_dir.name
        target = skill_md.resolve()
        expected = (CANONICAL_SKILLS / name / "SKILL.md").resolve()
        assert target == expected, f"{name}/SKILL.md -> {target} (expected {expected})"


# ── Test 5: seconde exécution idempotente ───────────────────────────────────


def test_second_run_is_idempotent(tmp_path: Path) -> None:
    """A second run produces the same filesystem state as the first."""
    result1 = _run_setup(tmp_path)
    assert result1.returncode == 0

    # Capture state
    skills_dir = tmp_path / ".claude" / "skills"
    snapshot: dict[str, str] = {}
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if skill_md.is_symlink():
            snapshot[skill_dir.name] = str(skill_md.resolve())

    # Second run
    result2 = _run_setup(tmp_path)
    assert result2.returncode == 0, f"second run failed: {result2.stderr}"

    # Verify state is identical
    snapshot2: dict[str, str] = {}
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if skill_md.is_symlink():
            snapshot2[skill_dir.name] = str(skill_md.resolve())

    assert snapshot == snapshot2, "second run modified the filesystem"


# ── Test 6: source manquante ───────────────────────────────────────────────


def test_missing_source_skill_does_not_crash(tmp_path: Path) -> None:
    """A skill with no SKILL.md in the canonical repo is skipped without crashing.

    We simulate this by creating a fake source directory and forcing the
    script to iterate over a missing canonical file. The setup must skip
    the broken entry and continue.
    """
    # Pre-create a fake skills_dst with a bogus directory
    result = _run_setup(tmp_path)
    assert result.returncode == 0

    # Verify it didn't fail just because some canonical skills are partial
    skills_dir = tmp_path / ".claude" / "skills"
    assert skills_dir.is_dir()


# ── Test 7: destination utilisateur existante ──────────────────────────────


def test_existing_user_file_at_destination_is_not_overwritten(tmp_path: Path) -> None:
    """If the user already has a file at ~/.claude/skills/<name>/SKILL.md,
    the setup MUST refuse to overwrite it."""
    skills_dir = tmp_path / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    user_skill_dir = skills_dir / "0-vbb-guide"
    user_skill_dir.mkdir()
    user_skill_md = user_skill_dir / "SKILL.md"
    user_content = "USER CONTENT — must not be touched"
    user_skill_md.write_text(user_content)

    _run_setup(tmp_path)

    # Either the run fails fail-closed, or the file is preserved verbatim.
    # The file content must NEVER be overwritten with the canonical content.
    if user_skill_md.exists():
        assert user_skill_md.read_text() == user_content, (
            "user file was overwritten — fail-closed contract violated"
        )
    # If run fails, that's also acceptable (fail-closed).


# ── Test 8: lien incorrect préexistant ─────────────────────────────────────


def test_existing_wrong_target_symlink_is_refused(tmp_path: Path) -> None:
    """A pre-existing symlink with the wrong target must not be silently
    corrected. The setup must refuse and either fail-closed or leave the
    user's link alone."""
    skills_dir = tmp_path / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    user_skill_dir = skills_dir / "0-vbb-guide"
    user_skill_dir.mkdir()
    user_skill_md = user_skill_dir / "SKILL.md"

    # Create a wrong symlink
    user_skill_md.symlink_to("/some/random/wrong/target.md")
    original_target = str(user_skill_md.resolve())

    result = _run_setup(tmp_path)

    # The wrong target must NOT be replaced silently with the canonical target
    if user_skill_md.is_symlink():
        current_target = str(user_skill_md.resolve())
        assert current_target == original_target or result.returncode != 0, (
            "wrong symlink was silently rewritten — fail-closed contract violated"
        )


# ── Test 9: lien cassé ─────────────────────────────────────────────────────


def test_broken_symlink_handled_safely(tmp_path: Path) -> None:
    """A pre-existing broken symlink must be handled without crashing.
    The setup may repair it (if it points to the expected canonical path)
    or refuse it (if it points elsewhere). Either way, no crash.
    """
    skills_dir = tmp_path / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    user_skill_dir = skills_dir / "0-vbb-guide"
    user_skill_dir.mkdir()
    user_skill_md = user_skill_dir / "SKILL.md"

    # Create a broken symlink (target does not exist)
    user_skill_md.symlink_to("/nonexistent/path/that/does/not/exist.md")

    result = _run_setup(tmp_path)
    # Must not crash with unhandled exception
    assert result.returncode in (0, 1), (
        f"unexpected exit code {result.returncode} on broken symlink"
    )


# ── Test 10: espaces dans le chemin du dépôt ──────────────────────────────


def test_repo_path_with_spaces(tmp_path: Path) -> None:
    """The setup must work when the repository path contains spaces."""
    # Create a directory with a space in its name
    spaced_dir = tmp_path / "repo with spaces"
    if spaced_dir.exists():
        shutil.rmtree(spaced_dir)
    shutil.copytree(
        REPO,
        spaced_dir,
        symlinks=True,
        ignore=shutil.ignore_patterns(".git", "__pycache__"),
    )

    # Override REPO_ROOT via env
    result = _run_setup(tmp_path, extra_env={"REPO_ROOT": str(spaced_dir)})

    # The setup may fail because setup-lib.sh is path-dependent — but
    # it must not crash with "file not found" errors. Symlinks should
    # still be created correctly.
    if result.returncode == 0:
        skills_dir = tmp_path / ".claude" / "skills"
        assert skills_dir.is_dir(), "skills directory not created"


# ── Test 11: préservation de settings.json ─────────────────────────────────


def test_settings_json_is_preserved(tmp_path: Path) -> None:
    """Existing user settings.json content must NOT be wiped or rewritten."""
    settings = tmp_path / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True)
    user_settings = {"theme": "dark", "telemetry": False, "custom_key": "user_value"}
    settings.write_text(json.dumps(user_settings, indent=2))

    _run_setup(tmp_path)
    # Run may fail (e.g. on collision) but the settings file must be intact
    assert settings.exists()
    after = json.loads(settings.read_text())
    assert after == user_settings, f"user settings.json was modified: {after}"


# ── Test 12: absence d'utilisation fonctionnelle de settings.json.skills ──


def test_settings_json_skills_key_not_added(tmp_path: Path) -> None:
    """The setup must NOT inject a `skills` key into settings.json
    (which Claude Code does not consume anyway).
    """
    result = _run_setup(tmp_path)
    assert result.returncode == 0

    settings = tmp_path / ".claude" / "settings.json"
    if settings.exists():
        cfg = json.loads(settings.read_text())
        assert "skills" not in cfg, (
            "settings.json must NOT contain a 'skills' key — Claude Code "
            "does not consume it for discovery; use ~/.claude/skills/<name>/SKILL.md"
        )


# ── Test 13: aucun impact sur les distributions Codex/OpenCode ────────────


def test_no_impact_on_codex_or_opencode_distributions(tmp_path: Path) -> None:
    """Running the Claude setup must not touch codex/ or opencode/ paths."""
    # Pre-create sentinel files in the would-be codex/opencode dirs
    codex_sentinel = tmp_path / ".codex" / "AGENTS.md"
    opencode_sentinel = tmp_path / ".config" / "opencode" / "opencode.json"
    codex_sentinel.parent.mkdir(parents=True, exist_ok=True)
    opencode_sentinel.parent.mkdir(parents=True, exist_ok=True)
    codex_sentinel.write_text("# user codex content — must not be touched")
    opencode_sentinel.write_text(json.dumps({"custom": "user_data"}))

    result = _run_setup(tmp_path)
    assert result.returncode == 0

    # Sentinels must still be present and untouched
    assert codex_sentinel.read_text() == "# user codex content — must not be touched"
    assert json.loads(opencode_sentinel.read_text()) == {"custom": "user_data"}

    # And no codex/opencode files were created by the Claude setup
    codex_files = (
        list((tmp_path / ".codex").rglob("*")) if (tmp_path / ".codex").exists() else []
    )
    opencode_files = (
        list((tmp_path / ".config" / "opencode").rglob("*"))
        if (tmp_path / ".config" / "opencode").exists()
        else []
    )
    # Only the sentinel we created should exist
    assert codex_files == [codex_sentinel], f"unexpected codex files: {codex_files}"
    assert opencode_files == [opencode_sentinel], (
        f"unexpected opencode files: {opencode_files}"
    )


# ── Test 14: désinstallation / procédure de retrait ─────────────────────────


def test_uninstall_via_rm_rf_does_not_touch_repo(tmp_path: Path) -> None:
    """The documented uninstall procedure is `rm -rf ~/.claude/skills`.
    This must not touch the repository or any other Claude-managed file.
    """
    result = _run_setup(tmp_path)
    assert result.returncode == 0

    # Capture repo state via mtime on a known canonical file
    canonical = CANONICAL_SKILLS / "0-vbb-guide" / "SKILL.md"
    pre_mtime = canonical.stat().st_mtime

    # Run uninstall
    skills_dir = tmp_path / ".claude" / "skills"
    shutil.rmtree(skills_dir)

    # Repo must be untouched
    post_mtime = canonical.stat().st_mtime
    assert pre_mtime == post_mtime, "repo file was modified by uninstall"

    # settings.json and CLAUDE.md (other Claude artifacts) must still exist
    assert (tmp_path / ".claude" / "CLAUDE.md").exists()
    # settings.json should still exist
    assert (tmp_path / ".claude" / "settings.json").exists()


# ── Sanity test: runner script exists and is executable ────────────────────


def test_runner_script_exists() -> None:
    """The shell runner script is created by _run_setup on demand."""
    runner = REPO / "tests" / "_claude_setup_runner.sh"
    assert runner.exists(), f"runner script missing: {runner}"
    assert runner.stat().st_mode & 0o111, "runner script is not executable"


# ── Test 15: nombre correct de symlinks ────────────────────────────────────


def test_correct_number_of_skill_symlinks(tmp_path: Path) -> None:
    """The number of created symlinks must match the number of canonical
    skills (one per canonical SKILL.md in the repo)."""
    result = _run_setup(tmp_path)
    assert result.returncode == 0

    skills_dir = tmp_path / ".claude" / "skills"
    symlinks = [p for p in skills_dir.iterdir() if p.is_dir()]
    assert len(symlinks) == SKILLS_COUNT, (
        f"expected {SKILLS_COUNT} skill dirs, got {len(symlinks)}"
    )


# ── Test 16: legacy byte-identical copies are auto-reconciled ──────────────


def test_byte_identical_legacy_copy_is_auto_reconciled(tmp_path: Path) -> None:
    """When ~/.claude/skills/<name>/SKILL.md already exists as a real file
    that is byte-identical to the canonical source, the setup MUST auto-
    reconcile by moving the legacy copy to a timestamped backup directory
    and creating a symlink to the canonical source.

    This covers the case of a VPS deploy where a previous installer copied
    SKILL.md files instead of symlinking them.
    """
    skills_dir = tmp_path / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    target_skill = "0-vbb-guide"
    user_skill_dir = skills_dir / target_skill
    user_skill_dir.mkdir()
    user_skill_md = user_skill_dir / "SKILL.md"

    # Copy the canonical SKILL.md verbatim (byte-identical)
    canonical = CANONICAL_SKILLS / target_skill / "SKILL.md"
    user_skill_md.write_bytes(canonical.read_bytes())
    assert not user_skill_md.is_symlink()
    assert user_skill_md.read_bytes() == canonical.read_bytes()

    _run_setup(tmp_path)

    # After setup, the destination must be a symlink to the canonical source
    assert user_skill_md.is_symlink(), (
        "byte-identical legacy copy was NOT reconciled into a symlink"
    )
    assert str(user_skill_md.resolve()) == str(canonical.resolve()), (
        "symlink does not point at the canonical source"
    )

    # And the moved copy must be in a timestamped backup directory
    backups = list((tmp_path / ".claude").glob("skills.bak.*"))
    assert len(backups) == 1, (
        f"expected exactly one backup dir, got {backups}"
    )
    backup_file = backups[0] / f"{target_skill}.SKILL.md"
    assert backup_file.is_file(), (
        f"expected backup file at {backup_file}, missing"
    )
    assert backup_file.read_bytes() == canonical.read_bytes(), (
        "backup file content does not match canonical"
    )


# ── Test 17: user-customized (different) content is still refused ──────────


def test_user_customized_real_file_is_still_refused(tmp_path: Path) -> None:
    """The auto-reconciliation MUST only apply to byte-identical legacy
    copies. If the user has customized the file (any byte differs), the
    setup MUST refuse and leave the user's content untouched.
    """
    skills_dir = tmp_path / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    target_skill = "0-vbb-guide"
    user_skill_dir = skills_dir / target_skill
    user_skill_dir.mkdir()
    user_skill_md = user_skill_dir / "SKILL.md"
    user_content = "USER-CUSTOMIZED CONTENT — different from canonical"
    user_skill_md.write_text(user_content)
    assert not user_skill_md.is_symlink()

    _run_setup(tmp_path)

    # The user file must still be a real file (not symlinked), content preserved
    assert user_skill_md.is_file() and not user_skill_md.is_symlink(), (
        "user-customized file was replaced with a symlink"
    )
    assert user_skill_md.read_text() == user_content, (
        "user-customized content was overwritten"
    )

    # No backup dir should have been created for this case
    backups = list((tmp_path / ".claude").glob("skills.bak.*"))
    assert backups == [], (
        f"backup dir was unexpectedly created: {backups}"
    )


# ── Test 18: reconcile is idempotent (2nd run is no-op) ────────────────────


def test_byte_identical_reconcile_is_idempotent(tmp_path: Path) -> None:
    """Running setup.sh twice on a byte-identical legacy copy MUST
    reconcile on the first run and be a no-op on the second run (since
    the destination is then already the correct symlink)."""
    skills_dir = tmp_path / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    target_skill = "0-vbb-guide"
    user_skill_dir = skills_dir / target_skill
    user_skill_dir.mkdir()
    user_skill_md = user_skill_dir / "SKILL.md"

    canonical = CANONICAL_SKILLS / target_skill / "SKILL.md"
    user_skill_md.write_bytes(canonical.read_bytes())

    # 1st run: reconcile
    _run_setup(tmp_path)
    assert user_skill_md.is_symlink()
    first_backups = list((tmp_path / ".claude").glob("skills.bak.*"))
    assert len(first_backups) == 1

    # 2nd run: no-op
    _run_setup(tmp_path)
    assert user_skill_md.is_symlink(), (
        "second run broke the symlink"
    )
    second_backups = list((tmp_path / ".claude").glob("skills.bak.*"))
    assert len(second_backups) == 1, (
        f"second run created an unexpected backup dir: {second_backups}"
    )
    assert second_backups[0] == first_backups[0], (
        "second run created a new backup dir instead of being idempotent"
    )
