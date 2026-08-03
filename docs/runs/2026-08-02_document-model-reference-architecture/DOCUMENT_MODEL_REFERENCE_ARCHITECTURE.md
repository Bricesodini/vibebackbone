# Document Model Reference Architecture

## Status and scope

This document is an architectural reference for the documentary system. It
does not define a new model, protocol, ontology, implementation or migration.
It reuses only the established foundations:

- Document Identity Model (DIM);
- documentary ontology;
- Document Graph Model (DGM);
- Document Transition Protocol (DTP);
- Document Tag Specification (DTS).

The architecture describes how these foundations cooperate while preserving
their separate responsibilities. It is not itself an authority over the
artefacts that the system may later describe.

## 1. System overview

The documentary system can be understood as a controlled path from a stable
responsibility to observable, governed representations:

```text
DIM          -> identifies what the responsibility is
Ontology     -> qualifies the governed state of a representation
DGM          -> relates identities, representations, decisions and evidence
DTS          -> makes the contract of that state observable and comparable
DTP          -> governs transitions after findings and human decisions
```

The models are complementary:

| Foundation | Sole responsibility | It does not do |
|---|---|---|
| DIM | Preserve the stable identity of a documentary responsibility | Decide authority, validate a graph, or migrate a file |
| Ontology | Describe authority, lifecycle, temporality, functions and loading policy | Establish identity or create authority |
| DGM | Represent governed relations and provenance between documentary objects | Replace the source content or decide remediation |
| DTS | Expose a comparable contract for an artefact or documentary state | Create authority, identity or compliance |
| DTP | Route findings through decision, transition, validation and publication | Decide silently or authorize itself to modify an artefact |

The dependency direction is intentional. DIM supplies the stable referent;
the ontology qualifies it; DGM connects the qualified objects; DTS exposes
the resulting contract; DTP acts on findings only through the existing
governance and explicit human decisions.

No foundation is a second source of truth for another foundation. A tag may
describe an identity, but does not replace DIM. A graph may show an authority
relation, but does not create authority. A transition may produce a new
revision, but does not redefine an identity without a governed decision.

## 2. Logical architecture

The system has five logical layers. These layers are responsibility boundaries,
not new models.

### 2.1 Identity layer

**Responsibility:** DIM establishes the stable documentary identity behind a
responsibility and separates it from representations, revisions and
locations.

**Inputs:** a claimed documentary responsibility, its scope and evidence of
continuity or separation.

**Outputs:** an identity reference, representation relationships, revision
continuity and distinct locations.

**Dependencies:** none within the documentary model. Authority is related to
the identity only through a governed relation; a path, name or version cannot
provide that relation.

### 2.2 Qualification layer

**Responsibility:** the ontology qualifies a representation or revision using
the six-part tuple:

```text
(authority, lifecycle, temporality, primary_function,
 secondary_functions, load_policy)
```

**Inputs:** a DIM identity or representation, its applicable authority,
lifecycle, period, function and loading expectation.

**Outputs:** an interpretable ontological qualification, including
`MULTI_PERIOD` where one active artefact explicitly spans distinct periods.

**Dependencies:** DIM for the object being qualified. The ontology does not
infer authority from function, age, path, freshness or citation.

### 2.3 Relations layer

**Responsibility:** DGM represents relations among identities, authorities,
scopes, decisions, contracts, representations, revisions, locations,
projections, distributions, runtimes, evidence, findings and validations.

**Inputs:** identified and qualified objects, declared sources, decisions and
observable evidence.

**Outputs:** a traceable graph of source, derivation, distribution,
supersession, governance, implementation and validation relationships.

**Dependencies:** DIM for node continuity and the ontology for the state of
the related representations. DGM preserves direction and provenance; it does
not turn a relation into an authority by itself.

### 2.4 Transition layer

**Responsibility:** DTP governs the handling of findings and transitions while
preserving identity, provenance, reversibility and the existing governance.

**Inputs:** an anchored documentary state, independent findings, relevant
graph and tag validations, and a human decision where required.

**Outputs:** a routed decision, an authorized transition path, validation
results, publication state and historical evidence.

**Dependencies:** DIM, ontology and DGM to understand what is changing; DTS to
compare the declared and observed contract; Critical Rule 16 to prevent silent
correction and require the explicit `OUI`, `NON` or `PLUS TARD` decision.

### 2.5 Observability layer

**Responsibility:** DTS makes the documentary contract observable for an
artefact, a repository state or a validated publication state.

**Inputs:** identity, representation, revision, authority when claimed,
ontology values, provenance, source relations and the applicable documentary
contract.

**Outputs:** comparable tag information and compatibility findings such as
`COMPATIBLE`, `MIGRATION_REQUIRED`, `INCOMPATIBLE` or `UNKNOWN`.

**Dependencies:** DIM, ontology and DGM for the facts it exposes. DTS is
consumed by DTP, but it cannot authorize a transition or make an artefact
conform by declaration.

## 3. Documentary flow

The complete flow is a logical sequence. A physical file, repository commit
or runtime is only one possible representation or location within it.

```text
Creation
   ↓ DIM identifies the responsibility
Qualification
   ↓ Ontology describes its governed state
Relations
   ↓ DGM connects source, scope, provenance and dependencies
Validation
   ↓ DTS exposes the contract and checks observability
Decision
   ↓ Critical Rule 16 obtains human direction when drift is found
Transition
   ↓ DTP routes the authorized procedure
Publication
   ↓ DTS/DGM record the observable published state and relations
History
   ↓ DGM preserves revisions, decisions, findings and evidence
```

Creation does not make an artefact canonical. Qualification does not create
authority. Relations do not prove truth without evidence or an applicable
decision. Validation observes; it does not remediate. Decision precedes any
authorized transition. Publication records an outcome; it does not erase
previous revisions or evidence.

## 4. Validation architecture

The validation sequence is:

```text
DIM
  ↓
Ontology
  ↓
DGM
  ↓
DTS
  ↓
DTP
```

### DIM first

Validation must first know whether the compared objects represent the same
documentary responsibility. Otherwise a path change, copy or new responsibility
could be mistaken for a revision or a conflict.

### Ontology second

Once identity and representation are distinct, the system can qualify
authority, lifecycle, temporality, function and loading policy. This prevents
the graph from relating objects whose roles are still ambiguous.

### DGM third

Relations and provenance can then be tested against stable identities and
interpretable qualifications. This reveals orphan projections, authority
conflicts, broken derivations, incorrect supersession and untraceable
distribution paths.

### DTS fourth

The observable contract is meaningful only after its identity, qualification
and relations are known. DTS can then compare a representation or published
state with the declared contract without treating the tag as the source.

### DTP fifth

DTP routes the resulting findings. It must not decide before the preceding
observations exist, and it must not turn a validation result into an automatic
write.

## 5. Decision architecture

The responsibilities are deliberately separated:

1. **Validators observe.** DIM, ontology, DGM and DTS establish facts,
   relationships, qualifications and findings. They may report uncertainty;
   they do not correct the object under review.
2. **DTP routes.** DTP determines which transition logic applies after the
   finding and the human decision are available. It distinguishes correction,
   canon change, historical classification, archiving and deletion.
3. **Critical Rule 16 controls the decision point.** When a governed artefact
   is not aligned with the applicable canon, the agent qualifies the drift,
   makes no automatic change and requests `OUI`, `NON` or `PLUS TARD`.
4. **Existing governance authorizes remediation.** A `OUI` permits the
   appropriate procedure to be determined; it does not itself define a new
   canon or authorize unrelated changes.

No component may modify an artefact alone. In particular, a validator cannot
write a correction, a tag cannot promote itself to authority, a graph cannot
resolve an authority conflict silently, and DTP cannot bypass human or
existing governance requirements.

## 6. Propagation architecture

When a governed identity or its authoritative revision changes, propagation is
understood as a relation-preserving update, not as the creation of parallel
truths:

```text
Identity / authoritative revision
        ↓
Representations
        ↓
Projections and generated views
        ↓
Distributions
        ↓
Runtimes
        ↓
Tags and published-state observations
```

DIM keeps the identity stable across the path. DGM records source,
derivation, distribution and runtime relations. DTS makes each state
comparable with the applicable contract. DTP governs any transition required
when a downstream state no longer matches its source.

Propagation does not mean that every representation must be updated at once.
It means that every derived state must remain attributable to its source and
that divergence must be observable. A generated representation remains
generated; a distribution remains a distribution; a runtime remains a runtime.
None becomes canonical merely because it is newer or deployed.

## 7. Multi-repository architecture

Multiple Vibe Backbone repositories can share the same documentary contract
without becoming one repository or requiring global synchronization.

The shared elements may include:

- common documentary identities where the responsibility is genuinely shared;
- a common ontology and compatible DTS contract;
- common DGM relationship semantics;
- DTP and Critical Rule 16 as the transition and decision constraints.

Each repository may still have:

- a different contract revision;
- local representations and scopes;
- local projections and distributions;
- local runtime locations;
- local findings, decisions and evidence.

The identity remains common only when continuity and scope are explicitly
traceable. A shared name or shared tag is insufficient. Repository-local
projections must declare their source and contract compatibility. An older
contract can remain interpretable when it is compatible; otherwise DTS reports
the mismatch and DTP routes it. No repository is made current by proximity to
another repository, and no global synchronization is implied.

## 8. Model boundaries

The documentary system interfaces with, but does not absorb, the following
domains:

| External domain | Interface with the documentary system | What remains outside |
|---|---|---|
| Git | Supplies revisions, locations and publication evidence | Branching, merging, commit policy and repository mechanics |
| CI | Supplies validation results or run evidence | Pipeline orchestration and execution policy |
| Releases | May provide a published location or revision reference | Release management, version delivery and rollout policy |
| Business workflow | Supplies decisions, scopes or obligations when documented | Operational ownership and business execution |
| Code | May be related through contracts or implementation relations | Program semantics, behavior and source-code architecture |
| Memory | May preserve run context or handoff evidence | Human or agent memory as an authority source |
| LLM | May perform observation or routing under governance | Model identity, inference quality and autonomous authority |

These interfaces provide evidence or consumers. They do not change the
meaning of identity, authority, relation, tag or transition inside the
documentary model.

## 9. Global invariants

The combined architecture implies the following invariants:

1. A documentary responsibility has one stable identity at a given governed
   scope; a path, filename, version, tag or runtime cannot create another one
   by itself.
2. Authority is always a governed, scoped relation. It is never inferred from
   recency, generation, deployment, citation or function alone.
3. Every projection, distribution or runtime that claims documentary
   derivation remains traceable to a source identity and representation.
4. Qualification, relation, observability and transition remain distinct;
   none may silently perform the responsibility of another.
5. A secondary function never creates authority, and `MULTI_PERIOD` never
   makes the currently applicable rule ambiguous.
6. A tag describes a documentary contract; it cannot establish identity,
   authority, compliance or publication on its own.
7. A finding is independent of the remediation decision. An observed drift
   remains a finding until the applicable governance and human decision route
   it.
8. No artefact is modified solely because a validator, graph, tag or runtime
   comparison detected an inconsistency.
9. A transition preserves the identity and provenance of the prior state, or
   records an explicit governed identity break.
10. Historical evidence remains distinguishable from current authority and
    cannot certify the current state merely by being retained.
11. Publication records an observable state; it does not retroactively make
    every related representation conformant.
12. A repository-local state may differ from another repository's state while
    remaining interpretable, provided its identity, contract, scope and
    compatibility are observable.

## Conclusion

DIM, the ontology, DGM, DTP and DTS form one logical architecture without
becoming interchangeable sources of truth. DIM preserves continuity, the
ontology explains state, DGM explains relations, DTS exposes what can be
compared, and DTP governs how an observed difference may proceed. The result
is a documentary system that can represent current authority, derived states,
historical evidence and repository-local variation without collapsing them
into one another.

This reference architecture is ready to guide future implementation work
without itself authorizing implementation, migration or canon change.
