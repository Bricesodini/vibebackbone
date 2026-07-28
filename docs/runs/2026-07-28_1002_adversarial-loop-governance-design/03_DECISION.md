---
run_id: "2026-07-28_1002_adversarial-loop-governance-design"
phase: "03_DECISION"
voie: "AUDIT"
status: "READY"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
agent: "claude-code"
started_at: "2026-07-28T08:34:00Z"
ended_at: "2026-07-28T08:52:00Z"
next_phase: "04_DESIGN_DOSSIER"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_AUDIT.md"
  - "docs/GATE_ASSURANCE_GOVERNANCE.md"
  - "docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md"
  - "docs/AGENTIC_RUN_PROTOCOL.md"
  - "docs/PILOTAGE.md"
artifacts_produced:
  - "03_DECISION.md"
---

# 03_DECISION — Structural arbitrations

Each decision states the options considered, the retained option, the reason,
and what the decision explicitly refuses. Decisions are **proposals**; none is
canonical until a separate governed run with its own ADR and human approval.

---

## D1 — Where does adversarial assurance live in the schema?

**Options**

| # | Option | Consequence |
|---|---|---|
| A | Reuse `OTHER` gate family | Adversarial results become invisible to family semantics; `OTHER` is defined as "outside both families", so aggregation and closeout policy cannot reason about them |
| B | Extend the `DESIGN` family | Corrupts `DESIGN` semantics ("the product is not fully specified") — a break found under adverse conditions is not a specification hole |
| C | Add a fourth family `ADVERSARIAL` in an additive `1.1` schema | Preserves existing semantics, extends aggregation and closeout deliberately, keeps `OTHER` for genuinely out-of-family gates |

**Retained: C.**

**Reason.** ADR 0050 states that `PASS/FAIL` is never interpreted without
`gate_family`; a robustness verdict carried by `OTHER` would be uninterpretable
by contract. `DESIGN` FAIL means "not fully specified" — semantically wrong for
"specified correctly but breaks under concurrency". A fourth family is the only
option that neither corrupts nor hides.

**Refused.** Creating a parallel `ADVERSARIAL_STATUS` block as a sibling of
`ASSURANCE_STATUS`. That would create a second assurance authority and violate
Critical Rule 5 (no parallel truth). Everything lands inside `ASSURANCE_STATUS`.

---

## D2 — Does the adversarial loop create a new phase?

**Options**: (A) new phase `08_ADVERSARIAL`; (B) reuse phases 01–07 with a
campaign artifact; (C) attach adversarial work exclusively to phase 06.

**Retained: B, with a third review profile in phase 06.**

**Reason.** `ENGINEERING_KNOWLEDGE_GOVERNANCE.md` already ruled that a second
loop reuses the seven phases and "does not create phase 08", and
`AGENTIC_RUN_PROTOCOL.md` §Règles dures states `07_CLOSEOUT.md` is always the
last artifact of a run. Repeating that precedent keeps one grammar. Option C is
insufficient: at level `A2` the campaign is a full run with its own intake,
scope, decisions and closeout, not a review pass.

**Consequence.** Two execution shapes:

- **Inline campaign** (level `A1`): the campaign artifact lives inside the
  delivery run and its verdict is a gate result at the `POST_IMPLEMENTATION`
  checkpoint.
- **Dedicated campaign run** (level `A2`): a distinct `AUDIT`-route run whose
  subject is the delivery, referenced by the delivery's closeout.

---

## D3 — How is the counter-proof (re-audit) represented without erasing history?

**Problem.** `GATE_ASSURANCE_GOVERNANCE.md` §Checkpoints is explicit: results
are append-only and "a later result cannot overwrite an earlier checkpoint";
aggregation says "any required `FAIL` makes the checkpoint fail". A finding
detected after implementation therefore writes a permanent `FAIL` at
`POST_IMPLEMENTATION`. Under the current closeout policy that run could never
final-close, even after a perfect fix.

**Options**

| # | Option | Consequence |
|---|---|---|
| A | Allow the counter-proof to overwrite the `POST_IMPLEMENTATION` result | Destroys the append-only invariant and hides that a break existed |
| B | Add a `COUNTER_PROOF` checkpoint, and a declared `resolution` link from the failing result to the closing one | History preserved; closure explicit; requires a documented amendment to the closeout policy |
| C | Never record the finding as a gate `FAIL`; record it only in the finding register | Findings become invisible to assurance; re-creates AG-05 |

**Retained: B.**

**Reason.** It is the only option that keeps the honest record ("this delivery
broke once, here is the proof it no longer does") while allowing closure. The
amendment is *deliberate and documented*, not a silent reinterpretation: the
closeout rule becomes "a required `FAIL` blocks closeout **unless** it carries
a `resolution` whose closing gate result is `PASS` at the `COUNTER_PROOF`
checkpoint and references the finding identifiers".

**Refused.** Any reading where the absence of a `COUNTER_PROOF` result is
benign. Absent or malformed `resolution` = still blocking (fail-closed, C4).

---

## D4 — Is adversarial work mandatory for every change?

**Retained: no — three declared levels, with a fail-closed default.**

- `A0_NONE` — no exploratory campaign. **Requires an explicit recorded
  declaration with a reason**; it is a decision, never an omission.
- `A1_TARGETED` — bounded campaign on the changed surface and its immediate
  blast radius.
- `A2_FULL` — full campaign across declared attack-surface classes, distinct
  actor, human decision, counter-proof.

**Fail-closed default (C4).** When criticality is undeclared, ambiguous, or the
classifier disagrees with the declaration, the level is `A1`, never `A0`.

**Refused.** A level that exempts a change from the **regression corpus**. The
corpus is part of the mechanical test surface and runs for every change at
every level (see D5). `A0` exempts *exploration*, never *regression*.

---

## D5 — Exploration and regression: one mechanism or two?

**Retained: two mechanisms, structurally separated, never substitutable.**

| Dimension | Exploration | Regression |
|---|---|---|
| Goal | Find an unknown break | Prove a known break stays fixed |
| Lifetime | Campaign-scoped | Permanent |
| Trigger | Criticality level `A1`/`A2` | Every change, mechanically |
| Location | Campaign artifact + finding records | Adversarial corpus, executed by the test surface |
| Success | Declared surface exercised at declared depth | 100 % of applicable corpus entries pass |
| Growth signal | New findings | New corpus entries derived from confirmed findings |

**Hard rule.** Executing the corpus **can never satisfy** an exploration
requirement. A campaign whose only activity was corpus execution declares
`exploration_performed: false` and cannot yield `PASS_ADVERSARIAL` at `A1`/`A2`.

**Reason.** This is the central failure mode of "we do adversarial testing"
programs: the regression suite grows, the team stops hunting, and coverage
metrics rise while real assurance falls. Separating the two makes the
substitution mechanically detectable.

---

## D6 — What kind of object is `CERTIFIED`?

ADR 0050 deliberately refused a universal aggregate certification verdict
because aggregating across checkpoints is unsound.

**Retained:** `certification_status` is **not** an aggregate. It is a declared
status whose `CERTIFIED` value is legal only when an **enumerated conjunction
of individually evidenced conditions** holds, **bound to one code state**
(`run_id` + commit + corpus version + declared scope). Each condition names the
artifact that evidences it. Nothing is inferred, averaged or rolled up.

**Consequence.** `CERTIFIED` is *revocable by construction*: a new confirmed
finding in scope, a corpus version change, or a scope change moves it to
`SUSPENDED`. Certification is a statement about a frozen state, not a property
of the project.

---

## D7 — Who arbitrates a finding?

**Retained: severity-dependent authority.**

| Severity | Who may arbitrate the disposition | Agent may |
|---|---|---|
| `S0` | Human only | Propose, never decide |
| `S1` | Human only | Propose, never decide |
| `S2` | Agent may decide `REMEDIATE`; `ACCEPTED_RISK` and `REJECTED` require a human | Decide only toward more work, never less |
| `S3` | Agent may decide any disposition, recorded and reviewable | Full |

**Reason.** The asymmetry is deliberate: an agent may always escalate work, and
may never unilaterally reduce assurance. This mirrors
`ENGINEERING_KNOWLEDGE_GOVERNANCE.md` §Roles ("Only a human approves, rejects,
narrows or defers") and Critical Rule 2.

---

## D8 — Where do confirmed findings become durable knowledge?

**Retained: the existing knowledge loop, with findings as a new producer.**

A confirmed finding produces an `OBSERVATION` (ADR 0049 maturity model). If it
generalizes, it becomes a `CANDIDATE` anti-pattern and follows the existing
promotion path: knowledge audit → independent knowledge review → human decision
→ structured integration → `CANONICAL`.

**Refused.** A direct path from "finding" to "normative rule". Promotion into
`docs/CONVENTIONS.md` or `AGENTS.md` must not bypass ADR 0049. The finding
register is evidence, never authority.

---

## D9 — New route family?

**Retained: no.** The adversarial campaign runs under the existing `AUDIT`
route. `docs/PILOTAGE.md` keeps five route families plus the MVP START gate;
only the triage rule gains a criticality-declaration step.

**Reason.** Route inflation is a documented Vibebackbone weakness (W1,
`WEAKPOINT_CONSOLIDATION_PLAN.md`: 64 skills, neighbouring perimeters, high
routing load). The change must add a *dimension*, not a *branch*.

---

## D10 — Enforcement posture

**Retained: mechanical validation from day one, with a declared advisory ramp.**

AG-12 records that declarative-only enforcement (log-only hooks, optional
strictness) is a recurring Vibebackbone weakness. The proposal therefore ships
its validator (`tools/vbb-adversarial-gate.py`) **in the same governed run** as
the schema, not later — but its blocking scope ramps per `05_MIGRATION_STRATEGY.md`.

**Refused.** Shipping the vocabulary without the validator. A status nobody
checks is process theater, which is the dominant risk identified in §6 of the
audit.

---

## Decision summary

| ID | Decision | Canon impact |
|---|---|---|
| D1 | Fourth gate family `ADVERSARIAL`, additive schema `1.1` | `GATE_ASSURANCE_GOVERNANCE.md` |
| D2 | No phase 08; campaign artifact + third review profile | `AGENTIC_RUN_PROTOCOL.md` |
| D3 | `COUNTER_PROOF` checkpoint + `resolution` link; documented closeout amendment | `GATE_ASSURANCE_GOVERNANCE.md` |
| D4 | Levels `A0`/`A1`/`A2`; default `A1` when undeclared | `PILOTAGE.md` |
| D5 | Exploration ≠ regression; corpus never satisfies exploration | `CONVENTIONS.md` P.R5, `pre-merge-gate.md` |
| D6 | `CERTIFIED` = enumerated conjunction bound to a code state, revocable | `GATE_ASSURANCE_GOVERNANCE.md` |
| D7 | Severity-dependent arbitration authority | new authority document |
| D8 | Findings feed the existing knowledge loop as anti-pattern observations | `ENGINEERING_KNOWLEDGE_GOVERNANCE.md` |
| D9 | No new route family | `PILOTAGE.md` |
| D10 | Validator ships with the schema; blocking scope ramps | `tools/`, migration |

Proceed to `04_DESIGN_DOSSIER`.
