---
run_id: "2026-07-15_1100_real-pocs"
phase: "01_INTAKE"
voie: "AUDIT"
status: "READY"
agent: "codex"
started_at: "2026-07-15T11:00:00+02:00"
ended_at: "2026-07-15T11:00:00+02:00"
next_phase: "02_AUDIT"
artifacts_consumed:
  - "docs/runs/2026-07-15_1015_hypothesis-poc/02_AUDIT_REPORT.md"
artifacts_produced:
  - "01_INTAKE.md"
  - "ADR.md"
  - "POC.md"
---

# 01_INTAKE — real-pocs

## Demande reçue

> go pour les pocs suivants

## Reformulation

Exécuter les trois POC réels restants : H-003 (validateurs d'autorité),
H-005/H-006 (contre-audit ciblé et findings secondaires) et H-007 (contamination
filesystem), sans modifier le cœur avant décision.

## Scope

### Dans le périmètre
- Fixtures temporaires Next.js, Docker et API.
- Quatre findings existants du dépôt pour le contre-audit.
- Corpus de chemins/contenus historiques du dépôt et de son historique git.

### Hors périmètre
- Modification de `skills/`, `tools/`, prompts ou distributions.
- Suppression ou déplacement de fichiers détectés.
- Installation de dépendances réseau.

## Classification du risque

- **Niveau** : `MODÉRÉ`
- **Justification** : les tests valident des règles de gouvernance et lancent
  une fixture HTTP locale, sans données sensibles ni changement canonique.

## Voie recommandée

- **Voie** : `AUDIT`
- **Justification** : contre-validation systémique et lecture seule.

## Handoff vers `02_AUDIT`

- **Entrées** : run précédente, `docs/PILOTAGE.md`, `docs/AUDIT_STATUS.md`.
- **Vigilance** : distinguer absence d'outil dans l'environnement et invalidité
  de l'hypothèse ; aucun faux GO ne doit être déduit d'une fixture synthétique.
