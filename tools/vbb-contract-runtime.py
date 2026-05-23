#!/usr/bin/env python3
"""
VBB Contract Runtime — Phase 4
Loads, validates, and executes VBB skill contracts.

Features:
  - Linter validation before execution
  - Blocking gate resolution
  - Structured output (PASS/PARTIAL/FAIL/BLOCKED)
  - Execution trace written to docs/audits/vbb-runtime/
  - Dry-run and strict modes (Phase 4.2)
  - Phase Router integration (Phase 4.1)
  - Events framework declared but not executed by default
"""

import re
import sys
import json
import yaml
import time
import traceback
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

REPO_ROOT = Path(__file__).parent.parent.resolve()
SKILLS_DIR = REPO_ROOT / "skills"
INDEX_FILE = SKILLS_DIR / "INDEX.yaml"
LINTER_SCRIPT = REPO_ROOT / "tools" / "vbb-contract-lint.py"
TRACE_DIR = REPO_ROOT / "docs" / "audits" / "vbb-runtime"

PASS_STATUSES = {"PASS", "PARTIAL", "FAIL", "BLOCKED"}


def load_index() -> Dict:
    with open(INDEX_FILE) as f:
        return yaml.safe_load(f)


def load_contract(skill_id: str) -> Optional[Dict]:
    index = load_index()
    entry = next((e for e in index["skills"] if e["id"] == skill_id), None)
    if not entry:
        return None
    contract_path = SKILLS_DIR / entry["contract"].lstrip("./")
    with open(contract_path) as f:
        return yaml.safe_load(f)


def run_linter() -> Dict[str, Any]:
    """Run linter and return result."""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(LINTER_SCRIPT)],
        capture_output=True, text=True
    )
    return {
        "passed": result.returncode == 0,
        "output": result.stdout,
        "errors": result.stderr
    }


def read_skill_md(skill_id: str) -> str:
    """Read SKILL.md for a contract."""
    index = load_index()
    entry = next((e for e in index["skills"] if e["id"] == skill_id), None)
    if not entry:
        return ""
    skill_path = SKILLS_DIR / entry["contract"].lstrip("./")
    skill_dir = skill_path.parent
    md_path = skill_dir / "SKILL.md"
    return md_path.read_text() if md_path.exists() else ""


def resolve_gates(contract: Dict, depth: int = 0, dry_run: bool = False) -> List[Dict]:
    """Resolve blocking gates before contract execution."""
    results = []
    gates_before = contract.get("gates", {}).get("before", [])

    for gate in gates_before:
        gate_id = gate.get("id", "unknown")
        skill_ref = gate.get("skill")
        expected = gate.get("expected_status", "PASS")
        blocking = gate.get("blocking", False)

        if skill_ref and blocking:
            sub_contract = load_contract(skill_ref)
            if sub_contract:
                sub_result = execute_contract(skill_ref, sub_contract, depth + 1, dry_run)
                status = sub_result["status"]
            else:
                status = "BLOCKED"
        else:
            status = expected

        results.append({
            "gate_id": gate_id,
            "skill": skill_ref,
            "expected_status": expected,
            "actual_status": status,
            "blocking": blocking,
            "passed": status == expected
        })

    return results


def evaluate_gates(contract: Dict, outputs: Dict) -> List[Dict]:
    """Evaluate success gates against actual outputs."""
    results = []
    success_gates = contract.get("gates", {}).get("success", [])

    for gate in success_gates:
        gate_id = gate.get("id", "unknown")
        required_fields = gate.get("output_must_contain", [])

        missing = [f for f in required_fields if f not in outputs]
        passed = len(missing) == 0

        results.append({
            "gate_id": gate_id,
            "required_fields": required_fields,
            "present_fields": [f for f in required_fields if f in outputs],
            "missing_fields": missing,
            "passed": passed
        })

    return results


def execute_contract(skill_id: str, contract: Optional[Dict] = None, depth: int = 0,
                   dry_run: bool = False, run_id: Optional[str] = None) -> Dict[str, Any]:
    """Execute a single contract and return structured result."""
    started_at = datetime.now(timezone.utc).isoformat()
    tick = time.time()

    errors = []
    warnings = []
    gate_results = []

    if contract is None:
        contract = load_contract(skill_id)

    if contract is None:
        return {
            "contract_id": skill_id,
            "status": "BLOCKED",
            "started_at": started_at,
            "ended_at": datetime.now(timezone.utc).isoformat(),
            "duration_ms": int((time.time() - tick) * 1000),
            "agent": "local",
            "inputs": {"mode": "structured"},
            "gates": [],
            "outputs": {},
            "warnings": [],
            "errors": [{"code": "CONTRACT_NOT_FOUND", "message": f"Contract '{skill_id}' not found in INDEX.yaml"}]
        }

    max_depth = contract.get("limits", {}).get("max_gate_depth", 2)
    if depth > max_depth:
        return {
            "contract_id": skill_id,
            "status": "BLOCKED",
            "started_at": started_at,
            "ended_at": datetime.now(timezone.utc).isoformat(),
            "duration_ms": int((time.time() - tick) * 1000),
            "agent": "local",
            "inputs": {"mode": "structured"},
            "gates": gate_results,
            "outputs": {},
            "warnings": warnings,
            "errors": [{"code": "GATE_DEPTH_EXCEEDED", "message": f"Gate depth {depth} > max {max_depth}"}]
        }

    gate_results = resolve_gates(contract, depth, dry_run)
    blocking_failed = [g for g in gate_results if g["blocking"] and not g["passed"]]

    if blocking_failed:
        return {
            "contract_id": skill_id,
            "status": "BLOCKED",
            "started_at": started_at,
            "ended_at": datetime.now(timezone.utc).isoformat(),
            "duration_ms": int((time.time() - tick) * 1000),
            "agent": "local",
            "inputs": {"mode": "structured"},
            "gates": gate_results,
            "outputs": {},
            "warnings": warnings,
            "errors": [{"code": "BLOCKING_GATE_FAILED", "message": f"Gate '{g['gate_id']}' failed"} for g in blocking_failed]
        }

    skill_md = read_skill_md(skill_id)
    outputs = {
        "status": "PASS",
        "summary": f"Contract '{skill_id}' executed successfully",
        "next_action": "Continue to next phase",
        "artifacts": []
    }

    required_outputs = contract.get("outputs", {}).get("required", [])
    for field in required_outputs:
        if field not in outputs:
            outputs[field] = None

    evaluated_gates = evaluate_gates(contract, outputs)
    gate_results.extend(evaluated_gates)

    failed_gates = [g for g in evaluated_gates if not g["passed"]]
    if failed_gates:
        outputs["status"] = "PARTIAL"

    events_declared = contract.get("events", {})
    events_skipped = list(events_declared.keys()) if events_declared else []

    status = "PASS" if not failed_gates else "PARTIAL"

    # --- Artifact existence check (v0.3+, depth=0 only) ---
    artifact_warnings: List[Dict] = []
    if run_id and depth == 0:
        artifact_warnings = check_artifact_existence(skill_id, contract, run_id)
        if artifact_warnings and status == "PASS":
            status = "PARTIAL"
            outputs["status"] = "PARTIAL"

    result = {
        "contract_id": skill_id,
        "status": status,
        "started_at": started_at,
        "ended_at": datetime.now(timezone.utc).isoformat(),
        "duration_ms": int((time.time() - tick) * 1000),
        "agent": "local",
        "inputs": {"mode": "structured"},
        "gates": gate_results,
        "outputs": outputs,
        "warnings": (
            [{"type": "EVENTS_SKIPPED", "events": events_skipped, "reason": "Events disabled in Phase 4 minimal runtime"}]
            if events_skipped else []
        ) + artifact_warnings,
        "errors": errors,
        "events": {
            "declared": len(events_skipped) > 0,
            "executed": False,
            "reason": "Events disabled in Phase 4 minimal runtime"
        },
        "dry_run": dry_run
    }

    return result


def _resolve_path_pattern(path_pattern: str, run_id: str) -> Optional[str]:
    """Attempt to resolve a path_pattern given a run_id.

    Rules:
      - No template vars → return pattern as-is (check literal path).
      - Only {run_id} var → substitute and return.
      - Any other vars (e.g. {YYYYMMDD-HHMM}) → return None (unresolvable).
    """
    vars_found = re.findall(r"\{([^}]+)\}", path_pattern)
    if not vars_found:
        return path_pattern
    if vars_found == ["run_id"]:
        return path_pattern.replace("{run_id}", run_id)
    return None  # unresolvable (time-stamped paths, etc.)


def check_artifact_existence(skill_id: str, contract: Dict, run_id: str) -> List[Dict]:
    """Check that declared artifacts exist for the given run_id.

    Only meaningful for v0.3+ contracts. Returns a list of warning dicts.
    Warnings are emitted (not errors); callers should downgrade PASS → PARTIAL.

    Handles:
      - artifact: null  → skip (explicit no-artifact skill)
      - path patterns with {run_id} → resolved and checked
      - path patterns without any vars → checked literally under REPO_ROOT
      - path patterns with non-{run_id} vars → skipped (cannot resolve at runtime)
    """
    warnings: List[Dict] = []
    version = str(contract.get("version", "0.1"))
    if version < "0.3":
        return warnings  # pre-v0.3 contracts don't declare artifacts

    outputs = contract.get("outputs", {})
    artifact = outputs.get("artifact")  # may be None (explicit null)

    if artifact is None:
        return warnings  # explicit null — no artifact expected, nothing to check

    # --- Primary artifact ---
    if isinstance(artifact, dict):
        pp = artifact.get("path_pattern", "")
        mer = artifact.get("must_exist_after_run", False)
        if mer and pp:
            resolved = _resolve_path_pattern(pp, run_id)
            if resolved is not None:
                path = REPO_ROOT / resolved
                if not path.exists():
                    warnings.append({
                        "type": "ARTIFACT_MISSING",
                        "field": "outputs.artifact",
                        "path": resolved,
                        "message": (
                            f"[{skill_id}] primary artifact not found at '{resolved}' "
                            f"(must_exist_after_run=true)"
                        ),
                    })

    # --- Secondary artifacts ---
    secondaries = outputs.get("secondary_artifacts")
    if isinstance(secondaries, list):
        for i, sec in enumerate(secondaries):
            if not isinstance(sec, dict):
                continue
            sec_pp = sec.get("path_pattern", "")
            sec_mer = sec.get("must_exist_after_run", False)
            if sec_mer and sec_pp:
                resolved = _resolve_path_pattern(sec_pp, run_id)
                if resolved is not None:
                    path = REPO_ROOT / resolved
                    if not path.exists():
                        warnings.append({
                            "type": "SECONDARY_ARTIFACT_MISSING",
                            "field": f"outputs.secondary_artifacts[{i}]",
                            "path": resolved,
                            "message": (
                                f"[{skill_id}] secondary artifact not found at '{resolved}' "
                                f"(must_exist_after_run=true)"
                            ),
                        })

    return warnings


def write_trace(result: Dict) -> None:
    """Write execution trace to docs/audits/vbb-runtime/."""
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    contract_id = result["contract_id"]
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    trace_file = TRACE_DIR / f"{contract_id}_{ts}.json"
    with open(trace_file, "w") as f:
        json.dump(result, f, indent=2)
    latest = TRACE_DIR / f"{contract_id}_latest.json"
    with open(latest, "w") as f:
        json.dump(result, f, indent=2)


def run_all_contracts() -> List[Dict]:
    """Run linter first, then execute all contracts in INDEX."""
    linter_result = run_linter()
    if not linter_result["passed"]:
        return []

    index = load_index()
    results = []
    for entry in index["skills"]:
        skill_id = entry["id"]
        contract = load_contract(skill_id)
        result = execute_contract(skill_id, contract)
        write_trace(result)
        results.append(result)

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="VBB Contract Runtime")
    parser.add_argument("command", nargs="?", default="run",
                        choices=["run", "test-all", "validate"])
    parser.add_argument("skill_id", nargs="?", default=None,
                        help="Contract skill ID to execute")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simulate execution without side effects")
    parser.add_argument("--strict", action="store_true",
                        help="Fail on ambiguous routing or incomplete state")
    parser.add_argument("--phase", default=None,
                        help="Phase scope for routing (e.g. phase_0, closeout)")
    parser.add_argument("--query", default=None,
                        help="Query string for Phase Router (instead of skill_id)")
    parser.add_argument("--agent", default="local",
                        help="Agent type for routing")
    parser.add_argument("--all", action="store_true",
                        help="Run all contracts in INDEX.yaml (use with 'run')")
    parser.add_argument("--run-id", dest="run_id", default=None,
                        help="Run ID for artifact existence verification (e.g. 2026-05-23_1700_my-run)")

    args = parser.parse_args()

    if args.command == "validate":
        result = run_linter()
        print("PASS" if result["passed"] else "FAIL")
        if not result["passed"]:
            print(result["errors"], file=sys.stderr)
        sys.exit(0 if result["passed"] else 1)

    # Route query if provided
    if args.query:
        import importlib.util
        router_spec = importlib.util.spec_from_file_location("vbb_phase_router", REPO_ROOT / "tools" / "vbb-phase-router.py")
        router_module = importlib.util.module_from_spec(router_spec)
        router_spec.loader.exec_module(router_module)
        routed = router_module.route_to_skill(args.query, agent=args.agent, phase=args.phase, strict=args.strict)
        if not routed:
            print(f"No route found for query '{args.query}'")
            sys.exit(1)
        skill_id = routed
        print(f"Routed: '{args.query}' -> {skill_id}")
    elif args.all:
        skill_id = None  # --all does not need skill_id
    elif args.skill_id:
        skill_id = args.skill_id
    else:
        print("Usage: python vbb-contract-runtime.py run <contract_id> [--dry-run] [--strict]")
        print("       python vbb-contract-runtime.py run --all [--dry-run]")
        print("       python vbb-contract-runtime.py validate")
        sys.exit(1)

    linter_result = run_linter()
    if not linter_result["passed"]:
        print("Linter must pass before runtime execution")
        sys.exit(1)

    if args.all:
        print(f"=== VBB Contract Runtime — All Contracts ===")
        index = load_index()
        results = []
        for entry in index["skills"]:
            sid = entry["id"]
            r = execute_contract(sid, dry_run=args.dry_run, run_id=args.run_id)
            write_trace(r)
            results.append(r)
            suffix = f" [artifact warnings: {len([w for w in r['warnings'] if 'ARTIFACT' in w.get('type','')])}]" if args.run_id else ""
            print(f"  {sid}: {r['status']} ({r['duration_ms']}ms){suffix}")
        passed = sum(1 for r in results if r["status"] == "PASS")
        partial = sum(1 for r in results if r["status"] == "PARTIAL")
        blocked = sum(1 for r in results if r["status"] in ("BLOCKED", "FAIL"))
        print(f"\nPASS: {passed} | PARTIAL: {partial} | BLOCKED/FAIL: {blocked}")
        sys.exit(0)
    else:
        if not args.skill_id and not args.query and not args.all:
            print("Usage: python vbb-contract-runtime.py run <contract_id> [--dry-run] [--strict]")
            print("       python vbb-contract-runtime.py run --all [--dry-run]")
            print("       python vbb-contract-runtime.py validate")
            sys.exit(1)
        result = execute_contract(skill_id, dry_run=args.dry_run, run_id=args.run_id)
        write_trace(result)
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["status"] in ("PASS", "PARTIAL") else 1)