# POC — Read-only document model validation pilot

## Hypothesis

The experimental C0 interface and the minimal C1 DIM / C2 ontology validators
can qualify bounded fixture data derived from the eleven PoA artefacts, return
`PASS`, `FAIL`, `UNKNOWN` or `NOT_APPLICABLE`, and leave every source artefact
unchanged.

## Test boundary

- Inputs are fixture records only; no existing document receives a tag or
  frontmatter change.
- C1 checks identity, representation, revision and location distinctions.
- C2 checks the six established ontology dimensions and their existing
  invariants.
- Unknown identity, revision or contract data must remain `UNKNOWN`.
- DTS, DGM and DTP are not implemented in this POC.

## Success criteria

- positive and negative C0 interface tests pass;
- DIM detects orphan representations and location-as-identity misuse;
- ontology detects invalid values, multiple primary functions and forbidden
  combinations;
- the eleven PoA fixtures preserve the expected distinctions;
- no validator writes to the repository.

## Stop criteria

Stop the pilot if the implementation requires a new vocabulary, infers an
identity from a path or date, changes an examined artefact, or turns an
unknown fact into a passing qualification.

## Decision

Décision: GO

This POC authorizes only the bounded C0–C2 validation pilot. It does not
authorize DTS, DGM, DTP, skills, distribution, migration or publication work.
