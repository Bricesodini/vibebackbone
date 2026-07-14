#!/usr/bin/env python3
"""
VBB Contract Linter — Phase 2
Validates VBB skill contracts (CONTRACT.yaml) against the schema.

Checks:
  1. YAML syntax
  2. Skill references (gates/events) exist in INDEX.yaml
  3. No circular dependencies
  4. Gate depth <= max_gate_depth
  5. Blocking gates have expected_status
  6. Outputs contain required fields
  7. Agents are recognized
  8. Contract schema version is explicit and supported
"""

import sys
import re
import yaml
from pathlib import Path
from typing import List, Dict, Set, Tuple

REPO_ROOT = Path(__file__).parent.parent.resolve()
SKILLS_DIR = REPO_ROOT / "skills"
INDEX_FILE = SKILLS_DIR / "INDEX.yaml"

KNOWN_AGENTS = {"claude-code", "codex", "pi", "opencode", "pi+", "pi-"}
PASS_STATUSES = {"PASS", "PARTIAL", "FAIL", "BLOCKED"}
SUPPORTED_VERSIONS = {"0.1", "0.2", "0.3"}
ARTIFACT_KINDS = {"phase_artifact", "audit_report", "ADR", "persistent_state_update"}
ARTIFACT_REQUIRED_FIELDS = {"path_pattern", "kind", "must_exist_after_run"}

# Non-blocking warning thresholds (CONVENTIONS.md Pillar 1, "SKILL.md description length")
DESCRIPTION_CHAR_TARGET = 500
DESCRIPTION_LINE_TARGET = 10


def load_index() -> Dict:
    with open(INDEX_FILE, "r") as f:
        return yaml.safe_load(f)


def get_indexed_skills() -> Set[str]:
    index = load_index()
    return {entry["id"] for entry in index.get("skills", [])}


def get_contract_skills() -> Set[str]:
    return {
        skill_dir.name
        for skill_dir in SKILLS_DIR.iterdir()
        if skill_dir.is_dir() and (skill_dir / "CONTRACT.yaml").exists()
    }


def load_contract(skill_dir: Path) -> Dict:
    contract_path = skill_dir / "CONTRACT.yaml"
    with open(contract_path, "r") as f:
        return yaml.safe_load(f)


def check_yaml_syntax(skill_id: str, contract: Dict) -> List[str]:
    errors = []
    required_top = [
        "id",
        "version",
        "contract_schema_version",
        "type",
        "formalization_level",
        "entrypoint",
        "compatibility",
        "inputs",
        "outputs",
        "gates",
        "events",
        "routing",
        "limits",
        "state_policy",
    ]
    for key in required_top:
        if key not in contract:
            errors.append(f"Missing top-level key: '{key}'")
    schema_version = str(
        contract.get("contract_schema_version", contract.get("version", ""))
    )
    if schema_version and schema_version not in SUPPORTED_VERSIONS:
        errors.append(
            f"Unsupported contract_schema_version: '{schema_version}' "
            f"(expected one of {sorted(SUPPORTED_VERSIONS)})"
        )
    if "version" in contract and "contract_schema_version" in contract:
        legacy_version = str(contract["version"])
        if legacy_version != schema_version:
            errors.append(
                f"version '{legacy_version}' must match contract_schema_version "
                f"'{schema_version}' while version is retained as a compatibility alias"
            )
    if "type" in contract and contract["type"] != "prompt_skill":
        errors.append(
            f"Unsupported type: '{contract['type']}' (expected 'prompt_skill')"
        )

    # Gate expected_status must match target contract's outputs.statuses
    # Done in check_gates to have access to all_contracts
    return errors


def check_gates(
    skill_id: str, contract: Dict, indexed: Set[str], all_contracts: Dict
) -> List[str]:
    errors = []
    gates = contract.get("gates", {})
    max_depth = contract.get("limits", {}).get("max_gate_depth", 2)
    for gate_type in ["before", "success", "after"]:
        for gate in gates.get(gate_type, []):
            gate_id = gate.get("id", "unknown")
            # Check depth
            if isinstance(gate, dict):
                depth = 1
                sub = gate.get("nested", [])
                while sub and depth <= max_depth:
                    depth += 1
                    sub = sub[0].get("nested", []) if sub else []
                if depth > max_depth:
                    errors.append(
                        f"[{skill_id}] gate '{gate_id}': depth {depth} > max {max_depth}"
                    )

            # Check blocking gate has expected_status
            if gate.get("blocking") and "expected_status" not in gate:
                errors.append(
                    f"[{skill_id}] gate '{gate_id}': blocking gate missing 'expected_status'"
                )

            # Check expected_status matches target contract's statuses
            if gate.get("blocking") and "expected_status" in gate and "skill" in gate:
                expected = gate["expected_status"]
                target_skill = gate["skill"]
                if target_skill in all_contracts:
                    target_statuses = (
                        all_contracts[target_skill]
                        .get("outputs", {})
                        .get("statuses", [])
                    )
                    if target_statuses and expected not in target_statuses:
                        errors.append(
                            f"[{skill_id}] gate '{gate_id}' expected_status '{expected}' not in target '{target_skill}' statuses {target_statuses}"
                        )

    return errors


def check_events(skill_id: str, contract: Dict, indexed: Set[str]) -> List[str]:
    errors = []
    events = contract.get("events", {})

    for event_type, handlers in events.items():
        for handler in handlers:
            ref_skill = handler.get("skill")
            if ref_skill:
                if ref_skill not in indexed:
                    errors.append(
                        f"[{skill_id}] event.{event_type}: references undefined skill '{ref_skill}' (indexed: {sorted(indexed)})"
                    )

    return errors


def check_circular_deps(
    skill_id: str, contract: Dict, all_contracts: Dict
) -> List[str]:
    errors = []
    visited = set()
    circular_found = []

    def dfs(sid: str, path: List[str]) -> bool:
        if sid in path:
            cycle_str = " -> ".join(path[path.index(sid) :] + [sid])
            circular_found.append(cycle_str)
            return True
        if sid in visited:
            return False
        visited.add(sid)
        path.append(sid)
        c = all_contracts.get(sid, {})
        for event_type, handlers in c.get("events", {}).items():
            for h in handlers:
                ref = h.get("skill")
                if ref and dfs(ref, path.copy()):
                    return True
        return False

    dfs(skill_id, [])
    for cycle in circular_found:
        errors.append(f"[{skill_id}] circular dependency detected: {cycle}")
    return errors


def check_outputs(skill_id: str, contract: Dict) -> List[str]:
    errors = []
    outputs = contract.get("outputs", {})
    required = outputs.get("required", [])
    expected = {"status", "summary", "next_action"}
    for field in expected:
        if field not in required:
            errors.append(f"[{skill_id}] outputs.required: missing '{field}'")
    statuses = outputs.get("statuses", [])
    if not all(s in PASS_STATUSES for s in statuses):
        errors.append(
            f"[{skill_id}] outputs.statuses: invalid statuses (expected {PASS_STATUSES})"
        )
    return errors


def check_agents(skill_id: str, contract: Dict) -> List[str]:
    errors = []
    agents = contract.get("compatibility", {}).get("agents", [])
    for agent in agents:
        if agent not in KNOWN_AGENTS:
            errors.append(
                f"[{skill_id}] agent '{agent}' not in known list {KNOWN_AGENTS}"
            )
    return errors


def _check_artifact_mapping(skill_id: str, label: str, artifact: Dict) -> List[str]:
    """Validate a single artifact mapping (primary or secondary)."""
    errors = []

    if not isinstance(artifact, dict):
        errors.append(
            f"[{skill_id}] {label}: must be a mapping (got {type(artifact).__name__})"
        )
        return errors

    # required fields
    for field in ARTIFACT_REQUIRED_FIELDS:
        if field not in artifact:
            errors.append(f"[{skill_id}] {label}: missing required field '{field}'")

    # path_pattern must be a non-empty string
    pp = artifact.get("path_pattern")
    if pp is not None and (not isinstance(pp, str) or not pp.strip()):
        errors.append(f"[{skill_id}] {label}.path_pattern: must be a non-empty string")

    # kind must be in the closed set
    kind = artifact.get("kind")
    if kind is not None and kind not in ARTIFACT_KINDS:
        errors.append(
            f"[{skill_id}] {label}.kind: '{kind}' not in {sorted(ARTIFACT_KINDS)}"
        )

    # must_exist_after_run must be a bool
    mer = artifact.get("must_exist_after_run")
    if mer is not None and not isinstance(mer, bool):
        errors.append(
            f"[{skill_id}] {label}.must_exist_after_run: must be a boolean (got {type(mer).__name__})"
        )

    # template, if specified, must point to an existing file
    tpl = artifact.get("template")
    if tpl is not None:
        if not isinstance(tpl, str) or not tpl.strip():
            errors.append(f"[{skill_id}] {label}.template: must be a non-empty string")
        else:
            tpl_path = REPO_ROOT / tpl
            if not tpl_path.exists():
                errors.append(
                    f"[{skill_id}] {label}.template: file not found at '{tpl}'"
                )

    # frontmatter_required, if specified, must be a list of strings
    fr = artifact.get("frontmatter_required")
    if fr is not None:
        if not isinstance(fr, list):
            errors.append(
                f"[{skill_id}] {label}.frontmatter_required: must be a list (got {type(fr).__name__})"
            )
        else:
            for i, key in enumerate(fr):
                if not isinstance(key, str):
                    errors.append(
                        f"[{skill_id}] {label}.frontmatter_required[{i}]: must be a string"
                    )

    # phase_artifact kind should declare a frontmatter_required (best practice)
    if kind == "phase_artifact" and fr is None:
        errors.append(
            f"[{skill_id}] {label}: kind=phase_artifact should declare 'frontmatter_required'"
        )

    return errors


def check_artifact(skill_id: str, contract: Dict) -> List[str]:
    """Validate outputs.artifact and outputs.secondary_artifacts (v0.3+)."""
    errors = []
    version = str(
        contract.get("contract_schema_version", contract.get("version", "0.1"))
    )

    # Schema field only required from v0.3 onwards.
    if version < "0.3":
        return errors

    outputs = contract.get("outputs", {})

    # outputs.artifact: required key (may be null for skills with no own artifact)
    if "artifact" not in outputs:
        errors.append(
            f"[{skill_id}] outputs.artifact: missing (required in v0.3+; use 'artifact: null' for skills with no file artifact)"
        )
    else:
        artifact = outputs["artifact"]
        if artifact is not None:
            errors.extend(
                _check_artifact_mapping(skill_id, "outputs.artifact", artifact)
            )

    # outputs.secondary_artifacts: optional list
    secondaries = outputs.get("secondary_artifacts")
    if secondaries is not None:
        if not isinstance(secondaries, list):
            errors.append(
                f"[{skill_id}] outputs.secondary_artifacts: must be a list (got {type(secondaries).__name__})"
            )
        else:
            for i, sec in enumerate(secondaries):
                errors.extend(
                    _check_artifact_mapping(
                        skill_id, f"outputs.secondary_artifacts[{i}]", sec
                    )
                )

    return errors


def check_description_length(skill_id: str) -> List[str]:
    """Non-blocking warning if SKILL.md description: exceeds the indicative target.

    Canon: CONVENTIONS.md Pillar 1, 'SKILL.md description length'.
    Target: <= DESCRIPTION_CHAR_TARGET chars AND <= DESCRIPTION_LINE_TARGET lines.
    Behavior: emits a warning (does NOT add to errors). Length is a proxy,
    not a quality guarantee — precise descriptions may legitimately exceed.
    """
    warnings = []
    skill_md = SKILLS_DIR / skill_id / "SKILL.md"
    if not skill_md.exists():
        return warnings

    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception as e:
        warnings.append(f"[{skill_id}] SKILL.md read error: {e}")
        return warnings

    # Extract frontmatter (between leading --- and next --- line)
    if not content.startswith("---\n"):
        return warnings
    end = content.find("\n---\n", 4)
    if end == -1:
        return warnings
    frontmatter = content[4:end]

    # Find description: | block (multi-line YAML literal)
    desc_match = re.search(
        r"^description:\s*\|\s*\n(.*?)(?=^[a-z_]+:|\Z)",
        frontmatter,
        re.MULTILINE | re.DOTALL,
    )
    if not desc_match:
        return warnings
    desc_text = desc_match.group(1)

    chars = len(desc_text.strip())
    lines = desc_text.strip().count("\n") + 1 if desc_text.strip() else 0

    if chars > DESCRIPTION_CHAR_TARGET or lines > DESCRIPTION_LINE_TARGET:
        warnings.append(
            f"[{skill_id}] SKILL.md description: {chars} chars / {lines} lines "
            f"(target: <= {DESCRIPTION_CHAR_TARGET} chars / <= {DESCRIPTION_LINE_TARGET} lines, "
            f"cf. CONVENTIONS.md Pillar 1). Non-blocking warning — length is a proxy, not a quality guarantee."
        )
    return warnings


def lint_all() -> Tuple[int, List[str], List[str]]:
    all_contracts = {}
    all_errors = []
    all_warnings: List[str] = []
    indexed = get_indexed_skills()
    contract_skills = get_contract_skills()

    missing_from_index = sorted(contract_skills - indexed)
    stale_index_entries = sorted(indexed - contract_skills)

    for skill_id in missing_from_index:
        all_errors.append(
            f"[{skill_id}] CONTRACT.yaml exists but skill is missing from INDEX.yaml"
        )
    for skill_id in stale_index_entries:
        all_errors.append(
            f"[{skill_id}] INDEX.yaml entry points to a skill without CONTRACT.yaml"
        )

    # Load all contracts
    for skill_dir in SKILLS_DIR.iterdir():
        if skill_dir.is_dir():
            contract_path = skill_dir / "CONTRACT.yaml"
            if contract_path.exists():
                try:
                    c = load_contract(skill_dir)
                    all_contracts[skill_dir.name] = c
                except Exception as e:
                    all_errors.append(f"[{skill_dir.name}] YAML parse error: {e}")

    # Lint each contract
    for skill_id, contract in all_contracts.items():
        all_errors.extend(check_yaml_syntax(skill_id, contract))
        all_errors.extend(check_gates(skill_id, contract, indexed, all_contracts))
        all_errors.extend(check_events(skill_id, contract, indexed))
        all_errors.extend(check_circular_deps(skill_id, contract, all_contracts))
        all_errors.extend(check_outputs(skill_id, contract))
        all_errors.extend(check_agents(skill_id, contract))
        all_errors.extend(check_artifact(skill_id, contract))

    # Non-blocking warnings: SKILL.md description length (CONVENTIONS.md Pillar 1)
    for skill_id in sorted(set(list(all_contracts.keys()) + list(indexed))):
        all_warnings.extend(check_description_length(skill_id))

    return len(all_errors), all_errors, all_warnings


if __name__ == "__main__":
    count, errors, warnings = lint_all()
    print(
        f"VBB Contract Linter — {len(errors)} error(s), {len(warnings)} warning(s) found"
    )
    for err in errors:
        print(f"  ✗ {err}")
    for warn in warnings:
        print(f"  ⚠️  {warn}")
    if count == 0:
        print("  ✓ All contracts valid")
    sys.exit(1 if count > 0 else 0)  # warnings do NOT change exit code
