---
run_id: "2026-07-14_1520_static-ci-promotion"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T15:15:00+02:00"
ended_at: "2026-07-14T15:17:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/audits/ci-baseline-20260714-1515.md"
  - "docs/adr/0035-supported-python-static-toolchain.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — Static CI promotion

## Demande et triage

Promouvoir Ruff check, Ruff format et mypy dans les CI locale et GitHub après
baseline zéro. Route STRUCTURED : modification d'enforcement partagé et distant.

## Acceptance

- Versions installées via `requirements-dev.txt` dans GitHub Actions.
- Trois checks bloquants et identiques sur les deux surfaces.
- Tests de wiring + preuves contrôlées failure/recovery.
- P.R2, workflow Ubuntu/macOS et credentials gate verts.

**Liée à ADR**: `docs/adr/0035-supported-python-static-toolchain.md`
**POC requis**: `docs/runs/2026-07-14_1520_static-ci-promotion/POC.md`
