---
run_id: "2026-07-14_1600_prompt-responsibility-matrix"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T15:57:00+02:00"
ended_at: "2026-07-14T15:59:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Prompt responsibility matrix

## Objectif

Rendre l'autorité et la precedence des surfaces prompt lisibles en une table.

## Pré-conditions

- Rapport Doc Harmonizer READY.
- Inventaire 7/25/1/5 vérifié, aucun alias manquant.
- Integration Gate PASS avant modification.

## Étapes ordonnées

1. Ajouter la matrice ownership/authority/cannot-override à la source canonique.
2. Décrire la precedence depuis gouvernance vers alias résolu.
3. Ajouter un lien inverse depuis le router détaillé, sans recopier la table.
4. Vérifier inventaire, liens et absence de changement sous `prompts/`.
5. Fermer DOC-001, exécuter P.R2 et consigner l'impact distributions.

## Critères d'acceptation

- Les quatre surfaces ont chacune une responsabilité exclusive.
- Router = sélection, jamais exécution ; alias = résolution, jamais autorité.
- Spécialisé ne peut contourner phase/gate/artefact canonique.
- Aucun fichier `prompts/*.md` modifié.

## Plan de rollback global

Retirer la matrice et le lien inverse ; aucune donnée migrée.

## Risques identifiés

- Créer une seconde matrice de routage concurrente.
- Présenter les alias comme une couche comportementale.
- Confondre ordre de résolution et niveau d'autorité.

## Analyse d'impact

Documentation Core de prompt architecture, héritée par les quatre distributions.
Aucun prompt, setup adapter, nom court ou runtime provider ne change.

## Integration Gate

- ADR: N/A (clarification non normative de responsabilités existantes)
- POC: `POC.md`
- CAN_CODE_START: en attente de `INTEGRATION_GATE.md`.
