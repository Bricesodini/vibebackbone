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
| `OTHER` | Represent a named gate outside both families without corrupting their semantics. | The named gate failed under its own contract. |

Local verdicts are `PASS`, `FAIL`, `NOT_ASSESSED` and `NOT_APPLICABLE`.
`PASS/FAIL` are never interpreted without `gate_family`, `gate_id`,
`checkpoint` and `subject`.

If a documentary finding changes or contradicts observable behavior, it is
reclassified as `DESIGN` and reopens the relevant Design gate. Evidence,
traceability or coherence findings remain `CERTIFICATION` only while behavior
stays unambiguous.

## Checkpoints and aggregation

Gate results are identified and append-only. The checkpoints are
`PRE_IMPLEMENTATION`, `POST_IMPLEMENTATION` and `CLOSEOUT`; a later result
cannot overwrite an earlier checkpoint.

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
