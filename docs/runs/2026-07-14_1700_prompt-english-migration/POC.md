# POC — Prompt migration inventory

## Baseline

- 33 total prompt files.
- 18 affected by unambiguous French prose markers.
- 15 already English.
- Surface inventory: 7 canonical, 25 specialized, 1 router, 5 valid aliases.

## Safety hypothesis

In-place translation is safe if file paths, executable tokens, link destinations,
machine enums, numerical thresholds and surface counts remain stable, embedded
human templates become English, and full tests pass.

**Verdict: GO**

```yaml
FINAL_STATUS: GO
hypothesis_validated: true
metric_observed: "18 affected / 33 total"
reproducible: true
```
