"""Direct characterization tests for the formal VBB executor."""

import importlib.util
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).parent.parent
EXECUTOR_PATH = REPO_ROOT / "tools" / "vbb-executor.py"


@pytest.fixture()
def executor():
    spec = importlib.util.spec_from_file_location("vbb_executor_test", EXECUTOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def contract(*, before=None, after=None, max_depth=2):
    """Build the smallest contract needed to exercise executor gate semantics."""
    return {
        "outputs": {"required": ["status", "summary", "next_action"]},
        "gates": {
            "before": before or [],
            "success": [],
            "after": after or [],
        },
        "limits": {"max_gate_depth": max_depth},
    }


def blocking_gate(skill):
    return {
        "id": f"{skill}_required",
        "skill": skill,
        "blocking": True,
        "expected_status": "PASS",
    }


def install_contracts(monkeypatch, executor, contracts):
    monkeypatch.setattr(executor, "load_contract", contracts.get)


def test_valid_nested_before_gate_uses_contract_status(monkeypatch, executor):
    contracts = {
        "parent": contract(before=[blocking_gate("child")]),
        "child": contract(),
    }
    install_contracts(monkeypatch, executor, contracts)

    result = executor.execute_skill("parent", strict=True)

    assert result["state"] == executor.ExecutorState.DONE
    assert result["gates"][0]["actual"] == "PASS"
    assert result["gates"][0]["passed"] is True


def test_valid_nested_after_gate_uses_contract_status(monkeypatch, executor):
    contracts = {
        "parent": contract(after=[blocking_gate("child")]),
        "child": contract(),
    }
    install_contracts(monkeypatch, executor, contracts)

    result = executor.execute_skill("parent")

    assert result["state"] == executor.ExecutorState.DONE
    assert result["gates"][0]["actual"] == "PASS"
    assert result["gates"][0]["passed"] is True
    assert result["warnings"] == []


def test_cycle_is_blocked_without_python_recursion(monkeypatch, executor):
    contracts = {
        "alpha": contract(before=[blocking_gate("beta")]),
        "beta": contract(before=[blocking_gate("alpha")]),
    }
    install_contracts(monkeypatch, executor, contracts)

    result = executor.execute_skill("alpha", strict=True)

    assert result["state"] == executor.ExecutorState.BLOCKED
    assert any(error["code"] == "GATE_FAILED" for error in result["errors"])


def test_cycle_detection_emits_explicit_error(monkeypatch, executor):
    install_contracts(monkeypatch, executor, {"alpha": contract()})

    result = executor.execute_skill("alpha", ancestors=("alpha",))

    assert result["state"] == executor.ExecutorState.BLOCKED
    assert result["errors"][0]["code"] == "CIRCULAR_GATE_DEPENDENCY"


def test_depth_limit_blocks_long_gate_chain(monkeypatch, executor):
    contracts = {
        "level0": contract(before=[blocking_gate("level1")]),
        "level1": contract(before=[blocking_gate("level2")]),
        "level2": contract(before=[blocking_gate("level3")]),
        "level3": contract(),
    }
    install_contracts(monkeypatch, executor, contracts)

    result = executor.execute_skill("level0", strict=True)

    assert result["state"] == executor.ExecutorState.BLOCKED
    assert result["gates"][0]["actual"] == "BLOCKED"


def test_missing_nested_contract_blocks_parent(monkeypatch, executor):
    contracts = {"parent": contract(before=[blocking_gate("missing")])}
    install_contracts(monkeypatch, executor, contracts)

    result = executor.execute_skill("parent")

    assert result["state"] == executor.ExecutorState.BLOCKED
    assert result["gates"][0]["actual"] == "BLOCKED"


def test_missing_top_level_contract_is_explicit(monkeypatch, executor):
    install_contracts(monkeypatch, executor, {})

    result = executor.execute_skill("missing")

    assert result["state"] == executor.ExecutorState.BLOCKED
    assert result["errors"][0]["code"] == "CONTRACT_NOT_FOUND"


def test_static_gate_keeps_declared_expected_status(monkeypatch, executor):
    static = {
        "id": "manual_precondition",
        "blocking": True,
        "expected_status": "PASS",
    }
    contracts = {"parent": contract(before=[static])}
    install_contracts(monkeypatch, executor, contracts)

    result = executor.execute_skill("parent")

    assert result["state"] == executor.ExecutorState.DONE
    assert result["gates"][0]["actual"] == "PASS"


def test_yaml_loader_parses_mapping(tmp_path, executor):
    source = tmp_path / "contract.yaml"
    source.write_text("root:\n  enabled: true\n", encoding="utf-8")

    assert executor._yaml_load(source) == {"root": {"enabled": True}}


def test_closeout_writer_preserves_phase_contract(tmp_path, monkeypatch, executor):
    monkeypatch.setattr(executor, "RUNS_DIR", tmp_path)
    result = {
        "state": executor.ExecutorState.DONE,
        "started_at": "2026-07-14T12:00:00+00:00",
        "ended_at": "2026-07-14T12:00:01+00:00",
        "duration_ms": 1000,
        "outputs": {"summary": "characterized"},
        "errors": [],
        "warnings": [],
    }

    path = executor.write_closeout("test-run", "test-skill", result)

    assert path == tmp_path / "test-run" / "07_CLOSEOUT.md"
    content = path.read_text(encoding="utf-8")
    assert "phase: 07_CLOSEOUT" in content
    assert "**Verdict global**: `DONE`" in content
    assert "characterized" in content
    assert not hasattr(executor, "write_closEOUT")
