---
context_role: audit-dashboard
phase: transverse
status: active
updated: 2026-07-14
temporal_provenance: TEMPORAL_PROVENANCE.md
---

# AUDIT_STATUS — vibebackbone

> Current audit state of this repository. Detailed and resolved findings remain
> in [`audits/`](audits/), [`runs/`](runs/), and git history; they are not
> duplicated here. Use `python tools/vbb-status-dashboard.py` for generated
> measurements and recent-run resolution.

## Global verdict

**`PARTIAL — reference-ready; bounded consumer, quality, and traceability gaps remain`**

The Core contracts, architecture checks, runtime executor, and four supported
distribution adapters are operational. No remediation run is mandatory. Reopen
`TER-001` only with an explicit ownership/generated-file design mandate.

## Active risks

| ID | Severity | Description | Status |
|---|---|---|---|
| TER-001 | P1 | Consumer refresh cannot safely reconcile customized project truth: skip mode does not refresh, while repeated overwrite replaces both the project file and its prior backup. | **OPEN — DEFERRED** — POC [`2026-07-14_0721_consumer-refresh-poc`](runs/2026-07-14_0721_consumer-refresh-poc/07_CLOSEOUT.md) is NO-GO; requires an ownership design. |
| GMA-003 | P1 | Executor loader duplication and concentrated typing debt remain outside the correctness fix. | **MITIGATING** — correctness paths are directly covered; cleanup is deferred to a bounded code-quality run. |
| SYS-POST-002 | P1 | A final external audit bypassed the canonical AUDIT artifact and FINAL_STATUS contract. | **OPEN / HISTORICAL** — commit `d0eab3c` cannot be retroactively rewritten; current runs follow the contract. |
| QOA-006 | P2 | `docs/runs/routing-fix-verification.md` is a loose artifact outside a timestamped run directory. | **OPEN** — archive or reconstruct only after explicit approval. |
| QOA-007 | P2 | Optional Ruff, formatting, mypy, and pyright baselines are not clean or canonically gated. | **OPEN** — keep non-gating until a dedicated baseline run. |
| GMA-005 | P2 | Long functions, Python naming ambiguity, and French prompt prose remain convention-drift candidates. | **OPEN** — requires a separate, bounded canon proposal and migration decision. |
| DOC-001 | P2 | Prompt entrypoints still lack one final responsibility matrix across canonical, specialized, router, and short-name layers. | **OPEN** — continue only if current navigation proves insufficient. |
| DOC-002 | P2 | Code-audit detector skills overlap without a single responsibility matrix. | **OPEN** — confirm whether bounded overlap is acceptable before adding documentation. |
| SYS-POC-004 | P2 | POC-to-implementation transitions do not always record a distinct durable decision. | **OPEN** — require the decision for future canon, architecture, and cross-service changes. |
| SYS-SUB-003 | P2 | Reintegration checks paths and presence more readily than counts, citations, and semantic contradictions. | **OPEN** — add semantic acceptance checks to future delegation briefs when delegation is used. |
| QA-004 | LOW | Temporal provenance is documented but not automated in artifact generators. | **OPEN** — automate only with a dedicated generator change. |
| QA-005 | LOW | Skill-level architecture decisions may lack explicit ADR traceability. | **OPEN** — verify on demand; do not create ADRs by count. |
| QA-007 | LOW | The canon-change proposal template has not been exercised. | **OPEN** — validate on the next real canon change. |

## Latest evidence

- Documentation cleanup: [`2026-07-14_0727_documentation-cleanup`](runs/2026-07-14_0727_documentation-cleanup/07_CLOSEOUT.md)
  and [documentation context report](audits/doc-context-20260714-0727.md).
- Consumer-refresh decision: [`2026-07-14_0721_consumer-refresh-poc`](runs/2026-07-14_0721_consumer-refresh-poc/07_CLOSEOUT.md).
- Dashboard risk prioritization: [`2026-07-14_0714_dashboard-risk-priority`](runs/2026-07-14_0714_dashboard-risk-priority/07_CLOSEOUT.md).
- Active-truth and skill compaction: [`2026-07-14_0700_truth-skill-diet`](runs/2026-07-14_0700_truth-skill-diet/07_CLOSEOUT.md).
- Executor correction: [`2026-07-14_0010_executor-correctness`](runs/2026-07-14_0010_executor-correctness/07_CLOSEOUT.md).
- Latest broad audit: [`2026-07-13_2351_deep-post-sanding-audit`](runs/2026-07-13_2351_deep-post-sanding-audit/02_AUDIT_REPORT.md).

## Resolved by the documentation cleanup

- `QOA-005`: replaced contradictory quality tables with one active register.
- `GMA-004`: repaired all confirmed actionable local-link failures on active,
  tracked Markdown surfaces; template placeholders remain intentionally virtual.
- `QOA-009`: removed copied catalog/runtime/test counters from the active status
  and navigation index; generated tools are the measurement source.

## Update policy

- Add only current unresolved or explicitly accepted risks to the active table.
- Link to run/audit evidence instead of copying measurements or resolved tables.
- Keep historical audits, runs, ADRs, and activity logs immutable.
- Move or archive documentation only after explicit human agreement.
