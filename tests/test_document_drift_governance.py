"""Contract tests for governed-artifact drift handling."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = (ROOT / "AGENTS.md").read_text(encoding="utf-8")


def test_drift_rule_covers_governed_artifacts_and_human_decision() -> None:
    assert "governed artifact" in AGENTS
    assert "never modifies the artifact automatically" in AGENTS
    assert "`OUI`, `NON`, or `PLUS TARD`" in AGENTS


def test_remediation_is_chosen_only_after_yes() -> None:
    assert "Only after `OUI` does the agent" in AGENTS
    assert "`NON`, it keeps" in AGENTS
    assert "`PLUS TARD`, it records" in AGENTS


def test_canon_change_is_conditional_and_adversarial_governance_is_untouched() -> None:
    assert "required only when" in AGENTS
    assert "the remediation actually changes the canon" in AGENTS
    assert "CR-2" not in AGENTS
    assert "CC-11" not in AGENTS
    assert "REVISE-C v3" not in AGENTS
    assert "ADR-0052" not in AGENTS
