---
run_id: "2026-07-13_1656_retire-hermes"
phase: "05_EXECUTION"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-13T17:07:00+02:00"
ended_at: "2026-07-13T17:13:00+02:00"
next_phase: "06_REVIEW"
artifacts_consumed:
  - "04_PLAN.md"
  - "POC.md"
  - "docs/adr/0025-supported-runtimes-pi-opencode-codex-claude.md"
artifacts_produced:
  - "05_EXECUTION.md"
  - "docs/audits/test-coverage-20260713-1711.md"
---

# 05_EXECUTION — Retire Hermes

## Résumé

La distribution Hermes/Cody et ses tests exclusifs ont été retirés. Le Core,
l'installateur, les hooks, l'architecture et la documentation active exposent
désormais uniquement Pi, OpenCode, Codex et Claude Code.

## Actions effectuées

| # | Étape du plan | Statut | Diff résumé |
|---|---|---|---|
| 1 | Retirer Hermes de l'installateur | `DONE` | provider, labels, plan et résumé supprimés de `setup.sh` |
| 2 | Supprimer la distribution et tests exclusifs | `DONE` | `distributions/hermes/` et test Cody retirés ; plan v2 archivé |
| 3 | Neutraliser le Core | `DONE` | hooks, outils, règles et vocabulaire rendus runtime-neutral |
| 4 | Aligner architecture et docs | `DONE` | README, GUIDE, catalogues, ADR, architecture et relations alignés |
| 5 | Clore | `DONE` | impact, test coverage, changelog et statut durable mis à jour |

## Écarts au plan

| Étape | Type d'écart | Raison | Décision prise |
|---|---|---|---|
| 3 | méthode | Le test des hooks dépendait d'un chemin externe historique | Exécuter explicitement les deux hooks locaux dans le test |
| 5 | ordre | La suite CI devait précéder le closeout final | Produire le closeout après preuve technique complète |

## Tests / validations passées

- [x] `bash -n setup.sh`
- [x] `bash tests/test_setup_smoke.sh` — 32 PASS
- [x] `bash tests/test_framework_gate_hook.sh` — 10 PASS
- [x] dry-run séparé pour `claude`, `codex`, `pi`, `opencode`
- [x] rejet de `--provider hermes`
- [x] `python tools/vbb-architecture.py lint` — 0 erreur, 0 warning
- [x] `python tools/vbb-contract-lint.py` — 0 erreur, 0 warning
- [x] `pytest tests/ -q` — 133 passed, 1 skipped
- [x] `bash scripts/vbb-ci-local.sh` — 7 PASS, 1 WARN non bloquant
- [x] audit de surface : `docs/audits/test-coverage-20260713-1711.md`

## Issues rencontrées

- Le test de gate appelait `~/02_Dev/vibebackbone`; il utilise maintenant le
  dépôt courant et enchaîne les hooks pre-commit et commit-msg.
- La CI locale choisit encore un ancien run comme « latest » et émet un warning
  non bloquant ; le run courant est validé explicitement en strict au closeout.

## Fichiers modifiés

```text
setup.sh
setup-lib.sh
distributions/hermes/
distributions/{pi,opencode,codex,claude}/
scripts/hooks/
tests/
tools/
README.md
GUIDE.md
AGENTS.md
core.README.md
CHANGELOG.md
docs/
prompts/1-p-vbb-structured-task.md
skills/t-vbb-test-coverage-mapper/SKILL.md
```

## Handoff vers `06_REVIEW`

- **À vérifier en review** : ensemble exact des quatre providers, absence de
  dépendance active au chemin supprimé, cohérence des documents canoniques.
- **Points de vigilance** : rupture volontaire pour les consommateurs Hermes ;
  historique conservé et état externe non modifié.
