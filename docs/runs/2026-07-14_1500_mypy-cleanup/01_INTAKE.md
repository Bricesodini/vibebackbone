---
run_id: "2026-07-14_1500_mypy-cleanup"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T14:55:00+02:00"
ended_at: "2026-07-14T14:57:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/audits/tech-debt-mypy-baseline-20260714-1455.md"
  - "docs/adr/0035-supported-python-static-toolchain.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — Mypy cleanup

## Demande et triage

Réduire les 20 erreurs mypy restantes à zéro sans ignore, abstraction nouvelle
ou promotion CI. Route STRUCTURED : les types touchent neuf outils Core et un
dynamic-import boundary.

## Acceptance

- `mypy tools` = 0 et Ruff check/format restent verts.
- Aucun `type: ignore`, `Any` opportuniste ou exclusion de fichier.
- Dynamic loader échoue explicitement si spec/loader manque.
- Tests ciblés, dry-run, P.R2 et CI locale verts.

**Liée à ADR**: `docs/adr/0035-supported-python-static-toolchain.md`
**POC requis**: `docs/runs/2026-07-14_1500_mypy-cleanup/POC.md`
