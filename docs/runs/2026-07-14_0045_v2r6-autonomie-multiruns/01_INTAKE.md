---
run_id: "2026-07-14_0045_v2r6-autonomie-multiruns"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-code"
started_at: "2026-07-13T23:16:00Z"
ended_at: "2026-07-13T23:20:00Z"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/strategy/vbb-improvements-roadmap/03_PLAN_REDUCTION_V2.md"
  - "docs/AGENTIC_RUN_PROTOCOL.md"
  - "docs/LONG_RUN_RULE.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — v2r6-autonomie-multiruns

## Demande reçue

> GO Brice « boucler le ponçage » — V2-R6 : protocole « run autonome »
> (N runs max sans checkpoint humain, loop-closure obligatoire entre runs,
> CLOSE-FINAL automatique après run terminé / CLOSE-HANDOFF réservé aux runs
> interrompus, stop conditions), consolidation AGENTIC_RUN_PROTOCOL +
> LONG_RUN_RULE en un protocole unique. Demande de fond Brice : « laisser
> itérer en autonomie sur plusieurs runs en maintenant l'hygiène
> audit → plan → implement → vérif/test par petits runs scopés ».

## Reformulation

Canoniser la conduite d'un agent qui enchaîne plusieurs runs sans humain :
bornes, gates inter-runs (fiables depuis V2-R1), discipline de clôture,
conditions d'arrêt. Un seul document porteur : `docs/AGENTIC_RUN_PROTOCOL.md`
gagne la section « Runs autonomes » et absorbe la fiche LONG_RUN_RULE
(réduite à un stub de redirection pour préserver les liens entrants).

## Scope

### Dans le périmètre
- `docs/AGENTIC_RUN_PROTOCOL.md` (section Runs autonomes + absorption fiche long-run)
- `docs/LONG_RUN_RULE.md` (→ stub de redirection)
- `docs/DISTRIBUTIONS.md` §7 (Rule 12)

### Hors périmètre
- Aucun outillage nouveau (le gate inter-runs = `vbb-loop-closure-check --strict`, livré V2-R1)
- PILOTAGE.md (les budgets long-run y restent canoniques, inchangés)

### Dépendances détectées
- ADR : `docs/adr/0031-autonomous-multirun-protocol.md`
- Prérequis plan V2 : V2-R1 (gates fiables) ✅ et V2-R4 (règle 40/75 + 4bis) ✅

## Classification du risque

- **Niveau** : `MODÉRÉ`
- **Justification** : règle de gouvernance transverse (conduite autonome des
  4 agents) ; additive — ne modifie aucun comportement supervisé existant.
