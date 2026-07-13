# Plan de correction — Durcir Cody selon la CODY RELIABILITY GATE (v2)

**Source :** retour ChatGPT sur le constat "Cody sur-produit, sous-prouve"
**Date :** 2026-06-02
**Cible :** `~/.hermes/profiles/vbb-cody-orchestrator/SOUL.md` + outillage + tests
**Auteur :** Hermes, suite à demande Brice
**Statut :** plan v2 — validé par Brice avec re-ordering

## Contexte

Constat opéré sur la session 2026-06-01/02 :

1. **Cody a produit un "deep framework remediation"** (commit `ac05b4c`, 95 fichiers modifiés, +1386/-409 lignes) **sans** :
   - Lancer `vbb-loop-closure-check.py` sur le run_id
   - Exécuter `vbb-contract-lint.py` ou `vbb-architecture.py lint`
   - Lancer `pytest tests/ -q`
   - Lancer `bash scripts/vbb-ci-local.sh`
   - Classifier ses findings en VERIFIED_FINDING / SIGNAL / HYPOTHESIS
2. **Cody a combiné AUDIT + STRUCTURED + CLOSEOUT en un seul méga-commit** sur le framework, ce qui viole la séparation des rôles.
3. **Cody a promu des HYPOTHESIS au rang P1** sans evidence (VBB-DEEP-003).
4. **Cody a marqué "COMPLETE" sans preuve de fermeture**.

C'est un pattern de **productivité sans vérifiabilité**.

## Objectif

Transformer Cody de **"agent producteur"** en **"agent prouvant"** : il ne déclare COMPLETE qu'après avoir démontré que tout est cohérent, vérifié, et tracé.

## Principe de séquencement (Brice 2026-06-02)

**Outillage après la règle.** Aucun run d'outillage avant que la règle humaine/runtime soit intégrée dans Cody SOUL. Donc Run 1 = SOUL d'abord, outillage ensuite.

## Découpage en runs (5 runs, ordre imposé)

### Run 1 — Cody SOUL reliability patch (STRUCTURED)

**But** : intégrer les 6 règles dans la SOUL de Cody.

**Fichiers** :
- `~/.hermes/profiles/vbb-cody-orchestrator/SOUL.md` (modif, ~100 lignes ajoutées)

**Critère de passage** : Cody ne peut plus déclarer COMPLETE sans evidence gate explicite.

**Ajouts à intégrer** (contenu complet dans le SKILL.md du futur `cody-reliability-gate`, mais aussi en clair dans SOUL.md) :

1. Role separation : AUDIT observe, STRUCTURED modifie, CLOSEOUT prouve. Exception framework remediation nécessite approve Brice explicite.
2. Evidence classification : VERIFIED_FINDING (P1/P2 only) / SIGNAL / HYPOTHESIS.
3. Closure validity : `vbb-loop-closure-check.py` doit PASS sinon pas de COMPLETE.
4. Verification coverage (framework changes) : architecture lint + contract-lint + loop-closure + pytest + ci-local.
5. Out-of-repo disclosure : path + reason + risk + rollback + install proof.
6. Evidence table before commit : `| Claim | Evidence | Status |` dans le message.

**Worker** : vbb-struct-worker (modif doc runtime, ~100 lignes)
**Estimation** : 30-45 min

### Run 2 — Closeout gate minimal (STRUCTURED)

**But** : étendre `vbb-loop-closure-check.py` pour que FINAL_STATUS=COMPLETE échoue si loop-closure courant FAIL.

**Fichiers** :
- `~/02_Dev/vibebackbone/tools/vbb-loop-closure-check.py` (modif, ajout mode "strict" qui retourne exit 2 si FAIL)

**Critère** : sur un run_id dont la closure a FAIL, le script retourne exit 2 avec message explicite. Tout consumer (Cody, close-worker, audits) doit traiter exit 2 = "ne pas produire FINAL_STATUS=COMPLETE".

**Dépendances** : aucune (étend l'existant).

**Worker** : vbb-struct-worker (modif outil Python, ~30 lignes)
**Estimation** : 30 min

### Run 3 — Evidence tooling (FAST, conditionné)

**But** : créer `cody-reliability-gate` ou `classify-evidence` SEULEMENT après stabilisation des règles (Runs 1+2).

**Fichiers** :
- `~/.hermes/skills/cody-reliability-gate/SKILL.md` (nouveau)
- `~/.hermes/skills/classify-evidence/SKILL.md` (nouveau, optionnel)
- `~/.hermes/bin/cody-reliability-gate` (nouveau, shell tool qui appelle les linters vbb)

**Critère** : l'outil aide à classifier VERIFIED_FINDING / SIGNAL / HYPOTHESIS **sans remplacer le jugement humain**. C'est un assistant, pas un oracle. Toute classification automatique doit être confirmée par Cody dans son output.

**Comportement de l'outil `cody-reliability-gate`** :
1. Accepte un argument : `run_id` (optionnel, défaut = run courant)
2. Exécute séquentiellement :
   - `vbb-contract-lint.py` (sur le repo vibebackbone si cible framework, sinon skip)
   - `vbb-architecture.py lint` (idem)
   - `vbb-loop-closure-check.py <run_id>` (en mode strict après Run 2)
   - `pytest tests/ -q` (si tests présents)
   - `bash scripts/vbb-ci-local.sh` (si présent)
3. Retourne JSON : `{"verdict": "PASS|FAIL", "checks": [...], "missing": [...], "errors": [...]}`

**Dépendances** : Run 1 (la SOUL documente comment utiliser le skill) + Run 2 (le tool vérifie la closure)

**Worker** : vbb-fast-worker (skill + shell tool, ~150 lignes total)
**Estimation** : 45-60 min

### Run 4 — Pre-commit / CI integration (STRUCTURED)

**But** : brancher le gate dans le workflow repo vibebackbone.

**Fichiers** :
- `~/02_Dev/vibebackbone/.git/hooks/pre-commit` (nouveau)
- Optionnel : step CI dans le framework si un pipeline existe

**Critère** : il **bloque** les faux COMPLETE (commit framework sans evidence table), mais **ne bloque PAS** les commits de travail WIP. Distinction :
- Commit WIP = message typique `wip: ...`, `draft: ...`, `chore: ...` → hook laisse passer
- Commit framework declaratif = `fix(...): ...` ou `feat(...): ...` sur fichiers du framework → hook exige `| Claim | Evidence | Status |` dans le message

**Dépendances** : Runs 1+2+3 (le hook appelle l'outil de Run 3)

**Worker** : vbb-struct-worker (hook bash, ~50 lignes)
**Estimation** : 30-45 min

### Run 5 — Regression test sur pattern `ac05b4c`-like (AUDIT + STRUCTURED)

**But** : vérifier que le système **refuse** le pattern "méga-commit framework auto-validé" qu'on a vu dans `ac05b4c` (95 fichiers, +1386/-409, sans linter, sans evidence table).

**Fichiers** :
- `~/02_Dev/vibebackbone/tests/test_cody_reliability_gate.py` (nouveau, pytest)
- Scenario reproduit : 50+ fichiers modifiés en un commit, message sans evidence table, linter pas lancé

**Critère** : test PASS = statut COMPLETE **impossible** sans preuves. Le test :
1. Crée un faux commit reproduisant le pattern `ac05b4c` (sur une branche jetable)
2. Tente de marquer le run comme COMPLETE
3. Vérifie que la gate rejette (exit 2)
4. Vérifie que le hook pre-commit rejette un commit framework sans evidence table

**Dépendances** : Runs 1+2+3+4 (test = intégration des 4)

**Worker** : vbb-audit-worker (AUDIT de la gate elle-même) + vbb-struct-worker (STRUCTURED pour le test)
**Estimation** : 45-60 min

## Séquencement

```
Run 1 (SOUL.md) ── Run 2 (loop-closure strict) ── Run 3 (skill+tool) ── Run 4 (hook) ── Run 5 (regression test)
```

**Séquentiel strict** : aucun run ne démarre avant que le précédent soit passé.

**Estimation totale** : 3h-4h, ~6 commits, ~8 fichiers créés/modifiés.

## Validation cible

Après les 5 runs :
- Cody a une SOUL qui documente les 6 règles comme non-négociables (Run 1)
- `vbb-loop-closure-check.py` rejette les faux COMPLETE (Run 2)
- Skill + outil aident à classifier sans remplacer le jugement (Run 3)
- Hook bloque les faux commits framework, laisse passer les WIP (Run 4)
- Test reproduit le pattern `ac05b4c` et vérifie qu'il est désormais impossible (Run 5)

**Critère de succès final** : scénario `ac05b4c` rejoué → Cody **refuse** de pousser ou **demande confirmation explicite** à cause de la rule 1 (role separation). Le test pytest Run 5 valide ce comportement de manière reproductible.

## Points d'attention

- **Résistance de Cody** : la SOUL doit être **explicite** ("non-negotiable") et Cody doit l'internaliser. Risque qu'il contourne en argumentant que c'est "un cas spécial". Solution : la SOUL doit lister explicitement ce qui constitue une exception, et "framework remediation" doit nécessiter `approve: brice` dans le prompt.

- **Skill `classify-evidence` ajoute de la latence** : à chaque finding, Cody devra invoquer le skill. C'est ~5s de plus par finding. Acceptable pour la qualité gagnée.

- **Le hook pre-commit peut être bypassé** par `--no-verify`. Il faut documenter que c'est interdit sauf exception.

- **Run 5 reproduit le pattern `ac05b4c`** : le test crée un faux commit sur une branche jetable. Risque de pollution du repo si pas isolé correctement. Le test doit être `tmp_path`-based.

## Hors scope

- Réécrire la SOUL de fond (juste ajouter la gate, pas refondre)
- Changer le format des commits framework existants
- Modifier le comportement des workers (uniquement Cody)
- Créer une UI de validation (Brice reste en lecture de commit messages Telegram)

## Next step

1. Brice a déjà validé le plan
2. Délégation Run 1 (SOUL.md) à vbb-struct-worker
3. Run 2 (loop-closure strict) à vbb-struct-worker
4. Run 3 (skill+tool) à vbb-fast-worker
5. Run 4 (hook) à vbb-struct-worker
6. Run 5 (regression test) à vbb-audit-worker + vbb-struct-worker
7. Validation : reproduire le scénario `ac05b4c` et vérifier que Cody refuse
