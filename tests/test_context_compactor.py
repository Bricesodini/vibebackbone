#!/usr/bin/env python3
"""
Tests for tools/vbb-context-compactor.py

Positive tests:
  1. Valid run → summary generated with all sections
  2. --stdout works
  3. --output works with custom path
  4. Summary contains expected sections

Negative tests:
  5. Non-existent run → error + exit 1
  6. Empty directory → error + exit 1
  7. Run with minimal artifacts still works

Usage:
    pytest tests/test_context_compactor.py -q
    python3 tests/test_context_compactor.py
"""

import sys
import subprocess
import tempfile
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
TOOL = REPO_ROOT / "tools" / "vbb-context-compactor.py"


def _run_compactor(args: list) -> tuple:
    """Run the compactor and return (rc, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, str(TOOL)] + args, capture_output=True, text=True
    )
    return result.returncode, result.stdout, result.stderr


# --- Fixtures ---

VALID_CLOSEOUT = textwrap.dedent("""\
    ---
    run_id: "2026-01-01_1000_test"
    phase: "07_CLOSEOUT"
    voie: "STRUCTUREE"
    status: "READY"
    agent: "claude-code"
    started_at: "2026-01-01T10:00:00Z"
    ended_at: "2026-01-01T10:30:00Z"
    artifacts_produced: []
    ---

    # 07_CLOSEOUT — Test Run

    **Date** : 2026-01-01
    **Voie** : STRUCTURÉE
    **Verdict** : ✅ PASS

    ## Résumé

    Test run for compactor validation.

    ## Décisions

    - Decision 1: use Python 3.11
    - Decision 2: no dashboard

    ## Risques résiduels

    - Risk A: incomplete coverage
    - Risk B: no negative tests

    ## Prochaine action

    RUN 11 — Dashboard status terminal
""")

VALID_INTAKE = textwrap.dedent("""\
    ---
    run_id: "2026-01-01_1000_test"
    phase: "01_INTAKE"
    voie: "STRUCTUREE"
    status: "READY"
    agent: "claude-code"
    started_at: "2026-01-01T10:00:00Z"
    ended_at: "2026-01-01T10:30:00Z"
    artifacts_produced: []
    ---

    # 01_INTAKE

    ## Objectif

    Validate the context compactor tool.
    It should produce a short, reliable summary.

    ## Scope

    - tools/vbb-context-compactor.py
    - tests/test_context_compactor.py
""")


# --- Tests ---


def test_valid_run_summary():
    """Valid run → summary generated with all expected sections."""
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "2026-01-01_1000_test"
        run_dir.mkdir()
        (run_dir / "01_INTAKE.md").write_text(VALID_INTAKE)
        (run_dir / "07_CLOSEOUT.md").write_text(VALID_CLOSEOUT)

        rc, out, err = _run_compactor([str(run_dir)])
        assert rc == 0, f"Expected exit 0, got {rc}\n{err}"
        summary_path = run_dir / "CONTEXT_SUMMARY.md"
        assert summary_path.exists(), f"Summary not created\n{out}{err}"

        content = summary_path.read_text()
        for section in [
            "Objective",
            "Current status",
            "Decisions",
            "Files changed",
            "Risks",
            "Next action",
            "Re-entry prompt",
        ]:
            assert f"## {section}" in content, f"Missing section: {section}"


def test_stdout_mode():
    """--stdout prints summary to stdout."""
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "2026-01-01_1000_test"
        run_dir.mkdir()
        (run_dir / "07_CLOSEOUT.md").write_text(VALID_CLOSEOUT)

        rc, out, err = _run_compactor([str(run_dir), "--stdout"])
        assert rc == 0, f"Expected exit 0, got {rc}\n{err}"
        assert "Context Summary" in out, f"Expected 'Context Summary' in stdout\n{out}"
        # File should NOT be created
        assert not (run_dir / "CONTEXT_SUMMARY.md").exists(), (
            "Summary file should not exist in --stdout mode"
        )


def test_output_flag():
    """--output writes to custom path."""
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "2026-01-01_1000_test"
        run_dir.mkdir()
        (run_dir / "07_CLOSEOUT.md").write_text(VALID_CLOSEOUT)

        custom_output = Path(tmp) / "custom_summary.md"
        rc, out, err = _run_compactor([str(run_dir), "--output", str(custom_output)])
        assert rc == 0, f"Expected exit 0, got {rc}\n{err}"
        assert custom_output.exists(), f"Custom output not created\n{out}{err}"
        content = custom_output.read_text()
        assert "Context Summary" in content


def test_run_id_in_summary():
    """Summary contains run_id from frontmatter."""
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "2026-01-01_1000_test"
        run_dir.mkdir()
        (run_dir / "07_CLOSEOUT.md").write_text(VALID_CLOSEOUT)

        rc, out, _ = _run_compactor([str(run_dir), "--stdout"])
        assert rc == 0
        assert "2026-01-01_1000_test" in out, "Expected run_id in summary"


def test_reentry_prompt():
    """Summary contains a usable re-entry prompt."""
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "2026-01-01_1000_test"
        run_dir.mkdir()
        (run_dir / "07_CLOSEOUT.md").write_text(VALID_CLOSEOUT)

        rc, out, _ = _run_compactor([str(run_dir), "--stdout"])
        assert rc == 0
        assert "Re-entry prompt" in out
        assert "Reprise" in out or "2026-01-01" in out


def test_nonexistent_run():
    """Non-existent run → error + exit 1."""
    rc, out, err = _run_compactor(["/nonexistent/path/2026-01-01_fake"])
    assert rc == 1, f"Expected exit 1, got {rc}"
    assert "not found" in err.lower() or "not found" in out.lower(), (
        f"Expected 'not found' in output\n{out}\n{err}"
    )


def test_empty_directory():
    """Empty directory → error + exit 1."""
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "empty_run"
        run_dir.mkdir()
        rc, out, err = _run_compactor([str(run_dir)])
        assert rc == 1, f"Expected exit 1, got {rc}"
        assert (
            "no markdown" in err.lower() or "no markdown" in out.lower() or rc == 1
        ), f"Expected error about no files\n{out}\n{err}"


def test_minimal_run():
    """Run with only 07_CLOSEOUT still produces valid summary."""
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "2026-01-01_1000_minimal"
        run_dir.mkdir()
        (run_dir / "07_CLOSEOUT.md").write_text(VALID_CLOSEOUT)

        rc, out, err = _run_compactor([str(run_dir), "--stdout"])
        assert rc == 0, f"Expected exit 0, got {rc}\n{err}"
        assert "Context Summary" in out


def test_real_run():
    """Dogfood: compact a real run from the repo."""
    # Find an existing run with closeout
    runs_dir = REPO_ROOT / "docs" / "runs"
    if runs_dir.exists():
        candidates = [
            d
            for d in runs_dir.iterdir()
            if d.is_dir() and (d / "07_CLOSEOUT.md").exists()
        ]
        if candidates:
            run = candidates[0]
            rc, out, err = _run_compactor([str(run), "--stdout"])
            assert rc == 0, f"Expected exit 0 for real run {run.name}, got {rc}\n{err}"
            assert "Context Summary" in out
            assert "## Objective" in out


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
