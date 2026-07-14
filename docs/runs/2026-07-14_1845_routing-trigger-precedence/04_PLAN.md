---
run_id: "2026-07-14_1845_routing-trigger-precedence"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T18:53:00+02:00"
ended_at: "2026-07-14T18:55:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "03_DECISION.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Routing trigger precedence

## Objectif

Remove all six exact collisions while preserving explicit access to every
responsibility and preventing recurrence.

## Preconditions

- ADR 0038 ACCEPTED.
- Impact classification NON_BREAKING.
- Integration Gate PASS before contract edits.

## Ordered steps

1. Replace duplicates only on the six secondary-owner surfaces.
2. Add a case-insensitive catalog-wide duplicate-trigger lint check.
3. Add a controlled duplicate fixture and strict responsibility corpus.
4. Record Core propagation and close PATT-04.
5. Run P.R2, credentials gate, commit and push.

## Acceptance criteria

- Zero exact case-insensitive duplicate triggers across 64 contracts.
- Each of the six generic queries routes to its declared owner in strict mode.
- Each qualified secondary query routes to its adjacent skill in strict mode.
- A controlled duplicate contract set fails lint.
- Full P.R2 and local CI pass.

## Plan de rollback global

Restore the six triggers, linter, tests and documentation as one atomic change.

## Risques identifiés

- Substring overlap between generic and qualified triggers.
- A qualified query accumulating unrelated generic matches.
- Lint depending on iteration order.

## Impact analysis

NON_BREAKING Core contract invariant inherited by all four distributions.

## Integration Gate

- ADR: `docs/adr/0038-unique-generic-routing-trigger-ownership.md`
- POC: `POC.md`
- CAN_CODE_START: `true` in `INTEGRATION_GATE.md`.
