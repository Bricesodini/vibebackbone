"""Corpus entry for S1.

Origin: docs/runs/2026-07-29_1130_gcg-genericity-stress-test/07_CLOSEOUT.md
Severity: S1
Confidence: CONFIRMED
State: DETECTED (open, not remediated)
Oracle: the compatibility scanner decides applicability from the run identity
        alone, while the canonical enforcer combines three sources by OR
        (identity, started_at, self-declaration). A subset of a disjunction is
        at most as inclusive, so the scanner can only under-report.

Registered under ADVERSARIAL_ASSURANCE_GOVERNANCE.md §9 destination 6.

This entry is a **behaviour pin**, not a regression guard for a fix. The defect
is open, so there is no fails_before/passes_after lock to encode. It asserts the
divergence as documented: the enforcer governs a self-declaring pre-cutover run,
the scanner does not. The day either predicate changes, this entry fails and the
finding must be re-arbitrated. A green run here means "the known divergence is
still exactly as documented", never "the scanner was aligned".
"""


def _write_run(tmp_path, name, intake, closeout=None):
    run_dir = tmp_path / name
    run_dir.mkdir()
    (run_dir / "01_INTAKE.md").write_text(intake, encoding="utf-8")
    if closeout is not None:
        (run_dir / "07_CLOSEOUT.md").write_text(closeout, encoding="utf-8")
    return run_dir


def test_s1_enforcer_governs_a_self_declaring_pre_cutover_run(loop_closure, tmp_path):
    """Source 3 of the applicability contract: self-declaration wins over date."""
    run_dir = _write_run(
        tmp_path,
        "2026-01-01_0000_long-before-any-cutover",
        '---\nknowledge_governance_version: "1.0"\n---\n',
    )
    intake, _ = loop_closure.read_frontmatter(run_dir / "01_INTAKE.md")

    assert loop_closure._knowledge_governance_required(run_dir, intake or {}, {}), (
        "the canonical enforcer stopped honouring self-declaration; S1 may be "
        "remediated from the enforcer side — re-arbitrate before deleting this pin"
    )


def test_s1_scanner_ignores_everything_but_the_run_identity(
    governance_compat, tmp_path
):
    """The scanner's own predicate: identity only, self-declaration ignored."""
    closeout = (
        "---\n"
        'adversarial_governance_version: "1.1"\n'
        "---\n"
        "```yaml\n"
        "adversarial:\n"
        '  level: "A2"\n'
        "```\n"
    )
    run_dir = _write_run(
        tmp_path,
        "2026-01-01_0000_long-before-any-cutover",
        '---\nadversarial_governance_version: "1.1"\n---\n',
        closeout,
    )

    result = governance_compat.classify_run(run_dir, {})

    assert result.category == governance_compat.HISTORICAL_VALID, (
        f"the scanner classified a self-declaring pre-cutoff run as "
        f"{result.category!r} instead of HISTORICAL_VALID. S1 may be remediated: "
        "rewrite this entry as a real regression guard and close the finding."
    )
    assert "predates applies_from" in result.reason, (
        "the classification reason changed; S1 must be re-arbitrated"
    )


def test_s1_divergence_is_permissive_not_strict(governance_compat):
    """The direction matters: a permissive gate hides failures, a strict one does not.

    HISTORICAL_VALID is outside BLOCKING, so the scanner's reading of a
    self-declaring pre-cutoff run cannot stop a merge, while the enforcer's
    reading can. That asymmetry is the whole severity of S1.
    """
    assert governance_compat.HISTORICAL_VALID not in governance_compat.BLOCKING, (
        "HISTORICAL_VALID became blocking; the direction of the S1 divergence "
        "changed and the finding must be re-arbitrated"
    )
