---
finding_id: "RUN1-A2-CR-02"
campaign_ref: "CAMP-2026-07-29-RUN1"
level: "A2"
severity: "S0"
confidence: "CONFIRMED"
state: "REMEDIATED"
discovered_by: "/root/run1_a2_distinct"
surface: "tools/vbb_run_resolution.py"
attack_class: "subject-substitution"
---

# FIND-RUN1-A2-CR-02

```yaml
id: "RUN1-A2-CR-02"
summary: "A valid historical commit could certify a different checked-out HEAD."
severity: "S0"
confidence: "CONFIRMED"
state: "REMEDIATED"
reproduction:
  setup: "Bind a run to an old valid commit, then advance HEAD."
  steps:
    - "Resolve the old binding historically."
    - "Invoke certification for the old commit while HEAD is newer."
  expected: "Historical lookup passes; certification fails on HEAD mismatch."
  observed: "At b8d2209 the only verifier accepted the old commit."
  oracle: "metadata commit == expected commit == evaluated HEAD in certification mode."
non_regression_lock:
  test_id: "test_certification_rejects_historical_commit_when_head_differs"
  test_path: "tests/test_run_resolution.py"
  fails_before: true
  passes_after: true
  witnessed_by: "PENDING_DISTINCT_A2_ACTOR"
promotion:
  destination_1_canonical_test: "tests/test_run_resolution.py"
  destination_2_integration_test: "both release gates call verify_certification_subject"
  destination_3_certification_gate: "tools/vbb-loop-closure-check.py and tools/vbb-adversarial-gate.py"
  destination_4_checklist: "docs/REFERENCE/pre-merge-gate.md"
  destination_5_normative_rule: "NOT_APPLICABLE: existing exact binding contract"
  destination_6_adversarial_corpus: "tests/adversarial_corpus/CORPUS-RUN1-A2-CR-02.py"
```
