# Document Graph Model (DGM)

## Purpose

DGM records observable relations among identities, representations, revisions,
locations, sources, decisions, evidence, projections, distributions, and
authorities. It makes provenance and competing claims inspectable; it does not
replace source content or decide remediation.

## DGM v1 relation vocabulary

| Relation | Meaning | Essential constraint |
| --- | --- | --- |
| `REPRESENTED_BY` | Identity to representation | No second identity without governing decision |
| `REVISION_OF` | Revision to representation | Never inferred only from path or date |
| `LOCATED_AT` | Representation to location | Location is never identity |
| `GENERATED_FROM` / `PROJECTS` | Projection and source | Projection has traceable source |
| `DISTRIBUTED_TO` | Source to distribution/runtime representation | Divergence is observable |
| `REFERENCES` | Artefact cites another | Citation does not create authority |
| `GOVERNS` | Authority applies to responsibility | Scope is explicit |
| `ESTABLISHED_BY` | Authority/transition to decision | Authority has observable provenance |
| `SUPPORTED_BY` | Claim/decision to evidence | Evidence is not authority |
| `SUPERSEDES` | Current state to earlier one | Earlier revision remains identifiable |
| `CONFLICTS_WITH` | Incompatible claims/authorities | Conflict has no implicit winner |

The historical names `PART_OF`, `BOUNDED_BY`, `IMPLEMENTS`, `DERIVED_FROM`, and
`REPLACES` remain design evidence but are outside DGM v1. They have no implicit
meaning, alias, validation, or compatibility effect.

## Invariants

1. A representation without identity, or a projection without source, is a
   finding or `UNKNOWN`.
2. A projection cannot become canonical through derivation.
3. Two authorities govern one scope only when scopes are explicitly disjoint;
   otherwise they conflict.
4. A live dependency on a superseded revision is not silently valid.
5. Published, local, and runtime states are distinct observations; disagreement
   neither proves independence nor authorises overwrite.
6. Missing relation evidence produces `UNKNOWN` when it prevents a conclusion.

DIM supplies stable nodes; the ontology qualifies them; DTS exposes comparable
facts; DTP routes graph findings only after Critical Rule 16's human decision.
DGM has no autonomous correction path.
