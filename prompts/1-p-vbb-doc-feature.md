---
description: Produce grounded Vibebackbone-compatible feature documentation
---

Produce documentation for this work in a Vibebackbone-compatible way: $@

Objective:
Generate documentation grounded in actual repository governance and the correct artifact type, not a generic technical document by default.

Preferred Vibebackbone skills:

- `1-vbb-code-doc-gap-integrator`
- `1-vbb-doc-harmonizer`
- `t-vbb-dependency-mapper`
- `t-vbb-impact-analyzer`

Skill routing rule:

- Use `1-vbb-code-doc-gap-integrator` as the primary skill when the goal includes detecting missing documentation and writing it.
- Use `1-vbb-doc-harmonizer` as the primary skill when the goal is strictly to harmonize existing documentation (no code scanning needed).
- Use `t-vbb-dependency-mapper` and `t-vbb-impact-analyzer` only to ground the documentation in repo structure and impact.
- Chain: after `1-vbb-code-doc-gap-integrator` writes missing docs, `1-vbb-doc-harmonizer` may run to harmonize the now-more-complete set.
- Do not mix this prompt with session handoff; if a handoff is needed, use `t-vbb-session-handoff` separately.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

User interaction (gap-integrator only):

When using `1-vbb-code-doc-gap-integrator`, ask the user up to 3 optional questions before scanning. Do not block on unanswered questions — use defaults silently.

1. **Scope** — "Quel périmètre souhaitez-vous couvrir ?" (module, répertoire, feature, ou tout le repo) → default: tout le repo
2. **Known gaps** — "Y a-t-il des modules ou features que vous savez non documentés ?" → default: aucun hint, scan complet
3. **Write threshold** — "Quel seuil d'écriture ?" (HIGH seul ou HIGH+MEDIUM) → default: HIGH+MEDIUM

Execution mode:

- If a local model subagent is available, use DELEGATED mode: the cloud agent executes scanning (steps 1-3) and prepares micro-contexts, then delegates fiche writing (step 4) to the local model per gap.
- If no subagent is available, use COMPLETE mode: a single agent executes all 4 steps.
- The micro-context for each gap must include: the default template (or detected convention), the module's source code, 1-2 nearby existing fiches for style reference, and the target file path.

Required process:

1. Restate the documentation goal briefly.
2. Ask the user questions (if gap-integrator is primary). Use defaults for unanswered questions.
3. Detect whether the repo is on Vibebackbone rails.
4. State which governance files are available and relevant.
5. Identify the artifact type before writing. Examples:
   - feature note
   - implementation report
   - handoff note
   - audit report
   - integration guide
   - architectural note
6. State whether the result is:
   - canonical
   - best-effort compatible draft
7. If gap-integrator is primary, determine execution mode (COMPLETE vs DELEGATED) and state it.
8. Then write the documentation.

Constraints:

- Do not invent a Vibebackbone standard from the name alone.
- Do not claim canonical compliance unless governance files have been detected and read.
- Prefer concise operational documentation over bloated generic documentation.
- Keep the document type explicit.
- When delegating to a local model, provide the micro-context as defined in the skill — never send the full repo context.
- The default template is 5 fields: À propos, Emplacement, Surface publique, Configuration, Dépendances directes. Use it unless ≥ 3 existing fiches share a coherent structure.

Output format:

- Goal
- Governance used
- Artifact type
- Compliance level
- Execution mode (COMPLETE / DELEGATED)
- Scope applied

---

## Closeout sequence (mandatory — run after documentation is written)

After the documentation is written:

1. `t-vbb-commit-ready` → verdict + conventional commit message
2. `git add <docs written>` → `git commit -m "<message>"` → `git push`
3. Update `docs/SESSION.md` (clear if session done, note state if re-entry planned)
4. Update `docs/CONTEXT.md` (status, run link, decisions, open points, next action)

> Documentation files are persistent artifacts — they must be versioned. Do not stop after writing the docs. The doc-feature loop is not closed until git push is done.
- Write threshold
- Primary skill used
- Supporting skills
- Fallback justification
- Documentation
