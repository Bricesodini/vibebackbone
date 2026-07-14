---
run_id: "2026-07-14_2145_skill-english-migration"
phase: "03_DECISION"
voie: "STRUCTUREE"
status: "ACCEPTED"
agent: "codex"
started_at: "2026-07-14T21:49:00+02:00"
ended_at: "2026-07-14T21:50:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed: ["02_AUDIT.md"]
artifacts_produced: ["03_DECISION.md", "docs/adr/0044-agent-facing-skill-english-convention.md"]
---

# 03_DECISION — Skill English migration

Adopt ADR 0044 and translate all five classified files in place. Extend the
existing prompt detector to skills rather than creating a second vocabulary.
