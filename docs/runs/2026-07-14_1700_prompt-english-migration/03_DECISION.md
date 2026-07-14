---
run_id: "2026-07-14_1700_prompt-english-migration"
phase: "03_DECISION"
voie: "STRUCTUREE"
status: "ACCEPTED"
agent: "codex"
started_at: "2026-07-14T17:02:00+02:00"
ended_at: "2026-07-14T17:03:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed:
  - "01_INTAKE.md"
  - "docs/adr/0036-agent-facing-prompt-english-migration.md"
artifacts_produced:
  - "03_DECISION.md"
---

# 03_DECISION — Apply existing English prompt convention

ADR 0036 is accepted. Translate in place, preserve all machine-facing contracts,
and add a conservative regression guard. No canon change is made.
