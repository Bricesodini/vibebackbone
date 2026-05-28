---
description: Execute an important work package sequentially with context compression at 40% threshold
---

Enter **Sequenced Execution Mode** for: $@

## What This Is

A method for executing large-scale work packages by chaining multiple focused runs, each respecting a ~40% context budget ceiling per step. Between runs, produce and consume compact context packets so knowledge is preserved without exceeding token limits.

## Core Principle

> _One run does not need to do everything. Each run does one thing well, hands off a compressed note, and the next run picks up exactly where you left off._

A work package can span dozens of steps. The plan drives execution, NOT reverse. You stop at 40% context or when a natural phase ends — whichever comes first.

---

## How to Use This Prompt

When instructed with this prompt, follow these rules:

### Phase 0 — Planning (before any write)

1. Restate the overarching goal.
2. Decompose into **phases** (A, B, C...) and **steps** within each phase.
3. For each step, estimate: scope, risk, dependencies, expected output artifact.
4. Identify natural _checkpoint boundaries_ where context compression should happen.
5. State the plan in a compact table format:

```
| Step | Phase | What | Risk | Dependencies | Output | Context Target |
|------|-------|------|------|-------------|--------|---------------|
| 0.1  | A     ...  | Low/None    | None   | README.md           | Plan file      | ~25%       |
| 0.2  | A     ...  | Medium  | Phase 0.1 analysis | Audit report | ~40%       |
```

6. Ask for confirmation before executing.

### Phase 1 Execution — Methodical Chain

For each step in the chain:

#### Per-Step Rules

1. **Before starting a step**, state:
   - Step number and goal
   - What you know from previous context packets
   - Any assumptions

2. **Execute the step** with clear, deliberate work.

3. **At ~40% context usage OR when the natural phase ends**, HALT and produce a **context packet**:

#### Context Packet Format (required at every checkpoint)

```markdown
## [Step N.M] Completion Packet
### Completed
- [ ] What was done (bullet list, specific)

### Decisions Made
| Decision | Rationale | Risk |
|----------|-----------|------|
| ...      | ...       | ...  |

### Artifacts Produced
- Path: `...` — purpose: `...`

### Open Questions / Blockers
- [ ] Item needing resolution before next step

### Context for Next Step
- Key facts that must be carried forward:
  - Fact 1
  - Fact 2
- Files/directories to examine first in next run
- State that must be preserved (e.g., "branch is at X", "tests pass")

### Next Step Preview
- What the next step should do
- Any preconditions or prerequisites
```

Save this context packet to `.pi/SEQ_PLAN.md` or a similarly discoverable location.

### Phase N+1 — Resuming from Context Packet

When starting a new run after a checkpoint:

1. Read `SEQ_PLAN.md` (or equivalent) for the latest context packet.
2. Acknowledge what was done and state any concerns about continuity.
3. Execute the next step following the same per-step rules.
4. Produce another context packet at the next checkpoint.

---

## Quality Guards

- **Never skip the planning phase.** A sequenced plan without explicit steps is just a stream of commits.
- **Compress context at ~40%, not higher.** If you're beyond 40% before completing a step, STOP and produce what you have, then continue in a new run.
- **Be specific in context packets.** Vague summaries are useless to the next run. Use file paths, concrete decisions, exact states.
- **Track progress explicitly.** Always state which step number you're on and whether it's complete.
- **Flag risks early.** If something smells wrong during a step, note it in the context packet and optionally stop before completing further steps.

---

## Example Flow (Abbreviated)

```
USER: Execute t-p-vbb-sequenced-ship for rewriting the auth module

YOU:
### Phase 0 — Planning Decomposed into Phases:
| Step | What                          | Risk     | Dependencies    | Output                  | Context Target |
|------|-------------------------------|----------|-----------------|-------------------------|---------------|
| 1.1  | Audit current auth code       | Low      | None            | audit.md                | ~25%          |
| 1.2  | Design new interface          | Medium   | audit.md        | design.md               | ~40%          |
| 2.1  | Implement core module         | High     | design.md       | auth.ts, types.ts       | ~35%          |
| 2.2  | Add tests                     | Medium   | auth.ts         | auth.test.ts            | ~40%          |

Confirm this plan? [yes/no]

USER: yes

YOU (Step 1.1):
Executing step 1.1: Audit current auth code
[Kir does audit work...]
--- CONTEXT PACKET ---
...packet content...

(run ends)

--- NEXT RUN ---

YOU (Step 1.2):
Resuming from step 1.1 context packet. Previous audit shows X patterns, Y risks.
Executing step 1.2: Design new interface
[Does design work...]
--- CONTEXT PACKET ---
...
```

---

## When to Use This Prompt

Use `t-p-vbb-sequenced-ship` when:
- The work package involves **multiple file changes** or cross-module modifications
- Risk level is **Medium or High** (refactoring critical paths, breaking API changes)
- You expect the context to approach **~40% or more** of your model's window
- The task spans **more logical phases** than can be cleanly done in one shot

Use a simpler prompt (quick-task or structured-task) for:
- Single-file changes under Medium risk
- Small, self-contained modifications
- Read-only analysis tasks
- Anything under ~20% context budget

---

## Skills

Primary: `t-vbb-dependency-mapper`, `1-vbb-intent-decomposer`
Supporting: `0-vbb-pilotage`, `t-vbb-impact-analyzer`, `t-vbb-session-handoff`, `3-vbb-risk-register`

---

## Output

When complete (all steps in the chain done), produce a final summary:

```markdown
### Final Summary — [Work Package Name]
**Steps Completed:** N/N
**Overall Status:** Success / Partial / Failed
**Key Decisions:** ...
**Remaining Work:** ...
**Recommendations for Next Phase:** ...
```

---

## Closeout sequence (mandatory — run after the final summary)

After the final summary is produced:

1. `t-vbb-commit-ready` → verdict + conventional commit message
2. `git add <files>` → `git commit -m "<message>"` → `git push`
3. Update `docs/SESSION.md` (clear if session done, note state if re-entry planned)
4. Update `docs/CONTEXT.md` (status, run link, decisions, open points, next action)

> The sequenced run is not finished until git push is done. A "success / partial / failed" summary without commit is an open loop.
