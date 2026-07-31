---
template_id: "POC"
version: "1.0"
lane_eligible: ["STRUCTURED", "AUDIT"]
related: ["docs/runs/2026-07-31_external-pilot-remediation-assurance/01_INTAKE.md"]
---

# POC — external pilot remediation and assurance alignment

## Hypotheses

1. A bounded v1 contract can support progressive scopes, explicit waivers,
   namespaced status extensions, and actionable out-of-scope suggestions
   without breaking existing v1 declarations.
2. A2 can be validated by operational isolation evidence; A3 can require
   stronger external independence. Historical v1.1 runs remain valid under
   their original contract.

## Test

- Reproduce all twelve pilot findings from preserved evidence.
- Run minimal and extended document scopes, including a real waiver case.
- Run A1/A2/A3 gate fixtures, including fail-closed missing-isolation and
  A2-not-A3 cases.
- Verify a historical v1.1 fixture remains accepted without retroactive
  reinterpretation.

## Decision

Verdict: GO

The implementation is bounded to confirmed RC blockers and a versioned
assurance clarification. No RC readiness is asserted by this POC.
