---
name: 3-vbb-risk-register
description: |
  Consolidates findings from existing Vibebackbone reports into a single risk register.
  Performs no new audit and no new analysis beyond normalization, deduplication,
  priority ordering, and explicit identification of unknown or uncovered areas.
  Use after phase 2 audits, or when compiling "identified and accepted risks".
version: "2.0"
phase: 3
token_budget: low
subagent_eligible: true
mode_sensitive: false
---

# Risk Register Compiler

Standard reference: `0-vbb-standard`

Read `docs/PILOTAGE.md` first.

## ROLE & POSTURE

You are a consolidator.
You do NOT re-audit.
You do NOT create new findings.
You compile, normalize, and order risks already present in existing reports.

Absolute rules:

- NO assumptions
- If a report is missing, mark the zone `UNKNOWN`
- No new analysis beyond consolidation
- No code patches
- No feature work

## INPUT CONTRACT

**Required:**

- [ ] Access to `docs/audits/`

**Optional:**

- [ ] `docs/AUDIT_STATUS.md`
- [ ] Recent phase 0, 1, and 2 reports
- [ ] Explicit decisions already documented (accept / mitigate / defer)

**Accepted sources:** Vibebackbone Markdown reports, `docs/AUDIT_STATUS.md`, project documentation

## BLOCKING CONDITIONS

- If `docs/audits/` is not accessible → STOP. Message: "Cannot compile risk register without access to reports."
- If no reports are present → STOP. Message: "No reports available to consolidate."
- If reports are too heterogeneous or incomplete to reconcile properly → conclude with a large `UNKNOWN` share.

## SCOPE

### Included

- consolidation of existing findings
- deduplication of risks
- grouping by risk families
- identification of uncovered areas
- reprise of explicit decisions if already present in reports

### Excluded

- re-audit
- creation of new findings
- speculative reinterpretation of reports
- product or operational decisions on behalf of the user

## PROCESS

1. List recent reports in `docs/audits/`.
2. Identify available relevant reports:
   - scope freeze
   - audit readiness
   - security
   - systemic risk
   - data integrity
   - db robustness
   - ops
   - ci
   - legal
   - api auditor
3. Extract findings and explicit risks.
4. Deduplicate manifestly redundant items without losing original references.
5. Group consolidated risks.
6. List uncovered areas or missing reports as `UNKNOWN`.
7. Reprise explicit decisions (`Accept`, `Mitigate`, `Defer`) only if already documented.

## OUTPUT CONTRACT

Ensure `docs/audits/` exists.

Write ONE Markdown file to:
`docs/audits/risk-register-{YYYYMMDD-HHMM}.md`

Then update `docs/AUDIT_STATUS.md`.

The report must follow this format:

# Identified and Accepted Risk Register — v1.0 — YYYY-MM-DD

## Identified and Accepted Risks

1. [SEC-02] ...
2. [SYS-05] ...
3. [DATA-03] ...

## UNKNOWN / Uncovered Areas

- Missing report: ...

## Decision

- Accept / Mitigate / Defer / UNKNOWN

Each consolidated risk must contain:

- original reference(s)
- risk summary
- priority level if visible
- decision state if explicitly documented

## VERDICT RULES

- `READY`
  - existing risks are cleanly consolidated
  - uncovered areas are explicitly listed
- `PARTIAL`
  - consolidation possible but several areas remain scattered or weakly linked
- `BLOCKED`
  - available reports are too absent or too incoherent to produce a useful register
- `UNKNOWN`
  - used only if documentary evidence is too weak to conclude properly