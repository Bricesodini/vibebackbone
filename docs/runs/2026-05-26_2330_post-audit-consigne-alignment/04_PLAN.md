---
run_id: "2026-05-26_2330_post-audit-consigne-alignment"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-05-26T21:35:00Z"
ended_at: "2026-05-26T21:40:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "prompts/canonical/05-p-vbb-execution.md"
  - "prompts/1-p-vbb-structured-task.md"
  - "docs/templates/07_CLOSEOUT.md.template"
artifacts_produced:
  - "docs/runs/2026-05-26_2330_post-audit-consigne-alignment/04_PLAN.md"
---

# 04_PLAN — post-audit-consigne-alignment

## Objectif

Aligner les consignes d'exécution post-audit avec le dépôt réel, sans créer de nouvelle architecture ni ajouter le Debt Guard complet.

## Scope

### Fichiers concernés

| Fichier | Action | Description |
|---------|--------|-------------|
| `prompts/canonical/05-p-vbb-execution.md` | MODIFIER | Ajouter le pré-check anti-dette post-audit aligné sur le dépôt réel |
| `prompts/1-p-vbb-structured-task.md` | MODIFIER | Faire remonter les prérequis minimaux dans le prompt structuré intégré |
| `docs/templates/07_CLOSEOUT.md.template` | MODIFIER | Ajouter un statut dette explicite |
| `docs/CONTEXT.md` | MODIFIER | Clarifier `docs/AUDIT_STATUS.md` comme source de vérité audit et ajouter le run |
| `docs/runs/2026-05-26_2330_post-audit-consigne-alignment/*` | CREER | Tracer le run documentaire |

### Fichiers hors scope

- `skills/*/CONTRACT.yaml` — aucun contrat de skill n'est modifié.
- `skills/INDEX.yaml` — aucun skill n'est ajouté ou changé.
- `.github/workflows/vbb-contracts.yml`, `scripts/vbb-ci-local.sh`, `tools/vbb-phase-router.py`, `tools/__pycache__/` — fichiers non suivis préexistants hors scope.

## Plan d'exécution

### RUN 01 — Correction documentaire minimale

**Objectif** : corriger les consignes qui peuvent induire un agent en erreur avant implémentation.

**Étapes** :
1. Ajouter dans le prompt d'exécution canonique le pré-check post-audit.
2. Ajouter dans le prompt structuré les mêmes prérequis sous forme compacte.
3. Ajouter dans le template de closeout une section `Statut dette`.
4. Produire les artefacts de run.

**Tests** :
- Recherche ciblée des références incohérentes.
- Vérification du loop closure sur le run.

**Critère de succès** : les prompts ne suggèrent plus de `CONTRACT.yaml` racine et imposent un finding cible avant implémentation post-audit.

## Risques d'implémentation

| Risque | Sévérité | Mitigation |
|--------|----------|------------|
| Sur-corriger la gouvernance | Moyenne | Limiter le patch aux prompts et au template concernés |
| Introduire le Debt Guard complet prématurément | Moyenne | Ajouter seulement le pré-check documentaire |
| Modifier des fichiers non suivis hors scope | Basse | Les lister explicitement et les laisser intacts |

## Dépendances

- `docs/AUDIT_STATUS.md` pour l'état d'audit actuel.
- `skills/*/CONTRACT.yaml` et `skills/INDEX.yaml` pour les futurs changements de skills.

## Contraintes héritées

- Ne pas créer de `CONTRACT.yaml` racine.
- Ne pas ajouter de nouvelle architecture.
- Ne pas intégrer le Debt Guard complet.

## Handoff

**Phase suivante** : 05_EXECUTION  
**Agent recommandé** : exécuteur documentaire  
**Entrées pour 05** : ce plan + fichiers concernés  
**Points de vigilance** : vérifier les occurrences exactes après patch
