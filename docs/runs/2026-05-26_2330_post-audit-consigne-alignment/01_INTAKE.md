---
run_id: "2026-05-26_2330_post-audit-consigne-alignment"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-05-26T21:30:00Z"
ended_at: "2026-05-26T21:35:00Z"
next_phase: "04_PLAN"
artifacts_consumed:
  - "AGENTS.md"
  - "SYSTEM.md"
  - "docs/CONTEXT.md"
  - "docs/SESSION.md"
  - "docs/PROJECT_MODE.md"
  - "docs/AUDIT_STATUS.md"
  - "skills/vibebackbone/docs/PILOTAGE.md"
artifacts_produced:
  - "docs/runs/2026-05-26_2330_post-audit-consigne-alignment/01_INTAKE.md"
---

# 01_INTAKE — post-audit-consigne-alignment

## Demande reçue

Corriger la consigne d'implémentation post-audit pour l'aligner avec l'état réel du dépôt avant toute intégration d'un garde-fou anti-dette complet.

## Reformulation

Rembourser la dette documentaire détectée : empêcher les futures consignes d'implémentation de demander un `CONTRACT.yaml` racine inexistant, de référencer des closeouts sous un mauvais nom, ou de lancer une implémentation post-audit sans finding cible et sans scope check du worktree.

## Scope

### Dans le périmètre

- Prompts canoniques ou spécialisés qui encadrent l'exécution structurée.
- Template de closeout pour tracer explicitement le statut dette.
- Artefacts de run nécessaires à la clôture.

### Hors périmètre

- Création d'un `CONTRACT.yaml` racine.
- Intégration d'un Debt Guard complet.
- Nouvelle architecture de prompts ou de skills.
- Modification des fichiers non suivis préexistants.

### Dépendances détectées

- `docs/AUDIT_STATUS.md` est la source de vérité de l'état d'audit actuel.
- Les contrats réels vivent sous `skills/*/CONTRACT.yaml` et sont indexés par `skills/INDEX.yaml`.
- Les closeouts réels sont nommés `07_CLOSEOUT.md`.

## Classification du risque

**Niveau** : MODERE

**Justification** : la tâche modifie des prompts de pilotage et un template canonique, sans toucher au runtime ni aux contrats.

## Voie recommandée

**Voie** : STRUCTUREE

**Justification** : changement documentaire multi-fichiers affectant le comportement futur des agents.

## Handoff

**Phase suivante** : 04_PLAN  
**Agent recommandé** : agent d'implémentation documentaire  
**Entrées pour la phase suivante** : ce fichier, prompts ciblés, template de closeout  
**Points de vigilance** : rester minimal, ne pas ajouter le garde-fou complet
