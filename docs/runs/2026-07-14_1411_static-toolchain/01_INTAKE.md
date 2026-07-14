---
run_id: "2026-07-14_1411_static-toolchain"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T14:10:00+02:00"
ended_at: "2026-07-14T14:11:00+02:00"
next_phase: "02_AUDIT"
artifacts_consumed:
  - "docs/audits/intent-decomp-20260714-1355.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — Supported Python static toolchain

## Demande et triage

Converger vers READY en décidant et configurant une seule toolchain statique.
Route STRUCTURED : changement de convention Core et configuration partagée.

## Décision humaine disponible

Le plan recommande Ruff + mypy, Pyright hors contrat ; Brice a répondu `Go` à
son exécution. Cette validation est bornée à Wave 2, sans promotion CI avant
baseline zéro.

## Acceptance

- ADR 0035 et CCP approuvés.
- Versions, Python cible, périmètres et commandes reproductibles.
- Aucun ignore global ni exclusion masquant les erreurs.
- Checks encore non-gating ; P.R2 reste verte.

**Liée à ADR**: `docs/adr/0035-supported-python-static-toolchain.md`
**POC requis**: `docs/runs/2026-07-14_1411_static-toolchain/POC.md`
