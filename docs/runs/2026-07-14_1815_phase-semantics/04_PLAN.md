---
run_id: "2026-07-14_1815_phase-semantics"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T18:20:00+02:00"
ended_at: "2026-07-14T18:22:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "03_DECISION.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Phase semantics

## Objectif

Make all sixteen Phase-1 skill/contract pairs conform to a documented,
backward-compatible dual namespace.

## Pré-conditions

- ADR 0037 ACCEPTED.
- Impact classification NON_BREAKING.
- Integration Gate PASS before edits.

## Étapes ordonnées

1. Change the eleven remaining `phase: 1` frontmatters to `02_AUDIT`.
2. Document lifecycle-vs-routing namespaces in the canonical map and standard.
3. Add a blocking linter invariant for every `1-vbb-*` pair.
4. Add controlled positive and negative tests plus router regression coverage.
5. Record Core propagation and close PATT-02.
6. Run P.R2, credentials gate, commit and push.

## Critères d'acceptation

- 16/16 frontmatters equal `02_AUDIT`.
- 16/16 contracts retain `phase_1` routing scope.
- Wrong frontmatter and wrong contract scope fail controlled tests.
- Existing `phase_1` router query still resolves.
- Full P.R2 and local CI pass.

## Plan de rollback global

Restore frontmatters, documentation, linter and tests as one atomic change.

## Risques identifiés

- Conflating lifecycle and router namespaces.
- Breaking existing router calls.
- Enforcing only the five previously migrated skills.

## Analyse d'impact

NON_BREAKING Core invariant inherited by all four distributions.

## Integration Gate

- ADR: `docs/adr/0037-dual-phase-namespace-semantics.md`
- POC: `POC.md`
- CAN_CODE_START: `true` in `INTEGRATION_GATE.md`.
