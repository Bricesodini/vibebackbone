---
run_id: "2026-07-14_2245_dashboard-ready-parser"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T22:50:00+02:00"
ended_at: "2026-07-14T22:51:00+02:00"
next_phase: "POC"
artifacts_consumed: ["03_DECISION.md"]
artifacts_produced: ["04_PLAN.md"]
---

# 04_PLAN — Dashboard READY parser

## Objectif

Make generated dashboard truth match canonical global verdicts.

## Pré-conditions

- Root cause reproduced.
- ADR 0045 ACCEPTED.
- Integration Gate PASS before tool/test edits.

## Ordered steps

1. Add a closed, ordered verdict vocabulary.
2. Parse the canonical section heading plus bounded following content.
3. Preserve a word-bounded legacy fallback.
4. Add canonical READY, same-line legacy and false-substring tests.
5. Run targeted tests, P.R2, commit/push and exact-SHA CI.

## Acceptance criteria

- Real dashboard returns `READY`.
- Canonical next-line and legacy same-line forms pass.
- Unrelated words containing status substrings do not match.
- JSON shape and CLI remain unchanged.
- Full P.R2 and local/remote CI pass.

## Plan de rollback global

Restore parser and tests atomically; do not alter `AUDIT_STATUS.md` truth.

## Risques identifiés

- False match from nearby prose.
- Legacy format regression.

## Integration Gate

- ADR: `docs/adr/0045-section-aware-dashboard-verdict-parsing.md`
- POC: `POC.md`
- CAN_CODE_START: `true` — `INTEGRATION_GATE.md` passed before edits.
