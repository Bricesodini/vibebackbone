# POC — Consumer governance refresh with existing initializer

**Statut**: CONCLUDED  
**Date**: 2026-07-14  
**Liée à ADR**: `docs/adr/0012-codegen-agents-claudemd.md`  
**Liée à RUN**: `docs/runs/2026-07-14_0721_consumer-refresh-poc/`

## Hypothèse

The existing initializer can refresh VBB-owned material repeatedly while
preserving customized project truth and domain files.

## Test (concret, exécutable)

```bash
tmp=$(mktemp -d /tmp/vbb-consumer-refresh.XXXXXX)
python tools/vbb-project-init.py --target-dir "$tmp" --project-name ConsumerPOC
# Add unique sentinels to docs/{CONTEXT,AUDIT_STATUS,ARCHITECTURE}.md and a domain file.
python tools/vbb-project-init.py --target-dir "$tmp" --overwrite --backup --dry-run
python tools/vbb-project-init.py --target-dir "$tmp" --project-name ConsumerPOC
python tools/vbb-project-init.py --target-dir "$tmp" --overwrite --backup
python tools/vbb-project-init.py --target-dir "$tmp" --overwrite --backup
rg -n 'CUSTOM_.*SENTINEL' "$tmp"
```

## Critère de réussite (mesurable)

GO only if all three project-truth sentinels remain available after two
refreshes, the domain sentinel stays untouched, and dry-run matches writes.

## Résultat observé

- **Date d'exécution**: 2026-07-14 07:21 Europe/Paris.
- **Dry-run**: correctly announced 21 overwrites and wrote nothing.
- **Default mode**: skipped all 22 existing targets and preserved all sentinels.
- **First overwrite+backup**: removed three sentinels from live files; backups
  retained them; domain sentinel survived.
- **Second overwrite+backup**: replaced those backups; only the domain sentinel
  remained.
- **Métrique**: project-truth sentinels surviving after two refreshes = 0/3
  (required 3/3); domain sentinel = 1/1.

## Décision

- **Verdict**: NO-GO
- **Justification**: current options are safe for bootstrap/idempotent skip, not
  for refresh; repeated overwrite destroys the only customized backup.

## Bilan

Keep `vbb-project-init.py` bootstrap-only. A safe refresh requires an explicit
ownership/versioning decision or generated-file boundary, which exceeds this
run's hard stops; TER-001 is deferred without implementation.

```yaml
FINAL_STATUS: NO-GO
adr_link: docs/adr/0012-codegen-agents-claudemd.md
hypothesis_validated: false
metric_observed: "0/3 project-truth sentinels after two refreshes"
metric_threshold: "3/3"
reproducible: true
verified_at: "2026-07-14T07:21:00+02:00"
verified_by: codex
```
