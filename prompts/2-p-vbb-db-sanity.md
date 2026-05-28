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

---

## Closeout sequence (mandatory — run after the sanity assessment)

After the database sanity assessment:

1. `t-vbb-commit-ready` → verdict + conventional commit message
2. `git add <any files modified or created during assessment>` → `git commit -m "<message>"` → `git push`
3. Update `docs/SESSION.md` (clear if session done, note state if re-entry planned)
4. Update `docs/CONTEXT.md` (status, run link, decisions, open points, next action)
5. Update `docs/AUDIT_STATUS.md` (new db-sanity assessment)

> Database sanity assessments are audit-critical artifacts — they must be recorded and versioned. Do not stop after the output. The db-sanity loop is not closed until git push is done.