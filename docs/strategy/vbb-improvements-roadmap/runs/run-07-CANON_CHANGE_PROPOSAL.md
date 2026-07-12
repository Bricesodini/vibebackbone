---
run_id: "2026-07-12_run07-handoff-vs-closeout"
phase: "03_DECISION"
status: "APPROVED"
agent: "pi"
created_at: "2026-07-12"
human_validated_by: "Brice Sodini (project lead & canon owner) — 2026-07-12 via chat 'go' after UN-C-1/2/3 default-policy alignment"
---

# Canon Change Proposal — Run 7 — HANDOFF vs CLOSEOUT route split

## Current Canon

Today, `docs/PILOTAGE.md` (the canonical operational entry point for agents) defines 4 route families. The **CLOSEOUT** route is described as:

| **CLOSEOUT** | End of session, handoff, pause | `t-vbb-commit-ready` → git commit → git push → update `SESSION.md` + `CONTEXT.md` | — |

This single route covers **three semantically distinct usages**:

1. **End of session, run complete** — the run is done, nothing meaningful remains.
2. **Handoff** — the run is paused, next session must resume from `SESSION.md`.
3. **Pause** — explicit pause without committing to a next session.

The action prescribed is identical for all three: `t-vbb-commit-ready` → commit → push → update `SESSION.md` + `CONTEXT.md`. The agent receiving a "CLOSEOUT" instruction cannot tell from the route alone which of the three usages applies.

Additionally, the artifact `07_CLOSEOUT.md` (whose template is in `docs/templates/07_CLOSEOUT.md.template`) now carries an explicit `kind: HANDOFF | CLOSEOUT` field (added by Run 1 QW-2, addressing AUDIT-C-001), but the **route** layer has not been updated to reflect this discrimination.

## Problem

1. **Agent-level ambiguity.** An agent receiving "do CLOSEOUT" must inspect `SESSION.md` and the `kind:` field of the latest `07_CLOSEOUT.md` to know whether to:
   - empty `SESSION.md` (run is done) — CLOSEOUT
   - preserve `SESSION.md` (handoff) — HANDOFF
   - set a pause marker — PAUSE

   The route should encode this discrimination, not push it to a downstream artifact inspection.

2. **Audit tool ambiguity.** `vbb-status-dashboard.py` and similar tools scan artifacts. Today, a `07_CLOSEOUT.md` with `kind: HANDOFF` looks like a final closeout unless the scanner reads the `kind:` field. A separate route family name makes the discrimination visible at the route layer.

3. **No history archive.** `SESSION.md` (gitignored) is overwritten each session. Without a local history archive (e.g., `docs/SESSION.history/`), a machine reinstall loses the entire handoff trail. (AUDIT-C-003, P2.)

4. **Prompt-level gap.** `prompts/canonical/07-p-vbb-closeout.md` does not compute the `kind:` automatically — agents must rely on tribal knowledge to set it. (AUDIT-C-004, P2 derived.)

## Proposed Canon

Modify `docs/PILOTAGE.md` to split the single `CLOSEOUT` route into two semantically explicit routes:

| **CLOSE-HANDOFF** | Pause, travail non terminé, reprise attendue | `t-vbb-commit-ready` → git commit → git push → archive `SESSION.md` to `docs/SESSION.history/` → update `SESSION.md` for next session | — |
| **CLOSE-FINAL** | Fin de session, run terminé | `t-vbb-commit-ready` → git commit → git push → empty `SESSION.md` → update `CONTEXT.md` | — |

Additional supporting changes (non-canon, included for context):

- `prompts/canonical/07-p-vbb-closeout.md` adds a **Étape 1 — Calculer le kind** section that computes `kind:` automatically based on `status`, `next_phase`, and `SESSION.md` content.
- `docs/SESSION_RULES.md` adds a **Handoff vs Closeout** section documenting the discrimination.
- `.gitignore` adds `docs/SESSION.history/` so the local archive is not versioned.
- `docs/SESSION.md` (gitignored) gains a note explaining the archive convention.

**Out of scope (explicitly):**
- `AGENTIC_RUN_PROTOCOL.md` phase 07 stays `CLOSEOUT` (artifact convention unchanged — only route layer changes).
- The artifact `07_CLOSEOUT.md` is **not** renamed `07_HANDOFF.md` (R-C-2 rejected — see Brice's exchange on UN-C-1/2).
- `docs/CONVENTIONS.md` not modified (concept HANDOFF/CLOSEOUT belongs to `SESSION_RULES.md`, not to the quality pillars).

## Benefits

1. **Route-layer discrimination.** Agents receiving "do CLOSE-HANDOFF" vs "do CLOSE-FINAL" know immediately which actions to take (preserve vs empty `SESSION.md`, archive vs not).
2. **Self-documenting.** The route name encodes the semantics. No need to read SESSION.md first.
3. **Audit-tool friendly.** Scanners can filter by route name (`CLOSE-HANDOFF` vs `CLOSE-FINAL`) without parsing artifact frontmatter.
4. **History continuity.** `docs/SESSION.history/{date}.md` (gitignored) preserves handoffs across machine reinstalls.
5. **Backward compatible.** Existing CLOSEOUT usage is **not** broken — the new routes are stricter subsets. An agent that used the old CLOSEOUT for both semantics will need to choose CLOSE-HANDOFF or CLOSE-FINAL explicitly, which is the intended clarity gain.

## Risks

1. **Agents still use the old "CLOSEOUT" label by reflex.**
   - **Severity**: low.
   - **Mitigation**: this proposal includes a pre-merge gate that grep's PILOTAGE.md for both new labels. A `vbb-status-dashboard` advisory can flag stale route usage if needed. Documentation updates propagate to `SESSION_RULES.md` (QW-C-2).

2. **The two routes create ambiguity about which to choose.**
   - **Severity**: low.
   - **Mitigation**: the discriminator is `SESSION.md` content + `status` + `next_phase`. The prompt `07-p-vbb-closeout.md` (QW-C-1) computes it explicitly. SESSION_RULES.md documents the rule of thumb.

3. **`docs/SESSION.history/` accumulates without bound.**
   - **Severity**: very low.
   - **Mitigation**: gitignored, local-only. A periodic cleanup script (out of scope) can prune old entries. Not committed, so no repo bloat.

4. **Splitting CLOSEOUT breaks a 3rd-party agent that grep'd "CLOSEOUT".**
   - **Severity**: low.
   - **Mitigation**: `vbb-status-dashboard.py` and similar tools are in-repo and updated if needed (out of scope for this run, but trivial).

5. **AGENTIC_RUN_PROTOCOL.md keeps "CLOSEOUT" as phase 07 name while PILOTAGE.md renames the route.**
   - **Severity**: low.
   - **Mitigation**: deliberate separation — phase = artifact convention, route = triage decision. Documented in PILOTAGE.md via cross-references. If confusion arises, a future run can rename the phase.

## Impact Analysis

### Files

| File | Change type | Description |
|------|-------------|-------------|
| `docs/PILOTAGE.md` | canon modification | replace 1 row (CLOSEOUT) with 2 rows (CLOSE-HANDOFF, CLOSE-FINAL) in the route families table |
| `prompts/canonical/07-p-vbb-closeout.md` | prompt enhancement | add "Étape 1 — Calculer le kind" section |
| `docs/SESSION_RULES.md` | governance doc | add "Handoff vs Closeout" section |
| `.gitignore` | gitignore | add `docs/SESSION.history/` entry |
| `docs/SESSION.md` | local (gitignored) doc | add archive convention note |
| `docs/runs/2026-07-12_run07-handoff-vs-closeout/01_INTAKE.md` | new artefact | Run intake |
| `docs/runs/2026-07-12_run07-handoff-vs-closeout/05_PATCH_SUMMARY.md` | new artefact | Run patch summary |
| `docs/runs/2026-07-12_run07-handoff-vs-closeout/07_CLOSEOUT.md` | new artefact | Run closeout |
| `docs/ACTIVITY_LOG.md` | activity log entry | +1 line |

### Modules / Architecture Blocks

| Block | Impact | Action |
|-------|--------|--------|
| Canon (`docs/PILOTAGE.md`) | Yes — route table modified | Modify |
| Canon (`docs/AGENTIC_RUN_PROTOCOL.md`) | No — phase 07 stays `CLOSEOUT` (artifact convention) | None |
| Canon (`docs/CONVENTIONS.md`) | No — quality pillars not affected | None |
| Canon (`docs/MVP_START_PROTOCOL.md`) | No | None |
| Prompt (`07-p-vbb-closeout.md`) | Yes — adds Étape 1 | Modify |
| Tool (`t-vbb-session-handoff`) | No — already handles SESSION.md update; archive is a SESSION.md convention, not a tool change | None (note in SESSION.md only) |

### Skills

| Skill | Change needed | Priority |
|-------|---------------|----------|
| None | No skill modification in this run | — |

### Prompts

| Prompt | Change needed | Priority |
|--------|---------------|----------|
| `prompts/canonical/07-p-vbb-closeout.md` | Add Étape 1 (compute kind automatically) | M (Run 7) |

### Tests

| Test | Must pass | Currently passing |
|------|-----------|-------------------|
| `python tools/vbb-contract-lint.py` | 0 errors, 0 warnings | Yes (no contract touched) |
| `grep "CLOSE-HANDOFF\|CLOSE-FINAL" docs/PILOTAGE.md` | 2 hits | Will be after run |
| `grep "CLOSE-HANDOFF\|CLOSE-FINAL" docs/AGENTIC_RUN_PROTOCOL.md` | 0 hits (artifact name unchanged) | Yes |
| `git diff docs/CONVENTIONS.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md` | empty | Yes (no unrelated canon touched) |

## Migration Plan

### Phase 1 — Communication
- [x] Affected parties notified — Brice approved the policy in conversation (UN-C-1/2/3 default choices accepted, "go" on the plan).
- [x] Migration timeline communicated — Run 7 executes immediately after this proposal is approved.

### Phase 2 — Parallel state
- [N/A] No parallel canon required. The new routes are **stricter subsets** of the old CLOSEOUT — old usage remains legal until agents learn the new naming. No deprecation needed because:
  - No in-repo script grep's "CLOSEOUT" as a route name (only as a phase/artifact name).
  - `vbb-status-dashboard.py` reads `kind:` from artifact frontmatter, not route names.

### Phase 3 — Cutover
- [ ] Edit `docs/PILOTAGE.md` — replace the CLOSEOUT row with CLOSE-HANDOFF + CLOSE-FINAL rows
- [ ] Edit `prompts/canonical/07-p-vbb-closeout.md` — add Étape 1
- [ ] Edit `docs/SESSION_RULES.md` — add Handoff vs Closeout section
- [ ] Edit `.gitignore` — add `docs/SESSION.history/`
- [ ] Edit `docs/SESSION.md` (gitignored) — add archive convention note

### Phase 4 — Verification
- [ ] `python tools/vbb-contract-lint.py` → 0 errors, 0 warnings
- [ ] `grep "CLOSE-HANDOFF" docs/PILOTAGE.md` → 1 hit
- [ ] `grep "CLOSE-FINAL" docs/PILOTAGE.md` → 1 hit
- [ ] `grep "CLOSEOUT" docs/PILOTAGE.md` → 0 hits (the old route label is gone)
- [ ] `grep "Étape 1 — Calculer le kind" prompts/canonical/07-p-vbb-closeout.md` → 1 hit
- [ ] `grep "Handoff vs Closeout" docs/SESSION_RULES.md` → 1 hit
- [ ] `grep "SESSION.history" .gitignore` → 1 hit
- [ ] `git diff docs/CONVENTIONS.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md` → empty
- [ ] Documentation links updated (cross-refs in SESSION_RULES.md and 07-p-vbb-closeout.md resolve)
- [ ] No competing canon remains (PILOTAGE.md is the only place route families are defined)

## Backward Compatibility

**Fully backward compatible at the artifact layer.** The artifact `07_CLOSEOUT.md` keeps its name and its `kind:` field (introduced by Run 1). No existing artifact is renamed or restructured.

**Mildly disruptive at the route layer.** Agents that grep "CLOSEOUT" as a route label in `PILOTAGE.md` will find nothing. They must use "CLOSE-HANDOFF" or "CLOSE-FINAL" instead. **Pre-verification**: `grep -rn '"CLOSEOUT"' tools/` returns no matches in tools (the only `tools/vbb-*.py` reference to CLOSEOUT is for artifact paths in `t-vbb-loop-closure-check.py` and `t-vbb-context-compactor.py`, which is the artifact name and is preserved). So no in-repo tool breaks.

If a 3rd-party agent relies on "CLOSEOUT" as a route label, it will need to migrate. This is acceptable: the gain in clarity is worth the small migration cost.

## Human Decision

- [x] **Approved** — proceed with migration plan
- [ ] **Rejected** — document rationale, close proposal, do not modify canon
- [ ] **Needs revision** — return to author with feedback

**Validator signature**: Brice Sodini (project lead & canon owner) **Date**: 2026-07-12

> **Validation**: Brice confirmed in chat via "go" after the policy alignment on UN-C-1 (logical distinction, not physical file rename), UN-C-2 (no physical rename acceptable), UN-C-3 (local non-versioned archive in `docs/SESSION.history/`). This validation is the canon gate for modifying `docs/PILOTAGE.md`.

## Verification Loop

Required before implementation can be declared complete (Pre-merge gate REQUIS, route STRUCTURED):

- [ ] `python tools/vbb-contract-lint.py` → 0 errors, 0 warnings
- [ ] `grep "CLOSE-HANDOFF" docs/PILOTAGE.md` → 1 hit
- [ ] `grep "CLOSE-FINAL" docs/PILOTAGE.md` → 1 hit
- [ ] `grep "CLOSEOUT" docs/PILOTAGE.md` → 0 hits (old route label gone)
- [ ] `grep "Étape 1 — Calculer le kind" prompts/canonical/07-p-vbb-closeout.md` → 1 hit
- [ ] `grep "Handoff vs Closeout" docs/SESSION_RULES.md` → 1 hit
- [ ] `grep "SESSION.history" .gitignore` → 1 hit
- [ ] `grep -rn '"CLOSEOUT"' tools/` → no false positive (only artifact-path references)
- [ ] `git diff docs/CONVENTIONS.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md` → empty
- [ ] Documentation links updated (none new needed — cross-refs use existing files)
- [ ] Closeout created in `docs/runs/2026-07-12_run07-handoff-vs-closeout/07_CLOSEOUT.md`

## Closeout Notes

*To be filled after the Verification Loop passes.*

- **Final status**: _____________
- **Closed by**: _____________
- **Date**: _____________

---

**Status**: `APPROVED` — Brice's signature is in place. Ready for execution.