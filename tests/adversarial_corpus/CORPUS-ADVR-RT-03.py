"""Corpus entry for ADVR-RT-03.

Origin: docs/runs/2026-07-30_0100_a2-auth-certification-of-m3-remediation/07_CLOSEOUT.md
Severity: S3
Confidence: CONFIRMED
State: ARBITRATED (deferred, not remediated)
Oracle: CERTIFIED condition 6.3.10 ("revocation_mechanism declared") is listed
        in the canon but never mechanically verified by the validator.

Registered under ADVERSARIAL_ASSURANCE_GOVERNANCE.md §9 destination 6, mandatory
for every CONFIRMED finding regardless of severity.

Behaviour pin, not a regression guard for a fix: the defect is open. A green run
means "the condition is still declarative only".
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GATE_SOURCE = REPO_ROOT / "tools" / "vbb-adversarial-gate.py"


def test_advr_rt_03_revocation_mechanism_is_listed_but_unverified(adversarial_gate):
    """Pin: 6.3.10 exists as text, and no gate_id enforces it."""
    gate = adversarial_gate

    listed = [c for c in gate.CERTIFIED_CONDITIONS if "revocation_mechanism" in c]
    assert listed, (
        "6.3.10 disappeared from CERTIFIED_CONDITIONS; ADVR-RT-03 must be re-arbitrated"
    )

    source = GATE_SOURCE.read_text(encoding="utf-8")
    gate_ids = set(re.findall(r'gate_id="([^"]+)"', source))
    enforcing = {gid for gid in gate_ids if "revocation" in gid.lower()}
    assert not enforcing, (
        f"ADVR-RT-03 appears remediated: {sorted(enforcing)} now enforces "
        "revocation_mechanism. Rewrite this entry as a real regression guard "
        "and move the finding out of ARBITRATED."
    )


def test_advr_rt_03_certification_passes_without_revocation_mechanism(adversarial_gate):
    """Pin: the only mentions of revocation_mechanism are declarative."""
    gate = adversarial_gate
    source = GATE_SOURCE.read_text(encoding="utf-8")

    mentions = [
        line.strip() for line in source.splitlines() if "revocation_mechanism" in line
    ]
    assert mentions, "the term vanished entirely; ADVR-RT-03 must be re-arbitrated"
    assert all(line.lstrip().startswith(('"', "#", "'")) for line in mentions), (
        f"revocation_mechanism is now read as data rather than quoted text: "
        f"{mentions} — ADVR-RT-03 must be re-arbitrated"
    )
    # Sanity: the condition list itself is still the 13-item canon.
    assert len(gate.CERTIFIED_CONDITIONS) == 13
