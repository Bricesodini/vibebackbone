---
description: Post-refactoring code↔doc coherence pipeline — audit, gap fill, harmonize, and prepare clean handoff
---

Run a complete post-refactoring code↔documentation coherence audit for: $@

## Objective

After substantial refactoring, debugging, or technical-debt reduction, restore
a sound baseline by verifying that ALL documentation accurately reflects the
actual state of the code.

Complete pipeline:

1. Audit code↔doc coherence (detect gaps)
2. Fill gaps (write missing documentation)
3. Harmonize documentation (eliminate redundancy)
4. Produce a clean handoff for continued work

## Preferred Vibebackbone skills

- `1-vbb-code-doc-coherence-auditor`
- `1-vbb-code-doc-gap-integrator`
- `1-vbb-doc-harmonizer`
- `t-vbb-session-handoff`

## Skill routing and chaining rule

### Phase 1 — Coherence audit

Run `1-vbb-code-doc-coherence-auditor` first.
It is the foundation: it produces the complete inventory and determines whether
the following phases are necessary.

If the user has not specified the scope, ask before scanning:
"Which scope: the entire repository or specific modules?"

- "Which modules were refactored recently?"

After the audit report, analyze the verdict:

| Verdict      | Action                                                           |
| ------------ | ---------------------------------------------------------------- |
| `COHERENT`   | Go directly to Phase 4 (handoff). The project is clean.           |
| `PARTIAL`    | Continue to Phase 2 for HIGH/MEDIUM gaps only.                    |
| `FRAGMENTED` | Continue to Phase 2 + Phase 3. The remediation is more extensive. |
| `UNKNOWN`    | Ask the user for clarification before continuing.                |

### Phase 2 — Gap filling

Run `1-vbb-code-doc-gap-integrator` to write missing documentation.

Use the coherence-auditor report as the **hint list**:

- Pass identified MISSING gaps as `known gaps` to the gap-integrator input
- Target the scope at refactored areas when specified
- Writing threshold: `HIGH+MEDIUM` in `PARTIAL` mode, `ALL` in `FRAGMENTED` mode

Do NOT run the gap-integrator if the coherence-auditor verdict is `COHERENT`.

### Phase 3 — Documentation harmonization

Run `1-vbb-doc-harmonizer` to:

- Address `REDUNDANT` gaps identified by the coherence-auditor
- Consolidate documentation after adding missing reference sheets (Phase 2)
- Propose an archival plan for obsolete documents

This phase is optional when there are few REDUNDANT items (< 3) and their severity is LOW.

### Phase 4 — Closeout handoff

Run `t-vbb-session-handoff` to seal the project's clean state.

The handoff must include:

- Summary of completed remediation work
- Verdicts from the 3 passes (audit → gap fill → harmonization)
- Accepted residual gaps (unaddressed LOW items, intentional orphans)
- Recommended next actions

### Verdict cascade rule

If phase N has a `BLOCKED` verdict, do not run phase N+1.
Ask the user to resolve the blocker.

If the gap-integrator produces a `READY` verdict, proceed to the next phase.
If `PARTIAL`, continue but report remaining gaps in the final handoff.
If `BLOCKED`, stop and ask for clarification.

### Manual fallback

Manual fallback is allowed only when a named skill is absent from the active `[Skills]` list.
If fallback is necessary, name the missing skill and explain why.

## Required process

1. **Restate** the objective in one sentence.
2. **Ask** for the scope and refactored areas (if not provided).
3. **Phase 1** — Run `1-vbb-code-doc-coherence-auditor`.
4. **Analyze** the verdict and select the next phases.
5. **Phase 2** — Run `1-vbb-code-doc-gap-integrator` (if needed), with hints from the audit report.
6. **Phase 3** — Run `1-vbb-doc-harmonizer` (if needed), with REDUNDANT items from the audit report.
7. **Phase 4** — Run `t-vbb-session-handoff`.
8. **Summarize** the complete pipeline and final state.

---

## Closeout sequence (mandatory — run after Phase 4 handoff)

After the Phase 4 handoff is produced:

1. `t-vbb-commit-ready` → verdict + conventional commit message
2. `git add <docs modified during the pipeline>` → `git commit -m "<message>"` → `git push`
3. Update `docs/SESSION.md` (clear if session done, note state if re-entry planned)
4. Update `docs/CONTEXT.md` (status, run link, decisions, open points, next action)

> The coherence pipeline produces and modifies persistent artifacts (audit reports, gap docs, harmonized doc) — they must be committed and pushed. Do not stop after the handoff. The post-refacto coherence loop is not closed until git push is done.

## Constraints

- Do not skip Phase 1 (audit). It is the foundation of the entire pipeline.
- Do not run the gap-integrator without passing it the audit report as a hint list.
- Do not run the doc-harmonizer without passing it the detected REDUNDANT items.
- Keep responsibilities distinct: the coherence-auditor detects, the gap-integrator writes, and the doc-harmonizer consolidates.
- Clearly distinguish intentional orphans (architecture, guides) from accidental orphans.
- Always run Phase 4 (handoff), even when the verdict is `COHERENT`, to preserve traceability.
- If the user interrupts the pipeline during a phase, produce a partial handoff with the known state.
- Follow the verdict cascade rule: BLOCKED → stop, PARTIAL → continue with a warning.

## Output format

- **Goal**: one-sentence summary
- **Scope**: audited scope
- **Phase 1 — Verdict**: coherence-auditor verdict + summary
- **Phase 2 — Gap fill**: if run, verdict + reference sheets written
- **Phase 3 — Harmonization**: if run, verdict + actions
- **Phase 4 — Handoff**: final handoff summary
- **Final state**: `ready to resume` | `ready with caveats` | `remediation required`
- **Residual gaps**: remaining work
- **Recommended next action**
