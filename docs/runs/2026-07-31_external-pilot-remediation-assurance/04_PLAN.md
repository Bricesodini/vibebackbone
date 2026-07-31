---
run_id: "2026-07-31_external-pilot-remediation-assurance"
phase: "04_PLAN"
document_convention: "vbb-doc-v1"
version: "1.0"
type: "run_artifact"
visibility: "internal"
status: "ready"
tags: [run, audit, documentation, governance, contract, security]
relations:
  - "01_INTAKE.md"
  - "POC.md"
  - "../../adr/0051-adversarial-assurance-dimension.md"
route: "STRUCTURED"
adversarial_level: "A2"
voie: "STRUCTUREE"
agent: "Codex"
started_at: "2026-07-31T12:00:00Z"
ended_at: "2026-07-31T12:20:00Z"
artifacts_produced: ["04_PLAN.md"]
---

# Plan

## Objectif

Fermer les trois bloqueurs RC confirmés du pilote documentaire et aligner A2
et A3 sous un profil versionné, sans réécrire l'historique ni déclarer une RC.

## Pré-conditions

Le dépôt est sur la branche isolée `codex/external-pilot-remediation-assurance`,
la gate ADR+POC passe, et Backbone Know est hors d'écriture.

## Étapes ordonnées

1. Reproduce the pilot evidence and create a finding-by-finding decision
   matrix: reproducibility, classification, criticality, RC-blocking status,
   and project-vs-contract ownership.
2. Import the existing v1 contract/linter implementation into this isolated
   branch, then remediate only confirmed RC blockers: progressive scopes and
   waivers, explicit namespaced status extensions, and `--suggest-scope`.
3. Add real pilot fixtures and preserve v1 compatibility; do not migrate
   Backbone Know or rewrite the pilot run.
4. Audit every A2 definition across ADRs, canon, templates, gates, tests and
   historical runs; record contradictions and impact.
5. Add a versioned A2/A3 clarification: A2 operational isolation, A3
   strengthened external independence, fail-closed gates, and historical
   compatibility. Propagate only the required Core authority references to
   the four distribution boot surfaces.
6. Execute focused tests, linter tests, fixture tests, A1/A2/A3 gate tests,
   architecture/contract lint, full suite, and closure checks.
7. Produce two independent closeout verdicts and explicitly keep RC readiness
   and unrelated RR blockers open.

## Critères d'acceptation

- Les findings F-PH1-01..10 et F-PH2-01 sont classifiés avec preuve.
- F-PH1-02, F-PH1-07 et F-PH1-10 sont fermés ou reclassifiés par test.
- Les profils A1/A2/A3 et la compatibilité historique v1.1 sont testés.
- La suite complète, les lints et la boucle de clôture passent.

## Plan de rollback global

Le commit est isolé sur cette branche. Un rollback consiste à supprimer la
branche et le worktree, sans toucher à Backbone Know ni à la branche source.

## Risques identifiés

- L'absence de repilot externe limite l'assurance d'adoption autonome.
- Les bloqueurs RR-BK-01..06 restent ouverts et ne sont pas couverts par ce run.
- La clarification v1.2 ne réinterprète aucun run historique v1.1.

## Gate before action

The linked POC is GO. The assurance clarification is linked to the existing
accepted ADR 0051 for compatibility analysis; a new ADR will record the
versioned decision and acceptance status.
