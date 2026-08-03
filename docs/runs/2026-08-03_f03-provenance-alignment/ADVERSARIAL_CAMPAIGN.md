---
campaign_id: "CAMP-2026-08-03-F03"
subject: "F-03 ADR-0051 / ADR-0053 provenance alignment"
scope: "ADR provenance and Pi SYSTEM representation only"
level: "A2"
attacker_identity:
  agent: "Volta"
  llm: "independent fresh-context reviewer"
  system_prompt_version: "disclosed in session metadata"
corpus_version: "not-applicable-bounded-provenance-review"
started_at: "2026-08-03T00:00:00Z"
ended_at: "2026-08-03T00:00:00Z"
actor: "Volta"
exploration_performed: true
---

# Adversarial Campaign — F-03

## Declared surface

```yaml
surfaces_declared:
  - "docs/adr/0051-adversarial-assurance-dimension.md"
  - "docs/adr/0053-a2-a3-assurance-alignment.md"
  - "docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md"
  - "distributions/pi/SYSTEM.md"
  - "SYSTEM.md"
```

## Attack-surface classes

```yaml
attack_classes:
  - name: "provenance contradiction"
    description: "Search for retroactive reinterpretation or wrong ADR authority."
    techniques: ["targeted text review", "cross-reference comparison"]
    oracles: ["ADR-0051 historical", "ADR-0053 v1.2", "governance adr field"]
  - name: "projection drift"
    description: "Check source/projection identity and runtime-rule consistency."
    techniques: ["symlink resolution", "byte comparison", "targeted text review"]
    oracles: ["SYSTEM resolves to Pi source", "v1.2 semantics preserved"]
```

## Depth / effort bound

```yaml
depth_bound:
  total_effort_hours: "1"
  parallel_actors: "1"
  techniques_planned: "5"
  techniques_executed: "5"
stop_criteria: "Stop after the declared surfaces and provenance assertions are checked."
```

## Surfaces unexplored

```yaml
surfaces_unexplored:
  - "Pi runtime déployé — aucune identité de déploiement observable."
  - "Adoption canonique et intégration main — explicitement hors périmètre."
```

## Findings

```yaml
findings:
  - finding_ref: "F03-A2-01"
    summary: "SYSTEM retains a residual distinct-actor proxy obligation in the v1.2 path."
    severity: "S1"
    confidence: "CONFIRMED"
    state: "CLASSIFIED"
  - finding_ref: "F03-A2-02"
    summary: "SYSTEM updated metadata predates the v1.2 alignment it contains."
    severity: "S1"
    confidence: "CONFIRMED"
    state: "CLASSIFIED"
```

## Verdict

```yaml
verdict: "FAIL_ADVERSARIAL"
non_claim: |
  This bounded campaign identified two confirmed findings in the declared
  provenance surface. It does not certify the runtime, adoption, or any
  unexplored surface.
```
