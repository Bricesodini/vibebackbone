"""Behaviour pin for confirmed historical finding A2-GP-02.

Origin: docs/runs/2026-07-29_1834_governance-principles/06_INDEPENDENT_REVIEW_A2.md#A2-GP-02
Severity: S1
Confidence: CONFIRMED
State: BEHAVIOUR_PIN (unremediated)
"""

from pathlib import Path


def test_a2_gp_02_identity_and_state_are_preserved():
    text = (Path(__file__).parents[2] / "docs/runs/2026-07-31_1137_clean-candidate-reconstruction/evidence/RR-BK-05_HISTORICAL_FINDINGS.md").read_text()
    assert "| A2-GP-02 | A2 | S1 | CONFIRMED | CLASSIFIED |" in text
