---
run_id: "2026-07-14_0727_documentation-cleanup"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T07:27:00+02:00"
ended_at: "2026-07-14T07:28:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/CONTEXT.md"
  - "docs/PILOTAGE.md"
  - "docs/PROJECT_MODE.md"
  - "docs/SESSION.md"
  - "docs/AUDIT_STATUS.md"
artifacts_produced:
  - "01_INTAKE.md"
  - "04_PLAN.md"
---

# 01_INTAKE — Documentation cleanup

## Request

Clean the repository documentation after the recent refinement work, without
adding weight.

## Evidence

The active audit dashboard is 36 KB and mixes current state, resolved history,
old measurements, and repeated audit summaries. The navigation index also
contains manual catalog counts. Historical runs and audit reports remain useful
evidence and must stay immutable.

## Scope

- Compact active documentation truth and remove stale manual measurements.
- Repair actionable local links on active Markdown surfaces.
- Produce one documentation-context audit report.
- Preserve historical runs, audits, plans, ADRs, and activity logs unchanged.
- No code, configuration, dependency, skill, template, move, or deletion.

## Route

`STRUCTUREE` — active Core documentation is consumed across Pi, OpenCode,
Codex, and Claude Code.

## Gate classification

No architecture choice or technical hypothesis is introduced. This run
compresses existing declarations and references existing evidence.
