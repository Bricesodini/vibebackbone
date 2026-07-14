---
run_id: "2026-07-14_1915_phase1-artifact-contracts"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T19:24:00+02:00"
ended_at: "2026-07-14T19:26:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "03_DECISION.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Phase-1 artifact contracts

## Objectif

Make all eight normative Phase-1 authored outputs truthful and enforceable in
their formal contracts.

## Preconditions

- ADR 0039 ACCEPTED.
- Impact classification NON_BREAKING.
- Integration Gate PASS before contract edits.

## Ordered steps

1. Add `design_document` to the closed linter kind set.
2. Populate the exact eight primary artifact mappings.
3. Add `AUDIT_STATUS.md` secondaries to the seven audit/report skills.
4. Add narrow authored-output null-drift lint and controlled tests.
5. Record Core propagation and update PATT-03 remaining count.
6. Run P.R2, credentials gate, commit and push.

## Acceptance criteria

- Eight target contracts have non-null exact primary paths.
- Seven audit/report contracts declare the required persistent update.
- API design uses `design_document`, without a false status update.
- A controlled normative writer with `artifact: null` fails lint.
- A controlled `design_document` mapping passes lint.
- Full P.R2 and local CI pass.

## Plan de rollback global

Restore the eight contracts, taxonomy, linter, tests and documentation as one
atomic change.

## Risques identifiés

- Misclassifying a design document as an audit or phase artifact.
- Treating conditional supplemental documentation as mandatory.
- Broad prose detection creating false positives.

## Impact analysis

NON_BREAKING Core contract alignment inherited by all four distributions.

## Integration Gate

- ADR: `docs/adr/0039-design-document-artifact-kind-and-authored-output-alignment.md`
- POC: `POC.md`
- CAN_CODE_START: `true` in `INTEGRATION_GATE.md`.
