#!/usr/bin/env python3
"""
Tests for tools/vbb-project-init.py

Positive tests (exit 0):
  1. Fresh project — all files created
  2. --dry-run — no files written, report printed
  3. --project-name — appears in CONTEXT.md
  4. --mode PROD — appears in PROJECT_MODE.md
  5. Templates copied from VBB distribution

Negative-ish tests (idempotency and overwrite):
  6. Existing file skipped (idempotent)
  7. --overwrite rewrites existing file
  8. .gitignore updated idempotently (no duplicates)

Bootstrap guard:
  9. Non-existent target dir → exit 1

Usage:
    pytest tests/test_project_init.py -q
    python3 tests/test_project_init.py
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
TOOL = REPO_ROOT / "tools" / "vbb-project-init.py"
TEMPLATES_SRC = REPO_ROOT / "docs" / "templates"
MANAGED_BUNDLE_TARGETS = (
    "scripts/install-vbb-hooks.sh",
    "scripts/hooks/pre-commit-framework-gate",
    "scripts/hooks/commit-msg-framework-gate",
    "tools/vbb-credentials-gate.py",
    "tools/vbb-loop-closure-check.py",
    "tools/vbb_run_resolution.py",
    ".vbb/requirements.txt",
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run(args: list, cwd=None):
    """Run vbb-project-init.py with given args. Returns (rc, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, str(TOOL)] + args,
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else None,
    )
    return result.returncode, result.stdout, result.stderr


def _git_init(path: Path):
    subprocess.run(["git", "init", "-q", str(path)], check=True)


# ---------------------------------------------------------------------------
# Positive tests
# ---------------------------------------------------------------------------

def test_fresh_project():
    """All governance files created in an empty directory."""
    with tempfile.TemporaryDirectory() as tmp:
        rc, out, err = _run(["--target-dir", tmp, "--project-name", "TestProj"])
        assert rc == 0, f"Expected exit 0\n{out}\n{err}"
        assert "docs/PROJECT_MODE.md" in out
        assert "docs/CONTEXT.md" in out
        assert "docs/AUDIT_STATUS.md" in out
        assert "docs/ARCHITECTURE.md" in out
        assert "docs/RELATIONS.md" in out
        assert "docs/INDEX.md" in out
        assert "docs/runs/README.md" in out
        assert "docs/audits/README.md" in out
        assert "docs/adr/README.md" in out
        # Verify files actually exist
        assert (Path(tmp) / "docs" / "PROJECT_MODE.md").exists()
        assert (Path(tmp) / "docs" / "CONTEXT.md").exists()
        assert (Path(tmp) / "docs" / "AUDIT_STATUS.md").exists()
        assert (Path(tmp) / "docs" / "ARCHITECTURE.md").exists()
        assert (Path(tmp) / "docs" / "RELATIONS.md").exists()


def test_dry_run_no_write():
    """--dry-run prints plan but writes nothing."""
    with tempfile.TemporaryDirectory() as tmp:
        rc, out, err = _run(["--target-dir", tmp, "--dry-run"])
        assert rc == 0, f"Expected exit 0\n{out}\n{err}"
        # Nothing written
        assert not (Path(tmp) / "docs").exists(), "docs/ should not be created in dry-run"
        # But output shows what would be created
        assert "CREATE" in out or "docs/PROJECT_MODE.md" in out


def test_project_name_in_context():
    """--project-name appears in CONTEXT.md."""
    with tempfile.TemporaryDirectory() as tmp:
        rc, out, err = _run(["--target-dir", tmp, "--project-name", "MyAwesomeProject"])
        assert rc == 0
        context = (Path(tmp) / "docs" / "CONTEXT.md").read_text()
        assert "MyAwesomeProject" in context, f"Project name not found in CONTEXT.md:\n{context[:300]}"


def test_mode_prod_in_project_mode():
    """--mode PROD appears in PROJECT_MODE.md."""
    with tempfile.TemporaryDirectory() as tmp:
        rc, out, err = _run(["--target-dir", tmp, "--mode", "PROD"])
        assert rc == 0
        pm = (Path(tmp) / "docs" / "PROJECT_MODE.md").read_text()
        assert "PROD" in pm, f"Mode PROD not found in PROJECT_MODE.md:\n{pm[:300]}"


def test_templates_copied():
    """7 phase templates are copied to docs/templates/."""
    with tempfile.TemporaryDirectory() as tmp:
        if not TEMPLATES_SRC.exists():
            # Skip if running outside VBB distribution
            return
        rc, out, err = _run(["--target-dir", tmp])
        assert rc == 0
        tpl_dir = Path(tmp) / "docs" / "templates"
        assert tpl_dir.exists(), "docs/templates/ not created"
        copied = list(tpl_dir.glob("*.md.template"))
        src_count = len(list(TEMPLATES_SRC.glob("*.md.template")))
        assert len(copied) == src_count, (
            f"Expected {src_count} templates, got {len(copied)}: {[t.name for t in copied]}"
        )


def test_architecture_initialized_as_fresh_state():
    """Fresh projects get their own architecture source, not VBB audit history."""
    with tempfile.TemporaryDirectory() as tmp:
        rc, out, err = _run(["--target-dir", tmp, "--project-name", "FreshImpl"])
        assert rc == 0, f"Expected exit 0\n{out}\n{err}"
        arch = (Path(tmp) / "docs" / "ARCHITECTURE.md").read_text()
        relations = (Path(tmp) / "docs" / "RELATIONS.md").read_text()
        assert "FreshImpl" in arch
        assert "Project Core" in arch
        assert "global-implementation-readiness" not in arch
        assert "source: ARCHITECTURE.md" in relations


def test_install_hook_copies_complete_managed_bundle():
    """--install-hook installs runnable canonical hooks and their sources."""
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)
        _git_init(target)

        rc, out, err = _run(["--target-dir", tmp, "--install-hook"])
        assert rc == 0, f"Expected exit 0\n{out}\n{err}"
        for rel in MANAGED_BUNDLE_TARGETS:
            assert (target / rel).is_file(), f"Missing managed target: {rel}"
        assert (target / ".git/hooks/pre-commit").is_file()
        assert (target / ".git/hooks/commit-msg").is_file()

        manifest = json.loads((target / ".vbb/managed-files.json").read_text())
        assert manifest["schema_version"] == 1
        assert manifest["owner"] == "vibebackbone"
        assert set(manifest["files"]) == set(MANAGED_BUNDLE_TARGETS)

        readme = target / "README.md"
        readme.write_text("consumer smoke test\n")
        subprocess.run(["git", "-C", tmp, "add", "README.md"], check=True)
        hook = subprocess.run(
            [str(target / ".git/hooks/pre-commit")],
            cwd=tmp,
            capture_output=True,
            text=True,
        )
        assert hook.returncode == 0, f"Hook failed\n{hook.stdout}\n{hook.stderr}"


def test_managed_bundle_refresh_is_idempotent():
    """An unchanged managed bundle can be refreshed with explicit hook replacement."""
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)
        _git_init(target)
        assert _run(["--target-dir", tmp, "--install-hook"])[0] == 0
        manifest = target / ".vbb/managed-files.json"
        before = manifest.read_text()
        context = target / "docs/CONTEXT.md"
        context.write_text("PROJECT_TRUTH_SENTINEL\n")

        rc, out, err = _run(
            ["--target-dir", tmp, "--install-hook", "--overwrite-hook"]
        )
        assert rc == 0, f"Expected exit 0\n{out}\n{err}"
        assert manifest.read_text() == before
        assert context.read_text() == "PROJECT_TRUTH_SENTINEL\n"


def test_customized_managed_asset_blocks_without_partial_copy():
    """A local customization is preserved and stops the whole bundle preflight."""
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)
        _git_init(target)
        assert _run(["--target-dir", tmp, "--install-hook"])[0] == 0
        custom = target / "scripts/hooks/pre-commit-framework-gate"
        custom.write_text(custom.read_text() + "\n# LOCAL_SENTINEL\n")
        untouched = target / "tools/vbb-credentials-gate.py"
        untouched_before = untouched.read_bytes()

        rc, out, err = _run(
            ["--target-dir", tmp, "--install-hook", "--overwrite-hook"]
        )
        assert rc == 1, f"Expected exit 1\n{out}\n{err}"
        assert "was customized" in err
        assert "LOCAL_SENTINEL" in custom.read_text()
        assert untouched.read_bytes() == untouched_before


def test_overwrite_managed_is_separate_from_hook_overwrite():
    """Replacing managed assets requires its own explicit flag."""
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)
        _git_init(target)
        assert _run(["--target-dir", tmp, "--install-hook"])[0] == 0
        custom = target / "tools/vbb-credentials-gate.py"
        custom.write_text("# LOCAL_SENTINEL\n")

        rc, out, err = _run(
            [
                "--target-dir", tmp,
                "--install-hook",
                "--overwrite-hook",
                "--overwrite-managed",
            ]
        )
        assert rc == 0, f"Expected exit 0\n{out}\n{err}"
        assert "LOCAL_SENTINEL" not in custom.read_text()


def test_existing_foreign_hook_is_preserved_by_document_overwrite():
    """--overwrite never grants permission to replace Git hooks."""
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)
        _git_init(target)
        hook = target / ".git/hooks/pre-commit"
        hook.write_text("#!/bin/sh\necho foreign\n")

        rc, out, err = _run(
            ["--target-dir", tmp, "--overwrite", "--install-hook"]
        )
        assert rc == 1, f"Expected exit 1\n{out}\n{err}"
        assert hook.read_text() == "#!/bin/sh\necho foreign\n"
        assert "--overwrite-hook" in err
        assert not (target / ".vbb/managed-files.json").exists()


def test_unmanaged_bundle_target_requires_explicit_adoption():
    """A pre-existing runtime source is not silently claimed by VBB."""
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)
        _git_init(target)
        unmanaged = target / "tools/vbb-credentials-gate.py"
        unmanaged.parent.mkdir()
        unmanaged.write_text("# PROJECT_OWNED_SENTINEL\n")

        rc, out, err = _run(["--target-dir", tmp, "--install-hook"])
        assert rc == 1, f"Expected exit 1\n{out}\n{err}"
        assert "unmanaged target exists" in err
        assert "--overwrite-managed" in err
        assert unmanaged.read_text() == "# PROJECT_OWNED_SENTINEL\n"
        assert not (target / ".vbb/managed-files.json").exists()


def test_install_hook_dry_run_writes_no_bundle_or_hooks():
    """Hook dry-run reports the bundle plan without writing runtime files."""
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)
        _git_init(target)

        rc, out, err = _run(
            ["--target-dir", tmp, "--install-hook", "--dry-run"]
        )
        assert rc == 0, f"Expected exit 0\n{out}\n{err}"
        assert "would sync" in out
        assert not (target / ".vbb").exists()
        assert not (target / ".git/hooks/pre-commit").exists()


def test_install_hook_failure_is_an_error():
    """A non-Git target cannot report hook installation as a successful skip."""
    with tempfile.TemporaryDirectory() as tmp:
        rc, out, err = _run(["--target-dir", tmp, "--install-hook"])
        assert rc == 1, f"Expected exit 1\n{out}\n{err}"
        assert "Cannot install managed hooks" in err
        assert "governance bootstrapped" not in out


# ---------------------------------------------------------------------------
# Idempotency and overwrite tests
# ---------------------------------------------------------------------------

def test_existing_file_skipped():
    """Existing file is reported as skipped, not overwritten."""
    with tempfile.TemporaryDirectory() as tmp:
        # Pre-create PROJECT_MODE.md with custom content
        docs = Path(tmp) / "docs"
        docs.mkdir()
        pm = docs / "PROJECT_MODE.md"
        pm.write_text("# My custom content\n")

        rc, out, err = _run(["--target-dir", tmp])
        assert rc == 0

        # File content must be unchanged
        assert pm.read_text() == "# My custom content\n", (
            "Existing file was overwritten without --overwrite flag"
        )
        # Must appear in skipped list
        assert "skipped" in out.lower() or "SKIP" in out, (
            f"Expected 'skipped' in output\n{out}"
        )


def test_overwrite_rewrites_file():
    """--overwrite replaces existing files."""
    with tempfile.TemporaryDirectory() as tmp:
        docs = Path(tmp) / "docs"
        docs.mkdir()
        pm = docs / "PROJECT_MODE.md"
        pm.write_text("# Old content\n")

        rc, out, err = _run(["--target-dir", tmp, "--overwrite"])
        assert rc == 0

        new_content = pm.read_text()
        assert "Old content" not in new_content, "File was not overwritten with --overwrite"
        assert "Mode actuel" in new_content, f"Expected VBB content in overwritten file:\n{new_content[:200]}"


def test_gitignore_idempotent():
    """Running init twice doesn't duplicate .gitignore entries."""
    with tempfile.TemporaryDirectory() as tmp:
        # First run
        rc1, _, _ = _run(["--target-dir", tmp])
        assert rc1 == 0

        # Second run
        rc2, out2, _ = _run(["--target-dir", tmp])
        assert rc2 == 0

        gi = Path(tmp) / ".gitignore"
        if gi.exists():
            content = gi.read_text()
            count = content.count("docs/SESSION.md")
            assert count <= 1, f".gitignore has {count} occurrences of SESSION.md (expected ≤ 1)"
        # Whether .gitignore was created or the entry was skipped is both valid
        assert "SESSION.md" in out2 or "already" in out2 or "SKIP" in out2, (
            f"Second run should note SESSION.md entries already present\n{out2}"
        )


# ---------------------------------------------------------------------------
# Bootstrap guard
# ---------------------------------------------------------------------------

def test_nonexistent_target():
    """Non-existent --target-dir → exit 1."""
    rc, out, err = _run(["--target-dir", "/nonexistent/path/that/does/not/exist"])
    assert rc == 1, f"Expected exit 1, got {rc}"


# ---------------------------------------------------------------------------
# Dogfood: running on VBB itself (all files exist → all skipped)
# ---------------------------------------------------------------------------

def test_dogfood_vbb_skips_all():
    """Running init on the VBB repo itself skips all existing files."""
    rc, out, err = _run(["--target-dir", str(REPO_ROOT)])
    assert rc == 0, f"Expected exit 0\n{out}\n{err}"
    # PROJECT_MODE.md, CONTEXT.md, etc. all exist → skipped
    assert "skipped" in out.lower() or "SKIP" in out, (
        f"Expected some files to be skipped on VBB itself\n{out}"
    )

# --- Direct execution fallback ---

if __name__ == "__main__":
    try:
        import pytest
        sys.exit(pytest.main([__file__, "-q"]))
    except ImportError:
        passed = failed = 0
        for _name, _fn in sorted(globals().items()):
            if _name.startswith("test_") and callable(_fn):
                try:
                    _fn()
                    print("  PASS " + _name)
                    passed += 1
                except AssertionError as _e:
                    print("  FAIL " + _name + ": " + str(_e))
                    failed += 1
        total = passed + failed
        print("Results: %d/%d passed, %d failed" % (passed, total, failed))
        sys.exit(0 if failed == 0 else 1)
