---
finding_id: "RUN1-A2-CR-03"
campaign_ref: "CAMP-2026-07-29-RUN1"
level: "A2"
severity: "S0"
confidence: "CONFIRMED"
state: "REMEDIATED"
discovered_by: "/root/run1_a2_distinct"
surface: "tools/vbb-status-dashboard.py"
attack_class: "risk-masking"
---

# FIND-RUN1-A2-CR-03

```yaml
id: "RUN1-A2-CR-03"
summary: "Canonical REOPENED risks were omitted from active release measurement."
severity: "S0"
confidence: "CONFIRMED"
state: "REMEDIATED"
reproduction:
  setup: "Declare documentary READY and a P0 risk with status REOPENED."
  steps: ["Extract active risks and combine documentary/measured verdicts."]
  expected: "The P0 is active and effective verdict is BLOCKED."
  observed: "At b8d2209 active risks were empty and READY remained possible."
  oracle: "All canonical non-terminal finding states are active; active P0/P1/P2 cannot yield READY."
non_regression_lock:
  test_id: "test_reopened_p0_is_active_and_forces_blocked"
  test_path: "tests/test_status_dashboard.py"
  fails_before: true
  passes_after: true
  witnessed_by: "PENDING_DISTINCT_A2_ACTOR"
promotion:
  destination_1_canonical_test: "tests/test_status_dashboard.py"
  destination_2_integration_test: "dashboard effective verdict"
  destination_3_certification_gate: "tools/vbb-status-dashboard.py --strict"
  destination_4_checklist: "docs/REFERENCE/pre-merge-gate.md"
  destination_5_normative_rule: "NOT_APPLICABLE: lifecycle authority already exists"
  destination_6_adversarial_corpus: "tests/adversarial_corpus/CORPUS-RUN1-A2-CR-03.py"
```
