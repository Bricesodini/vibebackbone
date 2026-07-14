---
run_id: "2026-07-14_0700_truth-skill-diet"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T07:00:11+02:00"
ended_at: "2026-07-14T07:01:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/audits/intent-decomp-20260714-0007.md"
  - "docs/adr/0030-boot-set-diet-and-portability.md"
  - "docs/AUDIT_STATUS.md"
artifacts_produced:
  - "01_INTAKE.md"
  - "04_PLAN.md"
---

# 01_INTAKE — Active truth and skill diet

## Request

Execute RUN 02 of the approved minimal remediation plan: reconcile active
project state and compress the five largest skill bodies without adding a new
governance layer.

## Scope

### Included

- Active CONTEXT/AUDIT_STATUS/TECH_DEBT/SESSION reconciliation.
- Active Core↔Distribution rule references and broken canonical links.
- Behavior-preserving compression of five identified `SKILL.md` hotspots.
- Character-budget measurement and distribution impact record.

### Excluded

- Consumer refresh, new generator, new linter, new skill or new reference doc.
- Rewriting historical runs/audits/ADRs.
- Ruff/mypy baseline work and code refactoring.

## Baselines and limits

- All skill bodies: 362,069 characters maximum after the run.
- Five hotspots: 73,766 → 62,700 characters maximum.
- Each touched skill: 13,000 characters maximum and no individual growth.
- Active Markdown outside run artifacts: net-negative character diff.

## Gate linkage

- **Liée à ADR** : `docs/adr/0030-boot-set-diet-and-portability.md`
- No POC required: this is content-preserving reduction and state
  reconciliation with measurable acceptance criteria.

## Route

`STRUCTUREE` — shared Core skills and governance surfaces are affected.
