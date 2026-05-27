---
audit_type: mvp-start-readiness
run_id: "2026-05-27_2142_mvp-start-readiness-audit"
status: PARTIAL
created_at: "2026-05-27T20:05:00Z"
agent: codex
---

# MVP Start Readiness Integration Audit

## Verdict

`PARTIAL` — l'integration est necessaire et faisable, mais elle doit etre traitee comme un changement systemique de gouvernance. Le depot ne possede pas encore de route MVP START, ni de gate canonique "no code before readiness", et des incoherences documentaires preexistantes doivent etre corrigees dans le meme chantier.

## Inventory (by class)

| Class | Files |
|---|---|
| Canonical governance | `AGENTS.md`, `SYSTEM.md`, `docs/CONTEXT.md`, `docs/PILOTAGE.md`, `docs/AGENTIC_RUN_PROTOCOL.md` |
| Routing | `prompts/t-p-vbb-phase-router.md`, `docs/router/ROUTER_MATRIX.md`, `tools/vbb-phase-router.py`, `skills/INDEX.yaml` |
| Startup/project framing | `prompts/0-p-vbb-before-building.md`, `prompts/1-p-vbb-project-init.md`, `skills/0-vbb-scope-freeze`, `skills/0-vbb-audit-readiness`, `skills/1-vbb-intent-decomposer` |
| Public narrative | `README.md`, `GUIDE.md`, `PROMPTS_ARCHITECTURE.md`, `CLAUDE.md` |
| Release/status | `docs/AUDIT_STATUS.md`, `CHANGELOG.md`, `RELEASE_CHECKLIST.md`, `docs/INDEX.md` |

## Drift & contradictions

| Area | Evidence | Required correction |
|---|---|---|
| Prompt count | Local count is 33. `README.md` and `docs/CONTEXT.md` say 33, but `CHANGELOG.md` and `CLAUDE.md` say 32. | Harmonize active docs to 33 before implementation, then recalculate after adding any prompt. |
| Route count wording | `docs/PILOTAGE.md` says "The 4 routes" while the table includes FAST-ZERO, FAST-MINIMAL, FAST, STRUCTURED, AUDIT, CLOSEOUT. `CHANGELOG.md` says "4 agentic routes" but lists six labels. | Decide vocabulary: 4 route families with FAST levels, or 6 route labels. Add MVP START consistently. |
| Readiness gate | Existing `before-building` prompt checks build prerequisites but is not a canonical protocol and does not define RICO minimum fields. | Add `docs/MVP_START_PROTOCOL.md`; keep prompt as executable entrypoint or create a dedicated MVP prompt. |
| Router coverage | `python tools/vbb-phase-router.py "rico readiness mvp start" --dry-run` returns no match. | Add indexed `0-vbb-rico-readiness` contract triggers and verify route. |
| Release state | `CONTEXT.md` says v1.0 hardening complete and next action tag v1.0.0; release files are rc.1. | Use one narrative: rc.1 ready for v1 tag, not final v1 already released. |

## Impact map

### Direct changes required

- `docs/MVP_START_PROTOCOL.md` — new canonical document.
- `docs/CONTEXT.md` — lightweight pointer to MVP Start protocol.
- `docs/PILOTAGE.md` — route or equivalent gate for MVP START.
- `docs/AGENTIC_RUN_PROTOCOL.md` — readiness validation and blocking rules before execution.
- `skills/0-vbb-rico-readiness/SKILL.md` — new Phase 0 skill.
- `skills/0-vbb-rico-readiness/CONTRACT.yaml` — new contract v0.3.
- `skills/INDEX.yaml` — index new skill.
- `prompts/t-p-vbb-phase-router.md` and `docs/router/ROUTER_MATRIX.md` — routing matrix update.

### Conditional changes

- `prompts/0-p-vbb-before-building.md` — either update to delegate to RICO readiness or leave as post-readiness build gate.
- New prompt `prompts/0-p-vbb-mvp-start.md` — recommended only if a session entrypoint is needed separate from the skill.
- `README.md`, `GUIDE.md`, `PROMPTS_ARCHITECTURE.md`, `CLAUDE.md`, `SYSTEM.md`, `AGENTS.md`, `CHANGELOG.md`, `RELEASE_CHECKLIST.md`, `docs/INDEX.md`, `docs/AUDIT_STATUS.md` — counter and narrative harmonization.

## Proposed canonical structure

1. `docs/CONTEXT.md` remains the boot router and points to `docs/MVP_START_PROTOCOL.md`.
2. `docs/MVP_START_PROTOCOL.md` becomes the required pre-implementation reference for new MVPs.
3. `docs/ARCHITECTURE.md` is produced only after readiness validation; it records architecture decisions, not raw RICO framing.
4. `0-vbb-rico-readiness` becomes the executable readiness evaluator.
5. `0-vbb-scope-freeze` and `0-vbb-audit-readiness` remain separate gates for scope stability and auditability.

## Blocking questions for implementation

1. Should MVP START be counted publicly as a fifth route, or documented as a mandatory pre-route/gate before STRUCTURED EXECUTION?
2. Should a new prompt be created, or should existing `0-p-vbb-before-building.md` be updated to call `0-vbb-rico-readiness` first?
3. Should historical release docs be amended in place, or should an `Unreleased` section record the counter correction?

## Validation plan

After implementation, run:

```bash
python tools/vbb-contract-lint.py
python tools/vbb-contract-runtime.py --all --dry-run
python tools/vbb-phase-router.py "rico readiness mvp start" --dry-run
bash scripts/vbb-ci-local.sh
find skills -mindepth 1 -maxdepth 1 -type d | wc -l
find skills -mindepth 2 -maxdepth 2 -name CONTRACT.yaml | wc -l
find prompts -type f -name '*.md' | wc -l
```

## Recommended implementation order

1. Add `docs/MVP_START_PROTOCOL.md`.
2. Add `0-vbb-rico-readiness` skill and contract.
3. Index the skill and verify router match.
4. Update `PILOTAGE`, `AGENTIC_RUN_PROTOCOL`, prompt router and router matrix.
5. Update `CONTEXT` as a compact pointer.
6. Harmonize counters and release/status docs.
7. Run validations and produce closeout.

## Residual risk

The largest risk is partial integration: a Markdown rule that says "no code before readiness" while the executable router and prompt entrypoints still allow normal STRUCTURED execution. The implementation must land documentation, contract, router, and prompt changes together.
