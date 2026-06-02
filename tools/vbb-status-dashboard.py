#!/usr/bin/env python3
"""
VBB Status Dashboard — read-only terminal dashboard for Vibebackbone repo health.

Usage:
    python tools/vbb-status-dashboard.py
    python tools/vbb-status-dashboard.py --json
    python tools/vbb-status-dashboard.py --full
    python tools/vbb-status-dashboard.py --repo <path>

Reads: docs/CONTEXT.md, docs/AUDIT_STATUS.md, docs/ACTIVITY_LOG.md,
       docs/runs/*, docs/audits/*, skills/*/CONTRACT.yaml, tests/*.

Displays: verdict, skills, contracts, tests, latest runs, open risks,
          next action.
"""

import sys
import json
import argparse
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).parent.parent.resolve()


def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def read_frontmatter(path: Path) -> Dict:
    """Read YAML frontmatter from a Markdown file."""
    content = read_file(path)
    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end == -1:
        return {}
    try:
        import yaml
        return yaml.safe_load(content[3:end].strip()) or {}
    except Exception:
        return {}


def count_skills(repo: Path) -> int:
    """Count skill directories that have at least SKILL.md."""
    skills_dir = repo / "skills"
    if not skills_dir.exists():
        return 0
    return sum(1 for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists())


def count_contracts(repo: Path) -> Tuple[int, int, int]:
    """Return (contracted, total, coverage%). Total = dirs with SKILL.md."""
    skills_dir = repo / "skills"
    if not skills_dir.exists():
        return 0, 0, 0
    total = 0
    contracted = 0
    for d in skills_dir.iterdir():
        if d.is_dir() and (d / "SKILL.md").exists():
            total += 1
            if (d / "CONTRACT.yaml").exists():
                contracted += 1
    coverage = round(contracted / total, 2) if total > 0 else 0
    return contracted, total, coverage


def count_indexed_contracts(repo: Path) -> int:
    """Count contract entries declared in skills/INDEX.yaml."""
    index_file = repo / "skills" / "INDEX.yaml"
    if not index_file.exists():
        return 0
    try:
        import yaml
        data = yaml.safe_load(index_file.read_text(encoding="utf-8")) or {}
    except Exception:
        return 0
    return len(data.get("skills", []))


def count_tests(repo: Path) -> int:
    """Count test*.py files in tests/."""
    tests_dir = repo / "tests"
    if not tests_dir.exists():
        return 0
    return sum(1 for f in tests_dir.iterdir() if f.is_file() and f.name.startswith("test_") and f.suffix == ".py")


def extract_verdict(repo: Path) -> str:
    """Extract global verdict from AUDIT_STATUS.md."""
    content = read_file(repo / "docs" / "AUDIT_STATUS.md")
    for line in content.split("\n"):
        if "Verdict global" in line or "verdict global" in line.lower():
            # Look for backtick content on next line or same line
            if "`" in line:
                return line.split("`")[1] if len(line.split("`")) > 1 else "UNKNOWN"
    # Fallback: look for PARTIAL/PASS/FAIL keywords near top
    for line in content.split("\n")[:30]:
        for keyword in ["PARTIAL", "PASS", "FAIL", "BLOCKED"]:
            if keyword in line.upper():
                return keyword
    return "UNKNOWN"


def extract_next_action(repo: Path) -> str:
    """Extract next action from CONTEXT.md."""
    content = read_file(repo / "docs" / "CONTEXT.md")
    for line in content.split("\n"):
        low = line.lower().strip()
        if (low.startswith("- **prochaine action**") or low.startswith("- prochaine action")
                or low.startswith("- **next action**") or low.startswith("- next action")):
            # Extract after colon or arrow
            parts = line.split(":", 1)
            if len(parts) > 1:
                return parts[1].strip().strip("*")
            parts = line.split("→", 1)
            if len(parts) > 1:
                return parts[1].strip().strip("*")
            return line.split("**")[-1].strip() if "**" in line else ""
    return ""


def _find_closeout(run_dir: Path) -> Optional[Path]:
    """Locate the closeout file inside a run directory.

    Accepts the canonical ``07_CLOSEOUT.md`` first, then falls back to any
    file matching ``*CLOSEOUT*.md`` (case-insensitive). Returns ``None`` if
    no closeout file is present.
    """
    canonical = run_dir / "07_CLOSEOUT.md"
    if canonical.is_file():
        return canonical
    matches = [p for p in run_dir.glob("*CLOSEOUT*.md") if p.is_file()]
    if not matches:
        return None
    # Prefer the most recently modified closeout candidate to defend against
    # stale duplicates from partial re-runs.
    return max(matches, key=lambda p: p.stat().st_mtime)


def get_latest_runs(repo: Path, limit: int = 5) -> List[Dict]:
    """Get N most recent run directories with their voie and status.

    Selection rules (RUN 3 stabilisation, 2026-06-03):
      * Only directories are considered (``README.md``, ``routing-fix-verification.md``
        and any other loose files in ``docs/runs/`` are excluded).
      * Sort key is the **directory mtime** (not the lexical name). mtime is robust
        to inconsistent naming (``20260602_0817_…`` vs ``2026-06-13_2200_…``) and
        to future-dated folder names that the lexical sort would mishandle.
      * Closeout detection accepts the canonical ``07_CLOSEOUT.md`` first, then
        falls back to any ``*CLOSEOUT*.md`` file (handles in-progress runs that
        write ``CLOSEOUT.md`` before the standard rename).
    """
    runs_dir = repo / "docs" / "runs"
    if not runs_dir.exists():
        return []
    # Filter: directories only. iterdir() yields loose files too; the
    # ``is_dir()`` check defensively drops ``README.md`` and any other
    # parasitic artefact that may land in ``docs/runs/``.
    run_dirs = [d for d in runs_dir.iterdir() if d.is_dir()]
    # Sort by mtime (newest first). mtime is the most reliable proxy for
    # "most recent" because it is independent of the folder name format.
    run_dirs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
    runs: List[Dict] = []
    for rd in run_dirs[: limit * 2]:  # extra buffer in case some lack closeout
        if len(runs) >= limit:
            break
        closeout = _find_closeout(rd)
        if closeout is None:
            continue
        fm = read_frontmatter(closeout)
        content = read_file(closeout)
        voie = str(fm.get("voie", "UNKNOWN")).strip() or "UNKNOWN"
        verdict = str(fm.get("status", "UNKNOWN")).strip() or "UNKNOWN"
        for line in content.split("\n")[:20]:
            low = line.lower()
            if voie == "UNKNOWN" and "voie" in low and ":" in line:
                voie = line.split(":")[-1].strip().strip("*")
            if verdict == "UNKNOWN" and "verdict" in low:
                for kw in ["COMPLETE", "READY", "PASS", "PARTIAL", "FAIL", "BLOCKED"]:
                    if kw in line.upper():
                        verdict = kw
                        break
        runs.append({"id": rd.name, "voie": voie, "verdict": verdict})
    return runs


def get_open_risks(repo: Path) -> List[Dict]:
    """Extract open risks from AUDIT_STATUS.md."""
    content = read_file(repo / "docs" / "AUDIT_STATUS.md")
    risks = []
    in_risk_section = False
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("## "):
            in_risk_section = stripped.lower().startswith("## risks identified")
            continue
        if not in_risk_section or "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 5 or parts[1] in ("ID", "---"):
            continue
        rid = parts[1].strip("`")
        severity = parts[2].strip("`")
        desc = parts[3].strip()
        status = parts[4].strip().strip("`")
        status_key = status.lower()
        if status_key.startswith("open") or status_key.startswith("mitigating"):
            risks.append({
                "id": rid,
                "severity": severity,
                "status": status,
                "description": desc[:80],
            })
    return risks


def index_present(repo: Path) -> bool:
    return (repo / ".vbb" / "index" / "manifest.json").exists()


def temporal_provenance_present(repo: Path) -> bool:
    return (repo / "docs" / "TEMPORAL_PROVENANCE.md").exists()


def get_temporal_notes(repo: Path) -> List[str]:
    """Report central artifacts dated after the local clock."""
    notes = []
    today = date.today().isoformat()
    acknowledged = temporal_provenance_present(repo)
    docs = [
        repo / "docs" / "CONTEXT.md",
        repo / "docs" / "AUDIT_STATUS.md",
        repo / "docs" / "ACTIVITY_LOG.md",
    ]
    for doc in docs:
        content = read_file(doc)
        for line in content.splitlines()[:20]:
            if "updated:" in line or "date:" in line:
                observed = line.split(":", 1)[1].strip().strip('"')
                if len(observed) >= 10 and observed[:10] > today:
                    notes.append(f"{doc.relative_to(repo)} dated {observed[:10]} after local date {today}")
                break

    runs_dir = repo / "docs" / "runs"
    if runs_dir.exists():
        future_runs = sorted(
            d.name for d in runs_dir.iterdir()
            if d.is_dir() and len(d.name) >= 10 and d.name[:10] > today
        )
        if future_runs:
            notes.append(f"{len(future_runs)} run directories are dated after local date {today}")
    if acknowledged and notes:
        return [
            f"local workspace date: {today}",
            "future-dated historical state acknowledged by docs/TEMPORAL_PROVENANCE.md",
        ] + notes
    return notes


def gather_status(repo: Path) -> Dict:
    """Gather full repo status."""
    contracted, total, coverage = count_contracts(repo)
    indexed_contracts = count_indexed_contracts(repo)
    verdict = extract_verdict(repo)
    next_action = extract_next_action(repo)
    latest_runs = get_latest_runs(repo)
    open_risks = get_open_risks(repo)
    test_count = count_tests(repo)

    return {
        "repo": str(repo),
        "local_date": date.today().isoformat(),
        "verdict": verdict,
        "skills": total,
        "contracts": contracted,
        "indexed_contracts": indexed_contracts,
        "contract_coverage": coverage,
        "runtime_contract_coverage": round(indexed_contracts / total, 2) if total > 0 else 0,
        "tests": test_count,
        "latest_runs": latest_runs,
        "risks": open_risks,
        "next_action": next_action,
        "index_present": index_present(repo),
        "temporal_provenance": temporal_provenance_present(repo),
        "temporal_notes": get_temporal_notes(repo),
    }


def format_terminal(status: Dict, full: bool = False) -> str:
    """Format status as terminal output."""
    def fit(value: object, width: int) -> str:
        text = str(value)
        return text[:width].ljust(width)

    pct = int(status["contract_coverage"] * 100)
    cov = fit(f"{status['contracts']}/{status['skills']} ({pct}%)", 29)
    idx = fit(f"{status['indexed_contracts']}/{status['skills']}", 29)
    lines = [
        f"╔══════════════════════════════════════════════════╗",
        f"║  VBB STATUS — {Path(status['repo']).name:<33}║",
        f"╠══════════════════════════════════════════════════╣",
        f"║  Verdict global : {status['verdict']:<29}║",
        f"║  Skills          : {status['skills']:<29}║",
        f"║  Contracts       : {cov}║",
        f"║  Indexed         : {idx}║",
        f"║  Test suites     : {status['tests']:<29}║",
    ]

    # Latest runs
    if status["latest_runs"]:
        lines.append(f"╠══════════════════════════════════════════════════╣")
        lines.append(f"║  Latest runs:                                    ║")
        for run in status["latest_runs"][:5]:
            rid = fit(run["id"], 29)
            v = fit(run.get("voie", "?").strip('"'), 7)
            vr = fit(run.get("verdict", "?"), 6)
            lines.append(f"║    {rid} {v} {vr} ║")

    # Open risks
    if status["risks"]:
        lines.append(f"╠══════════════════════════════════════════════════╣")
        lines.append(f"║  Open risks:                                     ║")
        for risk in status["risks"][:5]:
            rid = risk["id"]
            rs = risk["status"]
            desc = risk["description"][:28]
            lines.append(f"║    {fit(rid, 9)} {fit(rs, 11)} {fit(desc, 27)}║")

    if status["temporal_notes"]:
        lines.append(f"╠══════════════════════════════════════════════════╣")
        label = "Temporal provenance:" if status.get("temporal_provenance") else "Temporal warnings:"
        lines.append(f"║  {label:<47}║")
        for note in status["temporal_notes"][:3]:
            lines.append(f"║    {note[:43]:<43} ║")

    # Next action
    if status["next_action"]:
        na = fit(status["next_action"], 33)
        lines.append(f"╠══════════════════════════════════════════════════╣")
        lines.append(f"║  Next action: {na}║")

    lines.append(f"╚══════════════════════════════════════════════════╝")

    # Full mode: add extra details
    if full:
        lines.append("")
        # Activity log entries
        repo = Path(status["repo"])
        al = read_file(repo / "docs" / "ACTIVITY_LOG.md")
        if al:
            al_lines = [l for l in al.split("\n") if "|" in l and "Date" not in l and "---" not in l]
            if al_lines:
                lines.append("Activity log (recent):")
                for al_line in al_lines[-3:]:
                    lines.append(f"  {al_line.strip()}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="VBB Status Dashboard — read-only terminal view"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--full", action="store_true",
        help="Show extra details (activity log)"
    )
    parser.add_argument(
        "--repo", type=str, default=None,
        help="Path to repo root (default: auto-detect)"
    )

    args = parser.parse_args()

    repo = Path(args.repo) if args.repo else REPO_ROOT

    if not repo.exists():
        print(f"Error: repo not found: {repo}", file=sys.stderr)
        return 1

    status = gather_status(repo)

    if args.json:
        print(json.dumps(status, indent=2))
        return 0

    print(format_terminal(status, full=args.full))
    return 0


if __name__ == "__main__":
    sys.exit(main())
