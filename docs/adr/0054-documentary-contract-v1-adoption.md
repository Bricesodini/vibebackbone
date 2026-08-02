---
status: accepted
date: 2026-08-03
document_convention: vbb-doc-v1
version: "1.0"
type: adr
visibility: public
tags: [adr, governance, contract, documentation, adoption]
relations:
  - "../document-model/DOCUMENT_IDENTITY_MODEL.md"
  - "../document-model/DOCUMENT_ONTOLOGY.md"
  - "../document-model/DOCUMENT_GRAPH_MODEL.md"
  - "../document-model/DOCUMENT_TAG_SPECIFICATION.md"
  - "../document-model/DOCUMENT_TRANSITION_PROTOCOL.md"
  - "../document-model/DOCUMENT_MODEL_REFERENCE_ARCHITECTURE.md"
  - "../runs/2026-08-03_document-model-canon-adoption/05_TRACEABILITY_MATRIX.md"
adr_id: "0054"
decision_status: accepted
decision_makers:
  - "Brice — explicit adoption decision"
  - "Codex — local implementation record"
---

# ADR 0054 — Documentary Contract v1 adoption

**Status**: ACCEPTED
**Date**: 2026-08-03
**Decision**: Adopt the Vibe Backbone Documentary Contract v1.0 as the
canonical documentary foundation at the six locations under
`docs/document-model/`.

## Context

The DIM, Ontology, DGM, DTS, DTP and reference architecture were validated as
a coherent candidate. The earlier design documents, POC, strategies, fixtures
and reports remain historical evidence. Ontology and DTP are primary sources
recreated in the adoption run; they are not retroactively closed historical
runs.

## Decision

The six canonical representations are:

1. `docs/document-model/DOCUMENT_IDENTITY_MODEL.md`
2. `docs/document-model/DOCUMENT_ONTOLOGY.md`
3. `docs/document-model/DOCUMENT_GRAPH_MODEL.md`
4. `docs/document-model/DOCUMENT_TAG_SPECIFICATION.md`
5. `docs/document-model/DOCUMENT_TRANSITION_PROTOCOL.md`
6. `docs/document-model/DOCUMENT_MODEL_REFERENCE_ARCHITECTURE.md`

The reference architecture records five distinct responsibilities: identity,
qualification, relations, transition, and observability. Validators C0-C5 and
the four aligned documentary skills remain experimental/internal capabilities;
they observe and route but do not become sovereign authorities. Existing
artefacts are not automatically compliant, qualified, or migrated by this
adoption.

F-04, F-06, and the deployed Pi runtime remain deferred or `NOT_ASSESSED`.
No runtime certification is implied. A document tag creates neither identity,
authority, nor compliance. This adoption remains compatible with Critical Rule
16, ADR-0053, and adversarial governance v1.2.

## Consequences

- The six locations are the unique canonical representations of the adopted
  documentary foundation.
- Historical design materials remain evidence and are not current authority.
- Future changes require the existing governed change and human-decision
  processes; no automatic migration follows from this ADR.
- Repository declaration and navigation may expose the authorities without
  classifying every existing artefact.

## Alternatives rejected

- Promoting the design runs directly: rejected because their run provenance was
  not a complete adoption cycle.
- Treating validators or tags as authority: rejected because observation and
  authority are distinct responsibilities.
- Certifying Pi or migrating all documents: rejected as outside this adoption.
