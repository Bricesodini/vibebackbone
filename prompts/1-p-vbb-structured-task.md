---
description: Execute a structured Vibebackbone task with explicit grounding
---

Handle this as a Vibebackbone STRUCTURED task: $@

Objective:
Execute a structured task with explicit grounding, plan, and controlled changes.

Preferred Vibebackbone skills:

- `t-vbb-dependency-mapper`
- `t-vbb-impact-analyzer`
- `t-vbb-test-coverage-mapper`
- `1-vbb-conventions`

Skill routing rule:

- Use the first applicable skill in the list as the primary skill path.
- Use `t-vbb-dependency-mapper`, `t-vbb-impact-analyzer`, `t-vbb-test-coverage-mapper`, and `1-vbb-conventions` only in that order of support.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. Restate the goal briefly.
2. Confirm why the task is STRUCTURED.
3. State which governance files are available and relevant.
4. Identify the artifact or change type.
5. Produce a short but explicit plan.
6. Execute in a controlled way.
7. Summarize what changed and what remains open.

STRUCTURED triggers:

- data contracts
- authentication
- production state
- important multi-file behavior
- architecture-adjacent structure
- significant implementation flow

Constraints:

- Do not skip the plan.
- Do not claim canonical compliance without governance grounding.
- Keep the result aligned with project documentation.

Output format:

- Goal
- Why this is STRUCTURED
- Governance used
- Artifact type
- Primary skill used
- Supporting skills
- Fallback justification
- Plan
- Action
- Result
- Open points
