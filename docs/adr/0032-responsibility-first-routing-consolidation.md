# ADR — 0032-responsibility-first-routing-consolidation

**Status**: ACCEPTED
**Date**: 2026-07-14
**Route**: STRUCTUREE
**Décideurs**: Brice (`go`, 2026-07-14), Codex (formalisation)
**Liée à**: ADR 0030 (boot-set diet), ADR 0027 (gates fiables)
**Liée à POC**: `docs/runs/2026-07-14_0830_weakpoint-responsibility-routing/POC.md`

## Contexte

Le plan `docs/WEAKPOINT_CONSOLIDATION_PLAN.md` propose de réduire 64 skills à
environ 15–20, d'aplatir l'orchestration, de durcir deux gates et de documenter
un resync consommateur. La revue du 14 juillet confirme une charge de routage,
mais montre que le nombre de références textuelles ne mesure pas l'usage, que
les skills proposés à la fusion ont des contrats distincts, et que TER-001 a
déjà un POC `NO-GO` en l'absence de frontière d'ownership.

Un corpus reproductible de huit intentions mesure le routeur courant à 3/8.
Une simulation limitée à des déclencheurs contractuels plus précis atteint 8/8
sans fusion, sans suppression et sans changement d'algorithme.

## Décision

La consolidation suivra une approche **responsibility-first** : préserver les
skills spécialisés et l'orchestrateur obligatoire, documenter leurs frontières,
et corriger uniquement les déclencheurs contractuels prouvés par le corpus.

- Aucun skill n'est fusionné, archivé ou retiré dans ce run.
- `vibebackbone` reste le premier point de routage ; ENGINE_ONLY reste inchangé.
- Le routeur reçoit des tests top-1 sur le corpus avant toute extension.
- Le credentials gate devient un chantier AUDIT séparé ; ce run ne prétend pas
  clore P0-5-D.
- TER-001 reste différé jusqu'à une décision d'ownership/generated-file.

## Conséquences

### Positives
- Réduction mesurable des erreurs de routage sans casser les contrats publiés.
- Séparation audit/écriture préservée pour les skills code-doc.
- Compatibilité des quatre distributions maintenue par changement Core additif.

### Négatives / coûts
- Le catalogue reste à 64 skills.
- Le corpus initial ne couvre que huit intentions et devra grandir avec l'usage.

### Neutres
- Aucun changement de comportement des consommateurs existants.
- Aucun secret scanner n'est ajouté dans ce run.

## Alternatives rejetées (≥ 2)

### Alternative A — Fusionner les détecteurs en skills multimodes
- **Description** : remplacer six skills spécialisés par deux skills larges.
- **Pourquoi rejetée** : responsabilités, gates, artefacts et effets d'écriture
  différents ; aucune preuve de meilleur routage.

### Alternative B — Aplatir tous les prompts vers des workers directs
- **Description** : supprimer l'orchestrateur hors ENGINE_ONLY.
- **Pourquoi rejetée** : retire le point de triage commun sans corpus démontrant
  une non-régression des routes et escalades.

### Alternative C — Ne rien changer
- **Description** : conserver les contrats et déclencheurs actuels.
- **Pourquoi rejetée** : le corpus reproductible ne route correctement que 3/8
  intentions représentatives.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Sur-ajustement au corpus | moyenne | moyen | tests explicites et extension incrémentale |
| Nouveau chevauchement de triggers | faible | moyen | routeur `strict=True` dans les tests |
| Dérive distributions | faible | moyen | contrôle des quatre adaptateurs et CI locale |

## Hypothèses

- Les déclencheurs des `CONTRACT.yaml` sont la surface de correction la plus
  petite compatible avec l'architecture actuelle.
- Si l'usage réel montre que des contrats restent indiscernables, une nouvelle
  ADR devra réexaminer agrégation ou fusion.

## Références

- Plan évalué : `docs/WEAKPOINT_CONSOLIDATION_PLAN.md`
- État actif : `docs/AUDIT_STATUS.md` (`DOC-001`, `DOC-002`, `TER-001`)
- POC : `docs/runs/2026-07-14_0830_weakpoint-responsibility-routing/POC.md`

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: ARCHITECTURE
reversible: true
depends_on:
  - docs/runs/2026-07-14_0830_weakpoint-responsibility-routing/POC.md
blocks: []
supersedes: []
verified_at: "2026-07-14T08:30:47+02:00"
verified_by: "Brice + Codex"
verified_method: "human-review + reproducible routing POC"
```
