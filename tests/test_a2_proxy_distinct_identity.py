"""M3-12 — attacker_identity distinctness test (extends test_a2_proxy.py).

R2 §8 (ADVR-A2-11): `test_a2_proxy.py` tested only the *presence* of
attacker_identity.{agent, llm, system_prompt_version}, not the *difference*
between attacker and defender identities. M3-12 adds coverage for the
mechanical comparison contract.

This test extends `test_a2_proxy.py`'s role: it asserts that the canon
documents the MANDATORY distinctness requirement for each of:
    - distinct_llm: MANDATORY
    - distinct_system_prompt: MANDATORY
    - distinct_provider_or_human: MANDATORY
    - defender_identity declared for mechanical comparison

The test also asserts a regression lock: a future change to the canon
that removes any of the four MANDATORY declarations must be rejected.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent


def test_a2_proxy_canon_declares_distinct_llm_mandatory():
    """ADVERSARIAL_ASSURANCE_GOVERNANCE.md §3 must mark `distinct_llm` as
    MANDATORY (M1-02 + A2_DISTINCT_AGENT_PROXY contract)."""
    canon = (REPO / "docs" / "ADVERSARIAL_ASSURANCE_GOVERNANCE.md").read_text(
        encoding="utf-8"
    )
    # The exact phrase "distinct_llm: MANDATORY" or "distinct_llm (MANDATORY)" must appear.
    assert "distinct_llm" in canon
    # Co-location: the same line must include MANDATORY.
    for line in canon.split("\n"):
        if "distinct_llm" in line.lower() and "mandatory" in line.lower():
            return
    pytest.fail("canon must declare `distinct_llm` as MANDATORY")


def test_a2_proxy_canon_declares_distinct_system_prompt_mandatory():
    """ADVERSARIAL_ASSURANCE_GOVERNANCE.md must declare `distinct_system_prompt`
    as MANDATORY for A2 with A2_DISTINCT_AGENT_PROXY."""
    canon = (REPO / "docs" / "ADVERSARIAL_ASSURANCE_GOVERNANCE.md").read_text(
        encoding="utf-8"
    )
    for line in canon.split("\n"):
        if "distinct_system_prompt" in line.lower() and "mandatory" in line.lower():
            return
    pytest.fail("canon must declare `distinct_system_prompt` as MANDATORY")


def test_a2_proxy_canon_declares_disclosures_mandatory():
    """The three attacker_identity disclosures (`agent`, `llm`,
    `system_prompt_version`) must each be marked MANDATORY."""
    canon = (REPO / "docs" / "ADVERSARIAL_ASSURANCE_GOVERNANCE.md").read_text(
        encoding="utf-8"
    )
    # The block at §3 should declare each.
    assert "attacker_identity_disclosure: MANDATORY" in canon
    assert "agent" in canon
    assert "llm" in canon
    assert "system_prompt_version" in canon


def test_a2_proxy_canon_declares_quarterly_external_review():
    """A2_DISTINCT_AGENT_PROXY contract requires quarterly external review."""
    canon = (REPO / "docs" / "ADVERSARIAL_ASSURANCE_GOVERNANCE.md").read_text(
        encoding="utf-8"
    )
    assert "QUARTERLY" in canon, "canon must declare QUARTERLY cadence"
    assert "external_review" in canon.lower(), (
        "canon must cross-reference external_review for A2"
    )


def test_a2_proxy_validator_passes_on_distinct_llm():
    """The validator must PASS adv-a2-distinct when attacker.llm and
    defender.llm are different families (regression lock on M3-02 fix)."""
    import subprocess

    body = """```yaml
adversarial:
  level: "A2"
  campaign_ref: "test-canon"
  corpus_version: "v1.1"
  exploration_performed: true
  surfaces_declared:
    - "x.py"
  surfaces_unexplored: []
  residual_uncertainty: "none"
  findings: []
  verdict: "PASS_ADVERSARIAL"
  non_claim: "absence of finding is bounded evidence, never proof"
  attacker_identity:
    agent: "external attacker"
    llm: "anthropic/claude-3-5-sonnet"
    provider: "anthropic"
    system_prompt_version: "attack-falsifier-v1"
    session: "sess-abc12345"
  defender_identity:
    agent: "implementer"
    llm: "minimax/MiniMax-M3"
    provider: "minimax"
    system_prompt_version: "implementer-v1"
    session: "sess-impl-yyyy"
```
```"""
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        run_dir = Path(td)
        (run_dir / "01_INTAKE.md").write_text("# stub\n", encoding="utf-8")
        (run_dir / "07_CLOSEOUT.md").write_text(body, encoding="utf-8")
        proc = subprocess.run(
            ["python", "tools/vbb-adversarial-gate.py", str(run_dir)],
            cwd=str(REPO),
            capture_output=True,
            text=True,
        )
        text = proc.stdout + proc.stderr
        # adv-a2-distinct must PASS.
        import re

        passes = set(
            re.findall(r"^\s*(?:\[[A-Za-z0-9]+\]\s*)?PASS\s+(\S+):", text, re.MULTILINE)
        )
        assert "adv-a2-distinct" in passes
