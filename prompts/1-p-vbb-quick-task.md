---
description: Execute a low-risk task in Vibebackbone quick mode
---

Handle this as a Vibebackbone QUICK task unless risk analysis proves otherwise: $@

Objective:
Execute a low-risk task quickly, proportionally, and cleanly.

Preferred Vibebackbone skills:

- `0-vbb-audit-readiness`
- `1-vbb-conventions`
- `1-vbb-formatter`
- `1-vbb-doc-harmonizer`

Skill routing rule:

- Use the first applicable skill in the list as the primary skill path.
- Use `0-vbb-audit-readiness` only as a gate if the task might drift out of QUICK.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. Restate the goal briefly.
2. Verify that the task still qualifies as QUICK.
3. State any relevant governance file if present.
4. Give a very short plan.
5. Execute.
6. If risk increases, stop and escalate immediately.

QUICK criteria:

- low-risk
- local
- reversible
- non-sensitive
- outside auth/data-contract/security/production concerns

Output format:

- Goal
- Why this is QUICK
- Governance used
- Primary skill used
- Supporting skills
- Fallback justification
- Plan
- Action
- Result
- Escalation needed: yes/no

---

## Agent protocol alignment

**Corresponding phases**: 01_INTAKE (implicit) + 05_EXECUTION

This prompt combines framing and execution in one session. It is suitable only for the RAPIDE STANDARD route.

For RAPIDE-ZERO and RAPIDE-MINIMAL, use `0-p-vbb-zero-friction` instead.

**Expected artifacts** (RAPIDE STANDARD):
- `docs/runs/YYYY-MM-DD_HHmm_slug/01_INTAKE.md` — objective + RAPIDE classification (may be minimal)
- `docs/runs/YYYY-MM-DD_HHmm_slug/05_PATCH_SUMMARY_RUN_01.md` — change summary

These files may be short. They must exist and be named.

**Handoff to 07_CLOSEOUT**:

On the RAPIDE route, review is optional. After execution:
- For a minimal change → proceed directly to `canonical/07-p-vbb-closeout` or `t-p-vbb-session-handoff`
- For a sensitive change → create a `canonical/06-p-vbb-review` session

**Closeout sequence (always — including RAPIDE)**:

1. `t-vbb-commit-ready` → verdict + conventional message
2. `git add <files>` → `git commit -m "<message>"` → `git push`
3. Update `docs/SESSION.md` (clear it if the session is complete)
4. Update `docs/CONTEXT.md` (status, run link)

> Do not stop after execution. The loop remains open until git push succeeds. For RAPIDE-MINIMAL, `05_PATCH_SUMMARY.md` already exists — use it as the basis for the commit sequence.

**Mandatory escalation**: if risk increases during execution (auth, data, production, security) → stop immediately, document it in the patch summary, and create a new STRUCTURÉE or AUDIT session.
