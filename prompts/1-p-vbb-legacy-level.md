---
description: Assess legacy level and acceptability by project phase
---

Assess the legacy level of this implementation: $@

Objective:
Estimate how much the current codebase behaves like legacy and whether that level is acceptable for the current project phase.

Preferred Vibebackbone skills:

- `1-vbb-tech-debt`
- `t-vbb-dependency-mapper`
- `t-vbb-impact-analyzer`

Skill routing rule:

- Use `1-vbb-tech-debt` as the primary skill.
- Use `t-vbb-dependency-mapper` and `t-vbb-impact-analyzer` only to ground the debt analysis.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. Restate the goal briefly.
2. Identify the scope reviewed.
3. Assess legacy signals such as:
   - unclear architecture
   - brittle dependencies
   - hidden coupling
   - undocumented historical layers
   - duplicated logic
   - dead or half-abandoned code paths
   - naming drift
   - workaround accumulation
   - unclear source of truth
4. Evaluate the current legacy level:
   - low
   - moderate
   - high
   - critical
5. State whether this level is acceptable for:
   - current dev phase
   - pre-production
   - production

Constraints:

- In development, prefer low legacy accumulation.
- Do not normalize avoidable legacy.
- Distinguish legacy symptoms from normal iteration.

Output format:

- Goal
- Scope
- Primary skill used
- Supporting skills
- Fallback justification
- Legacy signals
- Legacy level
- Acceptability by phase
- Recommended cleanup priorities
