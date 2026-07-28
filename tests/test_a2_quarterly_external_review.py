"""A2 quarterly external review cadence tests.

Validates that the A2 external_review contract:
- Cadence is QUARTERLY (≤ 90 days).
- Failure mode = next CERTIFIED claim must wait for external_review pass.
- Different llm family OR human required.
"""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_cadence_quarterly():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    assert "QUARTERLY" in authority


def test_cadence_90_days():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    assert "90 days" in authority or "90 jours" in authority


def test_failure_mode_documented():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    # Failure mode text
    assert "external_review" in authority
    # Operator constraint: different llm family OR human
    assert "different llm family" in authority or "different LLM family" in authority


def test_last_external_review_field():
    """The 07_CLOSEOUT template documents last_external_review for A2."""
    template = _read("docs/templates/07_CLOSEOUT.md.template")
    assert "last_external_review" in template
