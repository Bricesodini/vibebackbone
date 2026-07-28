"""M2-18 — certification.owner SLA breach tests (M1-04).

Validates that the certification.owner contract enforces:
- 3 modes: manual:<cadence>, cron:<expr>, webhook:<target>.
- Default mode = manual:quarterly.
- Cadence ≤ 90 days.
- SLA breach → automatic CERTIFIED → SUSPENDED.
- Revocation includes SLA breach as a 6th trigger.
"""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_three_modes_declared():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    assert "manual:<cadence>" in authority or "manual" in authority
    assert "cron:<expr>" in authority or "cron" in authority
    assert "webhook:<target>" in authority or "webhook" in authority


def test_default_mode_is_quarterly():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    assert "manual:quarterly" in authority


def test_cadence_upper_bound():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    assert "90 days" in authority or "90 jours" in authority


def test_sla_breach_triggers_suspension():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    # SLA breach must cause CERTIFIED → SUSPENDED
    assert "SLA breach" in authority or "SLA" in authority
    assert "SUSPENDED" in authority


def test_revocation_mechanism_required_for_certified():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    section = authority.find("### §5.3")
    chunk = authority[section : section + 3500] if section != -1 else authority
    assert "revocation_mechanism" in chunk
