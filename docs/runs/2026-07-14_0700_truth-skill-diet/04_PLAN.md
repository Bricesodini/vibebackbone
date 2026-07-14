---
run_id: "2026-07-14_0700_truth-skill-diet"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T07:01:00+02:00"
ended_at: "2026-07-14T07:01:00+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "docs/audits/intent-decomp-20260714-0007.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Active truth and skill diet

## Objectif

Remove stale active-state claims, repair live references and reduce the five
largest skill bodies by at least 15% while preserving all executable behavior.

## Pré-conditions

- RUN 01 executor correction is committed and pushed.
- Character baselines are recorded in `01_INTAKE.md`.
- No uncommitted change exists at run start.

## Steps

1. Replace stale CONTEXT/SESSION state instead of appending history.
2. Reconcile AUDIT_STATUS and TECH_DEBT with closed/open findings.
3. Correct live Rule #11/#12 references and canonical local links.
4. Compress each hotspot by removing duplicated motivation, examples and
   repeated protocol prose; keep blocking conditions, process order, outputs,
   verdicts, triggers and support boundaries.
5. Measure each file and the aggregate before running validation.

## Files

- `docs/CONTEXT.md`, local `docs/SESSION.md`, `docs/AUDIT_STATUS.md`,
  `docs/TECH_DEBT.md`.
- `README.md`, `GUIDE.md`, `docs/DISTRIBUTIONS.md`, `distributions/README.md`
  and the active broken-link surfaces confirmed by the audit.
- Five hotspot `SKILL.md` files listed in `01_INTAKE.md` source plan.

## Critères d'acceptation

- Aggregate and individual character caps pass.
- Mandatory skill sections and semantic output keys remain present.
- Contract lint has 0 error / 0 warning.
- Active boot/canonical links in scope resolve.
- Full tests and P.R2 pass.

## Plan de rollback global

Restore only the five skills and active docs from the run-start commit if any
mandatory behavior, link or gate validation regresses. No schema or external
state migration is involved.

## Risques identifiés

- Over-compression may remove a blocking rule: mitigate with section/key checks.
- State cleanup may erase historical evidence: edit active summaries only;
  preserve versioned runs/audits.
- Rule-number fixes may miss a live surface: use a scoped repository search.

## ADR

- **Liée à ADR** : `docs/adr/0030-boot-set-diet-and-portability.md`
