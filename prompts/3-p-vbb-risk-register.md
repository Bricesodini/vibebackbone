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

---

## Closeout sequence (mandatory — run after the risk register is produced)

After the risk register is produced:

1. `t-vbb-commit-ready` → verdict + conventional commit message
2. `git add <risk register files>` → `git commit -m "<message>"` → `git push`
3. Update `docs/SESSION.md` (clear if session done, note state if re-entry planned)
4. Update `docs/CONTEXT.md` (status, run link, decisions, open points, next action)
5. Update `docs/AUDIT_STATUS.md` (new consolidated risks)

> The risk register is a decision-critical artifact — it must be versioned. Do not stop after producing the register. The risk-register loop is not closed until git push is done.

At the end:

- Primary skill used
- Supporting skills
- Fallback justification
