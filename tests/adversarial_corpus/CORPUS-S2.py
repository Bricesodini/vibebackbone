"""Corpus entry for S2.

Origin: docs/runs/2026-07-29_1130_gcg-genericity-stress-test/07_CLOSEOUT.md
Severity: S1
Confidence: CONFIRMED
State: DETECTED (open, not remediated)
Oracle: a run identity carries no declared timezone, and the corpus contains
        two conventions — identity in local time (identity - started_at = +2h)
        and identity in UTC (+0h) — on either side of the adversarial cutover.
        The debt window of adversarial 1.1 is six hours wide; the ambiguity is
        worth two.

Registered under ADVERSARIAL_ASSURANCE_GOVERNANCE.md §9 destination 6.

This entry is a **behaviour pin**. It asserts that both conventions are still
present in the corpus, so the ambiguity cannot be silently resolved — by
normalising the corpus, by declaring the unit, or by drift — without failing
here. A green run means "the frontier is still ambiguous as documented".
"""

from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNS_DIR = REPO_ROOT / "docs" / "runs"

# Restricted to the window where the two conventions actually collide: the runs
# that define the adversarial cutover and the runs it governs.
WINDOW_START = "2026-07-26"


def _identity_minus_started_at(loop_closure, run_dir):
    """Offset in hours between the run identity and its declared start."""
    import sys

    sys.path.insert(0, str(REPO_ROOT / "tools"))
    from vbb_run_resolution import run_identity_datetime

    identity = run_identity_datetime(run_dir)
    if identity is None:
        return None
    for artifact in ("01_INTAKE.md", "07_CLOSEOUT.md"):
        path = run_dir / artifact
        if not path.exists():
            continue
        frontmatter, _ = loop_closure.read_frontmatter(path)
        started_at = (frontmatter or {}).get("started_at")
        if not started_at:
            continue
        if isinstance(started_at, datetime):
            parsed = started_at
        else:
            try:
                parsed = datetime.fromisoformat(str(started_at).replace("Z", "+00:00"))
            except ValueError:
                continue
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        utc = parsed.astimezone(timezone.utc)
        return (identity.replace(tzinfo=timezone.utc) - utc).total_seconds() / 3600
    return None


def test_s2_both_identity_conventions_coexist_in_the_corpus(loop_closure):
    """Pin: the same field is written in local time by some runs, UTC by others."""
    offsets = {}
    for run_dir in sorted(p for p in RUNS_DIR.iterdir() if p.is_dir()):
        if run_dir.name < WINDOW_START:
            continue
        offset = _identity_minus_started_at(loop_closure, run_dir)
        if offset is not None:
            offsets[run_dir.name] = offset

    local_convention = [n for n, o in offsets.items() if 1.9 <= o <= 2.1]
    utc_convention = [n for n, o in offsets.items() if abs(o) < 0.1]

    assert local_convention, (
        "no run writes its identity in local time any more; the corpus may have "
        "been normalised. S2 must be re-arbitrated and this pin rewritten."
    )
    assert utc_convention, (
        "no run writes its identity in UTC any more; the corpus may have been "
        "normalised. S2 must be re-arbitrated and this pin rewritten."
    )


def test_s2_the_cutover_is_declared_in_two_units(loop_closure):
    """Pin: the same frontier exists as a run-identity key and as a UTC instant.

    Nothing in the canon states that the two denote the same instant — that is
    the finding. The pin fails the day one of the two disappears, which is what
    a real remediation would look like.
    """
    key = loop_closure.ADVERSARIAL_GOVERNANCE_CUTOVER_KEY
    at = loop_closure.ADVERSARIAL_GOVERNANCE_CUTOVER_AT

    assert isinstance(key, str) and key == "2026-07-28_1400", (
        "the identity-shaped bound changed; S2 must be re-arbitrated"
    )
    assert at.tzinfo is not None, (
        "the instant-shaped bound lost its timezone; S2 must be re-arbitrated"
    )
    # The declared unit is the whole point: a run identity has none, the
    # datetime has UTC. Nothing reconciles them.
    assert at == datetime(2026, 7, 28, 14, 0, tzinfo=timezone.utc), (
        "the instant-shaped bound moved; S2 must be re-arbitrated"
    )


def test_s2_day_granularity_identities_are_still_treated_as_instants():
    """Pin: an identity without an hour defaults to 00:00 — a 24h interval read
    as a point."""
    import sys

    sys.path.insert(0, str(REPO_ROOT / "tools"))
    from vbb_run_resolution import run_identity_datetime

    identity = run_identity_datetime(Path("20260615-usage-audit"))

    assert identity == datetime(2026, 6, 15, 0, 0), (
        "day-granularity identities are no longer collapsed to midnight; the "
        "S2 interval reading may be remediated — re-arbitrate before deleting"
    )
