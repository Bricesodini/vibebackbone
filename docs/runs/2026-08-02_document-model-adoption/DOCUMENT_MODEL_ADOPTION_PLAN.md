---
run_id: "2026-08-02_document-model-adoption"
artifact_kind: "adoption-proposal"
status: "proposed"
---

# Document Model Adoption Plan

## Purpose

This document prepares a human decision on the first canonical adoption of the
Vibe Backbone documentary system. It is a proposal only. It does not promote,
publish, tag, merge or modify any existing authority.

## 1. Official scope proposed for v1.0

The following models would become the normative documentary contract:

| Component | Proposed status | Responsibility |
|---|---|---|
| Document Identity Model (DIM) | Canonical | Stable identity, representation, revision and location distinctions. |
| Documentary ontology | Canonical | Authority, lifecycle, temporality, function and load policy. |
| Document Graph Model (DGM) | Canonical | Documentary identities, provenance, authority and dependency relations. |
| Document Transition Protocol (DTP) | Canonical | Human-gated observation, qualification, decision and transition routing. |
| Document Tag Specification (DTS) | Canonical | Meaning and compatibility responsibilities of documentary tags. |
| Reference Architecture | Canonical | The non-duplicating logical view of the five models and their order of use. |

Canonical means prescriptive within the declared Vibe Backbone documentary
scope. It does not make every existing artefact conformant, and it does not
override a domain authority such as adversarial assurance governance.

## 2. Material that remains non-canonical

| Material | Proposed status | Reason |
|---|---|---|
| Proof of Architecture | Historical evidence | Demonstrates sufficiency on a sample; does not prescribe the model. |
| Implementation Strategy | Planning artifact | Describes possible implementation sequencing. |
| Integration Plan | Planning artifact | Describes possible repository impacts. |
| Post-adoption Roadmap | Planning artifact | Describes future work and remains revisable. |
| C0 interface | Internal experimental | Coordinates validators; it is not a public documentary tag or new model. |
| C0-C5 fixtures and pilot reports | Internal experimental / evidence | Test data and observations; they do not qualify repository artefacts. |
| Validator findings and run records | Historical or run evidence | Record observations and decisions for a bounded run. |
| Existing aligned skill text | Operational consumer | Implements the contract after adoption; it is not an additional model. |
| `vbb-document-model-validation.py` | Internal tool, proposed compatible implementation | Executes pilot validation; its promotion requires the publication gates. |

No run document, fixture, test result or tool output becomes canonical merely
because it is recent or successful.

## 3. Proposed initial contract version

The candidate initial version is **Vibe Backbone Documentary Contract v1.0**.
It covers exactly the five canonical models and their reference architecture.
It does not absorb the existing adversarial, gate, distribution or runtime
governance contracts; those remain separate authorities connected through DGM
relations and DTP decisions.

### Compatibility

- A repository without an interpretable documentary contract remains `UNKNOWN`.
- An older contract may be `COMPATIBLE` only when the DTS validator has evidence
  for that result.
- A repository needing transformation is `MIGRATION_REQUIRED`; no migration is
  inferred or executed.
- An incompatible contract is `INCOMPATIBLE`.
- Existing untagged artefacts are not retroactively declared conformant.
- Historical evidence remains evidence and is not reinterpreted as current
  authority.

### Future migration rules

Future versions must be introduced through a governed DTP run. The run must
preserve DIM identity, make representation and revision continuity observable,
record compatibility before transformation, and retain the prior state as
identifiable evidence. No version may silently rewrite historical meaning or
promote a projection into authority.

## 4. Canonical changes to prepare, not execute

| Area | Exact candidate change | Current proposal status |
|---|---|---|
| Canonical documentary entry points | Add references to the adopted v1.0 contract in the appropriate existing authority documents. | Requires a separate approved canon change. |
| Adoption decision | Create one new ADR for adoption and scope, without reusing ADR 0052. | Required human decision; no ADR modified here. |
| ADR 0051 / ADR 0053 | Keep both decisions intact; preserve their distinct historical and v1.2 responsibilities. | No change proposed in this run. |
| Validators | Promote C1-C5 behavior as the supported validation implementation after the full validation gate passes. | Conditional; current pilot remains evidence. |
| Skills | Recognize the four aligned skills as supported consumers of C0-C5 and Critical Rule 16. | Conditional; current files are not changed here. |
| Tools | Recognize the validation tool as compatible only after its contract and regression gates pass. | Conditional; no tool change here. |
| Distributions | Publish compatible runtime representations only after source authority and propagation validation. | Deferred; no distribution publication here. |

The exact target files, including any source/projection pairs, must be confirmed
by a dedicated adoption execution run. This proposal intentionally does not
edit or classify them.

## 5. Human decisions required

1. Approve or reject the five-model canonical scope.
2. Approve or reject the candidate v1.0 contract boundary.
3. Approve the creation of a dedicated adoption ADR with a new number.
4. Decide whether C1-C5 and the four aligned skills are promoted together or in
   separately validated publication lots.
5. Resolve the current full-suite failure and the unknown deployed Pi state
   before claiming repository-wide or runtime adoption.

## Status

`DOCUMENT_MODEL_CANON_ADOPTION_PROPOSAL`

