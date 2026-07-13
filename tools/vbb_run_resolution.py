"""VBB shared run resolution (ADR-0027, TD-101).

Single source of truth for resolving "the current run" from docs/runs/,
shared by vbb-status-dashboard.py, vbb-loop-closure-check.py and the CI
path (which invokes those tools).

Two explicit selectors over two distinct populations — never assumed equal:

  * latest_existing_run — newest directory by mtime, whole population.
    Consumer: loop-closure auto-detection (the run being worked on).
  * latest_closed_run   — newest directory by mtime that has a closeout.
    Consumer: dashboard "latest runs" listing.

Sort key is the directory mtime, never the lexical name: mixed naming
schemes (``20260615-usage-audit`` vs ``2026-07-13_1811_slug``) make the
lexical order wrong (TD-101).
"""

from pathlib import Path
from typing import List, Optional

__all__ = [
    "list_runs_by_mtime",
    "latest_existing_run",
    "latest_closed_run",
    "find_closeout",
]


def list_runs_by_mtime(runs_dir: Path) -> List[Path]:
    """All run directories under ``runs_dir``, newest mtime first.

    Loose files (README.md, stray reports) are excluded: a run is a directory.
    """
    if not runs_dir.exists():
        return []
    run_dirs = [d for d in runs_dir.iterdir() if d.is_dir()]
    run_dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
    return run_dirs


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
    """Selector « dernier run existant » — newest run dir by mtime,
    closed or not. Population: every run directory."""
    runs = list_runs_by_mtime(runs_dir)
    return runs[0] if runs else None


def latest_closed_run(runs_dir: Path) -> Optional[Path]:
    """Selector « dernier run clôturé » — newest run dir by mtime that has
    a closeout artifact. Population: closed runs only (dashboard's)."""
    for run_dir in list_runs_by_mtime(runs_dir):
        if find_closeout(run_dir) is not None:
            return run_dir
    return None
