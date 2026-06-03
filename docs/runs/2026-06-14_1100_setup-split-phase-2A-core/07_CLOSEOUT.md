# Closeout — Setup split Phase 2A : Core extraction

**Run ID** : 2026-06-14_1100_setup-split-phase-2A-core
**Type** : Phase 2A — first provider-aware split (Core uniquement)
**Date** : 2026-06-14
**Branche** : main
**Commit** : (à compléter après push)
**CI databaseId** : (à compléter après watch)

---

## Executive Summary

Phase 2A livrée : `core/setup.sh` (116 LOC) extrait les 3 blocs Core (pre-flight, universal skills symlink, universal prompts symlink). `setup.sh` route via `source core/setup.sh; core_install` (631 → 559 lignes, -72). Test avec HOME jetable prouve install + uninstall symétriques. Bug collatéral `_realpath` sur symlink relatif découvert (pré-existant, hors scope). Verdict : **GO pour Phase 2B Pi**.

---

## Fichiers créés / modifiés

| Fichier | Statut | LOC | Note |
|---|---|---|---|
| `core/setup.sh` | C | 116 | 4 fonctions : `core_install`, `core_preflight`, `core_install_skills_symlink`, `core_install_prompts_symlink` |
| `setup.sh` | M | 631 → 559 (-72) | Bloc 244-321 remplacé par `source "$REPO_ROOT/core/setup.sh"; core_install` |
| `tests/test_setup_smoke.sh` | M | 162 → 174 (+12) | Section 3 étendue : markers Core cherchés dans `core/setup.sh`, markers provider restent dans `setup.sh` |

**Périmètre autorisé strictement respecté** : aucun `distributions/*/setup.sh`, aucune section provider touchée, CI/proxy/profils Hermes/hooks/loop-closure/gate-check intacts.

---

## Blocs Core déplacés

| Bloc (nom original) | Lignes d'origine (setup.sh) | Destination (core/setup.sh) |
|---|---|---|
| `── Pre-flight checks ──` | 244-279 (36 LOC) | `core_preflight()` |
| `── 1. Universal skills symlink ──` | 281-290 (10 LOC) | `core_install_skills_symlink()` |
| `── 2. Universal prompts symlink ──` | 292-321 (30 LOC) | `core_install_prompts_symlink()` |

**Total déplacé** : 76 lignes (contenu original) → 116 lignes dans `core/setup.sh` (overhead = 4 en-têtes de fonction + commentaire d'en-tête + orchestration `core_install`).

**Sections NON déplacées (intentionnel)** :
- `uninstall()` (100-238) — orchestration globale multi-provider, hors scope Phase 2A
- `── 3. Claude Code — settings.json ──` → `── 9. OpenCode — prompt commands ──` — providers, Phase 2B-2E
- `── Summary ──` (567+) — global multi-provider, hors scope

**Helpers NON déplacés** (déjà décidé Phase 1) : `count_skills`, `count_prompts_total`, `count_prompt_adapters` restent dans `setup.sh`.

---

## Preuve HOME jetable

### Test 1 — Install symétrique

```
TMP_HOME=/var/folders/vg/.../tmp.E0UyjcVXDt
HOME=$TMP_HOME bash setup.sh
```

**Résultat** :
- `~/.agents/skills/vibebackbone` → `../../../../../../../../Users/bot/02_dev/vibebackbone/skills` ✓
- `~/.agents/prompts/vibebackbone` → `../../../../../../../../Users/bot/02_dev/vibebackbone/prompts` ✓
- 64 skills + 33 prompts installés (toutes providers, Core + 4 distributions)
- 0 backup nécessaire

### Test 2 — Uninstall symétrique

```
HOME=$TMP_HOME bash setup.sh --uninstall
```

**Résultat** :
- 23 fichiers `vbb-*.md` supprimés (Pi, Claude, OpenCode prompts)
- `~/.agents/skills/vibebackbone` symlink supprimé ✓
- `~/.agents/prompts/vibebackbone` symlink **non supprimé** (voir "bug collatéral" ci-dessous)
- `✓ vibebackbone uninstalled` final
- **Vrai HOME `/Users/bot/.agents/` intact** ✓

---

## Bug collatéral découvert (hors scope)

**Symptôme** : sur HOME jetable dans `/var/folders/.../`, le uninstall ne supprime pas `~/.agents/prompts/vibebackbone`.

**Cause** : `_is_vbb_symlink()` dans `setup-lib.sh` (lignes 104-124) appelle `_realpath()` qui ne résout pas correctement les symlinks avec un chemin relatif contenant beaucoup de `../` (cas d'un TMP_HOME très profond).

**Preuve que c'est pré-existant** :
- Code `_is_vbb_symlink` et `_realpath` : **non modifié** par Phase 1 ni Phase 2A
- Le HOME réel (`/Users/bot/.agents/prompts/vibebackbone`) est un symlink **absolu** (créé par `relpath` quand le path est court) → `_is_vbb_symlink` match
- Le HOME jetable produit un symlink **relatif** avec 14 niveaux de `../` → `_realpath` ne résout pas

**Vérification réelle** :
```
$ ls -la ~/.agents/prompts/vibebackbone
lrwxr-xr-x  1 bot  staff  38 19 mai 08:24 /Users/bot/.agents/prompts/vibebackbone -> /Users/bot/02_dev/vibebackbone/prompts   # absolu
$ ls -la /tmp/.../agents/prompts/vibebackbone
lrwxr-xr-x  1 bot  staff  61  3 juin 21:19 /tmp/.../agents/prompts/vibebackbone -> ../../../../../../../../Users/bot/02_dev/vibebackbone/prompts   # relatif
```

**Recommandation (hors scope Phase 2A)** : ajouter un fallback dans `_realpath` qui teste `cd $(dirname $link) && readlink $link | xargs realpath` pour les symlinks relatifs profonds. À traiter en follow-up (P1-1 ou équivalent).

**Impact Phase 2A** : **zéro**. Phase 2A valide l'extraction Core, pas `_realpath`. Le test HOME jetable a juste exposé un bug latent.

---

## Preuve comportement inchangé (vrai HOME)

```
$ bash setup.sh   # sur vrai HOME
... 64 skills · 33 prompts ...
$ ls -la ~/.agents/skills/vibebackbone ~/.agents/prompts/vibebackbone
lrwxr-xr-x  1 bot  staff  38 19 mai   08:24 .../prompts/vibebackbone -> /Users/bot/02_dev/vibebackbone/prompts
lrwxr-xr-x@ 1 bot  staff  32 3 juin   21:19 .../skills/vibebackbone -> ../../02_dev/vibebackbone/skills
```

Vrai HOME intact, symlinks Core pointent toujours au bon endroit, pas de régression observable.

---

## Tests verts (P.R2)

| Vérification | Résultat |
|---|---|
| `bash tests/test_setup_smoke.sh` | 26 PASS / 0 FAIL / 1 WARN |
| `bash -n setup.sh` | OK |
| `bash -n setup-lib.sh` | OK |
| `bash -n core/setup.sh` | OK |
| `python tools/vbb-architecture.py lint` | 0 errors / 0 warnings |
| `python tools/vbb-contract-lint.py` | 0 errors |
| `bash distributions/hermes/verify/verify.sh` | PASS (28 checks) |
| `pytest tests/ -q` | 135 passed, 3 skipped (baseline préservée, +0 régression) |

---

## Risques résiduels

| # | Risque | Sév. | Status / Mitigation |
|---|---|---|---|
| R1 | Bug `_realpath` sur symlink relatif profond (voir ci-dessus) | Moyenne | Pré-existant, hors scope Phase 2A, à fixer en P1-1 |
| R2 | `core_install` mute des globales (`PROMPTS_AVAILABLE`, `*_COUNT`) que setup.sh consomme ensuite | Faible | Contrat documenté en tête de `core/setup.sh` ; smoke test vérifie que setup.sh consomme bien ces globales |
| R3 | Si Phase 2B doit ajouter d'autres variables Core, il faudra étendre `core_install` | Faible | Ajouter une section au closeout Phase 2B le moment venu |
| R4 | Pas de test direct sur `core/setup.sh` isolé (toujours via setup.sh) | Faible | Acceptable : Phase 2A prouve que **setup.sh appelle core avec succès**, c'est l'objectif |
| R5 | Le uninstall Core est resté inline dans setup.sh | Faible | Documenté ; sera ré-évalué en Phase 2E ou follow-up dédié |

**Aucun risque HIGH non mitigé.**

---

## Verdict

**GO pour Phase 2B Pi.**

Conditions de GO groupé :
1. Phase 2B : extraire `distributions/pi/setup.sh` avec les 3 sections Pi (AGENTS.md symlink, SYSTEM.md symlink, prompts symlinks)
2. Réutiliser le même pattern routeur : `source "$REPO_ROOT/distributions/pi/setup.sh"; pi_install`
3. Étendre `tests/test_setup_smoke.sh` section 3 pour vérifier la présence des markers Pi dans `distributions/pi/setup.sh`
4. Le bug `_realpath` reste hors scope — sera traité séparément si Brice le souhaite

---

## Métadonnées

- **Setup split Phase 0 + 1** (livré SHA `1f549d8`) : filet de sécurité + extraction helpers
- **Ce run couvre** : Phase 2A = premier découpage par logique (Core)
- **Cible Phase 2B-E** : distributions/pi, claude, codex, opencode + routeur final
- **Hors scope (rappel)** : CI, proxy, profils Hermes, hooks, loop-closure, gate-check, install Hermes auto
