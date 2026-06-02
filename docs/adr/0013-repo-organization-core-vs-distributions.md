# ADR 0013 — Repository Organization: VBB Core vs Distributions (LIGHT REORG)

**Status**: Proposed
**Date**: 2026-06-13
**Route**: STRUCTURED
**Décideurs**: Brice Sodini (validation future), Hermes (orchestration, `vbb-struct-worker`), Cody (delegation)

## Context

The separation between VBB Core and VBB Distributions is canonically defined in
`docs/DISTRIBUTIONS.md` (229 lines) and reinforced in `AGENTS.md` Critical Rule #11:

> "Core changes ripple to all distributions; Distribution changes must justify
> their placement (Core vs distribution)."

However, the separation is not materialized in the repository tree. A new
operator opening the repo must *guess* which folders are Core canon and which
belong to a specific distribution:

- `docs/hermes/` is Hermes-only but lives next to `docs/adr/`, `docs/ARCHITECTURE.md`, `docs/templates/`.
- `scripts/hermes/verify.sh` is Hermes-only but lives next to `scripts/hooks/`.
- `tools/proxy/` is Hermes/Cody-only but lives next to `tools/vbb-architecture.py`.
- `.pi/`, `.claude/` are distribution-only but live at the root, side by side with Core folders.
- `docs/adr/0006-0012` are proxy-distribution ADRs (UNTRACKED) but live in the
  Core `docs/adr/` directory.

The "30-second reading" test — can a newcomer tell what is Core and what is
distribution in 30 seconds? — is currently not passed. Drift risk: a future
contributor might modify `docs/hermes/INSTALL.md` thinking it is Core canon.

The repo must serve several distributions over time:

- **Hermes/Cody** (currently active, 5 SOUL.md profiles, 28/28 `verify.sh` PASS).
- **Pi** (anticipated, mentioned by root `SYSTEM.md` and by `setup.sh` symlink to `~/.pi/agent/SYSTEM.md`).
- **Codex / OpenCode / future** (anticipated, `setup.sh` already deploys to `~/.codex/AGENTS.md` and `~/.claude/CLAUDE.md`).

A formal architectural audit on 2026-06-13 (post-05d6b9e) concluded **GO WITH
LIGHT REORG**: the situation is workable but the tree should make the Core vs
Distribution split explicit without breaking 100+ existing references.

## Decision

We adopt a **LIGHT REORG** strategy, executed in 5 phases. **This ADR covers
Phase 1 only** — the rest is documented as future work, gated on Brice's
review.

**Phase 1 (this run, additive only — no moves, no renames):**

1. The current repository root remains VBB Core. No `core/` top-level
   directory is created; the 100+ `REPO_ROOT` references in `tools/vbb-*.py`,
   `setup.sh`, `AGENTS.md`, hooks and the 8 hardcoded paths in canonical docs
   stay valid.
2. A new top-level `distributions/` directory is created to host the
   operational declinations of VBB Core for specific agent runtimes.
3. A `core.README.md` sentinel is placed at the repository root to make the
   Core canon explicit in 30 seconds.
4. A `distributions/README.md` catalog sentinel describes the distribution
   mechanism generically.
5. Three distribution subfolder sentinels are created with README-only
   content: `distributions/hermes/`, `distributions/pi/`, `distributions/examples/`.

**Phases 2-5 (deferred, gated on ADR acceptance by Brice):**

- Phase 2: migrate Hermes-only documentation (`docs/hermes/INSTALL.md` → `distributions/hermes/install/INSTALL.md`, with symlinks for back-compat). Patch 8 hardcoded paths in canonical docs.
- Phase 3: migrate Hermes-only scripts and proxy code (`scripts/hermes/verify.sh` → `distributions/hermes/verify/`, `tools/proxy/` → `distributions/hermes/proxy/`, `tools/vbb-bypass-lint*` → `distributions/hermes/bypass-lint/`, `docs/adr/0006-0012` → `distributions/hermes/proxy/adr/`). Extend the pre-commit framework-gate whitelist to include `distributions/*`. Replace the hardcoded `~/02_Dev/vibebackbone/...` path in `test_framework_gate_hook.sh` with `$REPO_ROOT/...`.
- Phase 4: bootstrap Pi distribution (move root `SYSTEM.md` → `distributions/pi/SYSTEM.md`, `.pi/subagent-overrides.json` → `distributions/pi/overrides.template.json`).
- Phase 5: optional consolidation / cleanup of `distributions/examples/` if real example distributions emerge.

## Consequences

- (a) VBB Core canon remains at the root. No existing Core path is broken.
- (b) `distributions/{hermes,pi,examples}/` become the explicit future targets for Phases 2-3 migrations. The catalog in `distributions/README.md` is the entry point.
- (c) `skills/` and `prompts/` stay in Core. They are **not** duplicated between distributions. `setup.sh`'s existing symlink mechanism (`~/.agents/skills/vibebackbone`) is preserved.
- (d) `tools/proxy/` migrates in Phase 3 to `distributions/hermes/proxy/`. Until then it stays where it is.
- (e) After Phase 3, the gate-check will no longer flag proxy ADRs (0006-0012) as out-of-Core — because they will physically live in `distributions/hermes/proxy/adr/`. This is an **expected and desired false negative**: distribution ADRs are not Core canon, so they should not be checked against Core rules.
- (f) `scripts/hermes/verify.sh` will keep working after its path changes because it already uses portable environment variables (`$REPO_ROOT` style), not hardcoded absolute paths.
- (g) `setup.sh` is already distribution-aware (1484 lines, deploys to `~/.agents/skills/vibebackbone`, `~/.pi/agent/SYSTEM.md`, `~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`). No modification to `setup.sh` is required for Phase 1.

## Alternatives Rejected

**A1. KEEP — do nothing.** Rejected because the 30-second reading test is not
passed, and the audit's "new operator" drill fails. Long-term risk of Core vs
Distribution drift if a contributor modifies `docs/hermes/INSTALL.md` thinking
it is Core canon.

**A2. `core/` topological split (`core/skills/`, `core/tools/`, `core/docs/`, etc.).**
Rejected because it would break 100+ existing references: 12 `vbb-*.py` tools
using `REPO_ROOT` auto-detection, the `setup.sh` installer, `AGENTS.md` Rule
#11/#12 paths, 8 hardcoded paths in canonical docs, and 1 hardcoded path in
`test_framework_gate_hook.sh`. The audit's reading-30-seconds gain is null
relative to the sentinel approach.

**A3. Dispersed pairs (`docs/core/` + `docs/distributions/`, `tools/core/` + `tools/distributions/`, etc.).**
Rejected because multiplying Core/Distribution pairs in every sub-domain makes
the 30-second reading *more* confusing, not less. A single top-level
`distributions/` folder is more legible than N dispersed pairs.

## Risks

- (R1) Pre-commit framework-gate whitelist will need a `distributions/*` entry in Phase 3 to avoid blocking commits. **Mitigation:** patch in Phase 3, before any `distributions/*` content beyond sentinels is added.
- (R2) 8 hardcoded paths in canonical docs reference Hermes-only locations. **Mitigation:** patch in Phase 2, with `readlink -f` checks on symlinks for back-compat.
- (R3) `test_framework_gate_hook.sh` contains a hardcoded `~/02_Dev/vibebackbone/...` path. **Mitigation:** replace with `$REPO_ROOT/...` in Phase 3.
- (R4) Post-Phase 3, the gate-check will produce a "false negative" on proxy ADRs (no longer detected as out-of-Core). **Mitigation:** this is the *desired* behavior; document explicitly in `tools/vbb-gate-check.py --help`.
- (R5) Symlinks for back-compat may be forgotten or broken. **Mitigation:** add a `distributions/hermes/SYMLINKS.md` checklist in Phase 2 and verify with `readlink` in Phase 3.

## Hypotheses

- (H1) Brice will validate the LIGHT REORG strategy in a future run, transitioning this ADR from `Proposed` to `Accepted`.
- (H2) No migration (Phase 2-5) is attempted before the ADR is `Accepted`. Phase 1 is purely additive by design.
- (H3) `setup.sh` (1484 lines) is already distribution-aware; no modification is required for Phase 1.
- (H4) The 5 sentinels are sufficient to make the Core vs Distribution split readable in 30 seconds for a new operator, without moving a single existing file.

## References

- `docs/DISTRIBUTIONS.md` — the canonical definition of Core vs Distribution (229 lines).
- `AGENTS.md` — Critical Rule #11 (Core changes ripple to all distributions).
- ADR 0004 — short, simple ADR format adopted here.
- ADR 0006-0012 — proxy ADRs (UNTRACKED at the time of this ADR; will physically migrate in Phase 3).
- Architectural audit 2026-06-13 (post-05d6b9e) — verdict "GO WITH LIGHT REORG".

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS:
  status: PROPOSED
  date: 2026-06-13
  route: STRUCTURED
  decisions_count: 1
  alternatives_rejected: 3
  phase: 1_of_5
  author: vbb-struct-worker (delegated by Cody)
  next_action: Brice review -> Accepted -> Phase 1 sentinels (this run)
  files_created:
    - docs/adr/0013-repo-organization-core-vs-distributions.md
    - core.README.md
    - distributions/README.md
    - distributions/hermes/README.md
    - distributions/pi/README.md
    - distributions/examples/README.md
  files_modified: []
  files_moved: []
  files_renamed: []
  scope: additive only (no existing file moved, renamed, or modified)
  deferred_phases:
    - phase_2: docs/hermes/ -> distributions/hermes/install/ + 8 hardcoded paths patched
    - phase_3: scripts/hermes/verify.sh, tools/proxy/, tools/vbb-bypass-lint*/, docs/adr/0006-0012 -> distributions/hermes/; pre-commit whitelist extended; test_framework_gate_hook.sh path ported to $REPO_ROOT
    - phase_4: SYSTEM.md and .pi/subagent-overrides.json -> distributions/pi/
    - phase_5: distributions/examples/ consolidation if needed
  risks_open: 5 (R1-R5, see Risks section)
  hypotheses: 4 (H1-H4, see Hypotheses section)
  verdict: PROPOSED_PENDING_BRICE_REVIEW
```
