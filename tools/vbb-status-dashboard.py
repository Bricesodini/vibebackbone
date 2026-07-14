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
import importlib.util
import re
import subprocess
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).parent.parent.resolve()

# --- Shared run resolution (ADR-0027) ---------------------------------------
# Single source of truth for "latest run" selection, shared with
# vbb-loop-closure-check.py. Loaded via importlib for robustness when this
# script itself is loaded by path (tests) rather than executed from tools/.
_RUN_RES_SPEC = importlib.util.spec_from_file_location(
    "vbb_run_resolution", Path(__file__).parent / "vbb_run_resolution.py"
)
assert _RUN_RES_SPEC is not None and _RUN_RES_SPEC.loader is not None
_run_resolution = importlib.util.module_from_spec(_RUN_RES_SPEC)
_RUN_RES_SPEC.loader.exec_module(_run_resolution)

# --- P0-4 review-tier integration (opt-in, advisory only) ------------------
# Imported lazily via importlib because the module filename has hyphens.
_POC_TOOL_PATH = Path(__file__).parent / "vbb-review-threshold-poc.py"


def _load_review_tier_poc():
    """Lazy-load tools/vbb-review-threshold-poc.py. Returns the module or None."""
    if not _POC_TOOL_PATH.exists():
        return None
    spec = importlib.util.spec_from_file_location(
        "vbb_review_threshold_poc", _POC_TOOL_PATH,
    )
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
    except Exception:
        return None
    return mod


def _git_changed_paths(repo: Path, staged: bool = False) -> List[str]:
    """Return changed file paths. staged=True → staged only, else working tree."""
    cmd = ["git", "-C", str(repo), "diff", "--name-only"]
    if staged:
        cmd = ["git", "-C", str(repo), "diff", "--cached", "--name-only"]
    try:
        out = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10,
            check=False,
        )
    except (subprocess.TimeoutExpired, OSError):
        return []
    return [ln.strip() for ln in out.stdout.splitlines() if ln.strip()]


# Per-tier suggested actions (advisory, never enforced).
_TIER_SUGGESTED_ACTIONS: Dict[str, List[str]] = {
    "T1": ["quick read", "no review required"],
    "T2": ["run pytest locally", "verify no flaky test introduced"],
    "T3": ["run architecture lint + contract lint", "sanity-check side effects"],
    "T4": ["verify skill/template still loads", "re-read example in doc"],
    "T5": ["re-read CONVENTIONS.md and P.R1-P.R8",
           "notify Brice if changing Pillar 1-5"],
    "T6": ["run full P.R2 suite (arch+contract+loop-closure+pytest+ci-local)",
           "request Brice review before push"],
    "T7": ["audit credential surface", "run vbb-bypass-lint --strict",
           "request Brice explicit review"],
    "T8": ["audit action whitelist", "verify audit log wiring",
           "request Brice explicit review + dry-run prod mirror"],
}


def compute_review_tier(repo: Path, paths: Optional[List[str]] = None) -> Dict:
    """Compute advisory review-tier info. Returns a dict ready for JSON."""
    poc = _load_review_tier_poc()
    if poc is None:
        return {
            "review_tier": None,
            "label": "POC module unavailable",
            "reasons": [f"vbb-review-threshold-poc.py not found at {_POC_TOOL_PATH}"],
            "suggested_actions": ["re-run calibration POC or fix import path"],
            "blocking": False,
            "confidence": "low",
            "mode": "advisory",
            "files_analyzed": 0,
        }
    if paths is None:
        # Default: working-tree changes (unstaged + untracked not in diff)
        paths = _git_changed_paths(repo, staged=False)
    result = poc.review_tier(paths)
    tier = result.get("tier")
    label = result.get("tier_label", "UNMAPPED")
    # The POC label embeds the rank (e.g. "T6 — architecture / ...")
    # The dashboard label is the human summary (e.g. "Core tooling / governance").
    short_label = label.split(" — ", 1)[1] if " — " in label else label
    if tier is None:
        return {
            "review_tier": None,
            "label": "UNMAPPED",
            "reasons": result.get("reasons", []),
            "suggested_actions": ["verify file paths — none matched VBB tier patterns"],
            "blocking": False,
            "confidence": "low",
            "mode": "advisory",
            "files_analyzed": len(paths),
            "warning": result.get("warning"),
        }
    rank = result["tier_rank"]
    # Confidence heuristic: if multiple tiers matched AND MAX dominates by
    # margin > 1, confidence is high. If single tier matched, high. Otherwise medium.
    matched = result.get("matched_tiers", [])
    confidence = "high" if rank >= 7 or len(matched) <= 1 else "medium"
    return {
        "review_tier": tier,
        "label": short_label,
        "reasons": result.get("reasons", []),
        "suggested_actions": _TIER_SUGGESTED_ACTIONS.get(tier, []),
        "blocking": False,
        "confidence": confidence,
        "mode": "advisory",
        "files_analyzed": len(paths),
    }


def format_review_tier_text(info: Dict, paths: List[str]) -> str:
    """Human-readable rendering of the review-tier advisory."""
    lines: List[str] = []
    lines.append("VBB Review-Tier Advisory (P0-4 opt-in, advisory only)")
    lines.append("=" * 60)
    tier = info.get("review_tier")
    if tier is None:
        lines.append("  Tier : UNMAPPED")
        if info.get("warning"):
            lines.append(f"  Note : {info['warning']}")
    else:
        lines.append(f"  Tier : {tier} — {info.get('label', '?')}")
        lines.append(f"  Mode : {info.get('mode', 'advisory')} (blocking={info.get('blocking', False)})")
        lines.append(f"  Confidence : {info.get('confidence', '?')}")
        if info.get("reasons"):
            lines.append("  Reasons :")
            for r in info["reasons"]:
                lines.append(f"    - {r}")
        if info.get("suggested_actions"):
            lines.append("  Suggested actions (advisory) :")
            for a in info["suggested_actions"]:
                lines.append(f"    - {a}")
    lines.append(f"  Files analyzed : {info.get('files_analyzed', 0)}")
    if paths:
        lines.append("  Changed files :")
        for p in paths[:20]:  # cap display
            lines.append(f"    - {p}")
        if len(paths) > 20:
            lines.append(f"    ... ({len(paths) - 20} more)")
    lines.append("")
    lines.append("  NOTE: this is ADVISORY only. It does not gate, block, or")
    lines.append("  enforce anything. Use it to decide who should review.")
    return "\n".join(lines)


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
    return _run_resolution.find_closeout(run_dir)


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
    # Selector « dernier run clôturé » (ADR-0027): the dashboard's population
    # is runs WITH a closeout; ordering comes from the shared mtime resolution.
    run_dirs = _run_resolution.list_runs_by_mtime(runs_dir)
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
    """Extract open risks from recognized tables, ordered by severity."""
    content = read_file(repo / "docs" / "AUDIT_STATUS.md")
    risks: List[Dict] = []
    columns: Optional[Dict[str, int]] = None

    def clean(cell: str) -> str:
        return re.sub(r"(?<!\w)[*_`]+|[*_`]+(?!\w)", "", cell).strip()

    for line in content.split("\n"):
        stripped = line.strip()
        if not stripped.startswith("|"):
            columns = None
            continue

        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        headers = [clean(cell).lower() for cell in cells]
        aliases = {
            "id": {"id"},
            "severity": {"severity", "sévérité"},
            "status": {"status", "statut"},
            "description": {"description", "constat"},
        }
        detected = {
            name: next((i for i, header in enumerate(headers) if header in names), -1)
            for name, names in aliases.items()
        }
        if all(index >= 0 for index in detected.values()):
            columns = detected
            continue

        if columns is None or all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        if max(columns.values()) >= len(cells):
            continue

        rid = clean(cells[columns["id"]])
        severity = clean(cells[columns["severity"]])
        status = clean(cells[columns["status"]])
        desc = clean(cells[columns["description"]])
        status_key = status.lower()
        if status_key.startswith("open") or status_key.startswith("mitigating"):
            risks.append({
                "id": rid,
                "severity": severity,
                "status": status,
                "description": desc[:80],
            })

    def severity_rank(risk: Dict) -> int:
        severity = risk["severity"].upper()
        match = re.search(r"\bP([0-3])\b", severity)
        if match:
            return int(match.group(1))
        return {"BLOCKER": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}.get(severity, 99)

    unique: List[Dict] = []
    seen = set()
    for risk in sorted(risks, key=severity_rank):
        if risk["id"] not in seen:
            seen.add(risk["id"])
            unique.append(risk)
    return unique


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
    parser.add_argument(
        "--review-tier", action="store_true",
        help="Compute and display the P0-4 review-tier advisory (opt-in, non-blocking)"
    )
    parser.add_argument(
        "--tier", action="store_true",
        help="Alias for --review-tier"
    )

    args = parser.parse_args()

    repo = Path(args.repo) if args.repo else REPO_ROOT

    if not repo.exists():
        print(f"Error: repo not found: {repo}", file=sys.stderr)
        return 1

    # P0-4 review-tier advisory (opt-in branch)
    if args.review_tier or args.tier:
        paths = _git_changed_paths(repo, staged=False)
        info = compute_review_tier(repo, paths=paths)
        if args.json:
            print(json.dumps(info, indent=2))
        else:
            print(format_review_tier_text(info, paths))
        return 0

    status = gather_status(repo)

    if args.json:
        print(json.dumps(status, indent=2))
        return 0

    print(format_terminal(status, full=args.full))
    return 0


if __name__ == "__main__":
    sys.exit(main())
