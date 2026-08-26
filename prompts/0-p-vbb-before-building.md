---
description: Pre-build validation gate — verify that the project is ready to start building a new feature
---

Verify that the project is ready to start building: $@

## Objective

Before writing any code, validate that every prerequisite is in place for
healthy, traceable development. This prompt is the product architect's
pre-flight checklist before starting a substantial workstream.

## Preferred Vibebackbone skills

- `0-vbb-rico-readiness`
- `0-vbb-scope-freeze`
- `1-vbb-intent-decomposer`
- `t-vbb-dependency-mapper`
- `t-vbb-project-context-init`
- `t-vbb-anti-slop-gate`

## Skill routing and chaining rule

### Phase 1 — Verify governance

1. Check `$PWD/AGENTS.md`, otherwise `AGENTS.md` at the effective Git root;
   read the one contract found before project state. It is operational context
   and cannot alter VBB governance.
2. Verify that the repository is on Vibebackbone rails (docs/PROJECT_MODE.md exists).
3. If absent → run `t-vbb-project-context-init` to initialize it.
4. If present → read `docs/SESSION.md` and `docs/AUDIT_STATUS.md`.
5. If `docs/AUDIT_STATUS.md` contains BLOCKED items → STOP. Resolve them before continuing.

### Phase 2 — Verify RICO / MVP START readiness

1. If the work is an MVP from scratch, a RICO, an initial brief, or a request to code before framing → run `0-vbb-rico-readiness`.
2. If verdict = BLOCKED or UNKNOWN → STOP. Produce only the blocking questions.
3. If verdict = PARTIAL → remain in framing. Do not create application code, migrations, endpoints, models, UI components, Docker structures, persistence, or business logic.
4. If verdict = READY → continue to scope and architecture.

### Phase 3 — Verify scope

1. Run `0-vbb-scope-freeze` on the relevant scope.
2. If verdict = BLOCKED → the scope is insufficiently defined. STOP.
3. If verdict = PARTIAL → continue, but record the ambiguous areas.
4. If verdict = READY → the scope is frozen; continue.

### Phase 4 — Verify architecture

1. Verify that `docs/ARCHITECTURE.md` exists.
2. If absent → run `t-vbb-dependency-mapper`.
3. If present but stale (> 30 days or > 50 commits) → propose an update.

### Phase 5 — Verify code state

1. Run `t-vbb-anti-slop-gate` to verify the code surface.
2. If verdict = BLOCKED (broken build, failing tests) → STOP. Repair it before building.
3. If verdict = READY_WITH_WARNINGS → record the warnings and continue.
4. If verdict = READY → the surface is clean.

### Phase 6 — Decompose intent

1. Run `1-vbb-intent-decomposer` on the provided specification.
2. Use the resulting product plan as the roadmap.
3. Validate the plan with the architect before coding.

## Required process

1. **Restate** the objective: which feature will be built.
2. **Phase 1** — Verify or create project governance.
3. **Phase 2** — Validate RICO / MVP START readiness.
4. **Phase 3** — Freeze the scope.
5. **Phase 4** — Verify or create the architecture map.
6. **Phase 5** — Run the anti-slop gate.
7. **Phase 6** — Decompose the intent into a plan.
7. **Summarize** the readiness verdict, risks, and plan.

## Gate criteria — the project is ready to build when:

- [ ] Vibebackbone governance is present (PROJECT_MODE, SESSION, AUDIT_STATUS)
- [ ] RICO readiness is READY for an MVP from scratch or an initial brief
- [ ] Scope is frozen and documented
- [ ] Architecture is mapped (ARCHITECTURE.md)
- [ ] Code surface is clean (anti-slop READY or READY_WITH_WARNINGS)
- [ ] A product implementation plan exists (intent-decomposer ACTIONABLE)
- [ ] AUDIT_STATUS.md contains no BLOCKED items

## Blocking conditions

If a phase produces BLOCKED → do not proceed to the next phase.
Present the blocker to the architect and ask: "Do you want to resolve this before continuing?"

If the architect insists on continuing despite a blocker → document the risk acceptance
in SESSION.md and continue.

## Output format

- **Goal**
- **Phase 1 — Governance**: verdict
- **Phase 2 — RICO readiness**: rico-readiness verdict
- **Phase 3 — Scope**: scope-freeze verdict
- **Phase 4 — Architecture**: ARCHITECTURE.md state
- **Phase 5 — Code surface**: anti-slop verdict
- **Phase 6 — Plan**: plan summary (task count, waves, risks)
- **Readiness verdict**: READY / READY_WITH_CAVEATS / NOT_READY
- **Blockers**: list of blocking items
- **Next action**: start Wave 1 or resolve the blockers

---

## Agent protocol alignment

**Corresponding phases**: 01_INTAKE (phases 1–2) + 04_PLAN (phase 5)

This prompt covers several phases in one session. It suits contexts where speed takes priority over strict role separation.

**Expected artifacts**:
- `docs/runs/YYYY-MM-DD_HHmm_slug/01_INTAKE.md` — restatement + readiness verdict
- `docs/runs/YYYY-MM-DD_HHmm_slug/04_FIX_PLAN.md` — phase 5 product plan

Create these files at the end of each corresponding phase.

**Context warning**: this prompt orchestrates 5 phases and several skills. If LLM context is limited (<128K available tokens), prefer two separate sessions: `canonical/01-p-vbb-intake`, then `canonical/04-p-vbb-plan`.

**Handoff to 05_EXECUTION**:

If verdict is READY or READY_WITH_CAVEATS:
- State the planned runs and which one to execute first
- List target files
- Document accepted risks

If verdict is NOT_READY:
- List blockers and the required action for each
- Do not proceed to execution before resolution
