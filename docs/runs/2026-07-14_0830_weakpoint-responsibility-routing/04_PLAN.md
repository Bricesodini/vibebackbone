---
run_id: "2026-07-14_0830_weakpoint-responsibility-routing"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T08:34:00+02:00"
ended_at: "2026-07-14T08:35:00+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_AUDIT.md"
  - "POC.md"
  - "INTEGRATION_GATE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Responsibility-first routing consolidation

## Objectif

Faire passer le corpus strict de routage de 3/8 à 8/8 sans fusion, suppression,
nouveau skill ou contournement de l'orchestrateur.

## Pré-conditions

- ADR 0032 ACCEPTED.
- POC GO.
- Gate automatique `can_code_start=true`.
- Archive non suivie préexistante laissée intacte.

## Étapes ordonnées

| # | Action | Fichiers cibles | Validation | Rollback |
|---|---|---|---|---|
| 1 | Écrire mesure et matrice | `docs/WEAKPOINT_CONSOLIDATION_MEASUREMENT.md` | responsabilités distinctes | retirer le fichier |
| 2 | Ajouter triggers prouvés | 5 `CONTRACT.yaml` | corpus strict 8/8 | retirer les triggers |
| 3 | Ajouter tests | `tests/test_contract_lint.py` | pytest ciblé | retirer les tests |
| 4 | Corriger le plan obsolète | `docs/WEAKPOINT_CONSOLIDATION_PLAN.md` | statut non exécutable visible | restaurer l'en-tête |
| 5 | Vérifier Core/distributions | architecture, contracts, CI | P.R2 | revert du change set |

## Critères d'acceptation

- [ ] 8/8 cas routés vers le skill attendu en strict.
- [ ] 64/64 contrats restent indexés.
- [ ] Aucun skill ou prompt supprimé.
- [ ] P.R2 et CI locale passent.
- [ ] TER-001 et credentials restent explicitement hors scope.

## Plan de rollback global

Retirer les triggers et tests additifs ; aucun format persistant ou état externe
n'est migré.

## Risques identifiés

- Sur-ajustement : corpus borné et extension uniquement par nouveaux cas réels.
- Distribution : vérifier les quatre adaptateurs, sans modification de glue.

## Analyse d'impact

- **Effectuée ?** : OUI via `t-vbb-impact-analyzer`.
- **Périmètre** : skills-catalog, prompt-library, contract-tooling,
  distribution-adapters.
- **Effets de bord** : ambiguïtés de triggers, couvertes par strict routing.

## Integration Gate

- **ADR** : PASS — `docs/adr/0032-responsibility-first-routing-consolidation.md`
- **POC** : PASS — `POC.md` verdict GO
- [x] **CAN_CODE_START → YES**
