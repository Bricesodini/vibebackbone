---
run_id: "2026-07-15_1015_hypothesis-poc"
phase: "01_INTAKE"
voie: "AUDIT"
status: "READY"
agent: "codex"
started_at: "2026-07-15T10:15:00+02:00"
ended_at: "2026-07-15T10:15:00+02:00"
next_phase: "02_AUDIT"
artifacts_consumed: []
artifacts_produced:
  - "01_INTAKE.md"
  - "ADR.md"
  - "POC.md"
---

# 01_INTAKE — hypothesis-poc

## Demande reçue

> Je veux tout tester par POC et si concluant on intègre.

## Reformulation

Tester H-001 à H-010 par des POC isolés, mesurer un critère de succès explicite,
puis intégrer uniquement les hypothèses validées. Le cœur Vibe Backbone reste
intouché pendant la phase de preuve.

## Scope

### Dans le périmètre
- H-001 à H-010 de la mission contre-audit.
- Skills, prompts, templates, contrats et outils existants comme surface d'observation.
- POC read-only ou temporaires, sans changement de comportement canonique.

### Hors périmètre
- Correction immédiate du cœur.
- Suppression automatique d'artefacts filesystem.
- Déploiement ou modification des distributions Pi/Codex.

## Classification du risque

- **Niveau** : `MODÉRÉ`
- **Justification** : la campagne peut conduire à des changements de gouvernance,
  mais les POC sont isolés et aucune modification canonique n'est autorisée avant décision.

## Voie recommandée

- **Voie** : `AUDIT`
- **Justification** : validation systémique de règles de gouvernance et de qualité de preuve.

## Handoff vers `02_AUDIT`

- **Entrées à lire** : `docs/PILOTAGE.md`, `docs/AUDIT_STATUS.md`, mission jointe,
  skills/templates/prompts ciblés.
- **Points de vigilance** : ne pas confondre couverture existante et validation
  opérationnelle ; ne pas créer de nouvelle abstraction si une extension locale suffit.
