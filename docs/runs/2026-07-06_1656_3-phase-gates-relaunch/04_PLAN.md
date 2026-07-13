---
run_id: "2026-07-06_1656_3-phase-gates-relaunch"
phase: "04_PLAN"
voie: "AUDIT"
status: "READY"
agent: "pi"
started_at: "2026-07-06T16:57:00Z"
ended_at: "2026-07-06T16:58:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "docs/PILOTAGE.md"
  - "docs/PROJECT_MODE.md"
  - "docs/AUDIT_STATUS.md"
  - "docs/MVP_START_PROTOCOL.md"
artifacts_produced:
  - "04_PLAN.md"
  - "POC.md"
---

# 04_PLAN — Relance des 3 gates de Phase

## Objectif

Produire un verdict daté pour chacun des 3 gates de phase Vibebackbone sur
l'état actuel du repo core (juillet 2026), sous forme de 3 rapports
timbrés dans `docs/audits/` plus une trace consolidée dans `07_CLOSEOUT.md`.

## Pré-conditions

- Repo `/Users/bot/02_Dev/vibebackbone` sur branche courante propre
  (vérifié via `git status`).
- Run directory `docs/runs/2026-07-06_1656_3-phase-gates-relaunch/` créé.
- `01_INTAKE.md` rédigé (cf. artefact produit).
- `docs/PROJECT_MODE.md`, `docs/AUDIT_STATUS.md`, `docs/CONTEXT.md`,
  `docs/PILOTAGE.md`, `docs/MVP_START_PROTOCOL.md` lisibles.
- 5 ADRs accessibles dans `docs/adr/` (0001, 0002, 0003, 0004, 0013).

## ADR de référence

Cette run est un audit transverse du framework core. Les décisions
architecturales qui sous-tendent la structure auditée sont consignées dans
plusieurs ADRs ; la plus directement liée à la nature de cette run est
**ADR-0004 — Contract Schema Version Semantics** (`docs/adr/0004-contract-schema-version-semantics.md`,
statut ACCEPTED), qui cadre la cohérence entre contrats de skills et
exécution — référente pour l'évaluation gate 2 (ADR + POC + Integration).

ADR-0013 — Repository Organization Core vs Distributions est citée
secondairement pour la dimension « gouvernance du core ».

## Étapes ordonnées

| # | Action | Fichiers cibles | Validation | Rollback |
|---|--------|-----------------|------------|----------|
| 1 | Rédiger POC.md (validation que la run est prête pour gate-check) | `POC.md` | `grep -i "Verdict: GO" POC.md` | `rm POC.md` |
| 2 | **Gate 1** : produire le rapport RICO readiness | `02_AUDIT_RICO.md` + `docs/audits/rico-readiness-20260706-1656.md` | présence des deux artefacts | `rm` des deux |
| 3 | **Gate 2** : exécuter `vbb-gate-check.py` sur la run_dir | `02_AUDIT_GATE_CHECK.md` + sortie console | exit code + JSON parsé | `rm` artefact |
| 4 | **Gate 3** : produire le rapport mode transition | `02_AUDIT_MODE.md` + `docs/audits/mode-transition-20260706-1656.md` | présence des deux artefacts | `rm` des deux |
| 5 | Rédiger `07_CLOSEOUT.md` consolidé | `07_CLOSEOUT.md` | présence des 3 sections verdict + commit summary | `rm` |
| 6 | `git add` + commit + push | `.git/` | `git log -1` montre le commit | `git reset HEAD~1` |

## Critères d'acceptation (Definition of Done)

- [ ] `POC.md` rédigé avec ligne « Verdict: GO » (gate 2 pré-requis)
- [ ] `02_AUDIT_RICO.md` produit avec verdict `READY`/`PARTIAL`/`BLOCKED`/`UNKNOWN` + autorisation
- [ ] `docs/audits/rico-readiness-20260706-1656.md` timbré
- [ ] `02_AUDIT_GATE_CHECK.md` produit avec verdict `PASS`/`FAIL` + JSON gate-check
- [ ] `02_AUDIT_MODE.md` produit avec verdict `GO`/`GO_WITH_CONDITIONS`/`NO_GO`/`UNKNOWN`
- [ ] `docs/audits/mode-transition-20260706-1656.md` timbré
- [ ] `07_CLOSEOUT.md` consolidé avec verdict composite des 3 gates
- [ ] `git log -1` confirme le commit
- [ ] Rapport Telegram envoyé à l'utilisateur

## Hypothèses et risques

- **H1** : gate 1 (RICO) appliqué au framework core produira un verdict
  non-`READY` — c'est attendu, le skill est conçu pour des projets from
  zero ; le verdict sera annoté avec note de non-applicabilité partielle.
- **H2** : gate 2 (ADR+POC) produira `PASS` — POC explicite + ADR lié.
- **H3** : gate 3 (mode transition) produira `GO_WITH_CONDITIONS` ou
  `NO_GO` — verdict actuel `PARTIAL` (cf. AUDIT_STATUS) suggère des
  conditions résiduelles.
- **R1** : aucun code modifié — risque d'intégrité nul.
- **R2** : seul `docs/runs/<run_id>/` et `docs/audits/` reçoivent de
  nouveaux fichiers — réversibilité totale par `rm -rf`.

## Handoff vers `05_EXECUTION`

- **Entrées pour exécution** :
  - 01_INTAKE.md, 04_PLAN.md, POC.md (présents dans run_dir)
  - skills/0-vbb-rico-readiness/SKILL.md (lecture)
  - tools/vbb-gate-check.py (exécution)
  - skills/t-vbb-mode-transition-gate/SKILL.md (lecture)
- **Points de vigilance** :
  - Pour gate 1 : ne pas tenter de produire du code ou des contrats ;
    rester sur lecture + rapport.
  - Pour gate 2 : s'assurer que `docs/adr/0004-contract-schema-version-semantics.md`
    est bien valide (regex `**Status**: ACCEPTED`).
  - Pour gate 3 : ne PAS modifier `docs/PROJECT_MODE.md` (règle skill).
- **Décisions à arbitrer** :
  - Aucune — toutes les décisions sont pré-cadrees par les 3 skills.