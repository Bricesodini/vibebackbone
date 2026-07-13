#!/usr/bin/env python3
"""
VBB Gate Check — ADR + POC + Integration Gate.

For a given run directory, decides whether coding can start based on:
  1. ADR_REQUIRED?  — extracted from 01_INTAKE.md keywords
  2. POC_REQUIRED?  — extracted from 01_INTAKE.md keywords
  3. CAN_CODE_START — composite boolean

Usage:
    python tools/vbb-gate-check.py <run_dir>
    python tools/vbb-gate-check.py <run_dir> --json
    python tools/vbb-gate-check.py --help

Exit codes:
    0  PASS  — can_code_start = true
    1  FAIL  — can_code_start = false (blockers present)
    2  USAGE — usage error (run_dir missing, etc.)
    3  TOOL_BROKEN — internal error

Stdlib only. No LLM. No framework. ≤ 200 LOC.

Detection rules (synchronized with docs/GUIDE.md §ADR+POC+Integration-Gate):

  ADR_REQUIRED triggers (any match, case-insensitive, word boundary):
    - security / secret / auth / authentication / authorization
    - deploy / deployment
    - storage / persistence / database
    - stack / framework / language / runtime
    - protocol / api / interface / contract

  POC_REQUIRED triggers (any match):
    - ssh / nas / cloud / s3 / gcs
    - api (external)
    - github / actions / ci
    - mcp / telegram / discord / slack
    - docker / kubernetes / k8s / helm
    - llm / model / ollama / vllm / mlx
    - secret store / vault / keychain
    - orchestration / multi-agent

  ADR validation: file exists at docs/adr/{nnnn}-{slug}.md AND
                  contains '**Status**: ACCEPTED' (or 'SUPERSEDED').

  POC validation: file at docs/runs/{run_id}/POC.md exists AND
                  contains 'Décision: GO' (or 'Verdict: GO').

  Linkage: 01_INTAKE.md or 04_PLAN.md may reference an ADR (path or NNNN) and/or
           a POC (path). If neither is referenced but the run requires the
           gate, blockers include a "MISSING_LINK" message.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).parent.parent.resolve()
ADR_DIR = REPO_ROOT / "docs" / "adr"

# Rule 1: ADR obligatoire — sécurité, secret, auth, deploy, storage, stack, protocol
ADR_KEYWORDS = (
    r"\b(security|secret|auth|authentication|authorization|deploy|deployment"
    r"|storage|persistence|database|stack|framework|runtime|protocol"
    r"|interface|contract|governance|policy|convention)\b"
)

# Rule 3: POC obligatoire — hypothèse technique non validée
POC_KEYWORDS = (
    r"\b(ssh|nas|cloud|s3|gcs|external\s*api|github|actions|ci|cd"
    r"|mcp|telegram|discord|slack|docker|kubernetes|k8s|helm"
    r"|llm|model|ollama|vllm|mlx|keychain|vault|orchestration|multi-?agent)\b"
)

# Rule 4 (Phase 2 Run 1, P0-5-A §4.6): mode-transition recommendation
# If the intake mentions "deploy", "production", "prod", "migration",
# the t-vbb-mode-transition-gate skill is RECOMMENDED (warning, not
# blocker). The skill already exists; this check just makes the
# recommendation visible. Skip if docs/PROJECT_MODE.md is absent
# (micro-project without notion of mode).
MODE_TRANSITION_KEYWORDS = (
    r"\b(deploy|deployment|production|prod|migration|release|rollout)\b"
)

# Status accepted for an ADR
ADR_ACCEPTED_RE = re.compile(r"\*\*Status\*\*\s*:\s*(ACCEPTED|SUPERSEDED)", re.IGNORECASE)
_POC_VERDICT_LABEL = r"(?:\*\*)?(?:Décision|Verdict|decision)(?:\*\*)?"
POC_GO_RE = re.compile(
    rf"{_POC_VERDICT_LABEL}\s*:\s*GO\b", re.IGNORECASE
)
POC_NOGO_RE = re.compile(
    rf"{_POC_VERDICT_LABEL}\s*:\s*NO[\s\-]?GO\b", re.IGNORECASE
)
POC_PIVOT_RE = re.compile(
    rf"{_POC_VERDICT_LABEL}\s*:\s*PIVOT\b", re.IGNORECASE
)

# Patterns to extract ADR reference from 01_INTAKE or 04_PLAN
ADR_REF_RE = re.compile(
    r"docs/adr/(\d{4})-([a-z0-9\-]+)\.md|adr/(\d{4})-([a-z0-9\-]+)", re.IGNORECASE
)
POC_REF_RE = re.compile(
    r"docs/runs/[^\s)]*POC\.md|/\*POC\*\.md|run_id.*?POC", re.IGNORECASE
)


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        return ""


# Negation patterns: lines and clauses that negate the keyword context.
# Two strategies combined:
#  1. Per-line negation cues ("pas de", "aucun", "sans", "hors périmètre: X", ...)
#     — these strip the NEGATED CLAUSE only, not the whole line.
#     E.g. "Sans changer l'API, migrer le storage" → "migrer le storage"
#  2. Whole sections (### Hors périmètre / ### Out of scope) — everything below
#     the header up to the next ### or end of file is stripped.
#
# A negation clause is bounded by a cue word + (comma | "et" | "ou" | end of
# negated verb phrase). When the cue is at line start, the clause runs from the
# cue to the first comma/conjunction; the rest of the line is preserved.

# Cue words that introduce a negated clause. The clause runs from the cue to
# the first comma or coordinating conjunction AFTER the cue.
_NEGATION_CUE_RE = re.compile(
    r"(?ix)"
    r"\b(?:"
    r"  pas\s+de(?:s)?|"
    r"  aucun|aucune|"
    r"  sans(?:\s+(?:changer|rompre|casser|modifier|toucher|impact))?|"
    r"  hors\s+p[ée]rim[èe]tre\s*:|"
    r"  no\s+change|"
    r"  ne\s+\w+\s+pas|"
    r"  n'?applique(?:nt|rait)?|"
    r"  not\s+applicable|"
    r"  n/a"
    r")"
)

# End-of-clause marker after a negation cue.
_NEGATION_CLAUSE_END_RE = re.compile(
    r"(?ix)"
    r"\s*(?:,\s*|\s+et\s+|\s+ou\s+|\s+ni\s+|\.\s*$)"
)


def _strip_clause(line: str) -> str:
    """If a line starts with a negation cue, strip the negated clause only.

    Examples:
      "Sans changer l'API publique, migrer le storage"
        → "migrer le storage"
      "- pas de changement d'API"  (no comma after cue)
        → ""  (whole line is the negation)
      "- pas de changement d'API, garder le reste"
        → "- garder le reste"
      "remplacer le storage sans casser l'API"
        → "remplacer le storage"  (cue in the middle: strip from cue to clause end)
    """
    m = _NEGATION_CUE_RE.search(line)
    if not m:
        return line
    cue_start = m.start()
    # Find clause end AFTER the cue match
    rest = line[m.end():]
    end_m = _NEGATION_CLAUSE_END_RE.search(rest)
    if end_m:
        clause_end = m.end() + end_m.end()
        # Keep text before cue + text after clause (preserving leading "- " if any)
        return line[:cue_start] + line[clause_end:].lstrip()
    # No end marker found: the whole remainder is the negated clause
    # → drop it. But preserve leading list-bullet prefix.
    prefix_match = re.match(r"^(\s*-\s*)", line[:cue_start])
    if prefix_match:
        return prefix_match.group(1).rstrip() + "\n"
    return ""


_NEGATION_LINE_RE = re.compile(
    r"(?im)^(?P<line>[^\n]*)$"
)


def _strip_line_negations(text: str) -> str:
    """Apply per-line clause stripping. Preserves non-negated text on each line."""
    out_lines = []
    for line in text.split("\n"):
        out_lines.append(_strip_clause(line))
    return "\n".join(out_lines)


# Section headers that signal "this whole block is out of scope".
# Match the header line and everything up to the next "##" or "###" header.
_NEGATION_SECTION_RE = re.compile(
    r"(?im)"                                   # case-insensitive, multi-line
    r"^\s*#{2,4}\s*(?:Hors\s+p[ée]rim[èe]tre|Out\s+of\s+scope|"
    r"               Exclusions?|N/?A\s+scope)\s*$"
    r"[^\n]*(?:\n(?!#{1,4}\s)[^\n]*)*"         # body lines until next # header
)


def _strip_negations(text: str) -> str:
    """Remove lines, clauses, and sections that negate the keyword context.

    Stripped:
      - Per-line negation clauses: "Sans ...", "pas de ...", "aucun ...",
        "hors périmètre: X", etc. Only the NEGATED PORTION is removed;
        the rest of the line is preserved.
      - Whole sections: `### Hors périmètre` / `### Out of scope` /
        `### Exclusions` / `### N/A scope` (and all body lines up to next header)
    """
    text = _NEGATION_SECTION_RE.sub("", text)
    text = _strip_line_negations(text)
    return text


def detect_required(text: str) -> Tuple[bool, bool]:
    """Return (adr_required, poc_required) from intake text.

    Negation-aware: clauses like "hors périmètre", "pas de", "sans" are stripped
    before keyword matching to avoid false positives on exclusions.
    """
    cleaned = _strip_negations(text)
    adr_required = bool(re.search(ADR_KEYWORDS, cleaned, re.IGNORECASE))
    poc_required = bool(re.search(POC_KEYWORDS, cleaned, re.IGNORECASE))
    return adr_required, poc_required


def find_adr_ref(text: str) -> Optional[Tuple[str, str]]:
    """Return (nnnn, slug) if an ADR reference is found."""
    m = ADR_REF_RE.search(text)
    if not m:
        return None
    nnnn = m.group(1) or m.group(3)
    slug = m.group(2) or m.group(4)
    if nnnn and slug:
        return nnnn, slug.lower()
    return None


# ADR-0027 decision 3 — strict linkage. A run may cite several ADRs (consumed
# artifacts, historical context); only a LINKAGE-LABELED reference designates
# "the run's ADR". Labels: "Liée à ADR", "adr_link:", or a "- ADR :" bullet.
ADR_LINK_LABEL_RE = re.compile(
    r"(?im)^.*(?:li[ée]e?\s+à\s+ADR|adr_link|^\s*[-*]\s*ADR)\s*[:*]*\s*(?P<rest>.*)$"
)


def find_linked_adr_ref(text: str) -> Optional[Tuple[str, str]]:
    """Return (nnnn, slug) from a linkage-labeled line, if any.

    Takes precedence over any other ADR mention in the text: an explicitly
    linked ADR is always the one the gate must verify.
    """
    for m in ADR_LINK_LABEL_RE.finditer(text):
        ref = find_adr_ref(m.group(0))
        if ref:
            return ref
    return None


def find_adr_globally(text: str) -> Optional[Path]:
    """Search for the latest ACCEPTED ADR whose slug contains a relevant keyword.

    The fallback match requires that at least one ADR_KEYWORD (security, auth,
    storage, database, stack, protocol, etc.) appears in the slug. Random
    substring matches on common tokens (like "contract" matching anywhere) are
    rejected — only keywords that triggered `adr_required=True` in the first
    place may unlock a fallback match.
    """
    if not ADR_DIR.is_dir():
        return None
    # Extract the keywords actually present in the text (the ones that flipped
    # adr_required=True). We restrict fallback matching to those.
    relevant = [k.lower() for k in re.findall(ADR_KEYWORDS, text, re.IGNORECASE)]
    if not relevant:
        return None
    candidates: List[Tuple[int, Path]] = []
    for adr in sorted(ADR_DIR.glob("*.md")):
        if not ADR_ACCEPTED_RE.search(_read(adr)):
            continue
        slug = adr.stem.split("-", 1)[-1] if "-" in adr.stem else adr.stem
        slug_lower = slug.lower()
        for kw in relevant:
            if kw in slug_lower:
                candidates.append((len(slug), adr))
                break
    if not candidates:
        return None
    candidates.sort(key=lambda x: -x[0])  # longest slug first = more specific
    return candidates[0][1]


def check_adr(run_dir: Path) -> Tuple[bool, Optional[Path], str]:
    """Check ADR presence+ACCEPTED for the run.

    ADR-0027 decision 3 — strict linkage: when an ADR is explicitly
    referenced, the gate verifies THAT one and never falls back to some
    other globally accepted ADR (observed false PASS, 2026-07-13).
    Resolution order:
      1. linkage-labeled reference (« Liée à ADR », adr_link, "- ADR :")
      2. first explicit reference in intake/plan
      3. keyword fallback — ONLY when no explicit reference exists at all
    """
    intake_text = _read(run_dir / "01_INTAKE.md")
    plan_text = _read(run_dir / "04_PLAN.md") if (run_dir / "04_PLAN.md").exists() else ""
    combined = intake_text + "\n" + plan_text

    ref = find_linked_adr_ref(combined) or find_adr_ref(combined)
    if ref:
        nnnn, slug = ref
        candidate = ADR_DIR / f"{nnnn}-{slug}.md"
        if not candidate.exists():
            return False, None, "ADR_REF_NOT_FOUND"
        if ADR_ACCEPTED_RE.search(_read(candidate)):
            return True, candidate, ""
        return False, candidate, "ADR_NOT_ACCEPTED"

    # Keyword fallback — reachable only when the run references no ADR at all.
    matched = find_adr_globally(combined)
    if matched:
        return True, matched, ""

    return False, None, "MISSING_ADR"


def check_poc(run_dir: Path) -> Tuple[bool, Optional[Path], str]:
    """Check POC presence and require an explicit GO verdict for the run."""
    poc = run_dir / "POC.md"
    if not poc.exists():
        return False, None, "MISSING_POC"
    text = _read(poc)
    if POC_NOGO_RE.search(text):
        return False, poc, "POC_VERDICT_NO_GO"
    if POC_PIVOT_RE.search(text):
        return False, poc, "POC_VERDICT_PIVOT"
    if POC_GO_RE.search(text):
        return True, poc, ""
    return False, poc, "POC_VERDICT_ABSENT"


def check_mode_transition(run_dir: Path) -> Dict:
    """Phase 2 Run 1, P0-5-A §4.6.

    Returns a small dict:
        {
            "recommended": bool,
            "reason": "...",
            "skill": "t-vbb-mode-transition-gate" or None,
            "status": "RECOMMENDED" | "SKIPPED_NO_PROJECT_MODE" | "NOT_NEEDED",
        }
    """
    intake_text = _read(run_dir / "01_INTAKE.md")
    if not intake_text:
        return {
            "recommended": False,
            "reason": "no intake",
            "skill": None,
            "status": "NOT_NEEDED",
        }
    # Strip negations to avoid false positives (e.g. "pas de deploy en prod")
    cleaned = _strip_negations(intake_text)
    if not re.search(MODE_TRANSITION_KEYWORDS, cleaned, re.IGNORECASE):
        return {
            "recommended": False,
            "reason": "no mode-transition keyword in intake",
            "skill": None,
            "status": "NOT_NEEDED",
        }
    # Keyword matched. Is there a PROJECT_MODE.md?
    project_mode = REPO_ROOT / "docs" / "PROJECT_MODE.md"
    if not project_mode.exists():
        return {
            "recommended": False,
            "reason": "docs/PROJECT_MODE.md absent (micro-project without notion of mode)",
            "skill": None,
            "status": "SKIPPED_NO_PROJECT_MODE",
        }
    return {
        "recommended": True,
        "reason": "mode-transition keyword detected in intake",
        "skill": "t-vbb-mode-transition-gate",
        "status": "RECOMMENDED",
    }


def evaluate(run_dir: Path) -> Dict:
    """Main gate evaluation. Returns dict suitable for JSON output."""
    blockers: List[str] = []
    run_dir = run_dir.resolve()

    intake_path = run_dir / "01_INTAKE.md"
    if not intake_path.exists():
        return {
            "run_dir": str(run_dir),
            "intake_present": False,
            "adr_required": False,
            "adr_present_and_accepted": False,
            "poc_required": False,
            "poc_present_and_go": False,
            "can_code_start": False,
            "blockers": ["INTAKE_MISSING"],
            "exit_intent": "FAIL",
        }

    intake_text = _read(intake_path)
    adr_required, poc_required = detect_required(intake_text)

    adr_ok, adr_path, adr_blocker = check_adr(run_dir)
    poc_ok, poc_path, poc_blocker = check_poc(run_dir)
    mode_transition = check_mode_transition(run_dir)

    if adr_required and not adr_ok:
        blockers.append(adr_blocker or "ADR_NOT_ACCEPTED")
    if poc_required and not poc_ok:
        blockers.append(poc_blocker or "POC_NOT_GO")

    can_start = (not adr_required or adr_ok) and (not poc_required or poc_ok)

    return {
        "run_dir": str(run_dir),
        "intake_present": True,
        "adr_required": adr_required,
        "adr_present_and_accepted": adr_ok,
        "adr_path": str(adr_path) if adr_path else None,
        "poc_required": poc_required,
        "poc_present_and_go": poc_ok,
        "poc_path": str(poc_path) if poc_path else None,
        "can_code_start": can_start,
        "blockers": blockers,
        "mode_transition": mode_transition,
        "exit_intent": "PASS" if can_start else "FAIL",
    }


def render_text(report: Dict) -> str:
    lines = []
    lines.append(f"Run: {report['run_dir']}")
    lines.append(f"ADR_REQUIRED: {report['adr_required']} | "
                 f"ADR_ACCEPTED: {report['adr_present_and_accepted']}"
                 + (f" ({report['adr_path']})" if report.get('adr_path') else ""))
    lines.append(f"POC_REQUIRED: {report['poc_required']} | "
                 f"POC_GO: {report['poc_present_and_go']}"
                 + (f" ({report['poc_path']})" if report.get('poc_path') else ""))
    lines.append(f"CAN_CODE_START: {report['can_code_start']}")
    if report["blockers"]:
        lines.append("Blockers:")
        for b in report["blockers"]:
            lines.append(f"  - {b}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="vbb-gate-check",
        description="ADR + POC + Integration Gate check (stdlib only).",
    )
    parser.add_argument("run_dir", help="Path to run directory (containing 01_INTAKE.md)")
    parser.add_argument("--json", action="store_true", help="Emit JSON only")
    args = parser.parse_args(argv)

    run_dir = Path(args.run_dir)
    if not run_dir.exists() or not run_dir.is_dir():
        sys.stderr.write(f"ERROR: run_dir not found: {run_dir}\n")
        return 2

    try:
        report = evaluate(run_dir)
    except Exception as e:  # pragma: no cover - defensive
        sys.stderr.write(f"TOOL_BROKEN: {e}\n")
        return 3

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render_text(report))

    return 0 if report["can_code_start"] else 1


if __name__ == "__main__":
    sys.exit(main())
