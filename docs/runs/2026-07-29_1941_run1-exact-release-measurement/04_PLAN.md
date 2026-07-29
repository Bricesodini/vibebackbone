---
run_id: "2026-07-29_1941_run1-exact-release-measurement"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-29T19:48:00+02:00"
ended_at: "2026-07-29T19:50:00+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_AUDIT.md"
  - "POC.md"
  - "INTEGRATION_GATE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Run 1 exact release measurement

## Objectif

Close only `RR-BK-02` and `RR-BK-03` by enforcing an explicit release
`run_id` plus expected Git SHA and by making open active risks prevent false
`READY`.

## Pré-conditions

- clean isolated clone at the declared `origin/main` SHA;
- POC verdict `GO`;
- ADR 0027 accepted, with ADR 0046 and ADR 0051 as constraints;
- integration gate reports `can_code_start=true`;
- no modification before explicit `implementation_authorization: AUTHORIZED`.

## Étapes ordonnées

1. Reproduce every authorized defect with executable POC cases.
2. Add failing unit tests for subject substitution, SHA mismatch, future
   selection, canonical risk headers and P0/P1/P2 verdict behavior.
3. Implement the smallest Core changes proven by those tests.
4. Keep local CI, workflow and P.R2 command surfaces coherent.
5. Run focused tests, full pytest, local CI and four-distribution smoke checks.
6. Run a distinct A2 campaign against the exact final tree.
7. Close and commit atomically only when every exit criterion passes.

## Critères d'acceptation

- explicit run and expected SHA agree or the release gate fails;
- missing, wrong or future-selected subjects cannot pass;
- bare ID and path form cannot resolve to different release subjects;
- the exact canonical risk-table header is parsed;
- open P0 or P1 measures `BLOCKED`;
- open P2 cannot measure `READY`;
- prose `READY` cannot override measured blockers;
- release closure failure is blocking;
- focused tests, full pytest, local CI and distribution smoke pass;
- distinct A2 review finds no subject substitution, risk masking or false
  `READY` bypass.

## Plan de rollback global

If any negative proof still yields false `READY`, any gate disagrees on the
subject, or distribution smoke regresses, do not commit. Preserve run evidence,
return `BLOCKED`, and revert only the isolated branch changes with a normal Git
revert or branch deletion; never touch the historical workspace.

## Risques identifiés

- an additive CLI option could be omitted by a release caller;
- path normalization could hide rather than reject ambiguity;
- risk parsing could become permissive enough to consume unrelated tables;
- local CI could continue to use implicit latest-run discovery;
- A2 independence may remain unavailable, which blocks atomic completion.

## Implementation authorization

```yaml
implementation_authorization:
  status: "AUTHORIZED"
  required_gate_ids:
    - "RUN1-EXACT-SUBJECT"
    - "RUN1-RISK-MEASUREMENT"
  reasons:
    - "POC verdict is GO (4/4)."
    - "Integration Gate reports can_code_start=true with no blockers."
```
