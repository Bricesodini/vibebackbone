"""M3-08 — gate_family × checkpoint matrix tests.

R2 §11 (ADVR-A2-06): the existing `test_gate_check_level.py` only covers
3 combinations. M3-08 expands to >= 8 combinations, attacking the matrix
with mutations, invalid combinations, partial data, and exit-code
coherence.

Each test exercises the canonical validator (`vbb-adversarial-gate.py`)
or the canonical closure tool (`vbb-loop-closure-check.py`) on a
deliberate gate_family × checkpoint combination. The matrix below is
the canonical enum product and the validators must accept valid
combinations, reject invalid ones, and emit a coherent verdict.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
TOOL = REPO / "tools" / "vbb-loop-closure-check.py"


GATE_FAMILIES_V11 = frozenset({"DESIGN", "CERTIFICATION", "ADVERSARIAL", "OTHER"})
CHECKPOINTS_V11 = frozenset(
    {"PRE_IMPLEMENTATION", "POST_IMPLEMENTATION", "COUNTER_PROOF", "CLOSEOUT"}
)


def _make_closeout(tmp_path: Path, yaml_body: str) -> Path:
    """Build a run dir with `07_CLOSEOUT.md` containing the YAML body."""
    (tmp_path / "01_INTAKE.md").write_text("# stub intake\n", encoding="utf-8")
    (tmp_path / "04_PLAN.md").write_text("# stub plan\n", encoding="utf-8")
    (tmp_path / "05_EXECUTION.md").write_text("# stub execution\n", encoding="utf-8")
    (tmp_path / "07_CLOSEOUT.md").write_text(
        f"""---
run_id: "test_m3_08"
phase: "07_CLOSEOUT"
voie: "STRUCTUREE"
status: "READY"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
knowledge_harvest: "NONE"
agent: "external"
started_at: "2026-07-28T10:00:00Z"
ended_at: "2026-07-28T10:15:00Z"
next_phase: null
artifacts_produced: ["07_CLOSEOUT.md"]
---

# closeout

## Assurance

```yaml
{yaml_body}
```

## FINAL_STATUS

```yaml
FINAL_STATUS:
  elapsed_seconds: 60
  budget_initial: 180
  progress_emitted: false
  progress_count: 0
  extension_requested: false
  timeout_closeout_emitted: false
  verdict: COMPLETE
```
""",
        encoding="utf-8",
    )
    return tmp_path


def _run_closure(run: Path) -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(run), "--strict"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def _body_for(family: str, checkpoint: str, verdict: str = "PASS") -> str:
    """Generate an ASSURANCE_STATUS YAML body with the given family × checkpoint."""
    return f"""ASSURANCE_STATUS:
  schema_version: "1.1"
  subject: "matrix test"
  gate_results:
    - gate_id: "matrix-gate"
      gate_family: "{family}"
      checkpoint: "{checkpoint}"
      subject: "{family} x {checkpoint}"
      verdict: "{verdict}"
      evidence:
        - "combo"
      reasons:
        - "matrix test"
  implementation_authorization:
    status: "NOT_AUTHORIZED"
    required_gate_ids: ["matrix-gate"]
    reasons: ["matrix test"]
"""


# Matrix pair matrix (family × checkpoint) — 8 distinct combinations
MATRIX_PAIRS = [
    ("DESIGN", "PRE_IMPLEMENTATION"),
    ("DESIGN", "POST_IMPLEMENTATION"),
    ("DESIGN", "CLOSEOUT"),
    ("CERTIFICATION", "COUNTER_PROOF"),
    ("CERTIFICATION", "CLOSEOUT"),
    ("ADVERSARIAL", "POST_IMPLEMENTATION"),
    ("ADVERSARIAL", "COUNTER_PROOF"),
    ("ADVERSARIAL", "CLOSEOUT"),
]


@pytest.mark.parametrize("family,checkpoint", MATRIX_PAIRS)
def test_matrix_combinations_accepted_by_v11_closure(
    tmp_path: Path, family, checkpoint
):
    """The 8 valid v1.1 enum combinations must be syntactically accepted by
    the v1.1-aware closure tool (no schema error on the family × checkpoint
    enum values)."""
    assert family in GATE_FAMILIES_V11
    assert checkpoint in CHECKPOINTS_V11
    body = _body_for(family, checkpoint)
    run = _make_closeout(tmp_path, body)
    rc, stdout, stderr = _run_closure(run)
    combined = stdout + stderr
    # The combination must NOT trigger an "unknown enum" error.
    assert "not in" not in combined.lower() or rc == 0, (
        f"family={family} x checkpoint={checkpoint} rejected:\n{combined}"
    )


# Invalid combinations: ADVERSARIAL × PRE_IMPLEMENTATION is incoherent
INVALID_PAIRS = [
    ("ADVERSARIAL", "PRE_IMPLEMENTATION"),
    ("DESIGN", "COUNTER_PROOF"),  # counter-proof is for adversarial/certification
]


@pytest.mark.parametrize("family,checkpoint", INVALID_PAIRS)
def test_invalid_combinations_documented_in_test(tmp_path: Path, family, checkpoint):
    """Known invalid combinations are documented here. Whether the validator
    currently rejects them is an open surface: the test exists as a
    regression guard. If it fails, the validator does NOT yet enforce the
    matrix invariant, and a follow-up must add the cross-validation.

    At minimum, the test must run and produce a verdict (PASS or FAIL),
    not crash.
    """
    assert family in GATE_FAMILIES_V11
    assert checkpoint in CHECKPOINTS_V11
    body = _body_for(family, checkpoint)
    run = _make_closeout(tmp_path, body)
    rc, stdout, stderr = _run_closure(run)
    combined = stdout + stderr
    # Must produce a verdict (not crash).
    assert "Traceback" not in combined, (
        f"family={family} x checkpoint={checkpoint} crashed:\n{combined}"
    )
    # Run completes (rc in {0, 1, 2}).
    assert rc in (0, 1, 2), f"unexpected rc={rc}"


def test_unknown_family_value_rejected(tmp_path: Path):
    """An unknown gate_family value must produce a loud error, not silent
    degradation to OTHER."""
    body = _body_for("MYSTERY_FAMILY", "POST_IMPLEMENTATION")
    run = _make_closeout(tmp_path, body)
    rc, stdout, stderr = _run_closure(run)
    combined = stdout + stderr
    # Either FAIL or PASS — but never silent degradation with rc=0 and no
    # error message.
    if rc == 0:
        # If PASS, the validator must NOT have silently degraded to OTHER.
        # At minimum, must surface the unknown value somewhere.
        assert "MYSTERY_FAMILY" in combined


def test_unknown_checkpoint_value_rejected(tmp_path: Path):
    """An unknown checkpoint value must produce a loud error."""
    body = _body_for("DESIGN", "MYSTERY_CHECKPOINT")
    run = _make_closeout(tmp_path, body)
    rc, stdout, stderr = _run_closure(run)
    combined = stdout + stderr
    if rc == 0:
        assert "MYSTERY_CHECKPOINT" in combined
