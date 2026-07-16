---
template_id: "ADR"
version: "1.0"
---

# ADR — hypothesis-poc-campaign

**Status**: PROPOSED
**Date**: 2026-07-15
**Route**: AUDIT
**Décideurs**: mainteneur Vibe Backbone
**Liée à POC**: `docs/runs/2026-07-15_1015_hypothesis-poc/POC.md`

## Contexte

Le contre-audit suggère dix évolutions possibles. Le dépôt contient déjà une
partie des mécanismes proposés, notamment les niveaux de preuve et les règles
de limitation. Une campagne de POC est nécessaire avant toute évolution du cœur.

## Décision provisoire

Exécuter un POC isolé par hypothèse, conserver les résultats dans cette run,
et n'intégrer qu'après un verdict GO explicite fondé sur un critère mesurable.

## Alternatives rejetées

### Intégration immédiate
- Rejetée : risque de dupliquer des mécanismes déjà présents.

### Rejet théorique sans test
- Rejetée : certaines lacunes sont opérationnelles et non déductibles de la seule lecture.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Sur-cadrage | moyenne | moyen | POC bornés et critères de coût/valeur |
| Faux positif | moyenne | moyen | test discriminant ou verdict UNKNOWN |
| Propagation incomplète | faible | élevé | revue Core/distributions avant intégration |

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: PROPOSED
decision_class: GOUVERNANCE
reversible: true
depends_on:
  - "docs/runs/2026-07-15_1015_hypothesis-poc/POC.md"
blocks: []
supersedes: []
verified_at: "2026-07-15T10:15:00+02:00"
verified_by: "codex"
verified_method: "poc"
```
