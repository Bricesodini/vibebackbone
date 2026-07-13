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

# ADR — 0007-contracts-consumed-canonical-file

**Status**: ACCEPTED  
**Date**: 2026-07-12  
**Route**: STRUCTUREE  
**Décideurs**: Brice Sodini (project lead & canon owner)  
**Liée à**: docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md § Gap-05  
**Liée à POC**: vide

## Contexte

Vibebackbone n'a aujourd'hui aucune obligation structurelle pour un projet de **documenter ce qu'il consomme** depuis d'autres services. Aucun fichier `CONTRACTS_CONSUMED.md` n'existe nulle part dans le repo (vérifié : zéro hit `find`). Aucun template n'existe dans `docs/templates/` (vérifié `ls docs/templates/` : 7 templates de phase + ADR + POC + INTEGRATION_GATE + CANON_CHANGE_PROPOSAL + worker-evidence-paragraph, aucun `CONTRACTS_CONSUMED`).

Conséquence : un service qui consomme une API d'un autre service peut écrire cette dépendance en prose dans `CONTEXT.md` section « Stack principale » — ou pas. Aucun impact analyzer ne peut répondre à « quels services dépendent de mon endpoint X ». Aucune alerte de breaking change ne peut être générée pour les consommateurs. La discipline multi-service (database-per-service, API d'intégration) est entièrement dépendante de la vigilance humaine.

Le constat est documenté dans `01_GAP_ANALYSIS.md` § Gap-05. Le gap est classé **P0** car sans tracking des contrats consommés, les patterns database-per-service ne sont pas viables de façon vérifiable : l'analyse d'impact cross-service est impossible.

## Décision

**Chaque projet Vibebackbone qui consomme au moins un contrat externe doit maintenir un fichier canonique `docs/CONTRACTS_CONSUMED.md` documentant structurellement ce qu'il consomme.**

Structure du fichier (par projet) :

```markdown
# CONTRACTS_CONSUMED — <project_slug>

> **Owner** : <équipe / maintainer>
> **Last updated** : <YYYY-MM-DD>
> **Schema version** : 1.0 (cf. ADR-0007)

## Contrats consommés

| Provider | Type | Endpoint / resource | Version pinned | Criticité | Notes |
|----------|------|---------------------|----------------|-----------|-------|
| `<service-A>` | `rest_api` | `GET /v1/users/{id}` | `v1.4.2` | `critical` | Auth via JWT |
| `<service-A>` | `event` | `UserCreated` | `schema-v3` | `critical` | Event bus NATS |
| `<service-B>` | `db_replica` | `postgres://read-replica/orders` | snapshot daily | `medium` | Read-only |

## Légende

- **Type** : `rest_api` | `grpc` | `event` | `db_replica` | `db_shared_readonly` | `file` | `cron`
- **Criticité** : `critical` (bloquant) | `medium` (dégrade) | `low` (cosmétique)
- **Version pinned** : semver pour API/DB, schema-vN pour events

## Process de mise à jour

1. À l'ajout d'une dépendance : insérer une ligne + rationale.
2. À la modification d'un contrat consommé : vérifier la version pinned, mettre à jour si breaking.
3. À la suppression d'une dépendance : retirer la ligne + rationale.

## Références impact

Les modifications upstream sont tracées dans `docs/IMPACT_LOG.md` (Gap-06 — Run futur).
```

Un template `docs/templates/CONTRACTS_CONSUMED.md.template` est créé (exécution future — Run 9+) pour faciliter l'init.

**Effet sur les outils** (implémentation future) :

- `t-vbb-impact-analyzer` consomme ce fichier pour répondre à « qui dépend de mon endpoint X ? ».
- `vbb-multiservice-lint.py` (futur) vérifie que les contrats consommés sont à jour (date < 90 jours).
- `vbb-multiservice-graph.py` (futur) génère le graphe inter-services depuis ce fichier + `CONTRACTS_PROVIDED.md` (symétrique, à définir).

## Conséquences

### Positives
- L'analyse d'impact cross-service devient outillée (et non manuelle).
- L'alerte de breaking change vers les consommateurs devient possible.
- Le graphe inter-services (Gap-13, Étape 3) devient dérivable.
- La discipline multi-service passe de « vigilance humaine » à « vérification outillée ».

### Négatives / coûts
- Chaque nouveau projet doit maintenir un fichier de plus. Coût d'init : 5 minutes.
- Le format doit être stable : changer le schéma (colonnes) demande une migration des fichiers existants.
- Les outils consommateurs (`t-vbb-impact-analyzer`, linters) doivent apprendre à parser ce format.

### Neutres
- `CONTRACTS_PROVIDED.md` (symétrique, ce qu'un service expose) reste à définir — Run futur.
- L'enum `type` peut grandir (ex. ajouter `graphql`).

## Alternatives rejetées (≥ 2)

### Alternative A — Documenter dans `CONTEXT.md` section libre
- **Description** : continuer le statu quo avec prose libre dans `CONTEXT.md`.
- **Pourquoi rejetée** : impossible à parser / dériver. L'argument est identique à ADR-0005 Alternative A.

### Alternative B — README.md enrichi en YAML frontmatter
- **Description** : typer les dépendances dans le frontmatter YAML de `README.md`.
- **Pourquoi rejetée** : le frontmatter de `README.md` est prévu pour les métadonnées de présentation (titre, description), pas pour des données structurées d'architecture. Mélanger les deux réduit la lisibilité humaine du frontmatter.

### Alternative C — Fichier `package.json` / `Cargo.toml` / `requirements.txt` (le manifeste technique)
- **Description** : réutiliser le fichier de dépendances du langage.
- **Pourquoi rejetée** : ces fichiers ne tracent que les **dépendances de code** (libraries), pas les **dépendances de service** (APIs runtime). Un projet peut dépendre de `axios` ET consommer `GET /v1/users` — les deux notions sont orthogonales.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Le fichier n'est pas maintenu après le bootstrap | forte | moyen | Le linter (futur) vérifie `Last updated < 90 jours`. |
| Le schéma évolue et casse les fichiers existants | moyenne | moyen | Procédure d'extension documentée : nouvelle colonne est additive, les anciens fichiers restent valides |
| Le format YAML/table est trop rigide pour des cas exotiques | moyenne | faible | Une section `## Notes` par ligne permet les annotations libres |

## Hypothèses

- Le schéma à 6 colonnes (Provider, Type, Endpoint, Version, Criticité, Notes) couvre les cas d'usage actuels.
- L'enum `type` à 7 valeurs est extensible (graphql, etc. ajoutables).
- `CONTRACTS_PROVIDED.md` (symétrique) sera défini dans un Run futur indépendant.

## Références

- ADR amont : [`0005-db-orientation-context-extension.md`](0005-db-orientation-context-extension.md) (Gap-01, même esprit de structuration)
- ADR symétrique (futur) : `CONTRACTS_PROVIDED.md` (à définir)
- Audits : [`docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md`](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) § Gap-05
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
  - "Gap-04 (linter multi-service)"
  - "Gap-06 (IMPACT_LOG)"
  - "Gap-10 (taxonomie contrats cross-service)"
  - "Gap-13 (graphe inter-services)"
  - "Gap-15 (gate PR)"
supersedes:
  - vide
verified_at: "2026-07-12T00:30:00Z"
verified_by: "human"
verified_method: "human-review"
```
