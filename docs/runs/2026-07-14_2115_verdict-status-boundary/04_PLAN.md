---
run_id: "2026-07-14_2115_verdict-status-boundary"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T21:19:00+02:00"
ended_at: "2026-07-14T21:20:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "03_DECISION.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Verdict/status boundary

## Objectif

Close PATT-05 through one explicit, enforceable Core boundary.

## Pré-conditions

- ADR 0043 ACCEPTED.
- Impact NON_BREAKING.
- Integration gate PASS before contract/tool edits.

## Ordered steps

1. Remove the six unused mapping blocks.
2. Define orthogonality in `0-vbb-standard`.
3. Reject root mapping metadata in contract lint.
4. Add positive and negative regression tests.
5. Update durable truth, run P.R2, commit and push.

## Acceptance criteria

- Repository contains no root `verdict_mapping`.
- Runtime status vocabulary remains unchanged.
- Controlled mapping fixture fails lint.
- Full P.R2 and local CI pass.

## Plan de rollback global

Restore the six blocks, standard, lint and tests atomically.

## Risques identifiés

- Hidden external consumer outside the repository.
- Accidentally changing runtime semantics instead of metadata only.

## Integration Gate

- ADR: `docs/adr/0043-domain-verdict-runtime-status-orthogonality.md`
- POC: `POC.md`
- CAN_CODE_START: `true` — `INTEGRATION_GATE.md` passed before edits.
