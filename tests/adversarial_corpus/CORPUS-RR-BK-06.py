"""Active regression guard for FIND-RR-BK-06.

Origin: docs/runs/2026-07-31_1800_rr-bk-06-s2-remediation/07_CLOSEOUT.md#F-01
Severity: P0
State: ACTIVE (REMEDIATION_IN_PROGRESS at SHA 58e51ee — F-01 unsatisfied)

RR-BK-06 invariant: the adversarial gate's M3-02 distinct check
must NOT be satisfied when attacker and defender share the same LLM
family, system_prompt_version, and provider (no genuine A2 actor).
"""

import importlib.util
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GATE = REPO_ROOT / "tools" / "vbb-adversarial-gate.py"


def _import_gate():
    spec = importlib.util.spec_from_file_location("vbb_adversarial_gate_corpus", GATE)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["vbb_adversarial_gate_corpus"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_llm_family_distinct_rejects_same_family():
    """Two LLM identifiers in the same family must NOT be distinct."""
    gate = _import_gate()
    assert (
        gate._llm_family_distinct("minimax/MiniMax-M3", "minimax/MiniMax-M3") is False
    )


def test_llm_family_distinct_rejects_substring_match():
    """Two LLM identifiers with overlapping prefix must NOT be distinct."""
    gate = _import_gate()
    assert gate._llm_family_distinct("minimax/foo", "minimax/bar") is False


def test_llm_family_distinct_accepts_different_family():
    """Two LLM identifiers from different families ARE distinct."""
    gate = _import_gate()
    assert gate._llm_family_distinct("minimax/MiniMax-M3", "openai/gpt-4") is True


def test_llm_family_distinct_rejects_empty():
    """Empty LLM identifiers must NOT be distinct."""
    gate = _import_gate()
    assert gate._llm_family_distinct("", "minimax/MiniMax-M3") is False
    assert gate._llm_family_distinct("minimax/MiniMax-M3", "") is False
