---
run_id: "2026-07-27_1612_engineering-knowledge-governance"
phase: "03_DECISION"
voie: "AUDIT"
status: "READY"
agent: "codex"
started_at: "2026-07-27T14:25:00Z"
ended_at: "2026-07-27T14:31:00Z"
next_phase: "04_PLAN"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_AUDIT.md"
  - "CANON_CHANGE_PROPOSAL.md"
  - "POC.md"
  - "docs/audits/impact-analysis-engineering-knowledge-governance-20260727-1612.md"
artifacts_produced:
  - "03_DECISION.md"
---

# 03_DECISION — Engineering knowledge governance

## Question à trancher

Quelle architecture de gouvernance permet de capitaliser les apprentissages
sans casser les sept phases ni créer une seconde autorité ?

## Options envisagées

### Option A — Phase 08 Capitalization

- **Description** : prolonger chaque run par une huitième phase.
- **Coût / effort** : élevé ; contrats, outils, prompts et historique affectés.
- **Risques** : closeout n'est plus final, migration cassante.
- **Réversibilité** : difficile.

### Option B — Knowledge Harvest + run de connaissance séparé

- **Description** : le closeout dispose l'apprentissage ; une observation
  retenue ouvre un run utilisant les phases existantes.
- **Coût / effort** : modéré et additif.
- **Risques** : friction si le harvest est trop lourd.
- **Réversibilité** : moyenne.

### Option C — Capitalisation libre dans les runs et guides

- **Description** : laisser chaque projet documenter ses apprentissages.
- **Coût / effort** : faible.
- **Risques** : promotion implicite, portée non démontrée, vérité parallèle.
- **Réversibilité** : facile.

## Critères d'arbitrage

- Unicité de l'autorité — critique.
- Compatibilité avec les sept phases — critique.
- Indépendance audit/revue/décision — critique.
- Universalité technologique — forte.
- Friction proportionnée — moyenne.

## Verdict

- **Décision recommandée** : Option B.
- **Statut** : `GO`, after independent Review Run 02 and explicit human
  approval on 2026-07-27.
- **Conditions de validité** :
  - revue indépendante de la proposition ;
  - décision humaine finale ;
  - ADR 0049 accepté ;
  - enforcement rétrocompatible ;
  - revue Core → quatre distributions.

## Justification

L'option B est la seule qui transforme l'apprentissage en boucle gouvernée sans
faire du closeout une base normative et sans modifier la machine d'état. Elle
permet d'appliquer les mêmes séparations de rôles à la connaissance.

## Conséquences attendues

- **Court terme** : proposition canonique complète et gate bloqué.
- **Moyen terme** : intégration Core en runs bornés après validation.
- **Hypothèses à valider** : friction réelle et besoin éventuel d'un skill
  spécialisé après usage.

## Handoff vers `04_PLAN`

- **À planifier** : intégration documentaire, comportementale, outillée et
  distribuée.
- **À surveiller** : aucun fichier canonique ne doit être modifié avant décision
  humaine finale.
