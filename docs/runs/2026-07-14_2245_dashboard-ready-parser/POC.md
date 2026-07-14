# POC — Canonical READY reproduction

- Input: `## Global verdict` followed by
  `**\`READY — all seven campaign exit criteria evidenced\`**`.
- Current output: `UNKNOWN`.
- Expected output: `READY`.
- The defect is isolated to `extract_verdict()` and has no schema dependency.

**Verdict: GO**

```yaml
FINAL_STATUS: GO
hypothesis_validated: true
metric_observed: "canonical READY misparsed as UNKNOWN"
reproducible: true
```
