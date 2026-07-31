"""Fixtures for the versioned A2 isolation / A3 independence contract."""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("adv_gate", ROOT / "tools/vbb-adversarial-gate.py")
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
        external = {"independent_actor": True, "producer_control_absent": True, "actor_type": "external"}
    return {"level": level, "governance_version": "1.2", "operational_isolation": isolation, "external_independence": external}


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
