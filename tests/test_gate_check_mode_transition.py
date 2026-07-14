#!/usr/bin/env python3
"""
Tests for Phase 2 Run 1 extension to tools/vbb-gate-check.py

Covers P0-5-A §4.6 — check_mode_transition:
  - intake with no mode-transition keyword → NOT_NEEDED
  - intake with mode-transition keyword + no PROJECT_MODE.md → SKIPPED_NO_PROJECT_MODE
  - intake with mode-transition keyword + PROJECT_MODE.md present → RECOMMENDED

Usage:
    pytest tests/test_gate_check_mode_transition.py -q
"""

import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
TOOL = REPO_ROOT / "tools" / "vbb-gate-check.py"
PYTHON = sys.executable


_INTAKE_FM = textwrap.dedent("""\
    ---
    run_id: "{run_id}"
    phase: "01_INTAKE"
    voie: "STRUCTUREE"
    status: "READY"
    agent: "claude-code"
    started_at: "2026-05-23T10:00:00Z"
    ended_at: "2026-05-23T10:30:00Z"
    next_phase: "04_PLAN"
    artifacts_consumed: []
    artifacts_produced: []
    ---

    # 01_INTAKE

    {body}
""")


def _make_intake(tmp: Path, run_id: str, body: str) -> Path:
    run_dir = tmp / run_id
    run_dir.mkdir()
    (run_dir / "01_INTAKE.md").write_text(_INTAKE_FM.format(run_id=run_id, body=body))
    return run_dir


def _invoke(run_dir: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PYTHON, str(TOOL), str(run_dir), "--json"],
        capture_output=True,
        text=True,
    )


def test_mode_transition_not_needed() -> None:
    """No deploy / prod / migration keyword → status=NOT_NEEDED."""
    with tempfile.TemporaryDirectory() as tmp:
        # NB: run_id must NOT contain "deploy", "prod", "migration" or any
        # mode-transition keyword — the regex is applied to the whole
        # intake including frontmatter.
        run_dir = _make_intake(
            Path(tmp),
            "2026-06-13_1210_no_keywords",
            "## Objectif\n\nRefactor a helper function.",
        )
        proc = _invoke(run_dir)
        assert proc.returncode == 0, f"unexpected fail: {proc.stderr}"
        assert "NOT_NEEDED" in proc.stdout, (
            f"expected NOT_NEEDED, got stdout: {proc.stdout}"
        )


def test_mode_transition_skipped_without_project_mode() -> None:
    """Keyword present but no PROJECT_MODE.md → status=SKIPPED_NO_PROJECT_MODE.

    This vibebackbone repo doesn't have docs/PROJECT_MODE.md, so any
    deploy/migration keyword should be SKIPPED, not RECOMMENDED.
    """
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = _make_intake(
            Path(tmp),
            "2026-06-13_1211_kw_no_pm",
            "## Objectif\n\nPush the helper to staging.",
        )
        # Sanity: PROJECT_MODE.md must not exist for this test to be valid.
        project_mode = REPO_ROOT / "docs" / "PROJECT_MODE.md"
        if project_mode.exists():
            import pytest

            pytest.skip(
                "docs/PROJECT_MODE.md exists in this repo — cannot test SKIPPED state"
            )
        proc = _invoke(run_dir)
        assert proc.returncode == 0, f"unexpected fail: {proc.stderr}"
        assert "SKIPPED_NO_PROJECT_MODE" in proc.stdout, (
            f"expected SKIPPED_NO_PROJECT_MODE, got stdout: {proc.stdout}"
        )


def test_mode_transition_recommended_with_project_mode(
    tmp_path: Path, monkeypatch
) -> None:
    """Keyword present AND PROJECT_MODE.md present → status=RECOMMENDED.

    We simulate PROJECT_MODE.md by creating a temp file and using --runs-dir
    isn't enough; the tool resolves PROJECT_MODE.md from REPO_ROOT. So we
    use a different approach: verify the RECOMMENDED code path via direct
    function call with a stubbed REPO_ROOT, OR verify the function logic
    via import. We pick the import path for stability.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location("vbb_gate_check_test", str(TOOL))
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)

    # Build a fake REPO_ROOT that has docs/PROJECT_MODE.md
    fake_root = tmp_path / "fake_repo"
    fake_root.mkdir()
    (fake_root / "docs").mkdir()
    (fake_root / "docs" / "PROJECT_MODE.md").write_text("# mode")

    # Patch REPO_ROOT inside the module
    monkeypatch.setattr(mod, "REPO_ROOT", fake_root)

    # Build a run_dir with intake that triggers the keyword
    run_dir = tmp_path / "2026-06-13_1212_recommended"
    run_dir.mkdir()
    (run_dir / "01_INTAKE.md").write_text(
        _INTAKE_FM.format(
            run_id="2026-06-13_1212_recommended",
            body="## Objectif\n\nDeploy to production.",
        )
    )

    result = mod.check_mode_transition(run_dir)
    assert result["status"] == "RECOMMENDED", f"expected RECOMMENDED, got: {result}"
    assert result["skill"] == "t-vbb-mode-transition-gate", (
        f"expected t-vbb-mode-transition-gate, got: {result}"
    )


if __name__ == "__main__":
    test_mode_transition_not_needed()
    test_mode_transition_skipped_without_project_mode()
    # the recommended test relies on pytest monkeypatch; skip in direct mode
    print("OK — 2 tests passed (the 3rd requires pytest monkeypatch)")
