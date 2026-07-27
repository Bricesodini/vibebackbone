# INTEGRATION_GATE — Design/Certification governance audit

**Route**: AUDIT
**Purpose**: authorize audit analysis only, never implementation.

## ADR status

- **Baseline ADR**:
  `docs/adr/0043-domain-verdict-runtime-status-orthogonality.md`
- **Observed status**: `ACCEPTED`
- **Scope qualification**: ADR 0043 establishes verdict/status orthogonality;
  it does not pre-approve the proposed assurance taxonomy.

## POC status

- **POC required for this read-only governance audit**: no.
- A later implementation run may require a schema/migration POC depending on
  the option selected and the consumers found at that time.

## Automated gate

Executed:

```bash
python tools/vbb-gate-check.py \
  docs/runs/2026-07-27_2117_design-certification-gates-governance-audit --json
```

Observed result:

```yaml
adr_required: true
adr_present_and_accepted: true
poc_required: false
can_code_start: true
blockers: []
exit_intent: PASS
```

The tool's `can_code_start` field means that its ADR/POC preconditions are
satisfied. It does not override the run scope or the user's prohibition.

## Authorization boundary

- `CAN_AUDIT_START?`: YES.
- `CAN_CODE_START?`: NO. This run contains no implementation phase and the
  user explicitly prohibits governance modification.

## Decision

The gate can authorize production of audit artifacts only. A positive audit
recommendation must hand off to a distinct future governance-change run.
