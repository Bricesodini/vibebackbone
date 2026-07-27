---
run_id: "2026-07-27_1612_engineering-knowledge-governance"
phase: "03_DECISION"
status: "APPROVED"
agent: "codex"
created_at: "2026-07-27T14:25:00Z"
human_validated_by: "Brice — explicit final Core approval"
---

# Canon Change Proposal — Engineering knowledge governance

## Current Canon

Vibe Backbone governs reliable delivery through triage, seven agentic phases,
ADR/POC/integration gates, independent review and closeout. It does not define
what happens when delivery evidence reveals a reusable engineering learning.

The current canon contains adjacent protections:

- P.R3 gates action before execution;
- P.R8 prefers independent execution review;
- accepted ADRs are immutable and superseded by later ADRs;
- run artefacts remain evidence rather than active truth.

None of these defines a maturity model, evidence gate, independent knowledge
review, promotion decision or final-authority migration for engineering
knowledge.

## Problem

Without an explicit lifecycle:

- observations can be mistaken for reusable rules;
- patterns and anti-patterns can be promoted because they appear plausible;
- audit authors can become their own authority;
- rules can be copied into runs, playbooks or guides and form parallel truth;
- a promoted rule can be edited directly without renewed evidence;
- project-local learning can be over-generalized into Core.

## Proposed Canon

### 1. Two linked governance loops

The delivery loop remains:

```text
Implementation
→ Qualification
→ Independent delivery review
→ Delivery verdict
→ Closeout Knowledge Harvest
```

The closeout records exactly one disposition:

- `NONE` — no reusable learning identified;
- `OBSERVATION_RECORDED` — a bounded observation is created;
- `EVIDENCE_LINKED` — evidence is added to an existing candidate.

The closeout never promotes knowledge. A selected observation opens a distinct
knowledge run using the existing phases:

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

No phase 08 is created. `07_CLOSEOUT` remains the final artefact of each run.

### 2. Maturity states and transitions

#### OBSERVATION

Meaning: one contextual fact, failure, success or comparison.

Required:

- source run and precise evidence;
- context and observed outcome;
- no generalized normative wording.

Promotion to CANDIDATE requires:

- a reusable hypothesis;
- claimed scope and explicit non-scope;
- applicability and disconfirmation conditions;
- owner;
- at least one traceable observation.

#### CANDIDATE

Meaning: a reusable hypothesis under qualification, never an authority.

Required:

- stable identifier and maturity;
- claim, mechanism and expected outcome;
- claimed scope;
- evidence and counter-evidence;
- known limits and shared assumptions;
- candidate type: pattern, anti-pattern, qualification method, test strategy or
  engineering practice.

Promotion to VALIDATED requires:

- at least two validations that are independent in the claimed scope;
- reproducible qualification method;
- explicit counter-example or disconfirmation search;
- completed knowledge audit;
- mandatory review by an actor independent from the audit author;
- explicit human promotion decision.

#### VALIDATED

Meaning: reuse is demonstrated for the declared scope, but the knowledge is not
yet canonical.

Required:

- evidence gate passed;
- independent-review verdict;
- human decision and declared scope;
- target authority identified;
- migration, rollback and regression controls planned.

Promotion to CANONICAL requires:

- structured integration into one final authority;
- removal of any competing normative copy;
- verification appropriate to the target authority;
- independent integration review;
- human confirmation that the integration matches the promotion decision.

#### CANONICAL

Meaning: one versioned rule is authoritative within an explicit scope.

Required:

- stable identifier and version;
- one final authority;
- source candidate and decision links;
- supersession metadata;
- regression controls.

### 3. Independence of evidence

Independence is a demonstrated property, not a project counter.

Every promotion dossier must assess:

1. **Occurrence independence** — validations do not derive only from the same
   event, implementation or copied result.
2. **Context independence** — relevant operating conditions differ enough to
   challenge the claim.
3. **Actor independence** — at least one validation or qualification is
   performed by an actor who did not author the candidate.
4. **Method independence** — validation is reproduced or challenged through a
   method that is not merely the candidate author's interpretation.
5. **Assumption independence** — shared assumptions are listed; a broad claim
   requires evidence across the assumptions it purports to cover.

At least two independent validations are required. Their sufficiency is judged
against the claimed scope. Two projects may be insufficient; two contexts
inside one project may be sufficient.

### 4. Mandatory independent review

The knowledge auditor and independent reviewer are distinct roles.

The reviewer must assess:

- evidence provenance and independence;
- claimed scope versus demonstrated scope;
- counter-evidence and failed validations;
- documentary target and authority uniqueness;
- promotion risks and regression strategy.

The reviewer recommends; only a human decides promotion.

### 5. Unique authority

The promotion moves the rule to its final authority.

| Artefact | Responsibility | Authoritative? |
|---|---|---|
| Governance | Lifecycle, roles, gates and promotion rules | Yes, for governance only |
| Engineering standard | Normative reusable engineering rule | Yes, for the rule |
| Contract | Verifiable boundary obligations | Yes, for the boundary |
| ADR | Contextual decision and rationale | Yes, for that decision |
| Playbook | Operational procedure implementing an authority | No |
| Guide | Explanation and navigation | No |
| Knowledge record | Hypothesis, maturity and evidence history | No |
| Run | Execution evidence | No |
| Review | Independent evaluation evidence | No |
| Closeout | Harvest disposition and evidence links | No |

After promotion, the knowledge record retains identifiers, evidence, decisions
and a link to the final authority. It does not retain a competing normative
copy.

### 6. Pattern and anti-pattern lifecycle

A pattern record must include:

- recurring context and problem;
- proposed mechanism or practice;
- expected outcome;
- applicability boundaries;
- independent validations and counter-evidence.

An anti-pattern record must additionally include:

- recurring failure mechanism;
- observed harm;
- conditions under which the label does not apply;
- bounded corrective alternative when known.

Both use the same maturity and promotion gates.

### 7. Knowledge non-regression

Canonical knowledge is immutable.

A correction, weakening, extension or replacement:

1. creates a new Observation;
2. becomes a new Candidate and version;
3. passes knowledge audit;
4. passes mandatory independent review;
5. receives a human decision;
6. is integrated as the new canonical version;
7. explicitly supersedes, but never erases, the previous version.

Direct semantic edits to a canonical knowledge version are prohibited.

### 8. Roles and separation

| Role | May do | May not do |
|---|---|---|
| Harvester | Record observation or link evidence | Promote |
| Candidate owner | Maintain claim and evidence dossier | Self-validate |
| Knowledge auditor | Evaluate evidence and scope | Act as independent reviewer |
| Independent reviewer | Challenge audit and promotion dossier | Modify the dossier during review |
| Human authority | Approve, reject, narrow or defer promotion | Delegate the final decision to automation |
| Integrator | Move approved rule to final authority | Change the approved meaning |

## Benefits

1. Vibe Backbone governs both reliable delivery and durable method improvement.
2. Evidence quality scales with claimed scope rather than project count.
3. Independent review prevents audit self-authorization.
4. Unique-authority migration prevents parallel truth.
5. Canonical knowledge receives versioned non-regression.
6. The seven-phase protocol and historical runs remain compatible.

## Risks

1. Excessive process for low-value observations.
2. False claims of evidence independence.
3. Duplication between knowledge records and final authorities.
4. Invalidation of historical closeouts through over-eager enforcement.
5. Premature creation of a specialized skill before real usage evidence.

Mitigations:

- lightweight closeout disposition;
- explicit independence profile reviewed by a distinct actor;
- records lose normative wording after promotion;
- backward-compatible tool behavior;
- reuse existing phases and routing before considering a new skill.

## Impact Analysis

### Files

| File | Change type | Description |
|---|---|---|
| `AGENTS.md` | Additive governance | Compact Knowledge Harvest, independent review and non-regression rule |
| `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md` | New canonical authority | Own the lifecycle, roles, evidence and promotion boundaries |
| `docs/AGENTIC_RUN_PROTOCOL.md` | Additive protocol | Link delivery closeout to a separate knowledge run |
| `docs/CONVENTIONS.md` | Additive canon | Authority uniqueness, evidence independence and immutable versions |
| `docs/templates/KNOWLEDGE_RECORD.md.template` | New staging template | Non-authoritative candidate dossier |
| `docs/templates/07_CLOSEOUT.md.template` | Contract extension | Mandatory Knowledge Harvest disposition |
| `prompts/canonical/07-p-vbb-closeout.md` | Behavior extension | Harvest question and no-promotion rule |
| `docs/PILOTAGE.md` | Routing extension | Knowledge promotion enters AUDIT minimum |
| `skills/vibebackbone/SKILL.md` | Routing extension | Recognize knowledge-governance intent without a new worker skill |
| `docs/ARCHITECTURE.md` | Architecture update | Add knowledge governance responsibility and relations |
| `docs/RELATIONS.md` | Generated update | Regenerate from architecture |
| `docs/DISTRIBUTIONS.md` | Decision log | Record generic Core placement and four-runtime impact |
| `GUIDE.md`, `docs/INDEX.md`, `README.md` | Navigation | Explain and expose the second loop |

### Modules / Architecture Blocks

| Block | Impact | Action |
|---|---|---|
| Governance Core | Direct | Own lifecycle and routing |
| Prompt Library | Direct | Extend closeout behavior |
| Architecture Source | Direct | Map new canonical file |
| Audit Memory | Direct | Store candidate evidence history, not authority |
| Distribution adapters | Indirect | Verify propagation only |

### Skills

| Skill | Change needed | Priority |
|---|---|---|
| `vibebackbone` | Add routing triggers and point to canonical governance | P1 |
| New knowledge skill | Do not create in initial integration; require usage evidence first | DEFERRED |

Before any skill edit, its `CONTRACT.yaml` and `skills/INDEX.yaml` must be read
and validated.

### Prompts

| Prompt | Change needed | Priority |
|---|---|---|
| `07-p-vbb-closeout.md` | Mandatory harvest disposition and evidence links | P1 |
| `02-p-vbb-audit.md` | Knowledge-audit evidence dimensions | P1 |
| `06-p-vbb-review.md` | Explicit independent knowledge-review mode | P1 |
| `03-p-vbb-decision.md` | Human promotion decision boundaries | P1 |

### Tests

| Test | Must pass | Currently passing |
|---|---|---|
| Historical loop closure | Yes | Baseline to re-run correctly by run id |
| Template/prompt harvest alignment | Yes | Not implemented |
| Knowledge record schema validation | Yes | Not implemented |
| Promotion refusal without review/human decision | Yes | Not implemented |
| Architecture and contract lint | Yes | Baseline expected; integration not started |
| Four-distribution install smoke | Yes | Baseline expected; integration not started |

## Migration Plan

### Phase 1 — Canonical authority and vocabulary

- [ ] Accept ADR 0049 after independent review and final human decision.
- [ ] Add the single governance authority and knowledge-record template.
- [ ] Add navigation and architecture ownership.

### Phase 2 — Behavioral integration

- [ ] Extend audit, review, decision and closeout prompts.
- [ ] Extend closeout template with the three dispositions.
- [ ] Add routing to the existing orchestrator.

### Phase 3 — Backward-compatible enforcement

- [ ] Validate new candidate records algorithmically.
- [ ] Refuse promotion without audit, independent review and human decision.
- [ ] Preserve validity of historical runs.

### Phase 4 — Distribution and verification

- [ ] Verify Pi, OpenCode, Codex and Claude propagation.
- [ ] Run architecture graph regeneration and all P.R2 checks.
- [ ] Run an independent integration review.
- [ ] Close, commit and push only if every gate passes.

## Backward Compatibility

- [x] Grace period required — historical runs remain valid; new closeouts adopt
  the harvest contract after the effective canonical version.
- [ ] Fully backward compatible — no action required from consumers.
- [ ] Breaking change — consumer migration required.

## Human Decision

- [x] **Approved** — proceed with Core integration.
- [ ] **Rejected** — document rationale and close proposal.
- [ ] **Needs final decision** — independent review and impact analysis must be
  considered first.

**Run opening approved by**: Brice
**Core validator signature**: Brice
**Date**: 2026-07-27

## Verification Loop

- [ ] `python tools/vbb-architecture.py lint` → PASS
- [ ] `python tools/vbb-contract-lint.py` → 0 errors
- [ ] `python tools/vbb-loop-closure-check.py` → PASS
- [ ] `pytest tests/ -q` → all green
- [ ] `bash scripts/vbb-ci-local.sh` → all green
- [ ] `python tools/vbb-architecture.py graph --write` → RELATIONS updated
- [ ] Documentation links updated
- [ ] Independent integration review approved
- [ ] Closeout created

## Closeout Notes

Proposal phase only. No Core integration has started.

**Final status**: approved for the separately governed STRUCTURED integration
run after Review Run 02.
