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

# ADR — 0015-contract-lint-archetype-aware

**Status**: ACCEPTED  
**Date**: 2026-07-13  
**Route**: STRUCTUREE  
**Décideurs**: Brice Sodini (project lead & canon owner)  
**Liée à**: docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md § Gap-11  
**Liée à POC**: vide  
**Liée à ADR amont**: 0006 (Project Archetype, fournit la donnée)

## Contexte

`tools/vbb-contract-lint.py` valide aujourd'hui tous les `CONTRACT.yaml` avec les mêmes règles : schema version, gates, routing, agents reconnus. Mais un `CONTRACT.yaml` d'une **library** n'a pas la même forme qu'un `CONTRACT.yaml` d'un `api_service` (la library n'expose pas de runtime, l'api_service doit avoir un endpoint défini).

Aujourd'hui, tous les projets sont validés identiquement. Un projet typé `library` qui omet `outputs.artifact.kind` reçoit un warning, alors que pour une library c'est légitime. Un `worker` sans trigger explicite ne reçoit pas de signal.

Le constat est documenté dans `01_GAP_ANALYSIS.md` § Gap-11. Sans adaptation contextuelle, le linter force les workarounds en prose.

## Décision

**Étendre `tools/vbb-contract-lint.py` pour rendre les règles contextuelles au `project_archetype` (cf. ADR-0006).**

### Comportement par archetype

| Archetype | Règles actives | Règles assouplies |
|-----------|----------------|-------------------|
| `api_service` | Toutes les règles actuelles | Aucune |
| `read_only_consumer` | Toutes + « pas d'`outputs.artifact` exposé sauf read-only marker » | Aucune |
| `worker` | Toutes + « au moins un `gates.event` ou `gates.cron` ou `gates.queue` (trigger obligatoire) » | Aucune |
| `library` | Schema, gates, routing | `outputs.artifact.kind` optionnel, `gates.runtime` optionnel |
| `frontend_app` | Toutes | `gates.security` assoupli (auth traité au edge) |
| `orchestrator` | Toutes + « `outputs.artifact` obligatoire + références cross-service explicites » | Aucune |

### Source du `project_archetype`

Le `project_archetype` est lu depuis le frontmatter YAML de `docs/CONTEXT.md` (cf. ADR-0006) :

```yaml
---
project_archetype: <api_service | ...>
---
```

Si le frontmatter n'existe pas, **fallback** : règles actuelles (mode non-archetype-aware, comme aujourd'hui).

### Modes

- **Par défaut** : warning console, exit 0.
- **`--strict`** (CI) : les warnings deviennent errors, exit 2 si violation.
- **`--archetype <slug>`** : override le `project_archetype` détecté depuis CONTEXT.md (utile pour tester un projet avec un autre archetype).

### Exemple de message

```
[vbb-contract-lint] skill=1-vbb-code-janitor
  ⚠️  archetype=library detected: rule 'outputs.artifact.kind required' is relaxed
  ✓ All other rules passed
```

## Conséquences

### Positives
- Les règles sont adaptées au contexte projet.
- Les `library` ne reçoivent plus de faux warnings.
- Les `worker` reçoivent un signal explicite s'ils n'ont pas de trigger.
- La discipline devient contextuelle (pas universelle).

### Négatives / coûts
- `vbb-contract-lint.py` doit être étendu (~150 lignes).
- Les règles par archetype doivent être testées (out of scope ce run).
- Un projet qui change d'archetype peut voir de nouveaux warnings apparaître.

### Neutres
- Aucun canon modifié.
- Le schéma `CONTRACT.yaml` reste le même ; seul le linter devient contextuel.

## Alternatives rejetées (≥ 2)

### Alternative A — Règles universelles (statu quo)
- **Description** : continuer de valider tous les projets avec les mêmes règles.
- **Pourquoi rejetée** : génère des faux warnings pour les `library`, `worker`, etc.

### Alternative B — Schémas `CONTRACT.yaml` distincts par archetype
- **Description** : un schéma YAML différent pour chaque archetype (`api_service.schema.yaml`, `library.schema.yaml`, etc.).
- **Pourquoi rejetée** : multiplicité des schémas, complexité de maintenance, risque d'incohérence. Une seule couche de linter contextuelle est plus simple.

### Alternative C — Champ `archetype` dans `CONTRACT.yaml` lui-même
- **Description** : chaque `CONTRACT.yaml` déclare son archetype.
- **Pourquoi rejetée** : duplication avec `docs/CONTEXT.md`. Le `project_archetype` est une propriété de l'intent projet (CONTEXT.md), pas du skill individuel.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Les règles par archetype sont mal calibrées (trop strictes ou trop laxistes) | moyenne | moyen | Itération par projet concret (POC) avant généralisation |
| Un projet qui change d'archetype voit des warnings surgir | faible | faible | Documentation explicite ; mode `--archetype` permet de tester |
| L'extension casse la compatibilité avec l'existant | faible | moyen | Le mode `non-archetype-aware` reste le fallback par défaut |

## Hypothèses

- `docs/CONTEXT.md` est créé par `t-vbb-project-context-init` qui inclut le frontmatter (cf. ADR-0008).
- Le `project_archetype` est un enum à 6 valeurs (cf. ADR-0006).
- Les règles supplémentaires par archetype sont extensibles (ajout futur).

## Références

- ADR amont : [`0006-project-archetype-context-extension.md`](0006-project-archetype-context-extension.md)
- Audits : [`docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md`](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) § Gap-11
- Outil lié : [`tools/vbb-contract-lint.py`](../../tools/vbb-contract-lint.py) (à étendre)
- POCs : vide

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: ARCHITECTURE
reversible: true
depends_on:
  - "0006-project-archetype-context-extension.md"
blocks:
  - "tools/vbb-contract-lint.py extension (Run 13+)"
supersedes:
  - vide
verified_at: "2026-07-13T00:00:00Z"
verified_by: "human"
verified_method: "human-review"
```