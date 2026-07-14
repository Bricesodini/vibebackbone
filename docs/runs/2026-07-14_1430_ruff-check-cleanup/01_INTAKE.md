---
run_id: "2026-07-14_1430_ruff-check-cleanup"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T14:28:00+02:00"
ended_at: "2026-07-14T14:29:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/audits/code-janitor-ruff-check-baseline-20260714-1428.md"
  - "docs/adr/0035-supported-python-static-toolchain.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — Ruff check cleanup

## Demande et triage

Réduire la baseline Ruff canonique de 37 à zéro, sans formatage global, typage
ou changement de gate. Route STRUCTURED : 11 fichiers Python, dont outils Core.

## Acceptance

- Aucun unsafe fix.
- Appels de fixtures préservés quand leur valeur seule est inutilisée.
- Sorties texte inchangées à l'octet.
- Ruff zéro, tests ciblés/globaux et P.R2 verts.

**Liée à ADR**: `docs/adr/0035-supported-python-static-toolchain.md`
**POC requis**: `docs/runs/2026-07-14_1430_ruff-check-cleanup/POC.md`
