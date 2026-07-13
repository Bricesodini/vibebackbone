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

# ADR — 0006-project-archetype-context-extension

**Status**: ACCEPTED  
**Date**: 2026-07-12  
**Route**: STRUCTUREE  
**Décideurs**: Brice Sodini (project lead & canon owner)  
**Liée à**: docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md § Gap-02  
**Liée à POC**: vide

## Contexte

Vibebackbone traite aujourd'hui **tous les projets de la même façon**, indépendamment de leur nature. Un orchestrateur reçoit le même template `01_INTAKE.md.template` qu'un service API. Un consommateur read-only est validé par les mêmes contrats qu'un producteur. Une library est routée par le même skill-router qu'une application frontend.

Le constat est documenté dans `01_GAP_ANALYSIS.md` § Gap-02 : `tools/vbb-contract-lint.py` ligne 79 impose seulement `contract['type'] == 'prompt_skill'`, qui est un typage au niveau skill et non au niveau projet. `tools/vbb-project-init.py` ligne 264 expose un enum `--mode {DEV,PROD}` qui est l'unique dimension de variation.

Conséquence : la classification « ce projet est une stack frontend / un service API / un orchestrateur / un consommateur read-only » est purement conversationnelle. Vibebackbone ne peut pas adapter ses règles de validation, ses templates d'artefact, ou son linter au type de projet.

Tant qu'aucun typage projet n'est déclaré structurellement, le passage à l'échelle (N services de N types différents) force les architectes à inventer des workarounds en prose.

## Décision

**Le project_archetype d'un projet sera déclaré structurellement dans `docs/CONTEXT.md` via une nouvelle section `## Project Archetype` typée, choisie parmi l'enum canonique : `frontend_app` / `api_service` / `orchestrator` / `read_only_consumer` / `worker` / `library`.**

Chaque déclaration inclut : (a) la valeur de l'enum, (b) une rationale courte (1-3 phrases), (c) une référence à un ADR projet optionnel si la décision est non-triviale.

Les valeurs sémantiques :

| Valeur | Sens |
|--------|------|
| `frontend_app` | Application avec UI (SPA, MPA, mobile). Consomme des APIs. Pas de DB propre en général. |
| `api_service` | Service HTTP/gRPC qui expose des endpoints. Possède typiquement sa DB. |
| `orchestrator` | Service qui coordonne d'autres services. Stateful, business-logique complexe. |
| `read_only_consumer` | Service qui lit les données d'autres services. Pas de DB propre, pas d'écriture. |
| `worker` | Service qui exécute des jobs asynchrones (consume queue, produce output). |
| `library` | Package réutilisable (npm/pip/cargo/etc.). Pas de runtime propre. |

L'enum est **canonique** : un projet ne peut pas introduire une nouvelle valeur sans modifier cette ADR. Toute valeur hors-enum doit être rejetée par `vbb-project-init.py` étape de validation (implémentation future).

**Effet sur les outils** (implémentation future, post-Run 8) : un `api_service` active le linter de contrats, un `read_only_consumer` active un lint de cohérence avec les contrats consommés, un `library` reçoit des templates d'artefact simplifiés.

## Conséquences

### Positives
- L'archetype projet est exploitable par les outils (lint, templates, gates).
- Les workarounds conversationnels disparaissent au profit de règles outillées.
- Le passage à l'échelle (N services hétérogènes) devient gérable : chaque type a ses règles.
- Cohérence avec ADR-0005 (même schéma projet — `db_orientation` et `project_archetype` sont les deux axes du typage).

### Négatives / coûts
- L'enum à 6 valeurs doit être maintenu : ajouter une valeur (ex. `data_pipeline`) demande une révision de cette ADR.
- `tools/vbb-project-init.py` doit être étendu pour proposer le choix à l'init (Run futur).
- `tools/vbb-contract-lint.py` et d'autres linters doivent apprendre à être **archetype-aware** (Run futur, Étape 3+ de Phase 2).

### Neutres
- Aucun canon touché.
- `PROJECT_MODE.md` n'est pas modifié (l'archetype est orthogonal au mode DEV/PROD).

## Alternatives rejetées (≥ 2)

### Alternative A — Typer via `--mode` étendu (ex. `--mode {DEV,PROD,API,WORKER}`)
- **Description** : réutiliser le seul enum existant `--mode` et ajouter des valeurs.
- **Pourquoi rejetée** : `--mode` est sémantiquement lié au cycle dev/prod, pas au type de projet. Mélanger les deux crée une confusion (un `api_service` peut être en DEV ou en PROD).

### Alternative B — Créer un fichier `docs/ARCHETYPE.yaml` séparé
- **Description** : nouveau fichier machine-readable dédié à l'archetype.
- **Pourquoi rejetée** : même argument que ADR-0005 Alternative B — dispersion de l'intent projet sur N fichiers complique la lecture. `CONTEXT.md` est l'entrypoint canonique.

### Alternative C — Inférer l'archetype depuis la structure du repo (heuristique)
- **Description** : deviner l'archetype par grep (présence de `package.json` + `frontend/` → `frontend_app`, etc.).
- **Pourquoi rejetée** : heuristique fragile. Un projet qui migre de `api_service` à `orchestrator` doit pouvoir le déclarer explicitement. L'inférence ne marche pas pour les projets hybrides.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Un projet déclare un archetype erroné (ex. `api_service` au lieu de `worker`) | moyenne | faible | La rationale documente le choix ; un humain peut challenger en review. Pas de blocker. |
| L'enum ne couvre pas un cas émergent (ex. `data_pipeline`) | faible | moyen | Procédure d'extension documentée : ouvrir un PR avec nouvelle valeur + rationale |
| Les linters doivent devenir archetype-aware : complexité accrue | forte | moyen | Étape 3+ de Phase 2 avec POC pour valider le pattern |

## Hypothèses

- L'enum à 6 valeurs est suffisante pour les cas d'usage actuels (studio-projects contient a priori 1× `api_service` + 1× `worker` + 1× `orchestrator` + 1× `read_only_consumer`).
- L'archetype est orthogonal au `db_orientation` (ADR-0005) — un `api_service` peut avoir n'importe quel `db_orientation`.
- Aucun projet existant n'a encore besoin d'être reclassé (la déclaration est additive).

## Références

- ADR amont : [`0005-db-orientation-context-extension.md`](0005-db-orientation-context-extension.md) (même schéma projet)
- Audits : [`docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md`](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) § Gap-02
- POCs : vide
- Docs externes : [`docs/CONTEXT.md`](../../CONTEXT.md) (template actuel, à enrichir)

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: GOUVERNANCE
reversible: true
depends_on:
  - "0005-db-orientation-context-extension.md"
blocks:
  - "tools/vbb-contract-lint.py (archetype-aware, Run futur)"
  - "tools/vbb-project-init.py (ajout choix init, Run futur)"
supersedes:
  - vide
verified_at: "2026-07-12T00:30:00Z"
verified_by: "human"
verified_method: "human-review"
```
