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
5. If this is post-audit implementation, require a concrete finding / target before execution: id, file, skill, or behavior to fix.
6. For skill changes, read the relevant `skills/*/CONTRACT.yaml` and `skills/INDEX.yaml`; do not assume a root `CONTRACT.yaml` exists.
7. Treat `docs/AUDIT_STATUS.md` as the source of truth for the current audit state.
8. List pre-existing untracked files and leave them untouched unless they are explicitly in scope.
9. Produce a short but explicit plan.
10. Execute in a controlled way.
11. Summarize what changed and what remains open.

STRUCTURED triggers:

- data contracts
- authentication
- production state
- important multi-file behavior
- architecture-adjacent structure
- significant implementation flow

**Constraints:**

- Do not skip the plan.
- Do not claim canonical compliance without governance grounding.
- Keep the result aligned with project documentation.

**LONG-RUN RULE:**

This task follows the LONG-RUN RULE from `docs/PILOTAGE.md`.

**Budget (STRUCTURED):**
- Initial: 180s
- Extension 1: +300s
- Extension 2: +600s
- Hard max: 1200s (20 min)
- PROGRESS threshold: 90s (50% of initial — PROGRESS required if elapsed > 90s)

**OUTPUT CONTRACT (mandatory):**

Every STRUCTURED task MUST produce these blocks:

**1. PROGRESS** (if elapsed > 90s — at least one before FINAL_STATUS):
```
PROGRESS:
  phase: planning|editing|testing|closeout
  done: ""
  next: ""
  files_touched: []
  risks: []
  estimated_remaining: ""
  needs_extension: true|false
```

**2. EXTENSION_REQUEST** (if more time needed — before current budget expires):
```
EXTENSION_REQUEST:
  reason: ""
  additional_time_seconds: 300
  scope_unchanged: true|false
  next_bounded_step: ""
  risk_changed: true|false
```

**3. TIMEOUT_CLOSEOUT** (if hard timeout or controlled stop):
```
TIMEOUT_CLOSEOUT:
  completed: ""
  incomplete: ""
  files_touched: []
  tests_run: []
  tests_missing: []
  risks: []
  resume_from: ""
  recommended_next_prompt: ""
```

**4. FINAL_STATUS** (always required at end of output):
```
FINAL_STATUS:
  elapsed_seconds: 120
  budget_initial: 180
  progress_emitted: true|false
  progress_count: 0
  extension_requested: true|false
  timeout_closeout_emitted: true|false
  verdict: COMPLETE|EXTENDED|PARTIAL_CONTROL|FAILED_SILENT_TIMEOUT|BLOCKED
  files_touched: []
  tests_run: []
  tests_missing: []
  risks: []
  open_points: []
```

**Rules:**
- FINAL_STATUS is ALWAYS required.
- PROGRESS is required if elapsed > 90s.
- EXTENSION_REQUEST is required before any extension.
- TIMEOUT_CLOSEOUT is required on hard timeout or controlled stop.
- No silent timeout is acceptable.

**The controlling agent or human grants extension only if:**
- phase is clear
- files touched are known
- next step is bounded
- `risk_changed: false`
- `scope_unchanged: true` or explicitly approved

**Output format:**

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

**FINAL_STATUS block (mandatory — always last):**
The FINAL_STATUS block must appear both:
1. At the end of the output text (in the delegate summary)
2. Written inside the `07_CLOSEOUT.md` artifact file on disk

The 07_CLOSEOUT.md must end with `## LONG_RUN_SUMMARY` section containing the FINAL_STATUS block.

---

## Agent protocol alignment

**Corresponding phases**: 01_INTAKE + 04_PLAN + 05_EXECUTION

This prompt combines framing, planning, and execution in one session. It is suitable for the STRUCTURÉE route.

**Expected artifacts**:
- `docs/runs/YYYY-MM-DD_HHmm_slug/01_INTAKE.md` — restated objective + STRUCTURÉE classification
- `docs/runs/YYYY-MM-DD_HHmm_slug/04_FIX_PLAN.md` — plan produced before execution
- `docs/runs/YYYY-MM-DD_HHmm_slug/05_PATCH_SUMMARY_RUN_01.md` — change summary

Create these three files in the run directory. For multiple runs, use `05_PATCH_SUMMARY_RUN_02.md`, etc.

**Optional audit**: if an unexpected risk appears during exploration (security, data, compliance) → stop, create a `canonical/02-p-vbb-audit` session, and resume after its verdict.

**Handoff to 06_REVIEW**:

After execution, do not self-review. Create a new session with `canonical/06-p-vbb-review`.
Pass: `05_PATCH_SUMMARY_RUN_N.md` + list of modified files + unresolved points.

**Closeout sequence (run after approval)**:

1. `t-vbb-commit-ready` → verdict + conventional commit message
2. `git add <files>` → `git commit -m "<message>"` → `git push`
3. Update `docs/SESSION.md` (clear it or record the state)
4. Update `docs/CONTEXT.md` (status, run link, open points)

> Do not stop after review. The loop remains open until git push succeeds. For STRUCTURED, formal closeout is required — produce `07_CLOSEOUT.md` before committing.
