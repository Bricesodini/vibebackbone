---
run_id: 2026-08-03_document-model-main-integration
phase: planning
voie: STRUCTUREE
status: active
agent: codex
started_at: "2026-08-03T00:00:00Z"
ended_at: "2026-08-03T00:00:00Z"
artifacts_produced:
  - 04_PLAN.md
---

# DOCUMENT_MODEL_MAIN_INTEGRATION — Plan

1. Run the repository integration gate.
2. Cherry-pick `64bb43e`, `6beae84`, `f3035f6` and `668e3e0` in order.
3. Validate each lot and record its resulting SHA.
4. Reconstruct F-02, F-03 and F-05 as separate minimal lots only after the
   technical lots pass.
5. Run integrated validation and record divergence from `origin/main`.
6. Close without adoption, push, tag or merge.

No conceptual foundation, canonical contract, fixture contract, runtime or
publication is part of this run.

## Objectif

Porter les capacités techniques C0–C5 et les quatre skills alignées sur la
branche d’intégration, puis préparer séparément les remédiations autorisées.

## Pré-conditions

- `origin/main` vérifié à `067b8ea6e9a7d9bea65a29340bdc38da1361f039` ;
- `da494ad` descendant de cette base ;
- worktree propre avant ouverture du run ;
- Critical Rule 16 présente une seule fois ;
- gate dépôt PASS avec POC GO.

## Étapes ordonnées

1. Porter C0–C2 (`64bb43e`).
2. Valider puis porter C3–C4 (`6beae84`).
3. Valider puis porter C5 (`f3035f6`).
4. Valider puis porter les skills (`668e3e0`).
5. Reconstruire F-02, F-03 et F-05 en lots séparés si les preuves et décisions
   restent valides.
6. Exécuter les validations intégrées et clôturer sans publication.

## Critères d'acceptation

- chaque lot possède un SHA et un diff inspectés ;
- les tests ciblés et validations applicables passent ;
- aucun échec n’est inexpliqué ;
- aucun fondement conceptuel n’est promu au canon ;
- le worktree final est propre ;
- aucun push, tag ou merge n’est effectué.

## Plan de rollback global

Chaque lot est autonome et réversible par revert avant publication. En cas de
conflit ou d’échec non expliqué, arrêter au dernier SHA validé et conserver le
worktree source inchangé. Ne jamais réécrire ADR ou historique publié.

## Risques identifiés

- conflit avec une évolution de `origin/main` ;
- double représentation de Critical Rule 16 ;
- artefact de run refusé par les hooks ;
- confusion entre capacité expérimentale et adoption canonique ;
- divergence source/projection de `SYSTEM.md` ;
- contrat de convention absent ou non applicable.
