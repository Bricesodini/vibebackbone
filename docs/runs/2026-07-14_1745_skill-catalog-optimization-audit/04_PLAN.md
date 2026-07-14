---
run_id: "2026-07-14_1745_skill-catalog-optimization-audit"
phase: "04_PLAN"
voie: "AUDIT"
status: "READY"
agent: "codex-controller"
started_at: "2026-07-14T17:47:00+02:00"
ended_at: "2026-07-14T17:50:00+02:00"
next_phase: "02_AUDIT"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Skill catalog optimization audit

## Objectif

Produce an exhaustive, evidence-based catalog review and a final independent
READY verdict without changing the reviewed surfaces.

## Pré-conditions

- Exactly 64 skills and 64 contracts available.
- Worktree clean and local/tracking/live remote SHAs equal before scaffolding.
- ADR 0026 accepted and Integration Gate PASS before delegation.

## Étapes ordonnées

1. Delegate from a fresh context with a strict read-only brief.
2. Measure every skill: lines, words, description size, sections, references,
   contract alignment and repeated boilerplate.
3. Score all 64 skills on routing, scope, articulation, efficiency and loop fit.
4. Analyze cross-catalog variants and minority patterns.
5. Prioritize only optimizations supported by evidence and estimate effort.
6. Revalidate all seven READY criteria separately.
7. Write one audit report and no catalog edits.

## Critères d'acceptation

- One inventory row for each of exactly 64 skills.
- Every score has evidence or a clearly stated heuristic.
- P0/P1/P2 findings distinguish defects from optional optimization.
- Roadmap is ordered by ROI and avoids mass rewrites by line count alone.
- Seven READY criteria each receive PASS/FAIL/UNKNOWN evidence.
- Reviewer writes only `02_AUDIT_REPORT.md`.

## Plan de rollback global

Delete uncommitted scaffolding only if delegation cannot start. Preserve any
completed independent report, including a negative verdict.

## Risques identifiés

- Superficial scoring rewards short files rather than effective instructions.
- Repeated required boilerplate is mistaken for waste.
- Catalog-wide recommendations ignore phase or mode differences.
- The desired READY outcome biases the reviewer.

## Analyse d'impact

Read-only Core audit. Findings may later affect all four distributions, but this
run changes no shared or provider-specific behavior.

## Integration Gate

- ADR: `docs/adr/0026-global-maintainability-audit-before-remediation.md`
- POC: `POC.md`
- CAN_CODE_START: pending `INTEGRATION_GATE.md`.
