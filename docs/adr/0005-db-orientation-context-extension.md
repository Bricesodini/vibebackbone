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

# ADR — 0005-db-orientation-context-extension

**Status**: ACCEPTED  
**Date**: 2026-07-12  
**Route**: STRUCTUREE  
**Décideurs**: Brice Sodini (project lead & canon owner)  
**Liée à**: docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md § Gap-01  
**Liée à POC**: vide

## Contexte

Vibebackbone n'a aujourd'hui aucun moyen canonique d'exprimer l'**orientation DB** d'un projet — c'est-à-dire la topologie de persistance du projet vis-à-vis des autres services. Un projet bootstrapé par `t-vbb-project-context-init` produit un `CONTEXT.md` minimal (18 lignes) qui ne contient aucune section structurée pour déclarer si le projet possède sa propre DB, consomme une DB externe en lecture, ou est polyglotte.

Le constat est documenté dans `01_GAP_ANALYSIS.md` § Gap-01 : `tools/vbb-project-init.py` lignes 67-86 (`_project_mode_md`) et 88-110 (`_context_md`) ne déclarent aucun champ `db_orientation`. Lignes 112-140 (`_architecture_md`) non plus. La classification est purement conversationnelle — forçant l'architecte à écrire en prose dans `CONTEXT.md` section « Stack principale ».

Tant que cette information n'est pas structurée, il est **impossible** de : (a) dériver automatiquement des règles spécifiques (ex. « ce projet ne doit pas avoir de migration sans ADR ») ; (b) raisonner sur les dépendances DB lors d'un changement de contrat ; (c) signaler une violation de discipline DB sans grep manuel.

## Décision

**La orientation DB d'un projet sera déclarée structurellement dans `docs/CONTEXT.md` via une nouvelle section `## DB Orientation` typée, choisie parmi l'enum canonique : `owned_private` / `shared_external_owned` / `shared_external_readonly` / `polyglot` / `stateless`.**

Chaque déclaration inclut : (a) la valeur de l'enum, (b) une rationale courte (1-3 phrases), (c) une référence à un ADR projet optionnel si la décision est non-triviale (par exemple un reverse-proxy, un shared cache, etc.).

Les valeurs sémantiques :

| Valeur | Sens |
|--------|------|
| `owned_private` | Le projet possède sa propre DB, isolée des autres services. Modèle database-per-service. |
| `shared_external_owned` | Le projet consomme une DB possédée par un autre service (ex. shared auth DB). |
| `shared_external_readonly` | Le projet consomme une DB externe en lecture seule (replica, mirror). |
| `polyglot` | Le projet possède plusieurs DB de technologies hétérogènes (Postgres + Redis + etc.). |
| `stateless` | Le projet n'a aucune persistance propre (orchestrateur pur, lambda, etc.). |

L'enum est **canonique** : un projet ne peut pas introduire une nouvelle valeur sans modifier cette ADR. Toute valeur hors-enum doit être rejetée par `vbb-project-init.py` étape de validation (implémentation future).

## Conséquences

### Positives
- L'orientation DB est exploitable par les outils d'analyse (lint, impact analyzer, graph).
- L'architecte peut raisonner sur les dépendances DB sans grep manuel dans `CONTEXT.md`.
- Le pattern database-per-service devient outillé (vs purement conversationnel aujourd'hui).
- La règle « pas de migration sans ADR » peut être dérivée automatiquement pour les `owned_private`.

### Négatives / coûts
- L'enum doit être maintenu : ajouter une valeur (ex. `event_sourced_only`) demande une révision de cette ADR.
- Les projets bootstrapés avant cette décision devront migrer leur `CONTEXT.md` (une opération manuelle triviale).
- `tools/vbb-project-init.py` doit être étendu pour offrir le choix à l'init (Run futur).

### Neutres
- `PROJECT_MODE.md` n'est pas modifié (la DB Orientation est une propriété d'intent projet, pas de mode dev/prod).
- Aucun autre canon touché.

## Alternatives rejetées (≥ 2)

### Alternative A — Déclarer en prose libre dans `CONTEXT.md` section « Stack principale »
- **Description** : continuer le statu quo ; l'architecte écrit « j'utilise Postgres owned par ce service » en texte libre.
- **Pourquoi rejetée** : impossible à dériver / auditer. Aucun lint ne peut vérifier la cohérence. Aucune analyse d'impact cross-service n'est possible.

### Alternative B — Créer un fichier séparé `docs/DB_ORIENTATION.md`
- **Description** : nouveau fichier dédié à l'orientation DB, séparé de `CONTEXT.md`.
- **Pourquoi rejetée** : dispersion de l'intent projet sur N fichiers complique la lecture. `CONTEXT.md` est déjà le point d'entrée canonique pour l'intent ; ajouter un fichier crée un nouvel entrypoint sans gain de structure.

### Alternative C — Modifier le canon `CONVENTIONS.md` pour ajouter une section « DB Orientation »
- **Description** : poser la convention au niveau du framework, pas au niveau projet.
- **Pourquoi rejetée** : `CONVENTIONS.md` est le canon des **conventions de code** (Pillars 1-5). L'orientation DB est une **décision projet**, pas une convention de code. Le bon endroit est `CONTEXT.md`.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Un projet déclare une valeur hors-enum (ex. `hybrid_mixed`) | moyenne | moyen | Le lint de `CONTEXT.md` (futur) refusera les valeurs hors-enum avec un message clair pointant vers cette ADR |
| L'enum ne couvre pas un cas émergent (ex. `event_sourced`) | faible | moyen | Procédure d'extension documentée : ouvrir un PR avec nouvelle valeur + rationale |
| Les projets existants ne déclarent pas leur `db_orientation` | forte | faible | Migration manuelle triviale ; aucun blocker (la valeur par défaut raisonnable est `owned_private`, à valider projet par projet) |

## Hypothèses

- L'enum à 5 valeurs est suffisante pour les cas d'usage actuels (studio-projects, export-engine, compta).
- `tools/vbb-project-init.py` sera étendu dans un Run futur (Run 9+) pour proposer le choix à l'init.
- Aucun outil tiers ne parse aujourd'hui `CONTEXT.md` comme une source de données structurée (autre que prose).

## Références

- ADR amont : vide
- Audits : [`docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md`](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) § Gap-01
- POCs : vide
- Docs externes : [`docs/CONTEXT.md`](../../CONTEXT.md) (template actuel, à enrichir)

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: GOUVERNANCE
reversible: true
depends_on:
  - vide
blocks:
  - "docs/strategy/vbb-improvements-roadmap/runs/run-09+ (implémentation)"
supersedes:
  - vide
verified_at: "2026-07-12T00:30:00Z"
verified_by: "human"
verified_method: "human-review"
```
