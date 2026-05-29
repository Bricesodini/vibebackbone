# CONVENTIONS — Vibebackbone Quality Conventions

**Version**: 1.1
**Date**: 2026-05-29
**Status**: Canonical but evolvable
**Context role**: quality-conventions-source

---

## Principle

At any point in time, Vibebackbone must expose **one active convention** for each structural concern.

A convention can evolve, but only through explicit proposal, human validation, documentation update, and migration strategy.

No parallel truth. No competing canonical logic. No silent divergence.

---

## Pillar 1 — Readability

### Naming

- Use `camelCase` for variables and functions when applicable to the target language.
- Prefer clear, descriptive names over abbreviations.
- Exception: well-known abbreviations accepted for domain-specific terms (e.g., `id`, `url`, `api`, `db`).

### Function design

- Target around **20 lines** per function.
- If a function exceeds ~40 lines, decompose it.
- One clear purpose per function.
- Private helpers are acceptable if they serve one public interface.

### Comments

- Comments explain **intent, constraints, or non-obvious choices**.
- Comments must **not** repeat obvious code.
- Global intent belongs in **documentation**, not scattered inline comments.
- Every non-trivial decision in code must be traceable to a doc, ADR, or inline rationale.

### Documentation scope

- Every skill must have a machine-readable `CONTRACT.yaml`.
- Every skill must have a human-readable `SKILL.md` in English.
- Every governance file must declare its role in its frontmatter or header.
- `docs/ARCHITECTURE.md` is the canonical structured source — never edit `docs/RELATIONS.md` directly.

### Language

- All skills and prompts → **English only**.
- Governance documents → may remain in the existing repo language.
- Agent-actionable artifacts → **English mandatory**.
- Machine-facing contracts → **English mandatory**, machine-readable only.

---

## Pillar 2 — Modularity

### Structural organization

- Prefer **domain-oriented modules** over purely technical folders.
- One module or architecture block must have **one clear responsibility**.
- Interface stability: internal implementation may evolve; interface must not break without migration.

### Experimental logic

- Experimental logic must be **isolated** (separate module or flag-documented).
- No experimental code in production-stable modules without explicit documentation and owner.

### Layer separation

- **UI must not carry deep business logic** — keep it at the interface layer.
- UI/UX additions must follow the current canonical design system or documented placement logic.
- Front pipeline: ENGINE (business logic) before VISUAL (aesthetics). No aesthetic decisions before UX stabilization.

### Testing

- Tests must be **algorithmic and automated**, not dependent on LLM judgment.
- Test coverage focuses on critical paths and known failure modes, not maximum percentage.
- Test files belong to the same module or adjacent test directory.

### Architecture discipline

- `docs/ARCHITECTURE.md` contains blocks with: `id`, `type`, `status`, `role`, `responsibilities`, `depends_on`, `impacts`, `files`, `contracts`, `tests`, `risks`.
- Every architecture-sensitive file must be referenced by at least one block `files:` pattern.
- `vbb-architecture.py lint` enforces coverage; a lint failure blocks implementation until fixed.

---

## Pillar 3 — Coherence & Convergence

### One active canonical way

- For any given concern, there must be **one active canonical solution**.
- Temporary workarounds are allowed if documented, time-limited, and linked to a removal or migration plan.
- Permanent competing logic is prohibited.

### Proposal discipline

- LLMs may **identify and propose** better logic.
- LLMs must **not modify canonical rules alone**.
- Human validation is **mandatory** for any canon change.

### Change process (see also `docs/templates/CANON_CHANGE_PROPOSAL.md.template`)

A canon change requires:

1. **Current canon** — what exists now
2. **Problem identified** — why it needs to change
3. **Proposed new logic** — what changes
4. **Benefits** — what improves
5. **Risks** — what could break
6. **Impacted files/modules/skills/prompts** — what is touched
7. **Migration plan** — how to transition without breaking consumers
8. **Human validation** — explicit sign-off
9. **Verification loop** — all checks pass
10. **Closeout** — change documented and merged

### Exceptions

Exceptions are allowed only if all of the following are true:

- **Documented** — explicit trace in run artifact or ADR
- **Temporary** — time-limited or linked to cleanup
- **Justified** — rationale explicit
- **Linked to owner or follow-up** — someone responsible
- **Paired with a removal or migration strategy** — exit path defined

### Verification loop (mandatory before declaring complete)

Before any implementation is declared complete:

```bash
python tools/vbb-architecture.py lint
python tools/vbb-architecture.py graph --write
python tools/vbb-contract-lint.py
python tools/vbb-loop-closure-check.py
pytest tests/ -q
bash scripts/vbb-ci-local.sh
```

If any command fails → do not mark as implemented. Document the failure, correct if in scope, re-run the full loop.

---

## Pillar 4 — Traçabilité

Traçabilité is embedded in the system and does not require a separate pillar.
It is covered by:

- ADRs (`docs/adr/`) — timestamped architecture decisions with rationale
- Run artifacts (`docs/runs/`) — 40+ runs, 92% closeout rate, phase files with frontmatter
- Audit reports (`docs/audits/`) — 17 timestamped reports by theme
- ARCHITECTURE.md — structured source of truth for architecture blocks
- Risk register (`docs/AUDIT_STATUS.md`) — P0/P1/P2/P3 tracked with status
- Context handoff (`docs/SESSION.md`) — session resume, next action
- TEMPORAL_PROVENANCE.md — provenance of evidence dates

No separate Traçabilité pillar is needed — it is a built-in property of all artifacts.

---

## Pillar 5 — Robustness

Robustness means: the system must detect failure, prevent regression, protect
invariants, and verify before declaring complete.

### P.R1 — Fail Explicitly

**Silent failures are prohibited.**

- Helper functions return error indicators (`None`, `False`, error list)
- Only CLI entry points (`main()`) may call `sys.exit()`
- An error must produce an explicit, actionable message

Rationale: Silent failures bypass verification and produce false confidence.
OPS-001 (now closed) demonstrated this risk.

### P.R2 — One Verification Loop

Before any implementation may be declared complete, all checks must pass:

```bash
python tools/vbb-architecture.py lint
python tools/vbb-architecture.py graph --write
python tools/vbb-contract-lint.py
python tools/vbb-loop-closure-check.py
pytest tests/ -q
bash scripts/vbb-ci-local.sh
```

If any command fails → **do not mark as implemented**. Document the failure,
correct if in scope, re-run the full loop.

This loop is the canonical verification mechanism for all implementation runs.

### P.R3 — Gate Before Action

**Blocking gates must be evaluated before execution.**

- Preconditions must be enforced before the action they protect
- A skill with unmet preconditions must not proceed
- The executor state machine (READY → RUNNING → EVALUATING → terminal)
  enforces this for contract-based execution
- For agent work, phase routing enforces phase prerequisites

### P.R4 — Invariant Protection

**Canonical invariants must never be bypassed.**

- The run closure invariant requires all phase artifacts for the declared voie
- `vbb-loop-closure-check.py` must report FAIL for incomplete runs
- A PASS verdict is only valid when all required artifacts exist and are valid
- `07_CLOSEOUT.md` cannot be created if the loop closure check fails

### P.R5 — Regression Prevention First

**Algorithmic validation precedes trust.**

- Every tool change must pass `pytest tests/ -q`, `vbb-contract-lint.py`,
  and `vbb-architecture.py lint`
- Every contract change must pass contract lint and dry-run
- Every architecture change must pass architecture lint and RELATIONS.md regeneration
- These checks are enforced by CI on every push

### P.R6 — Error Handling by Layer

**Errors are handled at the appropriate layer.**

| Layer | Pattern |
|-------|--------|
| Pure helper function | Return error indicator (`None`, `False`, error list) |
| Stateful function | Return error indicator or raise `ValueError` with context |
| CLI entry point (`main()`) | Call `sys.exit()` with appropriate code (0 = pass, 1 = fail) |

Rationale: Separation of concerns. Helpers remain callable without side effects.
Entry points own process control.

### P.R7 — Escalate on Risk Class Change

**A task started in FAST that reveals a higher risk class must escalate immediately.**

Escalation triggers:
- Data, authentication, production state → STRUCTURED
- Security, integrity, compliance, systemic behavior → AUDIT

Protocol: Stop → document in current artifact → reclassify route → resume.

### P.R8 — Independent Review Preferred

**Executor and reviewer should be independent whenever practical.**

- Phase 05 (EXECUTION) and phase 06 (REVIEW) should be in separate sessions
- If independence is impossible (small project, quick run), the review must
  explicitly state it is self-review, including: acknowledgment of conflict of
  interest, specific artifacts reviewed, compensating controls if any
- Self-review without disclosure produces cognitive bias and false confidence

---

## Quality Convention References

These rules are referenced in:

- `docs/ARCHITECTURE.md` (architecture-source block)
- `docs/INDEX.md` (navigation)
- `docs/PILOTAGE.md` (pilotage reference)
- `AGENTS.md` (agent grammar)
- `SYSTEM.md` (runtime behavior)

To change any rule in this file, use `docs/templates/CANON_CHANGE_PROPOSAL.md.template`.

---

**Version history**: 1.0 (2026-05-29) — initial canonical quality conventions · 1.1 (2026-05-29) — Pillar 5 (Robustness) integrated · OPS-001/002/003 closed