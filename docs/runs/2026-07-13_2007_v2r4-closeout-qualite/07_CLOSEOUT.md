---
run_id: "2026-07-13_2007_v2r4-closeout-qualite"
phase: "07_CLOSEOUT"
kind: "CLOSEOUT"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-code"
started_at: "2026-07-13T18:25:00Z"
ended_at: "2026-07-13T18:35:00Z"
next_phase: null
artifacts_consumed:
  - "05_EXECUTION.md"
artifacts_produced:
  - "07_CLOSEOUT.md"
---

# 07_CLOSEOUT — v2r4-closeout-qualite (CLOSE-FINAL)

## Statut global

**READY** — run terminé, clôture `CLOSE-FINAL`. Roadmap V2 : 3/6 (R1, R3, R4).

## Résumé

Le closeout des chantiers devient le point de routage des audits qualité vers
le code fraîchement touché : passe scopée **déclenchée selon le risque**
(données/auth/sécurité/compliance/prod OU 4+ fichiers de code produit),
traçage obligatoire (`EXECUTED` / `SKIPPED (risque faible)` / `N/A (docs-only)`),
P0/P1 → runs de remédiation séparés. La règle de compaction de contexte est
canonisée dans SESSION_RULES : **40 % indicatif** (compactor + mini-handoff),
**75 % limite dure** avant toute nouvelle action. Couvre RB-2 et RB-4 ;
ADR-0029 ACCEPTED.

## Pre-merge gate (P.R2 — 5 vérifications canoniques)

Exécuté après rédaction de ce closeout — résultats dans la table d'évidence du
commit (exigence du hook commit-msg). Attendu : 5/5 PASS (aucun outil Python modifié).

## Passe qualité scopée (ADR-0029)

- **Décision** : `N/A (docs-only)`
- **Déclencheur évalué** : aucun critère atteint — le run modifie 1 prompt,
  1 template et 2 docs de gouvernance ; zéro fichier de code produit, pas de
  données/auth/prod. (Première application de la règle : à elle-même.)

## Décisions

- Déclencheur « selon risque » (réserve Brice) avec seuil aligné sur la route
  FAST-STANDARD (4+ fichiers de code produit) — révisable après V2-R5a.
- Skip jamais silencieux : la décision est un champ obligatoire du template.

## Points ouverts

- Calibration du déclencheur à valider sur le terrain → **V2-R5a** (audit trame,
  lecture seule) est le prochain run naturel ; **V2-R2** (portabilité + CCP)
  reste disponible en parallèle. V2-R6 (autonomie) a désormais ses deux
  prérequis (V2-R1 ✅, V2-R4 ✅).

## Risques résiduels

- Sur/sous-déclenchement du seuil : suivi via les sections « Passe qualité
  scopée » des prochains closeouts (données réelles).

## Handoff

Aucun (CLOSE-FINAL). Reprise : `docs/strategy/vbb-improvements-roadmap/03_PLAN_REDUCTION_V2.md` §2.
