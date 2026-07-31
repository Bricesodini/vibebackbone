---
run_id: "2026-07-31_1630_rr-bk-04-release-identity-remediation"
phase: "04_PLAN"
voie: "AUDIT"
route: "AUDIT"
status: "READY"
agent: "codex/gpt-5"
started_at: "2026-07-31T15:47:46+02:00"
ended_at: "2026-07-31T15:47:46+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "03_DECISION.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — RR-BK-04 candidate verification

**CANDIDATE_SHA**: `58e51eeebfd057a359eb78393ce16d6df4a05cf3`

1. Clone the repository with `--no-local`, detach exactly at the candidate SHA,
   and copy only the run evidence carrier into the disposable clone.
2. Run architecture, contract, closure, adversarial, corpus, pytest and local
   CI gates with explicit run/SHA binding.
3. Verify package/changelog/checklist coherence and emit the machine-readable
   identity table.
4. Keep `T` and `P` uncreated; issue only the preparation verdict.

No source or release mutation is authorized beyond the candidate metadata
commit already created.

## Objectif

Prove that `R=(V,S,C,T,P)` is non-circular and that RR-BK-06 is rebound to
`58e51eeebfd057a359eb78393ce16d6df4a05cf3` before independent revalidation.

## Pré-conditions

- technical subject commit exists at the exact candidate SHA;
- no tag `v1.1.0-rc.1` is created;
- run evidence carrier is copied into, but does not mutate, the clean clone.

## Étapes ordonnées

1. Verify exact checkout and release metadata.
2. Run all blocking gates with explicit subject binding.
3. Record raw outputs and update the closeout.
4. Hand off RR-BK-06 without executing independent revalidation.

## Critères d'acceptation

- every preparation document contains the full candidate SHA;
- package, changelog and checklist agree on `V`;
- all blocking local gates pass on the exact subject SHA;
- `T` and `P` are defined but uncreated.

## Plan de rollback global

No rollback is required or authorized. If a mismatch is found, stop and mark
the run `REVISE` or `BLOCKED`; do not retarget the candidate, tag or history.

## Risques identifiés

- a document may accidentally become self-referential if it is included in the
  technical subject commit;
- a clean-clone gate may evaluate the evidence carrier rather than `S`;
- the future tag may be mistaken for an existing release.
