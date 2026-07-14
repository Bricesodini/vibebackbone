---
run_id: "2026-07-14_2015_transverse-artifact-contracts"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T20:24:00+02:00"
ended_at: "2026-07-14T20:26:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "03_DECISION.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Transverse artifact contracts

## Objectif

Close all five remaining PATT-03 artifact gaps with truthful mandatory,
optional and generated-file semantics.

## Pré-conditions

- ADR 0041 ACCEPTED.
- Impact classification CONDITIONAL and bounded.
- Integration Gate PASS before edits.

## Ordered steps

1. Add `infrastructure_file` to the closed taxonomy.
2. Normalize anti-slop to the canonical audit directory.
3. Populate five primary contracts and justified secondaries.
4. Extend null-drift lint to bounded transverse writer patterns.
5. Add controlled optional/infrastructure/null-drift tests.
6. Close PATT-03, run P.R2, commit and push.

## Acceptance criteria

- Five primary contracts non-null.
- Git-sync remains optional.
- Docker deterministic bundle is explicitly typed.
- All catalog normative writers under enforced families are non-null.
- PATT-03 has zero remaining cases.
- Full P.R2 and local CI pass.

## Plan de rollback global

Restore the five contracts, anti-slop wording, taxonomy, lint and tests.

## Risques identifiés

- Overstating conditional Docker topology files.
- Breaking the optional Git-sync report.
- Leaving a hidden alternate anti-slop destination.

## Integration Gate

- ADR: `docs/adr/0041-transverse-artifact-and-infrastructure-file-semantics.md`
- POC: `POC.md`
- CAN_CODE_START: `true` in `INTEGRATION_GATE.md`.
