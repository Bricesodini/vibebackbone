---
run_id: "2026-07-14_1945_front-artifact-contracts"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T19:53:00+02:00"
ended_at: "2026-07-14T19:55:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "03_DECISION.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Front-pipeline artifact contracts

## Objectif

Formalize all six remaining front/release outputs without changing pipeline
execution semantics.

## Pré-conditions

- ADR 0040 ACCEPTED.
- Impact classification NON_BREAKING.
- Integration Gate PASS before contract edits.

## Ordered steps

1. Add `release_document` to the closed taxonomy.
2. Map five pass files and the primary/optional changelog paths.
3. Extend null-drift lint only to front-family normative emit/update patterns.
4. Test controlled rejection, release kind, and canonical pass order.
5. Record four-distribution propagation and PATT-03 remaining count.
6. Run P.R2, credentials gate, commit and push.

## Acceptance criteria

- Six primary contracts non-null with exact paths and truthful kinds.
- Versioned release note optional, never falsely required.
- Front normative emitter with null artifact fails controlled lint.
- Canonical 1→7 pass order remains unchanged.
- Full P.R2 and local CI pass.

## Plan de rollback global

Restore contracts, taxonomy, linter, tests and documentation atomically.

## Risques identifiés

- Expanding lint beyond the intended front family.
- Confusing release communication with design artifacts.
- Accidentally implying the visual pipeline was executed.

## Integration Gate

- ADR: `docs/adr/0040-front-pass-and-release-artifact-semantics.md`
- POC: `POC.md`
- CAN_CODE_START: `true` in `INTEGRATION_GATE.md`.
