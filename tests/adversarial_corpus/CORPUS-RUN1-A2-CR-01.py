"""Corpus guard for RUN1-A2-CR-01: GitHub carries the checked-out SHA."""

from pathlib import Path


def test_run1_a2_cr_01_remote_carrier_is_exact():
    workflow = (
        Path(__file__).resolve().parents[2] / ".github/workflows/vbb-contracts.yml"
    ).read_text(encoding="utf-8")
    for gate in ("vbb-loop-closure-check.py", "vbb-adversarial-gate.py"):
        assert (
            f'{gate} "$run_dir" --expected-commit "$VBB_HEAD_SHA" --strict' in workflow
        )
