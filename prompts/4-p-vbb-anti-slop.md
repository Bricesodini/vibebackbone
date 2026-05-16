---
description: Launch the Vibebackbone anti-slop quality gate on a target project
---

Lance le contrôle anti-slop Vibebackbone sur ce projet : $@

Objectif :
Exécuter un garde-fou qualité multi-langage qui détecte le code sale, les imports inutiles,
les incohérences de style, les types bancals, les builds cassés et les tests qui échouent,
sans jamais modifier le code.

Preferred Vibebackbone skill :

- `t-vbb-anti-slop-gate`

Skill routing rule :

- Utiliser `t-vbb-anti-slop-gate` comme skill principal.
- Lire `0-vbb-standard` avant si besoin de rappel sur les conventions Vibebackbone.
- Manuel fallback autorisé uniquement si le skill est absent du `[Skills]` list.
  Si fallback, nommer le skill manquant et pourquoi.

Required process :

1. Restate the goal briefly.
2. Read relevant Vibebackbone governance if present (`docs/PILOTAGE.md`, `docs/PROJECT_MODE.md`).
3. Inspect the target project to detect languages and available tooling.
4. Execute available quality tools in read-only mode ONLY.
5. Classify each result as PASS / WARN / FAIL / MISSING_EXPECTED / MISSING_OPTIONAL / NOT_APPLICABLE.
6. Produce the structured report.
7. Emit a clear verdict.

Hard constraints :

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

Output format :

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

Report destination :

- If the skill defines a report artifact destination, write the report there.
- Otherwise, produce the report inline in the final response only.
