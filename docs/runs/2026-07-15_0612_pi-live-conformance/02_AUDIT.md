---
run_id: "2026-07-15_0612_pi-live-conformance"
phase: "02_AUDIT"
route: "STRUCTURED"
status: "READY"
agent: "codex"
started_at: "2026-07-15T06:15:00+02:00"
ended_at: "2026-07-15T06:18:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed: ["tools/vbb_runtime_conformance.py", "conformance/runtime-scenarios.json", "conformance/result-schema.json", "conformance/runtime-adapters.json", "docs/ARCHITECTURE.md", "docs/RELATIONS.md"]
artifacts_produced: ["02_AUDIT.md", "docs/audits/impact-analysis-pi-live-conformance-20260715-0618.md"]
---

# 02_AUDIT — Pi live conformance compatibility

## Change analyzed

Accept Pi's machine-readable event wrapper when its final result is fenced JSON,
and constrain runtime-reported signals to the benchmark's canonical vocabulary.

## Direct impact

- `tools/vbb_runtime_conformance.py`: prompt construction, manifest validation,
  and nested envelope extraction.
- `conformance/runtime-scenarios.json`: shared signal vocabulary declaration.
- `conformance/result-schema.json`: signal enum aligned with that vocabulary.
- `tests/test_runtime_conformance.py`: Pi-shaped event-stream regression.

## Indirect impact

All four providers consume the same prompt and extractor. Existing raw JSON,
wrapper JSON, and JSONL forms remain accepted; the new fenced form is additive.

## External impact

No installed runtime files, provider commands, credentials, or project data are
changed. Live execution remains explicit, read-only, and outside CI.

## Classification

`NON_BREAKING` — additive parser support and a stricter documented output
vocabulary inside the existing schema.

## UNKNOWN areas

Model adherence to the canonical signal vocabulary remains empirical and is the
purpose of the ten-scenario Pi live rerun.
