---
description: Enter Vibebackbone planning mode before execution
---

Enter Vibebackbone planning mode for: $@

Objective:
Produce an explicit plan before any important modification.

Preferred Vibebackbone skills:

- `0-vbb-pilotage`
- `0-vbb-scope-freeze`
- `0-vbb-audit-readiness`
- `t-vbb-impact-analyzer`

Skill routing rule:

- Use `0-vbb-pilotage` as the primary routing skill.
- Use `0-vbb-scope-freeze` and `0-vbb-audit-readiness` to ground the path decision.
- Use `t-vbb-impact-analyzer` only when the planned work could propagate beyond the local file or action.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. Restate the goal briefly.
2. State the assumed execution path:
   - QUICK
   - STRUCTURED
   - AUDIT
3. State which governance files are available and relevant.
4. State key assumptions.
5. Produce a short plan.
6. Stay in read-only exploration until the plan is explicit.
7. If the task is sensitive, structured, or high-impact, do not execute yet. Wait for confirmation.
8. If governance is missing, say so explicitly and produce only a best-effort plan.

Constraints:

- Do not execute while the plan is still implicit.
- Do not claim Vibebackbone compliance unless governance has been detected and read.
- If risk increases during exploration, stop and escalate.

Output format:

- Goal
- Path
- Governance status
- Primary skill used
- Supporting skills
- Fallback justification
- Assumptions
- Plan
- Execution readiness:
  - ready to execute
  - waiting for confirmation
  - blocked by missing governance
