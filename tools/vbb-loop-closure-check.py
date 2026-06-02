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

Exit codes (--strict mode, used by Cody as COMPLETE gate):
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

import sys
import os
import argparse
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).parent.parent.resolve()
RUNS_DIR = REPO_ROOT / "docs" / "runs"

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

def check_run(run_id: str, runs_dir: Optional[Path] = None) -> Tuple[bool, List[str]]:
    """Verify the closure invariant for the given run_id.

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
    args = parser.parse_args()

    run_id = args.run_id or args.run_id_flag or os.environ.get("VBB_RUN_ID")

    base = Path(args.runs_dir) if args.runs_dir else RUNS_DIR

    if not run_id:
        # Auto-detect most recent run
        if base.exists():
            candidates = sorted(
                [d for d in base.iterdir() if d.is_dir()],
                reverse=True,
            )
            if candidates:
                run_id = candidates[0].name
                if not args.strict:
                    print(
                        f"[info] No run_id given — using most recent: {run_id}",
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
        passed, report_lines = check_run(run_id, runs_dir=base)
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
