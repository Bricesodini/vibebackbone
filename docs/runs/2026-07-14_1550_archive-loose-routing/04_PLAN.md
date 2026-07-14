---
run_id: "2026-07-14_1550_archive-loose-routing"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T15:47:00+02:00"
ended_at: "2026-07-14T15:49:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Archive loose routing evidence

## Objectif

Reclasser une note historique en archive sans changer un seul octet de contenu.

## Pré-conditions

- Rapport Doc Harmonizer READY.
- Source présente, destination absente.
- Validation humaine `Go` et hash source capturé.
- Integration Gate PASS avant déplacement.

## Étapes ordonnées

1. Déplacer le fichier vers `docs/archive/runs/2026-05-28-...`.
2. Comparer SHA-256 et diff Git de rename.
3. Vérifier les fichiers loose sous `docs/runs/`.
4. Mettre à jour uniquement les vérités actives (status/context/index si utile).
5. Exécuter liens Markdown, P.R2 et credentials gate.

## Critères d'acceptation

- Hash `d67c0460...110d8fd` identique à destination.
- Git détecte un rename, contenu inchangé.
- Aucun audit historique réécrit.
- QOA-006 absent des risques actifs.

## Plan de rollback global

Renvoyer le fichier à son chemin d'origine ; contenu immuable.

## Risques identifiés

- Casser un lien opérationnel actif.
- Réinterpréter à tort le statut historique PENDING.

## Analyse d'impact

Audit Memory uniquement. Aucun Core structurel, prompt, skill, distribution ou
runtime n'est modifié.

## Integration Gate

- ADR: N/A (aucun changement de décision/canon)
- POC: `POC.md`
- CAN_CODE_START: en attente de `INTEGRATION_GATE.md`.
