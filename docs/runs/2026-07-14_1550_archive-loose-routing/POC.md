# POC — Non-destructive archive move

## Hypothèse

La note peut quitter `docs/runs/` sans perte ni dépendance opérationnelle.

## Preuves avant exécution

- SHA-256 source :
  `d67c0460553cd1678e47fe67659abd041a5d2362412c3bb0e03b0d1ca110d8fd`.
- Destination absente.
- Les références actives sont AUDIT_STATUS et tests/documentation du filtre de
  fichiers loose ; les autres références appartiennent à des audits immuables.
- Le dashboard ignore déjà les fichiers, donc aucun comportement runtime ne
  dépend du chemin source.

## Verdict

**Verdict**: GO

```yaml
FINAL_STATUS: GO
hypothesis_validated: true
metric_observed: "one loose file; destination absent; stable SHA-256"
reproducible: true
```
