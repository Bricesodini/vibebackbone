---
template_id: "ADR"
version: "1.0"
---

# ADR — real-hypothesis-pocs

**Status**: PROPOSED
**Date**: 2026-07-15
**Route**: AUDIT
**Liée à POC**: `POC.md`

## Contexte

La première campagne a validé les formats mais pas leur efficacité sur des
artefacts réels. Cette run borne les trois validations restantes et accepte les
verdicts `PIVOT` ou `UNKNOWN` lorsque l'environnement ne permet pas une preuve.

## Décision provisoire

Utiliser des fixtures locales et des artefacts existants ; intégrer une
évolution seulement si son critère réel est atteint et si aucun doublon n'est
introduit.

## Alternatives rejetées

### Simuler uniquement les validateurs
- Rejetée : déjà fait dans la run précédente.

### Installer des outils réseau pour forcer un GO
- Rejetée : cela confond disponibilité d'environnement et validité du concept.

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: PROPOSED
decision_class: GOUVERNANCE
reversible: true
depends_on:
  - "POC.md"
blocks: []
supersedes: []
verified_at: "2026-07-15T11:00:00+02:00"
verified_by: "codex"
verified_method: "poc"
```
