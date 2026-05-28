---
description: Run a Vibebackbone audit-oriented analysis
---

Handle this as a Vibebackbone AUDIT task: $@

Objective:
Perform an audit-oriented analysis grounded in repository governance and explicit risk classification.

Preferred Vibebackbone skills:

- `0-vbb-audit-readiness`
- `0-vbb-scope-freeze`
- `t-vbb-dependency-mapper`
- `2-vbb-api-auditor`
- `2-vbb-db-robustness`
- `2-vbb-security`
- `2-vbb-systemic-risk`
- `2-vbb-data-integrity`
- `2-vbb-ops`
- `2-vbb-ci`
- `2-vbb-legal`
- `3-vbb-risk-register`

Skill routing rule:

- Use `0-vbb-audit-readiness` and `0-vbb-scope-freeze` as mandatory gates.
- Use `t-vbb-dependency-mapper` before domain audits when structural context is needed.
- Use the most relevant domain audit skill(s) next: API, DB robustness, security, systemic risk, data integrity, ops, CI, legal.
- Use `3-vbb-risk-register` only after findings exist.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. Restate the goal briefly.
2. Confirm why the task belongs to AUDIT.
3. State which governance files are available and relevant.
4. Identify the audit scope.
5. Follow the canonical audit sequence proportionally:
   - readiness / scope
   - structural context
   - domain audit
   - risk consolidation
6. Produce findings, risks, and recommended actions.

Constraints:

- Do not present an audit as canonical if governance is missing or unread.
- If some stages cannot be completed, say so clearly.
- Distinguish facts, inferences, and uncertainties.

Output format:

- Goal
- Why this is AUDIT
- Governance used
- Scope
- Primary skill path
- Supporting skills
- Fallback justification
- Findings
- Risks
- Recommendations
- Missing evidence / uncertainties

---

## Handoff & Closeout

**After audit findings** :

1. `3-vbb-risk-register` → consolidate findings into a risk register (if findings exist)
2. `t-vbb-commit-ready` → verdict + message conventionnel
3. `git add <fichiers>` → `git commit -m "<message>"` → `git push`
4. Mise à jour de `docs/SESSION.md` (vier ou noter l'état)
5. Mise à jour de `docs/CONTEXT.md` (statut, lien vers run, points ouverts)
6. Si applicable : mise à jour de `docs/AUDIT_STATUS.md` (nouveau rapport d'audit)

> Do not stop after "recommendations". The audit loop is not closed until findings are registered, report is committed, and git push is done.

**If implementation is required** :
- Do NOT implement in the same session
- Document findings + recommended actions in the audit report
- Create a new session for implementation (STRUCTURED or AUDIT route depending on risk class)
