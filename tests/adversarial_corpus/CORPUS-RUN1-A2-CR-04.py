"""Corpus guards for the Run 1 exact-subject remediation."""

import subprocess
import sys
from pathlib import Path
import re


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


def test_exact_subject_uses_carrier_sha_and_stable_candidate_id():
    repo = Path(__file__).resolve().parents[2]
    run_id = "2026-07-29_1941_run1-exact-release-measurement"
    expected = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    candidate = "RUN1-EXACT-RELEASE-MEASUREMENT-CANDIDATE-03"
    proc = subprocess.run(
        [
            sys.executable,
            str(repo / "tools/vbb-loop-closure-check.py"),
            run_id,
            "--expected-commit",
            expected,
            "--candidate-id",
            candidate,
            "--strict",
        ],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    wrong = subprocess.run(
        [
            sys.executable,
            str(repo / "tools/vbb-loop-closure-check.py"),
            run_id,
            "--expected-commit",
            expected,
            "--candidate-id",
            "OTHER-CANDIDATE",
            "--strict",
        ],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert wrong.returncode != 0
    assert "candidate_id" in wrong.stdout + wrong.stderr


def test_campaign_closeout_and_corpus_manifest_are_one_version_and_finding_set():
    repo = Path(__file__).resolve().parents[2]
    campaign = (
        repo
        / "docs/runs/2026-07-29_1941_run1-exact-release-measurement/ADVERSARIAL_CAMPAIGN.md"
    ).read_text()
    closeout = (
        repo / "docs/runs/2026-07-29_1941_run1-exact-release-measurement/07_CLOSEOUT.md"
    ).read_text()
    version = (repo / "tests/adversarial_corpus/VERSION").read_text().strip()
    versions = set(
        re.findall(
            r'corpus_version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)', campaign + closeout
        )
    )
    assert versions == {version} == {"1.4.0"}
    for finding in (
        "RUN1-A2-CR-04-RESIDUAL",
        "RUN1-A2-CR-04-CARRIER",
        "RUN1-A2-CR-04-LOCAL-CI",
    ):
        assert finding in campaign
        assert finding in closeout
