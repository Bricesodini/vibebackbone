#!/usr/bin/env python3
"""
vbb-review-threshold-poc — POC for review-tier classification (T1-T8).

Classifies a list of changed files into a single review tier (T1-T8) and
explains why. Dry-run only. No gate, no enforcement, no side effects.

Tier model (P0-4 calibration, 2026-06-13):
  T1 — documentation simple
  T2 — tests / fixtures / examples
  T3 — tooling local non critique
  T4 — templates / prompts / skills
  T5 — gouvernance Core (AGENTS / CONVENTIONS / DISTRIBUTIONS)
  T6 — architecture / migrations / hooks / CI
  T7 — sécurité / credentials / auth / données sensibles
  T8 — production / destruction / secrets / accès externe réel

Resolution rule: MAX(tiers_matched). T8 > T7 > T6 > T5 > T4 > T3 > T2 > T1.

Usage:
  python tools/vbb-review-threshold-poc.py <path> [<path> ...]
  python tools/vbb-review-threshold-poc.py --json <path> [...]
  git diff --name-only main..HEAD | xargs python tools/vbb-review-threshold-poc.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# --- Tier definitions ------------------------------------------------------

# Each tier is a (rank, label, [path_regex], [reason_hint]).
# rank 1 = lowest, 8 = highest. Max wins.
TIERS: List[Tuple[int, str, List[str], str]] = [
    (
        1,
        "T1 — documentation simple",
        [
            r"^README\.md$",
            r"^docs/[A-Z][A-Z_]+\.md$",  # e.g. docs/CONTEXT.md, docs/PILOTAGE.md
            r"^docs/runs/[^/]+/0[1-7]_[A-Z_]+\.md$",  # run artifacts (intake..closeout)
            r"^docs/audits/.*\.md$",
            r"\.md$",  # catch-all for any markdown OUTSIDE the rule above
        ],
        "doc-only change",
    ),
    (
        2,
        "T2 — tests / fixtures / exemples",
        [
            r"^tests/.*\.py$",
            r"^tests/.*\.sh$",
            r"^tests/.*\.md$",
            r".*[/_\-]test[s]?\.py$",  # e.g. distributions/*/tests/*.py
            r".*\.test\.[jt]sx?$",
            r".*\.spec\.[jt]sx?$",
            r"^tests/fixtures/.*$",
            r"^tests/.*/fixtures/.*$",
        ],
        "test/fixture change",
    ),
    (
        3,
        "T3 — tooling local non critique",
        [
            r"^tools/vbb-architecture\.py$",
            r"^tools/vbb-contract-lint\.py$",
            r"^tools/vbb-llm-healthcheck\.py$",
            r"^tools/vbb-loop-closure-check\.py$",  # loop-closure (read-only validator)
        ],
        "tooling local (non-gate)",
    ),
    (
        4,
        "T4 — templates / prompts / skills / READMEs distrib",
        [
            r"^docs/templates/.*$",
            r"^prompts/.*$",
            r"^skills/.*$",
            r"^core\.README\.md$",
            r"^distributions/[^/]+/README\.md$",
            r"^distributions/[^/]+/[^/]+/README\.md$",  # nested distribution README
        ],
        "template/prompt/skill/distrib-README change",
    ),
    (
        5,
        "T5 — gouvernance Core",
        [
            r"^AGENTS\.md$",
            r"^CONVENTIONS\.md$",
            r"^GUIDE\.md$",
            r"^docs/CONTEXT\.md$",
            r"^docs/PILOTAGE\.md$",
            r"^docs/DISTRIBUTIONS\.md$",
            r"^docs/RUNBOOK\.md$",
            r"^docs/DEPLOYMENT\.md$",
            r"^docs/adr/.*\.md$",
        ],
        "Core governance doc",
    ),
    (
        6,
        "T6 — architecture / migrations / hooks / CI",
        [
            r"^tools/vbb-gate-check\.py$",  # gate-check (gate logic)
            r"^tools/vbb-status-dashboard\.py$",  # status dashboard (writes docs/AUDIT_STATUS.md)
            r"^tools/vbb-context-compactor\.py$",  # context compactor (affects token budget)
            r"^tools/vbb-review-threshold-.*$",  # this very tool
            r"^scripts/hooks/.*$",  # git hooks
            r"^scripts/install-.*\.sh$",
            r"^\.github/workflows/.*\.ya?ml$",
            r"^setup\.sh$",
            r"^install\.sh$",
        ],
        "architecture/hook/CI change",
    ),
    (
        7,
        "T7 — sécurité / credentials / auth / données sensibles",
        [
            r"^distributions/[^/]+/proxy/(config|runtime|secret_store|hmac|crypto|client|actions|audit)\.py$",
            r"^distributions/[^/]+/proxy/(config|runtime)\.example\.yaml$",
            r"^distributions/[^/]+/bypass-lint/.*\.py$",  # bypass-lint core (secrets detection)
            r".*[/_\-]secrets?[/_\-].*\.(yaml|yml|json|env)$",
            r".*credentials.*\.(yaml|yml|json|env)$",
            r".*[_-]api[_-]?key.*\.(yaml|yml|json|env)$",
        ],
        "credential/auth surface",
    ),
    (
        8,
        "T8 — production / destruction / secrets / accès externe réel",
        [
            r"^distributions/[^/]+/proxy/actions\.py$",  # action whitelist (write surface)
            r"^distributions/[^/]+/proxy/audit\.py$",  # audit writer
        ],
        "production-grade write surface",
    ),
]

# --- Core logic ------------------------------------------------------------


def _compile_tiers() -> List[Tuple[int, str, List[re.Pattern], str]]:
    out = []
    for rank, label, patterns, reason in TIERS:
        compiled = [re.compile(p) for p in patterns]
        out.append((rank, label, compiled, reason))
    return out


COMPILED = _compile_tiers()


def classify_path(path: str) -> List[Tuple[int, str, str]]:
    """Return all tiers matching this path (may be many). Empty if no match."""
    hits = []
    for rank, label, patterns, reason in COMPILED:
        for pat in patterns:
            if pat.search(path):
                hits.append((rank, label, reason))
                break
    return hits


def review_tier(paths: List[str]) -> Dict:
    """Classify a list of paths. Returns a dict with tier, reasons, per-file."""
    per_file: List[Dict] = []
    seen: Dict[int, Tuple[str, str]] = {}  # rank -> (label, reason)
    for p in paths:
        hits = classify_path(p)
        per_file.append(
            {
                "path": p,
                "tiers": [
                    {"rank": rank, "label": label, "reason": reason}
                    for rank, label, reason in hits
                ],
            }
        )
        for rank, label, reason in hits:
            seen[rank] = (label, reason)
    if not seen:
        return {
            "tier": None,
            "tier_label": "UNMAPPED",
            "tier_rank": 0,
            "reasons": [],
            "per_file": per_file,
            "warning": "no tier matched — file outside known VBB surface",
        }
    # MAX wins
    max_rank = max(seen.keys())
    return {
        "tier": f"T{max_rank}",
        "tier_label": seen[max_rank][0],
        "tier_rank": max_rank,
        "reasons": [seen[r][1] for r in sorted(seen.keys(), reverse=True)],
        "matched_tiers": [seen[r][0] for r in sorted(seen.keys(), reverse=True)],
        "per_file": per_file,
    }


def render_text(result: Dict) -> str:
    lines: List[str] = []
    lines.append("VBB Review-Tier POC (T1-T8)")
    lines.append("=" * 50)
    tier = result["tier"] or "UNMAPPED"
    lines.append(f"  Tier proposé : {tier} — {result['tier_label']}")
    if result.get("matched_tiers"):
        lines.append(f"  Tous tiers touchés : {' > '.join(result['matched_tiers'])}")
    if result.get("reasons"):
        lines.append("  Raisons :")
        for r in result["reasons"]:
            lines.append(f"    - {r}")
    if result.get("warning"):
        lines.append(f"  WARNING: {result['warning']}")
    lines.append("")
    lines.append("  Détail par fichier :")
    for entry in result["per_file"]:
        path = entry["path"]
        if entry["tiers"]:
            labels = ", ".join(t["label"].split(" — ")[0] for t in entry["tiers"])
            lines.append(f"    {path}  →  {labels}")
        else:
            lines.append(f"    {path}  →  (no match)")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="POC review-tier classifier (T1-T8). Dry-run only."
    )
    parser.add_argument("paths", nargs="+", help="files to classify")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()
    paths = [str(Path(p)) for p in args.paths]
    result = review_tier(paths)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_text(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
