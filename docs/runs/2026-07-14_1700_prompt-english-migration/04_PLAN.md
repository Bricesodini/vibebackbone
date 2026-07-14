---
run_id: "2026-07-14_1700_prompt-english-migration"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T17:03:00+02:00"
ended_at: "2026-07-14T17:05:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "01_INTAKE.md"
  - "03_DECISION.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Prompt English migration

## Objectif

Reach zero unambiguous French instructional markers in active prompts without
changing their behavior or routing.

## Pré-conditions

- ADR 0036 ACCEPTED.
- 18/33 affected inventory frozen.
- Integration Gate PASS before delegation or editing.

## Étapes ordonnées

1. Correct the stale local SESSION pointer.
2. Delegate canonical and specialized translations as non-overlapping batches.
3. Review every diff and compare paths, executable inline tokens and link
   destinations; human placeholders may translate.
4. Add a conservative regression test and prove it catches a controlled marker.
5. Update ADR index, distribution log, risk truth and run evidence.
6. Run prompt inventory checks, targeted tests, full P.R2 and credentials gate.

## Critères d'acceptation

- 33 prompt files remain; the same 33 paths exist.
- No unambiguous French instructional marker remains.
- Executable inline tokens and Markdown link destinations are preserved;
  human-readable placeholders and templates are English.
- Router aliases and four surface counts remain 7/25/1/5.
- READY-GOV-001 and READY-GIT-002 are resolved on current evidence.
- Full tests and local CI pass.

## Plan de rollback global

Restore the 19 prompt files and remove the regression test; SESSION correction
is independently valid and need not be rolled back.

## Risques identifiés

- Translation changes a threshold, enum or required artifact.
- Parallel batches overlap or use inconsistent terminology.
- Language detector rejects contract tokens rather than prose.

## Analyse d'impact

Core prompt behavior is inherited by Pi, OpenCode, Codex and Claude Code. No
distribution adapter or provider runtime state changes in this repository.

## Integration Gate

- ADR: `docs/adr/0036-agent-facing-prompt-english-migration.md`
- POC: `POC.md`
- CAN_CODE_START: pending `INTEGRATION_GATE.md`.
