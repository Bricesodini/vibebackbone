---
run_id: "2026-07-14_1440_ruff-format"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T14:38:00+02:00"
ended_at: "2026-07-14T14:39:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/adr/0035-supported-python-static-toolchain.md"
  - "docs/audits/format-lint-20260714-1410.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — Ruff format baseline

## Demande et triage

Appliquer le formatter Ruff canonique aux 29 fichiers signalés, dans un commit
mécanique isolé. Route STRUCTURED en raison de la largeur du diff Core/tests.

## Acceptance

- `ruff format --check tools tests` = 0.
- AST Python identique avant/après pour les 29 fichiers.
- Aucun fichier hors `tools/` et `tests/` formaté.
- Ruff check, tests et P.R2 restent verts.

**Liée à ADR**: `docs/adr/0035-supported-python-static-toolchain.md`
**POC requis**: `docs/runs/2026-07-14_1440_ruff-format/POC.md`
