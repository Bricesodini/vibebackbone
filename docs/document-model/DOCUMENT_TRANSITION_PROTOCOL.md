# Document Transition Protocol (DTP)

## Purpose

DTP applies existing governance, the ontology, and Critical Rule 16 to a
documentary transition. It is not independent governance and cannot authorise,
select, or execute remediation by itself.

## Phases

| Phase | Input | Output | Invariant |
| --- | --- | --- | --- |
| 0. Anchor | Published/local/runtime observations and authority | Declared anchor, versions, scope | No state is authoritative only because newer or deployed |
| 1. Qualify | Observed artefacts | Ontology tuples and identities | Read-only qualification |
| 2. Detect | Qualifications and relations | Independent findings and evidence | Finding is separate from decision |
| 3. Decide | Finding | Human `OUI`, `NON`, `PLUS TARD` record | No remediation before response |
| 4. Route and transition | `OUI` record | Proposed procedure and controlled plan | Route proposes; it never writes |
| 5. Validate | Controlled-change evidence | Coherence, relation, version, contract results | No unproven runtime conformity |
| 6. Publish | Validated, approved state | Optional publication state and closure | Publication is not implicit adoption |

## Decision semantics

When a governed artefact is not aligned with applicable authority, the agent
qualifies the discrepancy, changes nothing automatically, and requests `OUI`,
`NON`, or `PLUS TARD`.

- `OUI` permits determination of a suitable procedure only: documentary
  correction, canon change, historical classification, archiving, or deletion.
- `NON` preserves the state and records the human decision.
- `PLUS TARD` records deferred documentary debt.

A canon-change proposal is required only when the selected remediation modifies
the canon. Procedure follows `OUI`; detection does not choose it.

## Invariants and boundary

1. Preserve identity and provenance, retaining prior state as identifiable
   evidence when a governed transition changes it.
2. Do not conflate a documentation correction and canon change in one action.
3. Do not treat historical evidence as current authority.
4. Insufficient authority, compatibility, source, or runtime provenance stops
   progress and remains `UNKNOWN`.
5. No validator, tag, graph, skill, or protocol component modifies an artefact
   alone.

DTP defines no tag syntax, migration tooling, Git workflow, or governance
hierarchy.
