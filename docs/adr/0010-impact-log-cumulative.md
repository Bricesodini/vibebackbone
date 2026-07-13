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

# ADR — 0010-impact-log-cumulative

**Status**: ACCEPTED  
**Date**: 2026-07-13  
**Route**: STRUCTUREE  
**Décideurs**: Brice Sodini (project lead & canon owner)  
**Liée à**: docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md § Gap-06  
**Liée à POC**: vide  
**Liée à ADR amont**: 0007 (CONTRACTS_CONSUMED, déclenche les entrées)

## Contexte

Quand un producteur modifie un contrat (API endpoint, DB schema, event schema), les consommateurs doivent être alertés pour se préparer à la migration. Vibebackbone dispose d'un outil `t-vbb-impact-analyzer` qui produit un rapport d'impact **au moment de la modification**, mais **aucun mécanisme ne persiste cet impact** pour analyse a posteriori.

Conséquence : impossible de répondre à des questions comme « qui a été impacté par le breaking change de l'endpoint X il y a 6 mois ? » ou « combien de breaking changes ce service a-t-il publiés en 2026 ? ». L'historique des impacts est perdu après chaque session.

Le constat est documenté dans `01_GAP_ANALYSIS.md` § Gap-06 : aucun fichier du framework ne maintient un log cumulatif des impacts. Le pipeline `t-vbb-impact-analyzer` produit un rapport mais ne le persiste pas.

## Décision

**Créer un fichier canonique `docs/IMPACT_LOG.md` (par projet), maintenu cumulativement, qui trace chaque changement de contrat (own ou consumed) avec une structure append-only.**

### Structure du fichier

```markdown
---
context_role: impact-log
phase: transverse
status: active
schema_version: "1.0"
---

# IMPACT_LOG — <project_slug>

> **Owner** : <équipe / maintainer>
> **First entry** : <YYYY-MM-DD>
> **Last entry** : <YYYY-MM-DD>
> **Total entries** : <count>

## Entries (append-only — newest first)

| Date | Type | Contrat | Avant | Après | Services impactés | Lien run |
|------|------|---------|-------|-------|-------------------|----------|
| 2026-07-15 | `breaking` | `GET /v1/users` | `v1` | `v2` | `studio-auth`, `studio-orders` | [run-2026-07-15-…](../runs/2026-07-15_…/) |
| 2026-07-10 | `additive` | `POST /v1/users/bulk` | — | `v2.1` | (none — new endpoint) | [run-2026-07-10-…](../runs/2026-07-10_…/) |
| 2026-07-01 | `deprecation` | `GET /v0/users` | — | `deprecated` | `studio-reports` (still using v0) | [run-2026-07-01-…](../runs/2026-07-01_…/) |
| 2026-06-25 | `consumed_change` | `event UserCreated` (from `studio-auth`) | `schema-v3` | `schema-v4` | `studio-notifications` | [run-2026-06-25-…](../runs/2026-06-25_…/) |

## Légende

- **Type** :
  - `breaking` — changement incompatible (consumer doit migrer)
  - `additive` — nouveau endpoint/champ (consumer peut rester sur l'ancien)
  - `deprecation` — endpoint marqué deprecated (consumer doit planifier migration)
  - `fix` — bug fix (transparent pour consumer)
  - `consumed_change` — changement d'un contrat consommé (impact = s'adapter)

## Process d'entrée

1. À chaque merge d'un changement de contrat : ajouter une ligne (ne **jamais** éditer rétroactivement).
2. À chaque PR de breaking change : l'entrée est obligatoire avant merge (vérifié par linter, cf. ADR-0009).
3. L'entrée est remplie via la skill `t-vbb-impact-log-update` (formulaire guidé).

## Références

Les contrats listés sont définis dans `docs/CONTRACTS_CONSUMED.md` (cf. ADR-0007) et `CONTRACTS_PROVIDED.md` (à définir, symétrique).
```

### Skill `t-vbb-impact-log-update` (à créer — Run 10+)

Facilite l'entrée en posant des questions structurées :
- Date du changement ?
- Type (breaking/additive/deprecation/fix/consumed_change) ?
- Contrat (avec autocompletion depuis `CONTRACTS_CONSUMED.md` / `CONTRACTS_PROVIDED.md`) ?
- Version avant / après ?
- Services impactés (avec autocompletion depuis `CONTRACTS_CONSUMED.md`) ?
- Lien vers le run qui a produit le changement ?

La skill formate la ligne Markdown et l'insère en haut du tableau.

### Garanties append-only

- **Pas d'édition rétroactive** : le format Markdown (table) interdit naturellement l'édition ; les outils d'analyse (lint, dashboard) traitent les entrées comme immuables.
- **Corrections** : ajoutent une nouvelle entrée avec note `corrects previous entry` plutôt que d'éditer l'ancienne.

## Conséquences

### Positives
- L'historique des impacts est préservable et analysable a posteriori.
- Les métriques de discipline (« combien de breaking changes par mois ? ») deviennent dérivables.
- L'alignement avec `CONTRACTS_CONSUMED.md` (ADR-0007) permet la cross-référence automatique.
- Le log sert de **trace vérifiable** en cas d'incident.

### Négatives / coûts
- Le fichier croît indéfiniment (mitigation : rotation par année via un script out of scope).
- Chaque PR de contrat doit ajouter une entrée (discipline, mais pas bloquant par défaut — ADR-0009 mode warning).
- L'automatisation (via skill `t-vbb-impact-log-update`) est différée à un Run futur.

### Neutres
- `t-vbb-impact-analyzer` n'est pas modifié (il produit le rapport à la volée ; `IMPACT_LOG.md` est la persistance).
- Le log n'est pas versionné par défaut (mais comme tout fichier `docs/`, il peut être versionné projet par projet).

## Alternatives rejetées (≥ 2)

### Alternative A — Persister dans `t-vbb-impact-analyzer` (base de données locale)
- **Description** : le tool persiste ses rapports dans un format binaire local (sqlite, jsonl).
- **Pourquoi rejetée** : non lisible humain, non versionnable, non diffable en PR. Un fichier Markdown est plus adapté à la discipline « tout est dans `docs/` ».

### Alternative B — Un fichier par impact (e.g. `docs/impacts/2026-07-15-*.md`)
- **Description** : un fichier par entrée d'impact, plutôt qu'un fichier cumulatif.
- **Pourquoi rejetée** : dispersion de l'historique. Le tri chronologique devient fastidieux. Une table cumulatives est plus lisible.

### Alternative C — Stocker dans le changelog git (`git log --grep`)
- **Description** : convention de message de commit pour tracer les impacts.
- **Pourquoi rejetée** : non structuré, non queryable directement, dépend de la convention de commit. Un fichier canonique est plus robuste.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Le log n'est pas maintenu | moyenne | moyen | Linter (ADR-0009) vérifie la présence d'au moins une entrée si contrats consommés existent |
| Le log devient trop volumineux | faible | faible | Rotation par année (out of scope) ; la table reste queryable |
| Incohérence entre `IMPACT_LOG.md` et `CONTRACTS_CONSUMED.md` | moyenne | faible | Cross-référence manuelle encouragée ; outil futur peut valider la cohérence |

## Hypothèses

- Le format table Markdown reste lisible jusqu'à ~1000 entrées (~10 ans à raison de 100/an).
- Le format `schema_version` dans le frontmatter permet l'évolution future du schéma.
- La skill `t-vbb-impact-log-update` est créée dans un Run futur (Run 10+).

## Références

- ADR amont : [`0007-contracts-consumed-canonical-file.md`](0007-contracts-consumed-canonical-file.md)
- ADR consommateur : [`0009-multiservice-lint-discipline.md`](0009-multiservice-lint-discipline.md)
- Outil lié : `t-vbb-impact-analyzer` (existant, rapport à la volée)
- Audits : [`docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md`](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) § Gap-06
- POCs : vide

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: DURABLE_CONVENTION
reversible: true
depends_on:
  - "0007-contracts-consumed-canonical-file.md"
blocks:
  - "t-vbb-impact-log-update (skill création, Run 10+)"
  - "0009-multiservice-lint-discipline.md (validation IMPACT_LOG)"
supersedes:
  - vide
verified_at: "2026-07-13T00:00:00Z"
verified_by: "human"
verified_method: "human-review"
```