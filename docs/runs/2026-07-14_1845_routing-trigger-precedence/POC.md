# POC — Routing collision characterization

## Baseline

- 64 contracts scanned.
- Six exact case-insensitive duplicate triggers found.
- Strict router ambiguity is based on a top-score gap below 0.5.

## Hypothesis

Unique generic owners plus qualified secondary triggers can make all twelve
representative intents deterministic without changing router scoring.

**Verdict: GO**

```yaml
FINAL_STATUS: GO
hypothesis_validated: true
metric_observed: "six exact collisions; zero other duplicate triggers"
reproducible: true
```
