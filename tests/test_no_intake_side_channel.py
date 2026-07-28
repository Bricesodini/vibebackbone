"""M3-04 — No dead `intake_text` path in `vbb-adversarial-gate.py`.

R2 ADVR-A2-05 observation: lines 885-887 read `01_INTAKE.md` and
dereference `intake_text` without using it. The "read then ignore"
pattern is either a bug (validation expected but missing) or a design
choice (intake has no effect on closeout validation).

M3-04 decision (per R2 §4): simplify by removing the dead read. If a
future intake-side check is needed, it must be added explicitly with a
test that the read has observable effect on the outcome.

This test asserts:
  1. The validator source does NOT contain a read-then-delete pattern.
  2. The validator's outcome on a run is invariant under arbitrary
     mutations to `01_INTAKE.md` (intake has no effect on the verdict).
  3. The validator outcome is unchanged regardless of intake text
     contents (no surprise side-channel).
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent


CANON_V11_BODY = """```yaml
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
    session: "sess-impl-xyz"
```
```"""


def _run_validator(run_dir: Path) -> tuple[int, str]:
    proc = subprocess.run(
        ["python", "tools/vbb-adversarial-gate.py", str(run_dir)],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


# Test 1: Validator source does not contain a `intake_text = ...; del intake_text` pattern.
def test_no_intake_read_then_delete_pattern():
    """The validator must not read `01_INTAKE.md` into a local variable and
    then immediately delete or ignore it (dead-code pattern)."""
    src = (REPO / "tools" / "vbb-adversarial-gate.py").read_text(encoding="utf-8")
    # FAIL-BEFORE: the pair `intake_text = intake.read_text(...)` followed by
    # `del intake_text` exists. Detect both lines.
    has_read = re.search(r"intake_text\s*=\s*intake\.read_text", src) is not None
    has_del = re.search(r"del\s+intake_text", src) is not None
    assert not (has_read and has_del), (
        "FAIL-BEFORE: vbb-adversarial-gate.py reads 01_INTAKE.md into "
        "`intake_text` and immediately deletes it (dead read)."
    )


# Test 2: Outcome invariance under intake mutation (intake has no side-channel effect).
def test_validator_outcome_invariance_under_intake_mutation(tmp_path: Path):
    """Mutating `01_INTAKE.md` (with attacker_identity at odds with the closeout)
    must NOT change the validator outcome. The closeout is the single source of
    truth for the validator. Intakes may add supplements, but the validator
    must not interpret them as gate-binding.

    FAIL-BEFORE: the dead read is silent — content has no effect. After M3-04,
    the dead read is removed. We assert that the validator's judgment on the
    closeout is unchanged whether the intake contains honest data, lying data,
    or no data at all."""
    # Baseline: intake contains canonical attacker_identity matching closeout.
    (tmp_path / "01_INTAKE.md").write_text(
        """# canonical intake
attacker_identity:
  agent: external attacker
  llm: anthropic/claude-3-5-sonnet
  system_prompt_version: attack-falsifier-v1
""",
        encoding="utf-8",
    )
    (tmp_path / "07_CLOSEOUT.md").write_text(CANON_V11_BODY, encoding="utf-8")
    rc1, text1 = _run_validator(tmp_path)

    # Mutated: intake contains lying attacker_identity (claims different LLM).
    (tmp_path / "01_INTAKE.md").write_text(
        """# lying intake — must be ignored
attacker_identity:
  agent: fake attacker
  llm: minimax/MiniMax-M3
  system_prompt_version: fake-version
""",
        encoding="utf-8",
    )
    rc2, text2 = _run_validator(tmp_path)

    # Validator's verdict and gates must be identical regardless of intake.
    # We extract gate verdict lines and compare.
    def _gate_lines(text: str) -> list[tuple[str, str]]:
        pattern = re.compile(r"^\s*(\S+)\s+(\S+):", re.MULTILINE)
        return sorted((m.group(2), m.group(1)) for m in pattern.finditer(text))

    gates1 = _gate_lines(text1)
    gates2 = _gate_lines(text2)
    assert gates1 == gates2, (
        f"intake mutation changed validator outcome:\n\n--- baseline ---\n{gates1}\n\n--- mutated ---\n{gates2}"
    )


# Test 3: An empty intake does not change verdict.
def test_validator_outcome_with_empty_intake(tmp_path: Path):
    """An empty `01_INTAKE.md` (stub) must produce the same verdict as a fully
    populated one. The validator must not derive data from the intake."""
    # Empty intake — just stub.
    (tmp_path / "01_INTAKE.md").write_text("# stub\n", encoding="utf-8")
    (tmp_path / "07_CLOSEOUT.md").write_text(CANON_V11_BODY, encoding="utf-8")
    rc, text = _run_validator(tmp_path)
    # The structural gates must PASS. The non-claim must PASS.
    passes = set(
        re.findall(r"^\s*(?:\[[A-Za-z0-9]+\]\s*)?PASS\s+(\S+):", text, re.MULTILINE)
    )
    expected = {
        "adv-block-exists",
        "adv-level-valid",
        "adv-a2-identity",
        "adv-a2-distinct",
        "adv-campaign-ref",
        "adv-corpus-version",
        "adv-surfaces-declared",
        "adv-surfaces-unexplored",
        "adv-residual-uncertainty",
        "adv-findings-shape",
        "adv-verdict-shape",
        "adv-non-claim",
    }
    assert expected.issubset(passes), (
        f"expected {expected} to be in PASSES, got {passes}"
    )
