"""Tests for the shared run resolution (ADR-0027, TD-101).

Covers:
  * mixed naming schemes: mtime ordering beats the lexical trap
    (``20260615-x`` sorts lexically AFTER ``2026-07-13_y``);
  * the two selectors over their distinct populations — latest existing
    vs latest closed — and their normal divergence when the newest run
    has no closeout yet;
  * loop-closure auto-detection (subprocess, --runs-dir) selecting the
    latest existing run instead of the lexical maximum (TD-101 repro);
  * voie alias normalization (STRUCTURED → STRUCTUREE).
"""

import importlib.util
import os
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
MODULE = REPO_ROOT / "tools" / "vbb_run_resolution.py"
LOOP_CLOSURE = REPO_ROOT / "tools" / "vbb-loop-closure-check.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("vbb_run_resolution_test", MODULE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _make_run(runs_dir: Path, name: str, closed: bool, mtime: float) -> Path:
    run = runs_dir / name
    run.mkdir(parents=True)
    (run / "01_INTAKE.md").write_text(
        "---\nvoie: STRUCTUREE\n---\n# intake\n", encoding="utf-8"
    )
    if closed:
        (run / "07_CLOSEOUT.md").write_text(
            "---\nvoie: STRUCTUREE\nstatus: READY\n---\n# closeout\n",
            encoding="utf-8",
        )
    os.utime(run, (mtime, mtime))
    return run


def _mixed_population(tmp_path: Path) -> Path:
    """Three runs reproducing the TD-101 layout:

    * ``20260615-usage-audit``  — closed, OLDEST mtime, lexical MAXIMUM
    * ``2026-07-13_1717_closed`` — closed, middle mtime
    * ``2026-07-13_1811_active`` — NOT closed, newest mtime
    """
    runs = tmp_path / "runs"
    now = time.time()
    _make_run(runs, "20260615-usage-audit", closed=True, mtime=now - 3000)
    _make_run(runs, "2026-07-13_1717_closed", closed=True, mtime=now - 1000)
    _make_run(runs, "2026-07-13_1811_active", closed=False, mtime=now)
    return runs


def test_mtime_order_beats_lexical_trap(tmp_path: Path) -> None:
    res = _load_module()
    runs = _mixed_population(tmp_path)
    ordered = [d.name for d in res.list_runs_by_mtime(runs)]
    assert ordered == [
        "2026-07-13_1811_active",
        "2026-07-13_1717_closed",
        "20260615-usage-audit",
    ]
    # The lexical order would have put the stale run first — the TD-101 trap.
    assert max(ordered) == "20260615-usage-audit"


def test_order_survives_a_fresh_clone(tmp_path: Path) -> None:
    """Identical mtimes must not scramble the order (audit finding F19).

    A `git clone` stamps every directory with the checkout time, so mtime
    carries no chronology on CI. Sorting on it returned the June legacy run as
    "latest", and the adversarial gate then validated the wrong run.
    """
    res = _load_module()
    runs = tmp_path / "runs"
    checkout = time.time()
    # Deliberately created in an order that contradicts chronology, all sharing
    # one mtime, exactly as a fresh checkout produces them.
    for name in (
        "20260615-usage-audit",
        "2026-07-13_1717_closed",
        "20260602_0817_legacy",
        "2026-07-30_0700_newest",
    ):
        _make_run(runs, name, closed=True, mtime=checkout)

    # Asserted through latest_closed_run, which exists in both the old and the
    # new API, so this fails on the ordering itself rather than on a rename.
    latest = res.latest_closed_run(runs)
    assert latest is not None and latest.name == "2026-07-30_0700_newest", (
        f"selector returned {latest.name if latest else None} on identical "
        f"mtimes — the order collapsed to filesystem order"
    )
    ordered = [d.name for d in res.list_runs_by_mtime(runs)]
    assert ordered == [
        "2026-07-30_0700_newest",
        "2026-07-13_1717_closed",
        "20260615-usage-audit",
        "20260602_0817_legacy",
    ], f"unexpected order: {ordered}"


def test_undated_run_sorts_below_every_dated_run(tmp_path: Path) -> None:
    """A name carrying no parsable date must never win the selector."""
    res = _load_module()
    runs = tmp_path / "runs"
    now = time.time()
    _make_run(runs, "scratch-notes", closed=True, mtime=now)
    _make_run(runs, "2026-01-02_0300_dated", closed=True, mtime=now - 5000)

    ordered = [d.name for d in res.list_runs_chronological(runs)]
    assert ordered[0] == "2026-01-02_0300_dated", (
        f"an undated directory outranked a dated run: {ordered}"
    )


def test_impossible_date_is_not_an_identity(tmp_path: Path) -> None:
    """A name-shaped but invalid date falls back to the undated population."""
    res = _load_module()
    runs = tmp_path / "runs"
    assert res.run_identity_datetime(runs / "2026-13-45_9999_bogus") is None
    assert res.run_identity_datetime(runs / "2026-07-30_0700_ok") is not None


def test_selectors_have_distinct_populations(tmp_path: Path) -> None:
    res = _load_module()
    runs = _mixed_population(tmp_path)
    latest_existing = res.latest_existing_run(runs)
    latest_closed = res.latest_closed_run(runs)
    assert latest_existing is not None and latest_closed is not None
    # Normal divergence: the active run is the latest existing, the closed
    # population points one run back. Identity is NOT required (POC (b)≠(c)).
    assert latest_existing.name == "2026-07-13_1811_active"
    assert latest_closed.name == "2026-07-13_1717_closed"


def test_selectors_on_empty_and_missing_dir(tmp_path: Path) -> None:
    res = _load_module()
    missing = tmp_path / "does-not-exist"
    assert res.list_runs_by_mtime(missing) == []
    assert res.latest_existing_run(missing) is None
    assert res.latest_closed_run(missing) is None


def test_explicit_run_argument_normalizes_bare_id_and_exact_path(
    tmp_path: Path,
) -> None:
    """Release callers cannot obtain two subjects from ID and path forms."""
    res = _load_module()
    runs = tmp_path / "runs"
    run = _make_run(
        runs,
        "2026-07-29_1200_target",
        closed=True,
        mtime=time.time(),
    )

    assert res.resolve_explicit_run(runs, Path(run.name)) == run.resolve()
    assert res.resolve_explicit_run(runs, run) == run.resolve()


def test_explicit_run_argument_rejects_outside_or_ambiguous_paths(
    tmp_path: Path,
) -> None:
    """A matching basename outside docs/runs cannot be substituted."""
    res = _load_module()
    runs = tmp_path / "runs"
    run = _make_run(
        runs,
        "2026-07-29_1200_target",
        closed=True,
        mtime=time.time(),
    )
    outside = tmp_path / "outside" / run.name
    outside.mkdir(parents=True)

    assert res.resolve_explicit_run(runs, outside) is None
    assert res.resolve_explicit_run(runs, Path("missing") / run.name) is None


def test_bound_subject_requires_exact_run_and_full_commit(tmp_path: Path) -> None:
    """The existing certification.bound_to contract binds run ID and SHA."""
    res = _load_module()
    runs = tmp_path / "runs"
    run = _make_run(
        runs,
        "2026-07-29_1200_target",
        closed=True,
        mtime=time.time(),
    )
    subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "config", "user.name", "VBB Test"],
        check=True,
    )
    subprocess.run(
        [
            "git",
            "-C",
            str(tmp_path),
            "config",
            "user.email",
            "vbb@example.invalid",
        ],
        check=True,
    )
    (tmp_path / "baseline").write_text("candidate\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "baseline"], check=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "commit", "-m", "candidate"],
        check=True,
        capture_output=True,
    )
    commit = subprocess.run(
        ["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    (run / "07_CLOSEOUT.md").write_text(
        "```yaml\n"
        "adversarial:\n"
        "  certification:\n"
        "    bound_to:\n"
        f'      run_id: "{run.name}"\n'
        f'      commit: "{commit}"\n'
        '      corpus_version: "1"\n'
        "```\n",
        encoding="utf-8",
    )

    ok, reason = res.verify_bound_subject(run, commit)
    assert ok, reason
    assert res.verify_bound_subject(run, "b" * 40)[0] is False

    text = (run / "07_CLOSEOUT.md").read_text(encoding="utf-8")
    (run / "07_CLOSEOUT.md").write_text(
        text.replace(run.name, "2026-07-30_0700_other"),
        encoding="utf-8",
    )
    assert res.verify_bound_subject(run, commit)[0] is False


def test_bound_subject_rejects_invented_full_sha(tmp_path: Path) -> None:
    """Forty hexadecimal characters are not evidence of a Git commit."""
    res = _load_module()
    subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
    run = _make_run(
        tmp_path / "runs",
        "2026-07-29_1200_target",
        closed=True,
        mtime=time.time(),
    )
    invented = "a" * 40
    (run / "07_CLOSEOUT.md").write_text(
        "```yaml\n"
        "adversarial:\n"
        "  certification:\n"
        "    bound_to:\n"
        f'      run_id: "{run.name}"\n'
        f'      commit: "{invented}"\n'
        "```\n",
        encoding="utf-8",
    )
    ok, reason = res.verify_bound_subject(run, invented)
    assert ok is False
    assert "not a Git commit object" in reason


def test_find_closeout_fallback(tmp_path: Path) -> None:
    res = _load_module()
    run = tmp_path / "run"
    run.mkdir()
    assert res.find_closeout(run) is None
    fallback = run / "CLOSEOUT.md"
    fallback.write_text("# wip closeout\n", encoding="utf-8")
    assert res.find_closeout(run) == fallback
    canonical = run / "07_CLOSEOUT.md"
    canonical.write_text("# canonical\n", encoding="utf-8")
    assert res.find_closeout(run) == canonical


def test_loop_closure_autodetect_uses_latest_existing(tmp_path: Path) -> None:
    """TD-101 non-regression: auto-detection must select the newest run by
    mtime, not the lexical maximum ``20260615-usage-audit``."""
    runs = _mixed_population(tmp_path)
    env = {k: v for k, v in os.environ.items() if k != "VBB_RUN_ID"}
    proc = subprocess.run(
        [sys.executable, str(LOOP_CLOSURE), "--runs-dir", str(runs)],
        capture_output=True,
        text=True,
        env=env,
    )
    assert "2026-07-13_1811_active" in proc.stderr
    assert "20260615-usage-audit" not in proc.stderr


def test_loop_closure_normalizes_voie_alias(tmp_path: Path) -> None:
    """`voie: STRUCTURED` (canonical English route name) is accepted as
    STRUCTUREE instead of failing with `unknown voie` (TD-101 evidence)."""
    runs = tmp_path / "runs"
    run = runs / "2026-07-13_1900_alias"
    run.mkdir(parents=True)
    (run / "01_INTAKE.md").write_text(
        "---\nvoie: STRUCTURED\n---\n# intake\n", encoding="utf-8"
    )
    env = {k: v for k, v in os.environ.items() if k != "VBB_RUN_ID"}
    proc = subprocess.run(
        [
            sys.executable,
            str(LOOP_CLOSURE),
            "2026-07-13_1900_alias",
            "--runs-dir",
            str(runs),
        ],
        capture_output=True,
        text=True,
        env=env,
    )
    combined = proc.stdout + proc.stderr
    assert "unknown voie" not in combined
    # The run legitimately FAILs on missing artifacts (no plan/exec/closeout),
    # but the voie must resolve to STRUCTUREE.
    assert "STRUCTUREE" in combined
