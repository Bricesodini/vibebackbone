# Document Identity Model (DIM)

## Purpose

DIM answers what a governed documentary artefact is independently of its
physical form. An identity names a stable documentary responsibility. It is
not a path, filename, version, Git object, or runtime copy.

## Distinctions

| Term | Meaning | Does not mean |
| --- | --- | --- |
| Identity | Stable responsibility recognisable across change | Filesystem location or title |
| Representation | Material expression of one identity | New identity because it is copied or generated |
| Revision | Distinguishable state of a representation | The identity itself |
| Location | Where a representation is observed | Evidence of authority or identity |

One identity can have several representations and successive revisions. A
representation can be observed at more than one location. A generated
representation is a projection of its source identity; it never creates an
identity merely by being generated.

## Authority and invariants

Identity enables continuity; it does not create authority. Authority is
qualified by the ontology and established by observable governing evidence.

1. A path, filename, date, and version are observations, never identity proof.
2. A representation belongs to exactly one observed identity unless evidence is
   insufficient, in which case it is `UNKNOWN`.
3. A revision belongs to a representation and does not replace its identity.
4. A migration preserves identity unless an explicit governing decision creates,
   splits, merges, or retires a responsibility.
5. A projection or distribution preserves source identity and provenance; it is
   not independently canonical merely because it is current.
6. Unproven continuity remains `UNKNOWN`; no identity is inferred from location.

## Interfaces

The ontology qualifies an identified artefact; DGM records relations; DTS
exposes identity, representation, revision, and contract observations; DTP
uses identity to preserve continuity while routing findings. DIM decides
neither authority, compatibility, remediation, publication, Git policy, nor
tag format.
