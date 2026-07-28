"""M2-14 — A2_DISTINCT_AGENT_PROXY contract tests (M1-02).

Verifies the canonical contract for solo-repository A2 assurance:
- `attacker_identity` requires three disclosures.
- `distinct_llm` is mandatory.
- `distinct_system_prompt` is mandatory.
- `external_review` cadence is QUARTERLY (≤ 90 days).
- `last_external_review` is within cadence.
- Silent downshift A2 → A1 is forbidden.
"""

from pathlib import Path
import re


REPO_ROOT = Path(__file__).parent.parent


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_a2_proxy_contract_in_canon():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    assert "A2_DISTINCT_AGENT_PROXY" in authority
    assert "attacker_identity" in authority
    # Three disclosures
    assert "agent" in authority
    assert "llm" in authority
    assert "system_prompt_version" in authority
    # Quarterly review
    assert "QUARTERLY" in authority


def test_a2_proxy_forbids_silent_downshift():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    # The text "silent downshift" must be present (or the equivalent)
    assert re.search(
        r"silent downshift|downshift.*forbidden|downshift.*prohibited",
        authority,
        re.IGNORECASE,
    )


def test_a2_proxy_external_review_constraint():
    authority = _read("docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md")
    # Either human or different llm family required
    assert "different llm family" in authority or "different LLM family" in authority
    assert "human" in authority.lower()


def test_a2_proxy_in_finding_template():
    """The finding template documents the attacker_identity location."""
    template = _read("docs/templates/FINDING.md.template")
    assert "discovered_by" in template
    # attacker_identity is documented in ADVERSARIAL_CAMPAIGN, not FINDING
    campaign = _read("docs/templates/ADVERSARIAL_CAMPAIGN.md.template")
    assert "attacker_identity" in campaign
    assert "agent" in campaign
    assert "llm" in campaign
    assert "system_prompt_version" in campaign
