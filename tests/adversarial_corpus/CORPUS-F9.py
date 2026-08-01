"""Active regression guard for FIND-F9.

Origin: docs/runs/2026-08-01_1100_release-freeze/evidence/raw/12_F9_strict_path.txt
Severity: P2
State: ACTIVE (CLOSED_REMEDIATED at SHA 58e51ee)

F9 invariant: the loop-closure gate accepts `--runs-dir` +
`--expected-commit <full-SHA>` + `--strict` as an explicit, unambiguous
path. Short-SHA must be rejected (no silent fallback).
"""

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))


def test_full_sha_explicit_path_accepted():
    """Full-SHA + --runs-dir must be accepted by the gate (no USAGE_ERROR)."""
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
    combined = result.stdout + result.stderr
    assert "USAGE_ERROR" not in combined
    assert "invalid_or_empty_expected_commit" not in combined


def test_short_sha_rejected_explicit():
    """Short SHA (less than 40 chars) must be rejected with a clear error."""
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


def test_empty_sha_rejected():
    """Empty SHA must be rejected."""
    result = _run(
        [
            sys.executable,
            "tools/vbb-loop-closure-check.py",
            "2026-08-01_1100_release-freeze",
            "--runs-dir",
            "docs/runs",
            "--expected-commit",
            "",
            "--strict",
        ]
    )
    combined = result.stdout + result.stderr
    # Either invalid_or_empty_expected_commit or USAGE_ERROR depending on gate
    # version; either is acceptable.
    assert (
        "invalid_or_empty_expected_commit" in combined
        or "USAGE_ERROR" in combined
        or result.returncode != 0
    )
