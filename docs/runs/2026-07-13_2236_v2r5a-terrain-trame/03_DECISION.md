---
run_id: "2026-07-13_2236_v2r5a-terrain-trame"
phase: "03_DECISION"
voie: "AUDIT"
status: "READY"
agent: "claude-code"
started_at: "2026-07-13T21:10:00Z"
ended_at: "2026-07-13T21:15:00Z"
next_phase: "07_CLOSEOUT"
artifacts_consumed:
  - "02_AUDIT.md"
artifacts_produced:
  - "03_DECISION.md"
---

# 03_DECISION — v2r5a-terrain-trame

## Décisions

1. **POC verdict GO entériné** : la grammaire VBB est suivie par un agent non
   supervisé en conditions réelles (6/8 PASS, 0 NO-GO). Le protocole scopé
   (ADR-0028) et le dispositif expérimentateur/sujet sont validés terrain.
2. **TER-001 (P1, dérive Core→consommateurs) → nouveau chantier prioritaire du
   backlog V2** : « refresh de gouvernance des projets consommateurs » —
   mécanisme de mise à jour des fichiers de gouvernance embarqués (PILOTAGE,
   closeout minima, étape 4bis, règle 40/75) dans les repos déjà initialisés.
   S'appuie sur ADR-0012 (codegen, design existant). À arbitrer avec Brice :
   avant ou après V2-R2/R6.
3. **TER-002/003 (protocole scopé) → micro-run FAST-MINIMAL différé** : ajouter
   au protocole un gabarit de finding (montrant le tag `scope:`) et une phrase
   sur le cas mono-scope (registre non requis si scope unique imposé). ≤2 fichiers.
4. **Remédiation trame** : les 2 commits restent **locaux au clone sandbox**.
   L'application au vrai dépôt trame (report des findings JAN-01…08 et/ou push)
   = V2-R5b, **GO Brice dédié requis** — conformément au plan V2.
5. Les findings JAN-01…08 produits par le sujet constituent l'entrée de V2-R5b
   (sélection à faire par Brice ; JAN-01 structurel = décision produit).

## Options rejetées

- Pousser les commits du sandbox vers trame : hors mandat V2-R5a (lecture seule
  sur le vrai dépôt), et la sélection des findings appartient à Brice.
- Corriger TER-002/003 en séance : ADR-0026 — pas de patch pendant l'audit.
