# Document Model Reference Architecture

## System

The documentary system has five non-overlapping responsibilities:

| Layer | Foundation | Input | Output |
| --- | --- | --- | --- |
| Identity | DIM | Responsibility, representations, revisions, locations | Stable identity or `UNKNOWN` |
| Qualification | Ontology | Identified artefact and governing evidence | Orthogonal tuple |
| Relations | DGM | Identities, provenance, decisions | Inspectable relations and conflicts |
| Transition | DTP | Findings and human decision | Proposed governed route, never execution |
| Observability | DTS | Applicable contract and observable facts | Compatibility outcome or `UNKNOWN` |

## Flow and validation order

Creation → DIM → Ontology → DGM → DTS → DTP → human decision → governed
transition → publication state → historical evidence.

DIM precedes qualification because path is not identity. The ontology precedes
graph validation because relation meaning depends on authority and lifecycle.
DGM precedes DTS because provenance is necessary to interpret compatibility.
DTS precedes DTP because unknown or incompatible contract is a finding to
route, not a condition to repair silently.

## Decision boundary and propagation

Validators observe. DTP routes. Critical Rule 16 establishes when a human
decision is required. Existing governance authorizes remediation. No layer can
modify an artefact alone.

An identity can have source, generated, distribution, and runtime
representations. DGM records provenance; DTS compares contract; no projection,
distribution, or runtime becomes a second truth. Repositories may share a
contract, use different versions, or project common identities locally without
mandatory global synchronization. Git, CI, releases, workflows, code, memory,
and LLMs remain external observation/evidence systems.

## Global invariants

1. Stable identity survives representation or location change.
2. Qualification is orthogonal: period, lifecycle, authority, function, and
   loading cannot substitute for another.
3. One responsibility has one applicable authority unless scopes are disjoint.
4. Derived representations preserve provenance and do not become canon merely
   by being current.
5. Compatibility and missing evidence are explicit; unknown is valid.
6. A finding is not remediation; remediation is never automatic.
7. Publication never rewrites historical meaning or certifies an unverified
   runtime.
