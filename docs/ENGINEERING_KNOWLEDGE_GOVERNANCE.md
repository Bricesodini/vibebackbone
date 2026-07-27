---
load_policy: reference
context_role: engineering-knowledge-governance
phase: transverse
status: active
version: "1.0"
updated: 2026-07-27
adr: "0049"
---

# Engineering Knowledge Governance

This document is the single authority for the lifecycle, evidence, review and
promotion of reusable engineering knowledge in Vibebackbone.

It governs how knowledge becomes authoritative. It does not contain the
engineering rules being promoted.

## Foundational principle — Governed capitalization

Every qualified implementation must be examined for reusable learning.
Learning must pass qualification, independent review and a human decision
before it is integrated into a documentary authority.

A delivery `PASS` closes the delivery question. It may open a governed
knowledge loop; it never promotes knowledge by itself.

## Two linked loops

### Delivery loop

```text
Implementation
→ Qualification
→ Independent delivery review
→ Delivery verdict
→ Closeout Knowledge Harvest
```

Every formal closeout records exactly one disposition:

- `NONE` — no reusable learning identified;
- `OBSERVATION_RECORDED` — a bounded observation was created;
- `EVIDENCE_LINKED` — evidence was linked to an existing candidate.

The closeout records or links evidence. It never promotes knowledge.

### Knowledge loop

```text
Observation
→ Candidate
→ Evidence accumulation
→ Knowledge audit
→ Independent knowledge review
→ Human promotion decision
→ Validated
→ Structured canonical integration
→ Independent integration review
→ Canonical
```

The loop reuses Vibebackbone's seven phases. It does not create phase 08.
`07_CLOSEOUT` remains the last artifact of every run.

## Maturity states

### OBSERVATION

A contextual fact, result, failure or comparison. It is non-normative and not
yet reusable.

Required evidence:

- source run or equivalent trace;
- precise context;
- observed outcome;
- no generalized rule.

Promotion to `CANDIDATE` requires:

- a reusable hypothesis;
- claimed scope and explicit non-scope;
- applicability and disconfirmation conditions;
- an owner;
- at least one traceable observation.

### CANDIDATE

A reusable hypothesis under qualification. A candidate is never an authority.

Required dossier:

- stable identifier and version;
- candidate type;
- claim, mechanism and expected outcome;
- claimed scope and boundaries;
- observations, validations and counter-evidence;
- shared assumptions and known limits;
- owner.

Promotion to `VALIDATED` requires:

- at least two independent validations in the claimed scope;
- a reproducible qualification method;
- explicit counter-example or disconfirmation search;
- a completed knowledge audit;
- a mandatory independent knowledge review;
- an explicit human promotion decision.

### VALIDATED

Reuse is demonstrated for the declared scope, but the knowledge is not yet
canonical.

Required:

- passed evidence gate;
- independent-review verdict;
- human decision and declared scope;
- identified final authority;
- migration, rollback and regression controls.

Promotion to `CANONICAL` requires:

- structured integration into one final authority;
- removal of any competing normative copy;
- verification appropriate to that authority;
- independent integration review;
- human confirmation that integration matches the promotion decision.

### CANONICAL

A versioned rule is authoritative within an explicit scope.

Required:

- stable identifier and version;
- exactly one final authority;
- links to source candidate, audit, review and decision;
- supersession metadata;
- regression controls.

## Independence of evidence

Independence is demonstrated, not inferred from the number of projects.

Every promotion dossier assesses:

1. **Occurrence independence** — evidence does not derive only from the same
   event, implementation or copied result.
2. **Context independence** — relevant conditions differ enough to challenge
   the claim.
3. **Actor independence** — at least one validation or qualification is
   performed by someone who did not author the candidate.
4. **Method independence** — evidence is reproduced or challenged through more
   than the candidate author's interpretation.
5. **Assumption independence** — shared assumptions are listed; broad claims
   require evidence across the assumptions they claim to cover.

At least two independent validations are required. Their sufficiency is judged
against the claimed scope. Two projects may be insufficient; two contexts
inside one project may be sufficient.

## Mandatory independent review

The knowledge auditor and independent reviewer are distinct roles.

The reviewer evaluates:

- evidence provenance and independence;
- claimed scope versus demonstrated scope;
- counter-evidence and failed validations;
- proposed final authority;
- promotion risks and regression strategy.

The reviewer recommends. Only a human approves, rejects, narrows or defers a
promotion.

## Documentary authority boundaries

| Artifact | Sole responsibility | Authoritative? |
|---|---|---|
| Governance | Lifecycle, roles, gates and promotion rules | Yes, for governance |
| Engineering standard | Normative reusable engineering rule | Yes, for the rule |
| Contract | Verifiable obligations at a boundary | Yes, for the boundary |
| ADR | Contextual decision and rationale | Yes, for that decision |
| Playbook | Operational procedure implementing an authority | No |
| Guide | Explanation and navigation | No |
| Knowledge record | Hypothesis, maturity and evidence history | No |
| Run | Execution evidence | No |
| Review | Independent evaluation evidence | No |
| Closeout | Harvest disposition and evidence links | No |

Promotion moves the rule to its final authority. The knowledge record then
retains history and links, not a competing normative copy.

## Patterns and anti-patterns

A pattern record contains:

- recurring context and problem;
- proposed mechanism or practice;
- expected outcome;
- applicability boundaries;
- independent validations and counter-evidence.

An anti-pattern record additionally contains:

- recurring failure mechanism;
- observed harm;
- conditions where the label does not apply;
- bounded corrective alternative when known.

Both follow the same maturity and promotion gates.

## Knowledge non-regression

Canonical knowledge is immutable.

Any semantic correction, weakening, extension or replacement:

1. creates a new `OBSERVATION`;
2. becomes a new `CANDIDATE` and version;
3. passes knowledge audit;
4. passes mandatory independent review;
5. receives a human decision;
6. is integrated as the new canonical version;
7. explicitly supersedes, but never erases, the prior version.

Direct semantic edits to a canonical knowledge version are prohibited.

## Roles

| Role | May do | May not do |
|---|---|---|
| Harvester | Record an observation or link evidence | Promote |
| Candidate owner | Maintain the claim and dossier | Self-validate |
| Knowledge auditor | Evaluate evidence and scope | Act as independent reviewer |
| Independent reviewer | Challenge audit and dossier | Modify reviewed evidence |
| Human authority | Approve, reject, narrow or defer | Delegate final promotion to automation |
| Integrator | Move an approved rule to final authority | Change approved meaning |

## Knowledge record lifecycle

Use [`templates/KNOWLEDGE_RECORD.md.template`](templates/KNOWLEDGE_RECORD.md.template).

The record:

- is a staging and evidence artifact;
- carries maturity and scope;
- links audit, review and human decision;
- names the final authority when promoted;
- becomes historical after promotion;
- never becomes the normative source.

Tools may validate structure, evidence presence and gate completion. Tools must
never decide promotion.

## Protocol version and compatibility

The v1 contract applies objectively to runs whose identifier is at or after
`2026-07-27_1712`, or whose declared `started_at` is at or after
`2026-07-27T15:12:21Z`, when they use an intake or closeout artifact.

Those runs must declare `knowledge_governance_version: "1.0"` in
`01_INTAKE.md` when present and in `07_CLOSEOUT.md`, plus a valid
`knowledge_harvest` disposition in the closeout. The version is a protocol
declaration, never an opt-in switch.

Earlier runs without this declaration predate the contract and remain valid.
They are not rewritten retroactively. FAST-MINIMAL runs, which have neither an
intake nor a closeout, remain governed by their existing activity-log contract.

## Promotion refusal conditions

Promotion is blocked when any of the following is true:

- fewer than two independent validations;
- claimed scope exceeds demonstrated scope;
- audit or independent review is missing;
- human decision is missing or not approved;
- final authority is absent or ambiguous;
- a competing normative copy would remain;
- supersession or rollback is undefined for an existing canonical rule.

## References

- [ADR 0049](adr/0049-engineering-knowledge-governance.md)
- [Agentic run protocol](AGENTIC_RUN_PROTOCOL.md)
- [Quality conventions](CONVENTIONS.md)
- [Canonical change proposal](runs/2026-07-27_1612_engineering-knowledge-governance/CANON_CHANGE_PROPOSAL.md)
