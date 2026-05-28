---
description: Initialize or assess a repository for Vibebackbone governance
---

Run Vibebackbone project initialization assessment for: $@

Objective:
Determine whether the repository is already on Vibebackbone rails and establish the minimum project context required to work safely.

Preferred Vibebackbone skills:

- `t-vbb-project-context-init`
- `0-vbb-rico-readiness`
- `0-vbb-audit-readiness`
- `t-vbb-mode-transition-gate`

Skill routing rule:

- Use `t-vbb-project-context-init` as the primary skill.
- Use `0-vbb-audit-readiness` and `t-vbb-mode-transition-gate` only as checks around the scaffold state.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. Restate the project goal briefly.
2. Check whether the repository contains:
   - `docs/PILOTAGE.md`
   - `docs/PROJECT_MODE.md`
   - `docs/SESSION.md`
   - `docs/AUDIT_STATUS.md`
3. State governance status:
   - on rails
   - partially initialized
   - not initialized
4. Identify what is missing.
5. Propose the minimum next steps to initialize or normalize the repo.
6. If the user wants to start a new MVP after initialization, route to
   `docs/MVP_START_PROTOCOL.md` and `0-vbb-rico-readiness` before any
   implementation.
7. If governance is missing, do not pretend the repo is fully Vibebackbone-compliant.

Constraints:

- Do not invent missing governance files.
- Be explicit about what exists and what does not.
- Prefer minimal viable initialization over bloated setup.

Output format:

- Project goal
- Governance status
- Files detected
- Missing files
- Primary skill used
- Supporting skills
- Fallback justification
- Recommended initialization steps
- Execution readiness

---

## Closeout sequence (mandatory — run after initialization recommendations)

After the initialization state is assessed and recommendations are produced:

1. `t-vbb-commit-ready` → verdict + conventional commit message
2. `git add <governance files created or modified>` → `git commit -m "<message>"` → `git push`
3. Update `docs/SESSION.md` (clear if session done, note state if re-entry planned)
4. Update `docs/CONTEXT.md` (status, run link, decisions, open points, next action)

> Governance files created during initialization are persistent artifacts — they must be versioned. Do not stop after the recommendations. The project-init loop is not closed until git push is done.