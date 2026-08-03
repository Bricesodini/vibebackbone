---
run_id: "2026-08-02_document-model-adoption"
artifact_kind: "publication-proposal"
status: "proposed"
---

# Document Model Publication Plan

## Purpose

This plan defines a possible publication sequence for the proposed Vibe
Backbone Documentary Contract v1.0. It authorizes no publication activity.

## Publication gates and order

### 1. Preparation commit

Create a dedicated branch from the approved publication base. Keep the
adoption ADR, canonical model references, validators and skill/tool changes in
separate, reviewable commits. Do not mix them with cleanup, runtime deployment
or unrelated governance changes.

### 2. Canonical contract commit

Publish the approved adoption ADR and the minimum references that identify the
five canonical models and their scope. Validate authority uniqueness, model
references and absence of a second documentary truth.

### 3. Validator compatibility commit

Publish the C1-C5 implementation only after the C0 interface remains internal,
all allowed verdicts are preserved, `UNKNOWN` remains fail-closed, and the
validator cannot write artefacts. Validate positive, negative and unknown cases.

### 4. Skill consumer commit

Publish the four aligned skills as consumers of the canonical contract. Verify
that they produce findings, request `OUI` / `NON` / `PLUS TARD`, and never
remediate autonomously.

### 5. Distribution compatibility commit

Only after source validation, publish the compatible distribution
representations. For Pi, compare the repository source, generated or symlinked
representation and deployed runtime before claiming convergence. Unknown
runtime provenance blocks certification, not historical evidence retention.

## Validation order

1. DIM identity and representation checks.
2. Ontology tuple and invariant checks.
3. DGM relation and provenance checks.
4. DTS contract compatibility checks.
5. DTP finding, decision and routing checks.
6. Architecture, contract and convention lint.
7. Unit, integration, adversarial and full regression tests.
8. Human review of the adoption ADR, source/projection mapping and rollback
   evidence.

No later publication stage may mask a failed earlier stage.

## Tag and merge order

Tags are created only after the corresponding human decision and validation:

1. candidate documentary-contract state;
2. validated validator/skill compatibility state;
3. final v1.0 adoption state;
4. distribution publication states, if separately approved.

Tags must identify an immutable state and must not be moved to repair history.
Merges follow the same dependency order. A failed candidate is rejected or
reworked; it is not merged merely to preserve the tag sequence.

## Rollback

- Stop before the next dependent commit when a validation fails.
- Revert the publication commit that introduced the incompatible capability;
  do not rewrite or delete historical runs, ADRs or prior tags.
- If a distribution was published, restore the last validated distribution
  state and record the runtime comparison as a new finding.
- If an adoption tag exists, leave it immutable and publish a new corrective
  state only after a new decision and validation.
- A rollback never promotes an older projection over its source and never
  silently changes a DIM identity.

## Publication boundaries

Git publication, release publication, distribution deployment and documentary
contract adoption are related but distinct decisions. None is implied by the
success of a validator or by a clean merge.

## Status

`DOCUMENT_MODEL_PUBLICATION_PLAN_PROPOSED`

