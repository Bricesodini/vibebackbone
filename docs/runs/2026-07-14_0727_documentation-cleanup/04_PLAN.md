---
run_id: "2026-07-14_0727_documentation-cleanup"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T07:28:00+02:00"
ended_at: "2026-07-14T07:28:00+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Documentation cleanup

## Objectif

Make the current repository state quick to read and mechanically navigable,
while retaining historical evidence at its existing paths.

## Pré-conditions

- Gate check allows execution without ADR or POC.
- Historical runs, audits, plans, ADRs, and activity logs remain immutable.
- The cleanup is limited to Markdown and introduces no new canon rule.

## Steps

1. Classify Markdown surfaces and measure active local-link failures.
2. Replace the mixed historical dashboard with one current risk register and
   evidence pointers.
3. Remove manual catalog counts from the navigation index and repair confirmed
   active links.
4. Write the required documentation-context report and distribution-impact
   decision.
5. Run link checks and the complete P.R2 closeout sequence.

## Acceptance criteria

- `docs/AUDIT_STATUS.md` contains one unambiguous active-risk table.
- Current measurements are generated or linked, not manually copied.
- No actionable local link is broken on the edited active surfaces.
- No historical evidence is moved, deleted, or rewritten.
- Markdown-only product diff; no new operational abstraction.

## Rollback

Restore the edited active Markdown files if compression drops an open finding
or makes navigation less precise. Run artifacts and the audit report remain as
the factual record of the attempt.

## Risques identifiés

- Dropping a still-open finding during compression: compare the generated
  dashboard before and after the edit.
- Treating template placeholders as broken links: exclude virtual paths from
  the actionable link set.
- Inflating skill contracts while fixing references: make link-only edits.

## ADR / POC

Not required: no new rule, interface, runtime behavior, or implementation
hypothesis.
