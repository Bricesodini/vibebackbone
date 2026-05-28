---
description: Classify a task into the correct Vibebackbone execution path
---

You are running the Vibebackbone triage protocol for this task: $@

Objective:
Classify the task into exactly one execution path:

- FAST-ZERO (micro-task, ≤ 3 files)
- FAST-MINIMAL (small non-trivial task)
- FAST-STANDARD (simple, low risk)
- STRUCTURED (architecture, contracts, multi-file)
- AUDIT (security, integrity, compliance, systemic risk)
- CLOSEOUT (session wrap-up, handoff)
- ENGINE_ONLY (UI/UX, visual architecture, graphic centralization, design system)

**UI/UX shortcut**: If the request mentions UI/UX, visual architecture, graphic centralization, design system, surface mapping, or "modifications graphiques" → classify as ENGINE_ONLY and route to `vibebackbone` skill first. Do not use the standard path matrix for these requests.

Preferred Vibebackbone skills:

- `vibebackbone` — orchestration and routing decision (use first for all requests)
- `0-vbb-pilotage` — detailed triage when path is not obvious
- `0-vbb-audit-readiness` — audit gate when needed
- `0-vbb-scope-freeze` — scope freeze when needed

Skill routing rule:

- Invoke `vibebackbone` first for routing decision.
- For UI/UX requests: `vibebackbone` will emit ENGINE_ONLY route → `4-vbb-user-experience-engine` (pass 1) + full 7-pass sequence.
- Use `0-vbb-pilotage` only as secondary triage reference.
- Do not invent a parallel workflow.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. Restate the user goal briefly.
2. Detect whether the repository appears to be on Vibebackbone rails.
3. **Check for UI/UX ENGINE_ONLY triggers first**:
   - UI/UX, visual architecture, graphic centralization, design system
   - "modifications graphiques" alone or combined with "optimiser" + "logiques"
   - If any trigger detected → classify ENGINE_ONLY, invoke `vibebackbone`, stop here
4. State which governance files are available and relevant:
   - `docs/PILOTAGE.md`
   - `docs/PROJECT_MODE.md`
   - `docs/SESSION.md`
   - `docs/AUDIT_STATUS.md`
5. Choose exactly one path from standard routes.
6. Justify the choice briefly.
7. State only the next recommended action.

Path rules:

- Choose STRUCTURED if the task affects data contracts, auth, production state, important multi-file behavior, or a significant structural change.
- Choose AUDIT if the task affects security, data integrity, compliance, systemic risk, or auditability.
- Choose FAST (ZERO/MINIMAL/STANDARD) only if the task is low-risk, local, reversible, and outside auth/data-contract/security/production concerns.
- Choose CLOSEOUT if the task is about session wrap-up, handoff, resumability, or documenting what was done and what remains.
- **Choose ENGINE_ONLY first** for any UI/UX, design system, or visual architecture request.

Output format:

- Goal
- UI/UX trigger detected (yes/no)
- Governance files detected
- Primary skill used
- Supporting skills
- Fallback justification
- Chosen path
- Reason
- Next action
  - For ENGINE_ONLY: list `4-vbb-user-experience-engine` as primary + `4-vbb-front-pipeline-reference` as companion
  - For standard path: list next skill by name
