---
description: Compile a Vibebackbone-style risk register
---

Compile a Vibebackbone-style risk register from the current findings: $@

Objective:
Consolidate identified risks into a clear, operational register.

Preferred Vibebackbone skills:

- `3-vbb-risk-register`
- `2-vbb-systemic-risk`
- `2-vbb-data-integrity`

Skill routing rule:

- Use `3-vbb-risk-register` as the primary skill.
- Use `2-vbb-systemic-risk` and `2-vbb-data-integrity` only to normalize or classify the source findings.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. List each risk explicitly.
2. State the affected area.
3. State the likely impact.
4. State the confidence level.
5. State the recommended mitigation.
6. Distinguish confirmed risks from suspected risks.

Constraints:

- This is a consolidation artifact, not a fresh exploratory audit.
- Do not invent risks without basis.
- Be explicit about uncertainty.

Output format:
For each risk:

- Risk
- Area
- Impact
- Confidence
- Mitigation
- Status:
  - confirmed
  - suspected
  - needs validation

At the end:

- Primary skill used
- Supporting skills
- Fallback justification
