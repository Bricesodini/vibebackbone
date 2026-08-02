# Document Tag Specification (DTS)

## Purpose

DTS is the comparable documentary-contract observation for an artefact or
repository state. It exposes facts; it neither creates identity or authority
nor requires a serialization or Git tag mechanism.

## Contract responsibilities

An interpretable tag declares or explicitly inherits identity, representation,
published revision, the ontology tuple, bounded authority scope, traceable
source for a projection or distribution, founding decision/provenance for an
asserted authority or transition, and applicable contract version. No field is
inferred silently from path, date, or filename.

The repository-level contract states its governing version, explicit
inheritance rules, and scope. An artefact without sufficient evidence remains
unknown rather than nonconforming by assumption.

## Compatibility outcomes

| Outcome | Meaning |
| --- | --- |
| `COMPATIBLE` | Observed contract is interpretable and compatible. |
| `MIGRATION_REQUIRED` | Observed contract is interpretable but needs a governed transition. |
| `INCOMPATIBLE` | Observed contract contradicts the applicable contract. |
| `UNKNOWN` | Required provenance, version, identity, source, or qualification cannot be concluded. |

## Invariants and boundary

1. Compatibility is never silently inferred.
2. A tag records authority; it cannot grant it.
3. A projection or distribution requires a declared traceable source.
4. An older contract is `COMPATIBLE` only through explicit evidence. When its
   version, provenance, or another required fact cannot be concluded, the
   outcome is `UNKNOWN`.
5. Artefact tag, repository state, and optional Git publication tag are distinct.
   A Git tag is publication evidence, not the documentary contract.
6. Historical artefacts can retain an earlier contract without being rewritten
   or presented as current.

DTS specifies responsibilities, not YAML, frontmatter, a database, or Git tag
syntax.
