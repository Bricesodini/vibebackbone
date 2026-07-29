"""Corpus entry for S4.

Origin: docs/runs/2026-07-29_1130_gcg-genericity-stress-test/07_CLOSEOUT.md
Severity: S1
Confidence: CONFIRMED
State: CLASSIFIED (specification repaired in model v2 §3.6, not implemented)
Oracle: the scanner has no notion of population. It assumes every member is
        dated and immutable, and returns a blocking UNKNOWN for anything it
        cannot date — so an undated but fully compliant population (the 67
        skills of ADR 0042) would be reported entirely non-conformant.

Registered under ADVERSARIAL_ASSURANCE_GOVERNANCE.md §9 destination 6.

This entry is a **behaviour pin**. It asserts the false-positive as documented:
an undatable artifact is blocking, not out of population. The day §3.6 is
implemented this entry fails and must be rewritten as a real guard. A green run
means "the population contract is still missing", never "S4 is fixed".
"""


def test_s4_an_undatable_artifact_is_blocking_not_out_of_population(
    governance_compat, tmp_path
):
    """Pin: the scanner cannot say "this artifact is not in my population"."""
    artifact = tmp_path / "1-vbb-conventions"
    artifact.mkdir()
    (artifact / "SKILL.md").write_text("## Purpose\n", encoding="utf-8")

    result = governance_compat.classify_run(artifact, {})

    assert result.category == governance_compat.UNKNOWN, (
        f"an undatable artifact now classifies as {result.category!r}. A "
        "population contract may be implemented — re-arbitrate S4 and rewrite "
        "this entry as a regression guard."
    )
    assert result.category in governance_compat.BLOCKING, (
        "UNKNOWN stopped being blocking; the S4 false-positive changed shape "
        "and the finding must be re-arbitrated"
    )
    assert "identity is not parsable" in result.reason, (
        "the reason changed; S4 must be re-arbitrated"
    )


def test_s4_the_act_declares_no_population_properties(governance_compat):
    """Pin: nothing in the act states dated / immutable / enumerable."""
    act = governance_compat.build_act([])

    assert "population" not in act, (
        "the act gained a `population` declaration: model v2 §3.6 appears "
        "implemented. S4 must be re-arbitrated and this pin rewritten."
    )
    for prop in ("dated", "immutable", "enumerable"):
        assert prop not in act, (
            f"the act declares {prop!r}; the population contract appears "
            "implemented and S4 must be re-arbitrated"
        )
