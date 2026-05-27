---
context_role: temporal-provenance
phase: transverse
status: active
updated: 2026-05-27
---

# TEMPORAL_PROVENANCE — vibebackbone

This workspace contains historical run and audit artifacts dated after the local
host date observed during the 2026-05-27 pilotage remediation session.

## Policy

- Do not rewrite historical `docs/runs/` or `docs/audits/` timestamps to match a
  later local checkout.
- Treat future-dated run directories as imported historical evidence from the
  repository state, not as proof that the local clock is wrong.
- Use the current local date for new remediation artifacts created in this
  workspace.
- When a status file summarizes future-dated artifacts, keep the original
  artifact dates visible and rely on this file as the provenance explanation.

## Current Known Skew

- Local remediation date: `2026-05-27`
- Future-dated historical runs present: `2026-06-10` through `2026-06-13`
- Affected zones: `docs/runs/`, historical audit reports, status summaries that
  reference those runs

## Operational Consequence

Future-dated historical artifacts are no longer treated as an unresolved pilotage
risk when this file is present. They remain visible as provenance notes in the
status dashboard.
