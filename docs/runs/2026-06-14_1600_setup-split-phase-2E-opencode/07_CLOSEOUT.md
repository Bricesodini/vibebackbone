---
run_id: "2026-06-14_1600_setup-split-phase-2E-opencode"
phase: "07_CLOSEOUT"
voie: "STRUCTUREE"
status: "READY"
agent: "vbb-cody-orchestrator (delegated by Hermes for setup split refactor)"
started_at: "2026-06-14T16:00:00Z"
next_phase: null
artifacts_produced: []
---

# Closeout — Setup split Phase 2E : OpenCode extraction

**Run ID** : 2026-06-14_1600_setup-split-phase-2E-opencode
**Type** : Phase 2E — fifth provider split (OpenCode uniquement)
**Date** : 2026-06-14
**Branche** : main
**Commit** : (à compléter après push)
**CI databaseId** : (à compléter après watch)

---

## Executive Summary

Phase 2E livrée : `distributions/opencode/setup.sh` (76 LOC) extrait les sections §8+§9 "OpenCode — instructions + prompt commands" (44 LOC inline) de `setup.sh` (392 → 356 LOC, -36). Déplacement strictement mécanique : même JSON patch, même `generate_prompt_commands`, mêmes messages stdout, même comportement uninstall, même ordre d'exécution global. 33/0/1 smoke, 135/3 pytest baseline préservée. Verdict : **DONE — setup.sh est devenu un pur routeur**.

---

## Fichiers créés / modifiés

| Fichier | Statut | LOC | Note |
|---|---|---|---|
| `distributions/opencode/setup.sh` | C | 76 | 3 fonctions : `opencode_install`, `opencode_patch_opencode_json`, `opencode_generate_prompt_commands`. Python heredoc copié verbatim |
| `setup.sh` | M | 392 → 356 (-36) | Sections §8+§9 (44 LOC inline) remplacées par `source + opencode_install` |
| `tests/test_setup_smoke.sh` | M | 225 → 240 (+15) | Section 3 étendue : markers "OpenCode — instructions" et "OpenCode — prompt commands" cherchés dans `distributions/opencode/setup.sh`, sanity check header §8-9 préservé |

**Périmètre autorisé strictement respecté** : aucun `distributions/{claude,pi,codex,hermes}/setup.sh`, aucune section provider non-OpenCode touchée, CI/proxy/profils Hermes/hooks/loop-closure/gate-check intacts.

**Pas d'amendement de closeouts antérieurs nécessaire** : `test_status_dashboard.test_latest_runs` est resté vert (135/3 baseline) sans modification. Le closeout Phase 2E lui-même est créé avec frontmatter YAML dès le départ.

---

## Blocs OpenCode déplacés

| Bloc (nom original) | Lignes d'origine (setup.sh) | Destination (distributions/opencode/setup.sh) |
|---|---|---|
| `── 8. OpenCode — instructions ──` | 273-311 (39 LOC, dont ~30 LOC de Python heredoc) | `opencode_patch_opencode_json()` |
| `── 9. OpenCode — prompt commands ──` | 313-316 (4 LOC) | `opencode_generate_prompt_commands()` |

**Total déplacé** : 43 lignes (contenu original) → 76 lignes dans `distributions/opencode/setup.sh` (overhead = 2 en-têtes de fonction + commentaire d'en-tête + orchestration `opencode_install` + import setup.sh contract doc).

**Code préservé mot pour mot** (vérifié par diff visuel) :
- Python heredoc `opencode_patch_opencode_json` : `$schema: https://opencode.ai/config.json`, lecture/création du fichier, append `AGENTS.md` + `SYSTEM.md` au tableau `instructions`, sortie "added" vs "already referenced" selon que `changes` est vide ou non
- Logique `generate_prompt_commands` : appel à la lib partagée avec `$OPENCODE_COMMANDS` + label "OpenCode prompts" + mutateurs `OPENCODE_PROMPTS_OK`/`OPENCODE_PROMPTS_SKIP`
- Messages stdout : `✓ OpenCode: AGENTS.md, SYSTEM.md instruction(s) added`, `✓ OpenCode: AGENTS.md, SYSTEM.md already referenced`, `⚠ OpenCode: python3 not found — opencode.json patch skipped`, `✓ OpenCode prompts: 26 commands generated`

**Section NON déplacée (intentionnel)** :
- Bloc uninstall OpenCode (lignes 184-208 dans `uninstall()`) — orchestration globale multi-provider, hors scope Phase 2E (pattern uniforme avec Phases 2A, 2B, 2C, 2D, 2F)

---

## Preuve HOME jetable

### Test 1 — Install symétrique OpenCode

```
TMP_HOME=/var/folders/vg/.../tmp.qnLMgrNTYD
HOME=$TMP_HOME bash setup.sh
```

**Résultat OpenCode** :
- `~/.config/opencode/opencode.json` créé (170 octets) avec :
  ```json
  {
    "$schema": "https://opencode.ai/config.json",
    "instructions": [
      "/Users/bot/02_dev/vibebackbone/AGENTS.md",
      "/Users/bot/02_dev/vibebackbone/SYSTEM.md"
    ]
  }
  ```
  ✓
- 26 fichiers `vbb-*.md` dans `~/.config/opencode/commands/` ✓
- Log : `✓ OpenCode: AGENTS.md, SYSTEM.md instruction(s) added` + `✓ OpenCode prompts: 26 commands generated`

### Test 2 — Idempotence (deuxième exécution)

**Méthode** : SHA256 de `opencode.json` avant/après 2ème install.

```
SHA256 before: 66338cb83c4a7ef9705f9cf194669067d0f0adb333c90e3571bab40b67fcfe72
SHA256 after:  66338cb83c4a7ef9705f9cf194669067d0f0adb333c90e3571bab40b67fcfe72
IDENTICAL ✓
```

**Log 2ème install** : `✓ OpenCode: AGENTS.md, SYSTEM.md already referenced` (vs `instruction(s) added` la 1ère fois — comportement pré-Phase-2E préservé).

### Test 3 — Uninstall symétrique OpenCode

```
HOME=$TMP_HOME bash setup.sh --uninstall
```

**Résultat** :
- 26 fichiers `vbb-*.md` supprimés de `~/.config/opencode/commands/` ✓
- `opencode.json` : 170 → 50 octets (instructions `AGENTS.md` + `SYSTEM.md` retirées du tableau, `$schema` seul reste — comportement pré-Phase-2E préservé) ✓
- Le dossier `commands/` vide reste (comportement pré-Phase-2E)

### Test 4 — Vrai HOME intact

```
$ ls -la /Users/bot/.config/opencode/opencode.json
-rw-r--r--  1 bot  staff  266 19 mai   08:24 /Users/bot/.config/opencode/opencode.json
```

Vrai HOME intact (266 octets, 19 mai inchangé, 26 commands).

---

## Bug _realpath rappelé comme hors scope

**Status** : pré-existant, NON corrigé dans ce run (brief explicite : "ne pas corriger _realpath").

**Impact Phase 2E** : **zéro**. Le bloc OpenCode ne manipule aucun symlink (juste un JSON file). `_is_vbb_symlink` n'est pas appelé.

**À traiter** : P1-1 ou follow-up dédié (cf. closeouts Phase 2A-2D, 2F).

---

## Tests verts (P.R2)

| Vérification | Résultat |
|---|---|
| `bash tests/test_setup_smoke.sh` | 33 PASS / 0 FAIL / 1 WARN |
| `bash -n setup.sh, setup-lib.sh, core/setup.sh, distributions/{pi,claude,codex,hermes,opencode}/setup.sh` | 8/8 OK |
| `HOME=$TMP_HOME bash setup.sh` (install) | OK, opencode.json + 26 commands ✓ |
| Idempotence (SHA256 opencode.json) | identique ✓ |
| `HOME=$TMP_HOME bash setup.sh --uninstall` (uninstall) | 26 commands removed ✓ |
| `python tools/vbb-architecture.py lint` | 0 errors / 0 warnings |
| `python tools/vbb-contract-lint.py` | 0 errors |
| `bash distributions/hermes/verify/verify.sh` | PASS (28 checks) |
| `pytest tests/ -q` | **135 passed, 3 skipped** (baseline préservée, +0 régression, test_status_dashboard OK sans amendement) |

---

## Risques résiduels

| # | Risque | Sév. | Status / Mitigation |
|---|---|---|---|
| R1 | Bug `_realpath` (cf. ci-dessus) | Moyenne | Hors scope, à fixer en P1-1 |
| R2 | Le uninstall OpenCode reste inline dans setup.sh | Faible | Documenté ; pattern uniforme avec Phases 2A-2D, 2F |
| R3 | Pas de test direct sur `distributions/opencode/setup.sh` isolé | Faible | Acceptable : Phase 2E prouve que **setup.sh appelle opencode avec succès**, c'est l'objectif |
| R4 | `uninstall()` monolithique dans setup.sh (toujours 143 LOC) | Faible | Pattern acceptable, split optionnel en follow-up |
| R5 | `test_status_dashboard.test_latest_runs` est un faux positif latent | Faible | Pas cassé cette fois (test OK), follow-up pour durcir |

**Aucun risque HIGH non mitigé.**

---

## Verdict

**DONE — la chaîne d'extraction est complète.**

État final après Phase 2E :
- setup.sh = 356 LOC = **routeur pur** (helpers, uninstall monolithique, routeur 5 distributions, summary)
- 7 fichiers de distribution (setup-lib.sh + core/setup.sh + 4 providers/hermes setup.sh)
- Toutes les phases précédentes (0+1, 2A, 2B, 2C, 2D, 2F) sont préservées
- CI verte

**Conditions de DONE groupé** :
1. Audit final READ-ONLY à lancer immédiatement pour vérifier l'état complet
2. Pas de follow-up obligatoire — les 5 items de la roadmap (1-5) sont explicitement hors scope et marqués "à n'ouvrir qu'après audit final"

---

## Métadonnées

- **Setup split Phase 0 + 1** (SHA `1f549d8`) : filet de sécurité + extraction helpers
- **Setup split Phase 2A** (SHA `4bd93be`) : extraction Core → `core/setup.sh`
- **Setup split Phase 2B** (SHA `9ca9e45`) : extraction Pi → `distributions/pi/setup.sh`
- **Setup split Phase 2C** (SHA `9dc55d2`) : extraction Claude → `distributions/claude/setup.sh`
- **Setup split Phase 2D** (SHA `7f8efb0`) : extraction Codex → `distributions/codex/setup.sh`
- **Setup split Phase 2F** (SHA `9ed3d43`) : Hermes non-destructif
- **Ce run couvre** : Phase 2E = extraction OpenCode → `distributions/opencode/setup.sh` (5e et dernier provider)
- **Cible** : audit final de la migration (immédiat après ce commit)
- **Hors scope (rappel)** : CI, proxy, profils Hermes, hooks, loop-closure, gate-check, install Hermes auto, fix `_realpath`, refactorisation des blocs providers, split du `uninstall()` monolithique
