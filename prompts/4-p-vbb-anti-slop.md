---
description: Launch the Vibebackbone anti-slop quality gate on a target project
---

Run the Vibebackbone anti-slop check on this project: $@

Objective:
Run a multi-language quality gate that detects low-quality code, unused imports,
style inconsistencies, weak typing, broken builds, and failing tests without ever
modifying the code.

Preferred Vibebackbone skill:

- `t-vbb-anti-slop-gate`

Skill routing rule:

- Use `t-vbb-anti-slop-gate` as the primary skill.
- Read `0-vbb-standard` first if a reminder of Vibebackbone conventions is needed.
- Manual fallback is allowed only if the skill is absent from the `[Skills]` list.
  If falling back, name the missing skill and explain why.

Required process:

1. Restate the goal briefly.
2. Read relevant Vibebackbone governance if present (`docs/PILOTAGE.md`, `docs/PROJECT_MODE.md`).
3. Inspect the target project to detect languages and available tooling.
4. Execute available quality tools in read-only mode ONLY.
5. Classify each result as PASS / WARN / FAIL / MISSING_EXPECTED / MISSING_OPTIONAL / NOT_APPLICABLE.
6. Produce the structured report.
7. Emit a clear verdict.

Hard constraints:

- NEVER modify code.
- NEVER apply automatic fixes (`--fix`, `--write`, `--unsafe-fixes`, `npm audit fix`).
- NEVER install missing tools.
- NEVER suppress or weaken a test to make the gate pass.
- NEVER transform a quality check into a business refactor.
- NEVER modify old migrations without explicit justification.
- NEVER touch secrets, `.env`, tokens, or credentials.
- NEVER launch destructive commands.
- Prefer existing project scripts (`npm run lint`, `npm run typecheck`, `npm run test`, `npm run build`) over raw tool invocation.
- Do not use `npx` in a way that may install missing packages. Use `./node_modules/.bin/<tool>` instead.
- ALWAYS distinguish verified fact, hypothesis, and unchecked item.
- ALWAYS produce a verdict.

Output format:

- Goal
- Scope (project path, detected languages)
- Governance used (which Vibebackbone files were read)
- Skill used : `t-vbb-anti-slop-gate`
- Tools detected (inventory table)
- Commands executed (one per tool, with exit code and status)
- Results summary (PASS / WARN / FAIL / MISSING_EXPECTED / MISSING_OPTIONAL / NOT_APPLICABLE counts)
- Critical errors (blocking)
- Warnings (non-blocking)
- Missing / Not Applicable tools (by category)
- Auto-fix opportunities (not applied)
- Verdict : READY | READY_WITH_WARNINGS | BLOCKED | UNKNOWN
- Recommendations
- Remaining risks

---

## Closeout sequence (mandatory — run after the verdict)

After the anti-slop gate verdict:

1. `t-vbb-commit-ready` → verdict + conventional commit message
2. `git add <files modified during the gate>` → `git commit -m "<message>"` → `git push`
3. Update `docs/SESSION.md` (clear if session done, note state if re-entry planned)
4. Update `docs/CONTEXT.md` (status, run link, decisions, open points, next action)

> The anti-slop gate is a quality gate — it should not leave files uncommitted. Do not stop after the verdict. The anti-slop gate loop is not closed until git push is done.

Report destination:

- If the skill defines a report artifact destination, write the report there.
- Otherwise, produce the report inline in the final response only.
