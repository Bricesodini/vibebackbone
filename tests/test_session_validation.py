"""M3-05 — `attacker_identity.session` minimum-format validation.

R2 §5: `session` must be present, non-empty, length ≥ 8 chars, and
not whitespace-only. The token is opaque (no UUID/structured-ID
requirement) but must be recordable as M1-02 traceability.

M1-02 §Contrat also requires that a separate session field be
recordable on both `attacker_identity` and `defender_identity`.
The minimum validation is mechanical (no semantic content check).
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent


CANON_BODY = """```yaml
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
    session: "{session}"
  defender_identity:
    agent: "implementer"
    llm: "minimax/MiniMax-M3"
    provider: "minimax"
    system_prompt_version: "implementer-v1"
    session: "sess-defender-yyyyyyyy"
```
```"""


def _make_body(session: str) -> str:
    return CANON_BODY.replace("{session}", session)


def _run_validator(run_dir: Path) -> tuple[int, str]:
    proc = subprocess.run(
        ["python", "tools/vbb-adversarial-gate.py", str(run_dir)],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def _fails(text: str) -> set[str]:
    return set(
        re.findall(r"^\s*(?:\[[A-Za-z0-9]+\]\s*)?FAIL\s+(\S+):", text, re.MULTILINE)
    )


def _passes(text: str) -> set[str]:
    return set(
        re.findall(r"^\s*(?:\[[A-Za-z0-9]+\]\s*)?PASS\s+(\S+):", text, re.MULTILINE)
    )


# Test 1: Empty session rejected
def test_adversarial_gate_rejects_empty_session(tmp_path: Path):
    (tmp_path / "01_INTAKE.md").write_text("# stub\n", encoding="utf-8")
    (tmp_path / "07_CLOSEOUT.md").write_text(_make_body(session=""), encoding="utf-8")
    rc, text = _run_validator(tmp_path)
    f = _fails(text)
    assert any("session" in s.lower() for s in f), (
        f"expected session-related FAIL, got {f}"
    )


# Test 2: Whitespace-only session rejected
def test_adversarial_gate_rejects_whitespace_session(tmp_path: Path):
    (tmp_path / "01_INTAKE.md").write_text("# stub\n", encoding="utf-8")
    (tmp_path / "07_CLOSEOUT.md").write_text(
        _make_body(session="        "), encoding="utf-8"
    )
    rc, text = _run_validator(tmp_path)
    f = _fails(text)
    assert any("session" in s.lower() for s in f), (
        f"expected session-related FAIL, got {f}"
    )


# Test 3: Too-short session rejected (shorter than 8 chars)
def test_adversarial_gate_rejects_short_session(tmp_path: Path):
    (tmp_path / "01_INTAKE.md").write_text("# stub\n", encoding="utf-8")
    (tmp_path / "07_CLOSEOUT.md").write_text(_make_body(session="x"), encoding="utf-8")
    rc, text = _run_validator(tmp_path)
    f = _fails(text)
    assert any("session" in s.lower() for s in f), (
        f"expected session-related FAIL, got {f}"
    )


# Test 4: Sufficiently long non-empty session passes
def test_adversarial_gate_accepts_long_enough_session(tmp_path: Path):
    (tmp_path / "01_INTAKE.md").write_text("# stub\n", encoding="utf-8")
    (tmp_path / "07_CLOSEOUT.md").write_text(
        _make_body(session="session-abc-12345678"), encoding="utf-8"
    )
    rc, text = _run_validator(tmp_path)
    p = _passes(text)
    # adv-a2-identity must PASS for a valid session.
    assert "adv-a2-identity" in p
