---
run_id: "2026-07-14_0015_v2r2-portabilite-diete"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-code"
started_at: "2026-07-13T22:25:00Z"
ended_at: "2026-07-13T22:30:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "docs/adr/0030-boot-set-diet-and-portability.md (ACCEPTED)"
  - "CANON_CHANGE_PROPOSAL.md (APPROVED)"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — v2r2-portabilite-diete

## Objectif

TD-105 (portabilité), TD-107 (réconciliation), diète du boot set à contenu
normatif constant (cible ≤ ~1 200 mots), pointeur externe `~/.claude/CLAUDE.md`.
Réf. : ADR-0030, CCP APPROVED.

## Pré-conditions

- Gate `can_code_start=true` (ADR-0030 liaison stricte, POC non requise).
- Inventaire des règles normatives du boot set dressé avant compression
  (consigné en 05_EXECUTION) — critère : chaque règle reste énoncée une fois.

## Étapes ordonnées

| # | Action | Fichiers |
|---|--------|----------|
| 1 | Chemins morts → relatifs repo : règle 11 + prompt library + commentaire source (AGENTS), bloc gate (PILOTAGE, RUNBOOK), source canonique (LONG_RUN_RULE) | `AGENTS.md`, `docs/PILOTAGE.md`, `docs/RUNBOOK.md`, `docs/LONG_RUN_RULE.md` |
| 2 | TD-107 : QOA-003 → RESOLVED (preuve V2-R1 `ca70f4a` + tests) ; TD-001 → PyYAML 6.0.2 installé/actif | `docs/AUDIT_STATUS.md`, `docs/TECH_DEBT.md` |
| 3 | Diète : SYSTEM.md recentré runtime + pointeurs vers AGENTS.md ; AGENTS.md sans compteurs ni chemins HOME ; CLAUDE.md sans compteurs | `SYSTEM.md`, `AGENTS.md`, `CLAUDE.md` |
| 4 | Synchroniser la copie distribution | `distributions/pi/SYSTEM.md` |
| 5 | Lot externe : sauvegarde `~/.claude/CLAUDE.md.bak-20260713` puis sections gouvernance VibeCodex → pointeur canon VBB (délégation locale conservée) | hors repo |
| 6 | Rule 12 : entrée Decisions log (impact réel : 4 distributions consomment le boot) | `docs/DISTRIBUTIONS.md` |
| 7 | P.R2 + closeout CLOSE-FINAL + SESSION/ACTIVITY_LOG + commit/push | docs du run |

## Critères d'acceptation

- 0 occurrence `02_Dev` / `/Users/bot` dans les surfaces actives (grep).
- Boot set ≤ ~1 300 mots (cible 1 200) avec inventaire des règles : aucune perdue.
- `diff SYSTEM.md distributions/pi/SYSTEM.md` vide après sync.
- `~/.claude/CLAUDE.md` : plus de grammaire VibeCodex, pointeur VBB, backup présent.
- P.R2 5/5 PASS.

## Risques identifiés

- Perte de règle à la compression → inventaire avant/après + revue diff (CCP).
- Lot externe : impact sur d'autres projets de la machine → sauvegarde datée,
  changement réversible en une copie.

## Rollback

Repo : `git revert`. Externe : restaurer `~/.claude/CLAUDE.md.bak-20260713`.
