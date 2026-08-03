---
run_id: "2026-08-02_document-model-adoption"
artifact_kind: "post-adoption-roadmap"
status: "proposed"
---

# Document Model Roadmap — Post Adoption

## Principles

Post-adoption work remains incremental, bounded and reversible. Each step has
its own findings, human decisions, validation evidence and rollback point.
No step assumes that adoption makes existing artefacts conformant.

## Stage 1 — Stabilize the adopted core

- Close the adoption ADR and publish the approved v1.0 state.
- Resolve the full-suite regression before claiming a complete validation
  baseline.
- Keep the deployed Pi state explicitly `UNKNOWN` until its source and runtime
  provenance are observed.
- Preserve the first cleanup lot and its deferred DTS/runtime debts as evidence.

Value: a bounded, reviewable contract with known limitations.

## Stage 2 — Resume the living-core cleanup

- Reopen only the next bounded set of active core artefacts.
- Apply DIM, ontology, DGM, DTS and DTP in that order.
- Produce independent findings and request one human decision per remediation.
- Keep historical runs, proofs and projections out of current authority unless
  an explicit relation proves their role.

Value: gradual reduction of parallel truths without mass migration.

## Stage 3 — Extend coverage to active non-core artefacts

- Examine distributions, templates, prompt maps and other active artefacts in
  separate runs.
- Validate source/projection and distribution provenance before any rewrite.
- Treat missing contract evidence as `UNKNOWN` and route it separately from
  canon changes.

Value: consistent documentary observability beyond the boot set.

## Stage 4 — Generalize to other Vibe Backbone repositories

- Introduce the v1.0 contract as an available target for Backbone Know and
  future Vibe Backbone repositories.
- Let each repository declare its applicable authorities and local projections.
- Do not require global synchronization or assume identical scoped authority.
- Use DTS compatibility results to distinguish compatible adoption from a
  migration-required state.

Value: shared documentary language with locally governed authorities.

## Stage 5 — Migrate existing repositories deliberately

For each existing repository:

1. anchor the published, local and runtime states;
2. qualify artefacts without modifying them;
3. detect findings independently of decisions;
4. obtain explicit `OUI`, `NON` or `PLUS TARD` decisions;
5. apply only the approved procedure;
6. validate source, projections, relations and history;
7. publish or roll back as a separate human decision.

No repository is declared migrated because its files merely resemble the v1.0
shape. Identity continuity, provenance and validation evidence are required.

## Deferred work that must remain separate

- Expansion of DTS scope.
- Identification and possible redeployment of the Pi runtime.
- Any new canonical model or ontology.
- Mass archival, deletion or renaming.
- Changes to adversarial governance semantics.

## Stop conditions

Stop and request arbitration when an authority conflict, provenance break,
unknown runtime state, incompatible contract or validator regression prevents a
bounded conclusion. Preserve the finding and do not infer a migration.

## Status

`DOCUMENT_MODEL_ROADMAP_PROPOSED`

