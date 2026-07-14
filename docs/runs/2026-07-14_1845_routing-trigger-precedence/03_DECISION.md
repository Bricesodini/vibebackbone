---
run_id: "2026-07-14_1845_routing-trigger-precedence"
phase: "03_DECISION"
voie: "STRUCTUREE"
status: "APPROVED"
agent: "codex"
started_at: "2026-07-14T18:51:00+02:00"
ended_at: "2026-07-14T18:53:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed:
  - "02_AUDIT.md"
artifacts_produced:
  - "03_DECISION.md"
  - "../../adr/0038-unique-generic-routing-trigger-ownership.md"
---

# 03_DECISION — Routing trigger precedence

ADR 0038 is accepted: exact triggers have one owner; adjacent skills use
qualified phrases; the catalog linter prevents recurrence.
