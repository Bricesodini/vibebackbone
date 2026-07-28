---
run_id: "2026-07-28_1002_adversarial-loop-governance-design"
phase: "02_AUDIT"
voie: "AUDIT"
status: "READY"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
agent: "claude-code"
started_at: "2026-07-28T08:12:00Z"
ended_at: "2026-07-28T08:34:00Z"
next_phase: "03_DECISION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "INTEGRATION_GATE.md"
  - "AGENTS.md"
  - "SYSTEM.md"
  - "docs/PILOTAGE.md"
  - "docs/AGENTIC_RUN_PROTOCOL.md"
  - "docs/GATE_ASSURANCE_GOVERNANCE.md"
  - "docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md"
  - "docs/CONVENTIONS.md"
  - "docs/REFERENCE/pre-merge-gate.md"
  - "docs/REFERENCE/scoped-audit-protocol.md"
  - "docs/AUDIT_STATUS.md"
  - "docs/WEAKPOINT_CONSOLIDATION_PLAN.md"
  - "tools/vbb-gate-check.py"
  - "tools/vbb-loop-closure-check.py"
  - "skills/INDEX.yaml"
artifacts_produced:
  - "02_AUDIT.md"
---

# 02_AUDIT — Current cycle map and adversarial gap analysis

Read-only. No authority, tool, template, skill or test was modified.

## 1. Cartography of the current cycle

### 1.1 Control layers actually in force

| # | Layer | Authority | Mechanism | Enforced by |
|---|---|---|---|---|
| L1 | Triage into route families | `docs/PILOTAGE.md` §Triage rule | Declarative classification at intake | Agent discipline |
| L2 | MVP START readiness gate | `docs/MVP_START_PROTOCOL.md` | `0-vbb-rico-readiness`, verdict `READY/PARTIAL/BLOCKED/UNKNOWN` | Skill + route rule |
| L3 | ADR + POC + Integration gate | `AGENTS.md` CR#11, `GUIDE.md` §10bis | `tools/vbb-gate-check.py <run_dir>` → `can_code_start` | Exit code, pre-implementation |
| L4 | Phase discipline (01→07) | `docs/AGENTIC_RUN_PROTOCOL.md` | One artifact per phase, closure invariant | `tools/vbb-loop-closure-check.py` |
| L5 | Pre-merge verification loop | `docs/REFERENCE/pre-merge-gate.md` | 5 fixed commands, ordered | Exit codes, `--strict` = exit 2 |
| L6 | Credentials gate | `AGENTS.md` CR#13, ADR 0033 | `tools/vbb-credentials-gate.py` | pre-commit hook + CI |
| L7 | Scoped quality pass | ADR-0029, `07-p-vbb-closeout.md` step 4bis | Risk-triggered invocation of `1-vbb-*` / `2-vbb-*` skills | Closeout checklist |
| L8 | Assurance families and authorization | `docs/GATE_ASSURANCE_GOVERNANCE.md`, ADR 0050 | `ASSURANCE_STATUS` v1, `DESIGN`/`CERTIFICATION`/`OTHER`, fail-closed `implementation_authorization` | Closeout contract + tests |
| L9 | Independent review profiles | ADR 0050 §Independent review profiles | Phase 06 `DESIGN_REVIEW` and `CERTIFICATION_REVIEW` | Review artifact |
| L10 | Knowledge Harvest | `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md`, ADR 0049 | Closeout disposition `NONE` / `OBSERVATION_RECORDED` / `EVIDENCE_LINKED` | Closeout contract + tests |
| L11 | Runtime execution status | `docs/PILOTAGE.md` §LONG-RUN RULE, ADR 0043 | `FINAL_STATUS` verdict vocabulary | Output contract |
| L12 | Audit dashboard and risk register | `docs/AUDIT_STATUS.md`, `3-vbb-risk-register` | Active risk table, accepted-risk owners, reopen triggers | Human + closeout update |

### 1.2 The cycle as currently executed

```text
TRIAGE ──► 01 INTAKE ──► [L3 gate] ──► 02 AUDIT? ──► 03 DECISION? ──► 04 PLAN
                                                                        │
                                                                        ▼
                                             05 EXECUTION ──► 06 REVIEW ──► 07 CLOSEOUT
                                                   │              │            │
                                              (implements)   (DESIGN_REVIEW +  (L5 loop,
                                                              CERTIFICATION_    L8 assurance,
                                                              REVIEW)           L10 harvest)
```

### 1.3 What each existing gate actually asks

| Gate | Question it answers | Question it does **not** ask |
|---|---|---|
| L2 readiness | "Is the intent specified enough to build?" | "How could the specified intent fail?" |
| L3 ADR+POC | "Is the decision recorded and the hypothesis validated?" | "What breaks the decision's assumptions?" |
| L5 pre-merge | "Do the declared checks pass on the declared surface?" | "What is outside the declared surface?" |
| L8 `DESIGN` | "Is observable behavior fully specified?" | "Does the specified behavior hold under attack, stress, adverse ordering or hostile input?" |
| L8 `CERTIFICATION` | "Is the documentary proof coherent and traceable?" | "Is the proof *sufficient*, or only internally consistent?" |
| L9 review profiles | "Does the delivery match its plan, DoD and evidence?" | "Can the reviewer make the delivery fail?" |
| L10 harvest | "What reusable learning did success produce?" | "What reusable learning did *failure* produce?" |

**Structural conclusion.** Every layer in force is *confirmatory*: it verifies
that declared artifacts satisfy declared contracts. No layer carries a
**falsification duty** — an obligation to actively attempt to break the
delivery and to report the attempt's depth and its residual uncertainty.

## 2. What already exists and must not be reinvented

The proposal must be proportionate. Vibebackbone already owns most of the raw
material:

| Existing asset | Adversarial value | Missing wiring |
|---|---|---|
| `2-vbb-security`, `2-vbb-systemic-risk`, `2-vbb-data-integrity`, `2-vbb-db-robustness`, `2-vbb-api-auditor`, `1-vbb-error-handling-auditor`, `1-vbb-test-mirage-detector` | A latent attack-technique toolkit already exists as skills | Invoked ad hoc by L7 on risk trigger; no campaign contract, no coverage declaration, no verdict feeding a gate |
| `docs/REFERENCE/scoped-audit-protocol.md` | Bounded audit scoping already formalized | Scopes *audits*, not adversarial campaigns; no finding lifecycle |
| `AUDIT_STATUS.md` active-risk table with owners and reopen triggers | Proto finding register | Free-form table; no state machine, no per-finding evidence contract, no mechanical validation |
| ADR 0050 assurance schema | Extensible, append-only, fail-closed, versioned, with a compatibility cutoff | Two families only; no falsification family; no re-audit checkpoint |
| ADR 0049 knowledge governance, incl. **anti-pattern records** | The promotion path for confirmed failure knowledge already exists | Nothing routes findings into it; harvest is success-oriented in practice |
| P.R5 "Regression Prevention First" | Names the priority of regression over new tests | No corpus, no rule that a confirmed finding *must* become a permanent test |
| `06_REVIEW_RUN_01/02/03` pattern (run `2026-07-27_2145`) | De facto detect → remediate → re-review cycle already practised | Ad hoc: unnamed, uncontracted, not required, invisible to any gate |

**This is the strongest argument for the change and against over-engineering:**
the adversarial loop is *already practised informally*. What is missing is
naming, contracting and gating it.

## 3. Gap analysis

Findings are numbered `AG-nn` (audit gap). Severity uses the scale proposed in
`04_DESIGN_DOSSIER.md` §5.2.

| ID | Gap | Severity | Evidence |
|---|---|---|---|
| AG-01 | **No falsification duty anywhere in the cycle.** All gates are confirmatory; "no finding" is structurally indistinguishable from "not looked for". | S1 | §1.3 table; `GATE_ASSURANCE_GOVERNANCE.md` §Gate families defines only specification closure and proof coherence |
| AG-02 | **No canonical finding lifecycle.** A defect has no identity, no states, no evidence contract, no closure conditions. | S1 | `AUDIT_STATUS.md` §Active risks is a free-text table; no template in `docs/templates/` |
| AG-03 | **Remediation is not required to produce a fail-before test.** A fix may close a finding with no permanent regression lock. | S1 | P.R5 states a priority, not an obligation; `pre-merge-gate.md` runs the suite but never checks that a new case exists |
| AG-04 | **Re-audit / counter-proof is not a gate.** Nothing requires that the exact reproduction of a confirmed finding be re-executed after the fix by an actor other than the fixer. | S1 | Review runs 01–03 of `2026-07-27_2145` did this by discipline, not by contract |
| AG-05 | **Assurance schema has no dimension for robustness.** `DESIGN` PASS + `CERTIFICATION` PASS can coexist with zero break attempts, and closeout may reach `CLOSEOUT`. | S1 | `GATE_ASSURANCE_GOVERNANCE.md` §Closeout policy: "All required final gates PASS → CLOSEOUT is possible" |
| AG-06 | **Four claims are conflated into two.** "Implemented" is inferred from the presence of `05_EXECUTION.md`; "robust" has no representation; "certified" is not a declared status at all — only per-gate verdicts exist. | S1 | `GATE_ASSURANCE_GOVERNANCE.md` §Checkpoints: "There is no universal aggregate Certification verdict" |
| AG-07 | **Criticality does not drive verification depth.** Routes scale *process weight* by risk; nothing scales *falsification effort* by risk. | S2 | `PILOTAGE.md` §Triage rule maps risk → route only |
| AG-08 | **Exploration and regression are not distinguished.** Running the existing suite can be presented as "we tested it"; there is no separate notion of a novelty-seeking campaign. | S2 | `pre-merge-gate.md` command 5 is the only test obligation |
| AG-09 | **Failure knowledge is not harvested.** ADR 0049 supports anti-patterns, but no rule routes a confirmed finding into an observation/candidate. | S2 | `ENGINEERING_KNOWLEDGE_GOVERNANCE.md` §Patterns and anti-patterns has no producer |
| AG-10 | **Certification claims have no scope binding or expiry.** Nothing states that a verdict is bound to a commit, a corpus version and a declared surface, nor what revokes it. | S2 | ADR 0050 §Checkpoints binds results to `subject` but not to code state |
| AG-11 | **Accepted risks lack a mechanical contract.** Owners and reopen triggers exist as prose in `AUDIT_STATUS.md`; expiry and human approval are not required fields. | S2 | `AUDIT_STATUS.md` §Active risks |
| AG-12 | **Declarative enforcement risk is a known, recurring weakness.** W3 of the 2026-07-14 external evaluation already flagged log-only hooks and optional strictness. Adding an unenforced adversarial rule would repeat it. | S2 | `docs/WEAKPOINT_CONSOLIDATION_PLAN.md` §W3 |
| AG-13 | **No epistemic rule against overclaiming.** Nothing forbids reading a green pipeline as proof of correctness. | S2 | absent from `CONVENTIONS.md` and `GATE_ASSURANCE_GOVERNANCE.md` |

## 4. Constraint check against the request

| Requested distinction | Currently expressible? | Where it would have to live |
|---|---|---|
| implementation finished | Implicit only (presence of `05_EXECUTION.md`) | New declared status |
| conformity verified | Partially — L5 loop + `DESIGN` family, but no single declared status | New declared status aggregating existing evidence |
| adversarial robustness verified | **Not expressible** | New gate family + status + campaign artifact |
| final certification | **Not expressible** — ADR 0050 explicitly refuses a universal aggregate | New status with explicit, enumerable conditions |

The last line is the sharpest constraint: ADR 0050 deliberately refused a
global certification verdict because aggregating across checkpoints was
unsound. Any `CERTIFIED` status must therefore be defined as a **conjunction of
named, individually evidenced conditions bound to one code state**, not as an
average or a rollup. `03_DECISION.md` §D6 arbitrates this.

## 5. Blast radius of any future change

Documents, gates and closeouts that a future normative run would have to touch:

| Artifact | Change class | Note |
|---|---|---|
| `docs/GATE_ASSURANCE_GOVERNANCE.md` | Schema v1.1 (additive) + closeout policy amendment | Requires ADR |
| `docs/PILOTAGE.md` | Triage rule + criticality matrix pointer | Requires ADR |
| `docs/AGENTIC_RUN_PROTOCOL.md` | Phase 06 third review profile; no phase 08 | Constrained by ADR 0049 |
| `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md` | Finding → anti-pattern producer rule | Additive |
| `docs/CONVENTIONS.md` | P.R5 strengthened; new epistemic rule | Canon change proposal required |
| `docs/REFERENCE/pre-merge-gate.md` | Corpus execution as a distinct reported check | Canonical single source; must not be duplicated |
| `AGENTS.md` | New Critical Rule (adversarial assurance) | Boot-set file; propagates to 4 distributions (CR#12) |
| `docs/templates/` | `07_CLOSEOUT`, `06_REVIEW`, new `ADVERSARIAL_CAMPAIGN`, `FINDING` | Additive |
| `tools/vbb-loop-closure-check.py`, `tools/vbb-gate-check.py` | New validations | Requires tests |
| `docs/AUDIT_STATUS.md` | Becomes a *view* over finding records | Prevents parallel truth (CR#5) |
| `distributions/{pi,opencode,codex,claude}` | Propagation | CR#12 mandatory |
| `docs/CONTEXT.md`, `docs/INDEX.md` | Navigation entries | Additive |

## 6. Audit verdict

The gap is **real, systemic and S1**. The current cycle can legitimately emit
`CLOSEOUT` with all gates `PASS` on a delivery that nobody ever tried to break,
and no artifact would record that omission. The cycle is not wrong — it is
*incomplete in a way it cannot currently express*.

The correction is **available at low structural cost**: the assurance schema is
explicitly additive and versioned with a cutoff precedent, the knowledge loop
already accepts anti-patterns, the technique skills already exist, and the
detect → remediate → re-review pattern is already practised. The dominant risk
is not architectural, it is **process theater and enforcement drift** (AG-12).

Proceed to `03_DECISION`.
