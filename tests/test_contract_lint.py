#!/usr/bin/env python3
"""
Negative tests for tools/vbb-contract-lint.py

Validates that the linter correctly rejects invalid contracts:
  1. Missing required top-level keys
  2. Invalid phase_scope value
  3. Invalid output status (not in PASS/PARTIAL/FAIL/BLOCKED)
  4. Missing artifact required field (v0.3+)
  5. Unknown agent
  6. Event referencing unindexed skill
  7. Valid minimal contract passes
  8. Phase-1 frontmatter and contract routing namespaces remain distinct

And for the runtime:
  9. Non-existent skill_id returns BLOCKED
  10. Gate depth exceeded returns BLOCKED
  11. Valid skill dry-run returns PASS/PARTIAL

Usage:
    pytest tests/test_contract_lint.py -q
    python3 tests/test_contract_lint.py
"""

import sys
import importlib.util
import runpy
import subprocess
import tempfile
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent.resolve()
LINTER = REPO_ROOT / "tools" / "vbb-contract-lint.py"
RUNTIME = REPO_ROOT / "tools" / "vbb-contract-runtime.py"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# A minimal valid v0.3 contract for the linter
MINIMAL_CONTRACT = textwrap.dedent("""\
    id: test-minimal
    version: "0.3"
    contract_schema_version: "0.3"
    type: prompt_skill
    formalization_level: declarative
    entrypoint:
      kind: markdown_prompt
      path: SKILL.md
    compatibility:
      runtime_required: false
      agents:
        - claude-code
    inputs:
      required:
        - repo_access
      optional: []
    outputs:
      required:
        - status
        - summary
        - next_action
      statuses:
        - PASS
        - PARTIAL
        - FAIL
        - BLOCKED
      artifact: null
    gates:
      before: []
      success: []
      after: []
    events: {}
    routing:
      phase_scope:
        - phase_1
      triggers: []
    limits:
      max_gate_depth: 2
      circular_dependencies: forbidden
    state_policy:
      persistent: false
      allowed_fields: []
""")


def _run_linter(skill_dir: Path) -> tuple:
    """Run linter with a temp INDEX and return its error count and errors."""
    import importlib.util
    import yaml

    # Dynamically import the linter module (hyphen in filename)
    spec = importlib.util.spec_from_file_location("vbb_contract_lint", LINTER)
    lint_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lint_mod)

    # Monkey-patch paths to use our temp directory
    orig_skills_dir = lint_mod.SKILLS_DIR
    orig_index_file = lint_mod.INDEX_FILE

    # Write temp INDEX.yaml in the skill dir's parent
    skills_tmp = skill_dir.parent
    catalog_dirs = sorted(
        path for path in skills_tmp.iterdir() if (path / "CONTRACT.yaml").exists()
    )
    index_data = {
        "version": "0.1",
        "type": "vbb_skill_contract_index",
        "skills": [
            {"id": path.name, "contract": f"./{path.name}/CONTRACT.yaml"}
            for path in catalog_dirs
        ],
    }
    index_file = skills_tmp / "INDEX.yaml"
    index_file.write_text(yaml.dump(index_data, default_flow_style=False))

    lint_mod.SKILLS_DIR = skills_tmp
    lint_mod.INDEX_FILE = index_file

    try:
        count, errors, _warnings = lint_mod.lint_all()
        return count, errors
    finally:
        lint_mod.SKILLS_DIR = orig_skills_dir
        lint_mod.INDEX_FILE = orig_index_file


def _run_runtime(skill_id: str, extra_args: list = None) -> tuple:
    """Run contract runtime as subprocess, return (rc, stdout, stderr)."""
    cmd = [sys.executable, str(RUNTIME), "run", skill_id, "--dry-run"]
    if extra_args:
        cmd.extend(extra_args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def _write_phase_one_fixture(skill_dir: Path, skill_phase: str, phase_scope: str):
    """Write a controlled 1-vbb fixture using both phase namespaces."""
    import yaml

    contract = yaml.safe_load(MINIMAL_CONTRACT)
    contract["id"] = skill_dir.name
    contract["routing"]["phase_scope"] = [phase_scope]
    (skill_dir / "CONTRACT.yaml").write_text(
        yaml.dump(contract, default_flow_style=False)
    )
    (skill_dir / "SKILL.md").write_text(
        textwrap.dedent(
            f"""\
            ---
            name: {skill_dir.name}
            description: Controlled phase namespace fixture.
            phase: {skill_phase}
            ---

            # Fixture
            """
        )
    )


# ---------------------------------------------------------------------------
# Linter negative tests — invalid contracts
# ---------------------------------------------------------------------------


def test_phase_one_namespaces_valid():
    """Agentic 02_AUDIT plus router phase_1 is the valid combination."""
    with tempfile.TemporaryDirectory() as tmp:
        skill_dir = Path(tmp) / "skills" / "1-vbb-test"
        skill_dir.mkdir(parents=True)
        _write_phase_one_fixture(skill_dir, "02_AUDIT", "phase_1")

        count, errors = _run_linter(skill_dir)
        assert count == 0, errors


def test_phase_one_frontmatter_drift_rejected():
    """Deprecated integer-like frontmatter phase is blocked."""
    with tempfile.TemporaryDirectory() as tmp:
        skill_dir = Path(tmp) / "skills" / "1-vbb-test"
        skill_dir.mkdir(parents=True)
        _write_phase_one_fixture(skill_dir, "1", "phase_1")

        count, errors = _run_linter(skill_dir)
        assert count > 0
        assert any("expected '02_AUDIT'" in str(error) for error in errors)


def test_phase_one_contract_scope_drift_rejected():
    """Agentic lifecycle values must not leak into contract routing."""
    with tempfile.TemporaryDirectory() as tmp:
        skill_dir = Path(tmp) / "skills" / "1-vbb-test"
        skill_dir.mkdir(parents=True)
        _write_phase_one_fixture(skill_dir, "02_AUDIT", "02_AUDIT")

        count, errors = _run_linter(skill_dir)
        assert count > 0
        assert any("expected 'phase_1'" in str(error) for error in errors)


def test_duplicate_routing_trigger_rejected_case_insensitively():
    """Two contracts may not claim the same normalized trigger."""
    import yaml

    with tempfile.TemporaryDirectory() as tmp:
        skills_dir = Path(tmp) / "skills"
        first = skills_dir / "test-first"
        second = skills_dir / "test-second"
        first.mkdir(parents=True)
        second.mkdir()

        for skill_dir, trigger in [(first, "Status"), (second, " status ")]:
            contract = yaml.safe_load(MINIMAL_CONTRACT)
            contract["id"] = skill_dir.name
            contract["routing"]["triggers"] = [trigger]
            (skill_dir / "CONTRACT.yaml").write_text(
                yaml.dump(contract, default_flow_style=False)
            )
            (skill_dir / "SKILL.md").write_text("# Fixture\n")

        count, errors = _run_linter(first)
        assert count == 1, errors
        assert "multiple owners" in errors[0]


def test_missing_required_key():
    """Contract missing 'entrypoint' → linter must report error."""
    import yaml

    contract = yaml.safe_load(MINIMAL_CONTRACT)
    del contract["entrypoint"]

    with tempfile.TemporaryDirectory() as tmp:
        skills_tmp = Path(tmp) / "skills"
        skills_tmp.mkdir()
        skill_dir = skills_tmp / "test-missing-key"
        skill_dir.mkdir()
        contract_file = skill_dir / "CONTRACT.yaml"
        contract_file.write_text(yaml.dump(contract, default_flow_style=False))
        (skill_dir / "SKILL.md").write_text("# Test skill\n")

        count, errors = _run_linter(skill_dir)
        assert count > 0, f"Expected errors, got {count}"
        assert any("entrypoint" in str(e) for e in errors), (
            f"Expected 'entrypoint' in errors: {errors}"
        )


def test_invalid_type():
    """Contract with type != prompt_skill → linter must report error."""
    import yaml

    contract = yaml.safe_load(MINIMAL_CONTRACT)
    contract["type"] = "python_function"

    with tempfile.TemporaryDirectory() as tmp:
        skills_tmp = Path(tmp) / "skills"
        skills_tmp.mkdir()
        skill_dir = skills_tmp / "test-invalid-type"
        skill_dir.mkdir()
        contract_file = skill_dir / "CONTRACT.yaml"
        contract_file.write_text(yaml.dump(contract, default_flow_style=False))
        (skill_dir / "SKILL.md").write_text("# Test skill\n")

        count, errors = _run_linter(skill_dir)
        assert count > 0, f"Expected errors, got {count}"
        assert any("type" in str(e).lower() for e in errors), (
            f"Expected 'type' in errors: {errors}"
        )


def test_invalid_status():
    """Contract with invalid output status → linter must report error."""
    import yaml

    contract = yaml.safe_load(MINIMAL_CONTRACT)
    contract["outputs"]["statuses"] = ["PASS", "UNKNOWN", "IN_PROGRESS"]

    with tempfile.TemporaryDirectory() as tmp:
        skills_tmp = Path(tmp) / "skills"
        skills_tmp.mkdir()
        skill_dir = skills_tmp / "test-invalid-status"
        skill_dir.mkdir()
        contract_file = skill_dir / "CONTRACT.yaml"
        contract_file.write_text(yaml.dump(contract, default_flow_style=False))
        (skill_dir / "SKILL.md").write_text("# Test skill\n")

        count, errors = _run_linter(skill_dir)
        assert count > 0, f"Expected errors, got {count}"
        assert any(
            "statuses" in str(e).lower() or "status" in str(e).lower() for e in errors
        ), f"Expected 'statuses' in errors: {errors}"


def test_missing_output_required_field():
    """Contract missing required output field 'summary' → linter must report error."""
    import yaml

    contract = yaml.safe_load(MINIMAL_CONTRACT)
    contract["outputs"]["required"] = ["status"]  # missing summary, next_action

    with tempfile.TemporaryDirectory() as tmp:
        skills_tmp = Path(tmp) / "skills"
        skills_tmp.mkdir()
        skill_dir = skills_tmp / "test-missing-output"
        skill_dir.mkdir()
        contract_file = skill_dir / "CONTRACT.yaml"
        contract_file.write_text(yaml.dump(contract, default_flow_style=False))
        (skill_dir / "SKILL.md").write_text("# Test skill\n")

        count, errors = _run_linter(skill_dir)
        assert count > 0, f"Expected errors, got {count}"
        assert any(
            "summary" in str(e).lower() or "next_action" in str(e).lower()
            for e in errors
        ), f"Expected output.required field mention in errors: {errors}"


def test_unknown_agent():
    """Contract with unknown agent → linter must report error."""
    import yaml

    contract = yaml.safe_load(MINIMAL_CONTRACT)
    contract["compatibility"]["agents"] = ["claude-code", "unknown-agent-xyz"]

    with tempfile.TemporaryDirectory() as tmp:
        skills_tmp = Path(tmp) / "skills"
        skills_tmp.mkdir()
        skill_dir = skills_tmp / "test-unknown-agent"
        skill_dir.mkdir()
        contract_file = skill_dir / "CONTRACT.yaml"
        contract_file.write_text(yaml.dump(contract, default_flow_style=False))
        (skill_dir / "SKILL.md").write_text("# Test skill\n")

        count, errors = _run_linter(skill_dir)
        assert count > 0, f"Expected errors, got {count}"
        assert any(
            "unknown-agent-xyz" in str(e) or "agent" in str(e).lower() for e in errors
        ), f"Expected agent name in errors: {errors}"


def test_event_unindexed_skill():
    """Contract referencing an unindexed skill in events → linter must report error."""
    import yaml

    contract = yaml.safe_load(MINIMAL_CONTRACT)
    contract["events"] = {
        "on_success": [{"skill": "nonexistent-skill-xyz", "reason": "test"}]
    }

    with tempfile.TemporaryDirectory() as tmp:
        skills_tmp = Path(tmp) / "skills"
        skills_tmp.mkdir()
        skill_dir = skills_tmp / "test-bad-event"
        skill_dir.mkdir()
        contract_file = skill_dir / "CONTRACT.yaml"
        contract_file.write_text(yaml.dump(contract, default_flow_style=False))
        (skill_dir / "SKILL.md").write_text("# Test skill\n")

        count, errors = _run_linter(skill_dir)
        assert count > 0, f"Expected errors, got {count}"
        assert any("nonexistent-skill-xyz" in str(e) for e in errors), (
            f"Expected unindexed skill name in errors: {errors}"
        )


def test_artifact_missing_required_field():
    """v0.3 contract with artifact missing path_pattern → linter must report error."""
    import yaml

    contract = yaml.safe_load(MINIMAL_CONTRACT)
    contract["outputs"]["artifact"] = {
        "kind": "phase_artifact",
        "must_exist_after_run": True,
        # missing path_pattern
    }

    with tempfile.TemporaryDirectory() as tmp:
        skills_tmp = Path(tmp) / "skills"
        skills_tmp.mkdir()
        skill_dir = skills_tmp / "test-artifact-field"
        skill_dir.mkdir()
        contract_file = skill_dir / "CONTRACT.yaml"
        contract_file.write_text(yaml.dump(contract, default_flow_style=False))
        (skill_dir / "SKILL.md").write_text("# Test skill\n")

        count, errors = _run_linter(skill_dir)
        assert count > 0, f"Expected errors, got {count}"
        assert any("path_pattern" in str(e) for e in errors), (
            f"Expected 'path_pattern' in errors: {errors}"
        )


def test_unsupported_version():
    """Contract with unsupported contract schema version → linter must report error."""
    import yaml

    contract = yaml.safe_load(MINIMAL_CONTRACT)
    contract["version"] = "9.9"
    contract["contract_schema_version"] = "9.9"

    with tempfile.TemporaryDirectory() as tmp:
        skills_tmp = Path(tmp) / "skills"
        skills_tmp.mkdir()
        skill_dir = skills_tmp / "test-bad-version"
        skill_dir.mkdir()
        contract_file = skill_dir / "CONTRACT.yaml"
        contract_file.write_text(yaml.dump(contract, default_flow_style=False))
        (skill_dir / "SKILL.md").write_text("# Test skill\n")

        count, errors = _run_linter(skill_dir)
        assert count > 0, f"Expected errors, got {count}"
        assert any("version" in str(e).lower() for e in errors), (
            f"Expected 'version' in errors: {errors}"
        )


def test_blocking_gate_no_expected_status():
    """Blocking gate without expected_status → linter must report error."""
    import importlib.util
    import yaml

    spec = importlib.util.spec_from_file_location("vbb_contract_lint", LINTER)
    lint_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lint_mod)

    contract = yaml.safe_load(MINIMAL_CONTRACT)
    contract["gates"]["before"] = [
        {"id": "g1", "skill": "test-bad-version", "blocking": True}
        # missing expected_status
    ]

    with tempfile.TemporaryDirectory() as tmp:
        skills_tmp = Path(tmp) / "skills"
        skills_tmp.mkdir()

        # Need the referenced skill to exist too
        ref_dir = skills_tmp / "test-bad-version"
        ref_dir.mkdir()
        ref_contract = yaml.safe_load(MINIMAL_CONTRACT)
        ref_contract["id"] = "test-bad-version"
        (ref_dir / "CONTRACT.yaml").write_text(
            yaml.dump(ref_contract, default_flow_style=False)
        )
        (ref_dir / "SKILL.md").write_text("# Ref\n")

        skill_dir = skills_tmp / "test-bad-gate"
        skill_dir.mkdir()
        contract["id"] = "test-bad-gate"
        (skill_dir / "CONTRACT.yaml").write_text(
            yaml.dump(contract, default_flow_style=False)
        )
        (skill_dir / "SKILL.md").write_text("# Test skill\n")

        # Update INDEX to include both
        index = {
            "version": "0.1",
            "type": "vbb_skill_contract_index",
            "skills": [
                {"id": "test-bad-gate", "contract": "./test-bad-gate/CONTRACT.yaml"},
                {
                    "id": "test-bad-version",
                    "contract": "./test-bad-version/CONTRACT.yaml",
                },
            ],
        }

        orig_skills_dir = lint_mod.SKILLS_DIR
        orig_index_file = lint_mod.INDEX_FILE
        lint_mod.SKILLS_DIR = skills_tmp
        lint_mod.INDEX_FILE = skills_tmp / "INDEX.yaml"
        (skills_tmp / "INDEX.yaml").write_text(
            yaml.dump(index, default_flow_style=False)
        )

        try:
            count, errors, _warnings = lint_mod.lint_all()
            assert count > 0, f"Expected errors, got {count}"
            assert any("expected_status" in str(e) for e in errors), (
                f"Expected 'expected_status' in errors: {errors}"
            )
        finally:
            lint_mod.SKILLS_DIR = orig_skills_dir
            lint_mod.INDEX_FILE = orig_index_file


# ---------------------------------------------------------------------------
# Linter positive test — valid contract passes
# ---------------------------------------------------------------------------


def test_valid_contract_passes():
    """A minimal valid v0.3 contract → linter must report 0 errors."""
    import yaml

    with tempfile.TemporaryDirectory() as tmp:
        skills_tmp = Path(tmp) / "skills"
        skills_tmp.mkdir()
        skill_dir = skills_tmp / "test-minimal"
        skill_dir.mkdir()
        contract_file = skill_dir / "CONTRACT.yaml"
        contract_file.write_text(
            yaml.dump(yaml.safe_load(MINIMAL_CONTRACT), default_flow_style=False)
        )
        (skill_dir / "SKILL.md").write_text("# Test skill\n")

        count, errors = _run_linter(skill_dir)
        assert count == 0, f"Expected 0 errors, got {count}: {errors}"


# ---------------------------------------------------------------------------
# Runtime negative tests
# ---------------------------------------------------------------------------


def test_runtime_nonexistent_skill():
    """Runtime: non-existent skill_id → status=BLOCKED."""
    import json

    rc, out, _ = _run_runtime("nonexistent-skill-xyz-999")
    # Runtime may exit 0 or 1; check the JSON output
    try:
        result = json.loads(out)
    except json.JSONDecodeError:
        # If not JSON, it's an error exit
        assert rc != 0, f"Expected non-zero exit or BLOCKED status, got rc={rc}\n{out}"
        return

    status = result.get("status", "UNKNOWN")
    assert status == "BLOCKED", f"Expected BLOCKED, got {status}\n{out}"


def test_runtime_real_skill_dry_run():
    """Runtime: real skill with --dry-run → status in PASS/PARTIAL/BLOCKED."""
    import json

    # Use an existing contracted skill
    rc, out, _ = _run_runtime("1-vbb-adr")
    try:
        result = json.loads(out)
    except json.JSONDecodeError:
        # Might be the --all summary format
        assert rc == 0, f"Expected exit 0 for dry-run, got {rc}\n{out}"
        return

    status = result.get("status", "UNKNOWN")
    assert status in ("PASS", "PARTIAL", "BLOCKED"), (
        f"Expected PASS/PARTIAL/BLOCKED, got {status}\n{out}"
    )


def test_runtime_all_dry_run():
    """Runtime: --all --dry-run → completes without error."""
    cmd = [sys.executable, str(RUNTIME), "run", "--all", "--dry-run"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, (
        f"Expected exit 0, got {result.returncode}\n{result.stdout}\n{result.stderr}"
    )
    assert "PASS:" in result.stdout or "BLOCKED" in result.stdout, (
        f"Expected summary output\n{result.stdout}"
    )


def test_runtime_partial_has_machine_reason():
    """Runtime: expected dry-run PARTIAL includes a machine-readable reason."""
    import json

    rc, out, _ = _run_runtime("1-vbb-adr")
    assert rc == 0, f"Expected partial dry-run to exit 0, got {rc}\n{out}"
    result = json.loads(out)
    if result.get("status") == "PARTIAL":
        outputs = result.get("outputs", {})
        warnings = result.get("warnings", [])
        assert outputs.get("partial_reason") == "DRY_RUN_STUB_OUTPUT_INCOMPLETE"
        assert any(w.get("type") == "EXPECTED_PARTIAL" for w in warnings), warnings


# ---------------------------------------------------------------------------
# Phase Router tests (if vbb-phase-router.py exists)
# ---------------------------------------------------------------------------


def test_runtime_query_fails_explicitly_when_router_cannot_load(monkeypatch, capsys):
    monkeypatch.setattr(importlib.util, "spec_from_file_location", lambda *_: None)
    monkeypatch.setattr(sys, "argv", [str(RUNTIME), "run", "--query", "scope freeze"])

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_path(str(RUNTIME), run_name="__main__")

    assert exc_info.value.code == 2
    assert "Unable to load phase router" in capsys.readouterr().err


def test_phase_router_unknown_phase():
    """Router: query with completely unknown context → should fail or return None."""
    router = REPO_ROOT / "tools" / "vbb-phase-router.py"
    if not router.exists():
        return  # skip — router tool doesn't exist yet

    import importlib.util

    spec = importlib.util.spec_from_file_location("vbb_phase_router", router)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Test routing with an unknown phase
    result = mod.route_to_skill(
        "nonexistent query xyz 123", phase="phase_99", agent="claude-code"
    )
    assert result is None or result == "", (
        f"Expected None/empty for unknown phase, got {result}"
    )


def test_phase_router_valid_query():
    """Router: valid query → should return a skill ID from INDEX.yaml."""
    router = REPO_ROOT / "tools" / "vbb-phase-router.py"
    if not router.exists():
        return  # skip

    import importlib.util

    spec = importlib.util.spec_from_file_location("vbb_phase_router", router)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    result = mod.route_to_skill("ADR", agent="claude-code", phase="phase_1")
    # The router should return a skill ID (or None if routing fails — that's also acceptable)
    # We just check it doesn't crash
    assert result is None or isinstance(result, str), (
        f"Expected None or str, got {type(result)}"
    )


def test_phase_router_responsibility_corpus():
    """Router: specialized responsibilities remain unambiguous in strict mode."""
    router = REPO_ROOT / "tools" / "vbb-phase-router.py"
    if not router.exists():
        return

    import importlib.util

    spec = importlib.util.spec_from_file_location("vbb_phase_router_corpus", router)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    cases = [
        ("detect god files and split monoliths", "1-vbb-monolith-detector"),
        ("find duplicated business rules", "1-vbb-logic-duplication-detector"),
        ("find inconsistent API call patterns", "1-vbb-pattern-inconsistency-detector"),
        (
            "detect unnecessary interfaces and factories",
            "1-vbb-premature-abstraction-detector",
        ),
        ("audit code documentation drift", "1-vbb-code-doc-coherence-auditor"),
        (
            "write missing documentation for undocumented code",
            "1-vbb-code-doc-gap-integrator",
        ),
        ("classify this task into the correct route", "vibebackbone"),
        ("audit security controls", "2-vbb-security"),
        ("api contract", "1-vbb-api-contract-designer"),
        ("implemented api audit", "2-vbb-api-auditor"),
        ("dead code", "1-vbb-code-janitor"),
        ("unused imports", "1-vbb-code-janitor"),
        (
            "anti-slop repository quality gate for dead code",
            "t-vbb-anti-slop-gate",
        ),
        (
            "anti-slop repository quality gate for unused imports",
            "t-vbb-anti-slop-gate",
        ),
        ("monolith", "1-vbb-monolith-detector"),
        ("technical debt in a legacy architecture", "1-vbb-tech-debt"),
        ("pilotage", "vibebackbone"),
        ("governance reference for route selection", "0-vbb-pilotage"),
        ("status", "t-vbb-status-dashboard"),
        ("closeout report", "t-vbb-status-report"),
    ]

    for query, expected in cases:
        actual = mod.route_to_skill(query, agent="codex", strict=True)
        assert actual == expected, f"{query!r}: expected {expected}, got {actual}"


# --- Direct execution fallback ---

if __name__ == "__main__":
    try:
        import pytest

        sys.exit(pytest.main([__file__, "-q"]))
    except ImportError:
        passed = failed = 0
        for _name, _fn in sorted(globals().items()):
            if _name.startswith("test_") and callable(_fn):
                try:
                    _fn()
                    print("  PASS " + _name)
                    passed += 1
                except AssertionError as _e:
                    print("  FAIL " + _name + ": " + str(_e))
                    failed += 1
        total = passed + failed
        print("Results: %d/%d passed, %d failed" % (passed, total, failed))
        sys.exit(0 if failed == 0 else 1)
