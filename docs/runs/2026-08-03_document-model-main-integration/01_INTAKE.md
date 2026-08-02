---
run_id: 2026-08-03_document-model-main-integration
route: STRUCTURED
voie: STRUCTUREE
phase: 01_INTAKE
agent: codex
started_at: "2026-08-03T00:00:00Z"
ended_at: "2026-08-03T00:00:00Z"
artifacts_produced:
  - 01_INTAKE.md
  - 04_PLAN.md
  - 05_EXECUTION.md
  - 07_CLOSEOUT.md
adversarial_level: A2
adversarial_governance_version: "1.2"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
status: active
scope:
  - approved technical ports C0-C5
  - four documentary skills aligned to C0-C5
  - separately reconstructed F-02, F-03 and F-05 remediations
out_of_scope:
  - canonical adoption of DIM, Ontology, DGM, DTS, DTP or Reference Architecture
  - conceptual foundation documents
  - F-04
  - F-06 and Pi runtime
  - tags, publication, push and merge
---

# DOCUMENT_MODEL_MAIN_INTEGRATION — Intake

## Anchor

- integration branch: `codex/document-model-main-integration`
- current head: `da494ada2d2a58c740912f13bbab41a58482bc98`
- expected base: `origin/main@067b8ea6e9a7d9bea65a29340bdc38da1361f039`

The anchor was verified before opening this run: the remote main SHA matches,
`da494ad` descends from it, the target worktree was clean, and Critical Rule
16 was present once in `AGENTS.md` with its dedicated test.

## Objective

Port only the already-authorized technical capabilities and reconstruct only
the separately authorized documentary remediations. This run does not adopt
the conceptual foundations canonically.
