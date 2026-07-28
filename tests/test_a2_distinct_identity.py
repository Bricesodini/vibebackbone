"""M3-02 fails-before and passes-after tests for `A2_DISTINCT_AGENT_PROXY`.

The validator must verify that `attacker_identity` is *distinct* from
`defender_identity` on at least one mechanical property (llm,
system_prompt_version, or provider). This is the M1-02 contract:
`distinct_llm: MANDATORY` and `distinct_system_prompt: MANDATORY`.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


ATTACKER = {
    "agent": "external attacker",
    "llm": "anthropic/claude-3-5-sonnet",
    "provider": "anthropic",
    "system_prompt_version": "attack-falsifier-v1",
    "session": "sess-abc12345",
}


def _write(tmp_path: Path, body: str) -> Path:
    (tmp_path / "01_INTAKE.md").write_text("# stub intake\n", encoding="utf-8")
    (tmp_path / "07_CLOSEOUT.md").write_text(body, encoding="utf-8")
    return tmp_path


def _attacker_yaml(**overrides) -> str:
    fields = dict(ATTACKER)
    fields.update(overrides)
    return "\n".join(f"    {k}: {v!r}" for k, v in fields.items())


def _defender_yaml(**overrides) -> str:
    base = {
        "agent": "implementer",
        "llm": "minimax/MiniMax-M3",
        "provider": "minimax",
        "system_prompt_version": "implementer-v1",
        "session": "sess-impl-xyz",
    }
    base.update(overrides)
    return "\n".join(f"    {k}: {v!r}" for k, v in base.items())


def _make_body(
    attacker_override: dict = {}, defender_block: str = "", defend_missing: bool = False
) -> str:
    """Build a complete v1.1 closeout body, optionally inserting a defender block."""
    attacker = _attacker_yaml(**attacker_override)
    a2_block = f"```yaml\nadversarial:\n  level: A2\n  campaign_ref: test\n  corpus_version: v1.1\n  exploration_performed: true\n  surfaces_declared:\n    - x.py\n  surfaces_unexplored: []\n  residual_uncertainty: none\n  findings: []\n  verdict: PASS_ADVERSARIAL\n  non_claim: 'absence of finding is bounded evidence, never proof'\n  attacker_identity:\n{attacker}\n"
    if not defend_missing and defender_block:
        a2_block += f"  defender_identity:\n{defender_block}\n"
    return a2_block + "```\n"


def _run_validator(run_dir: Path) -> tuple[int, str]:
    proc = subprocess.run(
        ["python", "tools/vbb-adversarial-gate.py", str(run_dir)],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def _passes(text: str) -> set[str]:
    return set(
        re.findall(r"^\s*(?:\[[A-Za-z0-9]+\]\s*)?PASS\s+(\S+):", text, re.MULTILINE)
    )


def _fails(text: str) -> set[str]:
    return set(
        re.findall(r"^\s*(?:\[[A-Za-z0-9]+\]\s*)?FAIL\s+(\S+):", text, re.MULTILINE)
    )


# Test 1: Same LLM on both sides (proxy mode that doesn't disclose distinction)
def test_adversarial_gate_rejects_identical_attacker_and_defender_llm(tmp_path: Path):
    """If attacker_identity.llm == defender_identity.llm, distinctness check
    must FAIL (M1-02 distinct_llm mandatory)."""
    body = _make_body(
        attacker_override={"llm": "minimax/MiniMax-M3"},
        defender_block=_defender_yaml(llm="minimax/MiniMax-M3"),
    )
    _write(tmp_path, body)
    rc, text = _run_validator(tmp_path)
    f = _fails(text)
    assert "adv-a2-distinct" in f, f"expected adv-a2-distinct in fails, got {f}"


# Test 2: Distinct LLMs (different families) — passes distinctness
def test_adversarial_gate_accepts_distinct_llm(tmp_path: Path):
    body = _make_body(
        defender_block=_defender_yaml(llm="minimax/MiniMax-M3"),
    )
    _write(tmp_path, body)
    rc, text = _run_validator(tmp_path)
    p = _passes(text)
    assert "adv-a2-distinct" in p, f"expected adv-a2-distinct in PASSES, got {p}"


# Test 3: Missing defender_identity block — FAIL closed
def test_adversarial_gate_rejects_missing_defender_identity(tmp_path: Path):
    """An A2 closeout without `defender_identity` must FAIL closed."""
    body = _make_body(defender_block="", defend_missing=True)
    _write(tmp_path, body)
    rc, text = _run_validator(tmp_path)
    f = _fails(text)
    assert "adv-a2-defender-identity" in f, (
        f"expected adv-a2-defender-identity in fails, got {f}"
    )


# Test 4: Same system_prompt_version on both sides
def test_adversarial_gate_rejects_identical_system_prompt(tmp_path: Path):
    body = _make_body(
        attacker_override={"system_prompt_version": "same-v1"},
        defender_block=_defender_yaml(system_prompt_version="same-v1"),
    )
    _write(tmp_path, body)
    rc, text = _run_validator(tmp_path)
    f = _fails(text)
    # distinctness must FAIL — same prompt version AND distinct LLMs but same prompt.
    # Actually M1-02 says both llm AND system_prompt must be distinct.
    assert "adv-a2-distinct" in f, f"expected adv-a2-distinct in fails, got {f}"


# Test 5: Both LLMs and system_prompts identical — strongest fail
def test_adversarial_gate_rejects_fully_identical_identity(tmp_path: Path):
    same = ATTACKER["llm"]
    same_p = ATTACKER["system_prompt_version"]
    body = _make_body(
        attacker_override={"llm": same, "system_prompt_version": same_p},
        defender_block=_defender_yaml(llm=same, system_prompt_version=same_p),
    )
    _write(tmp_path, body)
    rc, text = _run_validator(tmp_path)
    f = _fails(text)
    assert "adv-a2-distinct" in f, f"expected adv-a2-distinct in fails, got {f}"
