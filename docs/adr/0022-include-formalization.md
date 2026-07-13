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

# ADR — 0022-include-formalization

**Status**: ACCEPTED  
**Date**: 2026-07-13  
**Route**: STRUCTUREE  
**Décideurs**: Brice Sodini (project lead & canon owner)  
**Liée à**: docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md § Gap-16  
**Liée à POC**: vide

## Contexte

Les fichiers d'entry-point (`AGENTS.md` racine, `distributions/claude/CLAUDE.md`, `distributions/pi/SYSTEM.md`) utilisent une convention `@include` ad-hoc pour référencer d'autres fichiers :

```
@AGENTS.md
@SYSTEM.md
@docs/PILOTAGE.md
```

Cette convention est **documentaire** (lisible par certains agents), mais aucun parseur canonique ne valide la résolution. Si la cible est renommée ou supprimée, le lien casse silencieusement. Aucun warning CI, aucune vérification au build.

## Décision

**Formaliser la grammaire `@include` et créer `tools/vbb-include-lint.py` qui parse les entry-point files et valide les directives.**

### Grammaire canonique

```
@include <path-relative-to-current-file>
@include <path> [optional: <description>]
```

Exemples valides :

```
@include docs/PILOTAGE.md
@include AGENTS.md
@include ../shared/CONVENTIONS.md            # cross-directory
@include docs/AGENTIC_RUN_PROTOCOL.md          # canonical run protocol
@include docs/REFERENCE/pre-merge-gate.md      # P.R2 canonical reference
```

### Comportement du linter

`tools/vbb-include-lint.py` parse les fichiers entry-point et vérifie :

1. **Cible existe** : chaque `@include <path>` doit pointer vers un fichier réel.
2. **Pas de cycle** : le graphe d'inclusion est acyclique (A inclut B inclut A → erreur).
3. **Pas de `@generated`** : un fichier `@generated` ne peut pas être inclus (car son contenu change à chaque regen).
4. **Cohérence** : si un fichier est référencé par 3 entry-points, c'est suspect (warning, pas erreur).

### Modes

- Par défaut : warning console, exit 0.
- `--strict` : warning → error, exit 2.
- `--json` : sortie machine-readable.

## Conséquences

### Positives
- Les `@include` cassés sont détectés avant merge.
- Le graphe d'inclusion est visible et auditable.
- Cohérence avec le pattern des autres linters vbb-* (cf. ADR-0009, ADR-0015).

### Négatives / coûts
- Nouvel outil (~100 lignes Python).
- Les `@include` actuels (3 dans `CLAUDE.md`, 1 dans `AGENTS.md`) doivent être validés.

### Neutres
- Aucun canon direct modifié (le format `@include` reste ad-hoc dans les fichiers, juste formalisé par le linter).

## Alternatives rejetées (≥ 2)

### Alternative A — Conserver la convention ad-hoc, pas de linter
- **Description** : statu quo. Convention documentaire, pas de validation.
- **Pourquoi rejetée** : drift silencieux possible. Impossible de détecter les liens cassés.

### Alternative B — Convertir `@include` en liens Markdown explicites
- **Description** : remplacer `@AGENTS.md` par `[Voir AGENTS.md](AGENTS.md)`.
- **Pourquoi rejetée** : changement de format massif, incompatible avec les agents qui reconnaissent `@include` (Claude notamment).

### Alternative C — Pre-commit hook qui résout et copie les inclusions
- **Description** : au lieu de valider, le hook copie le contenu des inclusions dans un fichier `_expanded.md`.
- **Pourquoi rejetée** : complexifie le pipeline, modifie le comportement des fichiers. La validation est plus légère.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Un `@include` devient cyclique après refacto | faible | moyen | Détection par DFS dans le linter |
| Une cible est déplacée sans mise à jour des `@include` | moyenne | faible | Warning explicite avec chemin cassé |
| L'extension casse les agents qui ne reconnaissent pas la grammaire formelle | faible | faible | La grammaire est rétrocompatible (les agents actuels reconnaissent `@<path>` simple) |

## Hypothèses

- Les `@include` actuels respectent la grammaire (à valider empiriquement).
- Les agents comprennent un `@include` même avec description optionnelle (ignoré si non reconnu).

## Références

- Audits : [`docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md`](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) § Gap-16
- ADR lié : [`0012-codegen-agents-claudemd.md`](0012-codegen-agents-claudemd.md) (le codegen doit respecter la grammaire)
- POCs : vide

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: DURABLE_CONVENTION
reversible: true
depends_on:
  - vide
blocks:
  - "tools/vbb-include-lint.py (implémentation, Run 14+)"
  - "0012-codegen-agents-claudemd.md (le codegen émet des @include conformes)"
supersedes:
  - vide
verified_at: "2026-07-13T00:00:00Z"
verified_by: "human"
verified_method: "human-review"
```