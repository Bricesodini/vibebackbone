---
finding_id: "RUN1-A2-CR-01"
campaign_ref: "CAMP-2026-07-29-RUN1"
level: "A2"
severity: "S1"
confidence: "CONFIRMED"
state: "REMEDIATED"
discovered_by: "/root/run1_a2_distinct"
surface: ".github/workflows/vbb-contracts.yml"
attack_class: "carrier-bypass"
---

# FIND-RUN1-A2-CR-01

```yaml
id: "RUN1-A2-CR-01"
summary: "GitHub release gates omitted the checked-out SHA."
severity: "S1"
confidence: "CONFIRMED"
state: "REMEDIATED"
reproduction:
  setup: "Inspect the Explicit changed-run gates step at b8d2209."
  steps: ["Observe both gate commands carry only run_dir and --strict."]
  expected: "Both commands carry --expected-commit with VBB_HEAD_SHA."
  observed: "The workflow could validate a closeout without exact SHA binding."
  oracle: "Both workflow commands use the same explicit run/SHA interface as local CI and P.R2."
non_regression_lock:
  test_id: "test_remote_release_binding_carries_checked_out_sha_to_both_gates"
  test_path: "tests/test_pre_merge_gate_5b.py"
  fails_before: true
  passes_after: true
  witnessed_by: "PENDING_DISTINCT_A2_ACTOR"
promotion:
  destination_1_canonical_test: "tests/test_pre_merge_gate_5b.py"
  destination_2_integration_test: ".github/workflows/vbb-contracts.yml"
  destination_3_certification_gate: "GitHub Explicit changed-run gates"
  destination_4_checklist: "docs/REFERENCE/pre-merge-gate.md"
  destination_5_normative_rule: "NOT_APPLICABLE: existing exact binding contract"
  destination_6_adversarial_corpus: "tests/adversarial_corpus/CORPUS-RUN1-A2-CR-01.py"
```
