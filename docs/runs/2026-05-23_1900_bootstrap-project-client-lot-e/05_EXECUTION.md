---
run_id: "2026-05-23_1900_bootstrap-project-client-lot-e"
phase: "05_EXECUTION"
voie: "RAPIDE"
status: "READY"
agent: "claude-code"
started_at: "2026-05-23T19:05:00Z"
ended_at: "2026-05-23T19:45:00Z"
next_phase: "07_CLOSEOUT"
artifacts_consumed:
  - "docs/runs/2026-05-23_1800_artifact-verify-lot-c/07_CLOSEOUT.md"
  - "docs/templates/07_CLOSEOUT.md.template"
  - "skills/INDEX.yaml"
  - "docs/PROJECT_MODE.md"
artifacts_produced:
  - "tools/vbb-project-init.py"
  - "skills/t-vbb-project-context-init/SKILL.md"
  - "skills/t-vbb-project-context-init/CONTRACT.yaml"
  - "skills/INDEX.yaml"
  - "tests/test_project_init.py"
---

# 05_EXECUTION — bootstrap-project-client-lot-e

## Livrés

### `tools/vbb-project-init.py` (nouveau)

Outil Python idempotent. Opère sur `--target-dir` (défaut : cwd).

Fichiers créés dans le projet cible (si absents) :
- `docs/PROJECT_MODE.md` — mode initial (DEV/PROD)
- `docs/CONTEXT.md` — MOC avec nom du projet
- `docs/AUDIT_STATUS.md` — squelette NOT_RUN
- `docs/INDEX.md` — carte de navigation
- `docs/runs/README.md` — copié depuis la distribution VBB
- `docs/audits/README.md`
- `docs/adr/README.md`
- `docs/templates/*.md.template` — 7 templates de phase copiés depuis VBB
- `.gitignore` — entrées SESSION.md ajoutées si absentes

Idempotence :
- Skip par défaut si le fichier existe.
- `--overwrite` pour forcer ; `--backup` pour conserver l'ancien en `.bak`.
- `--dry-run` pour prévisualiser sans écriture.

Pre-commit hook : `--install-hook` copie et exécute
`scripts/install-vbb-pre-commit.sh` si `.git/hooks/pre-commit` absent.

### `skills/t-vbb-project-context-init/SKILL.md + CONTRACT.yaml` (nouveaux)

CONTRACT.yaml v0.3 :
- `outputs.artifact` : `docs/runs/{run_id}/07_CLOSEOUT.md` (`phase_artifact`)
- `secondary_artifacts` : PROJECT_MODE.md, CONTEXT.md, AUDIT_STATUS.md (`persistent_state_update`)
- Statuts : PASS / PARTIAL / FAIL / BLOCKED

SKILL.md :
- PROCESS en 9 étapes : dry-run, confirmation, exécution, vérification, guide CONTEXT.md
- BLOCKING CONDITIONS : outil absent, répertoire inexistant, projet déjà initialisé
- Compatible tous agents (claude-code, codex, pi, opencode)

### `skills/INDEX.yaml` (mis à jour)

`t-vbb-project-context-init` ajouté. INDEX.yaml désormais versionné (PR #4).

## Décisions d'exécution

- **CONTEXT.md** : inclut `<À compléter>` pour description et stack — signaux clairs
  pour l'agent/utilisateur que ces sections doivent être remplies.
- **.gitignore** : append non-destructeur ; idempotent via recherche de `docs/SESSION.md`.
- **`--install-hook`** : non-destructeur par défaut (skip si hook existant), `--overwrite`
  requis pour remplacer.
- **Template copy** : copie des 7 fichiers `.md.template` depuis `VBB_ROOT/docs/templates/`.
  Si la source est absente → erreur non-bloquante (fichier skippé avec message).
- **`files_created` et `files_skipped`** dans la sortie : requis par le contrat
  (`outputs.required: [files_created, files_skipped, ...]`).
