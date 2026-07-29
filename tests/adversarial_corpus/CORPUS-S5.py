"""Corpus entry for S5.

Origin: docs/runs/2026-07-29_1130_gcg-genericity-stress-test/07_CLOSEOUT.md
Severity: S2
Confidence: CONFIRMED
State: DETECTED (open, not remediated)
Oracle: two resolvers disagree on what "the closeout of a run" is.
        `find_closeout()` falls back to any `*CLOSEOUT*.md`; the knowledge rule
        hardcodes `07_CLOSEOUT.md`. On the real run
        `2026-07-28_1200_m1-adversarial-loop-normative-arbitration`, which holds
        `02_CLOSEOUT.md`, the same run both has and has not a closeout.

Registered under ADVERSARIAL_ASSURANCE_GOVERNANCE.md §9 destination 6.

This entry is a **behaviour pin**. The severity is structural rather than
observable: PENDING_LIFECYCLE is attributed on the *absence* of the
evidence-bearing artifact, so a resolver-dependent absence is an I6 bypass by
naming — a route the strict limit of model §4.1 does not cover, because that
limit governs the reason, not the resolution. A green run means "the two
resolvers still disagree as documented".
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DIVERGENT_RUN = (
    REPO_ROOT
    / "docs"
    / "runs"
    / "2026-07-28_1200_m1-adversarial-loop-normative-arbitration"
)


def test_s5_the_divergent_run_still_holds_a_non_canonical_closeout():
    """Pin the witness itself: without it the finding has no observable instance."""
    assert DIVERGENT_RUN.is_dir(), (
        "the witness run disappeared; S5 must be re-arbitrated against another "
        "instance or closed"
    )
    assert not (DIVERGENT_RUN / "07_CLOSEOUT.md").exists(), (
        "the witness run was renamed to the canonical closeout: S5 may be "
        "remediated by normalisation — re-arbitrate before deleting this pin"
    )
    assert (DIVERGENT_RUN / "02_CLOSEOUT.md").exists(), (
        "the witness run no longer holds 02_CLOSEOUT.md; S5 must be re-arbitrated"
    )


def test_s5_the_two_resolvers_disagree():
    """Pin: one resolver finds a closeout where the other reports none."""
    import sys

    sys.path.insert(0, str(REPO_ROOT / "tools"))
    from vbb_run_resolution import find_closeout

    permissive = find_closeout(DIVERGENT_RUN)
    strict = DIVERGENT_RUN / "07_CLOSEOUT.md"

    assert permissive is not None and permissive.name == "02_CLOSEOUT.md", (
        "find_closeout stopped accepting the non-canonical name; the resolvers "
        "may have converged — re-arbitrate S5 and rewrite this entry"
    )
    assert not strict.exists(), (
        "the hardcoded resolver now finds a closeout too; the resolvers may have "
        "converged — re-arbitrate S5"
    )


def test_s5_the_permissive_resolver_is_the_one_gcg_uses(governance_compat):
    """The direction matters: GCG sees a closeout the rule-B enforcer does not.

    That is what makes the divergence exploitable rather than merely untidy — a
    run can be judged on an artifact the governing rule does not even consider.
    """
    assert hasattr(governance_compat, "find_closeout"), (
        "the scanner no longer imports find_closeout; its resolution changed and "
        "S5 must be re-arbitrated"
    )
