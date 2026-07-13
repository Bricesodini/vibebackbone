---
run_id: "2026-07-13_1656_retire-hermes"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-13T17:04:00+02:00"
ended_at: "2026-07-13T17:07:00+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_AUDIT.md"
  - "03_DECISION.md"
  - "POC.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Retire Hermes

## Objectif

Livrer un framework cohérent, installé et documenté uniquement pour Pi,
OpenCode, Codex et Claude Code.

## Pré-conditions

- ADR 0025 ACCEPTED et POC GO.
- Changements utilisateur préexistants identifiés et protégés.
- Aucun fichier externe `~/.hermes/` dans le scope.

## Étapes ordonnées

| # | Action | Fichiers cibles | Validation | Rollback |
|---|--------|-----------------|------------|----------|
| 1 | Retirer Hermes de l'installateur | `setup.sh`, smoke tests | dry-run 4 providers + unknown Hermes | revert ciblé |
| 2 | Supprimer la distribution et tests exclusifs | `distributions/hermes/`, Cody test | pytest collection | restaurer depuis git |
| 3 | Neutraliser le Core | hooks, tools, PILOTAGE, prompts/skill | scans actifs + tests hooks | revert ciblé |
| 4 | Aligner architecture et docs | README, GUIDE, DEPLOYMENT, RUNBOOK, catalogs, ARCHITECTURE | links/rg/lint | restaurer fichiers |
| 5 | Clore | run, changelog, AUDIT_STATUS, SESSION | P.R2 + independent self-review disclosed | revert commit |

## Critères d'acceptation

- [ ] Seuls `claude`, `codex`, `pi`, `opencode` sont acceptés par `setup.sh`.
- [ ] `distributions/hermes/` n'existe plus.
- [ ] Aucun document actif ne présente Hermes/Cody comme supporté.
- [ ] Les références historiques sont explicitement non actives.
- [ ] P.R2 complet vert et aucun changement utilisateur hors scope commité.

## Plan de rollback global

Restaurer les fichiers supprimés et modifiés depuis le commit parent ; aucune
migration externe ni donnée utilisateur n'est touchée.

## Risques identifiés

- Imports externes inconnus du proxy : rupture documentée.
- Références actives oubliées : scan ciblé hors historique.
- Régression setup : tests et dry-runs par provider.

## Analyse d'impact

- **Effectuée ?** : OUI (via `t-vbb-impact-analyzer`).
- **Périmètre d'impact** : `distribution-setup`, governance Core, docs actives,
  hooks/tests et consommateurs externes Hermes.
- **Risques d'effet de bord** : CLI breaking ; historique à préserver.

## Integration Gate

- **ADR référencé** : `docs/adr/0025-supported-runtimes-pi-opencode-codex-claude.md`
- **POC référencé** : `docs/runs/2026-07-13_1656_retire-hermes/POC.md`
- **CAN_CODE_START** : soumis au gate automatique.
