---
finding_id: "RUN1-A2-03"
campaign_ref: "CAMP-2026-07-29-RUN1"
level: "A2"
severity: "S1"
confidence: "CONFIRMED"
state: "REMEDIATED"
discovered_by: "/root/run1_a2_review"
discovered_at: "2026-07-29T18:13:00Z"
surface: "tools/vbb-adversarial-gate.py"
attack_class: "subject-substitution"
---

# FIND-RUN1-A2-03

```yaml
id: "RUN1-A2-03"
summary: "Adversarial exact mode accepted a run outside the declared runs directory."
severity: "S1"
confidence: "CONFIRMED"
state: "REMEDIATED"
reproduction:
  setup: "Create an external run directory with matching bound_to fields."
  steps:
    - "Invoke the gate with the external path and --expected-commit."
  expected: "Exact mode rejects a subject outside the declared runs directory."
  observed: "Before remediation the real gate passed the external pytest directory."
  oracle: "Expected-commit mode uses resolve_explicit_run against the declared runs directory."
non_regression_lock:
  test_id: "test_expected_commit_rejects_external_run_directory"
  test_path: "tests/test_adversarial_gate_yaml_unwrap.py"
  fails_before: true
  passes_after: true
  witnessed_by: "PENDING_DISTINCT_A2_ACTOR"
  test_review: "FAIL"
  test_review_reviewer: "/root/run1_a2_review shares defender identity"
promotion:
  destination_1_canonical_test: "tests/test_adversarial_gate_yaml_unwrap.py"
  destination_2_integration_test: "NOT_APPLICABLE: real CLI subprocess test is canonical"
  destination_3_certification_gate: "tools/vbb-adversarial-gate.py exact mode"
  destination_4_checklist: "docs/REFERENCE/pre-merge-gate.md"
  destination_5_normative_rule: "NOT_APPLICABLE: existing exact-subject contract"
  destination_6_adversarial_corpus: "tests/adversarial_corpus/CORPUS-RUN1-A2-03.py"
```
