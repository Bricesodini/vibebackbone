---
run_id: "2026-07-27_1712_engineering-knowledge-core-integration"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-27T15:16:00Z"
ended_at: "2026-07-27T15:20:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "docs/adr/0049-engineering-knowledge-governance.md"
  - "POC.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Engineering knowledge Core integration

## Objectif

Integrate the accepted engineering-knowledge governance into Core without a
phase 08, a new specialized skill or historical-run regression.

## Pré-conditions

ADR 0049 must be accepted, the integration gate must authorize execution and
the bounded POC must be `GO`.

```bash
python tools/vbb-gate-check.py \
  docs/runs/2026-07-27_1712_engineering-knowledge-core-integration --json
rg -n "^\\- \\*\\*Verdict\\*\\*: GO$" \
  docs/runs/2026-07-27_1712_engineering-knowledge-core-integration/POC.md
```

Both commands must permit execution.

## Étapes ordonnées

Execution is split into two planned implementation runs followed by an
independent review; any blocking review finding requires a bounded remediation
run before closeout.

### Run 01 — Canon and behavior

1. Add `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md` as the single lifecycle
   authority and `docs/templates/KNOWLEDGE_RECORD.md.template` as a
   non-authoritative dossier.
2. Add the governing-capitalization principle to Core foundations.
3. Update PILOTAGE, agentic protocol, conventions, closeout template and
   prompts 02/03/06/07.
4. Extend the existing `vibebackbone` router and contract; do not create a new
   skill.
5. Update architecture, guide, index, README and distribution decision log.

Validation: documentary consistency, contract lint and architecture lint.

### Run 02 — Enforcement and regression tests

1. Extend loop closure with a cutover-aware Knowledge Harvest check.
2. Preserve all pre-cutover runs.
3. Add positive/negative tests for dispositions and historical compatibility.
4. Regenerate `docs/RELATIONS.md`.
5. Run targeted tests and full P.R2.

Validation: targeted pytest, full pytest, local CI and four-distribution smoke.

## Critères d'acceptation

- [ ] Principle visible in Core foundations.
- [ ] Four maturity states and transition evidence are canonical.
- [ ] Independent knowledge review precedes human promotion.
- [ ] Independence is assessed in the claimed scope.
- [ ] Final authority is unique; playbook/run/review/closeout/record are not.
- [ ] Canonical knowledge changes only through governed supersession.
- [ ] Seven phases and historical runs remain valid.
- [ ] Post-cutover closeouts require a valid harvest disposition.
- [ ] Pi/OpenCode/Codex/Claude inherit the same Core rule.
- [ ] Independent integration review and P.R2 pass.

## Plan de rollback global

Revert authority, behavioral surfaces, enforcement, tests and generated
relations atomically. Never retain enforcement without the governing authority.

## Risques identifiés

- A version marker used as an opt-in could permit post-cutover omission.
- Historical enforcement could invalidate already closed runs.
- Duplicating authority into records, runs or playbooks could create parallel
  truth.
- Distribution-specific copies could drift from the Core contract.

Each risk is covered respectively by objective-cutover tests, historical
fixtures, authority-boundary review and four-distribution smoke verification.

## Impact analysis

- **Performed**: YES,
  `docs/audits/impact-analysis-engineering-knowledge-governance-20260727-1612.md`.
- **Classification**: CONDITIONAL, conditions now satisfied by GO POC,
  Review Run 02 and final human approval.

## Handoff

Execute Run 01 only, write `05_PATCH_SUMMARY_RUN_01.md`, then Run 02 and
`05_PATCH_SUMMARY_RUN_02.md`. Review occurs in a distinct session.
