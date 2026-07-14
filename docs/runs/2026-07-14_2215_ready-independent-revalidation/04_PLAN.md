---
run_id: "2026-07-14_2215_ready-independent-revalidation"
phase: "04_PLAN"
voie: "AUDIT"
status: "READY"
agent: "codex-controller"
started_at: "2026-07-14T22:16:00+02:00"
ended_at: "2026-07-14T22:17:00+02:00"
next_phase: "02_AUDIT"
artifacts_consumed: ["01_INTAKE.md"]
artifacts_produced: ["04_PLAN.md"]
---

# 04_PLAN — Independent READY revalidation

## Objectif

Obtain a reproducible, contradiction-seeking verdict on all seven READY
criteria from an independent subagent.

## Pré-conditions

- Audit-readiness POC is GO.
- Worktree clean and `main == origin/main` before delegation.
- Integration Gate PASS before delegation.

## Ordered steps

1. Delegate in fresh context without a target verdict.
2. Require evidence for each READY criterion.
3. Require P.R2/local CI and exact-SHA GitHub CI checks.
4. Permit writing only `02_AUDIT_REPORT.md`.
5. Reconcile the report without rewriting its conclusion.

## Acceptance criteria

- Seven criteria evaluated separately with commands or durable evidence.
- Active truth contradictions and undecided risks explicitly searched.
- Reviewer changes only its assigned report.
- READY only if all seven criteria hold simultaneously.

## Plan de rollback global

Do not rollback a negative audit verdict. Remove the uncommitted scaffold only
if delegation cannot start.

## Risques identifiés

- Reviewer bias from prior closeouts.
- Treating historical counters as current evidence.
- Exact-SHA remote CI still running at audit time.

## Integration Gate

- ADR: N/A — read-only evaluation.
- POC: `POC.md`.
- CAN_CODE_START: `true` — `INTEGRATION_GATE.md` passed before delegation.
