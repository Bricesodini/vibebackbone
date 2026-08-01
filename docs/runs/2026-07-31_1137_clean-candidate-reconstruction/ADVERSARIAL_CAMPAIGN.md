---
run_id: "2026-07-31_1137_clean-candidate-reconstruction"
phase: "ADVERSARIAL_CAMPAIGN"
adversarial_level: "A2"
corpus_version: "v1.2.0"
status: "FINDINGS_OPEN"
---

# A2 campaign — exact-subject and corpus reconstruction

```yaml
attacker_identity:
  agent: "Codex adversarial proxy"
  llm: "GPT-5"
  system_prompt_version: "codex-desktop-2026-07-31"
defender_identity:
  agent: "Codex"
  llm: "GPT-5"
  provider: "OpenAI"
  system_prompt_version: "codex-desktop-2026-07-31"
  session: "current-task"
a2_proxy_mode:
  enabled: true
  limitations: ["Same provider and no external human reviewer; no certification claim."]
surfaces_declared:
  - "tools/vbb_run_resolution.py"
  - "tools/vbb-loop-closure-check.py"
  - "tools/vbb-adversarial-gate.py"
  - "tools/vbb-status-dashboard.py"
  - "tests/adversarial_corpus/"
surfaces_unexplored:
  - "remote CI workflows"
  - "Pi re-pilot"
  - "independent external review"
findings:
  - id: "A2-GP-01"
    severity: "S1"
    confidence: "CONFIRMED"
    state: "CLASSIFIED"
  - id: "A2-GP-02"
    severity: "S1"
    confidence: "CONFIRMED"
    state: "CLASSIFIED"
  - id: "A2-GP-03"
    severity: "S1"
    confidence: "CONFIRMED"
    state: "CLASSIFIED"
  - id: "FIND-RR-BK-05"
    severity: "S1"
    confidence: "CONFIRMED"
    state: "CLOSED_REMEDIATED"
verdict: "FINDINGS_OPEN"
```

The three historical conceptual findings remain `BEHAVIOUR_PIN`s and are not
claimed remediated. The RR-BK-05 measurement lock is active. This campaign is
technical evidence, not independent certification.
