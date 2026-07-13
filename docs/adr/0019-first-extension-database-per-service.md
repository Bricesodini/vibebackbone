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

# ADR — 0019-first-extension-database-per-service

**Status**: ACCEPTED  
**Date**: 2026-07-13  
**Route**: STRUCTUREE  
**Décideurs**: Brice Sodini (project lead & canon owner)  
**Liée à**: docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md § Gap-12  
**Liée à POC**: vide  
**Liée à ADR amont**: 0014 (canon vs extension, fournit le mécanisme)

## Contexte

Le mécanisme d'extension (ADR-0014, Gap-09) introduit `docs/extensions/<pattern>/MANIFEST.yaml`. Mais sans **première extension concrète**, le mécanisme reste théorique — pas de validation par la pratique, pas de template pour les suivantes.

L'extension la plus naturelle à créer en premier est **`multi-service-database-per-service`** : c'est le pattern central qui motive toute la Phase 1 multi-service (cf. `01_GAP_ANALYSIS.md` §0 : « pattern database-per-service »).

## Décision

**Créer `docs/extensions/multi-service-database-per-service/` comme première extension concrète, servant de POC et de template.**

### Contenu de l'extension

```
docs/extensions/multi-service-database-per-service/
├── MANIFEST.yaml
├── README.md
└── rules.yaml
```

### `MANIFEST.yaml`

```yaml
schema_version: "1.0"

pattern: multi-service-database-per-service
display_name: Multi-service database-per-service
version: "0.1.0"
status: experimental

canon_implications:
  contracts_consumed: additive
  impact_log: additive
  contracts_provided: additive
  consumers_required_field: additive

conflicts_with:
  - monolith-service

requires:
  patterns:
    - contracts-consumed-tracing    # ADR-0007
  tools:
    - vbb-multiservice-lint
    - vbb-multiservice-graph

author: Brice Sodini
created_at: 2026-07-13
last_updated: 2026-07-13
docs: ./README.md
```

### `README.md`

Document d'adoption :
- Quand utiliser cette extension (système multi-service avec DB isolées par service)
- Quand **ne pas** l'utiliser (monolithe, serverless stateful)
- Comment l'activer (copier le dossier, remplir le MANIFEST, déclarer dans `MULTIREPO.yaml`)
- Exemple concret avec un système à 3 services

### `rules.yaml`

Règles spécifiques à l'extension :
- Chaque service déclare `db_orientation: owned_private`
- Pas de DB partagée entre services (sauf via `shared_external_owned` documenté)
- Chaque service maintient son propre `CONTRACTS_CONSUMED.md`

### Positionnement

- L'extension vit dans `docs/extensions/multi-service-database-per-service/` du projet qui l'adopte (pas dans le framework canon).
- Le framework fournit le mécanisme (ADR-0014) ; les projets fournissent les extensions.
- Cette première extension sert de **template** : les suivantes (event-sourced, CQRS, etc.) suivent le même pattern.

## Conséquences

### Positives
- Le mécanisme d'extension (ADR-0014) est validé par un cas concret.
- Les projets multi-service ont un template à suivre.
- Les gaps Gap-09 + Gap-12 sont conjoints : le mécanisme ET son premier usage.

### Négatives / coûts
- L'extension doit être maintenue dans le projet qui l'adopte.
- Le format MANIFEST.yaml doit rester stable (cf. ADR-0014).

### Neutres
- Aucun canon modifié.
- Pas d'outillage supplémentaire requis (le mécanisme d'extension suffit).

## Alternatives rejetées (≥ 2)

### Alternative A — Extension codée en dur dans le framework
- **Description** : ajouter le pattern database-per-service comme type canonique de `db_orientation`.
- **Pourquoi rejetée** : extension locale par nature, pas un cas canonique universel. Le mécanisme d'extension (ADR-0014) est mieux adapté.

### Alternative B — Première extension = un pattern plus simple (e.g., « stateless-service »)
- **Description** : commencer par une extension triviale pour valider le mécanisme.
- **Pourquoi rejetée** : un pattern trivial ne démontre pas la valeur du mécanisme d'extension. Le pattern database-per-service est le plus représentatif.

### Alternative C — Pas de première extension, attendre les contributions
- **Description** : publier le mécanisme (ADR-0014) et attendre que des projets créent leurs extensions.
- **Pourquoi rejetée** : risque que personne ne crée d'extension (manque d'exemple), le mécanisme reste lettre morte.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| L'extension reste à `experimental` indéfiniment | moyenne | faible | Procédure de promotion `experimental → beta → stable` documentée dans `MANIFEST.yaml` |
| Le format MANIFEST.yaml doit évoluer | moyenne | faible | `schema_version` permet l'évolution additive |
| L'extension est copiée sans adaptation (copier-coller) | moyenne | faible | README explicite que l'extension doit être personnalisée par projet |

## Hypothèses

- Le pattern `database-per-service` est le bon premier exemple (validation par la pratique).
- Les projets adopteront l'extension après voir un POC concret.

## Références

- ADR amont : [`0014-canon-vs-extension.md`](0014-canon-vs-extension.md)
- Audits : [`docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md`](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) § Gap-12
- POCs : vide

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: ARCHITECTURE
reversible: true
depends_on:
  - "0014-canon-vs-extension.md"
blocks:
  - "docs/extensions/multi-service-database-per-service/ (création effective, Run 13+)"
supersedes:
  - vide
verified_at: "2026-07-13T00:00:00Z"
verified_by: "human"
verified_method: "human-review"
```