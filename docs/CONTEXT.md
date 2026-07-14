---
context_role: moc-central
phase: transverse
status: active
run_id: permanent
updated: 2026-07-14
temporal_provenance: TEMPORAL_PROVENANCE.md
---

# CONTEXT — persistent router

> Read first at startup. This file points to current truth; it does not retain
> session history or duplicate measured counters.

## Identity

- **Project**: Vibebackbone Core and its Pi, OpenCode, Codex, and Claude Code distributions
- **Mode**: [DISTRIBUTION](PROJECT_MODE.md#mode)
- **Governance**: [AGENTS.md](../AGENTS.md) · [SYSTEM.md](../SYSTEM.md) · [PILOTAGE.md](PILOTAGE.md)
- **MVP start**: new/from-zero products must pass [MVP_START_PROTOCOL.md](MVP_START_PROTOCOL.md)

## Active state

- **Route**: STRUCTURED
- **Release posture**: v1.0 hardening complete; bounded maintenance continues
- **Active run**: none
- **Latest completed run**:
  [`2026-07-14_1745_skill-catalog-optimization-audit`](runs/2026-07-14_1745_skill-catalog-optimization-audit/07_CLOSEOUT.md)
- **Audit truth and open blockers**: [AUDIT_STATUS.md](AUDIT_STATUS.md)
- **Measured health**: run `python tools/vbb-status-dashboard.py`; do not copy
  test, contract, prompt, or runtime counters into this router
- **Next action**: after human checkpoint, remediate PATT-02 phase semantics,
  then PATT-04 routing precedence as the next bounded sequence
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md) is canonical;
  [RELATIONS.md](RELATIONS.md) is generated
- **Quality**: [CONVENTIONS.md](CONVENTIONS.md), pillars P1–P5 and P.R1–P.R8

## Current priorities

1. Revalidate the seven READY exit criteria from a fresh, read-only context.
2. Preserve the accepted-risk owners and reopen triggers in `AUDIT_STATUS.md`.
3. Keep `main`, `origin/main`, CI and active governance truth aligned.

## Stable decisions

- UI/UX requests enter the ENGINE_ONLY pipeline through propagation mapping:
  [ADR-0002](adr/0002-surface-first-routing-ui-ux.md) and
  [ADR-0003](adr/0003-graphic-propagation-map.md).
- Structural Core changes require four-distribution impact review; see
  [DISTRIBUTIONS.md](DISTRIBUTIONS.md).
- Architecture changes update `ARCHITECTURE.md`; regenerate `RELATIONS.md`.
- Historical runs and audits are evidence, not active session state.

## Navigation

| Need | Source |
|---|---|
| Route and escalation | [PILOTAGE.md](PILOTAGE.md) |
| Current local handoff | `docs/SESSION.md` (gitignored) |
| Audit findings | [AUDIT_STATUS.md](AUDIT_STATUS.md) |
| Technical debt | [TECH_DEBT.md](TECH_DEBT.md) |
| Architecture | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Documentation index | [INDEX.md](INDEX.md) |
| Runs and closeouts | `docs/runs/*/07_CLOSEOUT.md` |
