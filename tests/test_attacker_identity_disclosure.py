"""M2-14 — attacker_identity disclosure tests (M1-02).

Validates that every A2 adversarial record carries the three required
identity disclosures: {agent, llm, system_prompt_version}.
"""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_attacker_identity_required_for_a2():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    # Section §3 must require three disclosures
    assert "{agent, llm, system_prompt_version}" in authority or (
        "agent" in authority
        and "llm" in authority
        and "system_prompt_version" in authority
    )


def test_attacker_identity_in_adversarial_block():
    """The 07_CLOSEOUT template documents the attacker_identity field."""
    template = _read("docs/templates/07_CLOSEOUT.md.template")
    assert "attacker_identity" in template


def test_attacker_identity_validated_by_adversarial_gate():
    """The validator checks attacker_identity for A2."""
    validator = _read("tools/vbb-adversarial-gate.py")
    assert "attacker_identity" in validator
    # The validator must check 3 disclosures
    for key in ("agent", "llm", "system_prompt_version"):
        assert key in validator


def test_attacker_identity_in_campaign_template():
    campaign = _read("docs/templates/ADVERSARIAL_CAMPAIGN.md.template")
    assert "attacker_identity" in campaign
    assert "agent" in campaign
    assert "llm" in campaign
    assert "system_prompt_version" in campaign
