"""Corpus entry for ADVR-RT-01.

Origin: docs/runs/2026-07-30_0100_a2-auth-certification-of-m3-remediation/07_CLOSEOUT.md
Severity: S3
Confidence: CONFIRMED
State: ARBITRATED (deferred, not remediated)
Oracle: adv-block-exists reports PASS for an empty adversarial block; the real
        enforcement is delegated to adv-block-shape.

Registered under ADVERSARIAL_ASSURANCE_GOVERNANCE.md §9 destination 6, which is
mandatory for every CONFIRMED finding regardless of severity.

This entry is a **behaviour pin**, not a regression guard for a fix. The defect
is open, so there is no fails_before/passes_after lock to encode. The entry
asserts the current, defective behaviour so that it cannot change silently: the
day adv-block-exists is renamed or reordered, this entry fails and must be
rewritten as a real guard. A green run here means "the known defect is still
exactly as documented", never "the defect is fixed".
"""


def test_advr_rt_01_block_exists_passes_on_empty_block(adversarial_gate):
    """Pin: an empty adversarial block still yields adv-block-exists PASS."""
    gate = adversarial_gate
    closeout = "```yaml\nadversarial:\n```\n"

    passes, fails = gate.check_adversarial_block(closeout, "corpus-advr-rt-01")
    by_id = {result.gate_id: result for result in passes + fails}

    exists = by_id.get("adv-block-exists")
    assert exists is not None and exists.verdict == "PASS", (
        "ADVR-RT-01 appears remediated: adv-block-exists no longer passes on an "
        "empty block. Rewrite this entry as a real regression guard and move the "
        "finding out of ARBITRATED."
    )
    # The reason is factually wrong for a None-valued block — the observable
    # symptom of the finding, and the part most likely to change on a fix.
    assert any("non-empty mapping" in reason for reason in exists.reasons), (
        "the misleading PASS reason changed; ADVR-RT-01 must be re-arbitrated"
    )
    # Not a fail-open: enforcement really happens, just under other gate ids.
    assert any(result.verdict == "FAIL" for result in fails), (
        "no downstream gate rejects the empty block any more — this would turn "
        "a cosmetic S3 into a real fail-open"
    )
