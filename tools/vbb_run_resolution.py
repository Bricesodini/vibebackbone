"""VBB shared run resolution (ADR-0027, TD-101).

Single source of truth for resolving "the current run" from docs/runs/,
shared by vbb-status-dashboard.py, vbb-loop-closure-check.py,
vbb-adversarial-gate.py and the CI path (which invokes those tools).

Two explicit selectors over two distinct populations — never assumed equal:

  * latest_existing_run — newest run, whole population.
    Consumer: loop-closure auto-detection (the run being worked on).
  * latest_closed_run   — newest run that has a closeout.
    Consumers: dashboard "latest runs" listing, adversarial gate --latest.

Ordering is the **run identity**: the ``YYYY-MM-DD_HHMM`` timestamp encoded in
the directory name, which is committed data. Directory mtime is used only as a
tiebreak for names that carry no parsable date.

Why not mtime (audit 2026-07-29, finding F19). The original implementation
sorted purely on ``st_mtime`` to avoid the lexical order, which mishandles mixed
naming schemes (``20260615-usage-audit`` vs ``2026-07-13_1811_slug``, TD-101).
But mtime is not chronology: in a fresh clone every directory carries the
checkout time, so the order is arbitrary. CI runs on fresh clones, so
``latest_closed_run`` there returned ``20260615-usage-audit`` — a June run with
no adversarial block — and the adversarial gate failed on the wrong run. The
defect stayed invisible while the only consumer in local CI was a non-blocking
warning. Parsing the identity fixes both problems: it is chronological *and*
immune to filesystem metadata.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

__all__ = [
    "list_runs_chronological",
    "list_runs_by_mtime",
    "latest_existing_run",
    "latest_closed_run",
    "find_closeout",
    "run_identity_datetime",
]

# Accepts the three naming schemes present in docs/runs/:
#   2026-07-30_0700_slug      2026-07-30 07:00
#   20260602_0817_slug        2026-06-02 08:17
#   20260615-usage-audit      2026-06-15 00:00
_RUN_ID_RE = re.compile(
    r"^(?P<year>\d{4})-?(?P<month>\d{2})-?(?P<day>\d{2})"
    r"(?:[_-](?P<hour>\d{2})(?P<minute>\d{2}))?"
)


def run_identity_datetime(run_dir: Path) -> Optional[datetime]:
    """Return the timestamp encoded in the run directory name, or None."""
    match = _RUN_ID_RE.match(run_dir.name)
    if not match:
        return None
    try:
        return datetime(
            int(match.group("year")),
            int(match.group("month")),
            int(match.group("day")),
            int(match.group("hour") or 0),
            int(match.group("minute") or 0),
        )
    except ValueError:
        # A name-shaped-but-impossible date (month 13, day 32) is not an identity.
        return None


def _sort_key(run_dir: Path) -> Tuple[int, float]:
    """Newest first: dated runs above undated ones, mtime only as a tiebreak."""
    identity = run_identity_datetime(run_dir)
    if identity is not None:
        return (1, identity.timestamp())
    try:
        return (0, run_dir.stat().st_mtime)
    except OSError:
        return (0, 0.0)


def list_runs_chronological(runs_dir: Path) -> List[Path]:
    """All run directories under ``runs_dir``, newest run identity first.

    Loose files (README.md, stray reports) are excluded: a run is a directory.
    """
    if not runs_dir.exists():
        return []
    run_dirs = [d for d in runs_dir.iterdir() if d.is_dir()]
    run_dirs.sort(key=_sort_key, reverse=True)
    return run_dirs


def list_runs_by_mtime(runs_dir: Path) -> List[Path]:
    """Deprecated alias kept for callers written against the old name.

    The ordering is no longer mtime-based; see ``list_runs_chronological``.
    """
    return list_runs_chronological(runs_dir)


def find_closeout(run_dir: Path) -> Optional[Path]:
    """Closeout artifact of a run: canonical 07_CLOSEOUT.md first, then any
    *CLOSEOUT*.md fallback (in-progress runs that write CLOSEOUT.md before
    the standard rename). Newest match wins."""
    canonical = run_dir / "07_CLOSEOUT.md"
    if canonical.exists():
        return canonical
    matches = [p for p in run_dir.glob("*CLOSEOUT*.md") if p.is_file()]
    if not matches:
        return None
    return max(matches, key=lambda p: p.stat().st_mtime)


def latest_existing_run(runs_dir: Path) -> Optional[Path]:
    """Selector « dernier run existant » — newest run by identity,
    closed or not. Population: every run directory."""
    runs = list_runs_chronological(runs_dir)
    return runs[0] if runs else None


def latest_closed_run(runs_dir: Path) -> Optional[Path]:
    """Selector « dernier run clôturé » — newest run by identity that has
    a closeout artifact. Population: closed runs only (dashboard's)."""
    for run_dir in list_runs_chronological(runs_dir):
        if find_closeout(run_dir) is not None:
            return run_dir
    return None
