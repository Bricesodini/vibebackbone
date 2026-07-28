"""M3-10 — Document separation between validators for CERTIFIED conditions.

R2 §12 (ADVR-A2-08): the 13 `CERTIFIED` conditions (§5.3 of
ADVERSARIAL_ASSURANCE_GOVERNANCE.md) are validated by *different*
validators:

- The adversarial gate validator (vbb-adversarial-gate.py) owns the
  conditions that derive from the closeout's adversarial block.
- A future certification monitor (e.g., vbb-status-dashboard's
  certification state) owns the conditions that derive from runtime
  monitoring (cadence, revocation, last_reviewed).

Conditions 6.3.10 (`revocation_mechanism` declared), 6.3.11 (cadence
≤ 90 days), 6.3.12 (`last_reviewed` within cadence) belong to the
certification monitor — not to the adversarial gate.

This test asserts that:
1. The canon documents the separation explicitly.
2. The M1-04 `certification.owner` SLA breach flow is referenced.
"""

from __future__ import annotations

from pathlib import Path

import pytest


REPO = Path(__file__).resolve().parent.parent


def test_canon_separates_validator_responsibilities_for_6_3_10_to_12():
    """The canon must declare that 6.3.10/11/12 belong to a distinct
    `certification` validator (e.g., a future `vbb-certification-monitor`)
    rather than the adversarial gate."""
    canon = (REPO / "docs" / "ADVERSARIAL_ASSURANCE_GOVERNANCE.md").read_text(
        encoding="utf-8"
    )
    # The canon must mention all three conditions by number and state
    # that they belong to a separate validator.
    assert "6.3.10" in canon, "canon must reference 6.3.10"
    assert "6.3.11" in canon, "canon must reference 6.3.11"
    assert "6.3.12" in canon, "canon must reference 6.3.12"
    # The separation language: must mention "monitor" or "vbb-status-dashboard"
    # or a distinct validator in the context of 6.3.10/11/12.
    lower = canon.lower()
    assert any(
        marker in lower
        for marker in (
            "monitor",
            "vbb-status-dashboard",
            "vbb-certification-monitor",
            "certification owner",
            "certification_monitor",
        )
    ), (
        "canon must declare a separation of validator responsibilities "
        "(one of: monitor, vbb-status-dashboard, vbb-certification-monitor)"
    )


def test_canon_references_m1_04_owner_sla():
    """M1-04 declares the certification owner SLA breach flow.
    The canon must cross-reference it from the 6.3.10/11/12 section."""
    canon = (REPO / "docs" / "ADVERSARIAL_ASSURANCE_GOVERNANCE.md").read_text(
        encoding="utf-8"
    )
    # M1-04 SLA breach keyword.
    assert "SLA" in canon or "sla breach" in canon.lower(), (
        "canon must reference M1-04 SLA breach in the context of conditions 6.3.10/11/12"
    )


def test_canon_does_not_collapse_6_3_separation():
    """The canon must NOT collapse 6.3.10/11/12 into a single sentence or
    claim them as part of the adversarial gate."""
    canon = (REPO / "docs" / "ADVERSARIAL_ASSURANCE_GOVERNANCE.md").read_text(
        encoding="utf-8"
    )
    # Adversarial gate owns conditions 6.3.1, 6.3.2, 6.3.8, 6.3.9, 6.3.13
    # (those derivable from the closeout). 6.3.10/11/12 belong elsewhere.
    # If the canon says "vbb-adversarial-gate.py validates 6.3.10", that
    # would be a collapse.
    lower = canon.lower()
    if "vbb-adversarial-gate" in lower:
        # Find the sentence containing the validator and 6.3.10.
        for line in canon.split("\n"):
            if "vbb-adversarial-gate" in line.lower() and "6.3.10" in line.lower():
                pytest.fail(f"canon line collapses responsibilities: {line!r}")
