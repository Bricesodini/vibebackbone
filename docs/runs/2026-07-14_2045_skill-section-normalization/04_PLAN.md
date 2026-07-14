---
run_id: "2026-07-14_2045_skill-section-normalization"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T20:54:00+02:00"
ended_at: "2026-07-14T20:56:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "03_DECISION.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Skill section normalization

## Objectif

Reach 64/64 exact mandatory section coverage with minimal semantic change.

## Pré-conditions

- ADR 0042 ACCEPTED.
- Impact classification NON_BREAKING.
- Integration Gate PASS before edits.

## Ordered steps

1. Split/rename equivalent headings in five skills.
2. Add concise missing sections to seven wrappers.
3. Declare the exact seven headings in the standard.
4. Add catalog-wide blocking lint and controlled negative test.
5. Verify 64/64, P.R2, commit and push.

## Acceptance criteria

- 64/64 skills contain all seven exact headings.
- No command, output path, routing trigger or verdict value changes.
- Compact wrappers remain concise and non-duplicative.
- Missing-heading fixture fails lint.
- Full P.R2 and local CI pass.

## Plan de rollback global

Restore the twelve skills, standard, lint and tests atomically.

## Risques identifiés

- Accidentally dropping prose while splitting combined sections.
- Inflating wrappers.
- Enforcing heading order when only presence is canonical.

## Integration Gate

- ADR: `docs/adr/0042-exact-seven-section-skill-layout.md`
- POC: `POC.md`
- CAN_CODE_START: `true` — `INTEGRATION_GATE.md` passed before edits.
