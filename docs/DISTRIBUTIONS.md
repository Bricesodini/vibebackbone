# DISTRIBUTIONS — VBB Core vs Operational Distributions

**Status**: Canonical · **Scope**: structural, not operational · **Audience**: humans and third-party agents reading this repo · **Date**: 2026-06-13

---

## 1. Purpose

This document clarifies the structural separation between **VBB Core** (the
generic, agent-agnostic method that lives in this repository) and
**Distributions** (operational declinations of VBB Core for a specific agent
runtime). Without it, a reader of the repo may confuse the canonical method
with one particular provider implementation and miss where to make
which kind of change. The rules below apply to **all** current and future
distributions.

## 2. VBB Core

VBB Core is the **generic, canonical, agent-agnostic method** for orchestrating
LLM agents predictably. It lives **in this repository** and is meant to be
shared by the four officially supported coding-agent runtimes.

VBB Core includes:
- `docs/` — canonical routing, governance, conventions, architecture
  (`CONTEXT.md`, `PILOTAGE.md`, `CONVENTIONS.md`, `ARCHITECTURE.md`,
  `AGENTIC_RUN_PROTOCOL.md`, plus `templates/` for one-per-phase +
  ADR/POC/Gate templates)
- `skills/` — 64 injectable skills (frontmatter + input/output contract)
- `prompts/` — 33 prompts (7 canonical + 25 specialised + 1 router)
- `providers/` — reserved templates (`example-consumer-repo/` only)
- `tools/` — CLI tooling (`vbb-architecture.py`, `vbb-contract-lint.py`,
  `vbb-gate-check.py`, `vbb-phase-router.py`, `vbb-loop-closure-check.py`, etc.)
- `AGENTS.md` — agent-facing critical rules
- `GUIDE.md` — long-form human guide
- `CONVENTIONS.md` — quality pillars (P1–P5) and rules (P.R1–P.R8)
- `PILOTAGE.md` — operational triage matrix
- `SYSTEM.md` — runtime behaviour (Pi-specific hook reference)

The repository also contains `distributions/<name>/` folders. They are part of
the repository layout, but they are **not Core**: they are operational
declinations of Core for specific agent runtimes.

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
  runtime. Distributions live in this repo under `distributions/` (currently
  `pi/`, `opencode/`, `codex/`, `claude/`) but
  remain logically separated from the VBB Core tree at the root.
- **Owns only what's specific** — provider paths, profile manifests,
  orchestration scripts, secrets, runtime configs, integration points.
- **Inherits canon** — any canon change in Core propagates to the distribution
  on the next sync; the distribution's job is to expose it to its runtime.

The relationship is **Core → Distribution**, never the reverse. Core does not
import or reference any distribution in its canonical content.

## 4. Supported distributions

The supported surface is intentionally limited to four coding-agent runtimes:

| Distribution | Runtime state outside the repo | Adapter responsibility |
|---|---|---|
| `pi/` | `~/.pi/` | AGENTS/SYSTEM/prompt symlinks and Pi package |
| `opencode/` | `~/.config/opencode/` | instructions and generated commands |
| `codex/` | `~/.codex/` | compiled AGENTS.md governance block |
| `claude/` | `~/.claude/` | settings, CLAUDE.md imports and commands |

There is no privileged orchestrator distribution. Each supported agent consumes
the same Core gates, conventions, skills and phase artifacts through its adapter.
Hermes/Cody was retired by ADR 0025; external Hermes state is never modified by
this repository.

## 5. Alignment rules (propagation)

Two rules govern how changes flow between Core and any distribution.

### Rule A — Core → Distribution (impact check)

> Before any structural change to VBB Core (`AGENTS.md`, `GUIDE.md`,
> `CONVENTIONS.md`, `PILOTAGE.md`, templates, skills, tools, providers),
> check the impact on all active distributions
> (`pi`, `opencode`, `codex`, `claude`).

Distribution breakage caused by a silent Core change is the most expensive
class of bug in this project. Check = list of active distributions, then
walk through "will this change affect them?".

### Rule B — Distribution → Core (promote-or-keep)

> Before any change to a distribution, ask: **"is this specific to
> this distribution, or should it be promoted to Core?"**

If the change encodes a generic principle (routing rule, gate, contract,
quality rule, template), it belongs in Core. If it is glue (profile path,
secret, runtime flag, persona), it stays in the distribution.

### Documentation requirement

Every decision to **promote to Core** or **keep in distribution** must be
recorded in the [Decisions log](#8-decisions-log) below. The log is the
audit trail for "why is X where it is".

## 6. Worked examples

Three examples to anchor the rule.

### 6.1. Example A — ADR/POC Integration Gate → **VBB Core**

The ADR/POC/Integration Gate is a generic VBB rule: before any non-trivial
work, an agent must (a) write an ADR, (b) build a POC, (c) clear the
integration gate. Applies to every supported agent runtime.
Where it lives in VBB Core:
- `tools/vbb-gate-check.py` (gate enforcement, stdlib, no LLM)
- `docs/templates/ADR.md.template`, `POC.md.template`, `INTEGRATION_GATE.md.template`
- `GUIDE.md` §10bis — narrative reference

The four supported distributions consume these through generated or linked
governance files. The rule stays in Core so every adapter shares it.

### 6.2. Example B — provider-generated governance → **Distribution**

Generated files such as `~/.codex/AGENTS.md` or provider command adapters are
runtime glue. Their paths and serialization stay in the distribution, while
generic rules such as "an audit is read-only" stay in Core and are referenced
or compiled by every adapter.

### 6.3. Example C — retired Hermes proxy → **not promoted**

The retired security proxy was Hermes-specific glue. ADR 0025 removes it rather
than promoting it to Core because no runtime-neutral requirement or adoption
evidence justifies that complexity. Its history remains available in git.

## 7. Consumer runtime bundle refresh

The project initializer distinguishes two ownership classes (ADR-0034):

- governance documents are project-owned and generated once; compare and merge
  canon changes manually when the project chooses to adopt them;
- the hook runtime bundle is VBB-managed through `.vbb/managed-files.json` and
  can be refreshed only while its recorded assets remain unchanged.

Non-destructive refresh checklist:

1. Commit or stash all consumer work and inspect `.vbb/managed-files.json`.
2. From the current VBB Core checkout, preview the operation:
   `python3 tools/vbb-project-init.py --target-dir <consumer> --install-hook --overwrite-hook --dry-run`.
3. Run the same command without `--dry-run`. Existing generated Git hooks need
   `--overwrite-hook`; this never grants document or managed-asset overwrite.
4. If an asset conflict is reported, diff it against Core and preserve the
   consumer file. Use `--overwrite-managed` only after deciding that the local
   customization must be discarded or adopted as VBB-owned.
5. Ensure the VBB Python requirements declared in `.vbb/requirements.txt` are
   available, run the installed pre-commit hook, then commit the manifest and
   managed assets together.
6. Review governance documents separately; never use the runtime refresh as a
   document merge mechanism.

Rollback is a normal Git revert of the bundle/manifest commit. Do not delete or
rewrite project-owned governance files as part of that rollback.

## 8. Decisions log

This log records every explicit decision of the form **"X is Core"** or
**"Y stays in distribution Z"**. Entries are dated and reference the change
that triggered the decision.

<!-- Add entries below as decisions are made -->

### 2026-07-14 — Exact seven-section skill layout (ADR-0042)
**Decision**: keep the exact skill layout and its blocking lint in Core; no
distribution owns a provider-specific section alias.
**Trigger**: PATT-01 and explicit `Go` from Brice.
**Reason**: predictable skill boundaries are a shared catalog invariant, while
compact wrappers remain free to keep their section bodies concise.
**Impact**: Pi, OpenCode, Codex and Claude Code inherit twelve normalized skills
and the same drift guard. No adapter, provider path or runtime state changes.
**Author**: Codex (GO Brice)

### 2026-07-14 — Transverse artifacts and infrastructure files (ADR-0041)
**Decision**: keep transverse artifact and Docker infrastructure semantics in
Core; distributions inherit the same observable outputs.
**Trigger**: final PATT-03 batch and explicit `Go` from Brice.
**Reason**: audit, sync, coverage and generated infrastructure artifacts are
provider-neutral shared contracts.
**Impact**: Pi, OpenCode, Codex and Claude Code inherit five corrected contracts,
`infrastructure_file`, deterministic anti-slop reports and blocking transverse
null-drift lint. No adapter or provider runtime state changes.
**Author**: Codex (GO Brice)

### 2026-07-14 — Front-pass and release artifact semantics (ADR-0040)
**Decision**: keep front/release artifact semantics in Core; distributions do
not reinterpret shared pass outputs or changelog artifacts.
**Trigger**: PATT-03 front batch and explicit `Go` from Brice.
**Reason**: pipeline and release artifacts are shared skill-contract behavior.
**Impact**: Pi, OpenCode, Codex and Claude Code inherit six corrected contracts,
`release_document`, and front-family null-drift lint. No adapter or provider
runtime state changes.
**Author**: Codex (GO Brice)

### 2026-07-14 — Phase-1 authored artifact alignment (ADR-0039)
**Decision**: keep artifact taxonomy and authored-output alignment in Core; no
distribution may reinterpret shared output kinds or paths.
**Trigger**: PATT-03 Phase-1 batch and explicit `Go` from Brice.
**Reason**: artifact truth and verification are generic skill-contract concerns
shared by Pi, OpenCode, Codex and Claude Code.
**Impact**: all four distributions inherit eight corrected contracts, the
`design_document` kind and blocking null-drift lint. No adapter or runtime state
changes.
**Author**: Codex (GO Brice)

### 2026-07-14 — Unique generic routing-trigger ownership (ADR-0038)
**Decision**: keep trigger ownership and collision lint in Core; no distribution
may introduce provider-specific precedence for shared skills.
**Trigger**: PATT-04 and explicit `Go` from Brice.
**Reason**: deterministic responsibility routing is a generic catalog invariant
shared by Pi, OpenCode, Codex and Claude Code.
**Impact**: the four distributions inherit six clarified trigger owners and the
blocking duplicate check. No adapter, provider path or runtime state changes.
**Author**: Codex (GO Brice)

### 2026-07-14 — Dual phase namespace semantics (ADR-0037)
**Decision**: keep the phase alignment rule in Core; no provider adapter owns
or overrides it.
**Trigger**: PATT-02 and explicit `Go` from Brice.
**Reason**: agentic lifecycle metadata and catalog-router compatibility are
generic skill-contract invariants shared by Pi, OpenCode, Codex and Claude Code.
**Impact**: all four distributions inherit `SKILL.md phase: 02_AUDIT`, stable
`CONTRACT.yaml routing.phase_scope: phase_1`, and the blocking Core linter.
No adapter or provider runtime state changes.
**Author**: Codex (GO Brice)

### 2026-07-14 — Consumer managed hook assets (ADR-0034)
**Decision**: keep the ownership and provenance mechanism in Core; no provider
adapter owns or overrides it.
**Trigger**: SEC-CRED-005 + TER-001 and explicit `Go` from Brice.
**Reason**: project-owned versus VBB-managed file ownership, SHA-256 provenance,
and local Git hook installation are generic contracts shared by Pi, OpenCode,
Codex and Claude Code. Paths, personas and provider secrets are unaffected.
**Impact**: the four distributions inherit the corrected project initializer.
No file under `distributions/{pi,opencode,codex,claude}` changes. Existing
consumer assets without a manifest require explicit adoption; project truth is
never included in the managed bundle.
**Author**: Codex (GO Brice)

### 2026-07-14 — Layered credentials enforcement (ADR-0033)
**Decision**: keep in Core (aucune déclinaison distribution requise)
**Trigger**: SEC-CRED-001/002 and explicit approval of SEC-01 Option A
**Reason**: staged-content and CI credentials enforcement is a generic security
invariant shared by Pi, OpenCode, Codex and Claude Code. Provider adapters do not
own Git diff semantics or the detection policy.
**Impact**: Core gains one stdlib scanner used by the canonical hook and both CI
surfaces. `distributions/{pi,opencode,codex,claude}` require no code change and
inherit the same rule when operating the Core repository. External consumer
hook installation remains outside observable state.
**Author**: Codex (GO Brice)

### 2026-07-13 — V2-R1 gates fiables : résolution de run partagée + hooks canoniques (ADR-0027)
**Decision**: keep in Core (aucune déclinaison distribution requise)
**Trigger**: run `2026-07-13_1811_v2r1-gates-fiables` (TD-101, TD-102, défaut gate-linkage)
**Reason**: `tools/vbb_run_resolution.py`, la liaison ADR stricte de `vbb-gate-check.py`
et l'installateur `scripts/install-vbb-hooks.sh` sont des mécaniques génériques de gate.
Vérification Rule A : aucune référence aux installateurs ni à ces outils dans
`distributions/{pi,opencode,codex,claude}` (grep 0 hit) — impact distributions nul.
**Impact**: Core : sélection de run fiable (2 sélecteurs déclarés), gate ADR sans bascule,
hooks locaux composés. Distributions : aucun changement ; les anciens installateurs
restent des redirections dépréciées (aucun chemin cassé).
**Author**: claude-code (GO Brice)

### 2026-07-13 — V2-R3 audits scopés : paramètre scope + protocole d'itération (ADR-0028)
**Decision**: keep in Core (aucune déclinaison distribution requise)
**Trigger**: run `2026-07-13_1902_v2r3-audits-scopes` (AUDIT-A-001/002, demande granularité Brice)
**Reason**: le paramètre `scope` des 3 skills anti-slop et le protocole
`docs/REFERENCE/scoped-audit-protocol.md` sont de la grammaire générique d'audit.
Vérification Rule A : aucune référence à ces skills ni au protocole dans
`distributions/{pi,opencode,codex,claude}` (grep 0 hit) ; changement additif et
rétro-compatible (défaut = analyse globale inchangée).
**Impact**: Core : granularité au choix (global ↔ bloc ↔ répertoire), registre
consolidé par skill. Distributions : consomment la nouvelle capacité via les
skills partagés, aucun code de distribution modifié.
**Author**: claude-code (GO Brice)

### 2026-07-13 — V2-R4 passe qualité au closeout + règle compaction 40/75 (ADR-0029)
**Decision**: keep in Core (aucune déclinaison distribution requise)
**Trigger**: run `2026-07-13_2007_v2r4-closeout-qualite` (RB-2/RB-4, réserve Brice « selon risque »)
**Reason**: le contrat de closeout (prompt canonique + template) et SESSION_RULES
sont de la gouvernance générique consommée telle quelle par les 4 adaptateurs.
Vérification Rule A : une seule référence dans les distributions —
`distributions/pi/SYSTEM.md:115` cite le prompt `07-p-vbb-closeout` **par nom**
(pas de duplication de contenu) → héritage automatique de la nouvelle étape ;
changement additif, aucun closeout existant invalidé.
**Impact**: Core : passe qualité scopée déclenchée par le risque (traçage
EXECUTED/SKIPPED/N-A obligatoire) + règle de compaction 40 % indicatif / 75 % dur.
Distributions : héritent du comportement via les artefacts Core partagés.
**Author**: claude-code (GO Brice)

### 2026-07-13 — V2-R2 portabilité + diète du boot set (ADR-0030, CCP APPROVED)
**Decision**: keep in Core — le boot set (CLAUDE/AGENTS/SYSTEM) reste la source unique
**Trigger**: run `2026-07-14_0015_v2r2-portabilite-diete` (TD-105, TD-107, RC-5)
**Reason**: impact réel sur les 4 distributions (toutes consomment le boot set) :
pi/opencode via `SYSTEM.md` (symlink racine → `distributions/pi/SYSTEM.md`, vérifié),
claude via `CLAUDE.md` (@AGENTS+@SYSTEM), codex via bloc généré depuis `AGENTS.md`.
Diète à contenu normatif constant : SYSTEM recentré runtime + pointeurs vers AGENTS
(énoncé unique des règles) ; compteurs manuels supprimés ; chemins HOME purgés.
**Impact**: boot 2 156 → 1 440 mots (−33 %) hérité par les 4 adaptateurs sans
changement de leur code ; état externe `~/.claude/CLAUDE.md` → pointeur canon
(backup `.bak-20260713`), fin de la double grammaire VibeCodex.
**Author**: claude-code (GO Brice « boucler le ponçage »)

### 2026-07-13 — V2-R6 protocole runs autonomes (ADR-0031)
**Decision**: keep in Core
**Trigger**: run `2026-07-14_0045_v2r6-autonomie-multiruns` (RB-3, exigence autonomie Brice)
**Reason**: conduite autonome = gouvernance générique des 4 runtimes ; s'appuie
uniquement sur des mécaniques Core existantes (loop-closure V2-R1, kind split
Run 7, 40/75 + 4bis V2-R4). Vérification Rule A : aucune distribution ne
duplique AGENTIC_RUN_PROTOCOL/LONG_RUN_RULE (grep) — héritage direct.
**Impact**: Core : section « Runs autonomes » canonique + stub LONG_RUN_RULE.
Distributions : aucune modification de code.
**Author**: claude-code (GO Brice)

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
  | VBB Core decision log | `docs/DISTRIBUTIONS.md` §8 |
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
distributions supportées l'appellent sans changement de CLI, de schéma JSON ni
de code de sortie. `PIVOT` bloque explicitement avec la raison
`POC_VERDICT_PIVOT`.

**Author**: Codex, validé par Brice (`go`, 2026-07-13)

### 2026-07-13 — Retrait de la distribution Hermes/Cody

**Decision**: Retirer Hermes/Cody et limiter le support officiel à Pi,
OpenCode, Codex et Claude Code.

**Trigger**: Retour d'usage et demande explicite de Brice ; ADR 0025.

**Reason**: Hermes n'a pas apporté une satisfaction suffisante pour justifier
sa surface de maintenance, de sécurité et de documentation. Le proxy et le
bypass-lint restent du glue Hermes et ne sont pas promus dans Core.

**Impact**: `distributions/hermes/` et `--provider hermes` sont supprimés. Les
quatre adaptateurs conservés restent indépendants et partagent le même Core.
Les artefacts historiques ne sont pas réécrits et aucun fichier `~/.hermes/`
n'est touché.

**Author**: Brice (décision), Codex (migration)

### 2026-07-14 — Correction de l'executor conservée dans Core

**Decision**: Garder la correction des gates imbriqués, de la profondeur et des
cycles dans `tools/vbb-executor.py`, sans modification des quatre adaptateurs.

**Reason**: Ces invariants sont génériques et consommés par tous les runtimes.

**Impact**: Aucun glue provider, chemin installé ou contrat public ne change ;
les distributions héritent du Core corrigé.

**Author**: Codex, après GO Brice

### 2026-07-14 — Diète des skills conservée dans Core

**Decision**: Compresser les cinq contrats les plus lourds dans le catalogue
Core. **Impact**: les quatre distributions héritent des contrats allégés ; aucun
glue provider ni état runtime ne change. **Author**: Codex, après GO Brice.

### 2026-07-14 — Priorité des risques du dashboard conservée dans Core

**Decision**: Corriger le parseur et le tri dans l'outil Core partagé.
**Impact**: les quatre distributions voient les mêmes P1 prioritaires ; aucun
adaptateur ni format JSON ne change. **Author**: Codex, après GO Brice.

### 2026-07-14 — Refresh consommateur différé

**Decision**: Garder `vbb-project-init.py` limité au bootstrap. Le POC montre
que l'overwrite répété remplace la vérité projet puis sa sauvegarde.
**Impact**: aucun adaptateur ne change ; un refresh attendra une frontière
d'ownership explicite. **Author**: Codex, après GO Brice.

### 2026-07-14 — Nettoyage documentaire conservé dans Core

**Decision**: Compacter la vérité documentaire active dans Core et corriger
les liens relatifs partagés, sans déclinaison spécifique par distribution.
**Impact**: Pi, OpenCode, Codex et Claude Code héritent du même état courant ;
seul le lien relatif du profil Pi est ajusté, sans changer son contenu ni son
runtime. Les preuves historiques restent à leur emplacement. **Author**: Codex,
après GO Brice.

### 2026-07-14 — Précision de routage conservée dans Core

**Decision**: Garder dans Core la matrice de responsabilités, les déclencheurs
contractuels additifs et leur corpus de non-régression (ADR 0032).

**Reason**: Les responsabilités et triggers sont génériques aux quatre runtimes.
Le POC atteint 8/8 sans modifier l'orchestrateur, les IDs, les outputs ou les
artefacts des skills.

**Impact**: Pi, OpenCode, Codex et Claude héritent des mêmes cinq contrats plus
précis via le catalogue partagé. Aucun adapter, chemin provider, secret ou état
runtime ne change. TER-001 reste différé.

**Author**: Codex, après GO Brice

### 2026-07-14 — Nettoyage de l'executor conservé dans Core

**Decision**: Dédupliquer le loader YAML, normaliser le writer closeout et
expliciter le type du résultat dans `tools/vbb-executor.py`.

**Reason**: Cette dette appartient à l'exécuteur générique partagé ; elle ne
porte aucun comportement, chemin ou secret propre à un provider.

**Impact**: Pi, OpenCode, Codex et Claude Code héritent du module nettoyé et de
ses tests. Aucun adaptateur, contrat CLI/JSON ou état runtime ne change.

**Author**: Codex, après GO Brice

### 2026-07-14 — Toolchain Python statique promue en Core

**Decision**: Ruff 0.13.1 et mypy 2.1.0 constituent la toolchain statique
supportée par Core sur Python 3.11 ; Pyright reste hors contrat (ADR 0035).

**Reason**: Les règles, versions et gates futurs sont génériques et doivent
rester identiques pour les quatre runtimes.

**Impact**: Pi, OpenCode, Codex et Claude Code héritent de `pyproject.toml`, de
`requirements-dev.txt` et de la convention. Aucun adaptateur ou état installé
ne change ; les checks restent non-gating jusqu'à baseline zéro.

**Author**: Brice (Go), Codex (formalisation)

### 2026-07-14 — Nettoyage Ruff conservé dans Core

**Decision**: Retirer les 37 findings Ruff dans les outils et tests Core sans
modifier les règles ni promouvoir le gate.

**Reason**: Les outils sont partagés par les quatre runtimes et les corrections
sont strictement mécaniques.

**Impact**: Pi, OpenCode, Codex et Claude Code héritent du code nettoyé. Aucun
adaptateur, contrat, sortie textuelle ou état installé ne change.

**Author**: Codex, après GO Brice

### 2026-07-14 — Format Ruff conservé dans Core

**Decision**: Appliquer le formatter canonique aux 29 outils/tests signalés,
dans un lot mécanique isolé.

**Reason**: Le style Python Core est partagé ; l'équivalence AST prouve
l'absence de changement sémantique.

**Impact**: Pi, OpenCode, Codex et Claude Code héritent du même code formaté.
Aucun adaptateur, contrat ou état runtime ne change.

**Author**: Codex, après GO Brice

### 2026-07-14 — Nettoyage mypy conservé dans Core

**Decision**: Expliciter les structures typées de neuf outils et protéger le
chargement dynamique du router, sans ignore ni modification de configuration.

**Reason**: Ces frontières appartiennent au Contract Tooling Core partagé.

**Impact**: Pi, OpenCode, Codex et Claude Code héritent des annotations et du
guard explicite. Aucun adaptateur, format sérialisé ou gate CI ne change.

**Author**: Codex, après GO Brice

### 2026-07-14 — Gates statiques promues dans Core CI

**Decision**: Rendre Ruff check, Ruff format et mypy bloquants dans les CI
locale et GitHub après baseline zéro.

**Reason**: Les invariants et leur configuration sont génériques aux quatre
runtimes ; les garder hors gate permettrait une régression silencieuse.

**Impact**: Pi, OpenCode, Codex et Claude Code héritent des mêmes gates de
repository. Aucun adaptateur, permission GitHub ou état runtime ne change.

**Author**: Codex, après GO Brice

### 2026-07-14 — Ownership des surfaces prompt conservé dans Core

**Decision**: Documenter dans `PROMPTS_ARCHITECTURE.md` l'autorité respective
des canoniques, spécialisés, router et noms courts, sans changer leurs fichiers.

**Reason**: L'ownership et la precedence sont génériques aux quatre runtimes ;
les alias provider restent du glue de résolution sans comportement propre.

**Impact**: Pi, OpenCode, Codex et Claude Code partagent la même lecture. Aucun
prompt installé, alias, adapter ou état runtime ne change.

**Author**: Codex, après GO Brice

### 2026-07-14 — Migration anglaise des prompts conservée dans Core

**Decision**: Traduire en place les 18 prompts agent-actionables contenant de
la prose française et ajouter un test de non-régression conservateur, selon
l'ADR 0036.

**Reason**: La langue des instructions et les contrats de phase sont génériques
aux quatre runtimes. Les dupliquer dans les adaptateurs créerait quatre vérités.

**Impact**: Pi, OpenCode, Codex et Claude Code héritent des mêmes prompts
anglais lors de l'installation/résolution suivante. Aucun alias, chemin, adapter,
setup provider ou état runtime installé n'est modifié dans ce dépôt.

**Author**: Brice (demande explicite), Codex (formalisation et intégration)

## 9. References

- `README.md` — entry point; "VBB Core vs Distributions" anchors the
  high-level distinction.
- `AGENTS.md` — Critical Rule #12 enforces the Core ↔ Distribution rule.
- `GUIDE.md`, `docs/PILOTAGE.md`, `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`
  — all describe VBB Core.

Supported runtime details live in each `distributions/<provider>/README.md`.

---

*This file is canon. Changes are governed by AGENTS.md Critical Rule #12 and
must be recorded in §8 above.*
