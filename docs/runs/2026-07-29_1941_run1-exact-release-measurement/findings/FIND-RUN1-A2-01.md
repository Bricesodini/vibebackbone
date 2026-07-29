---
finding_id: "RUN1-A2-01"
campaign_ref: "CAMP-2026-07-29-RUN1"
level: "A2"
severity: "S0"
confidence: "CONFIRMED"
state: "REMEDIATED"
discovered_by: "/root/run1_a2_review"
discovered_at: "2026-07-29T18:13:00Z"
surface: "tools/vbb-status-dashboard.py"
attack_class: "risk-masking"
---

# FIND-RUN1-A2-01

```yaml
id: "RUN1-A2-01"
summary: "Qualified Description header variants hid active P0/P1/P2 risks."
severity: "S0"
confidence: "CONFIRMED"
state: "REMEDIATED"
reproduction:
  setup: "Call production get_open_risks and measure_repository_health on a clean fixture."
  steps:
    - "Declare documented READY."
    - "Use Description & reopen trigger or Description and reopen triggers."
    - "Add an OPEN P0 row."
  expected: "The risk is parsed and measured readiness is BLOCKED."
  observed: "Before remediation risks=[] and measured READY."
  oracle: "Every Description-prefixed risk column preserves the active P0."
non_regression_lock:
  test_id: "test_qualified_description_header_variants_do_not_hide_risks"
  test_path: "tests/test_status_dashboard.py"
  fails_before: true
  passes_after: true
  witnessed_by: "PENDING_DISTINCT_A2_ACTOR"
  test_review: "FAIL"
  test_review_reviewer: "/root/run1_a2_review shares defender identity"
promotion:
  destination_1_canonical_test: "tests/test_status_dashboard.py"
  destination_2_integration_test: "NOT_APPLICABLE: deterministic parser/health unit boundary"
  destination_3_certification_gate: "tools/vbb-status-dashboard.py measured verdict"
  destination_4_checklist: "docs/REFERENCE/pre-merge-gate.md"
  destination_5_normative_rule: "NOT_APPLICABLE: no knowledge promotion in Run 1"
  destination_6_adversarial_corpus: "tests/adversarial_corpus/CORPUS-RUN1-A2-01.py"
```
