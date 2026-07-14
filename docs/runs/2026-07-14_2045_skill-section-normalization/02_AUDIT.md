---
run_id: "2026-07-14_2045_skill-section-normalization"
phase: "02_AUDIT"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T20:47:00+02:00"
ended_at: "2026-07-14T20:52:00+02:00"
next_phase: "03_DECISION"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "02_AUDIT.md"
  - "../../audits/impact-analysis-skill-section-normalization-20260714-2045.md"
---

# 02_AUDIT — Skill section normalization

## Evidence

Exact scan of the mandatory headings identifies the same twelve skills as the
independent audit: five use equivalent combined headings and seven compact/tool
skills omit structural wrappers. Every other catalog skill already has all
seven headings.

Canonical headings:

1. `ROLE & POSTURE`
2. `INPUT CONTRACT`
3. `BLOCKING CONDITIONS`
4. `SCOPE`
5. `PROCESS`
6. `OUTPUT CONTRACT`
7. `VERDICT RULES`

```yaml
FINAL_STATUS:
  verdict: PARTIAL
  tests_run:
    - "64-skill exact heading inventory"
  tests_missing: []
  risks:
    - "twelve layout variants"
  open_points:
    - "normalize five equivalents and seven wrappers"
```
