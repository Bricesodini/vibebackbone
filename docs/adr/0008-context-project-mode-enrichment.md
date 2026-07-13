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

# ADR — 0008-context-project-mode-enrichment

**Status**: ACCEPTED  
**Date**: 2026-07-12  
**Route**: STRUCTUREE  
**Décideurs**: Brice Sodini (project lead & canon owner)  
**Liée à**: docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md § Gap-14  
**Liée à POC**: vide

## Contexte

Le bootstrap d'un projet Vibebackbone (via `tools/vbb-project-init.py`) produit des fichiers `CONTEXT.md`, `PROJECT_MODE.md`, et `ARCHITECTURE.md` **minimaux** :

- `_context_md` (lignes 88-110) génère ~18 lignes, dont une section « Stack principale » en prose libre.
- `_project_mode_md` (lignes 67-86) génère une section mode (DEV/PROD/STAGING) sans schéma structuré.
- `_architecture_md` (lignes 112-140) génère un seul bloc `project-core` avec 3 champs.

Aucun des trois fichiers ne contient de sections structurées pour `db_orientation` (Gap-01), `project_archetype` (Gap-02), `scope` explicite, `contracts_expected`, `non_goals`. La qualité de l'intent projet dépend donc entièrement de la discipline individuelle de l'architecte.

Le constat est documenté dans `01_GAP_ANALYSIS.md` § Gap-14. Le gap est classé P1 : sur un système à 1 service, c'est contournable par prose. À l'échelle (N services), cela devient bloquant parce que les outils ne peuvent pas dériver de règles cohérentes.

## Décision

**Le contenu généré par `tools/vbb-project-init.py` sera enrichi pour produire un `CONTEXT.md` et un `PROJECT_MODE.md` structurés selon un schéma minimum, validé par lint à terme.**

### Sections structurées obligatoires dans `docs/CONTEXT.md` après bootstrap

```yaml
# Schema versionné — toute modification = révision de ADR-0008

## Project
- name: <string, required>
- slug: <string, required>     # ex. "studio-auth"
- description: <string, 1-3 phrases>

## DB Orientation
- value: <owned_private | shared_external_owned | shared_external_readonly | polyglot | stateless>
- rationale: <string, required>

## Project Archetype
- value: <frontend_app | api_service | orchestrator | read_only_consumer | worker | library>
- rationale: <string, required>

## Scope
- in_scope: <list of strings, required>
- out_of_scope: <list of strings, required>   # non-goals explicites

## Contracts Expected
- contracts_provided: <list of contract names>
- contracts_consumed: <list of references to docs/CONTRACTS_CONSUMED.md>

## Stack
- primary_language: <string>
- framework: <string>
- infrastructure: <string>

## Stakeholders
- owner: <team or person>
- consumers: <list of stakeholders>
```

### Sections structurées obligatoires dans `docs/PROJECT_MODE.md` après bootstrap

```yaml
# Schema versionné — toute modification = révision de ADR-0008

## Mode
- value: <DEV | STAGING | PROD>
- rationale: <string>

## Toolchain
- vbb_version: <semver>
- python_version: <semver>
- shell_runner: <bash | zsh>

## Local-only conventions
- secrets: <storage_location>
- local_state: <gitignored paths>
```

### Lint associé (implémentation future)

- `vbb-context-lint.py` (futur) valide la conformité à ce schéma.
- Les valeurs d'enum doivent correspondre à celles définies dans ADR-0005 et ADR-0006.

## Conséquences

### Positives
- L'intent projet est cohérent entre tous les bootstraps Vibebackbone.
- Les outils peuvent dériver des règles structurées (lint, templates, gates).
- La migration depuis un `CONTEXT.md` minimal vers la version enrichie est triviale.
- Cohérence avec ADR-0005/0006 — le schéma est le même pour les trois (DB Orientation, Archetype, Scope).

### Négatives / coûts
- `tools/vbb-project-init.py` est étendu : code additionnel (~50 lignes).
- Les projets existants devront re-bootstraper ou appliquer un patch manuel.
- Le schéma est canonique : modifier une section = réviser cette ADR.

### Neutres
- `docs/ARCHITECTURE.md` n'est pas dans le scope de cette ADR (Gap séparé, Run futur).
- Le schéma est volontairement minimal (pas exhaustif) pour rester adoptable.

## Alternatives rejetées (≥ 2)

### Alternative A — Laisser `CONTEXT.md` minimal, surcharger par des fichiers séparés
- **Description** : continuer le statu quo, ajouter des fichiers `.yaml` séparés pour chaque dimension (DB, Archetype, Scope).
- **Pourquoi rejetée** : dispersion de l'intent projet sur N fichiers complique la lecture et le bootstrap. L'architecte devrait consulter 4-5 fichiers pour comprendre un projet.

### Alternative B — Imposer un schéma exhaustif (15+ sections)
- **Description** : schéma très détaillé, forçant l'architecte à remplir beaucoup de champs.
- **Pourquoi rejetée** : barrière à l'entrée trop haute. Les petits projets (1 service) n'ont pas besoin de toutes les sections. Un schéma minimal est plus adoptable.

### Alternative C — Réutiliser le frontmatter YAML d'un fichier existant (`PROJECT_MODE.md`)
- **Description** : tout mettre en YAML frontmatter de `PROJECT_MODE.md`.
- **Pourquoi rejetée** : `PROJECT_MODE.md` est cyclique (le mode DEV/PROD change), alors que `CONTEXT.md` est relativement stable. Mélanger les deux polluerait `PROJECT_MODE.md`.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Le schéma est trop minimal et doit être étendu fréquemment | moyenne | faible | Procédure d'extension additive (nouvelles sections sans casser les anciennes) |
| Le lint associé est trop permissif (accepte les champs manquants) | moyenne | moyen | Le lint marquera les sections obligatoires en `required` |
| Les projets existants refusent de migrer | moyenne | faible | Pas de blocker — le schéma est recommandé, pas imposé run-time avant un Run futur |

## Hypothèses

- Le schéma proposé est suffisant pour les bootstraps actuels.
- Les migrations de projets existants sont triviales (script de patch, pas de Run dédié).
- Le lint `vbb-context-lint.py` est construit dans un Run futur (après cette décision).

## Références

- ADR amont : [`0005-db-orientation-context-extension.md`](0005-db-orientation-context-extension.md), [`0006-project-archetype-context-extension.md`](0006-project-archetype-context-extension.md), [`0007-contracts-consumed-canonical-file.md`](0007-contracts-consumed-canonical-file.md)
- Audits : [`docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md`](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) § Gap-14
- POCs : vide

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: GOUVERNANCE
reversible: true
depends_on:
  - "0005-db-orientation-context-extension.md"
  - "0006-project-archetype-context-extension.md"
  - "0007-contracts-consumed-canonical-file.md"
blocks:
  - "tools/vbb-project-init.py (extension Run futur)"
  - "vbb-context-lint.py (création Run futur)"
supersedes:
  - vide
verified_at: "2026-07-12T00:30:00Z"
verified_by: "human"
verified_method: "human-review"
```
