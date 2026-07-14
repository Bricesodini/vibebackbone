---
run_id: "2026-07-14_1700_prompt-english-migration"
phase: "05_EXECUTION"
voie: "STRUCTUREE"
status: "READY"
agent: "codex-controller + translators"
started_at: "2026-07-14T17:05:00+02:00"
ended_at: "2026-07-14T17:25:00+02:00"
next_phase: "06_REVIEW"
artifacts_consumed:
  - "04_PLAN.md"
  - "POC.md"
  - "INTEGRATION_GATE.md"
artifacts_produced:
  - "05_EXECUTION.md"
---

# 05_EXECUTION — Prompt English migration

## Result

- Reconciled local `SESSION.md` with the independent review and current run.
- Translated 18 prompt files in place: seven canonical, ten specialized and one
  session entrypoint.
- Translated embedded human templates and generic placeholders while preserving
  route/risk/verdict/status enums, real commands, paths, artifact names, links
  and numeric thresholds.
- Added three deterministic language regression tests with controlled-positive
  detection and an explicit enum allowlist.
- Recorded ADR 0036 and Core propagation to all four distributions.

## Test audit

| Assertion | Verification | Result |
|---|---|---|
| Detector catches French prose | controlled unit case | PASS, 4/4 markers |
| Active prompt prose is English | prompt language tests | PASS, zero findings |
| Accented tokens are approved enums | full-corpus accent scan | PASS |
| Prompt paths stable | inventory against HEAD | PASS, 33/33 |
| Link destinations stable | per-file before/after comparison | PASS, 18/18 |
| Numeric semantics stable | per-file comparison + manual review | PASS; two `1`→`one` prose translations only |
| Surface inventory stable | canonical/specialized/router/alias checks | PASS, 7/25/1/5 |

## Distribution impact

Pi, OpenCode, Codex and Claude Code inherit the English Core prompts. No adapter,
alias, installer path or installed provider state changed.
