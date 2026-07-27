---
load_policy: reference
context_role: quality-conventions-source
phase: transverse
status: active
---

# CONVENTIONS — Vibebackbone Quality Conventions

**Version**: 1.1
**Date**: 2026-05-29
**Status**: Canonical but evolvable
**Context role**: quality-conventions-source

`load_policy: reference` — this file is the canonical source for quality
conventions. The mandatory verification loop (P.R2) commands themselves
live in [`docs/REFERENCE/pre-merge-gate.md`](REFERENCE/pre-merge-gate.md)
(can unique) — they are not duplicated here.

---

## Principle

At any point in time, Vibebackbone must expose **one active convention** for each structural concern.

A convention can evolve, but only through explicit proposal, human validation, documentation update, and migration strategy.

No parallel truth. No competing canonical logic. No silent divergence.

---

## Foundational principle — Governed capitalization

Every qualified implementation is examined for reusable engineering learning.
Learning is not promoted by plausibility or by a delivery `PASS`.

Promotion requires:

1. evidence independent enough for the claimed scope;
2. a knowledge audit;
3. a distinct independent review;
4. an explicit human decision;
5. integration into one final authority.

Knowledge records, playbooks, guides, runs, reviews and closeouts document the
path; they are not the final authority. Canonical knowledge is immutable and
evolves only through a new governed version that supersedes the prior one.

The complete lifecycle and documentary boundaries are canonical in
[`ENGINEERING_KNOWLEDGE_GOVERNANCE.md`](ENGINEERING_KNOWLEDGE_GOVERNANCE.md).

---

## P.R1–P.R8 — Operational Principles

Ces 8 principes opérationnels s'appliquent à TOUT run VBB (toutes routes, tous workers). Chaque SOUL.md y fait référence.

| ID | Principe | Définition courte |
|---|---|---|
| P.R1 | Fail Explicitly | Échec visible, pas de catch silencieux |
| P.R2 | One Verification Loop | Un seul point de vérification par assertion |
| P.R3 | Gate Before Action | Validation préalable à toute mutation |
| P.R4 | Invariant Protection | État partagé protégé contre mutation accidentelle |
| P.R5 | Regression Prevention First | Régression = priorité #1 sur nouveau test |
| P.R6 | Error Handling by Layer | Erreur traitée au bon niveau (route/agent/contrôleur) |
| P.R7 | Escalate on Risk Class Change | Si la classe de risque augmente, STOP et reclassifie |
| P.R8 | Independent Review Preferred | Préférer un reviewer indépendant à une self-review |

> Définitions détaillées : voir `### P.R1 — Fail Explicitly` etc. sous [Pillar 5 — Robustness](#pillar-5--robustness).

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

### SKILL.md description length

The frontmatter `description:` of any `SKILL.md` is the routing surface used by Pi / Codex / OpenCode to decide which skill to invoke. It is hand-maintained (validated for **precision**, not length) — no vibebackbone mechanism auto-truncates it.

**Target (indicative, non-blocking):**

- `description:` content should target **≤ 500 chars / ≤ 10 lines**.

**If exceeded:**

- The `tools/vbb-contract-lint.py` emits a **non-blocking** warning (no CI gate, no merge block). Rationale: a precise description may legitimately exceed the target to cover routing keywords, edge cases, or to disambiguate from sibling skills. Length is a proxy, not a quality guarantee.

**Hard promotion (future, after ≥ 1 observation cycle):**

- A future run may promote warning → error if `description:` content exceeds **800 chars / 15 lines**. This is intentionally left out of this run's canon: the policy must be observed before being enforced.

**Reference:** [`docs/audits/audit-E-skill-descriptions-20260712-1400.md`](audits/audit-E-skill-descriptions-20260712-1400.md) · **Tracking:** `AUDIT-E-006` in `docs/AUDIT_STATUS.md`.

### Documentation scope

- Every skill must have a machine-readable `CONTRACT.yaml`.
- `CONTRACT.yaml.contract_schema_version` is the contract schema version; the
  legacy `version` field is retained as a compatibility alias and must match it.
  Functional skill versioning remains in `SKILL.md` frontmatter.
- Every skill must have a human-readable `SKILL.md` in English.
- Every governance file must declare its role in its frontmatter or header.
- `docs/ARCHITECTURE.md` is the canonical structured source — never edit `docs/RELATIONS.md` directly.

### Language

- All skills and prompts → **English only**.
- Governance documents → may remain in the existing repo language.
- Agent-actionable artifacts → **English mandatory**.
- Machine-facing contracts → **English mandatory**, machine-readable only.

### Supported Python static toolchain

Python 3.11 tooling uses one repository configuration in `pyproject.toml`:

- Ruff 0.13.1 checks `tools/` and `tests/` with `E4`, `E7`, `E9`, and `F` and
  provides the canonical formatter;
- mypy 2.1.0 checks `tools/`; missing typing metadata from external packages is
  ignored, but repository type errors are not;
- Pyright is not part of the supported contract. Reconsider it only when a
  distinct editor, consumer, or analysis requirement is evidenced.

Canonical measurement commands are `ruff check tools tests`,
`ruff format --check tools tests`, and `mypy tools`. Versions are pinned in
`requirements-dev.txt`. These checks remain non-blocking while the documented
baseline is non-zero. They may enter local and remote CI only together, after
all three pass on a clean checkout; no global ignore or source exclusion may be
introduced solely to obtain zero.

**Decision:** [ADR 0035](adr/0035-supported-python-static-toolchain.md).

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

Before any implementation is declared complete, run the 5 mandatory
verifications (P.R2). The canonical shell block and the FAIL behavior
live in [`docs/REFERENCE/pre-merge-gate.md`](REFERENCE/pre-merge-gate.md)
(can unique) — they are not duplicated here.

If any command fails → **do not mark as implemented**. Document the
failure, fix in scope, then re-run the loop. The `--strict` flag on
`vbb-loop-closure-check.py` returns exit code 2 (`GATE_BLOCKED`) on FAIL.

## Pillar 4 — Traceability / Traçabilité (Embedded Pillar)

Traceability is a canonical quality pillar, but it is implemented through
Vibebackbone's existing governance artifacts rather than through a separate
standalone ruleset. It is covered by:

- ADRs (`docs/adr/`) — timestamped architecture decisions with rationale
- Run artifacts (`docs/runs/`) — phase files with frontmatter; use
  `python tools/vbb-status-dashboard.py --full` for current counts
- Audit reports (`docs/audits/`) — timestamped reports by theme; use
  `find docs/audits -maxdepth 1 -name '*.md'` for current inventory
- ARCHITECTURE.md — structured source of truth for architecture blocks
- Risk register (`docs/AUDIT_STATUS.md`) — P0/P1/P2/P3 tracked with status
- Context handoff (`docs/SESSION.md`) — session resume, next action
- TEMPORAL_PROVENANCE.md — provenance of evidence dates

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

**The single verification loop is canonicalized at
[`docs/REFERENCE/pre-merge-gate.md`](REFERENCE/pre-merge-gate.md).**

Before any implementation may be declared complete, run the 5 mandatory
verifications (P.R2). The canonical shell block and the FAIL behavior
live in the reference above — they are not duplicated here.

If any command fails → **do not mark as implemented**. Document the
failure, fix in scope, then re-run the loop. The `--strict` flag on
`vbb-loop-closure-check.py` returns exit code 2 (`GATE_BLOCKED`) on FAIL.

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
