---
run_id: "2026-07-13_1656_retire-hermes"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-13T16:56:00+02:00"
ended_at: "2026-07-13T16:58:00+02:00"
next_phase: "02_AUDIT"
artifacts_consumed:
  - "docs/CONTEXT.md"
  - "docs/PILOTAGE.md"
  - "docs/PROJECT_MODE.md"
  - "docs/SESSION.md"
  - "docs/AUDIT_STATUS.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — Retire Hermes and focus supported runtimes

## Demande reçue

> « orienter Vibebackbone comme framework pour Pi, OpenCode, Codex et Claude
> Code uniquement ; retirer Hermes et aligner la documentation »

## Reformulation

Retirer la distribution Hermes/Cody du dépôt et repositionner la promesse du
framework sur quatre adaptateurs officiels : Pi, OpenCode, Codex et Claude Code.

## Scope

### Dans le périmètre

- Suppression de `distributions/hermes/` et des tests exclusivement Hermes.
- Retrait d'Hermes du routeur `setup.sh`.
- Neutralisation des règles Core qui dépendaient du vocabulaire Cody.
- Alignement des documents actifs, architecture, tests, hooks et changelog.

### Hors périmètre

- Toute suppression ou modification sous `~/.hermes/`.
- Réécriture des runs, audits et décisions historiques.
- Promotion du proxy ou du bypass-lint Hermes dans Core.
- Implémentation des ADR multi-services.

## Classification du risque

- **Niveau** : `ÉLEVÉ`
- **Justification** : suppression d'une distribution, rupture CLI et modification du canon.

## Voie recommandée

- **Voie** : `STRUCTUREE`
- **Justification** : architecture et installation multi-fichiers, sans migration de données ni production.

## Handoff vers `02_AUDIT`

- Lire ADR 0013, architecture, installateur, catalogues et références actives.
- Préserver strictement les modifications utilisateur préexistantes.
