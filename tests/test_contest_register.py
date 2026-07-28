"""M1-03 — contest_register tests.

Verifies the contest_register mechanism:
- A named gate expert may file a written objection.
- The objection names the trigger and rationale.
- A contested classification defaults to A1 until resolution.
- Detection is mechanical (in 01_INTAKE.md).
"""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_contest_register_in_canon():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    assert "contest" in authority.lower()
    assert "objection" in authority.lower() or "objector" in authority.lower()


def test_contest_register_in_intake_template():
    template = _read("docs/templates/01_INTAKE.md.template")
    assert "contest_register" in template


def test_contested_classification_defaults_to_a1():
    """§4.3 fail-closed rule for contested classifications."""
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    assert "contesté" in authority.lower() or "contested" in authority.lower()
    assert "A1" in authority


def test_pilotage_documents_fail_closed_rules():
    pilotage = _read("docs/PILOTAGE.md")
    assert "contesté" in pilotage.lower() or "contested" in pilotage.lower()
    assert "A1" in pilotage


def test_n_is_10():
    """N=10 runs for the S0/S1 history trigger."""
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    assert "N = 10" in authority or "N=10" in authority
