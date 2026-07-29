"""Corpus entry for ADVR-RT-02.

Origin: docs/runs/2026-07-30_0100_a2-auth-certification-of-m3-remediation/07_CLOSEOUT.md
Severity: S3
Confidence: CONFIRMED
State: ARBITRATED (deferred, not remediated)
Oracle: `level: '  A2  '` is silently accepted; the validator strips whitespace
        instead of rejecting or warning.

Registered under ADVERSARIAL_ASSURANCE_GOVERNANCE.md §9 destination 6, mandatory
for every CONFIRMED finding regardless of severity.

Behaviour pin, not a regression guard for a fix: the defect is open, so there is
no fails_before/passes_after lock to encode. A green run means "the known defect
is still exactly as documented".
"""


def _closeout(level_literal: str) -> str:
    return (
        "```yaml\n"
        "adversarial:\n"
        f"  level: {level_literal}\n"
        '  campaign_ref: "corpus-advr-rt-02"\n'
        '  corpus_version: "v1.1"\n'
        "  exploration_performed: true\n"
        '  surfaces_declared: ["fixture"]\n'
        "  surfaces_unexplored: []\n"
        '  residual_uncertainty: "fixture"\n'
        "  findings: []\n"
        '  verdict: "NOT_ASSESSED"\n'
        "```\n"
    )


def test_advr_rt_02_level_whitespace_is_silently_accepted(adversarial_gate):
    """Pin: a padded level still validates, with no warning."""
    gate = adversarial_gate

    passes, fails = gate.check_adversarial_block(
        _closeout("'  A2  '"), "corpus-advr-rt-02"
    )
    by_id = {result.gate_id: result for result in passes + fails}

    level_gate = by_id.get("adv-level-valid")
    assert level_gate is not None and level_gate.verdict == "PASS", (
        "ADVR-RT-02 appears remediated: a padded level no longer passes. "
        "Rewrite this entry as a real regression guard and move the finding out "
        "of ARBITRATED."
    )
    # The padding is erased rather than reported: no evidence mentions it.
    assert not any("  A2  " in item for item in level_gate.evidence), (
        "the validator now surfaces the raw padded value; ADVR-RT-02 must be "
        "re-arbitrated"
    )


def test_advr_rt_02_clean_level_is_indistinguishable_from_padded(adversarial_gate):
    """Pin: the padded and clean forms produce the same verdict and evidence."""
    gate = adversarial_gate

    padded_passes, _ = gate.check_adversarial_block(
        _closeout("'  A2  '"), "corpus-advr-rt-02"
    )
    clean_passes, _ = gate.check_adversarial_block(
        _closeout('"A2"'), "corpus-advr-rt-02"
    )

    def level_evidence(results):
        for result in results:
            if result.gate_id == "adv-level-valid":
                return result.verdict, result.evidence
        return None, None

    assert level_evidence(padded_passes) == level_evidence(clean_passes), (
        "padded and clean levels are now distinguishable; ADVR-RT-02 must be "
        "re-arbitrated"
    )
