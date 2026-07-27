---
status: accepted
date: 2026-07-27
decision_makers:
  - "Brice"
  - "Codex"
consulted:
  - "independent audit review"
informed:
  - "Pi"
  - "OpenCode"
  - "Codex"
  - "Claude Code"
---

# ADR 0050 — Design and Certification assurance schema

**Status**: ACCEPTED
**Date**: 2026-07-27
**Route**: STRUCTURED
**Décideur**: Brice (explicit approval)
**Liée à POC**:
`docs/runs/2026-07-27_2145_design-certification-gates-core-integration/POC.md`

## Context

The same unqualified `FAIL` currently describes an unfinished behavioral
contract and an uncertified documentary proof. This makes a designed product
appear unspecified and encourages unsafe inference from aggregate status.
ADR 0043 already separates domain verdicts from runtime worker status.

## Decision

Vibebackbone adopts assurance governance version `1.0`.

1. Gate results retain local verdicts `PASS`, `FAIL`, `NOT_ASSESSED` and
   `NOT_APPLICABLE`.
2. Every governed result declares `gate_family` as `DESIGN`,
   `CERTIFICATION` or `OTHER`, plus an immutable `gate_id`, `checkpoint`,
   `subject`, evidence and reasons. A `NOT_APPLICABLE` result additionally
   declares an applicability profile identifier and evidence.
3. `DESIGN` closes observable behavior. `CERTIFICATION` certifies coherence,
   traceability and proof. A documentary contradiction that changes observable
   behavior reopens `DESIGN`.
4. Results are append-only and checkpoint-specific. Pre-implementation and
   post-implementation certification never overwrite one another.
5. `ASSURANCE_STATUS` is a sibling of runtime `FINAL_STATUS`; neither implies
   the other.
6. `implementation_authorization` is explicit and fail-closed. Only
   `status: AUTHORIZED` authorizes work, and only with non-empty reasons and
   required gate identifiers. Missing, malformed or any other status means
   `NOT_AUTHORIZED`.
7. Phase 06 exposes separate `DESIGN_REVIEW` and `CERTIFICATION_REVIEW`
   profiles and distinct verdicts when applicable.
8. Knowledge Harvest remains a mandatory phase-07 closeout control and is not
   a Design or Certification gate.
9. The schema is additive and cutoff-aware. Historical runs are not rewritten;
   readers use assurance v1 when present and otherwise preserve legacy
   semantics.

## Canonical schema

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
        profile_id: "<required for NOT_APPLICABLE>"
        status: "NOT_APPLICABLE"
        evidence: ["<profile declaration path>"]
  implementation_authorization:
    status: "AUTHORIZED|NOT_AUTHORIZED"
    required_gate_ids: ["<gate-id>"]
    reasons: ["<explicit reason>"]
```

## Closeout semantics

- A failed pre-implementation Certification gate preserves Design PASS and
  forces `NOT_AUTHORIZED` plus `HANDOFF`.
- A failed post-implementation Certification gate preserves Design PASS unless
  reclassified and forces `HANDOFF`; the delivery is not certified.
- Missing Knowledge Harvest prevents final closeout independently.
- Final `CLOSEOUT` requires all required closeout gates to pass, an explicit
  authorization record where implementation occurred, and no critical open
  point.

## Compatibility

No existing field is removed or renamed. Runs before the objective cutoff keep
their original meaning. New readers ignore absent assurance; legacy readers
ignore the sibling block. Consumer projects migrate only on a future governed
run of their own.

## Consequences

Reviews and closeouts become multidimensional. Templates and loop closure must
enforce the schema for post-cutover Core runs. The additional explicitness is
accepted in exchange for eliminating ambiguous stability signals.

## Alternatives rejected

- A single unqualified `FAIL`: insufficient semantic precision.
- Replacing `FINAL_STATUS`: violates ADR 0043 and breaks readers.
- A Knowledge Harvest gate family or phase: conflates delivery assurance with
  governed learning.

FINAL_STATUS: ACCEPTED
