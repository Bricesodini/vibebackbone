# 01_INTAKE — Run 02 Prompts P.R2

> **Source spec** : `docs/strategy/vbb-improvements-roadmap/runs/run-02-prompts-pr2.md`
> **Date d'intake** : 2026-07-12
> **Route** : FAST-MINIMAL
> **Statut** : READY (avant exécution)

---

## Goal

Aligner 3 prompts canoniques sur les nouvelles conventions de loop discipline : ajouter la mention explicite de la phase suivante (pour 02-audit et 03-decision) et la référence canonique à `@pre-merge-gate.md` (pour 05-execution).

## Findings source

| ID | Finding | Fichier |
|----|---------|---------|
| AUDIT-B-001 (1/2) | 02-audit ne mentionne pas explicitement la transition vers 03_DECISION | `prompts/canonical/02-p-vbb-audit.md` |
| AUDIT-B-001 (2/2) | 03-decision ne mentionne pas explicitement la transition vers 04_PLAN | `prompts/canonical/03-p-vbb-decision.md` |
| AUDIT-B-002 | 05-execution ne référence pas `@pre-merge-gate.md` ni les 5 vérifications P.R2 canoniques | `prompts/canonical/05-p-vbb-execution.md` |

## Modifications

| QW | Fichier | Action |
|----|---------|--------|
| QW-2.1 | `02-p-vbb-audit.md` | Ajout section `## Next phase` (avant `## Handoff`) avec lien vers `03-p-vbb-decision.md` |
| QW-2.2 | `03-p-vbb-decision.md` | Ajout section `## Next phase` (avant `## Handoff`) avec lien vers `04-p-vbb-plan.md` |
| QW-2.3 | `05-p-vbb-execution.md` | Ajout section `## Pre-merge gate (P.R2)` (avant `## Handoff`) avec référence à `docs/REFERENCE/pre-merge-gate.md` |

## Acceptance criteria

- [x] 3 fichiers prompts modifiés
- [x] `git diff` canon = vide
- [x] Liens inter-prompt valides (04-p-vbb-plan.md, pre-merge-gate.md existent)
- [x] `05_PATCH_SUMMARY.md` existe
- [x] `07_CLOSEOUT.md` existe avec `kind: CLOSEOUT`
- [ ] ACTIVITY_LOG mis à jour
- [ ] git commit