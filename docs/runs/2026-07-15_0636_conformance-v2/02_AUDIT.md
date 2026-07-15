---
run_id: "2026-07-15_0636_conformance-v2"
phase: "02_AUDIT"
route: "STRUCTURED"
status: "READY"
agent: "codex"
started_at: "2026-07-15T06:37:00+02:00"
ended_at: "2026-07-15T06:38:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed: ["docs/ARCHITECTURE.md", "docs/RELATIONS.md", "conformance/runtime-scenarios.json", "conformance/result-schema.json", "tools/vbb_runtime_conformance.py"]
artifacts_produced: ["02_AUDIT.md", "docs/audits/impact-analysis-conformance-v2-20260715-0642.md"]
---

# 02_AUDIT — conformance v2 impact

## Change analyzed

Version the shared runtime conformance envelope and evaluator from v1 to v2.

## Direct impact

Manifest, JSON Schema, prompt, evaluator, live runner, focused tests, operator
documentation, architecture description, and distribution decision log.

## Indirect impact

All four provider adapters consume the prompt and must emit v2 envelopes. CI
remains deterministic and network-free.

## External impact

Existing v1 JSONL is intentionally incompatible with v2. No provider command,
credential, installation destination, or consumer project is modified.

## Classification

`BREAKING`, bounded to the benchmark result contract and explicitly versioned.

## UNKNOWN areas

Live provider adherence to v2 remains unknown until new opt-in sampling.
