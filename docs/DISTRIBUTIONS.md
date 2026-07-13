# DISTRIBUTIONS — VBB Core vs Operational Distributions

**Status**: Canonical · **Scope**: structural, not operational · **Audience**: humans and third-party agents reading this repo · **Date**: 2026-06-13

---

## 1. Purpose

This document clarifies the structural separation between **VBB Core** (the
generic, agent-agnostic method that lives in this repository) and
**Distributions** (operational declinations of VBB Core for a specific agent
runtime). Without it, a reader of the repo may confuse the canonical method
with one particular implementation (e.g. Hermes/Cody) and miss where to make
which kind of change. The rules below apply to **all** current and future
distributions.

## 2. VBB Core

VBB Core is the **generic, canonical, agent-agnostic method** for orchestrating
LLM agents predictably. It lives **in this repository** and is meant to be
consumable by any agent runtime.

VBB Core includes:
- `docs/` — canonical routing, governance, conventions, architecture
  (`CONTEXT.md`, `PILOTAGE.md`, `CONVENTIONS.md`, `ARCHITECTURE.md`,
  `AGENTIC_RUN_PROTOCOL.md`, plus `templates/` for one-per-phase +
  ADR/POC/Gate templates)
- `skills/` — 64 injectable skills (frontmatter + input/output contract)
- `prompts/` — 33 prompts (7 canonical + 25 specialised + 1 router)
- `providers/` — reserved templates (`example-consumer-repo/` only)
- `distributions/<name>/` — provider-specific adapters (claude, codex, pi, opencode, hermes)
- `tools/` — CLI tooling (`vbb-architecture.py`, `vbb-contract-lint.py`,
  `vbb-gate-check.py`, `vbb-phase-router.py`, `vbb-loop-closure-check.py`, etc.)
- `AGENTS.md` — agent-facing critical rules
- `GUIDE.md` — long-form human guide
- `CONVENTIONS.md` — quality pillars (P1–P5) and rules (P.R1–P.R8)
- `PILOTAGE.md` — operational triage matrix
- `SYSTEM.md` — runtime behaviour (Pi-specific hook reference)

**Anything that lives in VBB Core is reusable across all distributions.**

## 3. Distributions

A **Distribution** (or **Adapter**) is an **operational declination of VBB
Core** for a specific agent runtime. A distribution consumes VBB Core
(methods, skills, tools, templates) and adds the glue required to run it
against a particular agent process, profile system, or platform. A
distribution:
- **Imports / extends VBB Core** — it does not fork it.
- **Is isolated as a folder (`distributions/`)** on purpose: it preserves the
  agent-agnostic property of Core and avoids coupling Core to a specific
  runtime. Distributions live in this repo under `distributions/` (e.g.
  `distributions/hermes/`, `distributions/pi/`, `distributions/claude/`) but
  remain logically separated from the VBB Core tree at the root.
- **Owns only what's specific** — provider paths, profile manifests,
  orchestration scripts, secrets, runtime configs, integration points.
- **Inherits canon** — any canon change in Core propagates to the distribution
  on the next sync; the distribution's job is to expose it to its runtime.

The relationship is **Core → Distribution**, never the reverse. Core does not
import or reference any distribution in its canonical content.

## 4. Hermes/Cody Distribution

The **currently active distribution** is **Hermes/Cody**. It is the
operational declination of VBB Core for the Hermes agent runtime, with Cody as
the orchestrator.

Profiles (all live **outside** this repo, under `~/.hermes/profiles/`):

| Profile                       | Role                                         |
|-------------------------------|----------------------------------------------|
| `vbb-cody-orchestrator/`      | Orchestrator (Cody) — boot loop, delegation  |
| `vbb-fast-worker/`            | Fast worker — FAST-ZERO / FAST-MINIMAL route |
| `vbb-struct-worker/`          | Structured worker — STRUCTURED route         |
| `vbb-audit-worker/`           | Audit worker — AUDIT route (READ-ONLY)       |
| `vbb-close-worker/`           | Closeout worker — CLOSEOUT route             |

Each profile owns a `SOUL.md` (its persona + boot loop), a `MEMORY.md`
(per-profile state), a `config.yaml`, and a `skills/` directory.

Specific to the Hermes/Cody distribution (not in the repo):
- Hermes runtime, hermes CLI, hermes profiles mechanism
- The 5 `SOUL.md` files of the profiles above
- The orchestrator boot loop (Cody's 11-step loop and gate enforcement)
- The project registry: `~/.hermes/vbb-projects.yaml`
- The provider-specific config (`auth.json`, `config.yaml`, secrets, cron, hooks)
- The security proxy layer (binary, credentials, network config) — see §6.3

The Hermes/Cody distribution **imports** VBB Core through symlinks and
references: skills are loaded by profiles; tools are invoked as
`python ~/02_Dev/vibebackbone/tools/vbb-*.py`.

## 5. Alignment rules (propagation)

Two rules govern how changes flow between Core and any distribution.

### Rule A — Core → Distribution (impact check)

> Before any structural change to VBB Core (`AGENTS.md`, `GUIDE.md`,
> `CONVENTIONS.md`, `PILOTAGE.md`, templates, skills, tools, providers),
> check the impact on all active distributions
> (currently Hermes/Cody in `~/.hermes/profiles/vbb-*/`).

Distribution breakage caused by a silent Core change is the most expensive
class of bug in this project. Check = list of active distributions, then
walk through "will this change affect them?".

### Rule B — Distribution → Core (promote-or-keep)

> Before any change to a distribution (e.g.
> `~/.hermes/profiles/vbb-cody-orchestrator/`), ask: **"is this specific to
> this distribution, or should it be promoted to Core?"**

If the change encodes a generic principle (routing rule, gate, contract,
quality rule, template), it belongs in Core. If it is glue (profile path,
secret, runtime flag, persona), it stays in the distribution.

### Documentation requirement

Every decision to **promote to Core** or **keep in distribution** must be
recorded in the [Decisions log](#7-decisions-log) below. The log is the
audit trail for "why is X where it is".

## 6. Worked examples

Three examples to anchor the rule.

### 6.1. Example A — ADR/POC Integration Gate → **VBB Core**

The ADR/POC/Integration Gate is a generic VBB rule: before any non-trivial
work, an agent must (a) write an ADR, (b) build a POC, (c) clear the
integration gate. Applies to **any** agent runtime, not just Hermes.
Where it lives in VBB Core:
- `tools/vbb-gate-check.py` (gate enforcement, stdlib, no LLM)
- `docs/templates/ADR.md.template`, `POC.md.template`, `INTEGRATION_GATE.md.template`
- `GUIDE.md` §10bis — narrative reference

The Hermes/Cody distribution **consumes** these: each worker SOUL.md calls
`vbb-gate-check.py`, Cody references §10bis in its boot loop. The rule
stays in Core because any future distribution would need it too.

### 6.2. Example B — Hermes `SOUL.md` profiles → **Distribution**

The five `~/.hermes/profiles/vbb-*-worker/SOUL.md` files are **runtime
personas** — they describe how a Hermes profile behaves, which CLI it uses,
where its memory lives, and how it talks to the orchestrator. This is
**glue**, not method. It does not belong in Core:
- Specific to the Hermes profile mechanism (no equivalent in Codex or Pi).
- Hardcodes paths like `/Users/bot/.hermes/bin/...` — meaningless elsewhere.
- Encodes the Cody ↔ worker delegation protocol (a Hermes/Cody choice).

If a generic rule is discovered inside a SOUL.md (e.g. "the audit worker
must be READ-ONLY"), it should be **promoted** to Core; the SOUL.md
reference stays as the distribution's pointer to that Core rule.

### 6.3. Example C — Security Proxy → **Distribution** (mention only)

The security proxy is a runtime hardening layer that lives inside the
Hermes distribution. It is **not** part of VBB Core: it is specific to the
Hermes runtime, its config is secret-laden and environment-specific, and it
is governed by its own ADR cluster (proxy ADRs) which are operational to
the distribution, not canon to the method. Out of scope for VBB Core
changes.

## 7. Decisions log

This log records every explicit decision of the form **"X is Core"** or
**"Y stays in distribution Z"**. Entries are dated and reference the change
that triggered the decision.

<!-- Add entries below as decisions are made -->

### Template

```
### YYYY-MM-DD — <Title>
**Decision**: <promote to Core | keep in distribution Z>
**Trigger**: <PR / commit / audit finding / incident>
**Reason**: <why this placement, in 1–3 lines>
**Impact**: <what changes in Core | what stays in the distribution>
**Author**: <agent or human>
```

### 2026-06-13 — Hermes/Cody packaging strategy (F-015)
|**Decision**: Documentation + verify script first, then install script. Never overwrite existing profiles without backup.
|**Trigger**: Audit 20260602_1645 + audit post-766bbf3, Q8 verdict FIX BEFORE INSTALL.
|**Reason**: F-015 was newly identified as a P0 packaging blocker. The distribution must be installable on a new machine without ambiguity about what gets created, where, and how. Splitting packaging into (1) docs, (2) verify script, (3) install script allows each step to be validated independently and reduces the risk of corrupting an existing `~/.hermes/profiles/vbb-*/` setup.
|**Impact**:
  - VBB Core (this repo) gains: `docs/hermes/INSTALL.md` (future), `scripts/hermes/verify.sh` (future), `scripts/hermes/install.sh` (future).
  - Distribution: profiles stay under `~/.hermes/profiles/vbb-*/`. No overwrite without backup.
  - Next chantier: create `docs/hermes/INSTALL.md` (this run) and `scripts/hermes/verify.sh` (this run). Defer `scripts/hermes/install.sh` to a follow-up chantier (it is destructive, requires explicit confirmation).
|**Author**: vbb-struct-worker (delegated by Cody, audit-driven)

### 2026-06-13 — Hermes/Cody install layer step 1+2 (F-015)
|**Decision**: Provide `docs/hermes/INSTALL.md` + `scripts/hermes/verify.sh` only. `install.sh` remains DEFERRED.
|**Trigger**: F-015 packaging strategy. Previous run (5885d87) decided the strategy; this run implements the first two steps (documentation + verification).
|**Reason**: Verify-only is non-destructive. Operator can confirm environment readiness before any destructive install. `install.sh` is reserved for a follow-up run with explicit user confirmation (per F-015 step 3).
|**Impact**:
  - VBB Core (this repo) gains: `docs/hermes/INSTALL.md` + `scripts/hermes/verify.sh`.
  - Distribution: zero changes under `~/.hermes/profiles/vbb-*/`. `verify.sh` reads them but never writes.
  - Operator workflow: clone repo → set VBB_HOME/HERMES_HOME/CODY_CHECK → run `bash scripts/hermes/verify.sh` → expect PASS.
  - `verify.sh` covers 28 checks across VBB Core tools, Hermes profile presence, SOUL.md portability (F-004), and cody-check resolvability. Exits 0 on full PASS, 1 on any FAIL (with per-check hints).
|**Author**: vbb-struct-worker (delegated by Cody, F-015 implementation step 1+2)

### 2026-06-13 — Hermes/Cody documentation migration (ADR 0013 Phase 2)
|**Decision**: Migrate Hermes-only documentation to `distributions/hermes/`. Do NOT rewrite historical decision-log entries; append a forward-pointing note instead.
|**Trigger**: ADR 0013 Accepted (LIGHT REORG, fd46388). F-015 decision log entries above (2026-06-13) recorded pre-migration paths (`docs/hermes/INSTALL.md`, `scripts/hermes/verify.sh`). These paths are now historical; the live source of truth is under `distributions/hermes/`.
|**Reason**: ADR 0013 §5 mandates LIGHT REORG — Core canon stays in `docs/`, distributions own their docs/scripts/runtime. Phase 2 migrates documentation only (scripts/proxy runtime stay for Phase 3). Historical entries above are preserved verbatim (immutability convention) and supersede the obsolete path references for new code via this addendum.
|**Impact**:
  - **New canonical paths** (source of truth from this run onward):
    - `distributions/hermes/install/INSTALL.md` (← was `docs/hermes/INSTALL.md`, tracked `git mv`)
    - `distributions/hermes/docs/POC_USAGE.md` (← was `docs/proxy/POC_USAGE.md`, untracked `mv`)
    - `distributions/hermes/docs/POC_CLOSEOUT.md` (← was `docs/proxy/POC_CLOSEOUT.md`, untracked `mv`)
    - `distributions/hermes/proxy/adr/0006-0012*.md` (← was `docs/adr/0006-0012*.md`, 7 untracked ADRs)
  - **Untouched (Core canon, not distribution-owned)**:
    - `docs/adr/0001-0004*.md`, `docs/adr/0013*.md`, `docs/adr/README.md` — Core ADRs, stay in `docs/adr/`
    - `docs/audits/20260602_*.md` (3 files) — historical audits, immutable, keep old paths
    - `docs/archive/audits/` — historical, immutable
  - **Cross-references in Core canon** (`AGENTS.md`, `PILOTAGE.md`, `RUNBOOK.md`, `DEPLOYMENT.md`, `LONG_RUN_RULE.md`, `README.md`, `GUIDE.md`): 0 obsolete references found, no patches required.
  - **Cross-references in Core canon** (`DISTRIBUTIONS.md`): 4 occurrences of `docs/hermes/INSTALL.md` found in this decision log (historical F-015 entries l.187, 189, 193, 197). Preserved verbatim per immutability convention. This entry supersedes them for all future references.
  - **Distribution README updated**: `distributions/hermes/README.md` (sentinel) was already correct from Phase 1 (planned paths).
  - **Phase 3 (out of scope this run)**: `scripts/hermes/verify.sh` → `distributions/hermes/verify/`, `tools/proxy/` → `distributions/hermes/proxy/`, `tools/vbb-bypass-lint*` → `distributions/hermes/bypass-lint/`, pre-commit whitelist extended, `test_framework_gate_hook.sh` path ported to `$REPO_ROOT`.
|**Author**: vbb-struct-worker (delegated by Cody, ADR 0013 Phase 2 implementation)

### 2026-06-13 — Hermes/Cody scripts/outils/proxy migration (ADR 0013 Phase 3)
|**Decision**: Migrate runtime scripts, the proxy cluster, and the anti-bypass linter under `distributions/hermes/`. ADR 0001-0005 (Core canon) and `tools/vbb-*.py` (Core tools) remain untouched.
|**Trigger**: ADR 0013 Accepted (LIGHT REORG, fd46388). Phase 1 (sentinel) + Phase 2 (docs) already landed. Phase 3 prep R1 (commit a8af630) extended the pre-commit-framework-gate hook whitelist to `distributions/*`, unblocking the move.
|**Reason**: Phase 2 stopped at docs because the runtime cluster (17 proxy files + bypass-lint + verify.sh) had not yet been migrated. ADR 0013 §5 mandates LIGHT REORG — runtime artifacts specific to Hermes (proxy code, anti-bypass linter, verify script) belong in the distribution, not in VBB Core's `tools/` and `scripts/` trees. The verify script's `REPO_ROOT` auto-detection was adjusted from `../..` to `../../..` (3 levels up) to compensate for the new path depth; VBB_HOME default (`$HOME/02_Dev/vibebackbone`) is preserved.
|**Impact**:
  - **New canonical paths** (source of truth from this run onward):
    - `distributions/hermes/proxy/` (← was `tools/proxy/`, 17 source files + `fixtures/` + `tests/`, untracked `mv`; cluster was untracked)
    - `distributions/hermes/bypass-lint/vbb-bypass-lint.py` (← was `tools/vbb-bypass-lint.py`, untracked `mv`)
    - `distributions/hermes/bypass-lint/` (← was `tools/vbb-bypass-lint/`, untracked `mv`; contains `__init__.py`, `README.md`, `tests/`)
    - `distributions/hermes/verify/verify.sh` (← was `scripts/hermes/verify.sh`, tracked `git mv`)
  - **Untouched (Core canon, not distribution-owned)**:
    - `docs/adr/0001-0005*.md` — Core ADRs, stay in `docs/adr/`
    - `tools/vbb-*.py` (architecture, contract-lint, gate-check, phase-router, loop-closure-check, etc.) — Core tools
    - `docs/audits/20260602_*.md` (3 files) — historical audits, immutable
    - `distributions/hermes/proxy/adr/0006-0012*.md` — already in place since Phase 2
  - **Documentation patched**:
    - `distributions/hermes/README.md` — sentinel updated; migration items marked DONE (verify, proxy, bypass-lint); profiles-template still planned.
    - `distributions/hermes/install/INSTALL.md` — 4 references to `scripts/hermes/verify.sh` patched to `distributions/hermes/verify/verify.sh`; §4 path-note (`../../`) updated to `../../..`; §11 already correct from Phase 2.
    - `docs/DISTRIBUTIONS.md` — this entry (Phase 3 historical record). §4 and §6.3 already correctly describe the proxy at the distribution level (no path references to patch).
  - **Tests patched**:
    - `distributions/hermes/bypass-lint/tests/conftest.py` — `TOOLS_DIR = Path(__file__).resolve().parents[2]` adjusted to `parents[1]` (now `distributions/hermes/bypass-lint/`) so `LINTER_PATH` resolves to the new `vbb-bypass-lint.py` location.
    - `distributions/hermes/bypass-lint/tests/test_cli.py` — same `parents[2]` → `parents[1]` adjustment.
    - `distributions/hermes/bypass-lint/tests/test_allowlist.py` — `parents[3]` → `parents[2]` (was resolving to `~/02_Dev/vibebackbone/` from old `tools/vbb-bypass-lint/tests/`); regression test for `tools/proxy/` retained as documentation (guarded by `if proxy.exists()`).
  - **Linter guidance strings**: `distributions/hermes/bypass-lint/vbb-bypass-lint.py` contains ~25 guidance messages referencing `tools/proxy/client.py` (e.g. "Use tools/proxy/client.py with action 'nas_exec' instead."). These are guidance strings, not resolved paths; they remain pointing at the old path so that historical forensics in audit logs still match. Future work (Phase 4+) may update them to `distributions/hermes/proxy/client.py`.
  - **Phase 3 verification (28/28 PASS)**: `bash distributions/hermes/verify/verify.sh` exits 0 with all 28 checks PASS (VBB Core tools, Hermes profiles, SOUL.md portability F-004, cody-check resolvability).
  - **Pre-commit hook**: a8af630 extended the pre-commit-framework-gate whitelist to `distributions/*` (R1 prep), so the framework-gate hook will not block commits that touch only `distributions/hermes/`.
  - **Historical decision-log entries above (F-015 2026-06-13, Phase 2 2026-06-13)**: preserved verbatim per immutability convention. They continue to record the pre-Phase-3 paths they referenced. This entry supersedes them for all new code/docs.
  - **Out of scope this run**: Phase 4 (Pi/Claude migration), Phase 5 (final CI validation), `setup.sh` modifications (none required), Hermes profile modifications (none required), `install.sh` creation (DEFERRED per F-015).
|**Author**: vbb-struct-worker (delegated by Cody, ADR 0013 Phase 3 implementation)

### 2026-06-13 — Pi and Claude Code root → distributions migration (ADR 0013 Phase 4)
|**Decision**: Pi and Claude Code migrated from root to `distributions/{pi,claude}/` with symlinks for runtime compatibility. `.claude/` untouched (Claude Code runtime generates it).
|**Trigger**: Audit 2026-06-13 Phase 4 + ADR 0013 Accepted (LIGHT REORG, fd46388). Phase 1 (sentinels, cb1984c) + Phase 2 (docs, d7f9130) + Phase 3 (runtime, d5add57) already landed; Phase 4 was the last remaining Core-vs-Distribution move for Pi and Claude Code.
|**Reason**: Symlinks preserve runtime compatibility (Pi `mode projet` reads `SYSTEM.md` at root, Claude Code `@import` reads `CLAUDE.md` at root, `setup.sh` deploys `~/.pi/agent/SYSTEM.md` from `$REPO_ROOT/SYSTEM.md`) while making the Core vs Distribution split readable for humans. Migrating the file without a symlink would have broken Pi's discovery heuristic and required editing `setup.sh` (out of scope per Phase 3 closeout).
|**Impact**:
  - **New canonical paths** (source of truth from this run onward):
    - `distributions/pi/SYSTEM.md` (← was `SYSTEM.md` at root, tracked `git mv`)
    - `distributions/pi/overrides.template.json` (← was `.pi/subagent-overrides.json`, untracked `mv` — file was gitignored under `.pi/`)
    - `distributions/claude/CLAUDE.md` (← was `CLAUDE.md` at root, tracked `git mv`)
  - **Symlinks created at root** (runtime compat):
    - `SYSTEM.md` → `distributions/pi/SYSTEM.md` (relative)
    - `CLAUDE.md` → `distributions/claude/CLAUDE.md` (relative)
  - **Files patched (1 Core tool, 1 user doc)**:
    - `tools/vbb-llm-healthcheck.py` L21 — `OVERRIDES_PATH` updated from `.pi/subagent-overrides.json` to `distributions/pi/overrides.template.json` (the only Core-tool reference to the old path; verified via `grep -rn subagent-overrides`).
    - `docs/LLM_PROVIDERS.md` L62 + L68 — user-facing operational doc updated to reference the new path (additive note: "le symlink `.pi/subagent-overrides.json` historique n'est plus utilisé" to preserve the historical context).
  - **Distributions READMEs updated/created**:
    - `distributions/pi/README.md` — status flipped from `anticipated / placeholder` to `active`; lists migrated items + unchanged items (e.g. `setup.sh` needs no patch because of symlinks).
    - `distributions/claude/README.md` (new) — ≤ 30 lines, Role/What-belongs/What-does-NOT-belong/Status/See-also sections, status: active.
  - **Untouched (per constraints)**:
    - `.claude/settings.local.json` — KEEP ROOT (Claude Code runtime generates it, gitignored, per-machine).
    - `.claude/` directory at root — runtime-owned.
    - `setup.sh` — 0 lines modified (verified via `git diff setup.sh`); symlinks at root transparently preserve its `$REPO_ROOT/SYSTEM.md` lookup.
    - `.github/workflows/` — CI, untouched.
    - `tools/vbb-*.py` (other than `vbb-llm-healthcheck.py`) — Core canon, untouched.
    - `docs/adr/0001-0005*.md` — Core ADRs, untouched.
    - `docs/adr/0006-0012*.md` — proxy ADRs, already in `distributions/hermes/proxy/adr/` since Phase 2, untouched.
    - `docs/adr/0013-repo-organization-core-vs-distributions.md` — the ADR itself, untouched (its §5 / §6 already describe the planned Phase 4 paths; the historical "current `SYSTEM.md`" mentions on L23 and L147 of ADR 0013 are now historical and remain in place per immutability convention).
    - `install.sh` — not created (DEFERRED per F-015).
    - Hermes profiles (`~/.hermes/profiles/vbb-*/`) — 0 modifications.
    - Proxy code — already migrated in Phase 3, untouched.
    - `docs/audits/20260602_*.md` (3 files) — historical audits, immutable, left untracked.
  - **Verification** (post-migration):
    - `readlink SYSTEM.md` → `distributions/pi/SYSTEM.md` ✓
    - `readlink CLAUDE.md` → `distributions/claude/CLAUDE.md` ✓
    - `test -f distributions/pi/SYSTEM.md` → exists ✓
    - `test -f distributions/pi/overrides.template.json` → exists ✓
    - `test -f distributions/claude/CLAUDE.md` → exists ✓
    - `python tools/vbb-architecture.py lint` → 0 error ✓
    - `python tools/vbb-contract-lint.py` → 0 error ✓
    - `bash distributions/hermes/verify/verify.sh` → 28/28 PASS ✓
    - `python3 -m pytest tests/ -q` → 95/95 vert (2 skipped, baseline) ✓
    - `git diff setup.sh` → vide (0 modification) ✓
  - **Out of scope this run**: Phase 5 (final CI validation), `install.sh` creation, Hermes profile migration, proxy migration (already done in Phase 3), documentation harmonisation of pre-Phase-4 entries above (immutability convention).
|**Author**: vbb-struct-worker (delegated by Cody, ADR 0013 Phase 4 implementation)

### 2026-06-13 — ADR 0013 fully implemented (Phase 5 validation finale)

**Decision**: ADR 0013 LIGHT REORG marked fully implemented. Phases 1-4 closed, Phase 5 validation verte. ADR status remains `Accepted` per VBB convention (no `Implemented` status in historical ADRs); implementation is traced in this entry.

**Trigger**: Phase 5 validation finale (commit pending). Phases 1-4 commits: cd4899a (sentinels), d7f9130 (docs), a8af630 (R1 hook), d5add57 (scripts/outils/proxy), beecb28 (Pi + Claude).

**Reason**: All four migrations complete. No new file moves planned. Validate that the Core vs Distribution split is now readable in 30 seconds for any new operator.

**Impact**:
  - VBB Core (this repo) gains: confirmed canonical structure with sentinels + 3 active distributions.
  - Distributions: `hermes/` (active, ~40 files: install/verify/docs/proxy/bypass-lint), `pi/` (active, 3 files: SYSTEM.md + overrides.template.json + README), `claude/` (active, 2 files: CLAUDE.md + README), `examples/` (placeholder).
  - Active symlinks: `SYSTEM.md` → `distributions/pi/SYSTEM.md`, `CLAUDE.md` → `distributions/claude/CLAUDE.md`.
  - KEEP ROOT: `.claude/settings.local.json` (Claude Code runtime generates it).
  - 7 ADRs proxy (0006-0012) live under `distributions/hermes/proxy/adr/`.
  - 4 Core ADRs (0001-0004) live under `docs/adr/`.

**Canonical paths (2026-06-13 post Phase 5)**:
  | Concept | Path |
  |---|---|
  | VBB Core canon | repo root + `docs/` + `skills/` + `prompts/` + `tools/vbb-*.py` + `setup.sh` + `setup-lib.sh` + `core/setup.sh` + `distributions/` |
  | VBB Core ADR | `docs/adr/0001-0004` |
  | VBB Core decision log | `docs/DISTRIBUTIONS.md` §7 |
  | Distribution Hermes | `distributions/hermes/{install,verify,docs,proxy,bypass-lint}` |
  | Distribution Hermes ADR | `distributions/hermes/proxy/adr/0006-0012` |
  | Distribution Pi | `distributions/pi/{SYSTEM.md,overrides.template.json,README.md}` |
  | Distribution Claude | `distributions/claude/{CLAUDE.md,README.md}` |
  | Distribution examples | `distributions/examples/README.md` |
  | Runtime symlinks | `SYSTEM.md`, `CLAUDE.md` (root, symlinks → distributions) |
  | Runtime-generated (KEEP ROOT) | `.claude/settings.local.json` |
  | Verify script (distribution) | `distributions/hermes/verify/verify.sh` |
  | Pre-commit hook | `scripts/hooks/pre-commit-framework-gate` (whitelist includes `distributions/*` since R1 prep) |

**Author**: Hermes (orchestration), vbb-audit-worker (validation READ-ONLY)

### 2026-07-13 — Contrat des verdicts POC maintenu dans VBB Core

**Decision**: Conserver dans Core la reconnaissance des verdicts POC et rendre
`PIVOT` bloquant. Aucune logique spécifique n'est ajoutée aux distributions.

**Trigger**: Audit systémique `2026-07-13_1551_poc-subagents-methodology-audit`
et correction `2026-07-13_1639_poc-gate-verdict-contract`.

**Reason**: Le contrat GO/NO-GO/PIVOT est une règle de gouvernance générique,
partagée par tous les runtimes. Le template canonique exige déjà `GO` pour
autoriser le code.

**Impact**: `tools/vbb-gate-check.py` reste la source exécutable Core. Les
distributions Hermes/Cody continuent de l'appeler sans changement de CLI, de
schéma JSON ni de code de sortie. `PIVOT` bloque désormais explicitement avec
la raison `POC_VERDICT_PIVOT`. Les profils runtime externes n'ont pas été
modifiés.

**Author**: Codex, validé par Brice (`go`, 2026-07-13)

### Example entry (illustrative)

```
### 2026-06-13 — ADR/POC Integration Gate is VBB Core
**Decision**: Promote to Core
**Trigger**: Audit 20260602_1645 + §10bis of GUIDE.md already in place
**Reason**: Generic VBB rule applying to any agent runtime, not just Hermes.
**Impact**: tools/vbb-gate-check.py, templates, GUIDE §10bis stay in Core.
            Distribution keeps calling them from worker SOUL.md.
**Author**: vbb-audit-worker (delegated by Cody)
```

## 8. References

- `README.md` — entry point; "VBB Core vs Distributions" anchors the
  high-level distinction.
- `AGENTS.md` — Critical Rule #11 enforces the Core ↔ Distribution rule.
- `GUIDE.md`, `docs/PILOTAGE.md`, `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`
  — all describe VBB Core.

For Hermes/Cody runtime status, see
`~/.hermes/profiles/vbb-cody-orchestrator/SOUL.md` (lives outside this repo).

---

*This file is canon. Changes are governed by AGENTS.md Critical Rule #11 and
must be recorded in §7 above.*
