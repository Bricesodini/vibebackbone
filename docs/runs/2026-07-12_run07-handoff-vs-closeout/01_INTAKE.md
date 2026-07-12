---
run_id: "2026-07-12_run07-handoff-vs-closeout"
phase: "01_INTAKE"
voie: "STRUCTURED"
status: "READY"
kind: "INTAKE"
agent: "pi"
started_at: "2026-07-12T23:58:00Z"
human_validated_by: "Brice Sodini"
---

# 01_INTAKE — Run 07 HANDOFF vs CLOSEOUT

## Type de intake

**Kind** : `INTAKE` (STRUCTURED, après validation canon)
**Source spec** : [`docs/strategy/vbb-improvements-roadmap/runs/run-07-handoff-vs-closeout.md`](../../strategy/vbb-improvements-roadmap/runs/run-07-handoff-vs-closeout.md)
**Source canon proposal** : [`docs/strategy/vbb-improvements-roadmap/runs/run-07-CANON_CHANGE_PROPOSAL.md`](../../strategy/vbb-improvements-roadmap/runs/run-07-CANON_CHANGE_PROPOSAL.md) (status `APPROVED` by Brice)
**Source audit** : [`docs/audits/audit-C-handoff-closeout-calibration-20260712-1300.md`](../../audits/audit-C-handoff-closeout-calibration-20260712-1300.md) §AUDIT-C-002 (P2), AUDIT-C-003 (P2), AUDIT-C-004 (P2 dérivé)

## Goal (reformulé depuis spec)

Rendre la discrimination **HANDOFF vs CLOSEOUT** explicite à tous les niveaux :
1. **Niveau prompt** : `07-p-vbb-closeout.md` calcule le `kind:` automatiquement
2. **Niveau gouvernance** : `SESSION_RULES.md` documente la règle
3. **Niveau archive locale** : `docs/SESSION.history/` (gitignored)
4. **Niveau canon (route)** : `PILOTAGE.md` sépare `CLOSEOUT` en `CLOSE-HANDOFF` + `CLOSE-FINAL`

## Périmètre

**Inclus** :
- QW-C-1 : `prompts/canonical/07-p-vbb-closeout.md` (ajout Étape 1 — Calculer le kind)
- QW-C-2 : `docs/SESSION_RULES.md` (ajout section Handoff vs Closeout)
- QW-C-3 : `.gitignore` (ajout `docs/SESSION.history/`) + note dans `docs/SESSION.md`
- R-C-5 : `docs/PILOTAGE.md` (séparation CLOSEOUT → CLOSE-HANDOFF + CLOSE-FINAL)

**Excluded** :
- ❌ Renommage `07_CLOSEOUT.md` → `07_HANDOFF.md` (UN-C-1/2 : distinction logique)
- ❌ Modification de `07_CLOSEOUT.md.template` (déjà fait par Run 1 QW-2)
- ❌ Modification de `docs/AGENTIC_RUN_PROTOCOL.md` (phase 07 reste `CLOSEOUT`)
- ❌ Modification de `docs/CONVENTIONS.md` (concept HANDOFF/CLOSEOUT dans SESSION_RULES)
- ❌ Création d'ADR ou d'outil nouveau

## Risque canon

**Semi** — modifie `docs/PILOTAGE.md` (canon des routes). CANON_CHANGE_PROPOSAL validé par Brice.

## Pre-merge gate

**REQUIS** (route STRUCTURED). 5 vérifications P.R2 obligatoires.

## Acceptance criteria (depuis spec §8)

- ✅ CANON_CHANGE_PROPOSAL validé par Brice (`APPROVED`)
- ✅ `prompts/canonical/07-p-vbb-closeout.md` : section « Étape 1 — Calculer le kind » ajoutée
- ✅ `docs/SESSION_RULES.md` : section « Handoff vs Closeout » ajoutée
- ✅ `.gitignore` : `docs/SESSION.history/` ignoré
- ✅ `docs/SESSION.md` : note d'archivage ajoutée
- ✅ `docs/PILOTAGE.md` : routes `CLOSE-HANDOFF` et `CLOSE-FINAL` remplacent `CLOSEOUT`
- ✅ `docs/CONVENTIONS.md` / `AGENTIC_RUN_PROTOCOL.md` / `MVP_START_PROTOCOL.md` / `PHASE_TO_SKILLS.md` non modifiés
- ✅ Pre-merge gate (5 P.R2) passé
- ✅ `05_PATCH_SUMMARY.md` + `07_CLOSEOUT.md` créés avec `kind: CLOSEOUT`
- ✅ `docs/ACTIVITY_LOG.md` à jour
- ✅ git commit effectué

## Statut

**COMPLET** — intake validé par Brice, exécution autorisée et réalisée.