# POC — Prompt surface inventory

## Hypothèse

Une table de quatre lignes peut clarifier ownership et precedence sans recopier
la matrice phase/contexte détaillée.

## Preuves avant exécution

- 7 fichiers canoniques dans `prompts/canonical/`.
- 25 prompts spécialisés à la racine, hors router.
- 1 router exécutable `t-p-vbb-phase-router.md`.
- 5 noms courts documentés, tous résolus vers un fichier existant.
- `ROUTER_MATRIX.md` contient déjà la décision détaillée par phase et contexte.

## Verdict

**Verdict**: GO

```yaml
FINAL_STATUS: GO
hypothesis_validated: true
metric_observed: "7 canonical; 25 specialized; 1 router; 5 valid aliases"
reproducible: true
```
