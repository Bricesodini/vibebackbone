---
run_id: "2026-07-28_1002_adversarial-loop-governance-design"
phase: "03_DECISION"
status: "PROPOSED"
agent: "claude-code"
created_at: "2026-07-28T10:25:00Z"
human_validated_by: ""
---

# Canon Change Proposal — Adversarial assurance dimension

> **PROPOSED only.** No canon file was modified by the run that produced this
> proposal. Approval requires a genuinely independent review (see
> `06_INDEPENDENT_REVIEW.md` §1 and `COND-01`) and a human decision.

## Current Canon

`docs/GATE_ASSURANCE_GOVERNANCE.md` §Gate families:

> | `DESIGN` | Close observable behavior: contracts, ADRs, transactions, SQL,
> concurrency and history. | The product is not fully specified. |
> | `CERTIFICATION` | Certify coherence, traceability, references, oracles and
> proof. | The design may be closed, but the documentary proof is not certified. |
> | `OTHER` | Represent a named gate outside both families without corrupting
> their semantics. | The named gate failed under its own contract. |

`docs/CONVENTIONS.md` P.R5: *Regression Prevention First — Régression =
priorité #1 sur nouveau test.*

`docs/PILOTAGE.md` §Triage rule: risk class → route family.

## Problem

The canon verifies conformity and certifies proof. It contains no obligation
to **attempt falsification**, and no vocabulary to record that an attempt was
made, how deep it went, or what it left unexplored.

Concretely (`02_AUDIT.md` §3, findings `AG-01`…`AG-13`):

1. A delivery can reach `CLOSEOUT` with every gate `PASS` and zero break
   attempts; no artifact records the omission (`AG-01`, `AG-05`).
2. A defect has no identity, no lifecycle, no closure contract (`AG-02`).
3. A fix can close a defect with no test that failed before it (`AG-03`).
4. Re-verification after a fix is practised by discipline, not by contract
   (`AG-04`).
5. "Implemented", "conform", "robust" and "certified" are not four separable
   claims (`AG-06`).
6. Nothing scales falsification effort by criticality (`AG-07`).
7. Nothing separates hunting for new breaks from re-checking old ones
   (`AG-08`).
8. Confirmed failures do not feed the knowledge loop, although anti-pattern
   records exist for exactly that (`AG-09`).
9. Nothing forbids reading a green pipeline as proof of correctness (`AG-13`).

## Proposed Canon

Additive assurance schema `1.1` and one new authority document. Full design:
`04_DESIGN_DOSSIER.md`. Summary:

1. **Fourth gate family** `ADVERSARIAL`, alongside `DESIGN`, `CERTIFICATION`,
   `OTHER`.
2. **Fourth checkpoint** `COUNTER_PROOF`, with a `resolution` link on failing
   results. Checkpoint aggregation is unchanged; a separate, named
   `closure_evaluation` decides closeout.
3. **Four declared statuses**: `implementation_status`, `conformity_status`,
   `adversarial_status`, `certification_status`. No inference between them; a
   status without evidence is invalid.
4. **Three adversarial levels** `A0` / `A1` / `A2`, assigned by a trigger
   matrix; undeclared or contested → `A1` (fail-closed). Governance, prompt,
   skill, template and distribution changes are never `A0`.
5. **Canonical finding lifecycle**: detection → classification → arbitration →
   remediation → non-regression lock → gate update → counter-proof re-audit →
   knowledge harvest → closure, with reopening from any closed state.
6. **Explicit verdict conditions** for `PASS_CONFORMITY`, `PASS_ADVERSARIAL`
   and `CERTIFIED`, each an enumerated conjunction of evidenced conditions
   bound to one code state.
7. **Exploration ≠ regression**: a permanent corpus fed by every confirmed
   finding, executed at every level as a separately reported check; corpus
   execution never satisfies an exploration obligation.
8. **Six promotion destinations** answered explicitly for every confirmed
   finding; the normative destination routes through ADR 0049 only.
9. **Mandatory non-claim** attached to `PASS_ADVERSARIAL`: absence of finding
   is bounded evidence, never proof.

## Benefits

1. The four claims the request asks to separate become separately declarable,
   evidenced and machine-checkable.
2. A practice already performed informally (detect → fix → re-review) gains a
   contract, so it stops depending on the diligence of the session.
3. Confirmed failures become permanent assets: corpus entries, tests, gates,
   and — through ADR 0049 — anti-pattern knowledge.
4. Overclaiming becomes a contract violation rather than a matter of tone.
5. The cost is proportionate: `A0` is one declared line, and the corpus runs
   mechanically.

## Risks

1. **Process theater** — campaigns written to satisfy the gate (`MR-01`, S1).
2. **Enforcement drift** — vocabulary without validator, repeating weakness W3
   (`MR-02`, S1).
3. **Bureaucratic overload** on small changes (`MR-03`, S2).
4. **Corpus rot** through quarantine or deletion (`MR-04`, S2).
5. **Stale certification claims** (`MR-05`, S2).
6. **Two registers of findings** (`MR-06`, S2).
7. **Reviewer scarcity** — `A2` requires a distinct actor in a solo-maintained
   repository (`MR-07`, S2, **unresolved**, see `COND-04`).
8. **Level inflation** to `A2` (`MR-08`, S3).

## Impact Analysis

### Files

| File | Change type | Description |
|---|---|---|
| `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` | NEW | Single authority: levels, statuses, finding lifecycle, verdict conditions, corpus contract |
| `docs/GATE_ASSURANCE_GOVERNANCE.md` | MODIFY | Family `ADVERSARIAL`, checkpoint `COUNTER_PROOF`, schema `1.1`, closure vs aggregation, closeout policy delta |
| `docs/PILOTAGE.md` | MODIFY | Triage step 6 (level declaration); pointer to the new authority |
| `docs/AGENTIC_RUN_PROTOCOL.md` | MODIFY | Third phase-06 review profile; campaign artifact conventions; no phase 08 |
| `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md` | MODIFY | Findings as anti-pattern observation producers |
| `docs/CONVENTIONS.md` | MODIFY | P.R5 strengthened (confirmed finding ⇒ mandatory corpus entry); new epistemic rule on non-proof |
| `docs/REFERENCE/pre-merge-gate.md` | MODIFY | Corpus execution as a distinct reported check |
| `AGENTS.md` | MODIFY | New Critical Rule; boot set, propagates to four distributions |
| `docs/adr/00XX-adversarial-assurance-dimension.md` | NEW | Decision record |
| `docs/AUDIT_STATUS.md` | MODIFY | Becomes a view over finding records |
| `docs/CONTEXT.md`, `docs/INDEX.md` | MODIFY | Navigation entries |

### Modules / Architecture Blocks

| Block | Impact | Action |
|---|---|---|
| Assurance contract | Additive schema `1.1` | Update `docs/ARCHITECTURE.md`, regenerate `RELATIONS.md` |
| Gate tooling | New validator, two extended validators | New tests |
| Run artifacts | Two new templates | Additive |
| Distributions (`pi`, `opencode`, `codex`, `claude`) | Boot-set and prompt references | CR#12 propagation, `DISTRIBUTIONS.md` §Decisions log |

### Skills

| Skill | Change needed | Priority |
|---|---|---|
| `2-vbb-adversarial-campaign` (new) | Orchestrates existing technique skills into a contracted campaign | P1 |
| `t-vbb-adversarial-corpus` (new) | Corpus entry creation, quarantine, versioning | P1 |
| `2-vbb-security`, `2-vbb-systemic-risk`, `2-vbb-data-integrity`, `2-vbb-db-robustness`, `2-vbb-api-auditor`, `1-vbb-error-handling-auditor`, `1-vbb-test-mirage-detector` | Referenced as technique providers; no behavior change | P2 |
| `0-vbb-pilotage`, `0-vbb-standard` | Level declaration at triage | P1 |

### Prompts

| Prompt | Change needed | Priority |
|---|---|---|
| `0-p-vbb-triage` | Declare the adversarial level | P1 |
| `07-p-vbb-closeout` | Statuses, campaign verdict, promotion completeness | P1 |
| `2-p-vbb-audit-task` | Campaign shape for `A2` | P2 |
| `1-p-vbb-structured-task` | `A1` inline campaign | P2 |

### Tests

| Test | Must pass | Currently passing |
|---|---|---|
| `tests/test_adversarial_gate.py` (new) | Schema validation, fail-closed defaults, `resolution` links | n/a |
| `tests/test_loop_closure*.py` | Extended for `A1`/`A2` artifacts | yes (before change) |
| `tests/test_gate_check_*.py` | Extended for level classification | yes (before change) |
| `tests/test_engineering_knowledge_governance.py` | Non-regression on ADR 0049 contract | yes |
| `tests/test_runtime_conformance.py` | Four-distribution conformance | yes |

## Migration Plan

Full strategy: `05_MIGRATION_STRATEGY.md`. Phases M0 → M6, cutoff-based,
additive, with an enforcement ramp R0 → R2 and a grace rule keyed on `run_id`.

### Phase 1 — Communication
- [ ] Human decision recorded on this proposal
- [ ] Four-distribution impact review recorded in `DISTRIBUTIONS.md`
- [ ] Cutoff run key and timestamp declared

### Phase 2 — Parallel state
- [ ] Schema `1.1` active alongside `1.0`; v1.0 readers unaffected
- [ ] Pre-cutoff subjects declared `UNASSESSED_LEGACY`, never `NOT_CERTIFIED`
- [ ] Validator in advisory mode (R0)

### Phase 3 — Cutover
- [ ] `A2` enforcement (R1), then `A1` enforcement (R2)
- [ ] Corpus bootstrapped with `origin: HISTORICAL`
- [ ] Distributions propagated

### Phase 4 — Verification
- [ ] Architecture lint passed
- [ ] Contract lint passed
- [ ] Local CI passed
- [ ] Relevant pytest suite passed
- [ ] Documentation links updated
- [ ] No competing canon remains undocumented (`COND-05`)

## Backward Compatibility

- [x] **Fully backward compatible** — additive schema; no field removed or
      renamed; pre-cutoff runs keep their protocol and their verdicts; no
      existing baseline is downgraded.
- [ ] Grace period required — applies only to the *enforcement ramp*, not to
      the semantics.
- [ ] Breaking change — not applicable.

Consumer repositories adopt only through their own governed change, exactly as
for assurance v1.

## Human Decision

- [ ] **Approved** — proceed with migration plan
- [ ] **Rejected** — document rationale, close proposal
- [ ] **Needs revision** — return to author with feedback

**Conditions that must be satisfied before approval** (from
`06_INDEPENDENT_REVIEW.md` §5): `COND-01` (genuine independent review),
`COND-04` (`A2` distinct-actor fallback contract), `COND-05` (single authority
boundary), `COND-06` (interaction with autonomous-run sequences).

**Validator signature**: _________________________ **Date**: _______________

## Verification Loop

Required before any implementation can be declared complete (not applicable to
this proposal run, which changed no canon):

- [ ] `python tools/vbb-architecture.py lint` → PASS
- [ ] `python tools/vbb-contract-lint.py` → 0 errors
- [ ] `python tools/vbb-loop-closure-check.py <run> --strict` → PASS
- [ ] `pytest tests/ -q` → all green
- [ ] `bash scripts/vbb-ci-local.sh` → all green
- [ ] `python tools/vbb-architecture.py graph --write` → `RELATIONS.md` updated
- [ ] Documentation links updated
- [ ] Closeout created

## Closeout Notes

*To be filled after a future governed implementation run.*

**Final status**: _____________ **Closed by**: _____________ **Date**: ________
