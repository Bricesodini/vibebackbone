---
description: Evaluate or prepare a Vibebackbone dev-to-prod mode transition
---

Evaluate or prepare a Vibebackbone mode transition for: $@

Objective:
Make the current project mode explicit and verify whether the repository is ready to transition from development logic to production-oriented work.

Preferred Vibebackbone skills:

- `t-vbb-mode-transition-gate`
- `t-vbb-impact-analyzer`
- `2-vbb-ops`
- `2-vbb-ci`

Skill routing rule:

- Use `t-vbb-mode-transition-gate` as the primary skill.
- Use `t-vbb-impact-analyzer` for propagation, release, or dependency impacts.
- Use `2-vbb-ops` for operational readiness and rollback consequences.
- Use `2-vbb-ci` for pipeline or invariant coverage gaps.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. Restate the current goal briefly.
2. Identify the current mode if documented:
   - development
   - production preparation
   - production
   - unknown
3. State which governance files are available and relevant.
4. Identify what changes operationally when moving to production-oriented work.
5. List the required checks before transition.
6. State whether the repo is:
   - not ready
   - conditionally ready
   - ready for transition

Focus points:

- branch strategy expectations
- data and auth safety
- deployment clarity
- rollback readiness
- auditability
- unresolved high-risk legacy
- open technical debt that blocks safe release

Constraints:

- Do not treat development and production as equivalent.
- Do not declare production readiness without evidence.
- Be explicit about blockers.

Output format:

- Goal
- Current mode
- Governance used
- Primary skill used
- Supporting skills
- Fallback justification
- Transition checks
- Blockers
- Readiness
- Recommended next action

---

## Closeout sequence (mandatory — run after the readiness verdict)

After the mode-transition readiness verdict:

1. `t-vbb-commit-ready` → verdict + conventional commit message
2. `git add <any files modified during transition evaluation>` → `git commit -m "<message>"` → `git push`
3. Update `docs/SESSION.md` (clear if session done, note state if re-entry planned)
4. Update `docs/CONTEXT.md` (status, run link, decisions, open points, next action)
5. Update `docs/AUDIT_STATUS.md` (new mode-transition verdict)

> The mode-transition gate verdict is a production decision artifact — it must be recorded and versioned. Do not stop after the verdict. The mode-transition loop is not closed until git push is done.