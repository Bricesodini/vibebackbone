---
template_id: "POC"
version: "1.0"
lane_eligible:
  - "AUDIT"
---

# POC — real-hypothesis-pocs

**Statut**: IN_PROGRESS
**Date**: 2026-07-15
**Liée à ADR**: `ADR.md`

## Hypothèse

Nous supposons que les trois propositions restantes produisent un gain
observable sur des fixtures et artefacts réels sans élargir le périmètre.

## Tests

1. H-003 : détecter le type de projet, sélectionner son validateur d'autorité,
   puis exécuter le build/start/smoke disponible pour Next.js, Docker et API.
2. H-005/H-006 : sélectionner quatre findings existants, tenter leur
   reproduction minimale, séparer validation primaire et secondaires, mesurer
   le périmètre et le coût.
3. H-007 : scanner chemins et contenus historiques, classer les signaux et
   vérifier l'absence de suppression automatique.

## Critères de réussite

- H-003 : au moins deux familles de projets démontrent une détection que les
  validateurs génériques ne fournissent pas.
- H-005/H-006 : quatre findings traités, coût inférieur à 50 % d'un audit
  complet, aucun secondaire transformé en chantier automatique.
- H-007 : signaux détectés et classés, zéro suppression, faux positifs visibles.

## Résultat observé

Le runner réel a produit :

- H-003 : API smoke PASS ; Next CLI absente ; Docker daemon indisponible ;
  FastAPI importable mais démarrage incompatible.
- H-005 : quatre findings réels sélectionnés, mais coût non comparable.
- H-006 : un secondaire conservé en backlog, aucune action automatique.
- H-007 : 1 091 chemins scannés, 0 nom suspect, 5 faux positifs classés,
  0 suppression.

## Gate d'exécution

**Verdict**: GO — ce verdict autorise l'exécution des tests bornés ; il ne
préjuge pas du verdict final des hypothèses.

## Décision

À compléter dans `02_AUDIT_REPORT.md`.

## Décision intermédiaire

**Verdict**: PIVOT — aucun critère complet ne justifie encore une intégration du
cœur ; les limites d'environnement et de corpus sont explicites dans le rapport.
