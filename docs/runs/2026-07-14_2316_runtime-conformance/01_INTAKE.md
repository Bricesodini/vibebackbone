---
run_id: "2026-07-14_2316_runtime-conformance"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T23:16:17+02:00"
ended_at: "2026-07-14T23:19:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed: ["docs/CONTEXT.md", "docs/PILOTAGE.md", "docs/PROJECT_MODE.md", "docs/AUDIT_STATUS.md"]
artifacts_produced: ["01_INTAKE.md"]
---

# 01_INTAKE — runtime conformance benchmark

## Request

Build the multi-runtime conformance test proposed after the objective evaluation
of Vibebackbone.

## Scope

- One Core protocol shared by Pi, OpenCode, Codex, and Claude Code.
- Ten routing, escalation, safety, and closeout scenarios.
- Deterministic evaluation plus optional live LLM execution.
- CI, architecture, distribution-impact log, tests, and operator documentation.

## Exclusions

- No automatic paid LLM calls in CI.
- No provider credential changes.
- No write-enabled live agent execution.
- No product-project migration in this run.

## Risk and route

- Risk: MODERATE. The change adds a shared runtime protocol and CI surface but
  does not change existing provider installation behavior.
- Route: STRUCTURED because the framework runtime contract and all four
  distributions are affected.

## Gate linkage

- Linked ADR: `docs/adr/0047-runtime-conformance-benchmark.md`
- Linked POC: `docs/runs/2026-07-14_2316_runtime-conformance/POC.md`
