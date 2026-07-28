---
run_id: "2026-07-29_0300_a2-retry-certification-of-m3-remediation"
phase: "02_AUDIT"
voie: "AUDIT"
status: "READY"
agent: "A2-retry hostile-falsifier"
kind: "A2_RETRY_AUDIT_POINTER"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
started_at: "2026-07-29T03:00:00Z"
ended_at: "2026-07-29T05:00:00Z"
next_phase: "03_DECISION"
artifacts_produced:
  - "02_AUDIT.md (this file, pointer)"
  - "02_ADVERSARIAL_CAMPAIGN.md (canonical audit content)"
---

# 02_AUDIT — Pointer

This file is a thin pointer alias for the AUDIT voie canonical
naming expected by `vbb-loop-closure-check.py`.

The actual A2 adversarial campaign content lives in:

- [`02_ADVERSARIAL_CAMPAIGN.md`](./02_ADVERSARIAL_CAMPAIGN.md) — 33
  hostile fixtures, 6 axes obligatoires, M3-01..M3-12 replay
  matrix, declared limits evaluation, propagation comparison.

The audit artifact was produced by the A2-retry campaign on
commit M3 (`c4bb4b63`). It is a **read-only falsification
exercise**, not an implementation. No code, no templates, no
canon documents were modified.

See `02_ADVERSARIAL_CAMPAIGN.md` for the full audit content and
`03_FINDINGS.md` for the discovered findings.