---
run_id: "2026-05-27_2154_mvp-start-implementation-plan"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-05-27T19:54:48Z"
ended_at: "2026-05-27T20:00:00Z"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/audits/mvp-start-readiness-20260527-2142.md"
  - "docs/runs/2026-05-27_2142_mvp-start-readiness-audit/03_DECISION.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — MVP Start Implementation Plan

## Demande recue

> Planifie de maniere minutieuse cette implementation en runs.

## Reformulation

Produire un plan d'implementation detaille, sequentiel et executable pour integrer le MVP Start Protocol, le readiness gate RICO, le nouveau skill `0-vbb-rico-readiness`, le routage associe et l'harmonisation documentaire.

## Scope

### Dans le perimetre

- Decoupage en runs coherents et validables.
- Dependances entre runs.
- Fichiers cibles par run.
- Validations et criteres de sortie.
- Points de rollback et risques.

### Hors perimetre

- Ecriture effective de `docs/MVP_START_PROTOCOL.md`.
- Creation effective du skill ou des contrats.
- Correction effective des compteurs.
- Execution de CI post-implementation.

### Dependances detectees

- Audit source : `docs/audits/mvp-start-readiness-20260527-2142.md`.
- Decision source : `docs/runs/2026-05-27_2142_mvp-start-readiness-audit/03_DECISION.md`.
- Trois arbitrages ouverts : route publique vs pre-route, prompt dedie vs prompt existant, traitement du drift release.

## Classification du risque

- **Niveau** : `MODERE`
- **Justification** : le plan ne modifie pas encore la gouvernance cible, mais il organise une implementation systemique qui touchera gouvernance, router, prompts, contracts et documentation publique.

## Voie recommandee

- **Voie** : `STRUCTUREE`
- **Justification** : planification multi-fichiers avant execution, sans audit supplementaire.

## Handoff vers `04_PLAN`

- **Entrees a lire pour la phase suivante** :
  - `docs/audits/mvp-start-readiness-20260527-2142.md`
  - `docs/runs/2026-05-27_2142_mvp-start-readiness-audit/03_DECISION.md`
- **Points de vigilance** :
  - Conserver des runs petits et verifiables.
  - Ne pas melanger creation du gate et harmonisation documentaire finale.
  - Prevoir une validation apres chaque changement de routeur/contrat.
