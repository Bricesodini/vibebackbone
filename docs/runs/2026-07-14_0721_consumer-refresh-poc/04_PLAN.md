---
run_id: "2026-07-14_0721_consumer-refresh-poc"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T07:22:00+02:00"
ended_at: "2026-07-14T07:22:00+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Consumer refresh POC

## Objectif

Determine whether `vbb-project-init.py` can safely refresh an initialized,
customized consumer with its current options.

## Pré-conditions

- RUN 01 and RUN 02 corrections are complete.
- POC runs only in a temporary directory.

## Steps

1. Initialize a fresh consumer.
2. Add sentinels to project-owned governance and a domain file.
3. Run overwrite dry-run and default idempotent mode.
4. Run `--overwrite --backup` twice.
5. Compare live and backup sentinel survival; emit GO/NO-GO/PIVOT.
6. Implement nothing if any hard stop is reached.

## Files

- Temporary directory only for the experiment.
- Durable run/status/distribution records in this repository.
- `tools/vbb-project-init.py` only if the POC is GO and the patch stays ≤60
  product lines; otherwise unchanged.

## Critères d'acceptation

- GO only if custom project truth remains live and repeat backups preserve it.
- Domain files remain untouched.
- Dry-run predicts the performed action.
- Second safe refresh is idempotent.

## Plan de rollback global

Delete the temporary consumer after evidence capture. No repository code is
modified unless the POC is GO.

## Risques identifiés

- Overwrite may replace project truth despite creating a backup.
- Repeated backup may replace the only copy of custom content.

## ADR

- **Liée à ADR**: `docs/adr/0012-codegen-agents-claudemd.md`
