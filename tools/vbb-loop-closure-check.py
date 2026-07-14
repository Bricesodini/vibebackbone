#!/usr/bin/env python3
"""
VBB Loop Closure Check
Verifies that a run directory satisfies the closure invariant for its voie.

Usage:
    python3 tools/vbb-loop-closure-check.py <run_id>
    python3 tools/vbb-loop-closure-check.py --run-id <run_id>
    VBB_RUN_ID=<run_id> python3 tools/vbb-loop-closure-check.py
    python3 tools/vbb-loop-closure-check.py <run_id> --strict
    python3 tools/vbb-loop-closure-check.py <run_id> --json

Exit codes (default mode, --strict=False, retrocompatible):
    0  PASS  — all required artifacts present and valid
    1  FAIL  — one or more required artifacts missing or invalid
    2  GATE_BLOCKED — no run_id resolvable (usage error in default mode)

Exit codes (--strict mode, used by supported agents as the COMPLETE gate):
    0  PASS  — all required artifacts present and valid
    2  GATE_BLOCKED — loop-closure FAIL on the given run_id.
                     FINAL_STATUS=COMPLETE is FORBIDDEN in this state.
                     stderr carries the explicit blocking message.
    3  TOOL_BROKEN — internal error (unexpected exception).
                     The gate cannot decide; treat as FAIL.
    64 USAGE_ERROR — --strict was set without a --run_id (or equivalent
                     positional / VBB_RUN_ID env). The strict gate requires
                     an explicit run_id to evaluate.

--json output (when --json is passed) wraps the report with:
    {
      "exit_intent": "PASS" | "FAIL" | "GATE_BLOCKED",
      "run_id": "<resolved run_id or null>",
      "voie": "<resolved voie or null>",
      "errors": [<list of error strings>],
      "report": [<list of report lines, same as stdout text>]
    }

Invariant (from docs/runs/README.md):
    Voie RAPIDE-ZERO   → no docs/runs/ required (Activity Log only)
    Voie RAPIDE-MINIMAL → 05_PATCH_SUMMARY only (Activity Log required)
    Voie RAPIDE        → 01_INTAKE + 05_EXECUTION + 07_CLOSEOUT
    Voie STRUCTUREE    → 01_INTAKE + 04_PLAN + 05_EXECUTION + 07_CLOSEOUT
    Voie AUDIT         → 01_INTAKE + 02_AUDIT + 03_DECISION + 07_CLOSEOUT
    Voie CLOTURE       → 07_CLOSEOUT only (special case, no 01_INTAKE required)
"""

import re
import sys
import os
import argparse
import importlib.util as _importlib_util
import time
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).parent.parent.resolve()
RUNS_DIR = REPO_ROOT / "docs" / "runs"
AUDITS_DIR = REPO_ROOT / "docs" / "audits"

# Shared run resolution (ADR-0027): auto-detection uses the declared selector
# « dernier run existant » (newest by mtime, whole population) — the lexical
# sort mishandled mixed naming schemes (TD-101).

_RUN_RES_SPEC = _importlib_util.spec_from_file_location(
    "vbb_run_resolution", Path(__file__).parent / "vbb_run_resolution.py"
)
assert _RUN_RES_SPEC is not None and _RUN_RES_SPEC.loader is not None
_run_resolution = _importlib_util.module_from_spec(_RUN_RES_SPEC)
_RUN_RES_SPEC.loader.exec_module(_run_resolution)

# Route vocabulary aliases: the canonical route family names in AGENTS.md are
# English (FAST-*, STRUCTURED, CLOSEOUT) while run frontmatter historically
# uses the French voies. Both are accepted; the French form is canonical here.
VOIE_ALIASES: Dict[str, str] = {
    "STRUCTURED": "STRUCTUREE",
    "CLOSEOUT": "CLOTURE",
    "FAST": "RAPIDE",
    "FAST-STANDARD": "RAPIDE",
    "FAST-MINIMAL": "RAPIDE-MINIMAL",
    "FAST-ZERO": "RAPIDE-ZERO",
}

# Voie → required phase file stems (matches filenames in docs/runs/{slug}/)
VOIE_REQUIRED_PHASES: Dict[str, List[str]] = {
    "RAPIDE-ZERO":   [],                                    # Activity Log only
    "RAPIDE-MINIMAL": ["05_PATCH_SUMMARY"],                 # Activity Log + patch summary
    "RAPIDE":        ["01_INTAKE", "05_EXECUTION", "07_CLOSEOUT"],
    "STRUCTUREE":    ["01_INTAKE", "04_PLAN", "05_EXECUTION", "07_CLOSEOUT"],
    "AUDIT":         ["01_INTAKE", "02_AUDIT", "03_DECISION", "07_CLOSEOUT"],
    "CLOTURE":       ["07_CLOSEOUT"],
}

# Minimum frontmatter fields required in every phase artifact
FRONTMATTER_MIN = frozenset({
    "run_id", "phase", "voie", "status", "agent",
    "started_at", "ended_at", "artifacts_produced",
})

KNOWN_VOIES = frozenset(VOIE_REQUIRED_PHASES.keys())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_frontmatter(path: Path) -> Tuple[Optional[Dict], Optional[str]]:
    """Parse YAML frontmatter from a Markdown file.

    Returns (frontmatter_dict, error_string).
    On success, error_string is None.
    If no frontmatter block is found, returns ({}, None).
    """
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, str(exc)

    if not content.startswith("---"):
        return {}, None  # no frontmatter — not an error on its own

    end = content.find("\n---", 3)
    if end == -1:
        return None, "unclosed frontmatter block (missing closing ---)"

    fm_raw = content[3:end].strip()
    try:
        fm = yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError as exc:
        return None, f"YAML error in frontmatter: {exc}"

    return fm, None


# ---------------------------------------------------------------------------
# P0-1 — Claims evidence validation (extension, Phase 2 Run 1)
# ---------------------------------------------------------------------------
#
# Spec: docs/strategy/phase-1-contractualisation/phase-1-p0-1-evidence-claims.md
# Category: C (rule documented by VBB governance but not previously verified
# mécaniquement par le loop-closure).
#
# Comportement: pour chaque ligne qui matche un claim "fixed/passes/repaired/
# aligned/closed/merged" dans le 07_CLOSEOUT.md (sections "Résultat" et
# "Décisions prises" uniquement), vérifier qu'au moins une des 3 preuves est
# présente dans la même section (≤10 lignes):
#   1. Ligne "Evidence:" ou "Preuve:"
#   2. Bloc de code avec output cité (✓ / passed / 0 error)
#   3. Section "KNOWN LIMITATION:" ou "Volontairement non traité:"

CLAIM_VERB_RE = re.compile(
    r"^\s*-\s+(fixed|passes|repaired|aligned|closed|merged)\s*:",
    re.IGNORECASE,
)
# Evidence marker can appear anywhere in the window (start of line OR
# inline within a claim like "fixed: bar (Evidence: ...)").
EVIDENCE_MARKER_RE = re.compile(
    r"(?:^|\s)\b(?:Evidence|Preuve)\s*:",
    re.IGNORECASE,
)
# Output markers — accepted in any position within the window.
OUTPUT_MARKER_RE = re.compile(
    r"(?:[✓✗]|passed|0\s+errors?|0\s+erreurs?|exit\s+0|\bok\b|PASS|FAIL)",
    re.IGNORECASE,
)
KNOWN_LIMITATION_RE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:KNOWN\s+LIMITATION|Volontairement\s+non\s+traité)\s*:",
    re.IGNORECASE,
)
RESULT_SECTION_RE = re.compile(
    r"(?im)^#{1,6}\s*(?:R[ée]sultat|D[ée]cisions?\s+prises)\s*$"
)
END_SECTION_RE = re.compile(r"(?im)^#{1,6}\s+\S")
PLACEHOLDER_RE = re.compile(r"<\s*[A-Za-z][^>]*\s*>")


def _extract_scanned_sections(closeout_text: str) -> List[Tuple[str, str]]:
    """Yield (header, body) for sections 'Résultat' and 'Décisions prises'.

    Body is taken until the next markdown header of any depth, or end of
    document. The 'Décisions prises' header accepts singular/plural.
    """
    sections: List[Tuple[str, str]] = []
    lines = closeout_text.splitlines()
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        m = re.match(
            r"^#{1,6}\s*(R[ée]sultat|D[ée]cisions?\s+prises)\s*$",
            line,
            re.IGNORECASE,
        )
        if not m:
            i += 1
            continue
        header = m.group(1)
        body_lines: List[str] = []
        i += 1
        while i < n:
            nxt = lines[i]
            if re.match(r"^#{1,6}\s+\S", nxt):
                break
            body_lines.append(nxt)
            i += 1
        sections.append((header, "\n".join(body_lines)))
    return sections


def validate_claims_evidence(closeout_path: Path) -> List[str]:
    """Check that every claim in 07_CLOSEOUT.md has an Evidence line nearby.

    Scans only sections 'Résultat' and 'Décisions prises' to avoid false
    positives on artefacts list or handoff sections. Returns a list of error
    strings (empty = all claims are properly evidenced).
    """
    errors: List[str] = []
    if not closeout_path.exists():
        return errors  # existence check is the caller's responsibility
    try:
        text = closeout_path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"{closeout_path.name}: cannot read: {exc}"]

    scanned = _extract_scanned_sections(text)
    if not scanned:
        return errors  # no claims in 'Résultat' or 'Décisions prises' → PASS

    for header, body in scanned:
        # KNOWN LIMITATION at the section level exempts the whole section
        if KNOWN_LIMITATION_RE.search(body):
            continue
        lines = body.splitlines()
        for idx, ln in enumerate(lines):
            if not CLAIM_VERB_RE.match(ln):
                continue
            # Skip quoted lines (citations)
            if ln.lstrip().startswith(">"):
                continue
            # Look ahead up to 10 lines for evidence
            window = "\n".join(lines[idx: idx + 11])
            has_evidence = bool(EVIDENCE_MARKER_RE.search(window))
            has_output = bool(OUTPUT_MARKER_RE.search(window))
            has_known = bool(KNOWN_LIMITATION_RE.search(window))
            if not (has_evidence or has_output or has_known):
                errors.append(
                    f"{closeout_path.name}: section '{header}' has claim "
                    f"without evidence: {ln.strip()[:80]}"
                )
    return errors


# ---------------------------------------------------------------------------
# P0-2 — Plan sections validation (extension, Phase 2 Run 1)
# ---------------------------------------------------------------------------
#
# Spec: docs/strategy/phase-1-contractualisation/phase-1-p0-2-grill-plan.md
# Category: C (le template existe depuis longtemps mais le contenu n'est pas
# validé mécaniquement — un plan peut être vide ou contenir des <...>).
#
# Comportement: pour chaque section canonique du 04_PLAN.md, vérifier que
# (1) l'ancre existe (regex FR ou EN), (2) elle a ≥1 ligne de contenu non-
# whitespace, (3) aucun placeholder <...> ne reste.

PLAN_SECTION_ANCHORS: List[Tuple[str, Tuple[str, ...]]] = [
    ("Objectif",        (r"objectif", r"but", r"goal")),
    ("Pré-conditions",  (r"pr[ée]-conditions", r"pr[ée]requis", r"preconditions?", r"prerequisites?")),
    ("Étapes ordonnées",(r"[ée]tapes?\s+ordonn[ée]es?", r"steps?\s+ordonn[ée]es?",
                          r"ordered\s+steps?", r"steps?")),
    ("Critères d'acceptation", (
        r"crit[èe]res?\s+d'acceptation", r"crit[èe]res?\s+de\s+acceptation",
        r"definition\s+of\s+done", r"definition\s+of\s+done\s+\(dod\)",
        r"acceptance\s+criteria",
    )),
    ("Plan de rollback global", (
        r"plan\s+de\s+rollback\s+global", r"plan\s+de\s+rollback",
        r"rollback",
    )),
    ("Risques identifiés", (
        r"risques?\s+identifi[ée]s?", r"risques?",
    )),
]


def _find_section_header(body_lines: List[str], patterns: Tuple[str, ...]) -> Optional[int]:
    """Return the line index of the first matching header (case-insensitive)."""
    pat = re.compile(
        r"^#{1,6}\s*(?:" + "|".join(patterns) + r")\b",
        re.IGNORECASE,
    )
    for i, ln in enumerate(body_lines):
        if pat.match(ln.strip()):
            return i
    return None


def _section_body(body_lines: List[str], start: int) -> List[str]:
    """Return body lines from after `start` until next header or EOF."""
    out: List[str] = []
    for ln in body_lines[start + 1:]:
        if re.match(r"^#{1,6}\s+\S", ln):
            break
        out.append(ln)
    return out


def validate_plan_sections(plan_path: Path) -> List[str]:
    """Check that a 04_PLAN.md has the 6 canonical sections filled in.

    Returns list of error strings (empty = all sections present and non-empty).
    """
    errors: List[str] = []
    if not plan_path.exists():
        return [f"{plan_path.name}: missing"]
    try:
        text = plan_path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"{plan_path.name}: cannot read: {exc}"]

    # Strip frontmatter
    body = text
    if body.startswith("---"):
        end = body.find("\n---", 3)
        if end != -1:
            body = body[end + 4:]

    body_lines = body.splitlines()
    for canonical_name, patterns in PLAN_SECTION_ANCHORS:
        idx = _find_section_header(body_lines, patterns)
        if idx is None:
            errors.append(
                f"{plan_path.name}: MISSING_SECTION: {canonical_name}"
            )
            continue
        section_body = _section_body(body_lines, idx)
        # Require at least 1 non-whitespace line of content
        non_empty = [ln for ln in section_body if ln.strip()]
        if not non_empty:
            errors.append(
                f"{plan_path.name}: EMPTY_SECTION: {canonical_name}"
            )
            continue
        # Reject remaining placeholders
        joined = "\n".join(non_empty)
        m = PLACEHOLDER_RE.search(joined)
        if m:
            errors.append(
                f"{plan_path.name}: PLACEHOLDER_IN_SECTION: "
                f"{canonical_name}: {m.group(0)}"
            )
    return errors


# ---------------------------------------------------------------------------
# P0-3 — Test audit check (extension, Phase 2 Run 1)
# ---------------------------------------------------------------------------
#
# Spec: docs/strategy/phase-1-contractualisation/phase-1-p0-3-test-coverage.md
# Category: A (3 skills/outils EXISTENT — on n'invente rien, on contractualise
# leur invocation). Le check vérifie qu'au moins un rapport d'audit test a
# été produit dans la fenêtre de fraîcheur (par défaut 7 jours).
#
# Voies concernées: STRUCTUREE, AUDIT, CLOSEOUT. Si `05_EXECUTION.md` contient
# la phrase "no test surface" (case-insensitive), le check passe (tolérance).

TEST_AUDIT_GLOBS = ("test-coverage-*.md", "test-mirage-*.md")
TEST_AUDIT_FRESHNESS_DAYS = 7
NO_TEST_SURFACE_MARKER = "no test surface"


def _find_recent_test_audit(
    audits_dir: Path,
    max_age_seconds: int,
    now: Optional[float] = None,
) -> List[Path]:
    """Return a list of test-audit reports newer than max_age_seconds."""
    if not audits_dir.is_dir():
        return []
    if now is None:
        now = time.time()
    cutoff = now - max_age_seconds
    found: List[Path] = []
    for glob in TEST_AUDIT_GLOBS:
        for p in audits_dir.glob(glob):
            try:
                mtime = p.stat().st_mtime
            except OSError:
                continue
            if mtime >= cutoff:
                found.append(p)
    return found


def validate_test_audit(
    run_dir: Path,
    audits_dir: Optional[Path] = None,
    max_age_days: int = TEST_AUDIT_FRESHNESS_DAYS,
    now: Optional[float] = None,
) -> Tuple[List[str], List[str]]:
    """Check that a STRUCTUREE/AUDIT/CLOSEOUT run has a fresh test audit.

    Returns (errors, info_lines). info_lines is non-empty on PASS, describing
    which report satisfied the check.
    """
    errors: List[str] = []
    info: List[str] = []

    audits = audits_dir if audits_dir is not None else AUDITS_DIR
    if not audits.is_dir():
        return (
            [f"test-audit: SKIP (audits dir not found: {audits})"],
            info,
        )

    # Tolerance 1: explicit "no test surface" in 05_EXECUTION.md
    execution_path = run_dir / "05_EXECUTION.md"
    if execution_path.exists():
        try:
            exec_text = execution_path.read_text(encoding="utf-8")
        except OSError:
            exec_text = ""
        if NO_TEST_SURFACE_MARKER.lower() in exec_text.lower():
            info.append(
                "test-audit: PASS (explicit 'no test surface' in 05_EXECUTION.md)"
            )
            return errors, info

    reports = _find_recent_test_audit(
        audits,
        max_age_seconds=max_age_days * 86400,
        now=now,
    )
    if reports:
        info.append(
            "test-audit: PASS ("
            + ", ".join(p.name for p in sorted(reports))
            + f", < {max_age_days} days)"
        )
        return errors, info

    errors.append(
        f"test-audit: FAIL — no test audit report in {audits} "
        f"(looked for: {', '.join(TEST_AUDIT_GLOBS)}, "
        f"freshness ≤ {max_age_days} days). "
        f"Run t-vbb-test-coverage-mapper or 1-vbb-test-mirage-detector, "
        f"or add 'no test surface' to 05_EXECUTION.md."
    )
    return errors, info


def validate_artifact(path: Path) -> List[str]:
    """Check that a phase artifact file has valid frontmatter.

    Returns list of error strings (empty = valid).
    """
    errors: List[str] = []

    fm, parse_error = read_frontmatter(path)
    if parse_error:
        errors.append(f"{path.name}: {parse_error}")
        return errors

    if not fm:
        errors.append(
            f"{path.name}: no frontmatter found "
            "(expected YAML block between --- markers)"
        )
        return errors

    # Required fields
    for field in sorted(FRONTMATTER_MIN):
        if field not in fm:
            errors.append(
                f"{path.name}: frontmatter missing required field '{field}'"
            )

    # Placeholder detection — any <value> still means an unfilled template
    for key, val in fm.items():
        if isinstance(val, str) and val.startswith("<") and val.endswith(">"):
            errors.append(
                f"{path.name}: frontmatter field '{key}' "
                f"still has placeholder value '{val}'"
            )

    return errors


# ---------------------------------------------------------------------------
# Core check
# ---------------------------------------------------------------------------

def check_run(
    run_id: str,
    runs_dir: Optional[Path] = None,
    *,
    validate_claims: bool = False,
    validate_plan: bool = False,
    validate_test_audit_for_voies: Optional[Tuple[str, ...]] = (
        "STRUCTUREE", "AUDIT", "CLOSEOUT",
    ),
    audits_dir: Optional[Path] = None,
) -> Tuple[bool, List[str]]:
    """Verify the closure invariant for the given run_id.

    Optional extensions (all OFF by default, retrocompatible):
      - validate_claims: also call validate_claims_evidence on 07_CLOSEOUT
        (P0-1, spec: phase-1-p0-1-evidence-claims.md).
      - validate_plan: also call validate_plan_sections on 04_PLAN
        (P0-2, spec: phase-1-p0-2-grill-plan.md).
      - validate_test_audit_for_voies: if voie ∈ this tuple, also call
        validate_test_audit (P0-3, spec: phase-1-p0-3-test-coverage.md).
        Pass an empty tuple to disable the test-audit check.

    Returns (passed: bool, report_lines: List[str]).
    """
    base = runs_dir if runs_dir is not None else RUNS_DIR
    run_dir = base / run_id
    report: List[str] = []
    errors: List[str] = []

    report.append(f"VBB Loop Closure Check — {run_id}")
    report.append("=" * 60)

    # Step 1 — run directory must exist
    if not run_dir.exists():
        errors.append(f"run directory not found: {run_dir}")
        report.append("")
        report.append("Errors:")
        report.append(f"  ✗ {errors[0]}")
        report.append("")
        report.append(f"RESULT: FAIL — run directory '{run_id}' does not exist")
        return False, report

    # Step 2 — determine voie
    intake_path = run_dir / "01_INTAKE.md"
    closeout_path = run_dir / "07_CLOSEOUT.md"
    patch_path = run_dir / "05_PATCH_SUMMARY.md"
    voie: Optional[str] = None

    if intake_path.exists():
        fm, parse_error = read_frontmatter(intake_path)
        if parse_error:
            errors.append(f"01_INTAKE.md: {parse_error}")
        elif not fm:
            errors.append("01_INTAKE.md: no frontmatter found")
        else:
            raw = fm.get("voie", "")
            candidate = str(raw).strip().upper() if raw else ""
            candidate = VOIE_ALIASES.get(candidate, candidate)
            if not candidate:
                errors.append(
                    "01_INTAKE.md: frontmatter field 'voie' is missing or empty"
                )
            elif candidate not in KNOWN_VOIES:
                errors.append(
                    f"01_INTAKE.md: unknown voie '{candidate}' "
                    f"(expected one of {sorted(KNOWN_VOIES)})"
                )
            else:
                voie = candidate
    else:
        # No 01_INTAKE — try to infer voie from other artifacts.
        # Priority: closeout → patch summary → default error
        if closeout_path.exists():
            fm, _ = read_frontmatter(closeout_path)
            if fm:
                inferred = str(fm.get("voie", "")).strip().upper()
                inferred = VOIE_ALIASES.get(inferred, inferred)
                if inferred in ("CLOTURE", "RAPIDE-ZERO", "RAPIDE-MINIMAL"):
                    voie = inferred
        if voie is None and patch_path.exists():
            fm, _ = read_frontmatter(patch_path)
            if fm:
                inferred = str(fm.get("voie", "")).strip().upper()
                if inferred == "RAPIDE-MINIMAL":
                    voie = "RAPIDE-MINIMAL"
        if voie is None:
            # No intake and no inferable closeout/patch summary voie. Fail
            # explicitly rather than silently treating an ad-hoc run as valid.
            if closeout_path.exists():
                errors.append(
                    "01_INTAKE.md: not found and 07_CLOSEOUT.md does not "
                    "declare an inferable voie (CLOTURE, RAPIDE-ZERO, "
                    "or RAPIDE-MINIMAL)"
                )
            else:
                errors.append(
                    "01_INTAKE.md: not found and 07_CLOSEOUT.md: not found "
                    "(cannot infer voie for closure invariant)"
                )
            # Fall back to closeout-only requirement so the report still runs
            required_phases = ["07_CLOSEOUT"]

    # Step 3 — required phases
    if voie and voie in VOIE_REQUIRED_PHASES:
        required_phases = VOIE_REQUIRED_PHASES[voie]
    else:
        # Unknown voie — fall back to universal minimum
        required_phases = ["07_CLOSEOUT"]

    report.append(f"  Run     : {run_id}")
    report.append(f"  Voie    : {voie or 'UNKNOWN'}")
    report.append(f"  Required: {', '.join(required_phases)}")
    report.append("")

    # Step 4 — check each required artifact
    for phase_stem in required_phases:
        artifact_path = run_dir / f"{phase_stem}.md"
        if not artifact_path.exists():
            errors.append(
                f"{phase_stem}.md: missing "
                f"(required for voie {voie or 'UNKNOWN'})"
            )
        else:
            fm_errors = validate_artifact(artifact_path)
            if fm_errors:
                errors.extend(fm_errors)
            else:
                report.append(f"  ✓ {phase_stem}.md")

    # Step 4bis — optional extensions (P0-1, P0-2, P0-3)
    # P0-1 — claims evidence on 07_CLOSEOUT
    if validate_claims and (run_dir / "07_CLOSEOUT.md").exists():
        claim_errors = validate_claims_evidence(run_dir / "07_CLOSEOUT.md")
        if claim_errors:
            errors.extend(claim_errors)
        else:
            report.append("  ✓ claims evidence (07_CLOSEOUT.md)")

    # P0-2 — plan sections on 04_PLAN
    if validate_plan:
        plan_path = run_dir / "04_PLAN.md"
        if plan_path.exists():
            plan_errors = validate_plan_sections(plan_path)
            if plan_errors:
                errors.extend(plan_errors)
            else:
                report.append("  ✓ plan sections (04_PLAN.md)")
        else:
            # Only relevant if the voie requires 04_PLAN
            if voie and "04_PLAN" in VOIE_REQUIRED_PHASES.get(voie, []):
                errors.append(
                    "04_PLAN.md: missing "
                    f"(required for voie {voie}, --validate-plan)"
                )

    # P0-3 — test audit on STRUCTUREE/AUDIT/CLOSEOUT
    if (
        validate_test_audit_for_voies
        and voie in validate_test_audit_for_voies
    ):
        ta_errors, ta_info = validate_test_audit(
            run_dir, audits_dir=audits_dir
        )
        for line in ta_info:
            report.append(f"  {line}")
        errors.extend(ta_errors)

    # Step 5 — final verdict
    report.append("")
    if errors:
        report.append("Errors:")
        for e in errors:
            report.append(f"  ✗ {e}")
        report.append("")
        report.append(
            f"RESULT: FAIL — {len(errors)} issue(s) found"
        )
        return False, report
    else:
        report.append(
            f"RESULT: PASS — closure invariant satisfied "
            f"({voie}, {len(required_phases)} phases verified)"
        )
        return True, report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify VBB run closure invariant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "run_id",
        nargs="?",
        help=(
            "Run ID, e.g. 2026-05-23_1700_contracts-artifact-schema-lot-b-d. "
            "Omit to use VBB_RUN_ID env var or most-recent run."
        ),
    )
    parser.add_argument(
        "--run-id",
        dest="run_id_flag",
        metavar="RUN_ID",
        help="Run ID (flag form, equivalent to positional argument)",
    )
    parser.add_argument(
        "--runs-dir",
        metavar="DIR",
        help="Override docs/runs/ directory (used in tests)",
    )
    parser.add_argument(
        "--strict",
        dest="strict",
        action="store_true",
        default=False,
        help=(
            "Enable COMPLETE-gate semantics: FAIL on the resolved run_id "
            "returns exit 2 (GATE_BLOCKED), missing --run_id returns exit 64 "
            "(USAGE_ERROR), internal errors return exit 3 (TOOL_BROKEN). "
            "FINAL_STATUS=COMPLETE is FORBIDDEN when this gate exits non-zero. "
            "Default: False (retrocompatible with the original PASS=0/FAIL=1 contract)."
        ),
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        default=False,
        help=(
            "Emit a JSON wrapper with exit_intent, run_id, voie, errors, "
            "and the textual report. Exit codes are unchanged."
        ),
    )
    parser.add_argument(
        "--validate-claims",
        dest="validate_claims",
        action="store_true",
        default=False,
        help=(
            "P0-1: also validate that every claim in 07_CLOSEOUT.md "
            "(sections 'Résultat' and 'Décisions prises') is followed by an "
            "Evidence/Preuve line, an output marker, or a KNOWN LIMITATION."
        ),
    )
    parser.add_argument(
        "--validate-plan",
        dest="validate_plan",
        action="store_true",
        default=False,
        help=(
            "P0-2: also validate that 04_PLAN.md has the 6 canonical sections "
            "present, non-empty, and free of <...> placeholders."
        ),
    )
    parser.add_argument(
        "--validate-test-audit",
        dest="validate_test_audit",
        action="store_true",
        default=False,
        help=(
            "P0-3: for STRUCTUREE/AUDIT/CLOSEOUT runs, require a recent "
            "test-coverage-*.md or test-mirage-*.md report in docs/audits/ "
            "(< 7 days) or an explicit 'no test surface' in 05_EXECUTION.md."
        ),
    )
    parser.add_argument(
        "--audits-dir",
        metavar="DIR",
        help=(
            "Override docs/audits/ directory (used in tests). "
            "Only relevant with --validate-test-audit."
        ),
    )
    args = parser.parse_args()

    run_id = args.run_id or args.run_id_flag or os.environ.get("VBB_RUN_ID")

    base = Path(args.runs_dir) if args.runs_dir else RUNS_DIR

    if not run_id:
        # Auto-detect: selector « dernier run existant » (shared mtime
        # resolution, ADR-0027) — newest run dir by mtime, closed or not.
        latest = _run_resolution.latest_existing_run(base)
        if latest is not None:
            run_id = latest.name
            if not args.strict:
                print(
                    "[info] No run_id given — using latest existing run "
                    f"(mtime): {run_id}",
                    file=sys.stderr,
                )

    # ---- --strict mode: explicit run_id is required ----
    if args.strict and not run_id:
        msg = (
            "GATE FAILED: --run_id required in --strict mode. "
            "Provide the run_id via positional arg, --run-id, or VBB_RUN_ID env. "
            "The strict gate cannot evaluate a closure without a target run_id."
        )
        if args.json_output:
            import json as _json
            print(_json.dumps({
                "exit_intent": "GATE_BLOCKED",
                "run_id": None,
                "voie": None,
                "errors": [msg],
                "report": [],
            }, indent=2))
        else:
            print(msg, file=sys.stderr)
        return 64

    if not run_id:
        msg = (
            "Error: run_id is required.\n"
            "Usage: vbb-loop-closure-check.py <run_id>"
        )
        if args.json_output:
            import json as _json
            print(_json.dumps({
                "exit_intent": "GATE_BLOCKED",
                "run_id": None,
                "voie": None,
                "errors": [msg],
                "report": [],
            }, indent=2))
        else:
            print(msg, file=sys.stderr)
        return 1  # retrocompatible exit for "no run_id" in default mode

    # ---- Core check ----
    try:
        passed, report_lines = check_run(
            run_id,
            runs_dir=base,
            validate_claims=args.validate_claims,
            validate_plan=args.validate_plan,
            validate_test_audit_for_voies=(
                ("STRUCTUREE", "AUDIT", "CLOSEOUT")
                if args.validate_test_audit
                else ()
            ),
            audits_dir=(
                Path(args.audits_dir) if args.audits_dir else None
            ),
        )
    except Exception as exc:  # noqa: BLE001 — we want to surface ANY error as TOOL_BROKEN
        msg = (
            f"GATE FAILED: vbb-loop-closure-check internal error on "
            f"run_id={run_id}: {type(exc).__name__}: {exc}"
        )
        if args.json_output:
            import json as _json
            print(_json.dumps({
                "exit_intent": "GATE_BLOCKED",
                "run_id": run_id,
                "voie": None,
                "errors": [msg],
                "report": [],
            }, indent=2))
        else:
            print(msg, file=sys.stderr)
        return 3  # TOOL_BROKEN — same in both modes (an internal error is an
                  # internal error).

    if args.json_output:
        import json as _json
        # Build errors list from report (lines starting with "  ✗ ")
        errors = [ln.lstrip().lstrip("✗").strip() for ln in report_lines
                  if ln.strip().startswith("✗")]
        # Extract resolved voie from report
        voie = None
        for ln in report_lines:
            if ln.strip().startswith("Voie"):
                voie = ln.split(":", 1)[1].strip() if ":" in ln else None
                break
        exit_intent = "PASS" if passed else "GATE_BLOCKED"
        print(_json.dumps({
            "exit_intent": exit_intent,
            "run_id": run_id,
            "voie": voie,
            "errors": errors,
            "report": report_lines,
        }, indent=2))
    else:
        for line in report_lines:
            print(line)

    if passed:
        return 0

    # FAIL — branch on strict mode
    if args.strict:
        msg = (
            f"GATE FAILED: loop-closure FAIL on run_id={run_id}. "
            f"FINAL_STATUS=COMPLETE is not allowed. Fix closure before retrying."
        )
        print(msg, file=sys.stderr)
        return 2  # GATE_BLOCKED

    return 1  # retrocompatible FAIL


if __name__ == "__main__":
    sys.exit(main())
