---
description: Execute a low-risk task in Vibebackbone quick mode
---

Handle this as a Vibebackbone QUICK task unless risk analysis proves otherwise: $@

Objective:
Execute a low-risk task quickly, proportionally, and cleanly.

Preferred Vibebackbone skills:

- `0-vbb-audit-readiness`
- `1-vbb-conventions`
- `1-vbb-formatter`
- `1-vbb-doc-harmonizer`

Skill routing rule:

- Use the first applicable skill in the list as the primary skill path.
- Use `0-vbb-audit-readiness` only as a gate if the task might drift out of QUICK.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. Restate the goal briefly.
2. Verify that the task still qualifies as QUICK.
3. State any relevant governance file if present.
4. Give a very short plan.
5. Execute.
6. If risk increases, stop and escalate immediately.

QUICK criteria:

- low-risk
- local
- reversible
- non-sensitive
- outside auth/data-contract/security/production concerns

Output format:

- Goal
- Why this is QUICK
- Governance used
- Primary skill used
- Supporting skills
- Fallback justification
- Plan
- Action
- Result
- Escalation needed: yes/no
