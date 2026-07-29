"""Corpus guard for RUN1-A2-CR-04: an explicit empty SHA is invalid."""

import subprocess
import sys
from pathlib import Path


def test_loop_closure_rejects_explicit_empty_expected_commit():
    repo = Path(__file__).resolve().parents[2]
    run_id = "2026-07-29_1941_run1-exact-release-measurement"
    proc = subprocess.run(
        [
            sys.executable,
            str(repo / "tools/vbb-loop-closure-check.py"),
            run_id,
            "--expected-commit",
            "",
            "--strict",
            "--json",
        ],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode != 0
    assert '"exit_intent": "FAIL"' in proc.stdout
    assert '"reason": "invalid_or_empty_expected_commit"' in proc.stdout
