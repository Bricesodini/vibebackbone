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

# ADR — 0017-co-evolution-discipline

**Status**: ACCEPTED  
**Date**: 2026-07-13  
**Route**: STRUCTUREE  
**Décideurs**: Brice Sodini (project lead & canon owner)  
**Liée à**: docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md § Gap-07  
**Liée à POC**: vide  
**Liée à ADR amont**: 0010 (IMPACT_LOG, fournit le log)

## Contexte

Quand un producteur modifie un contrat (API endpoint, DB schema, event schema), les consommateurs doivent être alertés pour se préparer à la migration. Vibebackbone dispose d'un outil `t-vbb-impact-analyzer` qui produit un rapport d'impact au moment de la modification. Mais **aucun mécanisme ne génère** une séquence de tâches coordonnées chez les consommateurs.

Conséquence : la discipline « mini refacto coordonné chez les consommateurs » est entièrement manuelle. Aucun checklist, aucune trace imposée, aucune notification outillée. Le passage à l'échelle (N services, N producteurs, N consommateurs) la rend impraticable.

Le constat est documenté dans `01_GAP_ANALYSIS.md` § Gap-07. Le gap est classé P1 car les consommateurs peuvent temporairement continuer (avec l'API cassée) mais cela crée une dette croissante.

## Décision

**Étendre `t-vbb-impact-analyzer` pour générer une séquence de tâches coordonnées chez les consommateurs lors d'un breaking change.**

### Comportement

Quand `t-vbb-impact-analyzer` détecte un breaking change (`Type: breaking` ou `Type: deprecation` dans `IMPACT_LOG.md`, cf. ADR-0010), il produit **en plus du rapport d'impact** une **liste de tâches par consumer** :

```yaml
# Output de t-vbb-impact-analyzer --co-evolution
producer: <service-slug>
breaking_change:
  contract: <endpoint or schema>
  from_version: <old>
  to_version: <new>
  detected_at: <YYYY-MM-DD>

tasks:
  - consumer: <service-A>
    type: <code_migration | dependency_bump | config_update | test_update>
    description: <human-readable>
    priority: <P0 | P1 | P2>
    blocking: <true | false>
    estimated_effort: <S | M | L>

  - consumer: <service-B>
    type: <code_migration>
    description: ...
    priority: ...
    blocking: ...
    estimated_effort: ...
```

### Stockage

Les tâches sont stockées dans `docs/IMPACT_LOG.md` (cf. ADR-0010) — section `## Pending co-evolution tasks` (append-only, status `pending` / `in_progress` / `done`).

### Outillage

- **Génération** : `t-vbb-impact-analyzer --co-evolution --write` (ajoute la tâche dans `IMPACT_LOG.md`).
- **Suivi** : `t-vbb-impact-analyzer --status` affiche les tâches pending par consumer.
- **Validation** : `vbb-multiservice-lint.py` (cf. ADR-0009) vérifie que les breaking changes ont des tâches associées (sinon warning).

### Qui fait quoi

- **Le producteur** lance `t-vbb-impact-analyzer --co-evolution --write` après avoir mergé son breaking change.
- **Le consumer** voit les tâches via `t-vbb-impact-analyzer --status` ou via le dashboard `vbb-status-dashboard.py`.
- **Le linter** valide que toute tâche pending est traitée dans un délai raisonnable (out of scope : durée).

## Conséquences

### Positives
- La co-évolution passe de « vigilance humaine » à « tâches outillées ».
- Le producteur a la garantie que son breaking change est tracé chez chaque consumer.
- Le consumer a une checklist claire (description + priorité + type).
- Le log cumulatif (`IMPACT_LOG.md`) devient **machine-actionable**.

### Négatives / coûts
- `t-vbb-impact-analyzer` doit être étendu (~100 lignes).
- Le producteur doit penser à lancer `--co-evolution --write` après chaque breaking change (discipline).
- La classification `type: <code_migration | dependency_bump | ...>` est un enum extensible.

### Neutres
- Aucun canon modifié.
- La skill `t-vbb-impact-log-update` (cf. ADR-0010, à créer) reste compatible : elle peut être utilisée pour ajouter des entrées manuelles complémentaires.

## Alternatives rejetées (≥ 2)

### Alternative A — Checklist manuelle partagée (Google Doc, Notion)
- **Description** : le producteur rédige un document de migration qu'il partage manuellement.
- **Pourquoi rejetée** : non structuré, non versionnable, non linter-checkable. Le framework perd la traçabilité.

### Alternative B — Notification email automatique
- **Description** : envoyer un email aux maintainers des consumers automatiquement.
- **Pourquoi rejetée** : ajoute une dépendance externe (SMTP), pollue les boîtes mail, ne crée pas de trace canonique dans le repo.

### Alternative C — Génération automatique par le linter sans intervention du producteur
- **Description** : `vbb-multiservice-lint` scanne périodiquement les contrats et génère les tâches automatiquement.
- **Pourquoi rejetée** : le linter ne sait pas classifier le type de tâche (code_migration vs config_update vs ...) sans contexte métier. Le producteur doit fournir cette info.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Le producteur oublie de lancer `--co-evolution --write` | moyenne | moyen | Le linter (ADR-0009) peut warning si breaking change sans tâche |
| La classification des tâches est trop rigide (mauvais `type`) | moyenne | faible | Enum extensible ; procédure d'extension documentée |
| Les tâches pending s'accumulent sans être traitées | moyenne | moyen | Dashboard `vbb-status-dashboard.py` les affiche ; reporting périodique (out of scope) |

## Hypothèses

- Le rapport d'impact de `t-vbb-impact-analyzer` est déjà précis (sinon les tâches sont incorrectes).
- Les consumers maintiennent leur `CONTRACTS_CONSUMED.md` à jour (cf. ADR-0007).
- L'enum `type` à 4 valeurs est suffisant pour les cas d'usage actuels.

## Références

- ADR amont : [`0010-impact-log-cumulative.md`](0010-impact-log-cumulative.md) (fournit `IMPACT_LOG.md`)
- ADR consommateur : [`0009-multiservice-lint-discipline.md`](0009-multiservice-lint-discipline.md) (validation pending tasks)
- Audits : [`docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md`](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) § Gap-07
- POCs : vide

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: PROCESS
reversible: true
depends_on:
  - "0010-impact-log-cumulative.md"
  - "0009-multiservice-lint-discipline.md"
blocks:
  - "t-vbb-impact-analyzer --co-evolution (implémentation, Run 13+)"
supersedes:
  - vide
verified_at: "2026-07-13T00:00:00Z"
verified_by: "human"
verified_method: "human-review"
```