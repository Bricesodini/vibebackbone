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

# ADR — 0014-canon-vs-extension

**Status**: ACCEPTED  
**Date**: 2026-07-13  
**Route**: STRUCTUREE  
**Décideurs**: Brice Sodini (project lead & canon owner)  
**Liée à**: docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md § Gap-09  
**Liée à POC**: vide

## Contexte

Vibebackbone a un canon (CONVENTIONS.md, PILOTAGE.md, AGENTS.md) qui évolue lentement via des propositions explicites (`CANON_CHANGE_PROPOSAL.md`). Mais il n'existe aucun mécanisme pour qu'un projet **étende localement** le framework avec un pattern nouveau — sans modifier le canon.

Conséquence : chaque fois qu'un projet a besoin d'un pattern (ex. multi-service database-per-service, event-sourced, etc.), il doit soit :
- Forker le framework (et diverger du canon)
- Proposer un canon change (et attendre la validation, ce qui est lourd pour un besoin local)
- Réinventer le pattern localement sans aucun mécanisme d'enregistrement (donc invisible au framework)

Le constat est documenté dans `01_GAP_ANALYSIS.md` § Gap-09. Sans mécanisme d'extension, le framework reste rigide face à des besoins locaux légitimes.

## Décision

**Introduire le dossier `docs/extensions/<pattern>/` avec un fichier `MANIFEST.yaml` qui déclare chaque extension locale.**

### Structure

```
docs/extensions/
├── multi-service-database-per-service/
│   ├── MANIFEST.yaml       # déclaration
│   ├── rules.yaml          # règles spécifiques
│   └── README.md           # documentation
├── event-sourced/
│   ├── MANIFEST.yaml
│   └── ...
└── (autres patterns futurs)
```

### Format `MANIFEST.yaml`

```yaml
schema_version: "1.0"

pattern: <slug>          # ex. "multi-service-database-per-service"
display_name: <string>   # ex. "Multi-service database-per-service"
version: <semver>        # ex. "0.1.0"
status: <experimental | beta | stable | deprecated>

# Implications pour le canon
canon_implications:
  contracts_consumed: <additive | breaking | none>
  impact_log: <additive | breaking | none>
  contracts_provided: <additive | breaking | none>
  consumers_required_field: <additive | breaking | none>

# Conflits avec d'autres extensions
conflicts_with:
  - <pattern-slug>
  # ex. - "monolith-service"

# Dépendances
requires:
  patterns:
    - <pattern-slug>     # ex. - "consumed-tracing"
  tools:
    - <tool-name>        # ex. - "vbb-multiservice-lint"

# Métadonnées
author: <string>
created_at: <YYYY-MM-DD>
last_updated: <YYYY-MM-DD>
docs: <relative path to README.md or external link>
```

### Outil d'enregistrement

Un outil `tools/vbb-extension-register.py` lit le dossier `docs/extensions/` et expose :
- `python tools/vbb-extension-register.py list` — liste les extensions actives
- `python tools/vbb-extension-register.py check <pattern>` — valide la cohérence d'une extension (MANIFEST.yaml conforme, pas de conflit, deps satisfaites)
- `python tools/vbb-extension-register.py deps <pattern>` — arbre des dépendances

### Adoption

Une extension est **locale** : elle vit dans `docs/extensions/<pattern>/` du projet, pas dans le framework canon. Si l'extension devient stable et largement adoptée, elle peut migrer vers le canon (Run futur avec `CANON_CHANGE_PROPOSAL.md`).

## Conséquences

### Positives
- Les projets peuvent expérimenter localement sans fork.
- Les extensions sont **visibles** (listées par `vbb-extension-register list`).
- Les conflits sont détectés à l'enregistrement (champ `conflicts_with`).
- Migration extension → canon devient un acte explicite et tracé.

### Négatives / coûts
- Le dossier `docs/extensions/` est un nouveau pattern canonique.
- `MANIFEST.yaml` doit être maintenu pour chaque extension.
- L'outil `vbb-extension-register` (~150 lignes Python) doit être créé.

### Neutres
- Aucun canon direct n'est modifié (le dossier `docs/extensions/` est un nouveau pattern, pas une modif canonique).
- Le framework ne devient pas un « système de plugins » à part entière — c'est un mécanisme d'enregistrement local.

## Alternatives rejetées (≥ 2)

### Alternative A — Fork du framework par projet
- **Description** : chaque projet qui a besoin d'un pattern fork vibebackbone.
- **Pourquoi rejetée** : divergence, coût de maintenance, impossible de réconcilier les forks.

### Alternative B — Plugin runtime via entry points Python
- **Description** : `setup.py` déclare des entry points `vbb.extensions`, chargés dynamiquement.
- **Pourquoi rejetée** : ajoute du dynamic loading Python, complexité runtime, debugging plus difficile. Un dossier + manifest YAML est plus simple et plus testable.

### Alternative C — Modifier le canon pour chaque pattern
- **Description** : tout pattern doit passer par `CANON_CHANGE_PROPOSAL.md`.
- **Pourquoi rejetée** : disproportionné pour des besoins locaux. Le canon doit rester léger.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Trop d'extensions locales sans gouvernance | moyenne | moyen | Le statut `experimental | beta | stable | deprecated` force le projet à qualifier ses extensions |
| Conflits entre extensions non détectés | faible | moyen | `conflicts_with` est validé à l'enregistrement par `vbb-extension-register check` |
| Migration extension → canon mal gérée | faible | moyen | Procédure explicite (Run dédié avec `CANON_CHANGE_PROPOSAL.md`) |

## Hypothèses

- Le dossier `docs/extensions/` est le bon endroit (vs `skills/extensions/` ou autre).
- L'enum `status` à 4 valeurs est suffisant.
- Le mécanisme est volontairement minimal (pas de marketplace d'extensions).

## Références

- Audits : [`docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md`](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) § Gap-09
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
  - "tools/vbb-extension-register.py (implémentation, Run 13+)"
  - "Première extension concrète : docs/extensions/multi-service-database-per-service/ (Gap-12)"
supersedes:
  - vide
verified_at: "2026-07-13T00:00:00Z"
verified_by: "human"
verified_method: "human-review"
```