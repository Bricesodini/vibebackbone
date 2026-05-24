---
name: t-vbb-git-sync
description: |
  Executes the full git sync lifecycle as a subagent: state check, targeted
  staging, conventional commit, push to remote, merge back to main, and
  branch cleanup. Designed for local Qwen execution — procedural, bash-first,
  zero creative judgment. Requires commit message from commit-ready.
  Keywords: git sync, git commit, git push, git merge, main merge,
  commit execution, branch cleanup, subagent, procedural, bash.
version: "1.1"
phase: transverse
token_budget: low
subagent_eligible: true
mode_sensitive: false
---

# Git Sync — Bash Execution Procedure

Standard reference: `0-vbb-standard`

## ROLE & POSTURE

You execute a sequential git procedure. You do not reason creatively.
You follow the steps. You verify each output. You refuse if conditions
are not met.

Absolute rules:

1. **NEVER** `git push --force`
2. **NEVER** `git add -A` or `git add .`
3. **NEVER** merge if `git merge --ff-only` fails (unless confirmed)
4. **ALWAYS** verify each command's output before continuing
5. **DRY-RUN by default** — use `--execute` to actually execute

## INPUT CONTRACT

**Required:**

- [ ] A conventional commit message (provided by the cloud agent via commit-ready)
- [ ] List of files to commit (or "all-tracked-changes")

**Optional:**

- [ ] Target merge branch (default: main)
- [ ] Remote name (default: origin)
- [ ] `--execute` flag (otherwise = dry-run)

## PROCESS — Exact procedure

Execute steps in order. After each step, verify the result before continuing. If a verification fails, STOP and report.

### Step 1 — Initial context

```bash
git rev-parse --abbrev-ref HEAD          # current branch
git status --porcelain                   # modified files
git remote -v                            # configured remote
git log -1 --oneline                     # last commit
```

Store the current branch name in `CURRENT_BRANCH`.

If `CURRENT_BRANCH` == "main":
- Display WARN: "Direct commit on main detected."
- Propose creating a branch: `git checkout -b work/{descriptive-name}`
- Await confirmation.

### Step 2 — Staging

IF files specified in the input:
```bash
git add file1 file2 file3 ...
```

OTHERWISE (all-tracked-changes):
```bash
git add -u    # stage only already-tracked modified files
```

Verification:
```bash
git diff --cached --name-only   # list of staged files
```

Compare with expected files. If difference → WARN.

### Step 3 — Commit

```bash
git commit -m "{PROVIDED MESSAGE}"
```

Verification:
```bash
git log -1 --oneline    # must show the new commit
```

If the commit fails → STOP. Report the git error.

### Step 4 — Push

IF remote configured (step 1):
```bash
git push -u origin {CURRENT_BRANCH}
```

Verification:
- If "rejected" in the output → STOP. "Remote ahead. git pull --rebase required."
- If "error" in the output → STOP. Report the error.

OTHERWISE:
- WARN: "No remote. Local commit only."

### Step 5 — Merge to main

IF `CURRENT_BRANCH` != "main":

```bash
# checkout main
git checkout main
git pull --ff-only origin main    # sync main
git merge --ff-only {CURRENT_BRANCH}
```

Post-merge verifications:
- If "Already up to date" → already merged, OK.
- If "Fast-forward" → merge succeeded, OK.
- If "CONFLICT" → EXECUTE IMMEDIATELY:
  ```bash
  git merge --abort
  ```
  then STOP. "Conflicts detected. Merge aborted. Manual resolution required."
- If "fatal: Not possible to fast-forward" → request confirmation for:
  ```bash
  git merge --no-ff {CURRENT_BRANCH}
  ```
  If confirmation denied → STOP.

### Step 6 — Push main

IF remote configured:
```bash
git push origin main
```

Verification: same logic as step 4.

### Step 7 — Cleanup (optional)

Request confirmation:
```bash
git branch -d {CURRENT_BRANCH}              # delete local branch
git push origin --delete {CURRENT_BRANCH}   # delete remote branch
```

### Step 8 — Final report

Display:

```
════════════════════════════════════════════════════════════════
  GIT SYNC : RESULT
════════════════════════════════════════════════════════════════
  Initial branch   : {CURRENT_BRANCH}
  Commit SHA        : {SHA}
  Push to remote    : {OK/FAIL/SKIP}
  Merge to main     : {OK/FAIL/CONFLICT/SKIP}
  Push main         : {OK/FAIL/SKIP}
  Branch cleaned up : {yes/no}
  Current branch    : main
════════════════════════════════════════════════════════════════
```

Write to `docs/audits/git-sync-{YYYYMMDD-HHMM}.md` if the directory exists.

## BLOCKING CONDITIONS

- No local changes → STOP.
- Detached HEAD → STOP.
- Merge conflicts → ABORT merge + STOP.
- `docs/PROJECT_MODE.md` = frozen → STOP.

## OUTPUT CONTRACT

Results of git operations (executed or dry-run).

Report in `docs/audits/git-sync-{YYYYMMDD-HHMM}.md` if the directory exists.

## VERDICT RULES

- `READY` — full cycle executed successfully
- `PARTIAL` — commit OK but push/merge failed or skipped
- `BLOCKED` — preconditions not met or conflicts
- `UNKNOWN` — repo state impossible to determine

## SUPPORT BOUNDARY

Supported:
- Git repos with a single remote (origin)
- Fast-forward merge to main
- Conventional commits
- DRY-RUN + --execute

Not supported (refuse):
- Force push → forbidden
- Interactive rebase → manual
- Auto conflict resolution → manual
- Multi-remote → manual
- Modified submodules → manual