---
run_id: "2026-06-14_1300_setup-split-phase-2C-claude"
phase: "07_CLOSEOUT"
voie: "STRUCTUREE"
status: "READY"
agent: "vbb-cody-orchestrator (delegated by Hermes for setup split refactor)"
started_at: "2026-06-14T10:00:00Z"
next_phase: null
artifacts_produced: []
---

# Closeout — Setup split Phase 2C : Claude extraction

**Run ID** : 2026-06-14_1300_setup-split-phase-2C-claude
**Type** : Phase 2C — third provider split (Claude uniquement)
**Date** : 2026-06-14
**Branche** : main
**Commit** : (à compléter après push)
**CI databaseId** : (à compléter après watch)

---

## Executive Summary

Phase 2C livrée : `distributions/claude/setup.sh` (102 LOC) extrait les 3 sections Claude (§3 settings.json + §4 CLAUDE.md block + §5 prompt commands, 69 LOC inline) de `setup.sh` (527 → 465 LOC, -62). Routeur : `source distributions/claude/setup.sh; claude_install`. Test HOME jetable valide install (settings.json patché, bloc vibebackbone dans CLAUDE.md, 26 commands) et uninstall (settings/CLAUDE.md/commands nettoyés). 28/0/1 au smoke test, 135/3 pytest baseline préservée. Verdict : **GO pour Phase 2D Codex**.

---

## Fichiers créés / modifiés

| Fichier | Statut | LOC | Note |
|---|---|---|---|
| `distributions/claude/setup.sh` | C | 102 | 4 fonctions : `claude_install`, `claude_install_settings_json`, `claude_install_claude_md_block`, `claude_install_prompt_commands` |
| `setup.sh` | M | 527 → 465 (-62) | 3 sections §3+§4+§5 (69 LOC inline) remplacées par `source + claude_install` |
| `tests/test_setup_smoke.sh` | M | 181 → 196 (+15) | Section 3 étendue : markers "Claude Code — settings.json" et "Claude Code — CLAUDE.md block" cherchés dans `distributions/claude/setup.sh`, sanity check header §3-5 préservé dans setup.sh |

**Périmètre autorisé strictement respecté** : aucun `distributions/{codex,opencode,hermes}/setup.sh`, aucune section provider non-Claude touchée, CI/proxy/profils Hermes/hooks/loop-closure/gate-check intacts.

---

## Blocs Claude déplacés

| Bloc (nom original) | Lignes d'origine (setup.sh) | Destination (distributions/claude/setup.sh) |
|---|---|---|
| `── 3. Claude Code — settings.json ──` | 251-271 (21 LOC) | `claude_install_settings_json()` |
| `── 4. Claude Code — CLAUDE.md block ──` | 273-313 (41 LOC) | `claude_install_claude_md_block()` |
| `── 5. Claude Code — prompt commands ──` | 315-318 (4 LOC) | `claude_install_prompt_commands()` |

**Total déplacé** : 66 lignes (contenu original) → 102 lignes dans `distributions/claude/setup.sh` (overhead = 3 en-têtes de fonction + commentaire d'en-tête + orchestration `claude_install`).

**Logique "Deploying governance"** (anciennement entre §3 et §4) : migrée dans `claude_install_claude_md_block()` car elle est sémantiquement liée au déploiement du bloc gouvernance. Comportement préservé.

**Sections NON déplacées (intentionnel)** :
- `uninstall()` (lignes Claude inline, ~110-145) — orchestration globale multi-provider, hors scope Phase 2C
- `── 6. Codex — compiled AGENTS.md ──` à `── 9. OpenCode ──` — providers, Phase 2D-2E
- `── Summary ──` (495+) — global multi-provider, hors scope

**Helpers NON déplacés** (déjà décidé Phase 1) : `needs_python`, `generate_prompt_commands` restent dans `setup-lib.sh` (utilisés aussi par core + Pi + Claude).

---

## Preuve HOME jetable

### Test 1 — Install symétrique Claude

```
TMP_HOME=/var/folders/vg/.../tmp.cbQNAtsPWC
HOME=$TMP_HOME bash setup.sh
```

**Résultat Claude** :
- `~/.claude/settings.json` créé avec `{"skills": ["~/.agents/skills"]}` ✓
- `~/.claude/CLAUDE.md` créé avec bloc :
  ```
  # vibebackbone
  @/Users/bot/02_dev/vibebackbone/AGENTS.md
  @/Users/bot/02_dev/vibebackbone/SYSTEM.md
  ```
  ✓
- `~/.claude/commands/vbb-*.md` × 26 créés (26 prompt commands) ✓
- Logs : `✓ Claude Code: settings.json patched with '~/.agents/skills'`, `✓ Claude Code: AGENTS.md + SYSTEM.md reference added`, `✓ Claude prompts: 26 commands generated`

### Test 2 — Uninstall symétrique Claude

```
HOME=$TMP_HOME bash setup.sh --uninstall
```

**Résultat Claude** :
- `settings.json` : `{"skills": ["~/.agents/skills"]}` → `{}` (skill entry supprimé) ✓
- `CLAUDE.md` : bloc `# vibebackbone` + 2 lignes `@` → 0 mention vibebackbone ✓
- `commands/` : 26 fichiers → 0 (dossier vide reste) ✓
- Logs : `✓ Removed ~/.agents/skills from Claude Code settings`, `✓ Removed vibebackbone block from ~/.claude/CLAUDE.md`, `✓ Removed vbb-*.md` (× 26)

### Test 3 — Vrai HOME intact

```
$ cat /Users/bot/.claude/settings.json | head -5
{
  "theme": "auto",
  "skills": [
    "~/.agents/skills"
  ]
$ grep -c vibebackbone /Users/bot/.claude/CLAUDE.md
3
$ ls /Users/bot/.claude/commands/ | wc -l
26
```

Vrai HOME intact, re-install idempotent (`✓ Claude Code: settings.json already includes '~/.agents/skills'`, `✓ Claude Code: AGENTS.md + SYSTEM.md reference updated`).

---

## Bug _realpath rappelé comme hors scope

**Status** : pré-existant, NON corrigé dans ce run (brief explicite : "ne pas corriger _realpath / _is_vbb_symlink").

**Symptôme** : `_is_vbb_symlink` (dans `setup-lib.sh`) ne résout pas correctement les symlinks avec un chemin relatif contenant beaucoup de `../` (>10 niveaux). Visible uniquement sur HOME jetable dans `/var/folders/.../tmp.XXX`.

**Impact Phase 2C** : **zéro**. Phase 2C valide l'extraction Claude, pas `_realpath`. Les fichiers Claude (settings.json, CLAUDE.md) ne sont pas des symlinks, donc `_is_vbb_symlink` n'est pas appelé pour Claude.

**À traiter** : P1-1 ou follow-up dédié (cf. closeouts Phase 2A + 2B).

---

## Tests verts (P.R2)

| Vérification | Résultat |
|---|---|
| `bash tests/test_setup_smoke.sh` | 28 PASS / 0 FAIL / 1 WARN |
| `bash -n setup.sh` | OK |
| `bash -n setup-lib.sh` | OK |
| `bash -n core/setup.sh` | OK |
| `bash -n distributions/pi/setup.sh` | OK |
| `bash -n distributions/claude/setup.sh` | OK |
| `python tools/vbb-architecture.py lint` | 0 errors / 0 warnings |
| `python tools/vbb-contract-lint.py` | 0 errors |
| `bash distributions/hermes/verify/verify.sh` | PASS (28 checks) |
| `pytest tests/ -q` | 135 passed, 3 skipped (baseline préservée, +0 régression) |

**Tests HOME jetable Claude** :
- Install : `settings.json` ✓, `CLAUDE.md` block vibebackbone ✓, 26 commands ✓
- Uninstall : `settings.json` cleaned (`{}`) ✓, `CLAUDE.md` vibebackbone removed ✓, commands dir empty ✓

---

## Risques résiduels

| # | Risque | Sév. | Status / Mitigation |
|---|---|---|---|
| R1 | Bug `_realpath` (cf. ci-dessus) | Moyenne | Hors scope, à fixer en P1-1 |
| R2 | Le uninstall Claude reste inline dans setup.sh (lignes 110-145) | Faible | Documenté ; sera ré-évalué en Phase 2E ou follow-up dédié |
| R3 | `claude_install` mute `CLAUDE_PROMPTS_OK` / `CLAUDE_PROMPTS_SKIP` consommés par le summary | Faible | Contrat documenté en tête de `distributions/claude/setup.sh` ; smoke test vérifie que setup.sh consomme bien ces globales |
| R4 | Pas de test direct sur `distributions/claude/setup.sh` isolé (toujours via setup.sh) | Faible | Acceptable : Phase 2C prouve que **setup.sh appelle claude avec succès**, c'est l'objectif |
| R5 | Migration du log "Deploying governance" dans `claude_install` (vs setup.sh) — changement cosmétique mais observable | Faible | Test HOME jetable confirme l'output identique ; le log reste dans la même séquence d'exécution |

**Aucun risque HIGH non mitigé.**

---

## Verdict

**GO pour Phase 2D Codex.**

Conditions de GO groupé :
1. Phase 2D : extraire `distributions/codex/setup.sh` avec la section §6 Codex (compiled AGENTS.md)
2. Réutiliser le même pattern routeur : `source "$REPO_ROOT/distributions/codex/setup.sh"; codex_install`
3. Étendre `tests/test_setup_smoke.sh` section 3 pour vérifier la présence du marker "Codex — compiled AGENTS.md" dans `distributions/codex/setup.sh`
4. Le bug `_realpath` reste hors scope — sera traité séparément si Brice le souhaite

---

## Métadonnées

- **Setup split Phase 0 + 1** (SHA `1f549d8`) : filet de sécurité + extraction helpers
- **Setup split Phase 2A** (SHA `4bd93be`) : extraction Core → `core/setup.sh`
- **Setup split Phase 2B** (SHA `9ca9e45`) : extraction Pi → `distributions/pi/setup.sh`
- **Ce run couvre** : Phase 2C = extraction Claude → `distributions/claude/setup.sh`
- **Cible Phase 2D-E** : distributions/codex, opencode + routeur final
- **Hors scope (rappel)** : CI, proxy, profils Hermes, hooks, loop-closure, gate-check, install Hermes auto, fix `_realpath`
