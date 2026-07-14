---
run_id: "2026-07-14_0714_dashboard-risk-priority"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T07:14:00+02:00"
ended_at: "2026-07-14T07:15:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/AUDIT_STATUS.md"
  - "docs/CONTEXT.md"
artifacts_produced:
  - "01_INTAKE.md"
  - "04_PLAN.md"
---

# 01_INTAKE — Dashboard risk priority

## Request

After explicit GO, make the status dashboard reliably surface active P1 risks
before lower-severity items.

## Evidence

Current JSON lists QOA-005/006/007/009 and GMA-005, while active P1 rows
TER-001 and SYS-POST-002 are absent. The parser is limited to one heading,
does not normalize Markdown emphasis, and display truncation preserves document
order instead of severity.

## Scope

- Modify `tools/vbb-status-dashboard.py` and its direct tests only.
- Update active status/context and the Core↔Distribution decision log if needed.
- No new module, dependency, schema, skill, or historical rewrite.

## Route

`STRUCTUREE` — the change affects shared status behavior across the four
supported distributions.

## Gate classification

No architecture decision or technical hypothesis is introduced. The patch
repairs parsing of the existing Markdown tables and preserves the JSON shape.
