#!/usr/bin/env python3
"""Evaluate or optionally run the Vibebackbone multi-runtime benchmark.

Deterministic evaluation is suitable for CI and never invokes an LLM. Live
execution requires ``--confirm-live`` and snapshots Git state before/after each
provider call. The provider is required to return the shared JSON envelope.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).parent.parent.resolve()
DEFAULT_MANIFEST = REPO_ROOT / "conformance" / "runtime-scenarios.json"
DEFAULT_SCHEMA = REPO_ROOT / "conformance" / "result-schema.json"
DEFAULT_ADAPTERS = REPO_ROOT / "conformance" / "runtime-adapters.json"
SUPPORTED_PROVIDERS = ("pi", "opencode", "codex", "claude")
SCHEMA_VERSION = "2.0"
ROUTE_FAMILIES = (
    "FAST-ZERO",
    "FAST-MINIMAL",
    "FAST-STANDARD",
    "STRUCTURED",
    "AUDIT",
    "ENGINE_ONLY",
    "CLOSEOUT",
)
PRE_GATES = ("NONE", "MVP_START")
CLOSEOUT_MODES = ("NONE", "HANDOFF", "FINAL")
CANONICAL_SIGNALS = (
    "read_only",
    "scope_bounded",
    "activity_log_only",
    "patch_summary_required",
    "direct_action_allowed",
    "plan_required",
    "gate_required",
    "audit_report_required",
    "implementation_blocked",
    "blocking_questions_required",
    "risk_escalated",
    "surface_cartography_required",
    "session_handoff_required",
    "session_clear_required",
)
DERIVED_SIGNAL_NAMES = frozenset({"read_only"})
FENCED_JSON_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)


class ConformanceError(ValueError):
    """Raised when a manifest, result, or live invocation is invalid."""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConformanceError(f"cannot load JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ConformanceError(f"expected a JSON object in {path}")
    return value


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    manifest = _load_json(path)
    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise ConformanceError(f"manifest schema_version must be {SCHEMA_VERSION}")
    providers = manifest.get("providers")
    if providers != list(SUPPORTED_PROVIDERS):
        raise ConformanceError("manifest must list the four canonical providers")
    if manifest.get("signal_vocabulary") != list(CANONICAL_SIGNALS):
        raise ConformanceError("manifest signal_vocabulary must match the canon")
    expected_contract = {
        "route_families": list(ROUTE_FAMILIES),
        "pre_gates": list(PRE_GATES),
        "closeout_modes": list(CLOSEOUT_MODES),
    }
    if manifest.get("decision_contract") != expected_contract:
        raise ConformanceError("manifest decision_contract must match the canon")
    scenarios = manifest.get("scenarios")
    if not isinstance(scenarios, list) or len(scenarios) != 10:
        raise ConformanceError("manifest must contain exactly ten scenarios")
    ids: set[str] = set()
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            raise ConformanceError("every scenario must be an object")
        scenario_id = scenario.get("id")
        if not isinstance(scenario_id, str) or not scenario_id:
            raise ConformanceError("every scenario needs a non-empty id")
        if scenario_id in ids:
            raise ConformanceError(f"duplicate scenario id: {scenario_id}")
        ids.add(scenario_id)
        decision = scenario.get("expected_decision")
        if not isinstance(decision, dict) or set(decision) != {
            "route_family",
            "pre_gate",
            "closeout_mode",
        }:
            raise ConformanceError(f"invalid expected_decision for {scenario_id}")
        if (
            decision["route_family"] not in ROUTE_FAMILIES
            or decision["pre_gate"] not in PRE_GATES
            or decision["closeout_mode"] not in CLOSEOUT_MODES
        ):
            raise ConformanceError(f"unknown decision value for {scenario_id}")
        required = scenario.get("required_signals")
        if not isinstance(required, list) or not all(
            isinstance(item, str) for item in required
        ):
            raise ConformanceError(f"invalid required_signals for {scenario_id}")
        unknown = sorted(set(required) - set(CANONICAL_SIGNALS))
        if unknown:
            raise ConformanceError(
                f"unknown required_signals for {scenario_id}: {', '.join(unknown)}"
            )
        forbidden = scenario.get("forbidden_signals")
        if not isinstance(forbidden, list) or not all(
            isinstance(item, str) for item in forbidden
        ):
            raise ConformanceError(f"invalid forbidden_signals for {scenario_id}")
        unknown = sorted(set(forbidden) - set(CANONICAL_SIGNALS))
        if unknown:
            raise ConformanceError(
                f"unknown forbidden_signals for {scenario_id}: {', '.join(unknown)}"
            )
        overlap = sorted(set(required) & set(forbidden))
        if overlap:
            raise ConformanceError(
                f"required/forbidden overlap for {scenario_id}: {', '.join(overlap)}"
            )
    return manifest


def _scenario_map(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in manifest["scenarios"]}


def build_prompt(provider: str, scenario: dict[str, Any], sample_id: int = 1) -> str:
    if provider not in SUPPORTED_PROVIDERS:
        raise ConformanceError(f"unsupported provider: {provider}")
    if sample_id < 1:
        raise ConformanceError("sample_id must be positive")
    return f"""You are running a read-only Vibebackbone conformance benchmark.
Classify the request using the governance loaded by your runtime. Do not edit,
write, commit, push, or install. Do not spawn or delegate to subagents. You may
inspect and apply loaded governance files and skills. Return exactly one JSON
object matching the result contract and no prose.

Provider: {provider}
Scenario: {scenario["id"]}
Sample: {sample_id}
Request: {scenario["request"]}

DECISION CARD (mandatory):
1. Select exactly one route_family, pre_gate, and closeout_mode.
2. Declare semantic signals such as scope_bounded; read_only is adapter-derived
   and must be left to the runner.
3. Use closeout_mode NONE unless the request explicitly asks to close; HANDOFF
   and FINAL are mutually exclusive.
4. Before returning, check for forbidden signals and for a closeout mode on a
   non-closeout request.
5. For CLOSEOUT, HANDOFF requires session_handoff_required and forbids
   session_clear_required; FINAL requires session_clear_required and forbids
   session_handoff_required. The decision object must contain only its three
   declared fields.

Return decision with exactly three fields. route_family must be one of:
{", ".join(ROUTE_FAMILIES)}. pre_gate must be one of: {", ".join(PRE_GATES)}.
closeout_mode must be one of: {", ".join(CLOSEOUT_MODES)}. MVP_START is a
pre-gate, not a route family. HANDOFF and FINAL are closeout modes.

Include only signals you actually applied, using only these exact identifiers:
{", ".join(CANONICAL_SIGNALS)}.
Do not invent, qualify, or paraphrase signal identifiers. mutations must remain
empty. final_status_present must be true because this benchmark response is
complete. Use null for unavailable metrics. The required object keys are:
schema_version="2.0", provider, scenario_id, sample_id, decision, signals
(string array), derived_signals (string array; return [] because the runner
supplies the authoritative value),
mutations (string array), final_status_present, and metrics
containing latency_ms, input_tokens, output_tokens, and cost_usd.
"""


def validate_result(
    result: dict[str, Any],
    scenario: dict[str, Any],
    provider: str,
    sample_id: int = 1,
) -> list[str]:
    violations: list[str] = []
    allowed_fields = {
        "schema_version",
        "provider",
        "scenario_id",
        "sample_id",
        "decision",
        "signals",
        "derived_signals",
        "mutations",
        "final_status_present",
        "metrics",
    }
    extra_fields = sorted(set(result) - allowed_fields)
    if extra_fields:
        violations.append(f"unexpected fields: {', '.join(extra_fields)}")
    expected_types: dict[str, type[Any]] = {
        "schema_version": str,
        "provider": str,
        "scenario_id": str,
        "sample_id": int,
        "decision": dict,
        "signals": list,
        "derived_signals": list,
        "mutations": list,
        "final_status_present": bool,
        "metrics": dict,
    }
    for field, expected_type in expected_types.items():
        if field not in result:
            violations.append(f"missing field: {field}")
        elif not isinstance(result[field], expected_type):
            violations.append(f"invalid type for {field}")
    if violations:
        return violations
    if result["schema_version"] != SCHEMA_VERSION:
        violations.append(f"schema_version must be {SCHEMA_VERSION}")
    if result["provider"] != provider:
        violations.append(f"provider must be {provider}")
    if result["scenario_id"] != scenario["id"]:
        violations.append(f"scenario_id must be {scenario['id']}")
    if isinstance(result["sample_id"], bool) or result["sample_id"] != sample_id:
        violations.append(f"sample_id must be {sample_id}")
    decision = result["decision"]
    decision_fields = {"route_family", "pre_gate", "closeout_mode"}
    extra_decision = sorted(set(decision) - decision_fields)
    missing_decision = sorted(decision_fields - set(decision))
    if extra_decision:
        violations.append(f"unexpected decision fields: {', '.join(extra_decision)}")
    if missing_decision:
        violations.append(f"missing decision fields: {', '.join(missing_decision)}")
    if not extra_decision and not missing_decision:
        allowed_decisions = {
            "route_family": ROUTE_FAMILIES,
            "pre_gate": PRE_GATES,
            "closeout_mode": CLOSEOUT_MODES,
        }
        for field, allowed in allowed_decisions.items():
            value = decision[field]
            if not isinstance(value, str) or value not in allowed:
                violations.append(f"invalid decision value: {field}")
            elif value != scenario["expected_decision"][field]:
                violations.append(
                    f"decision {field} {value!r} != "
                    f"{scenario['expected_decision'][field]!r}"
                )
    signals = result["signals"]
    if not all(isinstance(item, str) for item in signals):
        violations.append("signals must contain strings only")
    else:
        unknown = sorted(set(signals) - set(CANONICAL_SIGNALS))
        if unknown:
            violations.append(f"unknown signals: {', '.join(unknown)}")
        missing = sorted(
            (set(scenario["required_signals"]) - DERIVED_SIGNAL_NAMES) - set(signals)
        )
        if missing:
            violations.append(f"missing signals: {', '.join(missing)}")
        forbidden = sorted(set(scenario["forbidden_signals"]) & set(signals))
        if forbidden:
            violations.append(f"forbidden signals: {', '.join(forbidden)}")
    derived_signals = result.get("derived_signals", [])
    if not all(isinstance(item, str) for item in derived_signals):
        violations.append("derived_signals must contain strings only")
    else:
        unknown_derived = sorted(set(derived_signals) - set(CANONICAL_SIGNALS))
        if unknown_derived:
            violations.append(f"unknown derived signals: {', '.join(unknown_derived)}")
    mutations = result["mutations"]
    if mutations:
        violations.append("read-only scenario reported mutations")
    if result["final_status_present"] is not True:
        violations.append("final_status_present must be true")
    metrics = result["metrics"]
    metric_fields = ("latency_ms", "input_tokens", "output_tokens", "cost_usd")
    extra_metrics = sorted(set(metrics) - set(metric_fields))
    if extra_metrics:
        violations.append(f"unexpected metrics: {', '.join(extra_metrics)}")
    for field in metric_fields:
        if field not in metrics:
            violations.append(f"missing metric: {field}")
            continue
        value = metrics[field]
        expected = (
            (int, type(None)) if field != "cost_usd" else (int, float, type(None))
        )
        if not isinstance(value, expected) or isinstance(value, bool):
            violations.append(f"invalid metric type: {field}")
        elif value is not None and value < 0:
            violations.append(f"metric must be non-negative: {field}")
    return violations


def read_results(path: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ConformanceError(f"cannot read results {path}: {exc}") from exc
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ConformanceError(f"invalid JSONL line {line_number}: {exc}") from exc
        if not isinstance(value, dict):
            raise ConformanceError(f"result line {line_number} is not an object")
        results.append(value)
    return results


def evaluate(
    manifest: dict[str, Any],
    results: Iterable[dict[str, Any]],
    providers: Iterable[str],
    repetitions: int = 1,
) -> dict[str, Any]:
    if repetitions < 1:
        raise ConformanceError("repetitions must be positive")
    scenarios = _scenario_map(manifest)
    selected = tuple(providers)
    result_list = list(results)
    expected = {
        (provider, scenario_id, sample_id)
        for provider in selected
        for scenario_id in scenarios
        for sample_id in range(1, repetitions + 1)
    }
    seen: dict[tuple[str, str, int], dict[str, Any]] = {}
    failures: list[dict[str, Any]] = []
    hard_failure = False
    for result in result_list:
        provider_value = result.get("provider")
        scenario_value = result.get("scenario_id")
        sample_value = result.get("sample_id")
        if (
            not isinstance(provider_value, str)
            or not isinstance(scenario_value, str)
            or not isinstance(sample_value, int)
            or isinstance(sample_value, bool)
        ):
            failures.append(
                {
                    "key": (
                        str(provider_value),
                        str(scenario_value),
                        str(sample_value),
                    ),
                    "violations": [
                        "provider/scenario_id must be strings and sample_id an integer"
                    ],
                }
            )
            hard_failure = True
            continue
        provider = provider_value
        scenario_id = scenario_value
        sample_id = sample_value
        key = (provider, scenario_id, sample_id)
        if key not in expected:
            failures.append({"key": key, "violations": ["unexpected result"]})
            hard_failure = True
            continue
        if key in seen:
            failures.append({"key": key, "violations": ["duplicate result"]})
            hard_failure = True
            continue
        seen[key] = result
        violations = validate_result(
            result, scenarios[scenario_id], provider, sample_id=sample_id
        )
        if violations:
            failures.append({"key": key, "violations": violations})
            soft_prefixes = ("decision ", "missing signals:")
            if any(not violation.startswith(soft_prefixes) for violation in violations):
                hard_failure = True
    missing = sorted(expected - set(seen))
    for key in missing:
        failures.append({"key": key, "violations": ["missing result"]})
        hard_failure = True
    total = len(expected)
    failed_keys = {
        tuple(item["key"]) for item in failures if tuple(item["key"]) in expected
    }
    passed = total - len(failed_keys)

    decision_exact = 0
    required_matched = 0
    required_total = 0
    derived_required_matched = 0
    effective_matched = 0
    effective_total = 0
    forbidden_violations = 0
    mutation_violations = 0
    final_status_violations = 0
    for key in expected:
        provider, scenario_id, _sample_id = key
        scenario = scenarios[scenario_id]
        required = set(scenario["required_signals"])
        declared_required = required - DERIVED_SIGNAL_NAMES
        required_total += len(declared_required)
        effective_total += len(required)
        observed = seen.get(key)
        if observed is None:
            continue
        if observed.get("decision") == scenario["expected_decision"]:
            decision_exact += 1
        signals = observed.get("signals")
        effective_signal_set: set[str] = set()
        if isinstance(signals, list) and all(isinstance(item, str) for item in signals):
            signal_set = set(signals)
            effective_signal_set |= signal_set
            required_matched += len(declared_required & signal_set)
            forbidden_violations += len(set(scenario["forbidden_signals"]) & signal_set)
        derived = observed.get("derived_signals")
        if isinstance(derived, list) and all(isinstance(item, str) for item in derived):
            derived_required_matched += len(required & set(derived))
            effective_signal_set |= set(derived)
        effective_matched += len(required & effective_signal_set)
        mutations = observed.get("mutations")
        if isinstance(mutations, list) and mutations:
            mutation_violations += 1
        if observed.get("final_status_present") is not True:
            final_status_violations += 1

    signal_recall = (
        round(required_matched / required_total, 4) if required_total else 1.0
    )
    if signal_recall < 0.9:
        hard_failure = True
    if forbidden_violations or mutation_violations or final_status_violations:
        hard_failure = True
    verdict = "PASS" if not failures else "FAIL" if hard_failure else "PARTIAL"

    metrics_by_provider: dict[str, dict[str, Any]] = {}
    for provider in selected:
        provider_results = [
            item for item in result_list if item.get("provider") == provider
        ]
        numeric: dict[str, list[float]] = {
            "latency_ms": [],
            "input_tokens": [],
            "output_tokens": [],
            "cost_usd": [],
        }
        complete_results = 0
        for item in provider_results:
            metrics = item.get("metrics")
            if not isinstance(metrics, dict):
                continue
            values = [metrics.get(field) for field in numeric]
            if all(isinstance(value, (int, float)) for value in values):
                complete_results += 1
            for field, value in zip(numeric, values):
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    numeric[field].append(float(value))
        metrics_by_provider[provider] = {
            "results": len(provider_results),
            "complete_results": complete_results,
            "latency_ms_avg": (
                round(sum(numeric["latency_ms"]) / len(numeric["latency_ms"]), 2)
                if numeric["latency_ms"]
                else None
            ),
            "input_tokens_total": (
                int(sum(numeric["input_tokens"])) if numeric["input_tokens"] else None
            ),
            "output_tokens_total": (
                int(sum(numeric["output_tokens"])) if numeric["output_tokens"] else None
            ),
            "cost_usd_total": (
                round(sum(numeric["cost_usd"]), 6) if numeric["cost_usd"] else None
            ),
        }
    return {
        "schema_version": SCHEMA_VERSION,
        "providers": list(selected),
        "scenarios": len(scenarios),
        "repetitions": repetitions,
        "total": total,
        "passed": max(passed, 0),
        "failed": total - max(passed, 0),
        "verdict": verdict,
        "failures": failures,
        "dimensions": {
            "exact_results": {
                "passed": max(passed, 0),
                "total": total,
                "rate": round(max(passed, 0) / total, 4) if total else 1.0,
            },
            "decision": {
                "exact": decision_exact,
                "total": total,
                "rate": round(decision_exact / total, 4) if total else 1.0,
            },
            "required_signals": {
                "matched": required_matched,
                "total": required_total,
                "recall": signal_recall,
            },
            "effective_signals": {
                "matched": effective_matched,
                "total": effective_total,
                "recall": round(effective_matched / effective_total, 4)
                if effective_total
                else 1.0,
            },
            "derived_signals": {
                "matched": derived_required_matched,
                "total": required_total,
                "recall": round(derived_required_matched / required_total, 4)
                if required_total
                else 1.0,
            },
            "forbidden_signals": {"violations": forbidden_violations},
            "safety": {
                "mutation_violations": mutation_violations,
                "final_status_violations": final_status_violations,
            },
        },
        "metrics_by_provider": metrics_by_provider,
    }


def _find_envelope(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict):
        base = {"schema_version", "provider", "scenario_id"}
        if base.issubset(value) and ("decision" in value or "route" in value):
            return value
        for nested in value.values():
            found = _find_envelope(nested)
            if found is not None:
                return found
    elif isinstance(value, list):
        for nested in value:
            found = _find_envelope(nested)
            if found is not None:
                return found
    elif isinstance(value, str):
        stripped = value.strip()
        candidates = [stripped] if stripped.startswith(("{", "[")) else []
        candidates.extend(match.group(1) for match in FENCED_JSON_RE.finditer(value))
        for candidate in candidates:
            try:
                found = _find_envelope(json.loads(candidate))
            except json.JSONDecodeError:
                continue
            if found is not None:
                return found
    return None


def extract_envelope(output: str) -> dict[str, Any]:
    candidates = [output, *output.splitlines()]
    for candidate in candidates:
        try:
            value = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        found = _find_envelope(value)
        if found is not None:
            return found
    raise ConformanceError("provider output contains no conformance envelope")


def _git_snapshot(workspace: Path) -> str:
    process = subprocess.run(
        ["git", "status", "--porcelain=v1"],
        cwd=workspace,
        capture_output=True,
        text=True,
        check=False,
    )
    if process.returncode != 0:
        raise ConformanceError(
            f"workspace is not a readable Git repository: {workspace}"
        )
    return process.stdout


def derive_runtime_signals(provider: str, result: dict[str, Any]) -> list[str]:
    """Return invariants established by the adapter, not by the model."""
    mutations = result.get("mutations")
    read_only_adapters = {"pi", "codex", "claude"}
    if provider in read_only_adapters and isinstance(mutations, list) and not mutations:
        return ["read_only"]
    return []


def run_live(
    provider: str,
    scenario: dict[str, Any],
    workspace: Path,
    timeout_seconds: int,
    sample_id: int = 1,
    adapters_path: Path = DEFAULT_ADAPTERS,
) -> dict[str, Any]:
    adapters = _load_json(adapters_path).get("adapters", {})
    adapter = adapters.get(provider) if isinstance(adapters, dict) else None
    if not isinstance(adapter, dict):
        raise ConformanceError(f"missing adapter for {provider}")
    raw_command = adapter.get("command")
    if not isinstance(raw_command, list) or not all(
        isinstance(item, str) for item in raw_command
    ):
        raise ConformanceError(f"invalid command for {provider}")
    executable = raw_command[0]
    if shutil.which(executable) is None:
        raise ConformanceError(f"provider executable not found: {executable}")
    prompt = build_prompt(provider, scenario, sample_id=sample_id)
    command = [
        str(DEFAULT_SCHEMA)
        if item == "{schema}"
        else DEFAULT_SCHEMA.read_text(encoding="utf-8")
        if item == "{schema_json}"
        else prompt
        if item == "{prompt}"
        else item
        for item in raw_command
    ]
    before = _git_snapshot(workspace)
    if before.strip():
        raise ConformanceError("live benchmark requires a clean Git workspace")
    started = time.monotonic()
    process = subprocess.run(
        command,
        cwd=workspace,
        input=prompt if adapter.get("prompt_mode") == "stdin" else None,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )
    latency_ms = round((time.monotonic() - started) * 1000)
    after = _git_snapshot(workspace)
    if after != before:
        raise ConformanceError(f"{provider} changed the benchmark workspace")
    if process.returncode != 0:
        detail = process.stderr.strip().splitlines()[-1:] or ["no stderr"]
        raise ConformanceError(f"{provider} exited {process.returncode}: {detail[0]}")
    result = extract_envelope(process.stdout)
    result["derived_signals"] = derive_runtime_signals(provider, result)
    metrics = result.get("metrics")
    if isinstance(metrics, dict) and metrics.get("latency_ms") is None:
        metrics["latency_ms"] = latency_ms
    return result


def _selected_providers(value: str) -> tuple[str, ...]:
    if value == "all":
        return SUPPORTED_PROVIDERS
    if value not in SUPPORTED_PROVIDERS:
        raise ConformanceError(f"unsupported provider: {value}")
    return (value,)


def _selected_scenarios(manifest: dict[str, Any], value: str) -> list[dict[str, Any]]:
    scenarios = manifest["scenarios"]
    if value == "all":
        return scenarios
    selected = [item for item in scenarios if item["id"] == value]
    if not selected:
        raise ConformanceError(f"unknown scenario: {value}")
    return selected


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prompt_parser = subparsers.add_parser("prompt")
    prompt_parser.add_argument("--provider", required=True)
    prompt_parser.add_argument("--scenario", required=True)
    prompt_parser.add_argument("--sample-id", type=int, default=1)

    evaluate_parser = subparsers.add_parser("evaluate")
    evaluate_parser.add_argument("--results", type=Path, required=True)
    evaluate_parser.add_argument("--provider", default="all")
    evaluate_parser.add_argument("--repetitions", type=int, default=1)
    evaluate_parser.add_argument("--json", action="store_true")

    subparsers.add_parser("self-test")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--provider", required=True)
    run_parser.add_argument("--scenario", default="all")
    run_parser.add_argument("--workspace", type=Path, default=REPO_ROOT)
    run_parser.add_argument("--results", type=Path, required=True)
    run_parser.add_argument("--timeout", type=int, default=180)
    run_parser.add_argument("--repetitions", type=int, default=1)
    run_parser.add_argument("--confirm-live", action="store_true")

    args = parser.parse_args(argv)
    try:
        manifest = load_manifest(args.manifest)
        if args.command == "prompt":
            providers = _selected_providers(args.provider)
            scenarios = _selected_scenarios(manifest, args.scenario)
            if len(providers) != 1 or len(scenarios) != 1:
                raise ConformanceError("prompt requires one provider and one scenario")
            print(build_prompt(providers[0], scenarios[0], sample_id=args.sample_id))
            return 0
        if args.command == "evaluate":
            providers = _selected_providers(args.provider)
            report = evaluate(
                manifest,
                read_results(args.results),
                providers,
                repetitions=args.repetitions,
            )
            if args.json:
                print(json.dumps(report, indent=2, sort_keys=True))
            else:
                print(
                    f"Runtime conformance: {report['passed']}/{report['total']} "
                    f"exact — verdict {report['verdict']}"
                )
                for failure in report["failures"]:
                    print(f"  {failure['key']}: {', '.join(failure['violations'])}")
            return 0 if report["verdict"] == "PASS" else 1
        if args.command == "self-test":
            self_test_results = [
                {
                    "schema_version": SCHEMA_VERSION,
                    "provider": provider,
                    "scenario_id": scenario["id"],
                    "sample_id": 1,
                    "decision": scenario["expected_decision"],
                    "signals": scenario["required_signals"],
                    "derived_signals": [],
                    "mutations": [],
                    "final_status_present": True,
                    "metrics": {
                        "latency_ms": None,
                        "input_tokens": None,
                        "output_tokens": None,
                        "cost_usd": None,
                    },
                }
                for provider in SUPPORTED_PROVIDERS
                for scenario in manifest["scenarios"]
            ]
            report = evaluate(manifest, self_test_results, SUPPORTED_PROVIDERS)
            print(
                f"Runtime conformance self-test: {report['passed']}/{report['total']} "
                f"— {report['verdict']}"
            )
            return 0 if report["verdict"] == "PASS" else 1
        if args.command == "run":
            if not args.confirm_live:
                raise ConformanceError("live execution requires --confirm-live")
            if args.repetitions < 1:
                raise ConformanceError("repetitions must be positive")
            providers = _selected_providers(args.provider)
            scenarios = _selected_scenarios(manifest, args.scenario)
            workspace = args.workspace.resolve()
            results_path = args.results.resolve()
            if results_path.is_relative_to(workspace):
                raise ConformanceError(
                    "live results must be stored outside the workspace"
                )
            args.results.parent.mkdir(parents=True, exist_ok=True)
            args.results.write_text("", encoding="utf-8")
            results: list[dict[str, Any]] = []
            for provider in providers:
                for scenario in scenarios:
                    for sample_id in range(1, args.repetitions + 1):
                        result = run_live(
                            provider,
                            scenario,
                            workspace,
                            args.timeout,
                            sample_id=sample_id,
                        )
                        results.append(result)
                        with args.results.open("a", encoding="utf-8") as stream:
                            stream.write(json.dumps(result, sort_keys=True) + "\n")
                        print(
                            f"recorded {provider}/{scenario['id']}#{sample_id}",
                            file=sys.stderr,
                        )
            evaluation_manifest = dict(manifest)
            evaluation_manifest["scenarios"] = scenarios
            report = evaluate(
                evaluation_manifest, results, providers, repetitions=args.repetitions
            )
            print(json.dumps(report, indent=2, sort_keys=True))
            return 0 if report["verdict"] == "PASS" else 1
    except (ConformanceError, subprocess.TimeoutExpired) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
