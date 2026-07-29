---
finding_id: "RUN1-A2-02"
campaign_ref: "CAMP-2026-07-29-RUN1"
level: "A2"
severity: "S1"
confidence: "CONFIRMED"
state: "REMEDIATED"
discovered_by: "/root/run1_a2_review"
discovered_at: "2026-07-29T18:13:00Z"
surface: "tools/vbb_run_resolution.py"
attack_class: "subject-substitution"
---

# FIND-RUN1-A2-02

```yaml
id: "RUN1-A2-02"
summary: "A matching but non-existent 40-hex SHA satisfied textual binding."
severity: "S1"
confidence: "CONFIRMED"
state: "REMEDIATED"
reproduction:
  setup: "Bind a closeout and expected-commit to forty 'a' characters."
  steps:
    - "Run the exact-subject verifier."
    - "Run git cat-file on the same value."
  expected: "Binding fails when the value is not a Git commit object."
  observed: "Before remediation binding passed while git cat-file returned 128."
  oracle: "verify_bound_subject requires git cat-file -e SHA^{commit}."
non_regression_lock:
  test_id: "test_bound_subject_rejects_invented_full_sha"
  test_path: "tests/test_run_resolution.py"
  fails_before: true
  passes_after: true
  witnessed_by: "PENDING_DISTINCT_A2_ACTOR"
  test_review: "FAIL"
  test_review_reviewer: "/root/run1_a2_review shares defender identity"
promotion:
  destination_1_canonical_test: "tests/test_run_resolution.py"
  destination_2_integration_test: "tests/test_loop_closure.py and tests/test_adversarial_gate_yaml_unwrap.py"
  destination_3_certification_gate: "tools/vbb-loop-closure-check.py and tools/vbb-adversarial-gate.py"
  destination_4_checklist: "docs/REFERENCE/pre-merge-gate.md exact release binding"
  destination_5_normative_rule: "NOT_APPLICABLE: existing bound_to contract"
  destination_6_adversarial_corpus: "tests/adversarial_corpus/CORPUS-RUN1-A2-02.py"
```
