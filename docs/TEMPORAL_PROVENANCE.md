---
context_role: temporal-provenance
phase: transverse
status: active
updated: 2026-08-01
provenance_attribution: "Brice Sodini <brice07@me.com> — release-freeze run 2026-08-01_1100 → rc.2 candidate"
known_skew_resolution: "F8 stale TEMPORAL_PROVENANCE.md resolved by this update as part of v1.1.0-rc.2 candidate preparation."
---

# TEMPORAL_PROVENANCE — vibebackbone

This workspace contains historical run and audit artifacts dated after the local
host date observed during the 2026-05-27 pilotage remediation session. The
provenance file was re-anchored on 2026-08-01 during preparation of the
v1.1.0-rc.2 release candidate (see `docs/runs/2026-08-01_1200_rc2-candidate/`).

## Policy

- Do not rewrite historical `docs/runs/` or `docs/audits/` timestamps to match a
  later local checkout.
- Treat future-dated run directories as imported historical evidence from the
  repository state, not as proof that the local clock is wrong.
- Use the current local date for new remediation artifacts created in this
  workspace.
- When a status file summarizes future-dated artifacts, keep the original
  artifact dates visible and rely on this file as the provenance explanation.
- The `updated` field of this file reflects the last provenance re-anchoring
  by the release owner, not the date of any specific remediation work.

## Current Known Skew

- Local remediation date (rc.2 candidate prep): `2026-08-01`
- Historical skew window: `2026-06-10` through `2026-06-13`
- Future-dated historical runs present: `2026-06-10` through `2026-07-31`
- Affected zones: `docs/runs/`, historical audit reports, status summaries that
  reference those runs

## Operational Consequence

Future-dated historical artifacts are no longer treated as an unresolved pilotage
risk when this file is present. They remain visible as provenance notes in the
status dashboard. The provenance has been re-anchored for v1.1.0-rc.2; the
F8 finding (stale `updated` header) is `RESOLVED` at SHA of the rc.2 candidate.

## Provenance Attribution

The 2026-08-01 re-anchoring was performed by Brice Sodini as part of the
release-freeze governance cycle initiated by the REJECT_RELEASE_FREEZE
decision on `v1.1.0-rc.1`. The decision is recorded in
`docs/runs/2026-08-01_1100_release-freeze/04_DECISION_REGISTRY.md` and the
new candidate is constructed in
`docs/runs/2026-08-01_1200_rc2-candidate/`.
