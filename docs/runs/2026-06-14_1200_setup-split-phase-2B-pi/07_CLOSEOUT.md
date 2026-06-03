---
run_id: "2026-06-14_1200_setup-split-phase-2B-pi"
phase: "07_CLOSEOUT"
voie: "STRUCTUREE"
status: "READY"
agent: "vbb-cody-orchestrator (delegated by Hermes for setup split refactor)"
started_at: "2026-06-14T10:00:00Z"
next_phase: null
artifacts_produced: []
---

# Closeout — Setup split Phase 2B : Pi extraction

**Run ID** : 2026-06-14_1200_setup-split-phase-2B-pi
**Type** : Phase 2B — second provider split (Pi uniquement)
**Date** : 2026-06-14
**Branche** : main
**Commit** : (à compléter après push)
**CI databaseId** : (à compléter après watch)

---

## Executive Summary

Phase 2B livrée : `distributions/pi/setup.sh` (74 LOC) extrait la section §7 "Pi — symlinks" (37 LOC inline) de `setup.sh` (559 → 527 LOC, -32). Routeur : `source distributions/pi/setup.sh; pi_install`. Test HOME jetable valide install (AGENTS + SYSTEM + 26 prompts) et uninstall (3 symlinks supprimés). 27/0/1 au smoke test, 135/3 pytest baseline préservée. Verdict : **GO pour Phase 2C Claude**.

---

## Fichiers créés / modifiés

| Fichier | Statut | LOC | Note |
|---|---|---|---|
| `distributions/pi/setup.sh` | C | 74 | 4 fonctions : `pi_install`, `pi_install_agents_symlink`, `pi_install_system_symlink`, `pi_install_prompts_symlinks` |
| `setup.sh` | M | 559 → 527 (-32) | Bloc §7 (37 LOC inline) remplacé par `source + pi_install` |
| `tests/test_setup_smoke.sh` | M | 174 → 181 (+7) | Section 3 étendue : marker "Pi — symlinks" cherché dans `distributions/pi/setup.sh`, sanity check header §7 préservé dans setup.sh |

**Périmètre autorisé strictement respecté** : aucun `distributions/{claude,codex,opencode,hermes}/setup.sh`, aucune section provider non-Pi touchée, CI/proxy/profils Hermes/hooks/loop-closure/gate-check intacts.

---

## Blocs Pi déplacés

| Bloc (nom original) | Lignes d'origine (setup.sh) | Destination (distributions/pi/setup.sh) |
|---|---|---|
| `── 7. Pi — symlinks (AGENTS + SYSTEM + prompts) ──` | 412-448 (37 LOC) | `pi_install()` (4 sous-fonctions) |

**Total déplacé** : 37 lignes (contenu original) → 74 lignes dans `distributions/pi/setup.sh` (overhead = 3 en-têtes de fonction + commentaire d'en-tête + orchestration `pi_install`).

**Sections NON déplacées (intentionnel)** :
- `uninstall()` (190-207) — orchestration globale multi-provider, hors scope Phase 2B
- `── 3. Claude Code ──` à `── 9. OpenCode ──` — providers, Phase 2C-2E
- `── Summary ──` (495+) — global multi-provider, hors scope

**Helpers NON déplacés** (déjà décidé Phase 1) : `symlink_if_absent`, `backup_file` restent dans `setup-lib.sh` (utilisés aussi par core + Pi).

---

## Preuve HOME jetable

### Test 1 — Install symétrique Pi

```
TMP_HOME=/var/folders/vg/.../tmp.b86suz6fMU
HOME=$TMP_HOME bash setup.sh
```

**Résultat Pi** :
- `~/.pi/agent/AGENTS.md` → `/Users/bot/02_dev/vibebackbone/AGENTS.md` ✓ (symlink absolu)
- `~/.pi/agent/SYSTEM.md` → `/Users/bot/02_dev/vibebackbone/SYSTEM.md` ✓
- `~/.pi/agent/prompts/*.md` → 26 symlinks vers `$PROMPTS_SRC/*.md` ✓
- Logs : `✓ Pi: AGENTS.md: symlink created`, `✓ Pi: SYSTEM.md: symlink created`, `✓ Pi prompts: 26 prompts linked`

### Test 2 — Uninstall symétrique Pi

```
HOME=$TMP_HOME bash setup.sh --uninstall
```

**Résultat Pi** :
- `~/.pi/agent/AGENTS.md` supprimé ✓
- `~/.pi/agent/SYSTEM.md` supprimé ✓
- 26 fichiers `*.md` dans `~/.pi/agent/prompts/` supprimés ✓ (le dossier vide reste, comportement pré-Phase-2B)
- Logs : `✓ Removed vbb-0-p-vbb-before-building.md` (× 26)

### Test 3 — Vrai HOME intact

```
$ ls -la /Users/bot/.pi/agent/AGENTS.md /Users/bot/.pi/agent/SYSTEM.md
lrwxr-xr-x  1 bot  staff  40 16 mai 13:10 /Users/bot/.pi/agent/AGENTS.md -> /Users/bot/02_Dev/vibebackbone/AGENTS.md
lrwxr-xr-x@ 1 bot  staff  40 3 juin 21:10 /Users/bot/.pi/agent/SYSTEM.md -> /Users/bot/02_dev/vibebackbone/SYSTEM.md
```

Vrai HOME intact, re-install idempotent (`✓ Pi: AGENTS.md: already linked (case-insensitive match)`, `✓ Pi: SYSTEM.md: already linked`).

---

## Bug _realpath rappelé comme hors scope

**Status** : pré-existant, NON corrigé dans ce run (brief explicite : "ne pas corriger _realpath / _is_vbb_symlink").

**Symptôme** : `_is_vbb_symlink` (dans `setup-lib.sh`) ne résout pas correctement les symlinks avec un chemin relatif contenant beaucoup de `../` (>10 niveaux). Visible uniquement sur HOME jetable dans `/var/folders/.../tmp.XXX` (le `relpath` produit 14 niveaux de `../`).

**Impact Phase 2B** : **zéro**. Phase 2B valide l'extraction Pi, pas `_realpath`. Le test Pi utilise des symlinks absolus (`/Users/bot/02_dev/vibebackbone/AGENTS.md`), donc `_is_vbb_symlink` match correctement.

**À traiter** : P1-1 ou follow-up dédié (cf. closeout Phase 2A §"Bug collatéral").

---

## Tests verts (P.R2)

| Vérification | Résultat |
|---|---|
| `bash tests/test_setup_smoke.sh` | 27 PASS / 0 FAIL / 1 WARN |
| `bash -n setup.sh` | OK |
| `bash -n setup-lib.sh` | OK |
| `bash -n core/setup.sh` | OK |
| `bash -n distributions/pi/setup.sh` | OK |
| `python tools/vbb-architecture.py lint` | 0 errors / 0 warnings |
| `python tools/vbb-contract-lint.py` | 0 errors |
| `bash distributions/hermes/verify/verify.sh` | PASS (28 checks) |
| `pytest tests/ -q` | 135 passed, 3 skipped (baseline préservée, +0 régression) |

**Tests HOME jetable** :
- Install : `$TMP_HOME/.pi/agent/AGENTS.md` ✓, `$TMP_HOME/.pi/agent/SYSTEM.md` ✓, 26 prompts ✓
- Uninstall : symlinks AGENTS+SYSTEM supprimés ✓, 26 prompts supprimés ✓

---

## Risques résiduels

| # | Risque | Sév. | Status / Mitigation |
|---|---|---|---|
| R1 | Bug `_realpath` (cf. ci-dessus) | Moyenne | Hors scope, à fixer en P1-1 |
| R2 | Le uninstall Pi reste inline dans setup.sh (lignes 190-207) | Faible | Documenté ; sera ré-évalué en Phase 2E ou follow-up dédié |
| R3 | `pi_install` mute `PI_PROMPTS_OK` / `PI_PROMPTS_SKIP` consommés par le summary | Faible | Contrat documenté en tête de `distributions/pi/setup.sh` ; smoke test vérifie que setup.sh consomme bien ces globales |
| R4 | Si Phase 2C ajoute d'autres variables Pi, il faudra étendre `pi_install` | Faible | Pas applicable (Phase 2C = Claude, pas Pi) |
| R5 | Pas de test direct sur `distributions/pi/setup.sh` isolé (toujours via setup.sh) | Faible | Acceptable : Phase 2B prouve que **setup.sh appelle pi avec succès**, c'est l'objectif |

**Aucun risque HIGH non mitigé.**

---

## Verdict

**GO pour Phase 2C Claude.**

Conditions de GO groupé :
1. Phase 2C : extraire `distributions/claude/setup.sh` avec les 3 sections Claude (settings.json, CLAUDE.md block, prompt commands)
2. Réutiliser le même pattern routeur : `source "$REPO_ROOT/distributions/claude/setup.sh"; claude_install`
3. Étendre `tests/test_setup_smoke.sh` section 3 pour vérifier la présence des markers Claude dans `distributions/claude/setup.sh`
4. Le bug `_realpath` reste hors scope — sera traité séparément si Brice le souhaite

---

## Métadonnées

- **Setup split Phase 0 + 1** (SHA `1f549d8`) : filet de sécurité + extraction helpers
- **Setup split Phase 2A** (SHA `4bd93be`) : extraction Core → `core/setup.sh`
- **Ce run couvre** : Phase 2B = extraction Pi → `distributions/pi/setup.sh`
- **Cible Phase 2C-E** : distributions/claude, codex, opencode + routeur final
- **Hors scope (rappel)** : CI, proxy, profils Hermes, hooks, loop-closure, gate-check, install Hermes auto, fix `_realpath`
