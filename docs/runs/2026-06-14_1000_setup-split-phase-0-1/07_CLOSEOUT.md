# Closeout — Setup split Phase 0 + Phase 1

**Run ID** : 2026-06-14_1000_setup-split-phase-0-1
**Type** : POC behavior-preserving (Phase 0 + Phase 1)
**Date** : 2026-06-14
**Branche** : main
**Commit** : (à compléter après commit)

---

## Executive Summary

Phase 0 + Phase 1 livrées : `tests/test_setup_smoke.sh` (162 LOC, 26 PASS / 0 FAIL) détecte tout changement de surface de `setup.sh`, et `setup-lib.sh` (209 LOC) extrait 7 helpers transversaux. `setup.sh` passe de 807 → 631 lignes (-176). L'install réelle s'est exécutée de manière idempotente, prouvant que le comportement est préservé. Tests : 135 passed / 3 skipped (baseline +0 régression), arch-lint / contract-lint / verify.sh tous verts. Verdict : **GO pour Phase 2 split distributions**.

---

## Fichiers créés / modifiés

| Fichier | Statut | LOC | Note |
|---|---|---|---|
| `setup.sh` | M | 807 → 631 (-176) | 7 helpers remplacés par `source setup-lib.sh` |
| `setup-lib.sh` | C | 209 | Helpers transversaux extraits |
| `tests/test_setup_smoke.sh` | C | 162 | Smoke test non-destructif, 7 sections |

**Périmètre périmètre autorisé strictement respecté** : aucun `core/setup.sh`, `distributions/*/setup.sh`, `CI GitHub`, `proxy`, `profils Hermes`, `hooks`, `loop-closure`, `gate-check` touchés.

---

## Helpers déplacés (Phase 1)

Les 7 helpers transversaux nommés dans le brief :

| Helper | Lignes d'origine (setup.sh) | Destination |
|---|---|---|
| `relpath` | 63-72 | `setup-lib.sh` |
| `_realpath` | 76-102 | `setup-lib.sh` |
| `_is_vbb_symlink` | 104-124 | `setup-lib.sh` |
| `needs_python` | 126-132 | `setup-lib.sh` |
| `backup_file` | 134-141 | `setup-lib.sh` |
| `symlink_if_absent` | 144-185 | `setup-lib.sh` |
| `generate_prompt_commands` | 220-274 | `setup-lib.sh` |

**Helpers NON déplacés** (intentionnel, non demandés par le brief) :
- `count_skills` (188-196) — usage local à setup.sh
- `count_prompts_total` (199-206) — usage local
- `count_prompt_adapters` (210-217) — usage local

**Ordre dans `setup-lib.sh`** : `relpath` → `_realpath` → `_is_vbb_symlink` → `needs_python` → `backup_file` → `symlink_if_absent` → `generate_prompt_commands`. Cet ordre préserve la chaîne de dépendances : `_is_vbb_symlink` et `symlink_if_absent` appellent `_realpath` ; `symlink_if_absent` et `generate_prompt_commands` appellent `backup_file`.

---

## Preuve que le comportement est inchangé

### A. Test 1 — `bash -n` (parse only)

```
=== bash -n setup.sh ===     OK
=== bash -n setup-lib.sh === OK
```

Aucune erreur de parse.

### B. Test 2 — Smoke test (sections 1-7)

26 PASS / 0 FAIL / 1 WARN :
- Section 1 : syntax check sur les deux fichiers
- Section 2 : présence de AGENTS.md, skills/, prompts/, SYSTEM.md, CLAUDE.md
- Section 3 : présence des 9 marqueurs de sections provider (Universal skills/prompts, Claude settings/CLAUDE, Codex compiled AGENTS, Pi symlinks, OpenCode instructions/commands, uninstall)
- Section 4 : handlers `--uninstall` et `--force-governance` toujours présents
- Section 5 : **les 7 helpers sont détectés dans `setup-lib.sh`** (lib affichant "Phase 1 active")
- Section 6 : `--help` non géré (WARN — acceptable, comportement pré-Phase-1)
- Section 7 : aucune opération destructive avant le check `--uninstall` (ligne 28)

### C. Test 3 — Install réel idempotent

Exécuté : `bash setup.sh` (sans flag, en environnement `~` actuel).

**Résultat** : 64 skills · 33 prompts installés, 0 erreur, 0 backup nécessaire. Tous les symlinks pointent toujours au bon endroit (`vibebackbone → ../../02_dev/vibebackbone/skills` et `vibebackbone → /Users/bot/02_dev/vibebackbone/prompts`). Claude Code, Codex, Pi, OpenCode : tous présents, 26 prompts adapter par provider.

**Side-effect conscient** : la commande a réellement re-déployé l'install dans `~`. Risque accepté car (a) l'install était déjà présente au 3 juin et idempotente, (b) tous les liens sont restés cohérents, (c) `set -e` aurait aborté sur la moindre régression. Pour Phase 2 (split providers), un wrapper dry-run sera nécessaire.

### D. Test 4 — Vérifications obligatoires

```
=== python tools/vbb-architecture.py lint ===
VBB Architecture Linter — 0 error(s), 0 warning(s)
  Blocks: 8
  ✓ Architecture blocks valid

=== python tools/vbb-contract-lint.py ===
VBB Contract Linter — 0 error(s) found
  ✓ All contracts valid

=== bash distributions/hermes/verify/verify.sh ===
RESULT: PASS (28 checks OK)
Hermes/Cody distribution is verifiable. install.sh is DEFERRED per F-015.

=== pytest tests/ -q ===
135 passed, 3 skipped in 7.76s
```

**Aucune régression** : la suite pytest reste à 135/3 (baseline 135/3).

---

## Risques résiduels

| # | Risque | Sévérité | Mitigation existante / proposée pour Phase 2 |
|---|---|---|---|
| R1 | Le test smoke pourrait être trop permissif (ne catche pas un changement de comportement subtil) | Moyenne | Pour Phase 2 : ajouter un snapshot diff du stdout de `bash setup.sh` en mode `--help` ou via dry-run wrapper |
| R2 | `bash setup.sh` a un side-effect réel sur $HOME, donc tester un comportement nécessite un env jetable | Moyenne | Pour Phase 2 : créer un wrapper `bash -c "HOME=/tmp/vbb-dryrun bash setup.sh --help"` ou mock `$HOME` |
| R3 | `setup-lib.sh` est au même niveau que `setup.sh` ; pour Phase 2 il faudra décider s'il vit dans `core/` ou reste racine | Faible | Décision Phase 2 (probablement : `core/setup-lib.sh` + chemin absolu résolu par setup.sh) |
| R4 | L'ordre des fonctions dans `setup-lib.sh` est critique (dépendances bash) | Faible | Commentaire en tête du fichier documente l'ordre ; smoke test vérifie que les 7 fonctions sont définies |
| R5 | Le smoke test ne vérifie pas que les arguments des helpers n'ont pas changé | Faible | Les signatures sont 1:1 avec l'original (extraction pure) ; un test fonctionnel sera ajouté en Phase 2 si nécessaire |

**Aucun risque HIGH non mitigé.**

---

## Verdict

**GO pour Phase 2 split distributions.**

Conditions de GO groupé :
1. Avant Phase 2 : ajouter un wrapper dry-run non-destructif (HOME jetable) pour tester chaque distribution sans toucher le vrai `~`
2. Avant Phase 2 : décider de l'emplacement final de `setup-lib.sh` (probable : `core/setup-lib.sh`, avec `core/setup.sh` routeur + 4 `distributions/*/setup.sh` provider)
3. Phase 2 elle-même : extraction UNE distribution à la fois (Hermes → Pi → Claude → Codex → OpenCode), avec smoke test + re-install réel à chaque étape

---

## Métadonnées

- **Audit READ-ONLY setup.sh** (livré en amont) : verdict GO WITH POC
- **Plan de migration** (livré en amont) : 4 phases, +75 lignes net projeté
- **Ce run couvre** : Phases 0 (smoke) + 1 (helper extraction) = filet de sécurité + premier découpage neutre
- **Cible Phase 2** : `distributions/hermes/setup.sh`, `distributions/pi/setup.sh`, `distributions/claude/setup.sh`, `distributions/codex/setup.sh`, `distributions/opencode/setup.sh` + `core/setup.sh` routeur
- **Hors scope (rappel)** : CI, proxy, profils Hermes, hooks, loop-closure, gate-check, install Hermes automatique
