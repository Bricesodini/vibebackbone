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
- `providers/` — provider adapters (Claude Code, Codex, Pi, OpenCode)
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
- **Is isolated outside this repository** — distributions do not live in the
  VBB Core tree, on purpose: it preserves the agent-agnostic property of
  Core and avoids coupling Core to a specific runtime.
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
