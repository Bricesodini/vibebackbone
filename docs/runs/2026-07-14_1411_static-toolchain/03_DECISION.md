---
run_id: "2026-07-14_1411_static-toolchain"
phase: "03_DECISION"
voie: "STRUCTUREE"
status: "APPROVED"
agent: "codex"
started_at: "2026-07-14T14:11:00+02:00"
ended_at: "2026-07-14T14:12:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed:
  - "02_AUDIT.md"
artifacts_produced:
  - "03_DECISION.md"
  - "CANON_CHANGE_PROPOSAL.md"
  - "docs/adr/0035-supported-python-static-toolchain.md"
---

# 03_DECISION — Ruff + mypy

**Décision**: ACCEPTED — ADR 0035.

Ruff 0.13.1 et mypy 2.1.0 deviennent la toolchain Python statique supportée sur
Python 3.11. Pyright reste hors contrat. L'activation CI attend une baseline
entièrement verte.
