---
run_id: "2026-07-29_1021_adversarial-gate-population"
phase: "05_EXECUTION"
voie: "STRUCTUREE"
status: "PARTIAL"
agent: "claude-opus-5 (Claude Code)"
started_at: "2026-07-29T08:21:00Z"
ended_at: "2026-07-29T09:40:00Z"
artifacts_produced:
  - "tools/vbb-governance-compat.py"
  - "tests/test_governance_compat_gate.py"
---

# 05_EXECUTION — GATE-POPULATION-01

## 1. Séquence exécutée

| # | Étape | Résultat |
|---|---|---|
| 1 | `vbb-gate-check.py` avant tout code | `CAN_CODE_START: False` — `MISSING_POC` |
| 2 | POC exécuté (agrégation post-cutoff, aucun outil modifié) | `exit 2`, 10 non conformes |
| 3 | `vbb-gate-check.py` après POC | `CAN_CODE_START: True` |
| 4 | Matrice de disposition, 10 runs | `status: PROPOSED` |
| 5 | Proposition de canon GCG | `status: PROPOSED` |
| 6 | `tools/vbb-governance-compat.py` | `exit 2`, 10 bloquants |
| 7 | Mutation de la règle anti-blanchiment | test rouge, comportement confirmé |
| 8 | Suite complète | 432 passed, 1 skipped |

Le gate ADR+POC a refusé le démarrage du code au premier appel. Le POC a été
**exécuté**, pas rédigé après coup : sa sortie littérale est celle de la commande,
et elle est antérieure à la première ligne de `vbb-governance-compat.py`.

## 2. Preuve négative — la règle anti-blanchiment peut échouer

La règle qui empêche le ledger de blanchir un défaut actuel a été mutée hors
dépôt : lecture du ledger **avant** la borne d'existence de l'outil.

```
-  CURRENT_NONCOMPLIANCE
+  HISTORICAL_NONCOMPLIANCE
FAILED tests/test_governance_compat_gate.py::test_ledger_cannot_launder_a_post_enforcement_run
1 failed, 5 passed
```

La mutation produit exactement le symptôme de blanchiment : une entrée de ledger
suffit à déclasser un défaut actuel en dette historique. Restauration : 6 passed.

Ce n'est pas une formalité. C'est la seule propriété qui distingue GCG d'un
mécanisme d'auto-absolution : sans elle, chaque défaut se règle en ajoutant une
ligne dans un tableau.

## 3. Ce que la mesure a produit

```
current conformance : 2/12
historical debt     : 0 registered
certification       : NOT_DERIVABLE_FROM_THIS_GATE
verdict             : FAIL  (exit 2)
```

Répartition des 10 bloquants : 4 `UNKNOWN` (antérieurs à l'outil, sans
disposition arbitrée), 5 `CURRENT_NONCOMPLIANCE`, 1 `OVERCLAIM`.

L'`OVERCLAIM` a été isolé **mécaniquement**, sans que la règle ait été écrite en
visant ce run : `2026-07-30_0500_final-publication-of-v1.1-certification` déclare
`adversarial_status: PASS_ADVERSARIAL` sans bloc validable.

## 4. Findings découverts pendant l'exécution

### `G7` (P2) — le hook pre-commit ment sur ce qu'il applique

`scripts/hooks/pre-commit-framework-gate` §P0-2 annonce *« validating plan
sections »* et affiche en cas d'échec *« 04_PLAN.md has missing/empty/placeholder
sections »*. Il gate en réalité sur le **code de sortie complet** de
`vbb-loop-closure-check.py --strict --validate-plan`, lequel inclut la présence
de `05_EXECUTION.md` et `07_CLOSEOUT.md`.

Conséquence observée sur ce run : `04_PLAN.md` passait `✓ plan sections` et
`✓ 04_PLAN.md`, le commit était refusé quand même, avec un message désignant une
cause fausse. Un run STRUCTUREE en cours ne peut pas être committé sans être
clos, ou sans `--no-verify`.

C'est la même forme de défaut que celle traitée par ce run : une surface qui
affirme mesurer une chose et en mesure une autre. Non corrigé ici — hors périmètre,
et corriger un hook pendant qu'on l'utilise mérite son propre run.

### `G8` (P3) — `--validate-plan` exige `ended_at` sur un plan de run ouvert

Le schéma impose `ended_at` dans le frontmatter de `04_PLAN.md`. Un plan est
écrit avant l'exécution ; sa date de fin n'existe pas. Renseigné à `null`.

## 5. Écarts au plan

- **ADR 0052 non écrit** — délibéré, motivé dans `04_PLAN.md`. Un ADR `accepted`
  face à une proposition de canon `PROPOSED` recréerait la vérité parallèle que
  le run précédent a corrigée.
- **Ledger non créé** — bloqué par l'arbitrage. Créer un ledger vide donnerait un
  contenant sans décision et inviterait à le remplir sans arbitrage.
- **CI non câblée** — délibéré. Le gate est rouge sur un état qu'aucun run ne peut
  résoudre seul.

## 6. Contraintes d'intake — vérification

| Contrainte | Vérification |
|---|---|
| §6.1 aucun bloc adverse écrit avant arrêt de la matrice | ✅ `git diff` : aucun `07_CLOSEOUT.md` existant modifié |
| §6.2 reconstructibilité conditionnée aux artefacts contemporains | ✅ aucune reconstruction tentée |
| §6.3 aucune rétrogradation de niveau | ✅ matrice §4 : aucune proposée |
| §6.4 le vert du gate ne vaut pas certification | ✅ `NOT_DERIVABLE_FROM_THIS_GATE`, pinné par test |
