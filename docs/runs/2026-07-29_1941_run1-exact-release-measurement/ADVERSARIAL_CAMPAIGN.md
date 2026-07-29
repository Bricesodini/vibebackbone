---
campaign_id: "CAMP-2026-07-29-RUN1"
subject: "Run 1 exact release measurement implementation"
scope: "RR-BK-02, RR-BK-03 and exact-subject portion of F9"
level: "A2"
attacker_identity:
  agent: "/root/run1_a2_review (Codex sub-agent)"
  llm: "gpt-5"
  provider: "openai"
  system_prompt_version: "codex-desktop-2026-07-29"
corpus_version: "1.2.0"
started_at: "2026-07-29T18:10:00Z"
ended_at: "2026-07-29T18:24:00Z"
actor: "/root/run1_a2_review"
exploration_performed: true
---

# Adversarial Campaign — Run 1

## 1. Declared surface

```yaml
surfaces_declared:
  - "tools/vbb_run_resolution.py"
  - "tools/vbb-adversarial-gate.py"
  - "tools/vbb-loop-closure-check.py"
  - "tools/vbb-status-dashboard.py"
  - "scripts/vbb-ci-local.sh"
  - ".github/workflows/vbb-contracts.yml"
```

## 2. Attack-surface classes

```yaml
attack_classes:
  - name: "subject substitution"
    description: "Validate a run or SHA other than the declared subject."
    techniques:
      - "future latest-run selection"
      - "bare ID versus path divergence"
      - "invented full SHA"
      - "external run directory"
    oracles:
      - "exact mode returns non-zero unless canonical run and real Git commit agree"
  - name: "risk masking"
    description: "Hide an open P0/P1/P2 from measured readiness."
    techniques:
      - "qualified description-header punctuation and plural drift"
      - "documented READY with active risk"
    oracles:
      - "risk remains visible and effective verdict is not READY"
  - name: "carrier bypass"
    description: "Obtain release-looking CI evidence without a complete subject."
    techniques:
      - "half-declared local subject"
      - "implicit future run in remote CI"
    oracles:
      - "local CI fails or skips honestly; remote CI uses explicit changed runs"
```

## 3. Depth / effort bound

```yaml
depth_bound:
  total_effort_hours: "1"
  parallel_actors: "1"
  techniques_planned: "10"
  techniques_executed: "13"
stop_criteria: "All three attack classes exercised once after counter-proof, or one unresolved S0/S1 remains."
```

## 4. Surfaces unexplored

```yaml
surfaces_unexplored:
  - "fresh-clone execution of the edited GitHub Actions workflow"
  - "real tag or release publication workflow"
  - "risk-table mutations that remove the Description prefix entirely"
```

## 5. Findings

```yaml
findings:
  - finding_ref: "RUN1-A2-01"
    summary: "Qualified description variants hid active risks"
    severity: "S0"
    confidence: "CONFIRMED"
    state: "REMEDIATED"
  - finding_ref: "RUN1-A2-02"
    summary: "Invented full SHA satisfied textual binding"
    severity: "S1"
    confidence: "CONFIRMED"
    state: "REMEDIATED"
  - finding_ref: "RUN1-A2-03"
    summary: "External directory could satisfy adversarial exact mode"
    severity: "S1"
    confidence: "CONFIRMED"
    state: "REMEDIATED"
```

All three fails-before cases now pass-after. They remain non-terminal because
the counter-proof actor shares the implementer's declared Codex/GPT-5/OpenAI
identity and therefore cannot supply the required independent A2 witness.

## 6. Residual uncertainty

```yaml
residual_uncertainty: |
  The scoped bypasses were reproduced and remediated, but no distinct provider
  or human actor verified the final state. Fresh remote workflow execution and
  real release/tag behavior were not exercised.
```

## 7. Verdict

```yaml
verdict: "FINDINGS_OPEN"
non_claim: |
  No PASS_ADVERSARIAL is claimed. The attack task was separated, but attacker
  and defender disclose the same Codex/GPT-5/OpenAI identity. The counter-proof
  is useful technical evidence, not independent A2 assurance.
```

## History

```yaml
history:
  - finding_ref: "RUN1-A2-01"
    transitions:
      - {from_state: "DETECTED", to_state: "CLASSIFIED", at: "2026-07-29T18:13:00Z", actor: "/root/run1_a2_review"}
      - {from_state: "CLASSIFIED", to_state: "REMEDIATION_IN_PROGRESS", at: "2026-07-29T18:16:00Z", actor: "codex"}
      - {from_state: "REMEDIATION_IN_PROGRESS", to_state: "REMEDIATED", at: "2026-07-29T18:22:00Z", actor: "codex"}
  - finding_ref: "RUN1-A2-02"
    transitions:
      - {from_state: "DETECTED", to_state: "CLASSIFIED", at: "2026-07-29T18:13:00Z", actor: "/root/run1_a2_review"}
      - {from_state: "CLASSIFIED", to_state: "REMEDIATION_IN_PROGRESS", at: "2026-07-29T18:16:00Z", actor: "codex"}
      - {from_state: "REMEDIATION_IN_PROGRESS", to_state: "REMEDIATED", at: "2026-07-29T18:22:00Z", actor: "codex"}
  - finding_ref: "RUN1-A2-03"
    transitions:
      - {from_state: "DETECTED", to_state: "CLASSIFIED", at: "2026-07-29T18:13:00Z", actor: "/root/run1_a2_review"}
      - {from_state: "CLASSIFIED", to_state: "REMEDIATION_IN_PROGRESS", at: "2026-07-29T18:16:00Z", actor: "codex"}
      - {from_state: "REMEDIATION_IN_PROGRESS", to_state: "REMEDIATED", at: "2026-07-29T18:22:00Z", actor: "codex"}
```
