# Audit READ-ONLY — Phase 2 Run 1 (contractualisation primitives)

- **Date** : 2026-06-13
- **SHA audité** : `aae0514` (HEAD main, post-closeout)
- **SHA framework** : `27375d7` (commit Phase 2 Run 1)
- **Périmètre** : 9 fichiers (tools/, AGENTS.md, templates/, hook, tests, closeout, distribution README, skill mapper, gate-check)
- **Mode** : READ-ONLY strict (0 patch, 0 commit, 0 push)
- **Auteur** : Hermes (audit) sur demande de Brice

---

## 1. Synthèse exécutive

| | |
|---|---|
| **Scorecard** | **7.75 / 10** |
| **Verdict** | **GO conditionnel** — POC P0-4 d'abord + 1 régression test |
| **Métrique dette méthodologique** | 80% → 52% (-28 pts, -35%) |
| **Catégorie D (vraie invention)** | 0 / 10 modifications (zéro invention, conforme contrainte Brice) |
| **CI** | smoke + vbb-contracts verts sur SHA `aae0514` (databaseId 26872427163 + 26872427211) |
| **Tests** | 110 → 111 passed, 3 skipped |

Le chantier contractualise des primitives **existantes** (catégories A/B/C uniquement, zéro catégorie D). Les ajouts sont opt-in (3 nouveaux flags `--validate-*` OFF par défaut), rétrocompatibles avec les 5 runs historiques, et n'augmentent pas la surface d'erreur. La voie rapide (FAST/FAST-MINIMAL/FAST-ZERO) reste fluide (skip documenté, hook exit 0).

Le chantier **n'a pas rendu VBB bureaucratique** mais a densifié un fichier central (vbb-loop-closure-check.py : 448 → 877 lignes, +96%). La suite de tests (P0-1/P0-2/P0-3) protège contre la régression silencieuse. Un test supplémentaire a été ajouté le 2026-06-13 (audit risk #1) pour figer l'invariant "fixed-price" (voir §4).

---

## 2. Réponses aux 6 questions de l'audit

### Q1 — Aligné avec VBB léger ? (7.5/10)

**OUI avec bémol.** Les 3 nouveaux flags sont opt-in :

- `--validate-claims` (P0-1.1)
- `--validate-plan` (P0-2.1)
- `--validate-test-audit` (P0-3.1)

Aucun run historique n'est cassé (5 runs re-testés, 100% vert). Le hook pre-commit bloque opt-in via arguments CLI ; le mode par défaut reste la closure check traditionnelle (phases présentes). `AGENTS.md` §CANON §6 documente explicitement le skip pour `FAST-MINIMAL` et `FAST-ZERO`.

**Bémol** : vbb-loop-closure-check.py a presque doublé (448 → 877 lignes). Pas bureaucratique, mais **dense** — 4 helpers + 3 validators + 1 marker finder partagent le même module. Risque de "god script" si P0-4/P0-5-D ajoutent d'autres validators sans refactor. (Voir Risque #2.)

### Q2 — Faux positifs acceptables ? (7/10)

**OUI sous conditions** — 4 cas limites identifiés, 4 mitigations en place :

| Cas limite | Mitigation actuelle | Test couvrant |
|---|---|---|
| EVIDENCE_MARKER inline (même ligne que claim) | Regex `(?:^|\s)\b(?:Evidence|Preuve)\s*:` | `test_claims_coherent_passes` |
| claim hors section `Résultat` (Décisions) | Section filtering + "Volontairement non traité:" | `test_claims_coherent_passes` |
| plan sans analyse d'impact | Section "Analyse d'impact" obligatoire | `test_plan_complete_passes` |
| test surface = "no test surface" | Marker "## No test surface" | `test_test_audit_no_surface_marker_passes` |
| `fixed-price` adjectif (audit risk #1) | Regex demande `:` après `fixed` | **`test_claims_fixed_price_not_detected_as_bugfix`** *(ajouté 2026-06-13)* |

Le test `fixed-price` a été ajouté post-audit après discussion avec Brice. Il est **PASS** sans patch du regex : `CLAIM_VERB_RE` exige déjà `fixed:` (pas `fixed-price`).

### Q3 — FAST/FAST-MINIMAL fluides ? (9/10)

**OUI, point fort du chantier.** Mesures concrètes :

- Les 3 nouveaux checks sont **opt-in** (OFF par défaut).
- AGENTS.md §CANON §6 (ligne 118) documente le SKIP explicite :
  > "FAST-MINIMAL et FAST-ZERO sont exemptées : ces voies n'ont pas de 04_PLAN ni de 05_EXECUTION structurés."
- Le hook pre-commit-framework-gate lignes 78-82 exit 0 sur ces voies (pas de check claims/plan/test-audit).
- FAST (la voie rapide standard) **reste entièrement bloquante** comme avant (closure check traditionnelle).

Aucun run FAST n'a été ralenti. Aucune régression sur le triptyque P.R2 (arch/contract/loop-closure).

### Q4 — Closeouts lisibles ? (7/10)

**OUI mais dense.** Le closeout Phase 2 Run 1 fait **173 lignes** (cf. `docs/runs/2026-06-13_1400_phase-2-run-1-contractualisation/07_CLOSEOUT.md`). Structure :

- Header frontmatter canonique
- 1ère moitié : "Résultat" (5 tables Claim|Evidence|Status) + décisions
- 2ème moitié : dette méthodologique (%), métrique catégorielle, P.R2 verts, SHA, scope de "ce qui n'est PAS dans ce run"

C'est **exécutable** (un LLM peut le re-lire et comprendre quoi rollback) mais **pas skimmable**. Risque d'inflation sur P0-4/P0-5-D si la même densité est conservée. (Voir Risque #4.)

### Q5 — Core indépendant des distributions ? (10/10)

**OUI strict.** Vérifications :

- `tools/vbb-loop-closure-check.py` (Core) ne fait aucun `import` vers `distributions/`.
- `AGENTS.md` §13 (credentials gate) mentionne **explicitement** "distribution tools" :
  > "Sensible information MUST be redacted in source via distribution-level tools (see `distributions/hermes/bypass-lint/README.md`)."
- `distributions/hermes/bypass-lint/README.md` est la **seule** porte d'entrée credentials (avec `redact_secrets()`), Core ne duplique pas.
- La règle DISTRIBUTIONS.md §5 (Rule A — pas de Core → Distribution dépendance) est **respectée**.

Aucune dépendance circulaire, aucun chemin codé en dur, aucune obligation de checkout Distribution pour exécuter Core.

### Q6 — Prêt pour P0-4 (Review Matrix) ? (6/10)

**PARTIELLEMENT** — techniquement prêt, méthodologiquement besoin POC.

- **Techniquement** : le hook pre-commit est **déjà extensible** (3 blocks claims/plan/test-audit, pattern uniforme). Ajouter un block P0-4 review = copier le pattern, ~30 lignes.
- **Méthodologiquement** : P0-4 Review Matrix est **catégorie D** (vraie capacité nouvelle). Le POC est **obligatoire** avant exécution :
  - Matrice T1-T8 non encore testée sur runs historiques.
  - Calibration des seuils (accept/reject) non faite.
  - Risque de sur-ingénierie (matrice trop stricte → blocages, trop laxiste → coquille vide).

**Recommandation** : POC P0-4 = (1) matrice T1-T8 draft, (2) application rétro-active sur 3 runs historiques, (3) mesure faux positifs/négatifs, (4) décision GO/NO-GO/PIVOT. Durée estimée : 1-2 jours. (Voir §5 options.)

---

## 3. Scorecard

| Question | Score | Justification |
|---|---|---|
| Q1 — VBB léger ? | 7.5 | Opt-in rétrocompatible, mais loop-closure +96% LOC |
| Q2 — Faux positifs ? | 7.0 | 4 cas limites + 4 mitigs, test `fixed-price` ajouté post-audit |
| Q3 — FAST fluides ? | 9.0 | SKIP documenté + hook exit 0, point fort |
| Q4 — Closeouts lisibles ? | 7.0 | Exécutable mais dense, 173 lignes pour 10 modifs |
| Q5 — Core indépendant ? | 10.0 | DISTRIBUTIONS.md §5 respectée, aucun import Core→Distrib |
| Q6 — Prêt P0-4 ? | 6.0 | Techniquement oui, méthodologiquement POC obligatoire |
| **Moyenne** | **7.75** | GO conditionnel |

---

## 4. Risques identifiés (5 max)

### Risque #1 — Faux positif "fixed-price" comme claim bugfix ✅ **RÉSOLU post-audit**

**Description** : un closeout contenant "- fixed-price contract signed" aurait pu être détecté comme un claim de type `fixed:`.

**Vérification** : `CLAIM_VERB_RE` ligne 128 :
```python
r"^\s*-\s+(fixed|passes|repaired|aligned|closed|merged)\s*:"
```
Le `\s*:` après `(fixed|...)` exige un `:` immédiat. "fixed-price" a un `-` après, pas un `:` — **pas de match**.

**Mitigation** : test `test_claims_fixed_price_not_detected_as_bugfix` ajouté dans `tests/test_loop_closure_p2.py` (lignes 234-279). 7/7 tests pass. Staged dans git (commit bloqué par hook table Claim|Evidence|Status, en attente de décision Brice sur commit).

**Statut** : ✅ clos.

### Risque #2 — vbb-loop-closure-check.py trop dense (god script)

**Description** : 448 → 877 lignes, 4 helpers + 3 validators + 1 finder. Si P0-4/P0-5-D ajoutent d'autres validators, le fichier devient illisible.

**Mitigation actuelle** : aucune.

**Recommandation** : refactor en sous-modules `vbb_loop_closure/validators.py` + `vbb_loop_closure/markers.py` + `vbb_loop_closure/cli.py` — **seulement** si P0-4 ou P0-5-D ajoutent ≥ 2 nouveaux validators. Pas urgent.

### Risque #3 — FAST-MINIMAL n'a pas d'exception explicite dans le hook

**Description** : AGENTS.md §CANON §6 documente le SKIP, mais le hook pre-commit-framework-gate lignes 78-82 fait `grep "voie: FAST-MINIMAL"` puis `exit 0`. Si le mot "FAST-MINIMAL" est malformé dans le frontmatter (ex: `voie: fast_minimal` ou `voie: FAST_MINIMAL`), le skip ne s'applique pas.

**Mitigation actuelle** : regex exacte `"voie: FAST-MINIMAL"` et `"voie: FAST-ZERO"`. Insensible à la casse ? **Non** — actuellement case-sensitive.

**Recommandation** : ajouter `re.IGNORECASE` ou un test de régression qui vérifie `voie: fast_minimal` est bien skip. Priorité basse (aucun cas réel observé).

### Risque #4 — Inflation closeouts (173 lignes pour 10 modifs)

**Description** : le closeout Phase 2 Run 1 (173 lignes) est dense mais exécutable. Si la même densité est conservée pour P0-4 + P0-5-D, on arrive à 500+ lignes cumulées sur 3 runs.

**Mitigation actuelle** : structure répétitive (tables Claim|Evidence|Status + dette méthodologique). Le lecteur LLM peut sauter à la table "dette".

**Recommandation** : split en (1) `07_CLOSEOUT.md` court (résumé, dette, SHA), (2) `08_EVIDENCE.md` détaillé (tables Claim|Evidence, captures, tests). Décision à prendre sur P0-4.

### Risque #5 — "no test surface" marker est ambigu

**Description** : le marker `## No test surface` permet de skipper le check test-audit. Mais "no test surface" peut vouloir dire (a) "aucun test à écrire" ou (b) "test surface non documentée" — sémantiquement différents.

**Mitigation actuelle** : une seule string reconnue, peu de risque de faux positif.

**Recommandation** : clarifier le wording dans `SKILL.md` de `t-vbb-test-coverage-mapper` (ex: `## No automated test surface (manual QA only)`). Priorité basse.

---

## 5. Recommandations minimales (3 max)

### R1 — POC P0-4 obligatoire avant Run 2

**Pourquoi** : P0-4 Review Matrix est catégorie D (vraie capacité nouvelle). Le risque #6 (Q6 = 6/10) le confirme. Sans POC, on risque de :

- produire une matrice trop stricte (blocages) ou trop laxiste (coquille vide) ;
- avoir à la recalibrer après 2-3 runs (dette technique).

**POC =** :
1. Matrice T1-T8 draft (1-2h).
2. Application rétro-active sur 3 runs historiques (2h).
3. Mesure faux positifs/négatifs (1h).
4. Décision GO/NO-GO/PIVOT (1h).
5. Documentation POC dans `docs/strategy/p0-4-poc-report.md`.

**Durée** : 1-2 jours. **Owner** : `vbb-struct-worker` (subagent) ou `cody-orchestrator` selon scope.

### R2 — Commit du test fixed-price (staged)

**Statut** : `tests/test_loop_closure_p2.py` est staged avec le test `test_claims_fixed_price_not_detected_as_bugfix` (+45 lignes, 7/7 tests pass). Le commit est **bloqué par le hook cody-reliability-gate** qui exige une table `| Claim | Evidence | Status |` — le commit message préparé respecte ce format.

**Action** : Brice valide le commit (1 ligne) ou refuse. Pas d'autre chemin (--no-verify explicitement évité par règle VBB).

### R3 — Pas de commit closeout amendé nécessaire

Le closeout `docs/runs/2026-06-13_1400_phase-2-run-1-contractualisation/07_CLOSEOUT.md` est déjà sur `main` (SHA `aae0514`). Aucune action requise.

---

## 6. Conclusion

Phase 2 Run 1 **réussi dans son scope strict** (10 modifications additives, 0 invention, CI vert, dette méthodologique divisée par 1.5). Le test `fixed-price` ferme l'unique faux positif identifié pendant l'audit.

**GO pour POC P0-4** (recommandation R1) — pas de GO pour Run 2 d'implémentation P0-4 sans POC validé.

---

## Annexes

### A. Fichiers audités (9)

| Fichier | LOC | Δ vs baseline | Catégorie |
|---|---|---|---|
| `tools/vbb-loop-closure-check.py` | 877 | +429 | C (validators ajoutés) |
| `tools/vbb-gate-check.py` | 449 | +57 | A (check mode_transition) |
| `AGENTS.md` | 161 | +42 | A (Pre-merge Gate Checklist + §13) |
| `docs/templates/04_PLAN.md.template` | 91 | +12 | A (Analyse d'impact) |
| `docs/templates/worker-evidence-paragraph.md` | 43 | new | B (nouveau template) |
| `scripts/hooks/pre-commit-framework-gate` | 135 | +99 | C (3 blocks opt-in) |
| `distributions/hermes/bypass-lint/README.md` | 129 | +11 | A (note explicative) |
| `skills/t-vbb-test-coverage-mapper/SKILL.md` | 135 | +19 | A (invocation guidance) |
| `tests/test_loop_closure_p2.py` | 314 | +49 (post-audit) | C (tests régression) |
| `tests/test_gate_check_mode_transition.py` | 154 | new | A (tests P0-5-A) |
| `docs/runs/2026-06-13_1400_phase-2-run-1-contractualisation/07_CLOSEOUT.md` | 173 | new | B (closeout) |

### B. Métrique catégorielle finale (10 modifs)

- **A** (transformation comportement existant) : 8
- **B** (nouveau template/document) : 1
- **C** (validators/hooks) : 2 *(overlap possible avec A selon granularité)*
- **D** (vraie invention) : **0** ✅

### C. Vérifications P.R2 (toutes vertes)

- `pytest tests/test_loop_closure_p2.py -q` → 7 passed (post-audit)
- `pytest tests/ -q` → 111 passed, 3 skipped
- `python tools/vbb-architecture.py lint` → 0 error, 0 warning
- `python tools/vbb-contract-lint.py` → 0 error
- `python tools/vbb-gate-check.py --help` → OK (l'ADR/POC gate-check existe déjà)
- `bash distributions/hermes/verify/verify.sh` → 28 checks OK
- `gh run watch smoke 26872427163` → success
- `gh run watch vbb-contracts 26872427211` → success

### D. Note sur l'infra ADR/POC existante

`tools/vbb-gate-check.py --help` affiche déjà "ADR + POC + Integration Gate check" — l'infrastructure ADR/POC/Integration est **déjà partiellement implémentée** dans VBB. Le présent audit ne l'a pas modifiée (scope READ-ONLY). Un futur audit dédié à `vbb-gate-check.py` est recommandé pour évaluer la complétude du flow ADR → POC → Integration → RecoPlan.
