# Document Model Proof of Architecture

## Status and scope

This proof applies DIM, the documentary ontology, DGM, DTS and DTP to a
bounded sample of real Vibe Backbone artefacts. It produces observations and
findings only. It does not add tags, change frontmatter, classify the rest of
the repository, correct drift, migrate artefacts or modify canon.

The DIM references, ontology tuples and DTS descriptions below are analytical
observations. They are not declarations that the repository already stores
these fields natively.

## 1. Method and sample

The sample contains eleven tracked artefacts and covers:

- canonical governance and architecture documents;
- an ADR that currently establishes a scoped authority;
- an older ADR that remains relevant as a decision record;
- a generated projection;
- a distribution source and its root runtime representation;
- a canonical prompt;
- completed run artefacts representing historical evidence.

For each artefact, the proof records:

1. the documentary identity observed by DIM;
2. the ontology tuple;
3. the DGM position and key relations;
4. the DTS contract that could be observed, including missing information;
5. a simulated drift and its DTP route.

No simulated drift is applied to the artefact. The route ends at a human
decision, as required by Critical Rule 16.

## 2. Sample classification

Notation:

```text
(authority, lifecycle, temporality, primary_function,
 secondary_functions, load_policy)
```

`SCOPED_AUTHORITY` means authority limited to the responsibility or runtime
scope explicitly described by the artefact. `NON_AUTHORITATIVE` means that the
artefact may be active or useful without prescribing the canon.

| # | Artefact | DIM identity | Ontology tuple |
|---|---|---|---|
| 1 | `AGENTS.md` | Governance Core agent-facing grammar | `(CANONICAL, ACTIVE, CURRENT, NORMATIVE, [REFERENCE], ALWAYS)` |
| 2 | `docs/ARCHITECTURE.md` | Canonical structured architecture source | `(CANONICAL, ACTIVE, CURRENT, NORMATIVE, [REFERENCE], ON_ROUTE)` |
| 3 | `docs/REFERENCE/pre-merge-gate.md` | P.R2 pre-merge gate reference | `(CANONICAL, ACTIVE, CURRENT, NORMATIVE, [REFERENCE], ON_ROUTE)` |
| 4 | `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` | Adversarial assurance domain governance | `(CANONICAL, ACTIVE, MULTI_PERIOD, NORMATIVE, [DECISION_RECORD, REFERENCE], ON_ROUTE)` |
| 5 | `docs/adr/0053-a2-a3-assurance-alignment.md` | A2/A3 assurance alignment decision | `(SCOPED_AUTHORITY, ACTIVE, MULTI_PERIOD, DECISION_RECORD, [NORMATIVE, REFERENCE], ON_ROUTE)` |
| 6 | `docs/adr/0001-formal-executor-boundary.md` | Formal executor boundary decision | `(SCOPED_AUTHORITY, ACTIVE, CURRENT, DECISION_RECORD, [NORMATIVE, REFERENCE], ON_ROUTE)` |
| 7 | `SYSTEM.md` -> `distributions/pi/SYSTEM.md` | Pi runtime posture representation | `(SCOPED_AUTHORITY, ACTIVE, CURRENT, NORMATIVE, [REFERENCE], ALWAYS)` |
| 8 | `distributions/pi/README.md` | Pi distribution responsibility and boundary | `(SCOPED_AUTHORITY, ACTIVE, CURRENT, REFERENCE, [DECISION_RECORD], ON_ROUTE)` |
| 9 | `prompts/canonical/04-p-vbb-plan.md` | Canonical PLAN prompt contract | `(SCOPED_AUTHORITY, ACTIVE, CURRENT, NORMATIVE, [REFERENCE], ON_DEMAND)` |
| 10 | `docs/RELATIONS.md` | Architecture relations projection | `(NON_AUTHORITATIVE, ACTIVE, CURRENT, GENERATED, [REFERENCE], ON_DEMAND)` |
| 11 | `docs/runs/2026-07-31_vbb-doc-v1-external-pilot/07_CLOSEOUT.md` | External pilot closeout record | `(NON_AUTHORITATIVE, RETIRED, PAST, RUN_ARTIFACT, [EVIDENCE, DECISION_RECORD], ON_DEMAND)` |

The classifications use responsibility and explicit relations, not file age or
path alone. In particular, the older ADR remains active because its decision
is still the documented boundary for a future executor; the historical
closeout is not current authority even though it contains a successful past
verdict.

## 3. Per-artefact proof records

### 3.1 `AGENTS.md`

- **DIM:** one identity for the compact, agent-facing Governance Core grammar.
  The file is the source representation; generated copies must not be pasted
  back into it.
- **Ontology:** canonical, active, current, normative, with reference as a
  secondary function, loaded always.
- **DGM:** `DOCUMENT_IDENTITY` governs the agent grammar and is related to
  `SYSTEM.md`, the canonical prompts, the skill catalog and the governance
  documents it references. It is the source for the compact rules, not a
  projection of a generated view.
- **DTS observation:** identity and representation are clear from the file and
  its references; authority, lifecycle and load policy are explicit in the
  governing content. A native DTS tag is not present as a separate object, so
  the contract is analytically reconstructable rather than independently
  machine-declared.
- **Simulated drift:** a Critical Rule in `AGENTS.md` contradicts the current
  governance while the referenced authority remains unchanged.
- **DTP route:** finding `drift in canonical normative source`; ask the human
  `OUI / NON / PLUS TARD`. No automatic edit. After `OUI`, the appropriate
  canon-remediation procedure is selected; `NON` records the decision; `PLUS
  TARD` records deferred documentary debt.

### 3.2 `docs/ARCHITECTURE.md`

- **DIM:** one identity for the canonical structured architecture source.
- **Ontology:** canonical, active, current, normative, with reference as a
  secondary function, loaded on route because architecture-sensitive work
  explicitly consumes it.
- **DGM:** source node for architecture blocks and the relations projection;
  `docs/RELATIONS.md` is `DERIVED_FROM` it and is not an independent authority.
  Architecture-sensitive files are connected through declared impact and file
  relations.
- **DTS observation:** source, status and projection relationship are
  explicit. The contract is observable, but no separate native DTS tag is
  present.
- **Simulated drift:** a generated relation is manually changed so it no
  longer corresponds to the architecture source.
- **DTP route:** finding `projection divergence`; request the human decision.
  A `OUI` can authorize the appropriate regeneration or correction procedure;
  the PoA does not execute it.

### 3.3 `docs/REFERENCE/pre-merge-gate.md`

- **DIM:** one identity for the unique P.R2 pre-merge gate reference.
- **Ontology:** canonical, active, current, normative, with reference as a
  secondary function, loaded on route for closeout and quality validation.
- **DGM:** governed by the quality and governance identities; referenced by
  `AGENTS.md`, `SYSTEM.md`, `docs/CONVENTIONS.md` and `docs/PILOTAGE.md`.
  These are `REFERENCES`, not competing copies of the gate.
- **DTS observation:** canonical status, reference-only role, and consumers are
  explicit. The tag is reconstructed from frontmatter and references rather
  than stored separately.
- **Simulated drift:** one consuming document reproduces an older P.R2 command
  sequence and claims it is the unique gate.
- **DTP route:** finding `parallel normative truth`; request a human decision.
  The route must preserve the single source relationship before any consumer
  is changed.

### 3.4 `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md`

- **DIM:** one identity for the adversarial assurance domain authority.
- **Ontology:** canonical, active, multi-period, normative, with decision
  record and reference as secondary functions, loaded on route. Its v1.2
  clarification preserves the meaning of historical v1.1 runs without
  retroactive reinterpretation.
- **DGM:** governed by the adversarial assurance identity and linked to the
  schema authority in `docs/GATE_ASSURANCE_GOVERNANCE.md`, ADR 0053, the
  adversarial validator and run artefacts. The links are scoped: schema shape
  and value meaning are not conflated.
- **DTS observation:** version, canonical status, ADR relation and referenced
  consumers are explicit. The multi-period qualification is required because
  the document describes both current v1.2 meaning and retained v1.1 history.
- **Simulated drift:** the v1.2 text is edited so that v1.1 run verdicts are
  reinterpreted retroactively.
- **DTP route:** finding `historical semantics changed by current text`; ask
  for the human decision before any remediation. No automatic normalization of
  the historical record is allowed.

### 3.5 `docs/adr/0053-a2-a3-assurance-alignment.md`

- **DIM:** one identity for the accepted A2/A3 alignment decision.
- **Ontology:** scoped authority, active, multi-period, decision record as the
  primary function, normative and reference as secondary functions, loaded on
  route. It records a past decision whose consequences remain current.
- **DGM:** `DECISION` establishes or modifies the scoped assurance relation;
  the ADR governs the v1.2 clarification and is related to the adversarial
  governance document. It does not govern unrelated assurance domains.
- **DTS observation:** accepted status, date, version, ADR identity and
  relations are explicit. The scope is inferable from the decision and its
  references, but a separate native tag is absent.
- **Simulated drift:** the ADR is marked rejected while the domain governance
  still declares its v1.2 clarification adopted.
- **DTP route:** finding `decision-status contradiction`; request human
  decision. A `OUI` requires reconciling the decision record and its governed
  authority through the existing governance; no status is changed here.

### 3.6 `docs/adr/0001-formal-executor-boundary.md`

- **DIM:** one identity for the formal executor boundary decision.
- **Ontology:** scoped authority, active, current, decision record as primary,
  normative and reference as secondary, loaded on route. Its 2026-05 decision
  remains applicable to the future executor boundary.
- **DGM:** the decision governs the executor boundary and is related to
  `docs/ARCHITECTURE.md`, generated relations, contracts and future runtime
  work. The ADR explicitly prevents generated projections from becoming
  canonical truth.
- **DTS observation:** status, route, date, decision and consequences are
  explicit. Its open follow-up is evidence of incompleteness of the future
  implementation, not evidence that the decision is historical only.
- **Simulated drift:** a later plan declares the executor to be authorized to
  rewrite governance policy autonomously.
- **DTP route:** finding `scoped decision boundary violated`; request human
  decision before any implementation or document correction.

### 3.7 `SYSTEM.md` -> `distributions/pi/SYSTEM.md`

- **DIM:** one identity for Pi runtime posture, with the root symlink as a
  representation/location and `distributions/pi/SYSTEM.md` as the distribution
  source representation.
- **Ontology:** scoped authority, active, current, normative for Pi runtime
  posture, with reference as secondary, always loaded. It does not replace
  `AGENTS.md` as the global rule source.
- **DGM:** the root path `LOCATED_AT` representation is linked to the Pi
  distribution source. The runtime representation is related to `AGENTS.md`
  through `CONSUMES`/`REFERENCES`, not through ownership of the global canon.
- **DTS observation:** the symlink and source relationship are observable;
  runtime role and load policy are explicit. The source file has a dated
  revision, so comparison to the current agent grammar remains necessary.
- **Simulated drift:** the root symlink points to a different distribution
  source whose runtime posture contradicts the active Pi source.
- **DTP route:** finding `representation-location mismatch`; ask the human
  decision. The route may later concern a distribution correction or runtime
  redeployment, but no such procedure is selected before `OUI`.

### 3.8 `distributions/pi/README.md`

- **DIM:** one identity for the Pi distribution boundary and ownership guide.
- **Ontology:** scoped authority, active, current, reference as primary, with
  decision record as secondary, loaded on route. It explains the distribution
  rather than prescribing the global governance grammar.
- **DGM:** related to `distributions/pi/SYSTEM.md`, the root symlink and setup
  material; it documents source versus consumer-owned runtime locations.
- **DTS observation:** distribution scope, active status and source/runtime
  boundary are explicit in content. The exact contract is not separately
  tagged, so compatibility is observable only through the referenced sources.
- **Simulated drift:** the README states that the Pi user directory is a
  repository source of truth, contrary to its current boundary description.
- **DTP route:** finding `distribution-boundary contradiction`; request the
  human decision before changing the README or any runtime state.

### 3.9 `prompts/canonical/04-p-vbb-plan.md`

- **DIM:** one identity for the canonical PLAN prompt contract.
- **Ontology:** scoped authority, active, current, normative as primary, with
  reference as secondary, loaded on demand when the PLAN route is selected.
- **DGM:** related to `PROMPTS_ARCHITECTURE.md`, the prompt library identity,
  the PLAN route and the skills that consume its output. It is a prompt
  representation, not a skill implementation.
- **DTS observation:** role, phase, output, input order and non-modification
  boundary are explicit. Its effective contract is comparable, but not stored
  as an independent DTS tag.
- **Simulated drift:** the prompt instructs the PLAN agent to modify files,
  contradicting its stated role.
- **DTP route:** finding `prompt-contract drift`; request human decision. A
  `OUI` would select the prompt-remediation procedure after the decision; the
  prompt is not silently rewritten.

### 3.10 `docs/RELATIONS.md`

- **DIM:** same architecture-relations identity as the generated projection,
  not a new architecture identity.
- **Ontology:** non-authoritative, active, current, generated as primary, with
  reference as secondary, loaded on demand.
- **DGM:** `PROJECTION` `DERIVED_FROM` `docs/ARCHITECTURE.md`; its graph nodes
  and edges are a view of the architecture source. It must not become a
  second source of truth.
- **DTS observation:** generated status and source are explicit in frontmatter
  and text. The projection is sufficiently identifiable for comparison, but
  generation revision and full source revision are not represented as a
  separate DTS object.
- **Simulated drift:** one relation is edited manually or differs from the
  source architecture.
- **DTP route:** finding `generated projection divergence`; ask the human
  decision. No direct edit is allowed; the post-decision procedure would be
  selected as a projection regeneration or an explicitly governed source
  change.

### 3.11 `docs/runs/2026-07-31_vbb-doc-v1-external-pilot/07_CLOSEOUT.md`

- **DIM:** one identity for the completed external-pilot closeout record.
- **Ontology:** non-authoritative, retired, past, run artifact as primary,
  evidence and decision record as secondary, loaded on demand.
- **DGM:** a `RUN_ARTIFACT` linked to the run's intake, audit, decision,
  execution, review, gate, POC and evidence. It records what that run
  observed; it does not govern the current repository.
- **DTS observation:** run identity, phase, status, verdict, governance
  versions and relations are explicit. Historical scope and evidence role are
  clear; no current-authority claim is justified.
- **Simulated drift:** a current governance document cites the pilot verdict as
  certification of the present state of main.
- **DTP route:** finding `historical evidence promoted to current authority`;
  ask for the human decision. The evidence remains preserved regardless of the
  `NON` or `PLUS TARD` outcome.

## 4. DGM integration result

The sample can be represented without adding a node type or relation:

```text
AGENTS.md
  ├── governs -> agent-facing governance identity
  ├── references -> SYSTEM.md, pre-merge gate, prompts and domain authorities
  └── constrains -> transitions and runtime consumption

ARCHITECTURE.md
  └── derived_into -> RELATIONS.md

ADVERSARIAL_ASSURANCE_GOVERNANCE.md
  ├── established/clarified_by -> ADR 0053
  └── referenced_by -> validator and governed run artefacts

SYSTEM.md root link
  └── located_at / represented_by -> distributions/pi/SYSTEM.md

PLAN prompt
  └── consumed_by -> PLAN route and related run artefacts

Historical closeout
  └── evidence_of -> completed run, never current canon
```

The proof finds no need for a second identity for the symlink, the generated
relations view or the historical closeout. Their representations and roles are
distinct, but their documentary responsibilities remain attributable to the
identities already described.

## 5. DTS integration result

The sample demonstrates that DTS can compare the relevant contracts, but also
shows the boundary between a conceptual specification and current repository
instrumentation:

- identity, role, status, source and references are often observable in
  frontmatter or content;
- generated status and source are explicit for `docs/RELATIONS.md`;
- symlink/source distinction is observable for the Pi runtime representation;
- a native, uniformly attached DTS tag is not present on every sample;
- missing revision, identity or inherited contract information must therefore
  remain `UNKNOWN`, not be inferred from the path or filename.

This is an observation about observability, not a request to add tags. It does
not contradict DTS: the specification explicitly allows an unknown or
unverified contract to produce a finding rather than silently declaring
compatibility.

## 6. DTP simulation result

Across the eleven simulations, the same routing invariant holds:

```text
observe -> qualify -> record finding -> ask OUI / NON / PLUS TARD
         -> only after OUI determine the appropriate procedure
```

The simulated findings fall into existing responsibilities:

| Finding observed | Responsible foundation | DTP consequence before human decision |
|---|---|---|
| Canonical rule contradicts current authority | Ontology + DGM | Stop; do not edit the normative source |
| Generated view diverges from source | DGM + DTS | Stop; do not edit the projection |
| Decision record contradicts domain authority | DGM + DTS | Stop; preserve both observations |
| Distribution or symlink points to another state | DIM + DGM + DTS | Stop; do not redeploy or rewrite |
| Prompt contract contradicts its role | Ontology + DTS | Stop; do not silently revise prompt |
| Historical evidence is cited as current authority | Ontology + DGM | Stop; preserve evidence and qualify the citation |

No finding requires a new conceptual model. The appropriate remediation, if
the human answers `OUI`, remains dependent on the artefact's existing
responsibility: canon correction, source/projection handling, distribution
handling, prompt handling or historical-record handling. The PoA does not
choose or execute that procedure.

## 7. Findings and observations

### Findings

1. **F-01 — Uniform DTS instrumentation is absent.** The repository exposes
   enough information to reconstruct several contracts, but not every sample
   has an independent native tag for identity, representation and revision.
   DTS therefore correctly requires `UNKNOWN` in cases where provenance cannot
   be established from existing content.
2. **F-02 — Runtime representation and distribution source are distinguishable.**
   The Pi symlink and `distributions/pi/SYSTEM.md` demonstrate that DIM and DGM
   can preserve one responsibility across multiple locations without making
   the runtime a new authority.
3. **F-03 — Generated projection is distinguishable from its source.**
   `docs/RELATIONS.md` declares its generated status and source, allowing DGM
   and DTS to detect divergence without treating the projection as canon.
4. **F-04 — Multi-period normative content is representable.** The adversarial
   governance document and ADR 0053 combine current applicability with
   retained historical semantics without requiring a new dimension.
5. **F-05 — Historical run evidence is separable from current authority.** The
   closeout record remains useful as evidence while its retired/past/run-artifact
   qualification prevents it from certifying the current state.

### Observations

1. The five foundations are sufficient for this sample to identify, qualify,
   relate, observe and route all simulated drifts.
2. No contradiction with the existing authority relationships was required to
   complete the sample. In particular, `AGENTS.md` remains the compact
   agent-facing source, `docs/ARCHITECTURE.md` remains the architecture source,
   and `docs/RELATIONS.md` remains a generated projection.
3. The proof depends on explicit content and relations; it does not use file
   age, filename, path or recency as a substitute for identity or authority.
4. The proof does not demonstrate that the entire repository is classified or
   that every artefact is already tag-complete. It demonstrates bounded
   applicability of the models.

## 8. Sufficiency assessment

| Capability | Result | Basis |
|---|---|---|
| Qualify current and historical state | PASS | Ontology separates authority, lifecycle, temporality and function; `MULTI_PERIOD` handles mixed periods |
| Preserve identity across copies and locations | PASS | DIM distinguishes identity, representation, revision and location |
| Relate source, projection, distribution, decision and evidence | PASS | DGM relations cover the sample without a parallel identity |
| Observe and compare documentary contracts | PASS WITH UNKNOWN CASES | DTS exposes available facts and leaves missing provenance unverified |
| Route drift without silent correction | PASS | DTP and Critical Rule 16 stop before remediation and require human decision |
| Preserve historical evidence without current certification | PASS | Ontology and DGM distinguish past run artefacts from current authority |

The `UNKNOWN` DTS cases are bounded observability findings, not a model
contradiction. They indicate that the existing repository state does not
uniformly expose every conceptual field; the proof does not add instrumentation
to resolve that limitation.

## Verdict

`PROOF_SUCCESSFUL`

The bounded real-repository sample demonstrates that DIM, the ontology, DGM,
DTS and DTP are sufficient to qualify, relate, validate and govern the tested
artefacts without introducing a new concept, modifying an artefact or
overriding existing canon. This verdict applies only to the sample and is not
a certification of the entire repository.
