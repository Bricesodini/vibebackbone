---
run_id: "2026-07-13_1637_restore-pr2-baseline"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-13T16:40:00+02:00"
ended_at: "2026-07-13T16:42:00+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Restore P.R2 baseline

1. Passer le gate pré-exécution.
2. Adapter les tests à `lint_all() -> (count, errors, warnings)` sans modifier le linter.
3. Régénérer `docs/RELATIONS.md` depuis `docs/ARCHITECTURE.md`.
4. Exécuter le test ciblé, puis les cinq vérifications P.R2.
5. Produire execution, closeout et commit atomique ciblé.

## Acceptance

- `pytest tests/test_contract_lint.py -q` : PASS.
- `pytest tests/ -q` et CI locale : PASS.
- Aucun fichier utilisateur préexistant n'est staged.
