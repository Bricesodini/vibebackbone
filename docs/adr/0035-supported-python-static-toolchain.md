# ADR — 0035-supported-python-static-toolchain

**Status**: ACCEPTED
**Date**: 2026-07-14
**Route**: STRUCTUREE
**Décideurs**: Brice (`Go`, 2026-07-14), Codex (formalisation)
**Liée à**: QOA-007, GMA-005
**Liée à POC**: `docs/runs/2026-07-14_1411_static-toolchain/POC.md`

## Contexte

Le dépôt ne possède ni configuration Python statique canonique ni versions de
développement reproductibles. Ruff et mypy sont exercés localement, tandis que
Pyright est absent et sans besoin distinct. La baseline mesurée reste non nulle,
donc une promotion immédiate en gate produirait un échec permanent.

## Décision

Vibebackbone supporte Ruff 0.13.1 pour le lint et le formatage, et mypy 2.1.0
pour le typage de `tools/`, sur Python 3.11. La configuration partagée vit dans
`pyproject.toml` et les versions dans `requirements-dev.txt`. Pyright reste hors
du contrat supporté. Les trois checks demeurent non bloquants jusqu'à ce que la
baseline atteigne zéro ; ils seront alors promus ensemble dans les CI locale et
distante par un run séparé.

## Conséquences

### Positives

- Résultats statiques reproductibles et une seule configuration active.
- Séparation claire entre mesure, nettoyage et promotion en gate.
- Pas de double maintenance de type checkers concurrents.

### Négatives / coûts

- Deux dépendances de développement supplémentaires.
- La configuration révèle explicitement une baseline temporairement rouge.

### Neutres

- P.R2 et les hooks existants restent inchangés pendant Wave 2.
- Les quatre distributions héritent de la convention Core sans adapter.

## Alternatives rejetées (≥ 2)

### Alternative A — Mypy et Pyright en parallèle

- **Description** : maintenir deux checkers de types sur le même périmètre.
- **Pourquoi rejetée** : aucun besoin distinct ne justifie les contradictions et
  le coût de maintenance supplémentaire.

### Alternative B — Gate immédiate sur baseline rouge

- **Description** : ajouter les checks à la CI avant nettoyage.
- **Pourquoi rejetée** : la CI deviendrait structurellement bloquée et perdrait
  sa valeur de signal.

### Alternative C — Defaults locaux sans versions

- **Description** : documenter seulement des commandes installées globalement.
- **Pourquoi rejetée** : les résultats dériveraient entre machines et runners.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| versions figées deviennent anciennes | moyenne | faible | upgrade dédiée avec nouvelle baseline |
| état non-gating persiste | moyenne | moyen | QOA-007 reste actif jusqu'à zéro + CI |
| exclusions cachent la dette | faible | fort | aucune exclusion de source ni ignore global |

## Hypothèses

- Python 3.11 reste la version supportée par la matrice CI.
- Ruff et mypy couvrent les besoins actuels ; un besoin Pyright distinct rouvrira
  la décision.

## Références

- Audit : `docs/audits/format-lint-20260714-1410.md`
- Plan : `docs/audits/intent-decomp-20260714-1355.md`
- POC : `docs/runs/2026-07-14_1411_static-toolchain/POC.md`

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: STACK
reversible: true
depends_on:
  - docs/audits/format-lint-20260714-1410.md
blocks:
  - READY Wave 3 static cleanup
supersedes: []
verified_at: "2026-07-14T12:11:00Z"
verified_by: "Brice + Codex"
verified_method: "explicit-human-approval + reproducible-baseline-poc"
```
