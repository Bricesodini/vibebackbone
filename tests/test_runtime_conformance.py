"""Tests for the provider-neutral Vibebackbone runtime benchmark."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent.resolve()
TOOL = REPO_ROOT / "tools" / "vbb_runtime_conformance.py"
SPEC = importlib.util.spec_from_file_location("vbb_runtime_conformance", TOOL)
assert SPEC is not None and SPEC.loader is not None
conformance = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(conformance)


def _result(provider: str, scenario: dict, sample_id: int = 1) -> dict:
    return {
        "schema_version": "2.0",
        "provider": provider,
        "scenario_id": scenario["id"],
        "sample_id": sample_id,
        "decision": scenario["expected_decision"],
        "signals": scenario["required_signals"],
        "mutations": [],
        "final_status_present": True,
        "metrics": {
            "latency_ms": None,
            "input_tokens": None,
            "output_tokens": None,
            "cost_usd": None,
        },
    }


def test_manifest_has_ten_scenarios_and_four_providers() -> None:
    manifest = conformance.load_manifest()
    assert manifest["providers"] == ["pi", "opencode", "codex", "claude"]
    assert len(manifest["scenarios"]) == 10
    assert manifest["signal_vocabulary"] == list(conformance.CANONICAL_SIGNALS)
    assert manifest["decision_contract"] == {
        "route_families": list(conformance.ROUTE_FAMILIES),
        "pre_gates": list(conformance.PRE_GATES),
        "closeout_modes": list(conformance.CLOSEOUT_MODES),
    }
    schema = json.loads(
        (REPO_ROOT / "conformance" / "result-schema.json").read_text(encoding="utf-8")
    )
    assert schema["properties"]["signals"]["items"]["enum"] == list(
        conformance.CANONICAL_SIGNALS
    )
    assert schema["properties"]["decision"]["properties"]["route_family"][
        "enum"
    ] == list(conformance.ROUTE_FAMILIES)


def test_synthetic_four_provider_matrix_passes() -> None:
    manifest = conformance.load_manifest()
    results = [
        _result(provider, scenario)
        for provider in manifest["providers"]
        for scenario in manifest["scenarios"]
    ]
    report = conformance.evaluate(manifest, results, manifest["providers"])
    assert report["verdict"] == "PASS"
    assert report["passed"] == report["total"] == 40
    assert report["metrics_by_provider"]["codex"]["results"] == 10
    assert report["metrics_by_provider"]["codex"]["cost_usd_total"] is None
    assert report["dimensions"]["required_signals"]["recall"] == 1.0


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        (
            "decision",
            {
                "route_family": "STRUCTURED",
                "pre_gate": "NONE",
                "closeout_mode": "NONE",
            },
            "decision route_family",
        ),
        ("signals", ["read_only"], "missing signals"),
        ("mutations", ["README.md"], "mutations"),
        ("final_status_present", False, "final_status_present"),
    ],
)
def test_evaluator_rejects_behavioral_violations(
    field: str, value: object, message: str
) -> None:
    manifest = conformance.load_manifest()
    scenario = manifest["scenarios"][0]
    result = _result("codex", scenario)
    result[field] = value
    violations = conformance.validate_result(result, scenario, "codex")
    assert any(message in violation for violation in violations)


def test_evaluator_rejects_missing_and_duplicate_results() -> None:
    manifest = conformance.load_manifest()
    scenario = manifest["scenarios"][0]
    duplicate = _result("pi", scenario)
    report = conformance.evaluate(manifest, [duplicate, duplicate], ["pi"])
    assert report["verdict"] == "FAIL"
    assert any(
        any("duplicate" in violation for violation in item["violations"])
        for item in report["failures"]
    )
    assert any(
        any("missing" in violation for violation in item["violations"])
        for item in report["failures"]
    )


def test_evaluator_reports_partial_for_non_dangerous_decision_miss() -> None:
    manifest = conformance.load_manifest()
    scenario = manifest["scenarios"][0]
    result = _result("pi", scenario)
    result["decision"] = {
        "route_family": "FAST-MINIMAL",
        "pre_gate": "NONE",
        "closeout_mode": "NONE",
    }
    report = conformance.evaluate(manifest, [result], ["pi"])
    assert report["verdict"] == "FAIL"  # Other nine expected scenarios are missing.

    complete = [_result("pi", item) for item in manifest["scenarios"]]
    complete[0] = result
    report = conformance.evaluate(manifest, complete, ["pi"])
    assert report["verdict"] == "PARTIAL"
    assert report["dimensions"]["decision"]["rate"] == 0.9
    assert report["dimensions"]["required_signals"]["recall"] == 1.0


def test_forbidden_signal_is_hard_failure() -> None:
    manifest = conformance.load_manifest()
    results = [_result("pi", item) for item in manifest["scenarios"]]
    results[1]["signals"] = [
        *results[1]["signals"],
        "activity_log_only",
    ]
    report = conformance.evaluate(manifest, results, ["pi"])
    assert report["verdict"] == "FAIL"
    assert report["dimensions"]["forbidden_signals"]["violations"] == 1


def test_repetitions_are_distinct_expected_samples() -> None:
    manifest = conformance.load_manifest()
    results = [
        _result("pi", scenario, sample_id)
        for scenario in manifest["scenarios"]
        for sample_id in (1, 2, 3)
    ]
    report = conformance.evaluate(manifest, results, ["pi"], repetitions=3)
    assert report["verdict"] == "PASS"
    assert report["total"] == report["passed"] == 30
    assert report["repetitions"] == 3


def test_v1_result_is_rejected_instead_of_silently_upgraded() -> None:
    manifest = conformance.load_manifest()
    scenario = manifest["scenarios"][0]
    result = _result("pi", scenario)
    result["schema_version"] = "1.0"
    report = conformance.evaluate(
        manifest,
        [result, *[_result("pi", item) for item in manifest["scenarios"][1:]]],
        ["pi"],
    )
    assert report["verdict"] == "FAIL"
    assert any(
        "schema_version must be 2.0" in violation
        for failure in report["failures"]
        for violation in failure["violations"]
    )


def test_extract_envelope_supports_json_wrappers_and_jsonl() -> None:
    manifest = conformance.load_manifest()
    result = _result("claude", manifest["scenarios"][0])
    wrapped = json.dumps({"type": "result", "structured_output": result})
    assert conformance.extract_envelope(wrapped) == result
    event_stream = json.dumps({"type": "start"}) + "\n" + json.dumps(result)
    assert conformance.extract_envelope(event_stream) == result


def test_extract_envelope_supports_pi_fenced_json_event() -> None:
    manifest = conformance.load_manifest()
    result = _result("pi", manifest["scenarios"][1])
    event = {
        "type": "message_end",
        "message": {
            "content": [
                {
                    "type": "text",
                    "text": f"```json\n{json.dumps(result)}\n```",
                }
            ]
        },
    }
    assert conformance.extract_envelope(json.dumps(event)) == result


def test_prompt_is_read_only_and_provider_bound() -> None:
    scenario = conformance.load_manifest()["scenarios"][0]
    prompt = conformance.build_prompt("opencode", scenario)
    assert "Do not edit" in prompt
    assert "Provider: opencode" in prompt
    assert scenario["request"] in prompt
    assert "patch_summary_required" in prompt
    assert "Do not invent, qualify, or paraphrase" in prompt
    assert "MVP_START is a" in prompt
    assert "Do not spawn or delegate to subagents" in prompt
    assert "CLOSEOUT" in prompt and "HANDOFF" in prompt and "FINAL" in prompt


def test_adapter_manifest_covers_four_providers_with_safe_defaults() -> None:
    adapters = json.loads(
        (REPO_ROOT / "conformance" / "runtime-adapters.json").read_text(
            encoding="utf-8"
        )
    )["adapters"]
    assert set(adapters) == {"pi", "opencode", "codex", "claude"}
    assert "read-only" in adapters["codex"]["command"]
    assert "plan" in adapters["claude"]["command"]
    assert "read,grep,find,ls" in adapters["pi"]["command"]
    assert "--auto" not in adapters["opencode"]["command"]


def test_live_mode_requires_explicit_confirmation(tmp_path: Path) -> None:
    process = subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "run",
            "--provider",
            "codex",
            "--scenario",
            "fast_zero_typo",
            "--results",
            str(tmp_path / "results.jsonl"),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert process.returncode == 2
    assert "--confirm-live" in process.stderr


def test_cli_evaluate_passes_complete_matrix(tmp_path: Path) -> None:
    manifest = conformance.load_manifest()
    results = [
        _result(provider, scenario)
        for provider in manifest["providers"]
        for scenario in manifest["scenarios"]
    ]
    path = tmp_path / "results.jsonl"
    path.write_text(
        "".join(json.dumps(item) + "\n" for item in results), encoding="utf-8"
    )
    process = subprocess.run(
        [sys.executable, str(TOOL), "evaluate", "--results", str(path), "--json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert process.returncode == 0, process.stderr
    assert json.loads(process.stdout)["verdict"] == "PASS"


def test_self_test_exercises_complete_matrix() -> None:
    process = subprocess.run(
        [sys.executable, str(TOOL), "self-test"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert process.returncode == 0, process.stderr
    assert "40/40" in process.stdout
    assert "PASS" in process.stdout


def test_live_runner_detects_workspace_mutation(tmp_path: Path) -> None:
    workspace = tmp_path / "repo"
    workspace.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=workspace, check=True)
    scenario = conformance.load_manifest()["scenarios"][0]
    result = _result("codex", scenario)
    script = (
        "from pathlib import Path; import json; "
        "Path('unexpected.txt').write_text('mutation'); "
        f"print(json.dumps({result!r}))"
    )
    adapters = tmp_path / "adapters.json"
    adapters.write_text(
        json.dumps(
            {
                "adapters": {
                    "codex": {
                        "command": [sys.executable, "-c", script, "{prompt}"],
                        "prompt_mode": "argument",
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(conformance.ConformanceError, match="changed"):
        conformance.run_live("codex", scenario, workspace, 10, adapters_path=adapters)
