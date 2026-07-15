# POC — decomposed conformance decision

**Status**: CONCLUDED
**Date**: 2026-07-15
**Linked ADR**: `docs/adr/0048-runtime-conformance-decision-model-v2.md`

## Hypothesis

A decision object can represent the existing PILOTAGE semantics without route
aliases: route family, MVP pre-gate, and closeout mode are orthogonal.

## Evidence

- The Pi baseline matched 31/33 required signals despite only 4/10 flat-route passes.
- `MVP START` is documented as a pre-route gate.
- Handoff and final are two dispositions of the closeout family.
- All ten scenarios map unambiguously to the three proposed fields.

## Success criterion

GO if every existing scenario has exactly one decision tuple and the evaluator
can keep mutation and contradictory signals as hard failures.

Verdict: GO
