---
context_role: assurance-governance
phase: transverse
status: active
version: "1.0"
updated: 2026-07-27
adr: "docs/adr/0050-design-certification-assurance-schema.md"
---

# Gate Assurance Governance

This document is the canonical authority for gate-family semantics and the
`ASSURANCE_STATUS` v1 contract. Runtime worker status remains governed by
`docs/PILOTAGE.md` and ADR 0043.

## Gate families

| Family | Purpose | Meaning of `FAIL` |
|---|---|---|
| `DESIGN` | Close observable behavior: contracts, ADRs, transactions, SQL, concurrency and history. | The product is not fully specified. |
| `CERTIFICATION` | Certify coherence, traceability, references, oracles and proof. | The design may be closed, but the documentary proof is not certified. |
| `ADVERSARIAL` | Document an attempted falsification: declared surface, declared depth, declared actor, named findings. | A confirmed finding at or above the blocking severity is unremediated within the declared scope. |
| `OTHER` | Represent a named gate outside the three named families without corrupting their semantics. | The named gate failed under its own contract. |

> **Schema 1.1 (effective 2026-07-28)** — extensions to ADR 0050:
> - The `ADVERSARIAL` family is added (`ADR 0051`).
> - The fourth checkpoint `COUNTER_PROOF` is added to the canonical checkpoint list.
> - `gate_results[].checkpoint` accepts `{PRE_IMPLEMENTATION, POST_IMPLEMENTATION, COUNTER_PROOF, CLOSEOUT}`.
> - `gate_results[].gate_family` accepts `{DESIGN, CERTIFICATION, ADVERSARIAL, OTHER}`.
> - A v1.0 reader that sees `gate_family: ADVERSARIAL` is non-conformant by **explicit declaration**, not by silent re-injection into `OTHER`. The POC `tools/vbb-adversarial-gate.py` enforces this.

Local verdicts are `PASS`, `FAIL`, `NOT_ASSESSED` and `NOT_APPLICABLE`.
`PASS/FAIL` are never interpreted without `gate_family`, `gate_id`,
`checkpoint` and `subject`.

If a documentary finding changes or contradicts observable behavior, it is
reclassified as `DESIGN` and reopens the relevant Design gate. Evidence,
traceability or coherence findings remain `CERTIFICATION` only while behavior
stays unambiguous.

## Checkpoints and aggregation

Gate results are identified and append-only. The checkpoints are
`PRE_IMPLEMENTATION`, `POST_IMPLEMENTATION`, `COUNTER_PROOF` (since v1.1,
ADR 0051) and `CLOSEOUT`; a later result cannot overwrite an earlier
checkpoint.

Two distinct evaluations are defined and **must not be collapsed** into a
single number:

| Evaluation | Scope | Effect of `resolution` |
|---|---|---|
| `checkpoint_aggregation` | Per checkpoint | **None.** A `POST_IMPLEMENTATION` `FAIL` stays `FAIL` forever. That is the historical truth. |
| `closure_evaluation` | Per run, at closeout | A `POST_IMPLEMENTATION` required `FAIL` stops blocking closure **iff** it carries a valid `resolution` whose closing gate result is `PASS` at `COUNTER_PROOF`. |

A run may therefore `final-close` while permanently displaying a failed
`POST_IMPLEMENTATION` checkpoint. The record reads "this broke once,
here is the proof it was closed", not "this never broke".

Within one checkpoint and its declared required-gate list, any required
`FAIL` makes the checkpoint fail, a missing required result makes it
`NOT_ASSESSED`, and all required `PASS` makes it pass. `NOT_APPLICABLE`
requires an explicit profile declaration. There is no universal aggregate
Certification verdict across checkpoints.

## Assurance contract v1

`ASSURANCE_STATUS` is a sibling of `FINAL_STATUS`, never a nested runtime
field:

```yaml
ASSURANCE_STATUS:
  schema_version: "1.0"
  subject: "<delivery or decision under assurance>"
  gate_results:
    - gate_id: "<stable-id>"
      gate_family: "DESIGN|CERTIFICATION|OTHER"
      checkpoint: "PRE_IMPLEMENTATION|POST_IMPLEMENTATION|CLOSEOUT"
      subject: "<bounded gate subject>"
      verdict: "PASS|FAIL|NOT_ASSESSED|NOT_APPLICABLE"
      evidence: ["<path or command>"]
      reasons: ["<factual reason>"]
      applicability:
        profile_id: "<required only for NOT_APPLICABLE>"
        status: "NOT_APPLICABLE"
        evidence: ["<profile declaration path>"]
  implementation_authorization:
    status: "AUTHORIZED|NOT_AUTHORIZED"
    required_gate_ids: ["<gate-id>"]
    reasons: ["<explicit reason>"]
```

`FINAL_STATUS` reports worker execution. `ASSURANCE_STATUS` reports assurance
of the subject. No mapping or inference is permitted in either direction.

## Explicit fail-closed authorization

Implementation is authorized only when all of these conditions hold:

1. `implementation_authorization.status` is exactly `AUTHORIZED`;
2. `required_gate_ids` is non-empty and each identifier resolves to a
   `PRE_IMPLEMENTATION` result with verdict `PASS`;
3. `reasons` is non-empty;
4. no required gate is missing, failed or not assessed.

Missing `ASSURANCE_STATUS`, a missing authorization record, malformed data, or
any status other than `AUTHORIZED` means `NOT_AUTHORIZED`. Design and
Certification PASS never authorize implementation implicitly.

A run containing `05_EXECUTION.md` cannot final-close with
`implementation_authorization.status: NOT_AUTHORIZED`; that contradiction is a
blocking `HANDOFF`. Any Design `FAIL` or `NOT_ASSESSED` likewise prevents final
closeout until Design is remediated or explicitly made non-applicable by its
profile.

`NOT_APPLICABLE` is valid only with a sibling `applicability` mapping whose
`status` is `NOT_APPLICABLE`, whose `profile_id` is non-empty and whose
evidence identifies the declaration that makes the gate non-applicable.
`NOT_ASSESSED` is never a successful final state for an applicable Design or
Certification gate.

## Independent review profiles

Phase 06 remains one phase with two separate profiles:

- `DESIGN_REVIEW`: observable behavior, invariants and completeness;
- `CERTIFICATION_REVIEW`: coherence, evidence, traceability and oracles.

When both apply, the reviewer records two independent verdicts. A Certification
finding that affects behavior explicitly reopens `DESIGN_REVIEW`.

## Closeout policy

| Condition | Required disposition |
|---|---|
| Pre-implementation Certification `FAIL` | Preserve Design result; `NOT_AUTHORIZED`; `HANDOFF`. |
| Post-implementation Certification `FAIL` | Preserve Design unless reclassified; delivery uncertified; `HANDOFF`. |
| Knowledge Harvest absent | Closeout contract incomplete; `HANDOFF`. |
| All required final gates `PASS` | `CLOSEOUT` is possible if no critical point remains. |

Knowledge Harvest remains the mandatory phase-07 learning control defined by
`ENGINEERING_KNOWLEDGE_GOVERNANCE.md`. It is not a Design gate, Certification
gate or additional phase.

## Compatibility and cutoff

Version 1 is additive. No existing field is removed or renamed, and historical
runs are not rewritten or reclassified. The objective cutoff is run key
`2026-07-27_2145` / timestamp `2026-07-27T19:45:52Z`.

- At or after the cutoff, formal runs with intake/closeout declare
  `assurance_governance_version: "1.0"` and closeouts contain a valid sibling
  `ASSURANCE_STATUS`.
- Earlier runs remain valid under their original protocol.
- Readers prefer v1 when present and preserve legacy semantics when absent.
- Consumer projects adopt this contract only through their own future governed
  change; Vibebackbone does not rewrite them.

### v1.1 additive delta (ADR 0051, effective 2026-07-28)

The schema is extended additively by ADR 0051 (adversarial assurance
dimension). `schema_version: "1.1"` is a strict superset of v1.0 — no
field removed or renamed. Schema 1.1 adds:

1. **Top-level statuses** (declared by ADR 0051 and operated in
   `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md`):
   - `implementation_status` ∈ {`NOT_STARTED`, `IN_PROGRESS`,
     `IMPLEMENTED`, `ABANDONED`}.
   - `conformity_status` ∈ {`NOT_ASSESSED`, `PASS_CONFORMITY`,
     `FAIL_CONFORMITY`, `NOT_APPLICABLE`}.
   - `adversarial_status` ∈ {`NOT_ASSESSED`, `NOT_REQUIRED`,
     `IN_CAMPAIGN`, `FINDINGS_OPEN`, `PASS_ADVERSARIAL`,
     `FAIL_ADVERSARIAL`}.
   - `certification_status` ∈ {`NOT_CERTIFIED`, `CERTIFIED`,
     `SUSPENDED`, `NOT_APPLICABLE`, `UNASSESSED_LEGACY`}.
2. **`status_evidence`** — one path or command per top-level status. A
   status without evidence is **invalid**, not merely undocumented.
3. **New `gate_family`** value: `ADVERSARIAL`. Documented in
   `ADVERSARIAL_ASSURANCE_GOVERNANCE.md`.
4. **New `checkpoint`** value: `COUNTER_PROOF`. A counter-proof verdict
   `PASS` may close a previously-failing `POST_IMPLEMENTATION` result
   via the `resolution` link on the failing entry.
5. **`resolution`** — optional block on a failing gate result that
   links to the closing gate at `COUNTER_PROOF` and to finding
   identifiers.
6. **Adversarial block** — `adversarial: { level, campaign_ref,
   corpus_version, exploration_performed, surfaces_declared,
   surfaces_unexplored, residual_uncertainty, findings, verdict }`.
7. **Certification block** — `certification: { status, scope, bound_to,
   conditions_met, owner, human_decision }`. The bound state makes the
   claim revocable (cf. §6.3 in the dossier and §6 in
   `ADVERSARIAL_ASSURANCE_GOVERNANCE.md`).
8. **`UNASSESSED_LEGACY`** — distinct value of
   `certification_status` for pre-cutoff subjects that were never
   adversarially assessed. **Not** `NOT_CERTIFIED`, **not** a failure.

9. **`PRE_CERTIFICATION`** (RATIFIED 2026-07-28, REM-01) — 6ᵉ value
   of `certification_status` for post-cutoff subjects awaiting first
   CERTIFIED. Mandatory companion fields: `transient_reason`,
   `bootstrapped_at`, `bootstrapped_by`. Distinct from
   `UNASSESSED_LEGACY` (which is strictly pre-cutoff) and from
   `NOT_CERTIFIED` (which means "evaluated and not passing"). Full
   semantics in `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §11.1.

10. **`MIGRATION`** (RATIFIED 2026-07-28, REM-01) — 7ᵉ value of
    `certification_status` for subjects in active transition between
    governance regimes (e.g., v1.0 → v1.1). Mandatory companion
    fields: `migrating_from`, `migrating_to`, `migration_started_at`,
    `migration_plan_ref`, `migration_completion_deadline`. Full
    semantics in `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §11.2.

11. **`certification.transient_reason`** (NEW v1.1) — non-empty
    string required when `certification_status ∈ {PRE_CERTIFICATION,
    MIGRATION}`. Describes why the subject is in a transient state.
    A status without `transient_reason` is **invalid**, not merely
    undocumented.

12. **`certification.bootstrapped_at`** (NEW v1.1) — ISO 8601 UTC
    timestamp required for `PRE_CERTIFICATION`. Records the moment
    the subject entered the bootstrap phase.

13. **`certification.bootstrapped_by`** (NEW v1.1) — non-empty
    identifier (agent or human) required for `PRE_CERTIFICATION`.

A v1.0 reader ignores the new top-level blocks and statuses. Where it
encounters a v1.1 enum value (`gate_family: ADVERSARIAL` or
`checkpoint: COUNTER_PROOF`), the reader is **non-conformant** by
explicit declaration. The current v1.1 reader checks for this and
applies the appropriate fail-closed default.

For `certification_status: PRE_CERTIFICATION` or `MIGRATION`, the
v1.0 reader MUST treat the value as `NOT_CERTIFIED` for aggregation
purposes (conservative interpretation) but MUST preserve the original
value in the durable record (no silent rewriting).

Cutoff key for adversarial governance:
`adversarial_governance_version: "1.1"` /
`cutoff_run_key: "2026-07-28_1400"` /
`cutoff_timestamp: "2026-07-28T14:00:00Z"`.
