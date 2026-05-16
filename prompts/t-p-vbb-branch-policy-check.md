---
description: Check whether branch strategy matches current Vibebackbone phase
---

Assess whether the current branch strategy matches Vibebackbone expectations for: $@

Objective:
Verify whether branch usage is appropriate for the project maturity and transition stage.

Preferred Vibebackbone skills:

- `t-vbb-mode-transition-gate`
- `t-vbb-impact-analyzer`
- `2-vbb-ops`

Skill routing rule:

- Use `t-vbb-mode-transition-gate` as the primary skill.
- Use `t-vbb-impact-analyzer` when branch policy affects release or deployment propagation.
- Use `2-vbb-ops` only for operational or rollback consequences.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. Restate the goal briefly.
2. Identify the current phase:
   - early dev
   - active dev
   - release preparation
   - production
3. State the observed or intended branch policy.
4. Assess whether it matches the current phase.

Preferred Vibebackbone logic:

- In early development, staying on `main` can be acceptable to maximize speed and reduce branch overhead.
- From production preparation onward, development should move to dedicated branches before merge.
- Production-oriented work should favor clearer isolation, reviewability, and rollback discipline.

Constraints:

- Do not assume one branch strategy fits all phases.
- Do not overcomplicate branching too early.
- Do not keep production-oriented work on `main` without strong reason.

Output format:

- Goal
- Current phase
- Current or intended branch policy
- Primary skill used
- Supporting skills
- Fallback justification
- Fit assessment
- Risks
- Recommended policy
