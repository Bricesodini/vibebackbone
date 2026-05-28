---
description: Produce a compact Vibebackbone session handoff
---

Produce a Vibebackbone-compatible session handoff for: $@

Objective:
Create a compact, reusable handoff at the end of a work session.

Preferred Vibebackbone skills:

- `t-vbb-session-handoff`
- `3-vbb-risk-register`

Skill routing rule:

- Use `t-vbb-session-handoff` as the primary skill.
- Use `3-vbb-risk-register` only when visible risks or dependencies need consolidation.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. Restate the work briefly.
2. List decisions that were made.
3. List open points.
4. List visible risks or dependencies.
5. Identify the next recommended action.
6. If present, align with `docs/SESSION.md` and `docs/AUDIT_STATUS.md`.

Constraints:

- Be compact.
- Be factual.
- Do not rewrite history.
- Separate completed work from assumptions and pending items.

---

## Closeout sequence (mandatory — run at the end of every session)

After the handoff artifact is produced:

1. `t-vbb-commit-ready` → verdict + conventional commit message
2. `git add <files>` → `git commit -m "<message>"` → `git push`
3. Update `docs/SESSION.md` (clear if session done, note state if re-entry planned)
4. Update `docs/CONTEXT.md` (status, run link, decisions, open points, next action)

> Do not stop after producing the handoff artifact. The session loop is not closed until git push is done.

Output format:

- Goal
- Work completed
- Decisions made
- Open points
- Risks / dependencies
- Primary skill used
- Supporting skills
- Fallback justification
- Next recommended step
