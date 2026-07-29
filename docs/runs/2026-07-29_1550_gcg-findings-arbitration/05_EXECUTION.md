---
run_id: "2026-07-29_1550_gcg-findings-arbitration"
phase: "05_EXECUTION"
voie: "STRUCTUREE"
status: "PARTIAL"
kind: "GOVERNANCE_FINDINGS_ARBITRATION"
agent: "claude-opus-5 (Claude Code)"
started_at: "2026-07-29T13:50:00Z"
ended_at: "2026-07-29T14:45:00Z"
artifacts_produced:
  - "02_FINDINGS_REGISTER.md"
  - "03_DEPENDENCY_AND_ARBITRATION_MAP.md"
  - "04_INDEPENDENT_ARBITRATION_REVIEW.md"
  - "05_DECISIONS_REQUIRED.md"
  - "06_RESUMPTION_SEQUENCE.md"
---

# 05_EXECUTION — GCG-ARB-01

## 1. Mesures exécutées

Chaque affirmation du registre est adossée à l'une de ces mesures, ou à une
mesure de la revue explicitement citée comme telle.

| # | Mesure | Résultat | Sert |
|---|---|---|---|
| 1 | `vbb-governance-compat.py --json` | 164 total, 15 applicables, `2/15`, `historical_debt: 0`, verdict FAIL | baseline |
| 2 | boucle `git log --oneline` sur chaque `07_CLOSEOUT.md` | **14** closeouts à plus d'un commit | GCG-21 |
| 3 | `git ls-files 'docs/runs/*/07_CLOSEOUT.md' \| wc -l` | **157** — le dénominateur correct, pas 164 | GCG-21, RA-F-K |
| 4 | sonde Python : identité vs `started_at` sur les closeouts | 105 mesurés, **74** en désaccord (>1 min), max 22,1 h | GCG-10 |
| 5 | `grep -rn "enforcement_effective_from" docs/` | aucune occurrence hors du modèle | GCG-09 |
| 6 | `sed -n '104,106p' tools/vbb-governance-compat.py` | bornes `datetime` **sans `tzinfo`** | GCG-18 |
| 7 | `sed -n '168,215p' tools/vbb-governance-compat.py` | **`HISTORICAL_VALID` en ligne 176, `OVERCLAIM` en ligne 197** | **GCG-36** |
| 8 | `git log --format='%G?' \| sort \| uniq -c` | **243 `N`, 1 `E`** — aucune signature | **GCG-01, GCG-02, D1, D2** |
| 9 | `grep -ci harvest` sur les 9 closeouts de GCG-28 | le mot n'apparaît qu'en clé de frontmatter dans tous | GCG-28 |
| 10 | lecture de `tests/test_corpus_mandatory.py` §`_confirmed_findings` | l'obligation se déclenche sur un bloc adverse de closeout | GCG-25 |
| 11 | `vbb-gate-check.py <run_dir>` | `CAN_CODE_START: False`, `MISSING_POC` | §3 |

## 2. La revue indépendante et ce qu'elle a coûté à l'arbitrage

Subagent `a2f715163e55cc42e`, contexte isolé, dépôt en lecture seule, mandat non
orienté. **Onze constats, aucun écarté sur les faits.** J'ai re-vérifié
moi-même les six qui portent contre mon travail — mesures 3, 7, 8, 9 ci-dessus,
plus la lecture croisée de `03` §3.6 et de `03` §7.

Ce qu'elle a changé, en substance et non en forme :

1. **Une quatrième voie de blanchiment** (GCG-36), que ni moi ni la première
   revue n'avions vue, et qui vise la seule catégorie que le modèle déclare
   non migrable. Vérifiée à la source : le commentaire du code, deux lignes
   au-dessus, affirme précisément ce que l'ordre des branches rend faux.
2. **Mes recommandations D1 et D2 étaient des réparations défensives.** Elles
   détectent les contre-exemples connus sans établir la propriété, dans un dépôt
   où 243 commits sur 244 ne sont pas signés. J'appliquais le test
   déclaré-vs-établi aux constats et pas à mes propres remèdes.
3. **Ma correction de GCG-22 était fausse dans le sens de la surestimation** —
   le mode d'échec exact que le constat reproche au modèle.
4. **La divergence V3 était une erreur de mesure**, résoluble par une commande,
   que j'avais figée en désaccord épistémique.
5. **Le chiffre « 5/8 » de duplication était faux**, et il portait
   l'ordonnancement D4 → D1/D2 ainsi que le second pilier du verdict.
6. **Trois conditions d'arrêt sur dix étaient infalsifiables ou déjà remplies.**

Toutes les corrections sont appliquées. **Aucun énoncé réfuté n'a été effacé** :
chaque section réécrite porte en citation ce qu'elle disait et qui l'a réfutée
(contrainte C7).

## 3. Gate d'autorisation d'implémentation

`vbb-gate-check.py` retourne `CAN_CODE_START: False` (`MISSING_POC`). Le run ne
porte pas de POC et **n'écrit aucun code**. La Critical Rule 11 est donc honorée
par abstention, non par dérogation. C'est la différence avec la déviation `G9`
du run `1050`, où du code avait été touché avec le même verdict de gate.

Vérification : `git status --short` ne montre que `docs/runs/2026-07-29_1550_*/`.
`tools/`, `tests/` et `docs/REFERENCE/` sont inchangés.

## 4. Écart déclaré — GCG-36 n'est épinglé par aucun corpus

GCG-36 est né dans ce run, il est `CONFIRMED`, et il est **P0**. L'obligation de
corpus (`ADVERSARIAL_ASSURANCE` §9 destination 6) se déclenche sur les findings
`CONFIRMED` déclarés dans le bloc `adversarial:` d'un closeout. Trois issues :

| Issue | Verdict |
|---|---|
| Déclarer GCG-36 dans le bloc adverse et écrire `CORPUS-GCG-36.py` | **refusé** — C3 interdit d'écrire du code, et cette contrainte vient de la demande, pas de ma reformulation. Le run `1130` a pris l'issue inverse et l'a payée d'une violation déclarée (`A5`) |
| Rétrograder la confiance en `PLAUSIBLE` pour désamorcer l'obligation | **refusé** — c'est littéralement « rétrograder un niveau pour obtenir le vert », interdit par la contrainte permanente et par C4 |
| **Déclarer `findings: []`, enregistrer le constat au registre, et déclarer le conflit** | **retenu** |

Le bloc adverse de ce run porte `findings: []` parce que **ce run ne conduit
aucune campagne** : il arbitre des constats produits ailleurs, et GCG-36 lui a
été apporté par une revue, non par une attaque de ce run. Le registre est le
porteur durable de GCG-36.

**Ce que cet écart révèle est le constat GCG-25 s'appliquant à lui-même.** Un
constat produit hors campagne n'a pas de porteur épinglé ; le seul moyen de
l'épingler force à écrire du code ; et une contrainte de périmètre légitime
suffit à laisser un P0 sans verrou. Les deux faces sont désormais instanciées :
le run `1130` ne pouvait pas y échapper, ce run ne peut pas y accéder.
**La décision D8 n'est plus théorique.**

## 5. Contraintes d'intake — vérification

| Contrainte | Vérification |
|---|---|
| C1 modèle en lecture seule | ✅ `docs/REFERENCE/governance-compatibility-model.md` inchangé |
| C2 aucun nouveau concept ajouté au modèle | ✅ le registre classe, il n'invente pas de catégorie ni d'invariant |
| C3 aucun correctif de code | ✅ `tools/`, `tests/`, `scripts/` inchangés ; six corrections identifiées et **non appliquées** (`03` §4.2) |
| C4 aucun finding rétrogradé | ✅ GCG-28 **monte** de `PLAUSIBLE` à `CONFIRMED` ; aucun ne descend |
| C5 aucun statut sans preuve dérivable | ✅ GCG-35 reste `INFERRED`, GCG-34 reste `PLAUSIBLE`, GCG-28 ne monte que sur le **fait** |
| C6 aucune prétention à A2 strict | ✅ déclaré au closeout ; même famille de LLM pour les deux revues |
| C7 divergences visibles | ✅ V1, V2 et V3-résolue en `03` §6 ; W1 et W2 en `04` §4 |
| C8 CI rouge non blanchie | ✅ `vbb-governance-compat.py` reste `2/15`, exit 2. GCG-36 **augmentera** le nombre de bloquants une fois réparé |
| C9 aucun run de la séquence ouvert | ✅ `docs/runs/` ne contient aucun des runs proposés |

## 6. Vérification finale

Voir `07_CLOSEOUT.md` §Vérification P.R2. Le run ne modifie aucun code, donc les
vérifications de qualité statique portent sur un arbre inchangé ; elles sont
exécutées quand même, parce que le closeout d'une voie STRUCTUREE les exige.
