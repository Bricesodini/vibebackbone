# 05_PATCH_SUMMARY — Run 12 Multi-service ADR restants

**Date** : 2026-07-13
**Route** : STRUCTURED
**Fichiers créés** : 4 ADR + index + 3 artefacts
**Lignes ajoutées** : ~600

---

## 4 ADR créés

### ADR-0018 — Multi-repo support (Gap-08, P0)

**Décision** : `docs/MULTIREPO.yaml` (par projet) déclare l'appartenance à un système multi-repo (system_name, repos[], tools[]).

**Justification** : sans déclaration, impossible de générer le graphe global (Gap-13) ou de traverser les frontières d'outils.

### ADR-0019 — Première extension concrète (Gap-12, P1)

**Décision** : créer `docs/extensions/multi-service-database-per-service/` (premier cas concret d'extension selon ADR-0014).

**Justification** : le mécanisme d'extension (ADR-0014) sans premier cas concret reste théorique. Cette extension sert de POC et de template.

### ADR-0020 — Graphe inter-services (Gap-13, P0)

**Décision** : `tools/vbb-multiservice-graph.py` consomme `CONTRACTS_CONSUMED.md` + `MULTIREPO.yaml` + `CONTRACTS_PROVIDED.md` (à venir), génère 4 modes : `--text`, `--dot`, `--json`, `--check-cycle`.

**Justification** : visualisation outillée + détection de cycles (intégrable en CI).

### ADR-0021 — Gate CI enforcement (Gap-15, P0)

**Décision** : `scripts/vbb-ci-local.sh` exécute en séquence les 4 vérifications canoniques (contract-lint, multiservice-lint --strict, multiservice-graph --check-cycle, architecture agents --check). Snippet copy-paste pour GitHub Actions / GitLab CI.

**Justification** : sans gate CI, la discipline multi-service n'est pas enforceable.

---

## Couverture Phase 2 design (après Run 12)

| Run | ADR créés | Gaps couverts | Cumul |
|-----|-----------|---------------|-------|
| Run 8 | 4 | Gap-01/02/05/14 | 4 |
| Run 9 | 3 | Gap-04/06/10 | 7 |
| Run 11 | 4 | Gap-03/07/09/11 | 11 |
| **Run 12** | **4** | **Gap-08/12/13/15** | **15** |
| Restant | 3 P2 | Gap-16/17/18 | 18 |

**Couverture Phase 2 design = 15/18 gaps** (83%).

---

## Vérifications P.R2

- ✅ Lint : 0/0
- ✅ 4 ADR créés avec ≥ 2 alternatives chacun
- ✅ Index ADR mis à jour
- ✅ Aucun canon / outil / template touché
- ✅ Pre-merge gate PASS

---

## Récapitulatif

| Métrique | Valeur |
|----------|--------|
| Fichiers créés | 5 (4 ADR + index) |
| Lignes ajoutées | ~600 |
| Canon touché | 0 |
| ADR créés | 4 (0018, 0019, 0020, 0021) |
| ADR status initial | ACCEPTED |
| Findings P0 résolus (design) | Gap-08, Gap-13, Gap-15 |
| Findings P1 résolus (design) | Gap-12 |
| Cumul ADR | 15/18 gaps |