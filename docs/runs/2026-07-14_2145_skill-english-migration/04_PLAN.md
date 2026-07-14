---
run_id: "2026-07-14_2145_skill-english-migration"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T21:50:00+02:00"
ended_at: "2026-07-14T21:51:00+02:00"
next_phase: "POC"
artifacts_consumed: ["03_DECISION.md"]
artifacts_produced: ["04_PLAN.md"]
---

# 04_PLAN — Skill English migration

## Objectif

Reach English-only active prose across all 64 skills.

## Pré-conditions

- ADR 0044 ACCEPTED.
- Five-file inventory classified.
- Integration gate PASS before skill/test edits.

## Ordered steps

1. Translate the Janitor block without changing its conditions.
2. Translate four bounded residues.
3. Extend prompt-language tests to the skill catalog.
4. Verify zero unapproved markers and exact catalog count.
5. Update durable truth, run P.R2, commit and push.

## Acceptance criteria

- 64/64 active skills pass both language checks.
- Commands, paths, IDs, routing contracts and verdict values are unchanged.
- Controlled French sentence remains rejected.
- Full P.R2 and local CI pass.

## Plan de rollback global

Restore the five skills and language tests atomically.

## Risques identifiés

- Translation drift in Janitor eligibility rules.
- Over-broad detector exceptions.

## Integration Gate

- ADR: `docs/adr/0044-agent-facing-skill-english-convention.md`
- POC: `POC.md`
- CAN_CODE_START: `true` — `INTEGRATION_GATE.md` passed before edits.
