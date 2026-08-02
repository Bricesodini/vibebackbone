---
run_id: "2026-08-03_document-model-canon-adoption"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-08-03T00:40:00+02:00"
ended_at: null
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "POC.md"
artifacts_produced:
  - "04_PLAN.md"
---
# 04_PLAN — document-model-canon-adoption

## Objectif

Adopter localement le Documentary Contract v1.0 et six autorités uniques,
avec traçabilité et validation complète, sans publication.

## Pré-conditions

- Branche `codex/document-model-main-integration` propre avant le run.
- `origin/main` vérifié à `067b8ea6e9a7d9bea65a29340bdc38da1361f039`.
- POC `5/5` conclu `GO`.
- Sources candidates et décisions humaines disponibles comme preuves.

## Étapes ordonnées

1. Ajouter les six autorités et la matrice de traçabilité.
2. Créer l'ADR d'adoption sans réutiliser un numéro.
3. Déclarer le contrat du dépôt et exposer les autorités.
4. Régénérer les relations et exécuter les validations.
5. Obtenir la revue A2 et fermer le run avec décision d'adoption en attente.

## Critères d'acceptation

- [ ] Six localisations canoniques uniques et traçables.
- [ ] ADR d'adoption accepté localement, sans modification d'ADR existant.
- [ ] Contrat déclaré sans qualification automatique des artefacts.
- [ ] Validations applicables passées ou limitations explicitement déclarées.
- [ ] Runtime Pi `NOT_ASSESSED`; aucun push, merge ou tag.

## Plan de rollback global

Chaque lot est annulable par revert de son commit local. Les sources historiques
et les runs de conception ne sont ni déplacés ni supprimés.

## Risques identifiés

- Une autorité historique pourrait être présentée comme canon : matrice et
  références explicites, arrêt si duplication.
- Le contrat pourrait être interprété comme conformité globale : scope borné,
  artefacts sans qualification maintenus `UNKNOWN`.
- Le runtime Pi pourrait être confondu avec l'état publié : certification
  explicitement exclue.

## Autorisation

```yaml
implementation_authorization:
  status: "AUTHORIZED"
  required_gate_ids: ["DMA-POC-01"]
  reasons: ["Le POC 5/5 est GO; la décision humaine d'adoption reste requise avant publication."]
```

## Ordre atomique

| # | Lot | Sortie | Rollback |
|---|---|---|---|
| 1 | Fondations | six autorités canoniques + matrice | revert du commit |
| 2 | Gouvernance | ADR d'adoption | revert du commit |
| 3 | Contrat | déclaration `.vbb` | revert du commit |
| 4 | Navigation | INDEX, CONTEXT, ARCHITECTURE, RELATIONS régénérée | revert du commit |
| 5 | Clôture | validations, revue A2, closeout | revert des preuves |

Chaque lot est inspecté et validé avant le suivant. Aucun lot ne publie,
merge, pousse ou crée de tag.

## Critères d'arrêt

- source canonique dupliquée ou historique promu : arrêt ;
- concept nouveau détecté : arrêt ;
- lint ou test inexpliqué : arrêt ;
- contrat ou runtime non interprétable : conserver `UNKNOWN` et arrêter toute
  prétention de conformité.

## Gate

```yaml
adr_status: "NOT_YET_CREATED"
poc_status: "GO"
can_code_start: true
```

Le gate est préalable à l'exécution; l'ADR d'adoption sera produit dans le
lot 2 et devra être validé avant le closeout.
