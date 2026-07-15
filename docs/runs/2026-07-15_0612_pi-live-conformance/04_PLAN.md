---
run_id: "2026-07-15_0612_pi-live-conformance"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-15T06:18:00+02:00"
ended_at: "2026-07-15T06:20:00+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed: ["01_INTAKE.md", "02_AUDIT.md", "POC.md", "docs/adr/0047-runtime-conformance-benchmark.md"]
artifacts_produced: ["04_FIX_PLAN.md"]
---

# 04_PLAN — Pi live conformance compatibility

## Objectif

Rendre la sortie native Pi évaluable sans assouplir les décisions canoniques,
puis mesurer les dix scénarios live en lecture seule.

## Pré-conditions

- ADR 0047 accepté.
- POC de sortie Pi clôturé avec verdict GO.
- Integration gate `can_code_start=true`.
- Exécution live dans un clone Git jetable et propre.

## Étapes ordonnées

1. Declare and validate one finite canonical signal vocabulary.
2. Include that vocabulary in the live prompt without revealing scenario
   expectations.
3. Parse fenced JSON recursively inside provider wrappers.
4. Add regressions for vocabulary drift and Pi-shaped fenced event output.
5. Run focused tests, deterministic 40/40, P.R2, then all ten live Pi cases.
6. Evaluate results, document the measured verdict, and close the run.

## Critères d'acceptation

- Le flux Pi clôturé est extrait par un test représentatif.
- Les signaux inconnus sont refusés et les trois surfaces de vocabulaire sont
  vérifiées identiques.
- Le self-test reste à 40/40.
- Les dix appels Pi terminent sans mutation et donnent un verdict explicite.
- Le P.R2 complet passe avant commit.

## Plan de rollback global

Revenir sur le parser clôturé, le vocabulaire déclaré et leurs tests, puis
restaurer l'état documentaire antérieur. Ne jamais conserver seulement une
normalisation Pi qui masquerait les divergences de route.

## Risques identifiés

- Le modèle peut ignorer le vocabulaire ou retourner une route non canonique.
- Le format événementiel Pi peut évoluer à nouveau.
- Les temps de réponse live sont variables et les métriques de coût peuvent
  rester indisponibles.
