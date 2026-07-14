---
run_id: "2026-07-14_1402_ready-contract"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T14:04:00+02:00"
ended_at: "2026-07-14T14:05:00+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — READY contract

## Objectif

Transformer le souhait READY en contrat de sortie vérifiable, sans clore les
dettes techniques par simple reclassification.

## Pré-conditions

- Plan de convergence approuvé par Brice.
- État initial PARTIAL conservé.

## Étapes ordonnées

1. Ajouter les sept critères READY dans le registre actif.
2. Déplacer SYS-POST-002 vers les risques acceptés historiques.
3. Confirmer QA-007 résolu par le CCP du run ADR 0034.
4. Relier le plan de convergence et pointer CONTEXT vers GMA-003.
5. Exécuter P.R2 et fermer le run sans basculer READY.

## Critères d'acceptation

- Chaque retrait de la table active possède une preuve et une condition de
  réouverture.
- Aucun autre finding n'est modifié.
- Dashboard reste PARTIAL.

## Plan de rollback global

Rétablir les deux lignes dans la table active et retirer la section de campagne.

## Risques identifiés

- Confondre acceptation historique et résolution.
- Faire passer READY avant les remédiations techniques.

## Analyse d'impact

- Governance Core seulement ; quatre distributions héritent de la lecture.
- Aucun impact API, outil, test ou runtime.

## Integration Gate

- Aucun code : ADR/POC/Integration Gate produit non requis pour ce run docs-only.
