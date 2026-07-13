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

# ADR — 0024-snapshot-to-log

**Status**: ACCEPTED  
**Date**: 2026-07-13  
**Route**: STRUCTUREE  
**Décideurs**: Brice Sodini (project lead & canon owner)  
**Liée à**: docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md § Gap-18  
**Liée à POC**: vide  
**Liée à ADR amont**: 0010 (IMPACT_LOG, cible de la projection)

## Contexte

`skills/t-vbb-impact-analyzer/SKILL.md` ligne 124 produit un snapshot timestampé `docs/audits/impact-analysis-{YYYYMMDD-HHMM}.md` à chaque exécution. Ces snapshots sont isolés — aucune vue longitudinale.

Parallèlement, `docs/IMPACT_LOG.md` (cf. ADR-0010) est conçu comme un log cumulatif, append-only, qui trace les changements de contrat dans la durée.

Le gap : comment **alimenter** `IMPACT_LOG.md` depuis les snapshots existants ? Manuellement ? Par un script ? Aucune politique définie.

Conséquence : les snapshots s'accumulent (`docs/audits/impact-analysis-*.md` × N) sans consolidation. L'historique des impacts est distribué sur plusieurs fichiers au lieu d'être centralisé.

## Décision

**Étendre `t-vbb-impact-analyzer` avec un mode `--project-to-log` qui projette les findings d'un snapshot vers `docs/IMPACT_LOG.md`.**

### Comportement

```bash
python t-vbb-impact-analyzer --project-to-log <snapshot-path> [--type <breaking|additive|deprecation|fix|consumed_change>]
```

1. Lit le snapshot (`docs/audits/impact-analysis-{YYYYMMDD-HHMM}.md`).
2. Extrait les findings (services impactés, type de changement, version avant/après).
3. Génère une ligne dans `IMPACT_LOG.md` au format canonique (cf. ADR-0010) :
   - Date : date du snapshot
   - Type : inféré du snapshot (ou `--type` explicite)
   - Contrat : endpoint ou schéma identifié
   - Avant/Après : extraits du snapshot si disponibles
   - Services impactés : liste
   - Lien run : lien vers le snapshot
4. Ajoute la ligne en haut du tableau `IMPACT_LOG.md` (append-only, newest first).

### Heuristique de typage

| Snapshot finding | Type inféré |
|------------------|-------------|
| Endpoint removed | `breaking` |
| Endpoint added | `additive` |
| Endpoint marked deprecated | `deprecation` |
| Field renamed | `breaking` |
| New optional field | `additive` |
| Behavior unchanged | `fix` |
| Provider version bump | `consumed_change` |

Si l'heuristique hésite → warning, demande confirmation humaine.

### Idempotence

Si le snapshot a déjà été projeté (idempotence key = `snapshot path + date`), la commande est silencieuse (no-op). Évite les doublons.

## Conséquences

### Positives
- Les snapshots deviennent **utiles** : ils alimentent le log cumulatif.
- L'historique des impacts est centralisé dans `IMPACT_LOG.md`.
- Le linter multi-service (ADR-0009, Gap-04) peut valider la fraîcheur du log.

### Négatives / coûts
- `t-vbb-impact-analyzer` doit être étendu (~80 lignes).
- L'heuristique de typage peut se tromper (warning + confirmation).
- L'idempotence demande un mécanisme de tracking (hash du snapshot).

### Neutres
- Les snapshots restent en `docs/audits/` (archivage historique).
- `IMPACT_LOG.md` reste append-only (cf. ADR-0010).

## Alternatives rejetées (≥ 2)

### Alternative A — Supprimer les snapshots, garder uniquement `IMPACT_LOG.md`
- **Description** : remplacer les snapshots par le log cumulatif seul.
- **Pourquoi rejetée** : perte d'historique détaillé (les snapshots contiennent les findings complets, le log est résumé).

### Alternative B — Snapshot ET log cumulatif en parallèle, jamais synchronisés
- **Description** : statu quo étendu — les deux vivent en parallèle, manuellement.
- **Pourquoi rejetée** : drift entre les deux ; double source de vérité.

### Alternative C — Mode `--project-to-log` automatique à chaque exécution de `t-vbb-impact-analyzer`
- **Description** : projeter automatiquement après chaque snapshot.
- **Pourquoi rejetée** : pas de relecture humaine possible ; le snapshot contient des findings bruts qui peuvent être mal typés.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| L'heuristique de typage est trop agressive (mauvais type) | moyenne | faible | Warning + confirmation humaine |
| Snapshot mal formé → projection échoue | moyenne | faible | Message d'erreur explicite |
| Idempotence cassée (doublons) | faible | faible | Hash du snapshot + check avant insertion |

## Hypothèses

- Le format des snapshots `t-vbb-impact-analyzer` est stable (peut être parsé).
- L'heuristique de typage est suffisamment précise pour les cas courants.
- Les snapshots existants peuvent être rétro-projetés (backfill manuel possible).

## Références

- ADR amont : [`0010-impact-log-cumulative.md`](0010-impact-log-cumulative.md) (cible du log)
- Audits : [`docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md`](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) § Gap-18
- Skill lié : `skills/t-vbb-impact-analyzer/SKILL.md`
- POCs : vide

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: PROCESS
reversible: true
depends_on:
  - "0010-impact-log-cumulative.md"
blocks:
  - "t-vbb-impact-analyzer extension (Run 14+)"
supersedes:
  - vide
verified_at: "2026-07-13T00:00:00Z"
verified_by: "human"
verified_method: "human-review"
```