# POC — Responsibility-first routing triggers

**Statut**: CONCLUDED  
**Date**: 2026-07-14  
**Liée à ADR**: `docs/adr/0032-responsibility-first-routing-consolidation.md`  
**Liée à RUN**: `docs/runs/2026-07-14_0830_weakpoint-responsibility-routing/`

## Hypothèse

Des déclencheurs contractuels plus précis peuvent porter le corpus de routage
de 3/8 à 8/8 sans fusionner de skills, retirer l'orchestrateur ou modifier
l'algorithme du routeur.

## Test (concret, exécutable)

```bash
# Charger tools/vbb-phase-router.py, étendre en mémoire les triggers des cinq
# contrats ciblés, puis appeler route_to_skill(..., strict=True) sur les huit
# cas consignés dans docs/WEAKPOINT_CONSOLIDATION_MEASUREMENT.md.
pytest tests/test_contract_lint.py -q
```

## Critère de réussite (mesurable)

GO si les huit intentions retournent le skill attendu avec `strict=True`, sans
changement d'identité ou d'output contract.

## Résultat observé

- **Baseline** : 3/8.
- **Simulation additive** : 8/8.
- **Erreurs d'ambiguïté après simulation** : 0.
- **Fusion/suppression de skills** : 0.

## Décision

- **Verdict** : GO
- **Justification** : le plus petit changement corrige le corpus complet sans
  dénaturer les responsabilités publiées.

## Bilan

Appliquer les cinq extensions de triggers et convertir le corpus en tests.

```yaml
FINAL_STATUS: GO
adr_link: docs/adr/0032-responsibility-first-routing-consolidation.md
hypothesis_validated: true
metric_observed: "8/8 strict routing fixtures"
metric_threshold: "8/8"
reproducible: true
verified_at: "2026-07-14T08:34:00+02:00"
verified_by: codex
```
