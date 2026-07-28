---
context_role: moc-central
phase: transverse
status: active
run_id: permanent
updated: 2026-07-28
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

- **Route**: HANDOFF after an AUDIT design run
- **Release posture**: READY; Design/Certification assurance v1 independently
  approved and integrated. The adversarial assurance dimension is `PROPOSED`
  only — no canon change.
- **Active run**:
  [`2026-07-28_1002_adversarial-loop-governance-design`](runs/2026-07-28_1002_adversarial-loop-governance-design/07_CLOSEOUT.md)
  — HANDOFF, design dossier delivered, canon change `PROPOSED`, blocked on
  `COND-01` (independent review by a distinct actor)
- **Latest completed run**:
  [`2026-07-27_2145_design-certification-gates-core-integration`](runs/2026-07-27_2145_design-certification-gates-core-integration/07_CLOSEOUT.md)
- **Audit truth and open blockers**: [AUDIT_STATUS.md](AUDIT_STATUS.md)
- **Measured health**: run `python tools/vbb-status-dashboard.py`; do not copy
  test, contract, prompt, or runtime counters into this router
- **Next action**: human decision on
  [`CANON_CHANGE_PROPOSAL.md`](runs/2026-07-28_1002_adversarial-loop-governance-design/CANON_CHANGE_PROPOSAL.md)
  after a distinct-actor independent review; separately, observe first-use
  friction in new assurance records. Any consumer adoption requires its own
  governed run.
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md) is canonical;
  [RELATIONS.md](RELATIONS.md) is generated
- **Quality**: [CONVENTIONS.md](CONVENTIONS.md), pillars P1–P5 and P.R1–P.R8

## Current priorities

1. Preserve the accepted-risk owners and reopen triggers in `AUDIT_STATUS.md`.
2. Keep `main`, `origin/main`, CI and active governance truth aligned.
3. Re-run independent READY validation after material Core changes.
4. Preserve the unique-authority and independent-review gates when the first
   engineering-knowledge candidates are processed.

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
