---
run_id: "2026-07-15_0612_pi-live-conformance"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-15T06:12:49+02:00"
ended_at: "2026-07-15T06:15:00+02:00"
next_phase: "02_AUDIT"
artifacts_consumed: ["docs/CONTEXT.md", "docs/PILOTAGE.md", "docs/PROJECT_MODE.md", "docs/AUDIT_STATUS.md", "docs/adr/0047-runtime-conformance-benchmark.md"]
artifacts_produced: ["01_INTAKE.md"]
---

# 01_INTAKE — Pi live conformance compatibility

## Request

Run the ten-scenario live runtime conformance benchmark for Pi.

## Reproduced target

The first live scenario produced an envelope, then the run stopped on the
second scenario because Pi returned the envelope as fenced JSON inside its
JSON event stream. Pi also emitted descriptive signal prose while the evaluator
expects stable canonical signal identifiers.

## Scope

- Make envelope extraction accept fenced JSON nested in provider event streams.
- Publish the finite canonical signal vocabulary in the provider-neutral prompt.
- Add focused regression coverage and rerun all ten Pi scenarios read-only.
- Preserve the result schema and all four adapter command contracts.

## Risk and route

- Risk: MODERATE. This is a shared runtime protocol compatibility fix.
- Route: STRUCTURED because the parser and prompt contract are shared by all
  four distributions.

## Gate linkage

- ADR: `docs/adr/0047-runtime-conformance-benchmark.md`
- POC: `docs/runs/2026-07-15_0612_pi-live-conformance/POC.md`
