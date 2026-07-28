# INTEGRATION_GATE — Adversarial loop governance design

**Run**: `docs/runs/2026-07-28_1002_adversarial-loop-governance-design/`
**Date**: 2026-07-28
**Voie**: AUDIT
**Purpose**: authorize analysis and proposal artifacts only, never
implementation and never a normative change.

## ADR status

- **Baseline ADR**: `docs/adr/0050-design-certification-assurance-schema.md`
- **Observed status**: `ACCEPTED`
- **Scope qualification**: ADR 0050 establishes the Design/Certification gate
  families and the fail-closed authorization record. It does **not**
  pre-approve a third assurance dimension. A new ADR is *proposed* by this run
  (`CANON_CHANGE_PROPOSAL.md`) and deliberately not written into `docs/adr/`.

## POC status

- **POC required**: no. This run introduces no unvalidated technical
  hypothesis; it produces documentary analysis and a proposal.
- A future implementation run will require a schema-compatibility POC covering
  the additive `1.1` assurance fields and the corpus execution surface.

## Automated gate

Executed from the repository root:

```bash
python tools/vbb-gate-check.py \
  docs/runs/2026-07-28_1002_adversarial-loop-governance-design --json
```

Observed result:

```yaml
intake_present: true
adr_required: true
adr_present_and_accepted: true
adr_path: docs/adr/0050-design-certification-assurance-schema.md
poc_required: false
can_code_start: true
blockers: []
mode_transition: NOT_NEEDED
exit_intent: PASS
exit_code: 0
```

`can_code_start: true` reports only that the tool's ADR/POC preconditions are
satisfied. It does not widen this run's scope and does not override the user
constraint C1 (no normative change) or C6 (no commit without authorization).

## Authorization boundary

| Question | Answer | Basis |
|---|---|---|
| `CAN_AUDIT_START?` | YES | AUDIT route, gate exit 0, read-only scope |
| `CAN_CODE_START?` | NO | No implementation phase in this run; user constraint C1 |
| `CAN_CANON_CHANGE?` | NO | Requires a separate governed run with ADR, human decision and independent review |

## Decision

The gate authorizes production of the audit, decision, design, migration,
review and closeout artifacts inside this run directory only. A positive
recommendation hands off to a distinct future governance-change run; nothing in
this run may be read as canonical.
