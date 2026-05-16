---
description: Execute a git sync lifecycle — delegate execution to local subagent for token economy
---

Execute the Vibebackbone git sync lifecycle for: $@

Objective:
Prepare the commit package on cloud (reasoning), then delegate git execution
to a local Qwen subagent (token economy). Cloud handles judgment, local handles bash.

Token economics:

- commit-ready runs on CLOUD (needs session context + reasoning for message quality)
- git-sync runs on LOCAL QWEN as subagent (procedural bash execution, zero creative judgment)
- Expected savings: ~10K cloud tokens per sync cycle

Stage 1 — COMMIT PREPARATION (cloud):
Run `t-vbb-commit-ready` to obtain:

- Change set summary
- Coherence check result
- Conventional commit message
- List of files to stage

If commit-ready returns BLOCKED → stop.
If commit-ready returns PARTIAL → confirm with user before delegating.

Stage 2 — EXECUTION (delegate to local Qwen subagent):
Delegate `t-vbb-git-sync` to a subagent with the following brief:

```
Execute t-vbb-git-sync with these inputs:
- COMMIT_MESSAGE: "<message from commit-ready>"
- FILES_TO_STAGE: "<file list from commit-ready, or 'all-tracked-changes'>"
- MERGE_TARGET: "main"
- REMOTE: "origin"
- MODE: "dry-run first, then --execute after user confirmation"
```

The subagent will:

1. Run git status checks (read-only)
2. Dry-run the full git cycle (no writes)
3. Show planned operations
4. On your confirmation, execute with --execute
5. Report commit SHA, push status, merge result

Safety rules (enforced by the skill):

- NEVER force push
- NEVER git add -A
- NEVER merge on conflict (abort instead)
- NEVER commit on main without warning
- DRY-RUN first, --execute only after confirmation

If the subagent reports CONFLICT → stop. Manual resolution required.
If the subagent reports PARTIAL → review and decide.
If the subagent reports READY → verify and close.

Output format:

- Goal
- Stage 1 — Commit Ready (cloud, reasoning)
  - Verdict
  - Commit message
  - Files to stage
  - Warnings
- Stage 2 — Git Sync (local subagent, procedural)
  - Subagent result: READY / PARTIAL / BLOCKED
  - Commit SHA
  - Push result
  - Merge result
  - Branch cleanup
- Final state
- Cloud tokens saved (estimated ~10K vs all-cloud)
