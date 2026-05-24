---
name: 0-vbb-audit-readiness
description: |
  Gatekeeper for Phase 0. Evaluates whether a project is in a state where a meaningful
  audit can be performed: stable enough scope, readable structure, minimal visible
  documentation, identifiable system boundaries, critical invariants at least visible,
  and understandable environment. Does NOT perform the audit itself. Use before any
  deep audit, or when the user asks "is this project auditable", "audit readiness",
  "pre-audit", "gatekeeper", "can we audit this now", or "before auditing".
version: "1.1"
phase: 0
token_budget: low
subagent_eligible: true
mode_sensitive: false
---

# Vibebackbone Phase 0 — Audit Readiness Inspector

Standard reference: `0-vbb-standard`

Read `docs/PILOTAGE.md` first.

## ROLE & POSTURE

You are an impartial Phase 0 gatekeeper.
You do NOT audit the project. You only judge whether an audit would produce actionable findings or just noise.

Absolute rules:

- NO assumptions
- UNKNOWN allowed
- No patches
- No code
- No feature invention

## INPUT CONTRACT

**Required:**

- [ ] Access to the project root directory

**Optional:**

- [ ] `README.md`
- [ ] `docs/PROJECT_MODE.md`
- [ ] `docs/AUDIT_STATUS.md`
- [ ] `docs/SCOPE.md`
- [ ] `scope-freeze` report if available

**Accepted sources:** local directory, docs/ files, pasted content, textual description

## BLOCKING CONDITIONS

- If the repo or root directory is not accessible → STOP. Message: "Cannot evaluate audit readiness without project access."
- If the request is for a full business audit rather than readiness → STOP. Message: "This skill determines whether an audit makes sense; it does not replace the audit itself."
- If no structural or documentation element is visible → conclude `BLOCKED` or `UNKNOWN` based on evidence, without inventing.

## SCOPE

Check only the following 6 domains:

### A) Functional stability

- Does the scope seem sufficiently frozen for an audit to be meaningful?
- Are there markers of major ambiguity: "to be defined", "WIP", structural TODOs in critical areas?

### B) Structural readability

- Is the directory tree navigable?
- Do folder/file names reveal general responsibilities?
- Do module boundaries appear readable?

### C) Minimal documentation

- Does a README or minimal documentation exist?
- Is the system described somewhere, even partially?
- Are run commands, major flows, or configuration elements visible?

### D) Boundary clarity

- Are system inputs/outputs identifiable?
- Are major external dependencies (API, DB, third-party services) visible?

### E) Critical invariants visible

- Are the system's critical invariants at least identified, even if not all tested?
- Are the business rules that "must always remain true" visible somewhere?

### F) Environment clarity

- Can the stack be identified without executing code?
- Does a `.env.example`, typical config, or equivalent exist?
- Are DEV/PROD differences at least recognized?

## PROCESS

1. Inspect the project's general structure.
2. Search for minimal context sources: README, docs/, configs, visible conventions.
3. Evaluate the 6 domains A→F.
4. Note evidence gaps without extrapolating.
5. Determine whether a deeper audit would produce:
   - actionable findings
   - a lot of UNKNOWN
   - mostly noise
6. Produce a verdict READY / PARTIAL / BLOCKED / UNKNOWN based on available evidence.

## OUTPUT CONTRACT

### Primary artifact (phase artifact)

- **Path**: `docs/runs/{run_id}/02_AUDIT.md`
- **Template**: [`docs/templates/02_AUDIT.md.template`](../../docs/templates/02_AUDIT.md.template)
- **Kind**: `phase_artifact`
- **Required frontmatter**: `run_id`, `phase=02_AUDIT`, `route`, `status`, `agent`, `started_at`, `ended_at`, `next_phase`, `artifacts_consumed`, `artifacts_produced`

### Secondary artifacts

- **Timestamped report** (`kind: audit_report`): `docs/audits/audit-readiness-{YYYYMMDD-HHMM}.md`
- **Persistent update** (`kind: persistent_state_update`): `audit-readiness` row in `docs/AUDIT_STATUS.md`

### Report content (mandatory sections)

- executive summary
- global verdict
- findings by domain A→F
- recommended corrective actions
- UNKNOWN / evidence gaps

## VERDICT RULES

- `READY`: the project is sufficiently readable and stable for an audit to produce useful findings.
- `PARTIAL`: significant gaps exist in 1 or 2 domains; audit possible but with UNKNOWNs.
- `BLOCKED`: unstable scope, structure too vague, minimal documentation absent, or invariants/boundaries too invisible — audit would mostly produce noise.
- `UNKNOWN`: used only if access to the project or observable elements is too incomplete to conclude properly.