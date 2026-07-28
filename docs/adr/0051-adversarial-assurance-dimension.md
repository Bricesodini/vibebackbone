---
status: accepted
date: 2026-07-28
decision_makers:
  - "Brice"
  - "AI arbitrator (M1)"
consulted:
  - "Distinct-actor independent review (08_INDEPENDENT_REVIEW_DISTINCT_ACTOR.md)"
  - "M1 arbitration (M1_DECISIONS.md)"
informed:
  - "Pi"
  - "OpenCode"
  - "Codex"
  - "Claude Code"
linked_adrs:
  - "0043-domain-verdict-runtime-status-orthogonality"
  - "0049-engineering-knowledge-governance"
  - "0050-design-certification-assurance-schema"
related:
  - "docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md (NEW — this ADR is the gate family charter)"
  - "docs/GATE_ASSURANCE_GOVERNANCE.md §Schema 1.1 (extended)"
  - "docs/runs/2026-07-28_1002_adversarial-loop-governance-design/ (design dossier)"
  - "docs/runs/2026-07-28_1200_m1-adversarial-loop-normative-arbitration/ (M1 arbitration)"
---

# ADR 0051 — Adversarial assurance dimension

**Status**: ACCEPTED (per M1 arbitration by external arbitrator)
**Date**: 2026-07-28
**Route**: STRUCTURED (M2 implementation)
**Décideur**: human explicit approval (post-M1)

## Context

ADR 0050 establishes the Design and Certification gate families, declaring
that "results are append-only and checkpoint-specific" and that "a later
result cannot overwrite an earlier checkpoint". This makes the conformance
loop robust against wishful thinking — but it leaves a systematic gap: every
gate is *confirmatory*. The cycle can legitimately emit `CLOSEOUT` with all
gates `PASS` on a delivery that nobody ever tried to break.

The adversarial assurance dimension addresses this gap by adding a
falsification duty — an obligation to actively attempt to break the
delivery — as a first-class, evidenced, fail-closed dimension of the
existing assurance schema (NOT a new route family, NOT a new phase, NOT a
parallel assurance block).

`docs/runs/2026-07-28_1002_adversarial-loop-governance-design/02_AUDIT.md`
documents 13 gap findings (AG-01..AG-13) that this ADR resolves.
`docs/runs/2026-07-28_1002_adversarial-loop-governance-design/03_DECISION.md`
documents 10 structural arbitrations (D1..D10) that this ADR confirms.

## Decision

Vibebackbone adds an **adversarial assurance dimension** to the canonical
cycle via **additive schema v1.1** of `ASSURANCE_STATUS`. No existing field
is removed or renamed.

1. **Fourth gate family** `ADVERSARIAL`, alongside `DESIGN`, `CERTIFICATION`
   and `OTHER` declared in ADR 0050. The new family has its own semantic
   ("the subject was subjected to a declared attack at a declared depth by
   a declared actor") and FAIL meaning ("a confirmed finding at or above
   the blocking severity is unremediated within the declared scope"). The
   enums `gate_family ∈ {DESIGN, CERTIFICATION, ADVERSARIAL, OTHER}` and
   `checkpoint ∈ {PRE_IMPLEMENTATION, POST_IMPLEMENTATION, COUNTER_PROOF,
   CLOSEOUT}` are declared explicitly in
   `docs/GATE_ASSURANCE_GOVERNANCE.md` §Schema 1.1 so that a v1.0 reader
   cannot silently re-inject `ADVERSARIAL` into `OTHER`.

2. **Fourth declared checkpoint** `COUNTER_PROOF`, alongside
   `PRE_IMPLEMENTATION`, `POST_IMPLEMENTATION`, `CLOSEOUT` from ADR 0050.
   A `POST_IMPLEMENTATION` `FAIL` is allowed to be overridden by a valid
   `resolution` link whose closing gate result is `PASS` at the
   `COUNTER_PROOF` checkpoint and references the finding identifiers.
   *Aggregation semantics are unchanged*: `checkpoint_aggregation` keeps
   its v1.0 invariant ("any required FAIL fails the checkpoint"). What
   changes is a separate, named `closure_evaluation` that uses the
   `resolution` link. A future implementation that collapses the two
   evaluations into one number is non-conformant.

3. **Four declared statuses**:
   - `implementation_status` ∈ {`NOT_STARTED`, `IN_PROGRESS`,
     `IMPLEMENTED`, `ABANDONED`};
   - `conformity_status` ∈ {`NOT_ASSESSED`, `PASS_CONFORMITY`,
     `FAIL_CONFORMITY`, `NOT_APPLICABLE`};
   - `adversarial_status` ∈ {`NOT_ASSESSED`, `NOT_REQUIRED`, `IN_CAMPAIGN`,
     `FINDINGS_OPEN`, `PASS_ADVERSARIAL`, `FAIL_ADVERSARIAL`};
   - `certification_status` ∈ {`NOT_CERTIFIED`, `CERTIFIED`, `SUSPENDED`,
     `NOT_APPLICABLE`, `UNASSESSED_LEGACY`}.

   No status may be inferred from another. A status without evidence is
   *invalid*, not merely undocumented. `NOT_ASSESSED` is the fail-closed
   default. `UNASSESSED_LEGACY` is reserved for pre-cutoff subjects (cf.
   §Compatibility) and is **distinct from `NOT_CERTIFIED`**.

4. **Three adversarial levels** `A0`/`A1`/`A2`, assigned by the criticality
   matrix in `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §Criticality
   Matrix. **Fail-closed default**: undeclared, ambiguous, or contested
   criticality → `A1`. The trigger `A2` on subjects with an existing
   `S0`/`S1` finding history uses a window of `N=10` runs. A "contested"
   classification is one for which a named gate expert has filed a written
   objection in `01_INTAKE.md` naming the trigger and rationale.

5. **Solo repository `A2` fallback**: a run requiring `A2` may be
   satisfied by `A2_DISTINCT_AGENT_PROXY` when no genuinely distinct human
   actor is available. The proxy MUST publish three identity disclosures
   (`{agent, llm, system_prompt_version}`) distinct from the defender's,
   and is subject to a quarterly external review per
   `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §A2 — Solo Repository
   Contract. A silent downshift `A2 → A1` is forbidden.

6. **`certification.owner`** owns the 5 revocation triggers
   (`ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §6.3) plus an SLA breach
   (cadence exceeded). Three mechanisms (`manual:<cadence>`, `cron:<expr>`,
   `webhook:<target>`) are declared per certification; cadence ≤ 90 days.
   Default `manual:quarterly`. SLA breach transitions the record
   automatically to `SUSPENDED`.

7. **Non-regression lock** at level `A2` requires `witnessed_by` (distinct
   from `discovered_by`) and `test_review` (PASS|FAIL verdict by a
   second agent or human). At level `A1`, the corpus entry is reviewed by
   a second agent within 30 days. The hypothesis that the oracle is
   correct and not a confirmation bias is falsifiable.

8. **`CERTIFIED`** is **not** an aggregate. It is a declared status whose
   `CERTIFIED` value is legal only when **13 named conditions** all hold,
   each individually evidenced, bound to one code state
   (`run_id` + commit + `corpus_version` + declared scope). The
   historical bound record remains valid for its bound state; the present
   claim transitions to `SUSPENDED` on any of 6 revocation triggers.

9. **`PASS_ADVERSARIAL`** carries a mandatory non-claim:
   "*a declared attack surface was exercised at a declared depth by a
   declared actor, and no unremediated confirmed finding remains within
   that scope. It does **not** mean the subject is correct, secure, or
   free of defects. Absence of finding is bounded evidence, never
   proof.*"

10. **Confirmed findings** route through the existing knowledge loop
    (`docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md`, ADR 0049) as
    anti-pattern observations. Promotion to `CONVENTIONS.md` or
    `AGENTS.md` is forbidden without transit through `OBSERVATION →
    CANDIDATE → KNOWLEDGE AUDIT → INDEPENDENT REVIEW → HUMAN
    DECISION → CANONICAL`. Critical Rule 5 (no parallel truth) is
    preserved.

11. **No new route family, no new phase, no parallel assurance block**.
    The cycle is additive. The technique skills already in `skills/2-vbb-*`
    and `skills/1-vbb-*` are referenced as providers; a new
    `2-vbb-adversarial-campaign` orchestrator is added in
    `skills/2-vbb-adversarial-campaign/SKILL.md` (per M2-29). The
    existing 7 phases (01..07) are reused.

12. **Distribution propagation**: per Critical Rule 12, the four
    active distributions (`pi`, `opencode`, `codex`, `claude`) must
    reference the new authority in their boot-set. The invocation glue
    remains in `distributions/`; the levels, statuses, verdict
    conditions and finding schema live in Core.

## Consequences

- Vibebackbone now distinguishes four claims (implemented / conforms /
  resists / certified) which were previously conflated.
- Review profiles increase from two to three in phase 06: the new
  `ADVERSARIAL_REVIEW` does not review the delivery's conformity; it
  reviews the campaign (attack list, depth, oracles, non-regression
  locks).
- A pre-existing informal practice (detect → remediate → re-review,
  as in run `2026-07-27_2145` review runs 01..03) gains a contract.
- Migration strategy (`docs/runs/2026-07-28_1002_*/05_MIGRATION_STRATEGY.md`)
  applies: M0→M6 phasing, R0→R2 enforcement ramp, grace rule keyed on
  `run_id` so that work in flight at stage activation completes under
  the prior stage.

## Compatibility

**Cutoff rule** (reuses ADR 0050 precedent):

```yaml
adversarial_governance_version: "1.1"
cutoff_run_key: "2026-07-28_1400"
cutoff_timestamp: "2026-07-28T14:00:00Z"
```

- At or after the cutoff: runs declare
  `adversarial_governance_version: "1.1"` in intake/closeout and carry
  a valid `adversarial` block, or a valid `A0` declaration (which
  itself requires a reason and survives classifier verification).
- Before the cutoff: runs remain valid under their original protocol.
  Readers preserve legacy semantics when the block is absent.
- `UNASSESSED_LEGACY` is reserved for pre-cutoff subjects that were
  never adversarially assessed. It is **not** `NOT_CERTIFIED` and is
  **not** a failure.

## Alternatives rejected

- **A new route family.** Vibebackbone already owns 5 routes plus the
  MVP START gate. Adding another would worsen the documented routing
  burden (W1 in `docs/WEAKPOINT_CONSOLIDATION_PLAN.md`).
- **A phase 08.** `ENGINEERING_KNOWLEDGE_GOVERNANCE.md` already ruled
  that a second loop reuses the 7 phases and "does not create phase 08".
- **Reusing `OTHER` for adversarial results.** `OTHER` is defined as
  outside both `DESIGN` and `CERTIFICATION`. Aggregation and closeout
  policy would not know how to reason about its results.
- **Extending `DESIGN`.** A break found under adverse conditions is not
  a specification hole. Corrupting `DESIGN` semantics is worse than
  adding a fourth family.
- **A parallel `ADVERSARIAL_STATUS` sibling**. CR#5 violation.
- **Reading a green pipeline as proof.** Forbidden by the mandatory
  non-claim attached to `PASS_ADVERSARIAL` (decision #9).

## Related files

- `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` (NEW — single authority for
  the domain: levels, statuses, lifecycle, verdict conditions, corpus
  contract, promotion matrix).
- `docs/GATE_ASSURANCE_GOVERNANCE.md` (EXTENDED — schema 1.1,
  `COUNTER_PROOF` checkpoint, `closure_evaluation`).
- `docs/PILOTAGE.md` (EXTENDED — triage step 6 + 7 fail-closed rules).
- `docs/CONVENTIONS.md` (EXTENDED — P.R5 strengthened).
- `docs/AGENTIC_RUN_PROTOCOL.md` (EXTENDED — third review profile).
- `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md` (EXTENDED — finding as
  anti-pattern producer).
- `docs/REFERENCE/pre-merge-gate.md` (EXTENDED — corpus execution as
  distinct check).
- `AGENTS.md` (NEW Critical Rule — propagates to four distributions).
- `tools/vbb-adversarial-gate.py` (NEW validator).
- `tools/vbb-gate-check.py` (EXTENDED).
- `tools/vbb-loop-closure-check.py` (EXTENDED).
- `docs/templates/ADVERSARIAL_CAMPAIGN.md.template` (NEW).
- `docs/templates/FINDING.md.template` (NEW).
- `docs/templates/01_INTAKE.md.template` (EXTENDED — contest_register,
  level declaration).
- `docs/templates/06_REVIEW.md.template` (EXTENDED — third profile).
- `docs/templates/07_CLOSEOUT.md.template` (EXTENDED — adversarial block).

FINAL_STATUS: ACCEPTED