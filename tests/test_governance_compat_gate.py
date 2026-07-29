"""The Governance Compatibility Gate must not be satisfiable by relabelling.

GCG exists because a canon that evolves was making its own history
automatically false. The cure introduces a risk of its own: a category that
excuses non-compliance is a category people will reach for. These tests pin the
two properties that keep it honest.

1. The ledger cannot launder a current defect. An entry is honored only for
   runs that predate the birth of the enforcing tool. Anything produced when
   the checker already existed stays blocking, whatever the ledger says.

2. An unsupported positive claim outranks every historical reading. A run that
   declares PASS_ADVERSARIAL or CERTIFIED without a validatable block is
   OVERCLAIM — never debt, never UNKNOWN, never ledgerable.
"""

import importlib.util
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()

_spec = importlib.util.spec_from_file_location(
    "vbb_governance_compat", REPO_ROOT / "tools" / "vbb-governance-compat.py"
)
assert _spec and _spec.loader
gcg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gcg)


def _write_closeout(tmp_path: Path, run_id: str, body: str) -> Path:
    run_dir = tmp_path / run_id
    run_dir.mkdir(parents=True)
    (run_dir / "07_CLOSEOUT.md").write_text(body, encoding="utf-8")
    return run_dir


NO_BLOCK = '---\nrun_id: "x"\nstatus: "READY"\n---\n\n# closeout\n'
CLAIMS_PASS = (
    '---\nrun_id: "x"\nadversarial_status: PASS_ADVERSARIAL\n---\n\n# closeout\n'
)


def test_ledger_cannot_launder_a_post_enforcement_run(tmp_path):
    """A run created after the checker existed stays CURRENT_NONCOMPLIANCE.

    This is the anti-laundering rule. Without it, every current defect can be
    moved into historical debt by adding one ledger row, and the gate becomes a
    formality that records its own bypass.
    """
    birth = gcg.ADVERSARIAL_ENFORCEMENT_EFFECTIVE_FROM
    after = birth.replace(hour=birth.hour + 2)
    run_id = f"{after.strftime('%Y-%m-%d_%H%M')}_post-enforcement"
    run_dir = _write_closeout(tmp_path, run_id, NO_BLOCK)

    # The most permissive ledger entry available, aimed straight at this run.
    hostile_ledger = {run_id: gcg.HISTORICAL_NONCOMPLIANCE}

    result = gcg.classify_run(run_dir, hostile_ledger)

    assert result.category == gcg.CURRENT_NONCOMPLIANCE, (
        f"a ledger entry laundered a post-enforcement run into "
        f"{result.category!r}; the gate can be bypassed by editing a table"
    )
    assert result.category in gcg.BLOCKING


def test_ledger_is_honored_for_a_pre_enforcement_run(tmp_path):
    """The counterpart: the rule must not make the ledger useless.

    A run that predates the checker could not have satisfied it. Its arbitrated
    disposition is honored — that is the whole point of distinguishing debt
    from defect.
    """
    before = gcg.ADVERSARIAL_APPLIES_FROM.replace(
        hour=gcg.ADVERSARIAL_APPLIES_FROM.hour + 1
    )
    assert before < gcg.ADVERSARIAL_ENFORCEMENT_EFFECTIVE_FROM
    run_id = f"{before.strftime('%Y-%m-%d_%H%M')}_pre-enforcement"
    run_dir = _write_closeout(tmp_path, run_id, NO_BLOCK)

    ledgered = gcg.classify_run(run_dir, {run_id: gcg.HISTORICAL_NONCOMPLIANCE})
    assert ledgered.category == gcg.HISTORICAL_NONCOMPLIANCE

    unledgered = gcg.classify_run(run_dir, {})
    assert unledgered.category == gcg.UNKNOWN, (
        "an unarbitrated historical run must block, not pass silently"
    )


def test_overclaim_outranks_the_historical_reading(tmp_path):
    """A false PASS is not excused by being old."""
    before = gcg.ADVERSARIAL_APPLIES_FROM.replace(
        hour=gcg.ADVERSARIAL_APPLIES_FROM.hour + 1
    )
    run_id = f"{before.strftime('%Y-%m-%d_%H%M')}_claims-pass"
    run_dir = _write_closeout(tmp_path, run_id, CLAIMS_PASS)

    result = gcg.classify_run(run_dir, {run_id: gcg.HISTORICAL_NONCOMPLIANCE})

    assert result.category == gcg.OVERCLAIM, (
        f"a run declaring PASS_ADVERSARIAL without a block was classified "
        f"{result.category!r}; an unsupported claim must never be ledgerable"
    )


def test_pre_cutoff_runs_are_historically_valid(tmp_path):
    """A canon evolution does not retroactively invalidate what predates it."""
    long_before = datetime(2026, 6, 1, 9, 0)
    run_id = f"{long_before.strftime('%Y-%m-%d_%H%M')}_ancient"
    run_dir = _write_closeout(tmp_path, run_id, NO_BLOCK)

    result = gcg.classify_run(run_dir, {})

    assert result.category == gcg.HISTORICAL_VALID
    assert result.category not in gcg.BLOCKING


def test_open_run_is_pending_lifecycle_not_a_failure(tmp_path):
    """A run in progress must not fail the gate that its own work will satisfy.

    Learned from the POC: the current run enters its own population. Counting
    it as non-compliant makes the gate unsatisfiable during any run.
    """
    after = gcg.ADVERSARIAL_ENFORCEMENT_EFFECTIVE_FROM
    run_id = f"{after.strftime('%Y-%m-%d_%H%M')}_still-open"
    run_dir = tmp_path / run_id
    run_dir.mkdir(parents=True)
    (run_dir / "01_INTAKE.md").write_text("---\n---\n", encoding="utf-8")

    result = gcg.classify_run(run_dir, {})

    assert result.category == gcg.PENDING_LIFECYCLE
    assert result.category not in gcg.BLOCKING


def test_certification_is_never_derived_from_the_gate(tmp_path):
    """The three readings stay orthogonal: a green gate is not a certification."""
    act = gcg.build_act([gcg.Classification("r", gcg.CURRENT, "passes", 0)])

    assert act["verdict"] == "PASS"
    assert act["certification"] == "NOT_DERIVABLE_FROM_THIS_GATE", (
        "the gate emitted a certification reading derived from conformance"
    )


def test_pending_lifecycle_never_covers_an_existing_failing_artifact(tmp_path):
    """The strict limit of PENDING_LIFECYCLE (model §4.1, invariant I6).

    The category exists for artifacts whose evidence has not been produced yet.
    It must never absorb an artifact whose evidence exists and is insufficient
    — a closed run failing because it is waiting for an independent review is a
    defect, not a lifecycle step. Without this limit every failing run declares
    itself "awaiting a later step", and the category becomes the same
    self-issued exemption the ledger was stopped from being.
    """
    after = gcg.ADVERSARIAL_ENFORCEMENT_EFFECTIVE_FROM
    after = after.replace(hour=after.hour + 2)
    run_id = f"{after.strftime('%Y-%m-%d_%H%M')}_closed-but-awaiting-review"

    # A closeout that says, in its own words, that it is waiting for a later step.
    awaiting = (
        '---\nrun_id: "x"\nstatus: "PARTIAL"\n---\n\n'
        "# closeout\n\nFINAL_STATUS: HANDOFF\n"
        "next_action: awaiting an independent A2 review\n"
    )
    run_dir = _write_closeout(tmp_path, run_id, awaiting)

    result = gcg.classify_run(run_dir, {})

    assert result.category == gcg.CURRENT_NONCOMPLIANCE, (
        f"a closed run awaiting review was classified {result.category!r}; "
        "declaring a later step must not exempt an artifact that exists and fails"
    )
    assert result.category in gcg.BLOCKING


def test_debt_window_is_bounded_on_both_sides(tmp_path):
    """A debt disposition is admissible only between the two declared bounds.

    Before applies_from the rule did not exist (HISTORICAL_VALID); after
    enforcement_effective_from the failure is a defect. The window never widens
    toward the present, so nothing produced today can enter it.
    """
    assert gcg.ADVERSARIAL_APPLIES_FROM < gcg.ADVERSARIAL_ENFORCEMENT_EFFECTIVE_FROM

    before = gcg.ADVERSARIAL_APPLIES_FROM.replace(
        day=gcg.ADVERSARIAL_APPLIES_FROM.day - 1
    )
    outside_before = _write_closeout(
        tmp_path, f"{before.strftime('%Y-%m-%d_%H%M')}_before", NO_BLOCK
    )
    assert gcg.classify_run(outside_before, {}).category == gcg.HISTORICAL_VALID

    after = gcg.ADVERSARIAL_ENFORCEMENT_EFFECTIVE_FROM
    after = after.replace(hour=after.hour + 1)
    outside_after = _write_closeout(
        tmp_path, f"{after.strftime('%Y-%m-%d_%H%M')}_after", NO_BLOCK
    )
    hostile = {outside_after.name: gcg.HISTORICAL_NONCOMPLIANCE}
    assert (
        gcg.classify_run(outside_after, hostile).category == gcg.CURRENT_NONCOMPLIANCE
    )
