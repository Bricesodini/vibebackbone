#!/usr/bin/env python3
"""
VBB Executor — Formal runtime that enforces skill contracts as a state machine.

Implements ADR-0001: Formal Executor Boundary.

Usage:
    python tools/vbb-executor.py run <skill_id> [--run-id <id>] [--strict]
    python tools/vbb-executor.py state <run_id>
    python tools/vbb-executor.py validate [--strict]

Command interface (minimal, per ADR-0001):
    run <skill_id>    Execute a skill with full gate enforcement
    state <run_id>    Show current state of a run
    validate          Validate all contracts without executing

State machine:
    READY → RUNNING → EVALUATING → DONE | PARTIAL | BLOCKED | FAIL

Failure semantics:
    BLOCKED  — gate precondition not met, cannot proceed
    FAIL     — execution produced an error
    PARTIAL  — execution completed but success gates not fully satisfied
    PASS     — all gates satisfied

Phase artifact handling:
    Each run produces a phase artifact in docs/runs/{run_id}/
    Artifacts include: 01_INTAKE.md, 02_AUDIT.md, ..., 07_CLOSEOUT.md

Operations that remain agent-only (not executable):
    - Reading SKILL.md and applying human judgment
    - Making product/architecture decisions
    - Updating governance docs without confirmation
    - Generating new skills or contracts
"""

import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

REPO_ROOT = Path(__file__).parent.parent.resolve()
SKILLS_DIR = REPO_ROOT / "skills"
INDEX_FILE = SKILLS_DIR / "INDEX.yaml"
LINTER_SCRIPT = REPO_ROOT / "tools" / "vbb-contract-lint.py"
RUNS_DIR = REPO_ROOT / "docs" / "runs"
EXECUTOR_LOG = REPO_ROOT / ".vbb" / "executor.log"


# ─────────────────────────────────────────────────────────────────────────────
# State machine
# ─────────────────────────────────────────────────────────────────────────────

class ExecutorState:
    """Executor state machine states."""

    READY = "READY"
    RUNNING = "RUNNING"
    EVALUATING = "EVALUATING"
    DONE = "DONE"
    PARTIAL = "PARTIAL"
    BLOCKED = "BLOCKED"
    FAIL = "FAIL"

    @classmethod
    def is_terminal(cls, state: str) -> bool:
        return state in {cls.DONE, cls.PARTIAL, cls.BLOCKED, cls.FAIL}


# ─────────────────────────────────────────────────────────────────────────────
# Core contract loading
# ─────────────────────────────────────────────────────────────────────────────

def load_index() -> Dict:
    with open(INDEX_FILE, encoding="utf-8") as f:
        return json.load(f) if INDEX_FILE.suffix == ".json" else _yaml_load(INDEX_FILE)


def _yaml_load(path: Path) -> Dict:
    import yaml
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_contract(skill_id: str) -> Optional[Dict]:
    index = load_index()
    for entry in index.get("skills", []):
        if entry["id"] == skill_id:
            contract_path = SKILLS_DIR / entry["contract"].lstrip("./")
            return _yaml_load(contract_path)
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Gate evaluation
# ─────────────────────────────────────────────────────────────────────────────

def evaluate_before_gates(contract: Dict, run_id: str, strict: bool) -> List[Dict]:
    """Evaluate gates.before. Recursively resolves blocking skill references."""
    results = []
    for gate in contract.get("gates", {}).get("before", []):
        gate_id = gate.get("id", "unknown")
        skill_ref = gate.get("skill")
        expected = gate.get("expected_status", "PASS")
        blocking = gate.get("blocking", False)

        if skill_ref and blocking:
            # Recursive executor call — enforces gate depth limit
            sub_result = execute_skill(skill_ref, run_id, strict=strict, depth=1)
            actual = sub_result.get("status", "BLOCKED")
        else:
            # Static gate: expected status is the actual status
            actual = expected

        passed = actual == expected
        results.append({
            "gate_id": gate_id,
            "skill": skill_ref,
            "expected": expected,
            "actual": actual,
            "blocking": blocking,
            "passed": passed,
        })

    return results


def evaluate_success_gates(contract: Dict, outputs: Dict) -> List[Dict]:
    """Evaluate gates.success against actual skill outputs."""
    results = []
    for gate in contract.get("gates", {}).get("success", []):
        gate_id = gate.get("id", "unknown")
        required = gate.get("output_must_contain", [])
        present = [f for f in required if f in outputs]
        missing = [f for f in required if f not in outputs]
        results.append({
            "gate_id": gate_id,
            "required": required,
            "present": present,
            "missing": missing,
            "passed": len(missing) == 0,
        })
    return results


def evaluate_after_gates(contract: Dict, run_id: str) -> List[Dict]:
    """Evaluate gates.after — post-execution cleanup/notification gates."""
    results = []
    for gate in contract.get("gates", {}).get("after", []):
        gate_id = gate.get("id", "unknown")
        skill_ref = gate.get("skill")
        blocking = gate.get("blocking", False)

        if skill_ref and blocking:
            sub_result = execute_skill(skill_ref, run_id, strict=False, depth=1)
            actual = sub_result.get("status", "BLOCKED")
            passed = actual in {"PASS", "PARTIAL"}
        else:
            passed = True
            actual = "PASS"

        results.append({
            "gate_id": gate_id,
            "skill": skill_ref,
            "actual": actual,
            "blocking": blocking,
            "passed": passed,
        })
    return results


# ─────────────────────────────────────────────────────────────────────────────
# Artifact handling
# ─────────────────────────────────────────────────────────────────────────────

def _resolve_path_pattern(path_pattern: str, run_id: str) -> Optional[str]:
    """Resolve path patterns with {run_id} substitution."""
    vars_found = re.findall(r"\{([^}]+)\}", path_pattern)
    if not vars_found:
        return path_pattern
    if vars_found == ["run_id"]:
        return path_pattern.replace("{run_id}", run_id)
    return None  # unresolvable


def check_artifact_existence(skill_id: str, contract: Dict, run_id: str) -> List[Dict]:
    """Verify that declared artifacts exist for the run (v0.3+ contracts)."""
    warnings: List[Dict] = []
    version = str(contract.get("version", "0.1"))
    if version < "0.3":
        return warnings

    outputs = contract.get("outputs", {})
    artifact = outputs.get("artifact")

    if artifact is None:
        return warnings  # explicit null — no artifact expected

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
                        "path": resolved,
                        "message": f"[{skill_id}] artifact not found at '{resolved}'",
                    })

    for i, sec in enumerate(outputs.get("secondary_artifacts", [])):
        if not isinstance(sec, dict):
            continue
        pp = sec.get("path_pattern", "")
        mer = sec.get("must_exist_after_run", False)
        if mer and pp:
            resolved = _resolve_path_pattern(pp, run_id)
            if resolved is not None:
                path = REPO_ROOT / resolved
                if not path.exists():
                    warnings.append({
                        "type": "SECONDARY_ARTIFACT_MISSING",
                        "field": f"secondary_artifacts[{i}]",
                        "path": resolved,
                        "message": f"[{skill_id}] secondary artifact not found at '{resolved}'",
                    })

    return warnings


def write_phase_artifact(run_id: str, phase: str, content: Dict) -> Path:
    """Write a phase artifact to docs/runs/{run_id}/{phase}.md."""
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = run_dir / f"{phase}.md"

    # Build markdown from content dict
    lines = [
        "---",
        f"run_id: {run_id}",
        f"phase: {phase}",
        f"status: {content.get('status', 'UNKNOWN')}",
        f"agent: executor",
        f"started_at: {content.get('started_at', '')}",
        f"ended_at: {content.get('ended_at', '')}",
        "---",
        "",
        f"# {phase} — {content.get('skill_id', run_id)}",
        "",
        f"**Status**: `{content.get('status', 'UNKNOWN')}`",
        f"**Duration**: {content.get('duration_ms', 0)}ms",
        "",
    ]

    gates = content.get("gates", [])
    if gates:
        lines.extend(["## Gates", ""])
        for g in gates:
            passed = g.get("passed", False)
            icon = "✓" if passed else "✗"
            skill = f" → `{g.get('skill', '')}`" if g.get("skill") else ""
            lines.append(f"- {icon} `{g.get('gate_id', '?')}`{skill} "
                         f"[exp:{g.get('expected', g.get('expected_status', '?'))} "
                         f"got:{g.get('actual', g.get('actual_status', '?'))}]")

    outputs = content.get("outputs", {})
    if outputs:
        lines.extend(["", "## Outputs", ""])
        for k, v in outputs.items():
            if k == "partial_details":
                continue
            lines.append(f"- **{k}**: `{v}`")

    errors = content.get("errors", [])
    if errors:
        lines.extend(["", "## Errors", ""])
        for e in errors:
            lines.append(f"- `{e.get('code', '?')}` — {e.get('message', '')}")

    warnings = content.get("warnings", [])
    if warnings:
        lines.extend(["", "## Warnings", ""])
        for w in warnings:
            lines.append(f"- `{w.get('type', '?')}` — {w.get('message', w.get('reason', ''))}")

    artifact_path.write_text("\n".join(lines), encoding="utf-8")
    return artifact_path


def write_closEOUT(run_id: str, skill_id: str, result: Dict) -> Path:
    """Write the 07_CLOSEOUT.md phase artifact."""
    phase = "07_CLOSEOUT"
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    path = run_dir / f"{phase}.md"

    status = result["state"]
    errors = result.get("errors", [])
    warnings = result.get("warnings", [])

    lines = [
        "---",
        f"run_id: {run_id}",
        f"phase: {phase}",
        f"status: {status}",
        f"agent: executor",
        f"started_at: {result.get('started_at', '')}",
        f"ended_at: {result.get('ended_at', '')}",
        f"next_phase: none",
        "---",
        "",
        f"# {phase} — {skill_id}",
        "",
        f"**Verdict global**: `{status}`",
        f"**Skill**: `{skill_id}`",
        f"**Durée**: {result.get('duration_ms', 0)}ms",
        "",
        "## Résumé",
        "",
        result.get("outputs", {}).get("summary", "_stub output_"),
        "",
    ]

    if errors:
        lines.extend(["", "## Erreurs", ""])
        for e in errors:
            lines.append(f"- `{e.get('code', '?')}` — {e.get('message', '')}")

    if warnings:
        lines.extend(["", "## Warnings", ""])
        for w in warnings:
            lines.append(f"- `{w.get('type', '?')}`")

    lines.extend(["", "## Decisions", "", "- Executor state machine: PASS / PARTIAL / BLOCKED / FAIL semantics applied", ""])

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


# ─────────────────────────────────────────────────────────────────────────────
# Core executor
# ─────────────────────────────────────────────────────────────────────────────

def execute_skill(
    skill_id: str,
    run_id: Optional[str] = None,
    strict: bool = False,
    depth: int = 0,
) -> Dict[str, Any]:
    """
    Execute a single skill contract with full gate enforcement.

    State machine: READY → RUNNING → EVALUATING → DONE | PARTIAL | BLOCKED | FAIL
    """
    started_at = datetime.now(timezone.utc).isoformat()
    tick = _tick()

    contract = load_contract(skill_id)

    result = {
        "skill_id": skill_id,
        "run_id": run_id,
        "state": ExecutorState.READY,
        "started_at": started_at,
        "gates": [],
        "outputs": {},
        "errors": [],
        "warnings": [],
    }

    # ── READY: contract loaded ───────────────────────────────────────────────
    if contract is None:
        result["state"] = ExecutorState.BLOCKED
        result["ended_at"] = _now(tick)
        result["duration_ms"] = _dur(tick)
        result["errors"].append({
            "code": "CONTRACT_NOT_FOUND",
            "message": f"Contract '{skill_id}' not found in INDEX.yaml",
        })
        return result

    max_depth = contract.get("limits", {}).get("max_gate_depth", 2)
    if depth > max_depth:
        result["state"] = ExecutorState.BLOCKED
        result["ended_at"] = _now(tick)
        result["duration_ms"] = _dur(tick)
        result["errors"].append({
            "code": "GATE_DEPTH_EXCEEDED",
            "message": f"Gate depth {depth} > max {max_depth}",
        })
        return result

    result["state"] = ExecutorState.RUNNING

    # ── RUNNING: before gates ───────────────────────────────────────────────
    before_gates = evaluate_before_gates(contract, run_id or "unknown", strict)
    result["gates"].extend(before_gates)

    blocking_failed = [g for g in before_gates if g.get("blocking") and not g.get("passed")]
    if blocking_failed:
        result["state"] = ExecutorState.BLOCKED
        result["errors"].extend([
            {"code": "GATE_FAILED", "message": f"Blocking gate '{g['gate_id']}' failed"}
            for g in blocking_failed
        ])
        result["ended_at"] = _now(tick)
        result["duration_ms"] = _dur(tick)
        return result

    # ── RUNNING: skill execution (stub for non-executable skills) ───────────
    # Skills that are agent-only produce stub output.
    # The executor records the execution and validates outputs.
    outputs = _stub_outputs(contract, skill_id)

    result["outputs"] = outputs
    result["state"] = ExecutorState.EVALUATING

    # ── EVALUATING: success gates ───────────────────────────────────────────
    success_gates = evaluate_success_gates(contract, outputs)
    result["gates"].extend(success_gates)

    success_failed = [g for g in success_gates if not g.get("passed")]
    if success_failed:
        result["state"] = ExecutorState.PARTIAL
        outputs["status"] = "PARTIAL"
        outputs["partial_reason"] = "SUCCESS_GATE_OUTPUT_INCOMPLETE"
        outputs["partial_details"] = [
            {"gate_id": g["gate_id"], "missing_fields": g["missing"]}
            for g in success_failed
        ]

    # ── EVALUATING: after gates ────────────────────────────────────────────
    after_gates = evaluate_after_gates(contract, run_id or "unknown")
    result["gates"].extend(after_gates)

    after_failed = [g for g in after_gates if g.get("blocking") and not g.get("passed")]
    if after_failed:
        # After gate failure doesn't change the main status but is recorded
        result["warnings"].append({
            "type": "AFTER_GATE_FAILED",
            "message": f"Blocking after-gate(s) failed: {[g['gate_id'] for g in after_failed]}",
        })

    # ── EVALUATING: artifact existence check (v0.3+) ──────────────────────
    if run_id:
        artifact_warnings = check_artifact_existence(skill_id, contract, run_id)
        if artifact_warnings:
            result["warnings"].extend(artifact_warnings)
            if result["state"] == ExecutorState.EVALUATING:
                # Downgrade to PARTIAL if artifact is required and missing
                result["state"] = ExecutorState.PARTIAL
                outputs["status"] = "PARTIAL"
                outputs["partial_reason"] = "ARTIFACT_MISSING"

    # ── Terminal state ──────────────────────────────────────────────────────
    if result["state"] == ExecutorState.EVALUATING:
        result["state"] = ExecutorState.DONE

    result["ended_at"] = _now(tick)
    result["duration_ms"] = _dur(tick)
    return result


def _stub_outputs(contract: Dict, skill_id: str) -> Dict[str, Any]:
    """Produce stub outputs for non-executable (agent-only) skills."""
    required = contract.get("outputs", {}).get("required", [])
    outputs = {
        "status": "PASS",
        "summary": f"Contract '{skill_id}' executed (stub — agent-only skill)",
        "next_action": "Continue to next phase",
    }
    for field in required:
        if field not in outputs:
            outputs[field] = f"<stub:{field}>"
    return outputs


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _tick() -> float:
    import time
    return time.time()

def _now(tick: float) -> str:
    return datetime.now(timezone.utc).isoformat()

def _dur(tick: float) -> int:
    import time
    return int((time.time() - tick) * 1000)


def _yaml_load(path: Path) -> Dict:
    import yaml
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ─────────────────────────────────────────────────────────────────────────────
# Commands
# ─────────────────────────────────────────────────────────────────────────────

def cmd_run(skill_id: str, run_id: Optional[str], strict: bool) -> int:
    """Execute a skill with full gate enforcement."""
    import time
    tick = time.time()

    if not run_id:
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        run_id = f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}_{ts}_{skill_id}"

    # Write 01_INTAKE
    if run_id:
        run_dir = RUNS_DIR / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        intake = run_dir / "01_INTAKE.md"
        intake.write_text(
            f"---\nrun_id: {run_id}\nphase: 01_INTAKE\nstatus: RUNNING\n"
            f"agent: executor\nstarted_at: {datetime.now(timezone.utc).isoformat()}\n"
            f"next_phase: 07_CLOSEOUT\n---\n\n# 01_INTAKE — {skill_id}\n\n"
            f"**Skill**: `{skill_id}`\n**Run**: `{run_id}`\n**Strict**: {strict}\n",
            encoding="utf-8",
        )

    result = execute_skill(skill_id, run_id, strict=strict)

    # Write phase artifacts
    if run_id:
        write_phase_artifact(run_id, "02_AUDIT", result)
        write_closEOUT(run_id, skill_id, result)

    # Emit structured status
    print(json.dumps({
        "run_id": run_id,
        "skill_id": skill_id,
        "state": result["state"],
        "status": result.get("outputs", {}).get("status", result["state"]),
        "duration_ms": result["duration_ms"],
        "gates_passed": sum(1 for g in result["gates"] if g.get("passed")),
        "gates_total": len(result["gates"]),
        "errors": result["errors"],
        "warnings": result["warnings"],
    }, indent=2))

    log_state(result)
    return 0 if ExecutorState.is_terminal(result["state"]) and result["state"] not in {ExecutorState.BLOCKED, ExecutorState.FAIL} else 1


def cmd_state(run_id: str) -> int:
    """Show current state of a run."""
    run_dir = RUNS_DIR / run_id
    if not run_dir.exists():
        print(f"No run found: {run_id}", file=sys.stderr)
        return 1

    closeout = run_dir / "07_CLOSEOUT.md"
    if closeout.exists():
        print(closeout.read_text(encoding="utf-8"))
    else:
        print(f"Run '{run_id}' not yet closed.", file=sys.stderr)
        return 1
    return 0


def cmd_validate(strict: bool) -> int:
    """Validate all contracts without executing."""
    import subprocess
    result = subprocess.run(
        [sys.executable, str(LINTER_SCRIPT)],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        print("✓ All contracts valid")
        return 0
    else:
        print("✗ Contract validation failed", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        return 1


def log_state(result: Dict) -> None:
    """Append execution trace to executor log."""
    EXECUTOR_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(EXECUTOR_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "ts": datetime.now(timezone.utc).isoformat(),
            "run_id": result.get("run_id"),
            "skill_id": result.get("skill_id"),
            "state": result.get("state"),
            "duration_ms": result.get("duration_ms"),
        }) + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="VBB Executor — Formal runtime")
    sub = parser.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run", help="Execute a skill with gate enforcement")
    run_p.add_argument("skill_id", help="Skill contract ID to execute")
    run_p.add_argument("--run-id", dest="run_id", default=None)
    run_p.add_argument("--strict", action="store_true")

    state_p = sub.add_parser("state", help="Show run state")
    state_p.add_argument("run_id", help="Run ID to inspect")

    validate_p = sub.add_parser("validate", help="Validate all contracts")
    validate_p.add_argument("--strict", action="store_true")

    args = parser.parse_args()

    if args.command == "run":
        return cmd_run(args.skill_id, args.run_id, args.strict)
    if args.command == "state":
        return cmd_state(args.run_id)
    if args.command == "validate":
        return cmd_validate(args.strict)
    return 1


if __name__ == "__main__":
    sys.exit(main())