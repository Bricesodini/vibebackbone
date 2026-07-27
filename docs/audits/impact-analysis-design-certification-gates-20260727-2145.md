---
kind: audit_report
audit_type: impact-analyzer
status: READY
updated: 2026-07-27
run_id: "2026-07-27_2145_design-certification-gates-core-integration"
---

# Impact analysis — Design/Certification gate integration

## Change analyzed

Introduce the additive `ASSURANCE_STATUS` v1 contract and distinguish
`DESIGN`, `CERTIFICATION` and `OTHER` gate families while preserving local
`PASS/FAIL` verdicts and runtime `FINAL_STATUS`.

## Direct impact

Core governance authorities, run/review/closeout templates, canonical prompts,
architecture relations, loop-closure validation and regression tests.

## Indirect impact

Pi, OpenCode, Codex and Claude consume shared Core files. The change must remain
generic and must not create distribution-specific policy copies.

## External impact

No consumer project is modified. Historical runs remain governed by their
original protocol. Unpublished external readers are not observable.

## Final classification

**CONDITIONAL** before execution; becomes **NON_BREAKING** only if the accepted
ADR, GO POC, cutoff-aware enforcement, historical fixtures and independent
review all pass.

## UNKNOWN

Unpublished external consumers outside the supported repository boundary.
