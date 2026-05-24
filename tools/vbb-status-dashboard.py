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
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).parent.parent.resolve()


def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


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


def get_latest_runs(repo: Path, limit: int = 5) -> List[Dict]:
    """Get N most recent run directories with their voie and status."""
    runs_dir = repo / "docs" / "runs"
    if not runs_dir.exists():
        return []
    run_dirs = sorted(
        [d for d in runs_dir.iterdir() if d.is_dir()],
        key=lambda d: d.name,
        reverse=True
    )
    runs = []
    for rd in run_dirs[:limit * 2]:  # extra buffer in case some lack closeout
        if len(runs) >= limit:
            break
        closeout = rd / "07_CLOSEOUT.md"
        if not closeout.exists():
            continue
        content = read_file(closeout)
        voie = "UNKNOWN"
        verdict = "UNKNOWN"
        for line in content.split("\n")[:20]:
            low = line.lower()
            if "voie" in low and ":" in line:
                voie = line.split(":")[-1].strip().strip("*")
            if "verdict" in low and ("pass" in low or "partial" in low or "fail" in low or "blocked" in low):
                for kw in ["PASS", "PARTIAL", "FAIL", "BLOCKED"]:
                    if kw in line.upper():
                        verdict = kw
                        break
        runs.append({"id": rd.name, "voie": voie, "verdict": verdict})
    return runs


def get_open_risks(repo: Path) -> List[Dict]:
    """Extract open risks from AUDIT_STATUS.md."""
    content = read_file(repo / "docs" / "AUDIT_STATUS.md")
    risks = []
    in_table = False
    for line in content.split("\n"):
        if "|" in line and "R-" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                rid = parts[1].strip() if len(parts) > 1 else ""
                if rid.startswith("R-"):
                    status = parts[3].strip() if len(parts) > 3 else ""
                    # Only include OPEN or MITIGATING
                    if status in ("OPEN", "MITIGATING", "`OPEN`", "`MITIGATING`"):
                        desc = parts[2].strip() if len(parts) > 2 else ""
                        risks.append({"id": rid, "status": status.strip("`"), "description": desc[:80]})
    return risks


def gather_status(repo: Path) -> Dict:
    """Gather full repo status."""
    contracted, total, coverage = count_contracts(repo)
    verdict = extract_verdict(repo)
    next_action = extract_next_action(repo)
    latest_runs = get_latest_runs(repo)
    open_risks = get_open_risks(repo)
    test_count = count_tests(repo)

    return {
        "repo": str(repo),
        "verdict": verdict,
        "skills": total,
        "contracts": contracted,
        "contract_coverage": coverage,
        "tests": test_count,
        "latest_runs": latest_runs,
        "risks": open_risks,
        "next_action": next_action,
    }


def format_terminal(status: Dict, full: bool = False) -> str:
    """Format status as terminal output."""
    pct = int(status["contract_coverage"] * 100)
    lines = [
        f"╔══════════════════════════════════════════════════╗",
        f"║  VBB STATUS — {Path(status['repo']).name:<33}║",
        f"╠══════════════════════════════════════════════════╣",
        f"║  Verdict global : {status['verdict']:<29}║",
        f"║  Skills          : {status['skills']:<29}║",
        f"║  Contracts       : {status['contracts']}/{status['skills']} ({pct}%){' ' * (23 - len(str(pct)))}║",
        f"║  Test suites     : {status['tests']:<29}║",
    ]

    # Latest runs
    if status["latest_runs"]:
        lines.append(f"╠══════════════════════════════════════════════════╣")
        lines.append(f"║  Latest runs:                                    ║")
        for run in status["latest_runs"][:5]:
            rid = run["id"][:32]
            v = run.get("voie", "?")[:8]
            vr = run.get("verdict", "?")[:6]
            lines.append(f"║    {rid:<32} {v:<8} {vr:<6} ║")

    # Open risks
    if status["risks"]:
        lines.append(f"╠══════════════════════════════════════════════════╣")
        lines.append(f"║  Open risks:                                     ║")
        for risk in status["risks"][:5]:
            rid = risk["id"]
            rs = risk["status"]
            desc = risk["description"][:28]
            lines.append(f"║    {rid:<8} {rs:<12} {desc:<28}║")

    # Next action
    if status["next_action"]:
        na = status["next_action"][:42]
        lines.append(f"╠══════════════════════════════════════════════════╣")
        lines.append(f"║  Next action: {na:<33}║")

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