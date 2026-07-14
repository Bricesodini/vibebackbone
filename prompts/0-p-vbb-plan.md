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

---

## Agent protocol alignment

**Corresponding phase**: 04_PLAN

This prompt produces a plan before execution. It corresponds to phase 04 of the Vibebackbone protocol.

If the task has not yet been framed, run `canonical/01-p-vbb-intake` or `0-p-vbb-triage` first.

**Expected artifact**: `docs/runs/YYYY-MM-DD_HHmm_slug/04_FIX_PLAN.md`

Create this file with the resulting plan. Name the run directory if it does not exist.

**Handoff to 05_EXECUTION**:

At the end of the plan, explicitly state:
- Planned runs (Run 01, Run 02...)
- The first run to execute
- Target files
- Points requiring attention

**Escalation**: if exploration reveals an unexpected risk → escalate to `canonical/02-p-vbb-audit` before execution.

---

## Closeout sequence (mandatory — run after the plan is produced)

After `04_FIX_PLAN.md` is created and the handoff is written:

1. `t-vbb-commit-ready` → verdict + conventional commit message
2. `git add docs/runs/*/04_FIX_PLAN.md` → `git commit -m "<message>"` → `git push`
3. Update `docs/SESSION.md` (clear if session done, note state if re-entry planned)
4. Update `docs/CONTEXT.md` (status, run link, decisions, open points, next action)

> The plan is a persistent artifact — it must be versioned so the executor can read it in a new session. Do not stop after the handoff. The plan loop is not closed until git push is done. The executor will close the execution loop separately.
