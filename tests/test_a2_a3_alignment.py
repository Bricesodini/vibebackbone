"""Fixtures for the versioned A2 isolation / A3 independence contract."""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "adv_gate", ROOT / "tools/vbb-adversarial-gate.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules["adv_gate"] = MODULE
SPEC.loader.exec_module(MODULE)


def block(level="A2", isolation=None, external=None):
    if isolation is None:
        isolation = {
            "session_distinct": True,
            "fresh_context": True,
            "adversarial_role_explicit": True,
            "defender_conclusions_exposed": False,
            "inputs_preserved": True,
            "raw_transcript_preserved": True,
            "findings_independent": True,
            "declared_scope": True,
            "runtime_identity_observed": True,
        }
    if external is None:
        external = {
            "independent_actor": True,
            "producer_control_absent": True,
            "actor_type": "external",
        }
    return {
        "level": level,
        "governance_version": "1.2",
        "operational_isolation": isolation,
        "external_independence": external,
    }


def test_a2_operational_isolation_passes_without_a3_claim():
    passes, fails = MODULE.check_a2_a3_clarification(block("A2"), "A2")
    assert not fails
    assert {item.gate_id for item in passes} == {"adv-a2-operational-isolation"}


def test_a2_missing_isolation_fails_closed():
    passes, fails = MODULE.check_a2_a3_clarification(block("A2", isolation={}), "A2")
    assert not passes
    assert any(item.gate_id == "adv-a2-operational-isolation" for item in fails)


def test_a3_requires_external_independence():
    _, fails = MODULE.check_a2_a3_clarification(block("A3", external={}), "A3")
    assert any(item.gate_id == "adv-a3-external-independence" for item in fails)


def test_historical_v11_profile_is_not_reinterpreted():
    historical = {"level": "A2", "governance_version": "1.1"}
    passes, fails = MODULE.check_a2_a3_clarification(historical, "A2")
    assert not passes and not fails


def test_v12_a2_does_not_call_legacy_distinct_actor_gate(monkeypatch):
    """v1.2 A2 must use isolation, not the superseded v1.1 actor test."""
    body = """```yaml
adversarial:
  level: A2
  governance_version: "1.2"
  campaign_ref: test-v12
  corpus_version: v1.2.0
  exploration_performed: true
  surfaces_declared:
    - tools/vbb-adversarial-gate.py
  surfaces_unexplored:
    - remote external review
  residual_uncertainty: "No A3 independence claim."
  findings: []
  verdict: FINDINGS_OPEN
  attacker_identity:
    agent: same-operational-proxy
    llm: GPT-5
    provider: OpenAI
    system_prompt_version: same-runtime
    session: isolated-v12-session
  defender_identity:
    agent: same-defender
    llm: GPT-5
    provider: OpenAI
    system_prompt_version: same-runtime
    session: current-session
  operational_isolation:
    session_distinct: true
    fresh_context: true
    adversarial_role_explicit: true
    defender_conclusions_exposed: false
    inputs_preserved: true
    raw_transcript_preserved: true
    findings_independent: true
    declared_scope: true
    runtime_identity_observed: true
```
"""

    def legacy_gate_must_not_run(_adv):
        raise AssertionError("v1.2 must not invoke the v1.1 distinct-actor gate")

    monkeypatch.setattr(MODULE, "check_a2_distinct_identity", legacy_gate_must_not_run)
    passes, fails = MODULE.check_adversarial_block(body, "test-v12")
    assert any(item.gate_id == "adv-a2-operational-isolation" for item in passes)
    assert not any(item.gate_id == "adv-a2-distinct" for item in fails)
