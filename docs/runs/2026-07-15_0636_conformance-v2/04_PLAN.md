---
run_id: "2026-07-15_0636_conformance-v2"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-15T06:38:00+02:00"
ended_at: "2026-07-15T06:39:00+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed: ["01_INTAKE.md", "02_AUDIT.md", "POC.md", "docs/adr/0048-runtime-conformance-decision-model-v2.md"]
artifacts_produced: ["04_PLAN.md"]
---

# 04_PLAN — runtime conformance v2

## Objectif

Deliver a fair, strict, provider-neutral v2 benchmark without changing runtime
installation or weakening safety failures.

## Pré-conditions

- ADR 0048 accepted.
- POC verdict GO.
- Integration gate `can_code_start=true`.
- Clean worktree before the run.

## Étapes ordonnées

1. Version the manifest and result schema with the decomposed decision.
2. Update prompt construction and strict result validation.
3. Add multidimensional scoring and explicit repetitions.
4. Add regression coverage for contradictions, PARTIAL, repeats, and v1 refusal.
5. Update operator and architecture documentation.
6. Run focused verification and the complete P.R2 sequence.

## Critères d'acceptation

- All ten scenarios have one valid decision tuple.
- The prompt exposes every allowed output token without revealing expectations.
- Forbidden signals and mutations force FAIL.
- Decision-only or small required-signal misses can produce PARTIAL.
- One-call default and explicit repeated samples are both tested.
- Deterministic four-provider self-test and P.R2 pass.

## Plan de rollback global

Revert all v2 protocol surfaces together. Never mix a v2 manifest with a v1
schema or evaluator.

## Risques identifiés

- Breaking historical JSONL compatibility.
- A permissive PARTIAL threshold could hide unsafe behavior.
- Repetition accounting could misclassify duplicate or missing samples.
