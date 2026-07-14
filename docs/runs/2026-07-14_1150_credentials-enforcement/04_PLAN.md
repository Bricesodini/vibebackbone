---
run_id: "2026-07-14_1150_credentials-enforcement"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T11:52:00+02:00"
ended_at: "2026-07-14T11:54:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "01_INTAKE.md"
  - "docs/adr/0033-layered-core-credentials-enforcement.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Layered Core credentials enforcement

## Objectif

Implémenter l'ADR 0033 avec un moteur différentiel unique et fermer les deux P1
sans introduire de dépendance ni de politique propre à une distribution.

## Pré-conditions

- SEC-01 terminé et findings reliés.
- Option A validée par Brice.
- ADR 0033 `ACCEPTED`.
- POC `GO` et `vbb-gate-check` PASS obligatoires avant code.

## Étapes ordonnées

| # | Action | Fichiers cibles | Validation | Rollback |
|---|---|---|---|---|
| 1 | Prouver l'extraction différentielle et la politique | POC temporaire + `POC.md` | corpus synthétique complet | supprimer uniquement le POC temporaire |
| 2 | Cartographier propagation | `02_AUDIT.md`, rapport impact, `DISTRIBUTIONS.md` | classification CONDITIONAL/NON_BREAKING | docs seulement |
| 3 | Passer l'Integration Gate | `INTEGRATION_GATE.md` | `can_code_start=true` | STOP sans code |
| 4 | Implémenter le moteur Core | `tools/vbb-credentials-gate.py` | tests unitaires | revert du fichier outil |
| 5 | Brancher le hook et les deux CI | hook, workflow, CI locale | tests intégration + parité | revert des appels |
| 6 | Réconcilier architecture et risques | architecture, audit, contexte | lints + liens | revert docs agrégées |
| 7 | Fermer avec P.R2 | run 05/06/07 | 5 vérifications PASS | HANDOFF si échec |

## Critères d'acceptation

- [ ] Ajout/modification sensible synthétique → exit non-zéro.
- [ ] Placeholder, variable d'environnement et contenu ordinaire → exit zéro.
- [ ] Suppression, ligne inchangée et binaire → aucun finding.
- [ ] Exception sans justification → finding ; exception justifiée → warning.
- [ ] Hook local et CI utilisent le même outil Core.
- [ ] Tests Linux/macOS compatibles, Python stdlib seulement.
- [ ] Les quatre distributions sont explicitement évaluées.
- [ ] P.R2 et CI locale passent.

## Plan de rollback global

Retirer les appels du hook et des workflows, puis l'outil et ses tests. La règle
canonique revient à la revue manuelle documentée par SEC-01 ; aucun format de
données ou état consommateur n'est migré.

## Risques identifiés

- Faux positifs sur documentation et fixtures.
- Base Git indisponible ou SHA zéro lors d'un premier push.
- Diff local et diff CI non équivalents.
- Marqueur d'exception utilisé pour contourner le gate.

## Analyse d'impact

- **Effectuée ?**: EN COURS via `t-vbb-impact-analyzer` avant code.
- **Périmètre d'impact**: contract-tooling, hook local, CI locale/distante,
  quatre distributions consommatrices du Core.
- **Effets de bord**: commits/PR bloqués sur findings ; aucun runtime externe.

## Integration Gate

- **ADR référencée**: `docs/adr/0033-layered-core-credentials-enforcement.md`
- **Statut attendu**: ACCEPTED
- **POC référencé**: `POC.md`
- **Verdict attendu**: GO
- **CAN_CODE_START**: YES — gate PASS à 12:02, voir `INTEGRATION_GATE.md`.
