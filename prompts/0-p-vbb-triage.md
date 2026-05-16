---
description: Classify a task into the correct Vibebackbone execution path
---

You are running the Vibebackbone triage protocol for this task: $@

Objective:
Classify the task into exactly one execution path:

- QUICK
- STRUCTURED
- AUDIT
- CLÔTURE

Preferred Vibebackbone skills:

- `0-vbb-pilotage`
- `0-vbb-audit-readiness`
- `0-vbb-scope-freeze`

Skill routing rule:

- Use `0-vbb-pilotage` as the primary routing skill.
- Use `0-vbb-audit-readiness` and `0-vbb-scope-freeze` only as gates when the path is not obvious.
- Do not invent a parallel workflow.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. Restate the user goal briefly.
2. Detect whether the repository appears to be on Vibebackbone rails.
3. State which governance files are available and relevant:
   - `docs/PILOTAGE.md`
   - `docs/PROJECT_MODE.md`
   - `docs/SESSION.md`
   - `docs/AUDIT_STATUS.md`
4. Choose exactly one path.
5. Justify the choice briefly.
6. State only the next recommended action.

Path rules:

- Choose STRUCTURED if the task affects data contracts, auth, production state, important multi-file behavior, or a significant structural change.
- Choose AUDIT if the task affects security, data integrity, compliance, systemic risk, or auditability.
- Choose QUICK only if the task is low-risk, local, reversible, and outside auth/data-contract/security/production concerns.
- Choose CLÔTURE if the task is about session wrap-up, handoff, resumability, or documenting what was done and what remains.

Output format:

- Goal
- Governance files detected
- Primary skill used
- Supporting skills
- Fallback justification
- Chosen path
- Reason
- Next action
