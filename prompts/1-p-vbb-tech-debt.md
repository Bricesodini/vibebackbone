---
description: Evaluate technical debt with Vibebackbone discipline
---

Evaluate technical debt for: $@

Objective:
Identify and classify technical debt with a practical focus on maintainability, risk, and future cost. Surface noise is cleaned first; structural debt is diagnosed second.

Preferred Vibebackbone skills:

- `1-vbb-code-janitor`
- `1-vbb-tech-debt`
- `t-vbb-dependency-mapper`
- `t-vbb-test-coverage-mapper`

Skill routing and chaining rule:

- Phase 1 — Surface cleanup: run `1-vbb-code-janitor` first. This reduces noise so that the structural audit sees real problems instead of surface-level clutter.
- Phase 2 — Structural audit: run `1-vbb-tech-debt` using the janitor report as input. The tech-debt skill focuses on what the janitor cannot address: architectural fragility, systemic duplication, responsibility distribution, and structural debt.
- Use `t-vbb-dependency-mapper` and `t-vbb-test-coverage-mapper` as supporting skills when structural context or test coverage gaps are relevant.
- If the janitor verdict is `READY_WITH_STRUCTURAL_SIGNALS`, the structural signals must be carried forward as input to the tech-debt pass.
- If the janitor verdict is `READY` with no structural signals, the tech-debt pass may still proceed but focuses on deeper systemic patterns not visible at the surface level.
- If the janitor verdict is `BLOCKED`, the repo has too much surface entropy for a reliable structural audit. Surface cleanup must be addressed first before proceeding.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. Restate the goal briefly.
2. Run janitor pass (Phase 1). Wait for the janitor report before proceeding.
3. Carry forward any structural signals from the janitor report.
4. Identify the scope reviewed.
5. Run tech-debt audit (Phase 2), using janitor findings and structural signals as input.
6. Classify technical debt by category:
   - structural
   - code quality
   - documentation
   - tests
   - deployment / ops
   - data layer
   - UX / product implementation mismatch
7. For each debt item, state:
   - what it is
   - why it matters
   - current impact
   - likely future cost
   - urgency
8. Distinguish between:
   - tolerable debt
   - active debt
   - blocking debt

Constraints:

- Do not confuse preference differences with real technical debt.
- Be concrete.
- Prioritize operational relevance over style purity.
- Never conclude on overall system quality from the janitor report alone. A "clean" surface does not guarantee structural health.
- The janitor and tech-debt passes are sequential, not parallel. The tech-debt skill must have the janitor report available before it starts.

Output format:

- Goal
- Scope
- Janitor verdict and structural signals (from Phase 1)
- Primary skill used
- Supporting skills
- Fallback justification
- Debt items
- Classification
- Priority
- Recommended treatment
