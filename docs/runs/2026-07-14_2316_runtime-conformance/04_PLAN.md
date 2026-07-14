---
run_id: "2026-07-14_2316_runtime-conformance"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T23:19:00+02:00"
ended_at: "2026-07-14T23:21:00+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed: ["01_INTAKE.md", "POC.md", "docs/audits/impact-analysis-runtime-conformance-20260714-2319.md"]
artifacts_produced: ["04_PLAN.md"]
---

# 04_PLAN — runtime conformance benchmark

## Objectif

Deliver a deterministic, provider-neutral conformance benchmark with an
explicit opt-in live runner for all four supported runtimes.

## Pré-conditions

- Clean synchronized `main` at run start.
- ADR 0047 accepted and POC verdict GO.
- Integration gate reports `can_code_start=true`.

## Étapes ordonnées

| # | Action | Target | Validation | Rollback |
|---|---|---|---|---|
| 1 | Define ten scenarios and result schema | `conformance/` | schema and manifest unit tests | remove new directory |
| 2 | Implement evaluator and live command harness | `tools/vbb-runtime-conformance.py` | focused unit tests | remove tool |
| 3 | Cover valid, invalid, mutation, and parity cases | `tests/test_runtime_conformance.py` | pytest | remove tests |
| 4 | Add deterministic CI invocation | CI scripts/workflows | local CI | revert CI lines |
| 5 | Update architecture and distribution impact | canonical architecture/docs | architecture lint | revert blocks/log entry |

## Definition of done

- [ ] Ten scenarios cover FAST, STRUCTURED, AUDIT, MVP START, escalation,
  mutation safety, and closeout.
- [ ] Four providers can be evaluated from the same result format.
- [ ] Live execution is opt-in and read-only by default.
- [ ] CI performs no LLM or network call.
- [ ] Full local CI passes.

## Plan de rollback global

Revert the new conformance files and remove the added CI, architecture, and
distribution-log references. No installed provider state needs rollback.

## Risques identifiés

- External CLI event schemas may drift; fail explicitly instead of guessing.
- Live calls can consume credits; require `--confirm-live` and keep them out of CI.
- Agent mutation would invalidate the benchmark; require a clean Git workspace
  and compare state before and after every call.

## Impact analysis

- Performed via `t-vbb-impact-analyzer`.
- Classification: CONDITIONAL, non-breaking for existing installations.
- Affected blocks: governance core, contract tooling, distribution setup.

## Integration gate

- Linked ADR: `docs/adr/0047-runtime-conformance-benchmark.md` — ACCEPTED.
- Linked POC: `docs/runs/2026-07-14_2316_runtime-conformance/POC.md` — GO.
- CAN_CODE_START: pending automated gate verification.
