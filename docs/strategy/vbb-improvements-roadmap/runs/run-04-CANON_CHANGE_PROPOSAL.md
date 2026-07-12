---
run_id: "2026-07-12_run04-canon-length-descriptions"
phase: "03_DECISION"
status: "APPROVED"
agent: "pi"
created_at: "2026-07-12"
human_validated_by: "Brice Sodini (project lead & canon owner) — 2026-07-12 via chat 'go' after policy alignment"
---

# Canon Change Proposal — Run 4 — SKILL.md description length target

## Current Canon

Today, `docs/CONVENTIONS.md` (Pillar 1 — Readability) covers:

- **Naming** — `camelCase`, descriptive names, well-known abbreviations.
- **Function design** — ~20 lines/function, decompose > 40 lines, one clear purpose.
- **Comments** — explain intent/constraints, never repeat obvious code.

It does **not** cover the length of the `description:` field in `SKILL.md` frontmatter. The validation in `skills/0-vbb-standard/SKILL.md` (step 6, PROCESS) verifies **precision** ("description is precise enough for Pi routing") but does not give a numeric target. `tools/vbb-contract-lint.py` validates CONTRACT.yaml (schema, gates, routing, schema version) but does **not** lint `SKILL.md` frontmatter content.

## Problem

Why does this matter:

1. **No objective judge for "this description is too long".** Today, a PR adding a `SKILL.md` with a 1500-char description has no canonical reason to be reduced. (AUDIT-E-001, P1.)
2. **Phase 1 (`1-vbb-*`) drift observed.** 10 of 16 skills in Phase 1 have descriptions > 500 chars, avg 506 chars. The longest is `1-vbb-logic-duplication-detector` at 669 chars / 13 lines. (AUDIT-E-003, P2.)
3. **No CI guard.** `vbb-contract-lint.py` does not lint `description:` length. A 2000-char description passes silently. (AUDIT-E-005, P2.)
4. **No tracking entry.** Unlike `LLM-LOAD-002` (5 SKILL.md > 13 KB), the description-length issue has no formal entry in `docs/AUDIT_STATUS.md`. (AUDIT-E-006, P2 — created by this proposal.)
5. **Mental model confusion risk.** Brice has previously thought that descriptions are "auto-reduced by Codex". They are not — `setup.sh` only replaces a block in `~/.codex/AGENTS.md`, not in-repo descriptions. An objective canon reduces that confusion by making the field obviously "hand-maintained, precision-validated". (AUDIT-E-002, P1 — partially addressed by Run 1 QW-1 in `skills/0-vbb-standard/SKILL.md` line 99.)

## Proposed Canon

Add the following **indicative** target in `docs/CONVENTIONS.md`, Pillar 1 — Readability, after the "Comments" subsection:

```markdown
### SKILL.md description length

The frontmatter `description:` of any `SKILL.md` is the routing surface used
by Pi / Codex / OpenCode to decide which skill to invoke.

**Target (indicative, non-blocking):**

- `description:` content should target **≤ 500 chars / ≤ 10 lines**.

**If exceeded:**

- The `tools/vbb-contract-lint.py` emits a **non-blocking** warning
  (no CI gate, no merge block). Rationale: a precise description may
  legitimately exceed the target to cover routing keywords, edge cases,
  or to disambiguate from sibling skills. Length is a proxy, not a
  quality guarantee.

**Hard promotion (future, after ≥ 1 observation cycle):**

- A future run may promote warning → error if `description:` content
  exceeds **800 chars / 15 lines**. This is intentionally left out of
  this run's canon: the policy must be observed before being enforced.

**Reference:** [`docs/audits/audit-E-skill-descriptions-20260712-1400.md`](audits/audit-E-skill-descriptions-20260712-1400.md)
**Tracking:** `AUDIT-E-006` in `docs/AUDIT_STATUS.md`.
```

Three properties of this canon:

1. **The target is indicative, not blocking.** No CI failure. The lint emits a warning that is visible to the developer and recorded in CI logs but never fails a build or a merge.
2. **The target is generous.** 500 chars / 10 lines. 60% margin to the future hard threshold (800 chars). Most current skills (44/64) already comply.
3. **The hard promotion is announced, not enacted.** Mentioning "future run, 800 chars" gives Brice and contributors a forward-looking signal without making today's canon brittle.

This is **not** a "compression rule". This is a **proxy-target canon** with an observation period before enforcement. Length drift becomes visible before it becomes punitive.

## Benefits

1. **An objective judge exists.** A PR review can ask "is this description above 500 chars? If yes, justify, or compress." Today there is no canonical question to ask.
2. **Phase 1 drift becomes addressable.** Run 5 (planned, not in this proposal) can use the target as a baseline to compress the 10 Phase 1 descriptions > 500 chars while preserving keywords.
3. **CI gets a non-blocking signal.** `vbb-contract-lint.py` outputs ≥ 20 warnings after Run 4 lands. These warnings appear in CI logs without breaking pipelines.
4. **Tracking parity with LLM-LOAD-002.** `AUDIT-E-006` in `docs/AUDIT_STATUS.md` gives the description-length drift the same visibility as the SKILL.md-size drift.
5. **Future enforcement is reversible.** If after the observation cycle the 800-char threshold proves too aggressive, it can be relaxed in a follow-up ADR — no consumer was locked into it today.

## Risks

1. **Risk: devs over-compress, hurting precision.**
   - **Severity**: medium.
   - **Mitigation**: the canon explicitly says "indicative, non-blocking". The lint warning is non-blocking. The 500-char target is generous (P90 of current skills ≈ 580 chars; even 580 chars is well within "precise routing description" territory). Brice's exchange (UN-E-4) was explicit: he wants "une bonne politique si c'est sûr que cela ne dénature pas la pertinence". The canon never blocks precision, only signals drift.

2. **Risk: the warning is ignored, becoming noise.**
   - **Severity**: low.
   - **Mitigation**: the warning lands in CI logs. `AUDIT-E-006` in `AUDIT_STATUS.md` makes it queryable via `vbb-status-dashboard`. Promotion to error at 800 chars (future run) prevents long-term noise — at some point, ignoring the warning becomes impossible.

3. **Risk: signature breakage in `vbb-contract-lint.py` (tuple arity 2 → 3).**
   - **Severity**: low (limited blast radius).
   - **Mitigation**: pre-merge gate P.R2 §5 (documentation coherence) verifies `grep -rn "lint_all()" tools/` returns only `vbb-contract-lint.py:__main__`. No other consumer is affected.

4. **Risk: drift detection is only manual (no auto-quantile tracking).**
   - **Severity**: low.
   - **Mitigation**: AUDIT-E-006 entry + dashboard query covers this for the next observation cycle. A future run could add a `tools/vbb-description-stats.py` (out of scope).

5. **Risk: future 800-char enforcement is premature.**
   - **Severity**: low.
   - **Mitigation**: announced as "future, after ≥ 1 observation cycle". Not enacted by Run 4. Reversible in a follow-up.

## Impact Analysis

### Files

| File | Change type | Description |
|------|-------------|-------------|
| `docs/CONVENTIONS.md` | canon modification | +15 lines, new subsection in Pillar 1 |
| `tools/vbb-contract-lint.py` | tool enhancement | +50 lines (new function + tuple arity + main output), exit code 0 if no errors (warnings do not change exit) |
| `docs/AUDIT_STATUS.md` | tracking entry | +1 line, `AUDIT-E-006` entry analogue to `LLM-LOAD-002` |
| `docs/runs/2026-07-12_run04-canon-length-descriptions/01_INTAKE.md` | new artefact | Run intake |
| `docs/runs/2026-07-12_run04-canon-length-descriptions/05_PATCH_SUMMARY.md` | new artefact | Run patch summary |
| `docs/runs/2026-07-12_run04-canon-length-descriptions/07_CLOSEOUT.md` | new artefact | Run closeout |
| `docs/ACTIVITY_LOG.md` | activity log entry | +1 line |

### Modules / Architecture Blocks

| Block | Impact | Action |
|-------|--------|--------|
| Canon layer (`docs/CONVENTIONS.md`) | Yes — Pillar 1 augmented | Modify |
| Tool layer (`tools/vbb-contract-lint.py`) | Yes — new check + signature change | Modify |
| Skill standard (`skills/0-vbb-standard/SKILL.md`) | No — line 99 already documents "not auto-truncated" (Run 1 QW-1) | None |
| Tracking (`docs/AUDIT_STATUS.md`) | Yes — new entry | Modify |

### Skills

| Skill | Change needed | Priority |
|-------|---------------|----------|
| None (no in-skill modification in this run) | Compression of 10 Phase 1 descriptions > 500 chars is deferred to Run 5 | — |

> Note: Run 4 does **not** modify any individual `SKILL.md`. It only sets up the canon, the warning, and the tracking entry. The actual compression (Run 5) is a separate, opt-in run that uses this canon as its baseline.

### Prompts

| Prompt | Change needed | Priority |
|--------|---------------|----------|
| None | No prompt currently references description length canonically | — |

### Tests

| Test | Must pass | Currently passing |
|------|-----------|-------------------|
| `python tools/vbb-contract-lint.py` | 0 errors, ≥ 20 warnings on current 64 skills | Yes (0 errors expected, 20 warnings expected from AUDIT-E distribution) |
| `python -c "from tools.vbb-contract-lint import lint_all; print(len(lint_all()))"` | imports OK, tuple arity 3 | Yes (post-modification) |
| `grep -rn "lint_all()" tools/` | returns only `vbb-contract-lint.py:__main__` | Yes (no other consumer) |
| Sanity check: `git diff docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md` | empty | Yes (no unrelated canon touched) |

## Migration Plan

### Phase 1 — Communication
- [x] Affected parties notified — Brice approved the policy in conversation: 500 chars target, warning non-bloquant, pas de hook automatique, run futur pour promotion
- [x] Migration timeline communicated — Run 4 executes after this proposal is approved

### Phase 2 — Parallel state
- [N/A] The change is **additive** — a new subsection is appended to CONVENTIONS.md, a new warning is added to vbb-contract-lint.py. There is no "old canon" to deprecate in parallel; today's canon is silent on this topic.

### Phase 3 — Cutover
- [ ] Edit `docs/CONVENTIONS.md` — add the new subsection in Pillar 1, after "Comments"
- [ ] Edit `tools/vbb-contract-lint.py` — add `check_description_length()`, update `lint_all()` signature, update `__main__` to print warnings
- [ ] Edit `docs/AUDIT_STATUS.md` — add `AUDIT-E-006` row
- [ ] Documentation updated (the "tracking" entry itself)

### Phase 4 — Verification
- [ ] `python tools/vbb-contract-lint.py` → 0 errors, ≥ 20 warnings (matches the 20 skills > 500 chars in AUDIT-E distribution), exit code 0
- [ ] `python -c "from tools.vbb-contract-lint import lint_all; rc = lint_all(); print(f'ok: errors={rc[0]}, warnings={len(rc[2])}')"` works
- [ ] `grep -rn "lint_all()" tools/ | grep -v __pycache__` → only `vbb-contract-lint.py:__main__`
- [ ] `git diff docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md` → empty
- [ ] Documentation links updated (none expected; the new canon subsection self-references `docs/audits/audit-E-...md` and `docs/AUDIT_STATUS.md` which both exist)
- [ ] No competing canon remains (the new subsection is the only place description length is canonically specified)

## Backward Compatibility

**Fully backward compatible.**

- No consumer breaks: `vbb-contract-lint.py`'s exit code is still 0 if no errors. Warnings are appended to stderr but never change the exit code.
- No contract is renamed or restructured. `CONTRACT.yaml` schema is untouched.
- No skill file is renamed or restructured (only an unused field is added to the canon spec, in CONVENTIONS.md).
- The change is purely additive: a new subsection, a new function, a new tracking row.

A consumer that parses `tools/vbb-contract-lint.py`'s `lint_all()` return will break only if it does `return value[0]` and expects a 2-tuple. **Pre-modification check**: `grep -rn "lint_all()" tools/ | grep -v __pycache__` confirms no other caller exists. The run's pre-merge gate verifies this.

## Human Decision

- [ ] **Approved** — proceed with migration plan (Phase 3 + 4 above)
- [ ] **Rejected** — document rationale, close proposal, do not modify canon
- [ ] **Needs revision** — return to author with feedback

**Validator signature**: Brice Sodini (project lead & canon owner) **Date**: 2026-07-12

> **Validation**: Brice a confirmé en chat la politique complète : cible 500 chars, warning non-bloquant, pas de pre-commit hook, promotion warning → error à 800 chars dans un run futur après observation. Cette validation est la porte canon pour la modification de `docs/CONVENTIONS.md`.

## Verification Loop

Required before implementation can be declared complete (Pre-merge gate REQUIS, route STRUCTURED):

- [ ] `python tools/vbb-contract-lint.py` → 0 errors, ≥ 20 warnings, exit code 0
- [ ] `python -c "from tools.vbb-contract-lint import lint_all; rc = lint_all(); ..."` → import OK, returns 3-tuple
- [ ] `grep -rn "lint_all()" tools/ | grep -v __pycache__` → only `vbb-contract-lint.py:__main__`
- [ ] `pytest tests/ -q` → all green (if a test suite exists; N/A otherwise)
- [ ] `git diff docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md` → empty
- [ ] `grep -n "SKILL.md description length" docs/CONVENTIONS.md` → 1 hit (new subsection)
- [ ] `grep -n "AUDIT-E-006" docs/AUDIT_STATUS.md` → 1 hit (new entry)
- [ ] Documentation links updated (no new cross-refs needed — self-contained)
- [ ] Closeout created in `docs/runs/2026-07-12_run04-canon-length-descriptions/07_CLOSEOUT.md`

## Closeout Notes

*To be filled after the Verification Loop passes.*

- **Final status**: _____________
- **Closed by**: _____________
- **Date**: _____________
- **Warnings emitted at closeout**: _____ (expected ≈ 20, matching AUDIT-E distribution)
- **Observations for future runs**:
  - The 500-char threshold is observed against today's skill distribution.
  - Promotion to error at 800 chars is deferred to a future run after ≥ 1 observation cycle.

---

**Status**: `PROPOSED` — awaiting Brice's signature for canon gate.