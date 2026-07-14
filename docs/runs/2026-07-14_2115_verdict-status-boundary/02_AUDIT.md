---
run_id: "2026-07-14_2115_verdict-status-boundary"
phase: "02_AUDIT"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T21:16:00+02:00"
ended_at: "2026-07-14T21:18:00+02:00"
next_phase: "03_DECISION"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "02_AUDIT.md"
  - "docs/audits/impact-analysis-verdict-status-boundary-20260714-2115.md"
---

# 02_AUDIT — Verdict/status boundary

Six of 64 contracts define `verdict_mapping`. No Core tool or distribution
adapter reads it. Five mappings use four values; one adds `NOT_APPLICABLE` as a
runtime target although the closed runtime taxonomy excludes that value.

The current runtime and executor compare only `outputs.statuses`. Therefore the
root mappings are dead metadata and their removal is non-breaking inside the
observable repository boundary.
