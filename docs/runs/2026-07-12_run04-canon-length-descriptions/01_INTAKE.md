---
run_id: "2026-07-12_run04-canon-length-descriptions"
phase: "01_INTAKE"
voie: "STRUCTURED"
status: "READY"
kind: "INTAKE"
agent: "pi"
started_at: "2026-07-12T23:06:00Z"
human_validated_by: "Brice Sodini"
---

# 01_INTAKE — Run 04 Canon longueur descriptions

## Type de intake

**Kind** : `INTAKE` (STRUCTURED, après validation canon)
**Source spec** : [`docs/strategy/vbb-improvements-roadmap/runs/run-04-canon-length-descriptions.md`](../../strategy/vbb-improvements-roadmap/runs/run-04-canon-length-descriptions.md)
**Source canon proposal** : [`docs/strategy/vbb-improvements-roadmap/runs/run-04-CANON_CHANGE_PROPOSAL.md`](../../strategy/vbb-improvements-roadmap/runs/run-04-CANON_CHANGE_PROPOSAL.md) (status `APPROVED` by Brice)
**Source audit** : [`docs/audits/audit-E-skill-descriptions-20260712-1400.md`](../../audits/audit-E-skill-descriptions-20260712-1400.md) §AUDIT-E-001 (P1), AUDIT-E-003 (P2), AUDIT-E-005 (P2), AUDIT-E-006 (P2, créé par ce run)

## Goal (reformulé depuis spec)

Établir une cible canon **indicative** (≤ 500 chars / ≤ 10 lignes) pour la longueur du champ `description:` du frontmatter des `SKILL.md`, et instrumenter un **warning non-bloquant** dans `tools/vbb-contract-lint.py` qui signale les dépassements, sans casser la pertinence ni l'efficacité du routing.

## Périmètre

**Inclus** :
- R-E-1 : Ajout sous-section « SKILL.md description length » dans `docs/CONVENTIONS.md` (Pillar 1 Readability)
- R-E-2 : Ajout `check_description_length()` dans `tools/vbb-contract-lint.py` (warning non-bloquant)
- AUDIT-E-006 : Entrée de suivi dans `docs/AUDIT_STATUS.md` (analogue à LLM-LOAD-002)

**Excluded** :
- ❌ Compression manuelle des 10 descriptions Phase 1 > 500 chars — Run 5 ultérieur
- ❌ Promotion warning → error > 800 chars — Run futur après observation
- ❌ Pre-commit hook — reporté
- ❌ Création d'ADR — non requis (changement de conventions, pas d'architecture)
- ❌ Création d'outil nouveau (POC) — modification d'un outil existant
- ❌ R-E-3 (note dans 0-vbb-standard) — déjà couverte par Run 1 QW-1 (ligne 99)

## Risque canon

**Semi** — modifie `docs/CONVENTIONS.md` (canon), `tools/vbb-contract-lint.py` (outil), `docs/AUDIT_STATUS.md` (tracking). CANON_CHANGE_PROPOSAL validé par Brice avant exécution.

## Pre-merge gate

**REQUIS** (route STRUCTURED, cf. `docs/REFERENCE/pre-merge-gate.md`). 5 vérifications P.R2 obligatoires.

## Acceptance criteria (depuis spec §8)

- ✅ CANON_CHANGE_PROPOSAL validé par Brice (`APPROVED`)
- ✅ `docs/CONVENTIONS.md` : sous-section « SKILL.md description length » dans Pillar 1
- ✅ `tools/vbb-contract-lint.py` : `check_description_length()` ajoutée, 0 erreur, ≥ 0 warnings (5 actuellement)
- ✅ `docs/AUDIT_STATUS.md` : entrée `AUDIT-E-006` ajoutée
- ✅ Canon non lié intact (PILOTAGE / AGENTIC_RUN_PROTOCOL / MVP_START_PROTOCOL / PHASE_TO_SKILLS.md)
- ✅ Pre-merge gate (5 P.R2) passé
- ✅ Artefacts run créés avec `kind: CLOSEOUT`
- ✅ ACTIVITY_LOG.md à jour
- ✅ git commit effectué

## Statut

**COMPLET** — intake validé par Brice, exécution autorisée et réalisée.