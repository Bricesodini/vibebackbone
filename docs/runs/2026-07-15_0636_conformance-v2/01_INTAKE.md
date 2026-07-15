---
run_id: "2026-07-15_0636_conformance-v2"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-15T06:36:04+02:00"
ended_at: "2026-07-15T06:37:00+02:00"
next_phase: "02_AUDIT"
artifacts_consumed: ["docs/PILOTAGE.md", "docs/PROJECT_MODE.md", "docs/AUDIT_STATUS.md", "docs/audits/runtime-conformance-pi-20260715-0619.md"]
artifacts_produced: ["01_INTAKE.md"]
---

# 01_INTAKE — runtime conformance benchmark v2

## Request

Correct the benchmark after the first Pi live baseline and its systemic study.

## Concrete targets

- Replace the ambiguous flat route with route family, MVP pre-gate, and closeout mode.
- Supply the complete output vocabulary to every provider.
- Detect forbidden/contradictory signals.
- Report exact decision, signal recall, contradictions, and safety separately.
- Add explicit repetitions without changing the one-call default.

## Scope and route

The shared result protocol, evaluator, tests, documentation, and four runtime
consumers are affected. Route: STRUCTURED. No provider setup, credential, or
installed runtime state changes.

## Gate linkage

- ADR: `docs/adr/0048-runtime-conformance-decision-model-v2.md`
- POC: `docs/runs/2026-07-15_0636_conformance-v2/POC.md`
