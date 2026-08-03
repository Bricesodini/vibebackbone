---
run_id: 2026-08-03_f03-governance-alignment
route: STRUCTURED
adversarial_level: A2
adversarial_governance_version: "1.2"
status: active
scope:
  - docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md
  - docs/adr/0053-a2-a3-assurance-alignment.md
  - distributions/pi/SYSTEM.md
  - SYSTEM.md
out_of_scope:
  - any modification
  - candidate documentary model
  - ADR changes
  - main integration
  - canonical adoption
---

# F03-GOVERNANCE-ALIGNMENT — Intake

## Objective

Determine whether the residual F03 finding is a real v1.2 governance drift,
a deliberate difference between ADR-0053 and the governance document, or a
false positive. This run is analytical and read-only.

## Authority and evidence boundary

- ADR-0053 is the accepted v1.2 decision.
- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` is the domain authority under review.
- `distributions/pi/SYSTEM.md` and the root `SYSTEM.md` symlink are contextual
  projections only.

