#!/usr/bin/env python3
"""
Tests for tools/vbb-loop-closure-check.py

Positive tests (exit 0):
  1. RAPIDE  : 01_INTAKE + 05_EXECUTION + 07_CLOSEOUT
  2. STRUCTUREE : 01_INTAKE + 04_PLAN + 05_EXECUTION + 07_CLOSEOUT
  3. AUDIT   : 01_INTAKE + 02_AUDIT + 03_DECISION + 07_CLOSEOUT
  4. CLOTURE : 07_CLOSEOUT only (no 01_INTAKE)
  5. RAPIDE-ZERO : closeout with voie=RAPIDE-ZERO → PASS (no phases required)
  6. RAPIDE-MINIMAL : 05_PATCH_SUMMARY only → PASS

Negative tests (exit 1):
  7. Missing 07_CLOSEOUT
  8. Missing required phase for voie (STRUCTUREE without 04_PLAN)
  9. Missing 01_INTAKE for non-CLOTURE voie
  10. Frontmatter missing required field
  11. Frontmatter placeholder not replaced
  12. Run directory not found
  13. Invalid voie value

Usage:
    pytest tests/test_loop_closure.py -q
    python3 tests/test_loop_closure.py
"""

import sys
import subprocess
import tempfile
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
TOOL = REPO_ROOT / "tools" / "vbb-loop-closure-check.py"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_VALID_FM = textwrap.dedent("""\
    ---
    run_id: "{run_id}"
    phase: "{phase}"
    voie: "{voie}"
    status: "READY"
    agent: "claude-code"
    started_at: "2026-05-23T10:00:00Z"
    ended_at: "2026-05-23T10:30:00Z"
    next_phase: null
    artifacts_consumed: []
    artifacts_produced: []
    ---

    # {phase}
""")


def _make_artifact(path: Path, run_id: str, phase: str, voie: str) -> None:
    path.write_text(_VALID_FM.format(run_id=run_id, phase=phase, voie=voie))


def _run(run_id: str, runs_dir: Path, extra_args=None):
    """Invoke vbb-loop-closure-check.py and return (returncode, stdout, stderr)."""
    cmd = [sys.executable, str(TOOL)]
    if extra_args:
        cmd.extend(extra_args)
    cmd.extend([run_id, "--runs-dir", str(runs_dir)])
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


# ---------------------------------------------------------------------------
# Positive tests
# ---------------------------------------------------------------------------

def test_rapide_complete():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_rapide"
        d.mkdir()
        rid = "2026-01-01_1000_rapide"
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, f"Expected exit 0, got {rc}\n{out}"
        assert "PASS" in out, f"Expected PASS in output\n{out}"


def test_structuree_complete():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_struct"
        d.mkdir()
        rid = "2026-01-01_1000_struct"
        for phase in ["01_INTAKE", "04_PLAN", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "STRUCTUREE")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, f"Expected exit 0, got {rc}\n{out}"
        assert "PASS" in out


def test_audit_complete():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_audit"
        d.mkdir()
        rid = "2026-01-01_1000_audit"
        for phase in ["01_INTAKE", "02_AUDIT", "03_DECISION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "AUDIT")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, f"Expected exit 0, got {rc}\n{out}"
        assert "PASS" in out


def test_cloture_complete():
    """CLOTURE voie: only 07_CLOSEOUT required, no 01_INTAKE."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_cloture"
        d.mkdir()
        rid = "2026-01-01_1000_cloture"
        _make_artifact(d / "07_CLOSEOUT.md", rid, "07_CLOSEOUT", "CLOTURE")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, f"Expected exit 0, got {rc}\n{out}"
        assert "PASS" in out


def test_rapide_zero():
    """RAPIDE-ZERO voie: closeout with voie=RAPIDE-ZERO → PASS (no required phases)."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_zero"
        d.mkdir()
        rid = "2026-01-01_1000_zero"
        # RAPIDE-ZERO only needs a closeout with the voie set
        _make_artifact(d / "07_CLOSEOUT.md", rid, "07_CLOSEOUT", "RAPIDE-ZERO")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, f"Expected exit 0, got {rc}\n{out}"
        assert "PASS" in out
        assert "RAPIDE-ZERO" in out


def test_rapide_minimal():
    """RAPIDE-MINIMAL voie: 05_PATCH_SUMMARY only → PASS."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_minimal"
        d.mkdir()
        rid = "2026-01-01_1000_minimal"
        patch = textwrap.dedent(f"""\
            ---
            run_id: "{rid}"
            phase: "05_PATCH_SUMMARY"
            voie: "RAPIDE-MINIMAL"
            status: "DONE"
            agent: "claude-code"
            started_at: "2026-05-23T10:00:00Z"
            ended_at: "2026-05-23T10:30:00Z"
            artifacts_produced: []
            ---

            # Patch Summary
        """)
        (d / "05_PATCH_SUMMARY.md").write_text(patch)
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 0, f"Expected exit 0, got {rc}\n{out}"
        assert "PASS" in out
        assert "RAPIDE-MINIMAL" in out


# ---------------------------------------------------------------------------
# Negative tests
# ---------------------------------------------------------------------------

def test_missing_closeout():
    """RAPIDE run missing 07_CLOSEOUT → FAIL."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_no-closeout"
        d.mkdir()
        rid = "2026-01-01_1000_no-closeout"
        _make_artifact(d / "01_INTAKE.md", rid, "01_INTAKE", "RAPIDE")
        _make_artifact(d / "05_EXECUTION.md", rid, "05_EXECUTION", "RAPIDE")
        # 07_CLOSEOUT.md intentionally absent
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, f"Expected exit 1, got {rc}"
        assert "FAIL" in out, f"Expected FAIL in output\n{out}"
        assert "07_CLOSEOUT" in out, f"Expected '07_CLOSEOUT' mentioned\n{out}"


def test_missing_required_phase():
    """STRUCTUREE run missing 04_PLAN → FAIL with 04_PLAN in error."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_no-plan"
        d.mkdir()
        rid = "2026-01-01_1000_no-plan"
        # 04_PLAN intentionally absent
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "STRUCTUREE")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, f"Expected exit 1, got {rc}"
        assert "FAIL" in out, f"Expected FAIL\n{out}"
        assert "04_PLAN" in out, f"Expected '04_PLAN' in error output\n{out}"


def test_missing_intake_non_cloture():
    """RAPIDE run without 01_INTAKE → FAIL even if 07_CLOSEOUT exists."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_no-intake"
        d.mkdir()
        rid = "2026-01-01_1000_no-intake"
        # 07_CLOSEOUT has voie=RAPIDE — not CLOTURE, so 01_INTAKE is required
        _make_artifact(d / "05_EXECUTION.md", rid, "05_EXECUTION", "RAPIDE")
        _make_artifact(d / "07_CLOSEOUT.md", rid, "07_CLOSEOUT", "RAPIDE")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, f"Expected exit 1, got {rc}"
        assert "FAIL" in out
        assert "01_INTAKE" in out, f"Expected '01_INTAKE' in error\n{out}"


def test_missing_frontmatter_field():
    """07_CLOSEOUT.md missing required field 'status' → FAIL."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_bad-fm"
        d.mkdir()
        rid = "2026-01-01_1000_bad-fm"
        _make_artifact(d / "01_INTAKE.md", rid, "01_INTAKE", "RAPIDE")
        _make_artifact(d / "05_EXECUTION.md", rid, "05_EXECUTION", "RAPIDE")
        # closeout without 'status'
        bad = textwrap.dedent(f"""\
            ---
            run_id: "{rid}"
            phase: "07_CLOSEOUT"
            voie: "RAPIDE"
            agent: "claude-code"
            started_at: "2026-05-23T10:00:00Z"
            ended_at: "2026-05-23T10:30:00Z"
            artifacts_produced: []
            ---

            # Closeout
        """)
        (d / "07_CLOSEOUT.md").write_text(bad)
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, f"Expected exit 1, got {rc}"
        assert "FAIL" in out
        assert "status" in out, f"Expected 'status' mentioned in error\n{out}"


def test_placeholder_not_replaced():
    """07_CLOSEOUT.md with <placeholder> values → FAIL."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_placeholder"
        d.mkdir()
        rid = "2026-01-01_1000_placeholder"
        placeholder = textwrap.dedent("""\
            ---
            run_id: "<run_id>"
            phase: "07_CLOSEOUT"
            voie: "CLOTURE"
            status: "READY"
            agent: "claude-code"
            started_at: "<ISO8601>"
            ended_at: "<ISO8601>"
            artifacts_produced: []
            ---

            # Closeout
        """)
        (d / "07_CLOSEOUT.md").write_text(placeholder)
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, f"Expected exit 1, got {rc}"
        assert "FAIL" in out
        assert "placeholder" in out, f"Expected 'placeholder' in error\n{out}"


def test_run_not_found():
    """Non-existent run_id → FAIL immediately."""
    with tempfile.TemporaryDirectory() as tmp:
        rc, out, _ = _run("nonexistent-run-id", Path(tmp))
        assert rc == 1, f"Expected exit 1, got {rc}"
        assert "FAIL" in out


def test_invalid_voie():
    """01_INTAKE with unknown voie value → FAIL."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_bad-voie"
        d.mkdir()
        rid = "2026-01-01_1000_bad-voie"
        bad_voie = textwrap.dedent(f"""\
            ---
            run_id: "{rid}"
            phase: "01_INTAKE"
            voie: "INVENTED"
            status: "READY"
            agent: "claude-code"
            started_at: "2026-05-23T10:00:00Z"
            ended_at: "2026-05-23T10:30:00Z"
            artifacts_produced: []
            ---

            # Intake
        """)
        (d / "01_INTAKE.md").write_text(bad_voie)
        _make_artifact(d / "07_CLOSEOUT.md", rid, "07_CLOSEOUT", "RAPIDE")
        rc, out, _ = _run(rid, Path(tmp))
        assert rc == 1, f"Expected exit 1, got {rc}"
        assert "FAIL" in out
        assert "INVENTED" in out, f"Expected bad voie value in error\n{out}"


# ---------------------------------------------------------------------------
# Dogfood: PR #3 run must pass its own check
# ---------------------------------------------------------------------------

def test_pr3_run_passes():
    """The PR #3 run artifact set must satisfy the closure invariant."""
    rc, out, _ = _run(
        "2026-05-23_1800_artifact-verify-lot-c",
        REPO_ROOT / "docs" / "runs",
    )
    assert rc == 0, f"PR #3 run should pass the loop-closure check\n{out}"
    assert "PASS" in out

# ---------------------------------------------------------------------------
# --strict mode (VBB COMPLETE gate semantics)
# ---------------------------------------------------------------------------

def test_strict_fail_returns_exit_2():
    """--strict on a FAIL run_id → exit 2 (GATE_BLOCKED) + blocking msg on stderr."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_strict-fail"
        d.mkdir()
        rid = "2026-01-01_1000_strict-fail"
        # Build a STRUCTUREE run missing 04_PLAN → FAIL
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "STRUCTUREE")
        rc, out, err = _run(rid, Path(tmp), extra_args=["--strict"])
        assert rc == 2, f"Expected exit 2 (GATE_BLOCKED), got {rc}\nstderr:\n{err}"
        assert "GATE FAILED" in err, f"Expected GATE FAILED on stderr\nstderr:\n{err}"
        assert "FINAL_STATUS=COMPLETE is not allowed" in err, \
            f"Expected explicit COMPLETE-forbidden message\nstderr:\n{err}"
        assert rid in err, f"Expected run_id in blocking message\nstderr:\n{err}"


def test_strict_no_run_id_returns_exit_64():
    """--strict without any run_id (no positional, no env) → exit 64 (USAGE_ERROR)."""
    # Use a fresh empty runs-dir so auto-detect cannot find a run.
    with tempfile.TemporaryDirectory() as tmp:
        empty = Path(tmp) / "empty_runs"
        empty.mkdir()
        cmd = [sys.executable, str(TOOL), "--strict", "--runs-dir", str(empty)]
        # Ensure VBB_RUN_ID is unset for this test
        env = {k: v for k, v in __import__("os").environ.items() if k != "VBB_RUN_ID"}
        result = subprocess.run(
            cmd, capture_output=True, text=True, env=env,
        )
        assert result.returncode == 64, \
            f"Expected exit 64 (USAGE_ERROR), got {result.returncode}\nstderr:\n{result.stderr}"
        assert "GATE FAILED" in result.stderr
        assert "--run_id required" in result.stderr, \
            f"Expected explicit 'required' message\nstderr:\n{result.stderr}"


def test_strict_pass_returns_exit_0():
    """--strict on a PASS run_id → exit 0 (no blocking message)."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "2026-01-01_1000_strict-pass"
        d.mkdir()
        rid = "2026-01-01_1000_strict-pass"
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d / f"{phase}.md", rid, phase, "RAPIDE")
        rc, out, err = _run(rid, Path(tmp), extra_args=["--strict"])
        assert rc == 0, f"Expected exit 0 on PASS, got {rc}\nstdout:\n{out}\nstderr:\n{err}"
        assert "PASS" in out
        # On PASS, the strict gate does NOT emit a blocking message
        assert "GATE FAILED" not in err, \
            f"Strict PASS should be silent on stderr\nstderr:\n{err}"


def test_default_mode_retrocompatible_exit_codes():
    """Default mode (no --strict) preserves original exit codes: 1 for FAIL, 0 for PASS."""
    with tempfile.TemporaryDirectory() as tmp:
        # FAIL case: STRUCTUREE missing 04_PLAN
        d_fail = Path(tmp) / "2026-01-01_1000_default-fail"
        d_fail.mkdir()
        rid_fail = "2026-01-01_1000_default-fail"
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d_fail / f"{phase}.md", rid_fail, phase, "STRUCTUREE")
        rc_fail, out_fail, _ = _run(rid_fail, Path(tmp))  # no extra_args
        assert rc_fail == 1, \
            f"Default mode FAIL should still be exit 1, got {rc_fail}\n{out_fail}"

        # PASS case: complete RAPIDE
        d_pass = Path(tmp) / "2026-01-01_1000_default-pass"
        d_pass.mkdir()
        rid_pass = "2026-01-01_1000_default-pass"
        for phase in ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"]:
            _make_artifact(d_pass / f"{phase}.md", rid_pass, phase, "RAPIDE")
        rc_pass, out_pass, _ = _run(rid_pass, Path(tmp))
        assert rc_pass == 0, \
            f"Default mode PASS should still be exit 0, got {rc_pass}\n{out_pass}"


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
