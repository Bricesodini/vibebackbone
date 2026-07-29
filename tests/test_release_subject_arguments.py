"""Fail-closed parsing locks for release subject selector arguments."""

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent.parent.resolve()
LOOP = ROOT / "tools" / "vbb-loop-closure-check.py"
ADVERSARIAL = ROOT / "tools" / "vbb-adversarial-gate.py"
RUN_ID = "2026-07-29_1941_run1-exact-release-measurement"
GOOD_SHA = "f" * 40
BAD_SHA = "b" * 40
GOOD_CANDIDATE = "RUN1-EXACT-RELEASE-MEASUREMENT-CANDIDATE-03"
BAD_CANDIDATE = "wrong-candidate"


def _env() -> dict[str, str]:
    return {k: v for k, v in os.environ.items() if not k.startswith("VBB_")}


def _invoke(tool: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(tool), *args, "--strict"],
        capture_output=True,
        text=True,
        env=_env(),
    )


def test_loop_rejects_duplicate_expected_commit_matrix():
    cases = [
        (BAD_SHA, GOOD_SHA),
        (GOOD_SHA, BAD_SHA),
        (GOOD_SHA, GOOD_SHA),
        ("", GOOD_SHA),
        (GOOD_SHA, ""),
    ]
    for first, second in cases:
        proc = _invoke(
            LOOP,
            RUN_ID,
            "--expected-commit",
            first,
            "--expected-commit",
            second,
        )
        assert proc.returncode != 0
        assert "duplicate_critical_argument" in proc.stdout + proc.stderr


def test_loop_rejects_duplicate_candidate_id_matrix():
    for first, second in (
        (BAD_CANDIDATE, GOOD_CANDIDATE),
        (GOOD_CANDIDATE, GOOD_CANDIDATE),
    ):
        proc = _invoke(
            LOOP,
            RUN_ID,
            "--candidate-id",
            first,
            "--candidate-id",
            second,
        )
        assert proc.returncode != 0
        assert "duplicate_critical_argument" in proc.stdout + proc.stderr


def test_adversarial_rejects_duplicate_critical_arguments():
    for args in (
        ("--expected-commit", BAD_SHA, "--expected-commit", GOOD_SHA),
        ("--expected-commit", GOOD_SHA, "--expected-commit", GOOD_SHA),
        ("--candidate-id", BAD_CANDIDATE, "--candidate-id", GOOD_CANDIDATE),
        ("--candidate-id", GOOD_CANDIDATE, "--candidate-id", GOOD_CANDIDATE),
        ("--expected-commit", "", "--expected-commit", GOOD_SHA),
        ("--expected-commit", GOOD_SHA, "--expected-commit", ""),
    ):
        proc = _invoke(ADVERSARIAL, RUN_ID, *args)
        assert proc.returncode != 0
        assert "duplicate_critical_argument" in proc.stdout + proc.stderr


def test_workflow_style_single_occurrence_is_not_rejected():
    """The carrier's one explicit occurrence remains parseable."""
    proc = _invoke(LOOP, RUN_ID, "--expected-commit", GOOD_SHA)
    assert "duplicate_critical_argument" not in proc.stdout + proc.stderr
