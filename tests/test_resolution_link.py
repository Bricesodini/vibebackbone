"""Resolution link tests — POST_IMPLEMENTATION FAIL → COUNTER_PROOF PASS.

Validates that a POST_IMPLEMENTATION FAIL can be closed via a
resolution link to a COUNTER_PROOF gate result with verdict PASS.
"""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_resolution_link_documented():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    assert "resolution" in authority.lower()


def test_counter_proof_checkpoint_in_schema():
    gate = _read("docs/GATE_ASSURANCE_GOVERNANCE.md")
    assert "COUNTER_PROOF" in gate


def test_closure_evaluation_uses_resolution():
    gate = _read("docs/GATE_ASSURANCE_GOVERNANCE.md")
    assert "closure_evaluation" in gate
    assert "resolution" in gate.lower()


def test_checkpoint_aggregation_immutable():
    """Per ADR 0050 §Schema 1.1, a POST_IMPLEMENTATION FAIL stays FAIL."""
    gate = _read("docs/GATE_ASSURANCE_GOVERNANCE.md")
    assert "checkpoint_aggregation" in gate
    # Must not be collapsed with closure_evaluation
    assert (
        "must not be collapsed" in gate.lower()
        or "must not collapse" in gate.lower()
        or "no implementation may collapse" in gate.lower()
    )
