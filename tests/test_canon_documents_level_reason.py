"""M3-03 — Canon documentation test for `level_reason`.

The `level_reason` field is required by:
- `docs/templates/01_INTAKE.md.template:71`
- `docs/templates/07_CLOSEOUT.md.template:88`
- `tools/vbb-adversarial-gate.py` (validation, gate `adv-a0-reason`)

But it is absent from `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md`. M3-03
closes this documentary contradiction by adding a normative declaration
to the canon.
"""

from __future__ import annotations

from pathlib import Path

import pytest


REPO = Path(__file__).resolve().parent.parent


def test_canon_documents_level_reason_field():
    canon = (REPO / "docs" / "ADVERSARIAL_ASSURANCE_GOVERNANCE.md").read_text(
        encoding="utf-8"
    )
    assert "level_reason" in canon, (
        "FAIL-BEFORE: `level_reason` is documented in templates and validated "
        "by vbb-adversarial-gate.py but absent from the canon. M3-03 closes "
        "this contradiction by declaring `level_reason` in the canon."
    )


def test_canon_documents_level_reason_for_a0():
    canon = (REPO / "docs" / "ADVERSARIAL_ASSURANCE_GOVERNANCE.md").read_text(
        encoding="utf-8"
    )
    # Either an explicit "level_reason for A0" sentence or, minimally,
    # the literal token "level_reason" appearing in an A0-related section.
    lower = canon.lower()
    assert "level_reason" in lower
    # Co-location: the same context must discuss A0 (case-insensitive).
    # Find line containing 'level_reason' and verify A0 is in the surrounding window.
    lines = lower.split("\n")
    for i, line in enumerate(lines):
        if "level_reason" in line:
            window = "\n".join(lines[max(0, i - 5) : i + 6])
            assert "a0" in window, (
                f"level_reason must be declared in an A0-related context (around line {i})"
            )
            return
    pytest.fail("level_reason not found in canon")


def test_canon_and_templates_level_reason_consistent():
    """The canon and the templates must declare the same set of fields.

    Sanity check: `level_reason` appears in templates but not in canon (FAIL-BEFORE)."""
    canon = (REPO / "docs" / "ADVERSARIAL_ASSURANCE_GOVERNANCE.md").read_text(
        encoding="utf-8"
    )
    tpl_intake = (REPO / "docs" / "templates" / "01_INTAKE.md.template").read_text(
        encoding="utf-8"
    )
    tpl_closeout = (REPO / "docs" / "templates" / "07_CLOSEOUT.md.template").read_text(
        encoding="utf-8"
    )
    assert "level_reason" in tpl_intake
    assert "level_reason" in tpl_closeout
    assert "level_reason" in canon, (
        "convergence: templates declare level_reason, validator enforces it, "
        "canon is silent -> closes with M3-03."
    )
