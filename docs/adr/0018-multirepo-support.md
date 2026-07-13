---
template_id: "ADR"
version: "1.0"
lane_eligible:
  - "STRUCTUREE"
  - "AUDIT"
related:
  - "docs/adr/README.md"
  - "docs/CONVENTIONS.md#pr3--gate-before-action"
---

# ADR — 0018-multirepo-support

**Status**: ACCEPTED  
**Date**: 2026-07-13  
**Route**: STRUCTUREE  
**Décideurs**: Brice Sodini (project lead & canon owner)  
**Liée à**: docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md § Gap-08  
**Liée à POC**: vide

## Contexte

Vibebackbone est conçu pour un repo unique. Aujourd'hui, un projet qui appartient à un système multi-repo (par exemple studio-projects avec 4 services) ne peut pas exprimer cette appartenance. Chaque service est traité indépendamment par les outils (`vbb-status-dashboard`, `vbb-context-compactor`, etc.) — la vue d'ensemble est reconstruite à la main par l'humain.

Conséquence : impossible de répondre à des questions comme « quels sont les services qui dépendent de `studio-auth` ? » ou « quel est le graphe global du système studio-projects ? » directement depuis les outils. Le graphe multi-repo (Gap-13, ADR-0020) ne peut pas être généré.

## Décision

**Introduire un fichier `docs/MULTIREPO.yaml` (par projet) qui déclare l'appartenance du repo à un système multi-repo.**

### Format

```yaml
schema_version: "1.0"

system_name: <string>   # ex. "studio-projects"
description: <string>

# Repos dans le système
repos:
  - name: <repo-slug>   # ex. "studio-auth"
    path: <relative path to local clone>   # ex. "../studio-auth" (optional, for monorepo-style local dev)
    role: <auth | api | worker | orchestrator | consumer | library>
    services_provided:
      - <service-slug>   # ex. "studio-auth-api"
    remote: <git url>     # for cross-repo reference

  # ... (other repos)

# Outils qui traversent les frontières
tools:
  - <tool-name>   # ex. "vbb-multiservice-graph"
```

### Positionnement

- Le fichier est **optionnel** : un projet mono-repo peut ne pas le créer.
- Quand il existe, les outils existants le lisent pour exposer une vue d'ensemble.

### Comportement des outils

| Outil | Avec `MULTIREPO.yaml` | Sans |
|-------|------------------------|------|
| `vbb-status-dashboard` | Affiche section "system overview" | Mode mono-repo actuel |
| `vbb-context-compactor` | Inclut les autres repos si `path:` est défini et lisible | Mode mono-repo actuel |
| `vbb-multiservice-graph` (Gap-13) | Génère graphe cross-repo | Génère graphe intra-repo |
| `vbb-extension-register` (Gap-09) | List extensions de tous les repos | List extensions locales |

### Validation

Un mini-script de validation `tools/vbb-multirepo-check.py` (à créer) vérifie :
- Schema YAML conforme
- `path:` pointe vers un dossier existant (si défini)
- Pas de doublons dans `repos[*].name`

## Conséquences

### Positives
- L'appartenance multi-repo est explicite et vérifiable.
- Le graphe global (Gap-13) devient dérivable.
- Les outils peuvent traverser les frontières de manière transparente.

### Négatives / coûts
- Chaque projet multi-repo doit maintenir `MULTIREPO.yaml`.
- Les outils doivent apprendre à lire ce fichier (extension optionnelle, rétrocompatible).

### Neutres
- Aucun canon direct modifié.
- Le format YAML est cohérent avec `MULTISERVICE_DISCIPLINE.yaml` (ADR-0009).

## Alternatives rejetées (≥ 2)

### Alternative A — Documenter l'appartenance dans `CONTEXT.md` (prose)
- **Description** : ajouter une section « System membership » dans `CONTEXT.md`.
- **Pourquoi rejetée** : non structuré, non dérivable. Le graphe ne peut pas être généré.

### Alternative B — Regrouper tous les services dans un monorepo
- **Description** : forcer l'usage d'un monorepo avec plusieurs dossiers `services/`.
- **Pourquoi rejetée** : ne correspond pas à la réalité (certains projets ont des repos distincts pour des raisons administratives, organisationnelles, de release).

### Alternative C — Créer un repo "meta" qui indexe les autres
- **Description** : un repo central qui contient des pointeurs vers tous les autres.
- **Pourquoi rejetée** : ajoute un niveau d'indirection. Chaque service doit rester autonome.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| `MULTIREPO.yaml` pas maintenu (drift) | moyenne | moyen | `vbb-status-dashboard` peut signaler un warning si `Last updated` trop ancien |
| `path:` pointe vers un dossier supprimé | faible | faible | `vbb-multirepo-check` valide |
| Confusion entre `repos` et `services` | moyenne | faible | Le format est strict : 1 repo = 1 dépôt git ; 1 service = 1 unité fonctionnelle (peut être plusieurs services par repo) |

## Hypothèses

- Le format YAML est accepté (cohérent avec `MULTISERVICE_DISCIPLINE.yaml`).
- Les projets multi-repo sont minoritaires aujourd'hui (la majorité sont mono-repo).

## Références

- ADR lié (consommateur) : [`0020-multiservice-graph.md`](0020-multiservice-graph.md)
- Audits : [`docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md`](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) § Gap-08
- POCs : vide

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: ARCHITECTURE
reversible: true
depends_on:
  - vide
blocks:
  - "tools/vbb-multirepo-check.py (implémentation, Run 13+)"
  - "0020-multiservice-graph.md (utilise MULTIREPO.yaml)"
supersedes:
  - vide
verified_at: "2026-07-13T00:00:00Z"
verified_by: "human"
verified_method: "human-review"
```