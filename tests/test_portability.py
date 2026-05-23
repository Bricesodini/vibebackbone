#!/usr/bin/env python3
"""
Portability smoke test — PR #5 / Lot 5b

Verifies that vbb-project-init + vbb-loop-closure-check work correctly
when operating on a project OUTSIDE the vibebackbone repository.

Scenario:
  1. Create a fresh empty project in a temp directory.
  2. Run vbb-project-init.py on it → governance files created.
  3. Manually create a minimal RAPIDE run (01_INTAKE + 05_EXECUTION + 07_CLOSEOUT)
     with valid frontmatter inside the fresh project.
  4. Run vbb-loop-closure-check.py against that run → must exit 0 (PASS).
  5. Verify that loop-closure-check works even though CWD / VBB_ROOT are
     completely separate from the temp project.

Usage:
    python3 tests/test_portability.py
"""

import sys
import subprocess
import tempfile
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
INIT_TOOL = REPO_ROOT / "tools" / "vbb-project-init.py"
CLOSURE_TOOL = REPO_ROOT / "tools" / "vbb-loop-closure-check.py"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run(tool: Path, args: list, cwd=None):
    """Run a VBB tool with the given args. Returns (rc, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, str(tool)] + args,
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else None,
    )
    return result.returncode, result.stdout, result.stderr


_passed = 0
_failed = 0


def test(name: str, fn) -> None:
    global _passed, _failed
    try:
        fn()
        print(f"  ✓ {name}")
        _passed += 1
    except AssertionError as exc:
        print(f"  ✗ {name}: {exc}")
        _failed += 1


# ---------------------------------------------------------------------------
# Helpers for building minimal run artifacts
# ---------------------------------------------------------------------------

_INTAKE_TMPL = textwrap.dedent("""\
    ---
    run_id: "{run_id}"
    phase: "01_INTAKE"
    voie: "RAPIDE"
    status: "READY"
    agent: "test-runner"
    started_at: "2026-05-23T20:00:00Z"
    ended_at: "2026-05-23T20:01:00Z"
    next_phase: "05_EXECUTION"
    artifacts_consumed: []
    artifacts_produced:
      - "docs/runs/{run_id}/01_INTAKE.md"
    ---

    # 01_INTAKE — portability-smoke-test

    Test run for portability verification.
    """)

_EXECUTION_TMPL = textwrap.dedent("""\
    ---
    run_id: "{run_id}"
    phase: "05_EXECUTION"
    voie: "RAPIDE"
    status: "READY"
    agent: "test-runner"
    started_at: "2026-05-23T20:01:00Z"
    ended_at: "2026-05-23T20:09:00Z"
    next_phase: "07_CLOSEOUT"
    artifacts_consumed:
      - "docs/runs/{run_id}/01_INTAKE.md"
    artifacts_produced:
      - "docs/runs/{run_id}/05_EXECUTION.md"
    ---

    # 05_EXECUTION — portability-smoke-test

    Portability smoke: governance files created in fresh project.
    """)

_CLOSEOUT_TMPL = textwrap.dedent("""\
    ---
    run_id: "{run_id}"
    phase: "07_CLOSEOUT"
    voie: "RAPIDE"
    status: "READY"
    agent: "test-runner"
    started_at: "2026-05-23T20:09:00Z"
    ended_at: "2026-05-23T20:10:00Z"
    next_phase: null
    artifacts_consumed:
      - "docs/runs/{run_id}/05_EXECUTION.md"
    artifacts_produced:
      - "docs/runs/{run_id}/01_INTAKE.md"
      - "docs/runs/{run_id}/05_EXECUTION.md"
      - "docs/runs/{run_id}/07_CLOSEOUT.md"
    ---

    # 07_CLOSEOUT — portability-smoke-test

    ## Résultat

    Portability smoke test passed.
    """)


def _write_run(base: Path, run_id: str) -> None:
    """Write a minimal RAPIDE run (01+05+07) under base/docs/runs/."""
    run_dir = base / "docs" / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    for tmpl, stem in [
        (_INTAKE_TMPL, "01_INTAKE"),
        (_EXECUTION_TMPL, "05_EXECUTION"),
        (_CLOSEOUT_TMPL, "07_CLOSEOUT"),
    ]:
        (run_dir / f"{stem}.md").write_text(tmpl.format(run_id=run_id))


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def _test_init_creates_governance_files():
    """vbb-project-init creates governance files in a fresh external project."""
    with tempfile.TemporaryDirectory() as tmp:
        rc, out, err = _run(INIT_TOOL, ["--target-dir", tmp, "--project-name", "SmokeProj"])
        assert rc == 0, f"Expected exit 0\n{out}\n{err}"
        assert (Path(tmp) / "docs" / "PROJECT_MODE.md").exists(), "PROJECT_MODE.md missing"
        assert (Path(tmp) / "docs" / "CONTEXT.md").exists(), "CONTEXT.md missing"
        assert (Path(tmp) / "docs" / "AUDIT_STATUS.md").exists(), "AUDIT_STATUS.md missing"
        assert (Path(tmp) / "docs" / "INDEX.md").exists(), "INDEX.md missing"
        assert (Path(tmp) / "docs" / "runs" / "README.md").exists(), "runs/README.md missing"


def _test_loop_closure_passes_outside_vbb():
    """loop-closure-check passes on a valid RAPIDE run in a fresh external project."""
    with tempfile.TemporaryDirectory() as tmp:
        # Init governance
        rc_init, _, err = _run(INIT_TOOL, ["--target-dir", tmp])
        assert rc_init == 0, f"Init failed: {err}"

        run_id = "2026-05-23_2000_portability-smoke"
        _write_run(Path(tmp), run_id)

        rc, out, err = _run(
            CLOSURE_TOOL,
            [run_id, "--runs-dir", str(Path(tmp) / "docs" / "runs")],
        )
        assert rc == 0, f"Expected exit 0\n{out}\n{err}"
        assert "PASS" in out, f"Expected PASS in output\n{out}"


def _test_loop_closure_fails_missing_closeout():
    """loop-closure-check fails when 07_CLOSEOUT is absent in external project."""
    with tempfile.TemporaryDirectory() as tmp:
        run_id = "2026-05-23_2000_portability-smoke-bad"
        run_dir = Path(tmp) / "docs" / "runs" / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        # Write only INTAKE — no CLOSEOUT
        (run_dir / "01_INTAKE.md").write_text(
            _INTAKE_TMPL.format(run_id=run_id)
        )
        rc, out, err = _run(
            CLOSURE_TOOL,
            [run_id, "--runs-dir", str(Path(tmp) / "docs" / "runs")],
        )
        assert rc != 0, f"Expected non-zero exit for missing closeout\n{out}\n{err}"


def _test_loop_closure_fails_missing_execution():
    """loop-closure-check fails when 05_EXECUTION is absent (RAPIDE requires it)."""
    with tempfile.TemporaryDirectory() as tmp:
        run_id = "2026-05-23_2000_portability-smoke-no-exec"
        run_dir = Path(tmp) / "docs" / "runs" / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        # Write INTAKE + CLOSEOUT but skip EXECUTION
        (run_dir / "01_INTAKE.md").write_text(
            _INTAKE_TMPL.format(run_id=run_id)
        )
        (run_dir / "07_CLOSEOUT.md").write_text(
            _CLOSEOUT_TMPL.format(run_id=run_id)
        )
        rc, out, err = _run(
            CLOSURE_TOOL,
            [run_id, "--runs-dir", str(Path(tmp) / "docs" / "runs")],
        )
        assert rc != 0, f"Expected non-zero exit for missing 05_EXECUTION\n{out}\n{err}"


def _test_init_idempotent_outside_vbb():
    """Running vbb-project-init twice on an external project is idempotent."""
    with tempfile.TemporaryDirectory() as tmp:
        rc1, _, _ = _run(INIT_TOOL, ["--target-dir", tmp])
        assert rc1 == 0, "First init failed"

        rc2, out2, _ = _run(INIT_TOOL, ["--target-dir", tmp])
        assert rc2 == 0, "Second init failed"

        assert "skipped" in out2.lower() or "SKIP" in out2, (
            f"Second run should report all files skipped\n{out2}"
        )


def _test_init_dry_run_outside_vbb():
    """--dry-run on fresh external dir writes nothing."""
    with tempfile.TemporaryDirectory() as tmp:
        rc, out, _ = _run(INIT_TOOL, ["--target-dir", tmp, "--dry-run"])
        assert rc == 0
        assert not (Path(tmp) / "docs").exists(), (
            "docs/ should not be created during --dry-run"
        )
        assert "CREATE" in out or "PROJECT_MODE.md" in out, (
            f"--dry-run should print intended actions\n{out}"
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=== VBB Portability Smoke Test ===")
    print()

    print("Project init (external project):")
    test("vbb-project-init creates governance files", _test_init_creates_governance_files)
    test("vbb-project-init is idempotent outside VBB", _test_init_idempotent_outside_vbb)
    test("vbb-project-init --dry-run writes nothing", _test_init_dry_run_outside_vbb)

    print()
    print("Loop closure (external project):")
    test("loop-closure-check PASS on valid RAPIDE run", _test_loop_closure_passes_outside_vbb)
    test("loop-closure-check FAIL when 07_CLOSEOUT missing", _test_loop_closure_fails_missing_closeout)
    test("loop-closure-check FAIL when 05_EXECUTION missing", _test_loop_closure_fails_missing_execution)

    print()
    total = _passed + _failed
    print(f"Results: {_passed}/{total} passed, {_failed} failed")
    return 0 if _failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
