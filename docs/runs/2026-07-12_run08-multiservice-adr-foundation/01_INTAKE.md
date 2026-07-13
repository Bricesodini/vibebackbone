---
run_id: "2026-07-12_run08-multiservice-adr-foundation"
phase: "01_INTAKE"
voie: "STRUCTURED"
status: "READY"
kind: "INTAKE"
agent: "pi"
started_at: "2026-07-12T00:35:00Z"
human_validated_by: "Brice Sodini (scope ADR-only, no runtime)"
---

# 01_INTAKE — Run 08 Multi-service ADR foundation

## Type de intake

**Kind** : `INTAKE` (STRUCTURED)
**Source spec** : [`docs/strategy/vbb-improvements-roadmap/runs/run-08-multiservice-adr-foundation.md`](../../strategy/vbb-improvements-roadmap/runs/run-08-multiservice-adr-foundation.md)
**Source stratégie** : [`docs/strategy/vbb-evolution-multi-service-support/`](../../strategy/vbb-evolution-multi-service-support/) (Phase 1, READY_FOR_PHASE_2)

## Goal

Produire 4 Architecture Decision Records (ADR) vibebackbone pour les gaps P0/P1 identifiés en Phase 1 multi-service. **Pas d'implémentation runtime** — décisions documentées seulement.

## Périmètre

**Inclus** :
- ADR-0005 (Gap-01, P1) — DB Orientation (CONTEXT.md extension)
- ADR-0006 (Gap-02, P1) — Project Archetype (CONTEXT.md extension)
- ADR-0007 (Gap-05, P0) — CONTRACTS_CONSUMED canonique (nouveau fichier)
- ADR-0008 (Gap-14, P1) — CONTEXT.md / PROJECT_MODE.md enrichi (vbb-project-init.py enrichment)
- Mise à jour `docs/adr/README.md` (index)

**Excluded** :
- ❌ Implémentation runtime (Run 9+)
- ❌ Création d'outils (`vbb-multiservice-lint.py`, etc.)
- ❌ Création de templates concrets (`CONTRACTS_CONSUMED.md.template`)
- ❌ Modification de canon `CONVENTIONS.md` / `PILOTAGE.md`
- ❌ ADR pour les autres gaps (Gap-03/04/06/07/08/09/10/11/12/13/15)

## Risque canon

**Faible** — les ADR sont des documents de design. Aucune modif directe de canon. Les outils et templates concrets sont diffés à des Runs ultérieurs.

## Pre-merge gate

**REQUIS** (route STRUCTURED). 5 vérifications P.R2 obligatoires.

## Acceptance criteria (depuis spec §8)

- ✅ 4 ADR créés
- ✅ Chaque ADR suit le template
- ✅ Chaque ADR a ≥ 2 alternatives rejetées
- ✅ `docs/adr/README.md` mis à jour
- ✅ Aucun canon non lié touché
- ✅ Pre-merge gate PASS
- ✅ `05_PATCH_SUMMARY.md` + `07_CLOSEOUT.md` créés avec `kind: CLOSEOUT`
- ✅ `docs/ACTIVITY_LOG.md` à jour
- ✅ git commit effectué

## Statut

**READY** — intake validé, exécution autorisée sur GO utilisateur.