---
run_id: "2026-07-14_1615_ready-risk-reconciliation"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T16:18:00+02:00"
ended_at: "2026-07-14T16:20:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_AUDIT_REPORT.md"
  - "03_DECISION.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Publish residual risk decisions

## Objectif

Réconcilier la vérité active avec la décision auditée, sans changement canonique
ni comportemental.

## Pré-conditions

- Audit de conventions au verdict READY.
- Décision durable acceptée.
- Integration Gate vert avant publication dans les surfaces actives.

## Ordered steps

1. Retirer les cinq lignes du tableau actif.
2. Publier chaque acceptation avec owner et reopen trigger.
3. Publier la partie résolue de GMA-005 séparément.
4. Mettre à jour le contexte et l'activité sans déclarer READY prématurément.
5. Exécuter P.R2, credentials gate, commit et push.

## Acceptance criteria

- Aucun P2/LOW résiduel n'est indécidé.
- Chaque acceptation contient owner et reopen trigger.
- Le verdict global reste PARTIAL jusqu'à la review indépendante.
- Aucun fichier `tools/`, `tests/`, `prompts/`, `skills/` ou canon modifié.

## Rollback

Restaurer le tableau actif et retirer la section d'acceptation de ce run.

## Risques identifiés

- Faire passer une acceptation bornée pour une résolution technique.
- Déclarer READY avant le septième critère.
- Masquer la divergence linguistique réellement observée.

## Impact analysis

Truth surfaces uniquement. Aucun impact distribution, runtime ou contrat.

## Integration Gate

- ADR: `03_DECISION.md` (décision de disposition locale, pas ADR architecture)
- POC: `POC.md`
- CAN_CODE_START: en attente de `INTEGRATION_GATE.md`.
