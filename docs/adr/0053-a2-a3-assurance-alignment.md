---
status: accepted
date: 2026-07-31
document_convention: vbb-doc-v1
version: "1.0"
type: adr
visibility: public
tags: [adr, governance, contract, security]
relations:
  - "../ADVERSARIAL_ASSURANCE_GOVERNANCE.md"
  - "../runs/2026-07-31_external-pilot-remediation-assurance/05_EXECUTION.md"
adr_id: "0053"
decision_status: accepted
decision_makers:
  - "Brice — explicit task authorization"
  - "Codex — implementation record"
---

# ADR 0053 — A2/A3 assurance alignment

**Status**: ACCEPTED
**Date**: 2026-07-31
**Decision**: Adopt the versioned v1.2 clarification that defines A2 by
verifiable operational isolation and A3 by strengthened external independence.

## Context

ADR 0051 and its closeout-era runs used a stricter A2 interpretation in which
a distinct human, model, or provider was treated as mandatory. The newer
conceptual distinction is operational: isolation is the A2 minimum; external
independence is the A3 addition. Both interpretations coexist in history and
must not be conflated.

## Decision

New runs may declare v1.2. A2 requires the operational-isolation evidence
listed in `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md`; model/provider are
disclosed metadata. A3 additionally requires independent actor control and
absence of producer control. The validator fails closed when required evidence
is absent. v1.1 runs and their verdicts remain governed by v1.1.

## Consequences

- An isolated A2 can pass without being represented as A3.
- A missing isolation record cannot pass by relying on model/provider labels.
- Historical runs are append-only evidence; re-evaluation requires a new run.
- This decision aligns assurance semantics only; it does not close RR-BK-01..06
  or declare Vibe Backbone Release Candidate ready.
