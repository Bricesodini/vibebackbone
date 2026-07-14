---
description: Pre-release gate — full product quality audit before shipping to production
---

Evaluate whether the product is ready for production release: $@

## Objective

This is the final gate before shipping. It performs a complete product-readiness
check across security, integrity, operations, legal, performance, accessibility,
and documentation, then produces a clear GO / NO-GO decision.

It is the product architect's final review before release.

## Preferred Vibebackbone skills

- `2-vbb-security`
- `2-vbb-systemic-risk`
- `2-vbb-data-integrity`
- `2-vbb-db-robustness`
- `2-vbb-ops`
- `2-vbb-ci`
- `2-vbb-legal`
- `2-vbb-api-auditor`
- `2-vbb-performance`
- `2-vbb-accessibility`
- `2-vbb-analytics`
- `2-vbb-spec-validator`
- `t-vbb-mode-transition-gate`
- `3-vbb-risk-register`

## Skill routing and chaining rule

### Wave 1 — Security & risks (mandatory)

Run sequentially:

1. `2-vbb-security` — security audit
2. `2-vbb-systemic-risk` — systemic risks
3. `2-vbb-data-integrity` — data integrity

If any of the three is BLOCKED → immediate NO-GO.

### Wave 2 — Infrastructure & operations (mandatory)

Run sequentially: 4. `2-vbb-db-robustness` — database robustness 5. `2-vbb-ops` — operational readiness 6. `2-vbb-ci` — CI/CD 7. `2-vbb-legal` — legal compliance

### Wave 3 — Product quality (mandatory)

Run in parallel: 8. `2-vbb-api-auditor` — API audit (if applicable) 9. `2-vbb-performance` — performance 10. `2-vbb-accessibility` — accessibility (for UI) 11. `2-vbb-analytics` — instrumentation 12. `2-vbb-spec-validator` — specification compliance

### Wave 4 — Transition & consolidation (mandatory)

13. `t-vbb-mode-transition-gate` — ready for PROD?
14. `3-vbb-risk-register` — consolidated risk register

## Required process

1. **Restate** the product and target release.
2. **Wave 1** — Security & risks.
3. **Wave 2** — Infrastructure & operations.
4. **Wave 3** — Product quality.
5. **Wave 4** — Transition & consolidation.
6. **Final verdict**: GO / CONDITIONAL_GO / NO_GO.

## Verdict rules

### GO 🟢

- All Wave 1 audits: READY
- All Wave 2 audits: READY or PARTIAL (with PARTIAL items documented and accepted)
- All Wave 3 audits: READY, PARTIAL, or ADEQUATE
- Mode-transition-gate : READY
- Risk-register: no unresolved P0

### CONDITIONAL_GO 🟡

- Wave 1: READY or PARTIAL (no BLOCKED)
- Wave 2: at least one PARTIAL with accepted risk
- Wave 3: documented gaps and a post-release remediation plan
- Mode-transition-gate: PARTIAL with documented acceptance
- The product architect explicitly accepts residual risks

### NO_GO 🔴

- A BLOCKED verdict in Wave 1 or Wave 2
- Mode-transition-gate : BLOCKED
- Risk-register contains unresolved P0 items
- The architect refuses to sign off residual risks

## Output format

- **Product / Release**
- **Wave 1 — Security**: security verdict, systemic-risk verdict, data-integrity verdict
- **Wave 2 — Infrastructure**: db-robustness, ops, CI, legal verdicts
- **Wave 3 — Quality**: api-auditor, performance, accessibility, analytics, spec-validator verdicts
- **Wave 4 — Transition**: mode-transition verdict, risk-register summary
- **Final verdict**: GO / CONDITIONAL_GO / NO_GO
- **Accepted risks**: list for CONDITIONAL_GO
- **Blockers**: list for NO_GO
- **Next action**: deploy / fix and re-check / escalate

---

## Closeout sequence (mandatory — run after the final verdict)

After the GO / CONDITIONAL_GO / NO_GO verdict:

1. `t-vbb-commit-ready` → verdict + conventional commit message
2. `git add docs/audits/release-check-*.md docs/runs/*/03_DECISION_RECORD.md` → `git commit -m "<message>"` → `git push`
3. Update `docs/SESSION.md` (clear if session done, note state if re-entry planned)
4. Update `docs/CONTEXT.md` (status, run link, decisions, open points, next action)
5. Update `docs/AUDIT_STATUS.md` (new release-check report)

> Release-check reports and decision records are product-critical artifacts — they must be versioned. Do not stop after the verdict. The release-check loop is not closed until git push is done.

---

## Agent protocol alignment

**Corresponding phases**: 02_AUDIT (waves 1–3) + 03_DECISION (wave 4 + verdict)

This prompt orchestrates 14 skills in 4 waves within one session. It is the heaviest prompt in the catalog.

**⚠️ Context warning**: if available LLM context is below 200K tokens, or the repository is large (>50 active files), prefer running each wave in a separate session:

| Wave | Dedicated session | Canonical prompt |
|------|---------------|-----------------|
| Wave 1 | Session 1 | `canonical/02-p-vbb-audit` + skills security, systemic-risk, data-integrity |
| Wave 2 | Session 2 | `canonical/02-p-vbb-audit` + skills db-robustness, ops, ci, legal |
| Wave 3 | Session 3 | `canonical/02-p-vbb-audit` + skills api-auditor, perf, a11y, analytics, spec-validator |
| Wave 4 | Session 4 | `canonical/03-p-vbb-decision` + mode-transition-gate + risk-register |

**Expected artifacts**:
- `docs/runs/YYYY-MM-DD_HHmm_slug/02_AUDIT_REPORT.md` — consolidated report for waves 1–3
- `docs/runs/YYYY-MM-DD_HHmm_slug/03_DECISION_RECORD.md` — GO/CONDITIONAL_GO/NO_GO verdict + accepted risks
- `docs/audits/release-check-YYYYMMDD-HHMM.md` — persistent timestamped report

**Handoff after verdict**:

- If GO → create a `canonical/05-p-vbb-execution` session or proceed with deployment
- If CONDITIONAL_GO → create a `canonical/03-p-vbb-decision` session to document accepted risks, then deploy
- If NO_GO → create a `canonical/04-p-vbb-plan` session to plan fixes, then run this prompt again
