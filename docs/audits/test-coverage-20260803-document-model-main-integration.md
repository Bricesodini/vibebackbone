---
audit: test-coverage
scope: document-model-main-integration
date: 2026-08-03
verdict: PARTIAL
---

# Test coverage audit — document model main integration

## Identified critical paths

- C0 result contract and authorized validation verdicts;
- DIM identity/representation/revision/location boundaries;
- Ontology dimensions and invalid combinations;
- DTS compatibility and DGM provenance relations;
- C5 finding normalization, human decisions and non-mutating routes;
- documentary skill consumption of C0–C5 and Critical Rule 16;
- F-02/F-03 adversarial governance and provenance alignment.

## Visible coverage

The C0–C5 pilot and documentary-skill alignment tests cover the positive,
negative and UNKNOWN cases required by the approved pilots. Targeted F-02/F-03
governance tests also pass. This report does not claim coverage of the Pi
runtime, distributions other than the edited source, or canonical adoption.

## Priority gaps

1. F-05 `docs/CONTEXT.md` still needs a separate fact-based update and test.
2. Full propagation across all distributions is not part of this lot.
3. Runtime Pi conformance remains unverified and is explicitly deferred.

## Recommended next tests

- focused parseability test for the recalculated F-05 next action;
- source/projection equivalence check for the edited Pi system representation;
- integrated C0–C5 and skill suite after F-05;
- adversarial gate on the completed run closeout.

## Unknowns and evidence limits

No runtime, publication, tag, merge or multi-deposit state was inspected as
part of this audit. The report is evidence for this integration run only.

