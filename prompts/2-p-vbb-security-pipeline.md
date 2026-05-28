---
description: Run full Vibebackbone security pipeline
---

Run the full Vibebackbone security pipeline on the current system: $@

## Objective

Produce a complete security analysis followed by a prioritized remediation plan.

## Pipeline order — mandatory

1. `2-vbb-security`
2. `2-vbb-systemic-risk`
3. `3-vbb-risk-register`
4. `4-vbb-security-remediation`

## Rules

- Each skill must operate strictly within its scope.
- Do not merge steps.
- Do not skip steps.
- Do not invent findings.
- UNKNOWN is allowed.
- Evidence is required.
- No code patches.
- No feature work.
- No new findings after the phase 2 audits (steps 1–2).
- The risk register (step 3) consolidates only.
- The remediation (step 4) transforms existing risks into actions only.

## Fallback rule

If a required skill is missing, STOP and explicitly state the missing skill.
Manual fallback is allowed only if explicitly justified.

## Expected process

### Step 1 — Security Audit

Use `2-vbb-security`.

Scope: authentication, authorization, secrets, input validation, injection risks, API exposure, configuration leaks.

Produces: `docs/audits/security-{YYYYMMDD-HHMM}.md`

### Step 2 — Systemic Risk

Use `2-vbb-systemic-risk`.

Scope: implicit assumptions, hidden dependencies, trust-boundary fragility, SPOFs, non-return operations, risky compositions.

Produces: `docs/audits/systemic-risks-{YYYYMMDD-HHMM}.md`

### Step 3 — Risk Register

Use `3-vbb-risk-register`.

Scope: consolidation, deduplication, normalization, missing-zone identification.
No new findings. No new audit.

Produces: `docs/audits/risk-register-{YYYYMMDD-HHMM}.md`
Updates: `docs/AUDIT_STATUS.md`

### Step 4 — Security Remediation

Use `4-vbb-security-remediation`.

Scope: transform consolidated risks into prioritized action plan.
No new findings. No code. No feature work.

Produces: `docs/audits/security-remediation-{YYYYMMDD-HHMM}.md`
Updates: `docs/AUDIT_STATUS.md`

## Final output

After all 4 steps, summarize:

- reports created or updated
- main risks identified
- remediation priorities (P0 / P1 / P2)
- readiness status
- skills used in order
- missing inputs or limitations

---

## Closeout sequence (mandatory — run after the final summary)

After the final summary:

1. `t-vbb-commit-ready` → verdict + conventional commit message
2. `git add docs/audits/security-*.md docs/audits/systemic-risks-*.md docs/audits/risk-register-*.md docs/audits/security-remediation-*.md` → `git commit -m "<message>"` → `git push`
3. Update `docs/SESSION.md` (clear if session done, note state if re-entry planned)
4. Update `docs/CONTEXT.md` (status, run link, decisions, open points, next action)

> Audit reports are persisted in `docs/audits/` — they must be committed and pushed. Do not stop after the summary. The security pipeline loop is not closed until git push is done.
