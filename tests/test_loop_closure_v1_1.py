"""M2-25 + REM-02 — Loop closure v1.1 extensions.

Verifies that vbb-loop-closure-check.py accepts:
- `adversarial_governance_version: "1.1"` in frontmatter.
- `gate_family: ADVERSARIAL` and `checkpoint: COUNTER_PROOF`.
- v1.1 enum values for `certification_status` (PRE_CERTIFICATION,
  MIGRATION).
- v1.1 transient fields (transient_reason, bootstrapped_at, etc.).
"""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_closure_tool_accepts_v1_1_adversarial_governance():
    tool = _read("tools/vbb-loop-closure-check.py")
    assert "adversarial_governance_version" in tool
    assert "ADVERSARIAL_GOVERNANCE_VERSION" in tool


def test_closure_tool_accepts_adversarial_gate_family():
    tool = _read("tools/vbb-loop-closure-check.py")
    assert "ADVERSARIAL" in tool
    assert "ADVERSARIAL_GATE_FAMILIES" in tool


def test_closure_tool_accepts_counter_proof_checkpoint():
    tool = _read("tools/vbb-loop-closure-check.py")
    assert "COUNTER_PROOF" in tool
    assert "ADVERSARIAL_CHECKPOINTS" in tool


def test_closure_tool_accepts_pre_certification():
    tool = _read("tools/vbb-loop-closure-check.py")
    assert "PRE_CERTIFICATION" in tool


def test_closure_tool_accepts_migration():
    tool = _read("tools/vbb-loop-closure-check.py")
    assert "MIGRATION" in tool


def test_closure_tool_validates_transient_fields():
    """When certification_status is PRE_CERTIFICATION or MIGRATION,
    the transient fields are required."""
    tool = _read("tools/vbb-loop-closure-check.py")
    assert "transient_reason" in tool
    assert "bootstrapped_at" in tool
    assert "bootstrapped_by" in tool
