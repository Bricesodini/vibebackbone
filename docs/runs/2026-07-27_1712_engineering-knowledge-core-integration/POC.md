# POC — Approved knowledge-governance compatibility

**Statut**: CONCLUDED
**Date**: 2026-07-27
**Liée à ADR**: `docs/adr/0049-engineering-knowledge-governance.md`
**Liée à RUN**: `docs/runs/2026-07-27_1712_engineering-knowledge-core-integration/`

## Hypothèse

The accepted design can preserve historical loop closure while making
Knowledge Harvest mandatory for runs created after the integration cutover.

## Test

```bash
python tools/vbb-loop-closure-check.py \
  2026-07-15_1100_real-pocs --strict
python tools/vbb-loop-closure-check.py \
  2026-07-27_1612_engineering-knowledge-governance --strict
```

## Critère de réussite

Both pre-cutover runs remain `PASS`; the integration test suite must later
prove that post-cutover closeouts without a valid harvest disposition fail.

## Résultat observé

Both pre-cutover reference runs pass before integration. The post-cutover
negative and positive fixtures remain required in execution Run 02.

## Décision

- **Verdict**: GO
- **Justification**: historical compatibility is preserved at baseline and the
  enforcement acceptance criterion is explicit.

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: GO
adr_link: docs/adr/0049-engineering-knowledge-governance.md
hypothesis_validated: partial
metric_observed: "2/2 pre-cutover runs PASS"
metric_threshold: "2/2 pre-cutover runs PASS; post-cutover fixtures pending"
reproducible: true
verified_at: "2026-07-27T15:16:00Z"
verified_by: "codex"
```
