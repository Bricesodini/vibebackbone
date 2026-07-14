---
run_id: "2026-07-14_0714_dashboard-risk-priority"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T07:15:00+02:00"
ended_at: "2026-07-14T07:15:00+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Dashboard risk priority

## Objectif

Return every active risk table row with a stable severity-first order so the
five-line terminal view cannot hide a P1 behind earlier P2/P3 rows.

## Pré-conditions

- Worktree clean at run start.
- Current failure reproduced from the real dashboard JSON.

## Steps

1. Add a regression fixture containing French/English headers, bold cells,
   multiple sections, duplicate IDs, and mixed severities.
2. Replace section-specific parsing with header-driven table parsing.
3. Normalize display markup, deduplicate by ID, and sort P0→P3 stably.
4. Verify the real JSON contains TER-001 and SYS-POST-002 before P2/P3 entries.
5. Run direct tests, full tests, and P.R2.

## Files

- `tools/vbb-status-dashboard.py`
- `tests/test_status_dashboard.py`
- active status/context and required run/decision artifacts only

## Critères d'acceptation

- Existing JSON keys and terminal layout remain unchanged.
- Active bold and bilingual risk tables are parsed.
- P1 entries precede P2/P3 entries; duplicate IDs appear once.
- Direct tests and full CI pass.
- Product-code diff remains local; no new abstraction or dependency.

## Plan de rollback global

Restore the parser and added tests if table parsing produces false risks or
changes the public JSON shape.

## Risques identifiés

- Generic table parsing could capture unrelated tables: require recognized
  ID, severity, status, and description headers.
- Duplicate risk summaries could appear: deduplicate by ID.

## ADR

Not required: no architecture choice; this is a bounded parser correction.
