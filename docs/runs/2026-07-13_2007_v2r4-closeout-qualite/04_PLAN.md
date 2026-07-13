---
run_id: "2026-07-13_2007_v2r4-closeout-qualite"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-code"
started_at: "2026-07-13T18:12:00Z"
ended_at: "2026-07-13T18:16:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "docs/adr/0029-risk-triggered-closeout-quality-pass.md (ACCEPTED)"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — v2r4-closeout-qualite

## Objectif

Passe qualité scopée au closeout, déclenchée selon le risque (RB-2) + règle de
compaction 40 % indicatif / 75 % limite dure dans SESSION_RULES.md (RB-4).
Réf. : ADR-0029 (ACCEPTED).

## Pré-conditions

- Gate levé : `can_code_start=true`, ADR-0029 par liaison stricte, POC non requise.
- V2-R3 livré : `scope` et `docs/REFERENCE/scoped-audit-protocol.md` existent.

## Étapes ordonnées

| # | Action | Fichiers |
|---|--------|----------|
| 1 | Étape « Passe qualité scopée (selon risque) » dans le prompt canonique : déclencheur (données/auth/sécurité/compliance/prod OU 4+ fichiers de code produit), skills à invoquer avec `scope` = périmètre du chantier, P0/P1 → runs de remédiation, traçage EXECUTED/SKIPPED/N/A | `prompts/canonical/07-p-vbb-closeout.md` |
| 2 | Section « Passe qualité scopée » + case de checklist dans le template closeout | `docs/templates/07_CLOSEOUT.md.template` |
| 3 | Règle « Context compaction (40 % / 75 %) » dans SESSION_RULES.md | `docs/SESSION_RULES.md` |
| 4 | Rule 12 : impact 4 distributions + entrée Decisions log | `docs/DISTRIBUTIONS.md` |
| 5 | Pre-merge gate P.R2 + closeout CLOSE-FINAL (avec sa propre section de passe qualité renseignée) + SESSION/ACTIVITY_LOG + commit/push | docs du run |

## Critères d'acceptation

- Le prompt closeout contient le déclencheur exact et renvoie au protocole
  canonique sans le dupliquer.
- Le template trace la décision (EXECUTED / SKIPPED (risque faible) / N/A
  (docs-only)) — un skip est déclaré, jamais silencieux.
- SESSION_RULES formule 40 % (indicatif, compactor + mini-handoff) et 75 %
  (dur, compaction ou nouvelle session avant toute action) en cohérence avec
  le critère « context <75% » existant.
- Pre-merge gate 5/5 PASS ; aucun outil Python modifié.

## Risques identifiés

- Sur/sous-déclenchement du seuil « 4+ fichiers de code produit » : assumé,
  révisable après V2-R5a (noté dans l'ADR).
- Duplication du protocole dans le prompt : mitigé par renvoi au chemin canonique.

## Rollback

Additif (aucun closeout existant invalidé). `git revert` du commit du run.
