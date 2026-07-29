"""Corpus entry for S3.

Origin: docs/runs/2026-07-29_1130_gcg-genericity-stress-test/07_CLOSEOUT.md
Severity: S1
Confidence: CONFIRMED
State: CLASSIFIED (specification repaired in model v2 §6.1, not implemented)
Oracle: the Compatibility Act is mono-rule by construction — one `rule_set`
        string, one flat `counts` table, one `current_conformance` ratio. It
        cannot represent an artifact that is OVERCLAIM under one rule and
        compliant under another, and the ratio is meaningless across rules with
        different populations.

Registered under ADVERSARIAL_ASSURANCE_GOVERNANCE.md §9 destination 6.

This entry is a **behaviour pin**. Model v2 specifies the multi-rule act; no
code implements it. The pin asserts the mono-rule shape, so the day the act
gains a per-rule structure it fails and must be rewritten as a real guard. A
green run means "the act is still mono-rule as documented", never "S3 is fixed".
"""


def test_s3_the_act_is_mono_rule(governance_compat):
    """Pin: one rule identifier, one classification table, one ratio."""
    act = governance_compat.build_act([])

    assert isinstance(act.get("rule_set"), str), (
        "rule_set is no longer a single string; the act may have become "
        "multi-rule — rewrite this entry as a regression guard and close S3"
    )
    assert "rules" not in act, (
        "the act gained a `rules` collection: model v2 §6.1 appears implemented. "
        "S3 must be re-arbitrated and this pin rewritten."
    )
    assert isinstance(act.get("counts"), dict), (
        "counts changed shape; S3 must be re-arbitrated"
    )
    assert isinstance(act.get("current_conformance"), str), (
        "current_conformance is no longer a single global ratio; S3 may be "
        "remediated — re-arbitrate before deleting this pin"
    )


def test_s3_the_act_still_refuses_to_derive_certification(governance_compat):
    """Not a fail-open: the mono-rule act is wrong about scope, not about
    certification.

    S3 is a representation defect. If fixing the shape ever silently reintroduced
    a derived certification, the cure would be worse than the disease — so the
    pin holds that line too.
    """
    act = governance_compat.build_act([])

    assert act["certification"] == "NOT_DERIVABLE_FROM_THIS_GATE", (
        "the act started deriving a certification; this is a regression on I4, "
        "far more serious than S3 itself"
    )
