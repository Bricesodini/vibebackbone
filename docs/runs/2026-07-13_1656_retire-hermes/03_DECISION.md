---
run_id: "2026-07-13_1656_retire-hermes"
phase: "03_DECISION"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-13T17:03:00+02:00"
ended_at: "2026-07-13T17:04:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed:
  - "02_AUDIT.md"
  - "docs/adr/0025-supported-runtimes-pi-opencode-codex-claude.md"
artifacts_produced:
  - "03_DECISION.md"
---

# 03_DECISION — Supported runtimes

**Decision**: ACCEPTED.

Vibebackbone supports Pi, OpenCode, Codex and Claude Code only. Hermes-specific
assets are removed rather than deprecated in place. Generic governance already
present in Core is retained and renamed where it still uses Cody terminology.

The security proxy and bypass-lint remain classified as Hermes glue and are not
promoted to Core. Git history and historical run/audit documents preserve them.
