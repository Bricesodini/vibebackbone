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

# ADR — 0009-multiservice-lint-discipline

**Status**: ACCEPTED  
**Date**: 2026-07-13  
**Route**: STRUCTUREE  
**Décideurs**: Brice Sodini (project lead & canon owner)  
**Liée à**: docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md § Gap-04  
**Liée à POC**: vide  
**Liée à ADR amont**: 0007 (CONTRACTS_CONSUMED, fournit les données)

## Contexte

Vibebackbone définit une discipline multi-service (database-per-service, API d'intégration, co-évolution) qui est **documentée** dans nos conversations mais **pas outillée**. Le constat est documenté dans `01_GAP_ANALYSIS.md` § Gap-04 : aucun linter n'interdit l'accès direct à la DB d'un autre service, n'exige la mise à jour d'un log d'impact avant modification de contrat, ni ne vérifie que les contrats consommés sont tracés dans `CONTRACTS_CONSUMED.md`.

Conséquence concrète : un projet multi-service peut importer directement le client DB d'un autre service sans qu'aucun signal ne soit émis. La dépendance n'est pas détectée. La régression peut être introduite silencieusement dans une PR, puis découverte en production.

Cette dépendance à la vigilance humaine est fragile : elle ne survit pas au passage à l'échelle (N services, N producteurs, N consommateurs) ni aux changements d'équipe.

## Décision

**Créer un nouvel outil canonique `tools/vbb-multiservice-lint.py` qui valide, pour chaque projet multi-service, trois familles de règles de discipline, en consommant un fichier de configuration par projet `docs/MULTISERVICE_DISCIPLINE.yaml`.**

### Les 3 familles de règles

| Famille | Règle | Source de vérité |
|---------|-------|------------------|
| **DB isolation** | Si le projet déclare `db_orientation: shared_external_*`, interdire l'usage direct du client DB d'un autre service sans passer par une API documentée | `db_orientation` (ADR-0005), grep des imports/sources |
| **IMPACT_LOG à jour** | Si `docs/IMPACT_LOG.md` existe (ADR-0010), vérifier qu'au moins une entrée existe si le projet a des contrats consommés (ADR-0007) | `IMPACT_LOG.md` + `CONTRACTS_CONSUMED.md` |
| **CONTRACTS_CONSUMED à jour** | Si `docs/CONTRACTS_CONSUMED.md` existe, vérifier `Last updated < 90 jours` | `CONTRACTS_CONSUMED.md` |

### Le fichier de configuration `docs/MULTISERVICE_DISCIPLINE.yaml`

```yaml
# Config par projet — overridable
schema_version: "1.0"

# Règles actives
rules:
  db_isolation:
    enabled: true
    severity: error       # error | warning
  impact_log_required:
    enabled: true
    severity: warning
  contracts_consumed_freshness:
    enabled: true
    severity: warning
    max_age_days: 90

# Allow-list explicite (cas justifiés)
allowlist:
  db_isolation:
    - path: "scripts/migration/"
      reason: "migration tools can access any DB during deploy window"
```

### Comportement du linter

- **Mode par défaut** : warning console, exit code 0.
- **Mode `--strict`** (CI) : error si une règle est violée, exit code 2 (`GATE_BLOCKED`).
- **Mode `--json`** : sortie machine-readable pour intégration dashboard.
- **Skip explicite** : `rules.<name>.enabled: false` désactive la règle par projet.

### Positionnement par rapport à `vbb-contract-lint.py`

- `vbb-contract-lint.py` valide les **contrats au niveau framework** (schéma, gates, routing, schema version).
- `vbb-multiservice-lint.py` valide la **discipline au niveau projet** (DB isolation, freshness).

Les deux sont complémentaires : un contrat peut être valide au niveau framework mais violer la discipline au niveau projet (ex. consumer non tracé). Les deux doivent passer pour un merge propre.

## Conséquences

### Positives
- La discipline multi-service passe de « vigilance humaine » à « vérification outillée ».
- Les régressions sont détectées avant merge (via `--strict` en CI).
- Le linter est configurable par projet (allow-list explicite documentée).
- Cohérence avec ADR-0007 (consomme `CONTRACTS_CONSUMED.md`) et ADR-0010 (consomme `IMPACT_LOG.md`).

### Négatives / coûts
- Nouveau code à maintenir (~200-300 lignes Python).
- Le fichier `MULTISERVICE_DISCIPLINE.yaml` doit être créé dans chaque projet multi-service.
- Les règles par défaut peuvent être trop strictes au début → itération nécessaire.
- `--strict` peut bloquer des merges existants → adoption progressive recommandée.

### Neutres
- `vbb-contract-lint.py` n'est pas modifié.
- Aucun canon direct n'est modifié.

## Alternatives rejetées (≥ 2)

### Alternative A — Discipline purement conversationnelle (statu quo)
- **Description** : continuer de s'appuyer sur la vigilance humaine à chaque PR.
- **Pourquoi rejetée** : ne survit pas au passage à l'échelle ni aux changements d'équipe. Régression silencieuse possible.

### Alternative B — Intégrer dans `vbb-contract-lint.py` (un seul outil)
- **Description** : ajouter les règles multi-service dans le linter de contrats existant.
- **Pourquoi rejetée** : séparation des concerns. `vbb-contract-lint` valide des contrats au niveau framework (indépendant du projet), `vbb-multiservice-lint` valide la discipline au niveau projet (config par projet). Les modes (warning vs strict) et la gouvernance diffèrent.

### Alternative C — Créer un hook pre-commit générique
- **Description** : utiliser un framework pre-commit existant (pre-commit.com) avec des hooks YAML.
- **Pourquoi rejetée** : ajoute une dépendance externe. Vibebackbone doit pouvoir fonctionner sans réseau. Un outil Python interne est plus contrôlable.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Les règles par défaut bloquent des merges légitimes au déploiement | forte | moyen | Mode warning par défaut ; adoption progressive ; allow-list par projet |
| Le fichier `MULTISERVICE_DISCIPLINE.yaml` n'est pas créé dans les projets existants | forte | faible | Le linter est silencieux si le fichier n'existe pas (no-project mode) |
| Faux positifs sur la règle DB isolation (grep peut matcher des strings) | moyenne | faible | Allow-list par chemin avec rationale documentée |

## Hypothèses

- L'enum `db_orientation` d'ADR-0005 est la source de vérité pour la règle DB isolation.
- ADR-0007 et ADR-0010 sont exécutés (ou seront) — sinon le linter est en mode dégradé.
- L'allow-list par projet est un mécanisme acceptable (vs une règle globale).

## Références

- ADR amont : [`0007-contracts-consumed-canonical-file.md`](0007-contracts-consumed-canonical-file.md)
- ADR lié (à exécuter) : [`0010-impact-log-cumulative.md`](0010-impact-log-cumulative.md)
- Audits : [`docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md`](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) § Gap-04
- Outils existants : [`tools/vbb-contract-lint.py`](../../tools/vbb-contract-lint.py) (séparation des concerns)
- POCs : vide

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: ARCHITECTURE
reversible: true
depends_on:
  - "0007-contracts-consumed-canonical-file.md"
  - "0010-impact-log-cumulative.md"
blocks:
  - "tools/vbb-multiservice-lint.py (implémentation, Run 10+)"
  - "Gap-15 (gate CI multi-service)"
supersedes:
  - vide
verified_at: "2026-07-13T00:00:00Z"
verified_by: "human"
verified_method: "human-review"
```