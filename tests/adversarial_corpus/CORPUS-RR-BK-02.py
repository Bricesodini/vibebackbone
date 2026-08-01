"""Active regression guard for FIND-RR-BK-02.

Origin: docs/runs/2026-08-01_1100_release-freeze/INDEPENDENT_RELEASE_REVALIDATION.md#RR-BK-02
Severity: P1
State: ACTIVE (PASS_REVALIDATED on SHA 58e51ee)

RR-BK-02 invariant: the loop-closure gate binds to an explicit
run-id and an explicit full-length SHA (no short-SHA fallback).
"""

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))


def test_loop_closure_full_sha_accepted():
    """Full-length SHA must be accepted by the gate binding."""
    result = _run(
        [
            sys.executable,
            "tools/vbb-loop-closure-check.py",
            "2026-08-01_1100_release-freeze",
            "--runs-dir",
            "docs/runs",
            "--expected-commit",
            "58e51eeebfd057a359eb78393ce16d6df4a05cf3",
            "--strict",
        ]
    )
    # Gate returns 0 even on FAIL (writes report) under non-strict;
    # under --strict the exit code may be 2 for binding FAIL — we
    # only verify the path was accepted (no USAGE_ERROR).
    assert "USAGE_ERROR" not in result.stderr
    assert "invalid_or_empty_expected_commit" not in result.stderr


def test_loop_closure_short_sha_rejected():
    """Short SHA must be rejected (no fallback to short SHA)."""
    result = _run(
        [
            sys.executable,
            "tools/vbb-loop-closure-check.py",
            "2026-08-01_1100_release-freeze",
            "--runs-dir",
            "docs/runs",
            "--expected-commit",
            "58e51ee",
            "--strict",
        ]
    )
    combined = result.stdout + result.stderr
    assert "invalid_or_empty_expected_commit" in combined
