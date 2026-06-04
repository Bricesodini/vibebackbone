# Hermes/Cody — Installation Guide

Status: VERIFY-ONLY. Install script (`distributions/hermes/install/install.sh`,
DEFERRED in F-015 step 3 — destructive) is **not yet authored**. All references
to `scripts/hermes/install.sh` below describe the F-015 future plan, not a
shipped artifact.
See `docs/DISTRIBUTIONS.md` (F-015, 2026-06-13) and §9 below.

> **Note (Phase 2F, 2026-06-14)**: a non-destructive `distributions/hermes/setup.sh`
> has been authored and is sourced by the root `setup.sh` (last install step,
> read-only check of the Hermes runtime coherence). It does **not** create or
> modify any file in `~/.hermes/`. For the full agent-mediated installation
> procedure (operator-led, with backups and rollback), see
> [`distributions/hermes/AGENT_INSTALL.md`](../AGENT_INSTALL.md). This `INSTALL.md`
> remains the canonical "verify-only" doc; `AGENT_INSTALL.md` is the canonical
> "agent-mediated install" doc.

## 1. Role of the Hermes/Cody distribution

The Hermes/Cody distribution is the currently active distribution of VBB Core
(see `AGENTS.md` Critical Rule #11 for the Core ↔ Distribution rule).

It is composed of:

- One orchestrator: **Cody** (`vbb-cody-orchestrator`) — plans, delegates,
  never executes code.
- Four workers: **FAST**, **STRUCT**, **AUDIT**, **CLOSE** (see §6).

All five profiles live under `~/.hermes/profiles/vbb-*/` (one folder per
profile, each containing a `SOUL.md`). The Hermes CLI itself is assumed to
be installed at `~/.hermes/bin/` (operator responsibility; outside scope).

## 2. Status: verify-only, install deferred

This run provides only:

- `distributions/hermes/install/INSTALL.md` — this document (F-015 step 1,
  originally authored at `docs/hermes/INSTALL.md` and migrated here in
  ADR 0013 Phase 2; the historical path is preserved in §11 for the record).
- `distributions/hermes/verify/verify.sh` — non-destructive verification (F-015 step 2).

`distributions/hermes/install/install.sh` (F-015 step 3, **destructive**)
is **DEFERRED** to a follow-up run requiring explicit user confirmation.
See §9. (Pre-Phase 3, the planned location for this script was
`scripts/hermes/install.sh`; that path is now superseded by
`distributions/hermes/install/` per ADR 0013.)

The split is intentional: each step is independently auditable, and a verify
step before any destructive install dramatically reduces the risk of
corrupting an existing `~/.hermes/profiles/vbb-*/` setup.

## 3. Prerequisites

| Requirement | Notes |
| --- | --- |
| `bash` (POSIX-compatible) | macOS `/bin/bash` 3.2+; Linux 4+/5+ typically. |
| `python` 3.10+ | Required only if you also run VBB Core tools. |
| VBB Core repo cloned | Default path: `~/02_Dev/vibebackbone`. |
| Hermes CLI installed | At `~/.hermes/bin/`; `cody-check` must be executable. |
| POSIX builtins | `grep`, `printf`, `command -v`, `readlink` — used by `verify.sh`. |

## 4. Environment variables

| Variable | Default | Meaning |
| --- | --- | --- |
| `CODY_CHECK` | `${HERMES_HOME:-$HOME/.hermes}/bin/cody-check` | Path to `cody-check`. |
| `HERMES_HOME` | `$HOME/.hermes` | Hermes installation root. |
| `VBB_HOME` | `$HOME/02_Dev/vibebackbone` | VBB Core repo (parent of `tools/`, `docs/`, `scripts/`). |

`verify.sh` auto-detects VBB Core from its own location
(`distributions/hermes/verify/verify.sh` → `../../..`), so `VBB_HOME` does not need to be
exported for in-tree runs. Set `VBB_HOME_OVERRIDE=1` to force auto-detection
even if `VBB_HOME` is set.

## 5. Expected paths

### VBB Core (`${VBB_HOME}`)

- `tools/vbb-architecture.py`
- `tools/vbb-contract-lint.py`
- `tools/vbb-gate-check.py`
- `tools/vbb-phase-router.py` (optional but recommended)

### Hermes profiles (`${HERMES_HOME}/profiles/`)

`vbb-cody-orchestrator/SOUL.md`, `vbb-fast-worker/SOUL.md`,
`vbb-struct-worker/SOUL.md`, `vbb-audit-worker/SOUL.md`,
`vbb-close-worker/SOUL.md`.

### Hermes runtime (`${HERMES_HOME}/bin/`)

- `cody-check` (executable, provided by Hermes runtime).

## 6. Expected profiles

| Profile name | Role |
| --- | --- |
| `vbb-cody-orchestrator` | Orchestrator (Cody): plan, delegate, never execute code. |
| `vbb-fast-worker` | FAST: low-risk, high-volume structural changes. |
| `vbb-struct-worker` | STRUCT: non-trivial code/docs work, main doer. |
| `vbb-audit-worker` | AUDIT: read-only audits, evidence-driven. |
| `vbb-close-worker` | CLOSE: closeout, merge, CI watch. |

Each `SOUL.md` must contain the portable form
`${CODY_CHECK:-${HERMES_HOME:-$HOME/.hermes}/bin/cody-check}` (F-004) and
must **not** contain any hardcoded `/Users/bot/.hermes/bin/cody-check`.

## 7. Verification command

From the VBB Core repo root:

```bash
bash distributions/hermes/verify/verify.sh
```

- Exit `0` → all checks PASS, environment is ready.
- Exit `1` → at least one check FAIL, see hints in the output.

The script is non-destructive: it only reads paths and grep-matches files;
it never writes, copies, or modifies anything.

## 8. What `verify.sh` checks

1. **VBB Core tools** — `VBB_HOME` is a directory; the main
   `tools/vbb-*.py` scripts are present; `vbb-gate-check.py --help` exits 0.
2. **Hermes profiles** — all five `SOUL.md` files exist.
3. **SOUL.md portability (F-004)** — every `SOUL.md` references
   `CODY_CHECK` and `HERMES_HOME`, and none contains a hardcoded
   `/Users/bot/.hermes/bin/cody-check`.
4. **cody-check resolvability** — `CODY_CHECK` path is set and the binary
   is executable.

## 9. Install script status

`distributions/hermes/install/install.sh` is **DEFERRED** (F-015 step 3).
It will be authored in a follow-up run with explicit operator
confirmation before it touches `~/.hermes/profiles/vbb-*/`. (Pre-Phase 3,
the planned path for this script was `scripts/hermes/install.sh`; that
location is now superseded by `distributions/hermes/install/` per ADR 0013.)

Reason (F-015, 2026-06-13): the install is destructive (creates/overwrites
files in the operator's Hermes profile tree), and splitting packaging into
(1) docs, (2) verify, (3) install lets each step be validated
independently. Installing before a clean verify pass risks corrupting an
existing setup.

### Non-destructive setup.sh (Phase 2F, 2026-06-14)

`distributions/hermes/setup.sh` is a **read-only** check that the root
`setup.sh` sources as its last step. It verifies the Hermes runtime
coherence (expected paths, profiles, proxy contract) **without** writing
to `~/.hermes/`. It is **not** an installer. To install Hermes profiles,
follow the agent-mediated procedure in
[`distributions/hermes/AGENT_INSTALL.md`](../AGENT_INSTALL.md).

### Manual install (interim, until `install.sh` lands)

```bash
# 1. Create the profile directory
mkdir -p "${HERMES_HOME}/profiles/vbb-struct-worker"

# 2. Drop a SOUL.md in it (paste from a sibling profile as a starting
#    template, or use the repo's profile sources if/when they exist).

# 3. Re-run verify.sh to confirm the new profile is detected.
bash distributions/hermes/verify/verify.sh
```

This is intentionally manual: every step is an explicit operator decision,
no implicit copies, no destructive overwrites.

## 10. References

- `docs/DISTRIBUTIONS.md` — Core ↔ Distribution rule, F-004 + F-015 log.
- `AGENTS.md` — Critical Rule #11 (Core changes ripple to distributions) and
  Rule #12 (the distribution owns its own profiles).
- `GUIDE.md` §10bis — ADR + POC + Integration Gate workflow (Core).
- `GUIDE.md` §10 — general distribution governance.

## 11. Location note (added by ADR 0013 Phase 2)

As of the 2026-06-13 Phase 2 migration of ADR 0013 (LIGHT REORG), the
canonical path of this document is:

- `distributions/hermes/install/INSTALL.md` (current, source of truth)

The §2 line referencing `docs/hermes/INSTALL.md` records the path at the
time of the F-015 step 1 delivery run and is preserved verbatim as part
of the historical record. All new cross-references must use the current
`distributions/hermes/install/INSTALL.md` path.
