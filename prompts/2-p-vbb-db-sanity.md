---
description: Assess database sanity in a Vibebackbone-compatible way
---

Perform a Vibebackbone-style database sanity assessment for: $@

Objective:
Assess whether the database layer appears structurally sane, coherent, and safe enough for the current phase of the project.

Preferred Vibebackbone skills:

- `2-vbb-db-robustness`
- `2-vbb-data-integrity`
- `t-vbb-dependency-mapper`
- `t-vbb-impact-analyzer`

Skill routing rule:

- Use `2-vbb-db-robustness` first for schema, migrations, constraints, indexes, backup/restore, and persistence resilience.
- Use `2-vbb-data-integrity` for business invariants and persistence assumptions.
- Use `t-vbb-dependency-mapper` if schema meaning depends on module or boundary context.
- Use `t-vbb-impact-analyzer` if the DB change propagation matters.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. Restate the goal briefly.
2. State the available evidence:
   - schema
   - migrations
   - constraints
   - indexes
   - seed logic
   - transaction patterns
   - ORM usage
3. Assess core sanity dimensions:
   - schema coherence
   - naming consistency
   - key and relation clarity
   - nullability discipline
   - uniqueness and integrity constraints
   - migration hygiene
   - obvious data-risk patterns
4. Distinguish:
   - confirmed issues
   - suspected issues
   - missing evidence
5. State whether the database state appears:
   - sane
   - acceptable with caveats
   - fragile
   - unsafe

Constraints:

- Do not claim deep database certainty without inspecting relevant artifacts.
- Be explicit about unknowns.
- Prefer operational sanity over theoretical perfection.

Output format:

- Goal
- Evidence reviewed
- Primary skill used
- Supporting skills
- Fallback justification
- Sanity assessment
- Confirmed issues
- Suspected issues
- Missing evidence
- Recommended fixes
