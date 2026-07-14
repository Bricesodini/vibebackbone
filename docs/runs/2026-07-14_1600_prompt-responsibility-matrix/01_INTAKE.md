---
run_id: "2026-07-14_1600_prompt-responsibility-matrix"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T15:55:00+02:00"
ended_at: "2026-07-14T15:57:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/audits/doc-context-20260714-1545.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — Prompt responsibility matrix

## Demande et triage

Fermer DOC-001 avec une matrice compacte couvrant prompts canoniques,
spécialisés, router et noms courts, sans dupliquer la matrice de décision
détaillée. Route STRUCTURED : documentation de responsabilité transversale.

## Acceptance

- Une source unique d'ownership/precedence dans `PROMPTS_ARCHITECTURE.md`.
- `ROUTER_MATRIX.md` renvoie à cette source.
- 7 canoniques, 25 spécialisés, 1 router et 5 alias vérifiés.
- Aucun prompt ou comportement installé modifié.

**Liée à ADR**: aucune — clarification d'une architecture existante
**POC requis**: `docs/runs/2026-07-14_1600_prompt-responsibility-matrix/POC.md`
