---
run_id: "2026-07-31_external-pilot-remediation-assurance"
phase: "02_AUDIT"
document_convention: "vbb-doc-v1"
version: "1.0"
type: "audit_report"
visibility: "internal"
status: "ready"
tags: [run, audit, contract, governance, security]
relations:
  - "../2026-07-31_vbb-doc-v1-external-pilot/02_AUDIT.md"
  - "../2026-07-31_vbb-doc-v1-external-pilot/03_DECISION.md"
  - "04_PLAN.md"
route: "AUDIT"
subject: "vbb-doc-v1 and A2/A3 assurance alignment"
verdict: "CONFIRMED_FINDINGS_REMEDIATED_OR_RECLASSIFIED"
---

# Independent exploitation of the external pilot

The historical pilot evidence was read in full, including the inventory,
minimal and extended linter outputs, declaration, mapping decisions, review,
and closeout. Backbone Know remains read-only.

## Finding disposition

| Finding | Reproducible | Classification | Criticality | RC blocker | Decision |
|---|---|---|---|---|---|
| F-PH1-01 uppercase/lowercase status ambiguity | Yes, contract text vs BK inventory | CONTRACT_DEFECT | S2 | No | Clarified: canonical status is lowercase; project meaning uses explicit extensions. |
| F-PH1-02 compound BK statuses lack extension mechanism | Yes | CONTRACT_DEFECT | S1 | Yes | Fixed with `status_extensions: project:status:<value>` and contract text. |
| F-PH1-03 `context_role` vocabulary | Yes | PROJECT_SPECIFIC | S3 | No | Keep as `project:role:*`; no contract change. |
| F-PH1-04 `phase` vocabulary | Yes | PROJECT_SPECIFIC | S3 | No | Keep as project dimension/tag; no contract change. |
| F-PH1-05 kind/audit_type/poc_id/increment | Yes | PROJECT_SPECIFIC | S3 | No | Keep as namespaced project vocabulary; no contract change. |
| F-PH1-06 canonical read order not technically enforced | Yes | PUBLIC_DOCUMENTATION_DEFECT | S2 | No | Post-v1 improvement; the order is documented and remains advisory. |
| F-PH1-07 out-of-scope docs not surfaced | Yes, extended scope stayed silent | LINTER_DEFECT | S1 | Yes | Fixed with non-blocking `--suggest-scope`. |
| F-PH1-08 relation targets not existence-checked | Yes | LINTER_DEFECT | S3 | No | Post-v1 improvement; not required for autonomous RC adoption. |
| F-PH1-09 scope relation coherence not checked | Yes | LINTER_DEFECT | S3 | No | Post-v1 improvement; not required for autonomous RC adoption. |
| F-PH1-10 no progressive adoption/waivers | Yes, extended scope fails closed without migration path | CONTRACT_DEFECT | S1 | Yes | Fixed with multi-root-compatible scope filtering and explicit expiring waivers. |
| F-PH2-01 unnamespaced `research` tag | Yes, minimal pilot first run | PROJECT_SPECIFIC | S3 | No | Correct mapping is `project:domain:research`; no contract change. |

All findings are confirmed as observations of the pilot evidence. The three
RC blockers are genuine only insofar as they prevent a third-party maintainer
from progressively understanding, declaring, applying, or verifying the
contract. F-PH1-06/08/09 are real improvements but do not meet that threshold.

## Historical assurance interpretation audit

The old A2 meaning appears in ADR 0051 §1/§3, the adversarial canon, the A2
proxy tests, campaign templates, and multiple v1.1 runs. The newer isolation
meaning appears in the conceptual governance-principles closeout and in
recent review language, but had not been integrated into a versioned gate
contract. The contradiction affected new-run classification only; rewriting
old runs would destroy their contractual truth. ADR 0053 resolves the
contradiction for v1.2 runs and leaves v1.1 historical semantics intact.
