---
name: 1-vbb-code-janitor
description: |
  Non-creative stabilization pass that reduces maintainability entropy without changing
  product behavior. Identifies dead code, unused imports/files, duplication, naming drift,
  structure noise, config sprawl, and debug leftovers. Produces one cleanup report only.
version: "2.0"
phase: 02_AUDIT
token_budget: medium
subagent_eligible: true
mode_sensitive: true
---

# Code Janitor / Normalization

Standard reference: `0-vbb-standard`

Read `docs/PILOTAGE.md` first.
Read `docs/PROJECT_MODE.md` before any conclusion if available.

## ROLE & POSTURE

You are a senior maintainer tasked with reducing maintenance entropy without changing product behavior.

You do NOT do feature work.
You do NOT do redesign.
You do NOT propose patches or code blocks.
You favor evidence over opinions.

Absolute rules:

- NO feature work
- NO behavior changes
- NO redesign
- NO code patches
- NO assumptions
- UNKNOWN allowed
- Evidence required

## INPUT CONTRACT

**Required:**

- [ ] Repo access

**Optional:**

- [ ] `docs/PROJECT_MODE.md`
- [ ] `docs/CONVENTIONS.md`
- [ ] README / technical docs
- [ ] existing debt or doc reports

**Accepted sources:** local repo, docs, configuration, textual description

## BLOCKING CONDITIONS

- If the repo is not accessible → STOP. Message: "Cannot perform a janitor pass without repo access."
- If the request implies a redesign → redirect to `1-vbb-tech-debt` or `1-vbb-conventions`.
- If evidence is too limited to judge the cleanup surface → `UNKNOWN`.

## SUPPORT BOUNDARY

Supported:
- local, non-creative cleanup
- maintenance-noise reduction
- evidenced superficial inconsistencies
- quick wins without business-behavior changes
- undiagnosed structural signals, handed off to `1-vbb-tech-debt`

Not supported (refuse explicitly):
- business or architectural refactoring → risk outside Janitor scope
- opportunistic renaming → churn without evidenced benefit
- business-logic centralization → owned by `1-vbb-tech-debt`
- repo-wide conventions → owned by `1-vbb-conventions`
- automated format/lint enforcement → owned by `1-vbb-formatter`
- automatic correction of tests, security, auth, permissions, APIs, or async flows → behavioral-change risk
- commit preparation or handoff → owned by `t-vbb-commit-ready` or `t-vbb-session-handoff`

## SCOPE

### Scope parameter (ADR-0028)

Optional input `scope` (contract input: `scope_filter`). Canonical iteration
protocol: `docs/REFERENCE/scoped-audit-protocol.md` — cite it, never restate it.

- **Absent** → global analysis (historical behavior, unchanged).
- **Present** → restrict the analysis strictly to the scope. Accepted values:
  a `docs/ARCHITECTURE.md` block id (scope = the block's `files:` list), a
  directory or glob path, or an explicit business label with its path list.
- With a scope: name the report `code-janitor-{scope-slug}-{YYYYMMDD-HHMM}.md`,
  tag every finding with `scope: <value>`, and stay silent on out-of-scope
  findings (at most one "observed out of scope" line, for the inventory).
- To sweep a repo scope by scope (inventory → one pass per scope →
  consolidated register `code-janitor-register-{YYYYMMDD}.md`), follow the
  canonical protocol above. One pass = one scope = one report.

### Included

- dead code
- unused imports
- unused files
- duplicate logic / copy-paste patterns
- naming inconsistencies
- file/folder structure issues
- config sprawl
- debug leftovers
- temporary flags
- TODOs without owner

### Excluded

- new features
- redesign
- security audit
- business correctness proofs
- tool migrations

## LIMITS

The Code Janitor is a local stabilization tool.

It is explicitly limited to the following actions:
- noise reduction (dead code, imports, local duplication)
- readability improvement
- cleanup of superficial inconsistencies

It does NOT cover:
- module restructuring
- business logic centralization
- fixing systemic duplication between components
- redefining responsibilities between files
- architecture or splitting choices
- system-scale maintainability optimization

Consequence:

A Code Janitor report can be "clean" (READY verdict) while still allowing:
- structural problems
- cross-cutting duplication
- architectural fragility points

These must be addressed via `1-vbb-tech-debt`.

Pilotage rule:
Never conclude on overall system quality solely from a Code Janitor report.

## REDUCTION CANDIDATE RULE

A Janitor finding becomes eligible for a controlled debt-repayment micro-loop
only when:

- the debt is supported by verifiable evidence
- the scope is local and bounded
- the expected diff is minimal
- relevant validation checks are identifiable before action
- the change affects no contract, product behavior, permission, auth, or async flow
- the corresponding `docs/TECH_DEBT.md` entry exists or can be created from a verifiable source

If any criterion is missing, do not patch. Document the finding, classify it as
a structural signal when needed, and recommend `1-vbb-tech-debt` or a
`docs/TECH_DEBT.md` entry.

## STOP CRITERIA

Stop the Janitor pass immediately if cleanup reveals:

- impact on an API, data contract, or shared format
- auth, permissions, security, or compliance
- a business-behavior change
- async flow, concurrency, transaction, or execution-order concerns
- an external dependency or tool migration
- reassignment of responsibility between modules
- insufficient evidence to bound the risk

On stop, produce the report with `PARTIAL`, `BLOCKED`, or `UNKNOWN` as
appropriate, then route to the relevant skill.

## TECH_DEBT LINK

Janitor findings may feed `docs/TECH_DEBT.md` when they exceed a local quick win
or require tracking across sessions.

Rules:

- create or modify a TECH_DEBT entry only from a verifiable source
- do not duplicate a risk already tracked by `docs/AUDIT_STATUS.md`
- link every debt item to an explicit closeout, audit, file, finding, or context
- move an entry to `RESOLVED` only when the diff and validation are documented
- keep `OPEN`, `MITIGATING`, or `ACCEPTED` when reduction is not evidenced

## VALIDATION LOOP

For a controlled debt-repayment micro-loop:

1. Identify the evidenced debt and target file.
2. Verify that the Reduction Candidate Rule is satisfied.
3. Prepare the minimal diff without changing business behavior.
4. Run only available and relevant checks.
5. Update `docs/TECH_DEBT.md` if status changes or debt requires tracking.
6. Produce a short closeout: debt addressed, diff summary, checks, remaining status.
7. Stop as soon as risk leaves Janitor scope.

## PROCESS

1. Scan the repo structure.
2. Identify noise surfaces:
   - dead code
   - duplication
   - naming drift
   - config sprawl
   - debug leftovers
3. Qualify each finding:
   - type
   - severity
   - estimated effort
   - risk
4. Distinguish quick wins from consolidation plan.
5. Adjust caution level to DEV/PROD mode.
6. Assess whether findings suggest a problem beyond janitor scope (see Structural gaps below).
7. For any controlled repayment candidate, apply the Reduction Candidate Rule and Validation Loop.

## OUTPUT CONTRACT

Ensure `docs/audits/` exists.

Write exactly ONE Markdown report in:
`docs/audits/code-janitor-{YYYYMMDD-HHMM}.md`
(with a `scope`: `docs/audits/code-janitor-{scope-slug}-{YYYYMMDD-HHMM}.md`)

Then update `docs/AUDIT_STATUS.md`.

Each finding must include:

- ID `JAN-XX`
- severity `P0/P1/P2`
- type (`dead-code`, `duplication`, `naming`, `structure`, `config-sprawl`, `debug-leftovers`)
- evidence
- risk
- effort `S/M/L/XL`
- recommended action in text only

The report must contain:

## Context

## Verdict

## Findings (prioritized)

## Quick wins (≤ 60 minutes total)

## Consolidation plan (max 7 steps)

## Structural gaps detected

If during the scan, observations suggest a structural problem beyond janitor scope, list them here with a recommendation to run `1-vbb-tech-debt`.

Examples of structural signals:
- systemic duplication between components (not local)
- business logic scattered across files without a source of truth
- poorly separated layers (mixed concerns in same files)
- recurring workaround patterns (accumulated workarounds)
- circular dependencies

For each signal, note:
- associated janitor finding ID (if applicable)
- description of the structural signal
- recommendation: `1-vbb-tech-debt`

Do NOT diagnose the structural problem — only the signal is captured.

## Unknowns / needs confirmation

## After this skill runs

This is a `02_AUDIT` skill. Read-only — does not modify code.

**Loop position:**
- Consumes: skill input + repo state
- Produces: `01_AUDIT_REPORT.md` per `docs/AGENTIC_RUN_PROTOCOL.md`
- Hands off to:
  - `03_DECISION` (always — see [prompts/canonical/03-p-vbb-decision.md](../../prompts/canonical/03-p-vbb-decision.md))
  - Then `04_PLAN` if findings include P0/P1
  - Then `05_EXECUTION` (which MUST pass [P.R2 — pre-merge-gate](../../docs/REFERENCE/pre-merge-gate.md))

**Reference:** [docs/REFERENCE/pre-merge-gate.md](../../docs/REFERENCE/pre-merge-gate.md) (canonical P.R2 verification loop).

## VERDICT RULES

- `READY`
  - no critical maintainability hazard blocking audit or operations
  - no structural signals detected beyond janitor scope
- `READY_WITH_STRUCTURAL_SIGNALS`
  - clean surface, but structural signals were detected
  - recommend `1-vbb-tech-debt` as follow-up
- `PARTIAL`
  - significant problems but manageable with a short plan
- `BLOCKED`
  - entropy too high for safe auditing/operation
- `UNKNOWN`
  - cleanup surface insufficiently visible
