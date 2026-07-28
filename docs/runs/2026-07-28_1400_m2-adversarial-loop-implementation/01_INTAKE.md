---
run_id: "2026-07-28_1400_m2-adversarial-loop-implementation"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
agent: "external implementer (distinct session, distinct provider)"
started_at: "2026-07-28T14:00:00Z"
ended_at: "2026-07-28T14:05:00Z"
next_phase: "04_PLAN"
artifacts_consumed:
  - "M1 source normatif unique"
artifacts_produced:
  - "01_INTAKE.md"
  - "04_PLAN.md"
---

# 01_INTAKE — M2 Implémentation structurée de la boucle adversariale

## Mandat

Implémenter les **37 modifications normatives** (M2-01 à M2-37) définies par M1,
dans `M1_DECISIONS.md` §8. Strictement consommation.

## Source normative unique

| Source | Rôle |
|---|---|
| `docs/runs/2026-07-28_1200_m1-adversarial-loop-normative-arbitration/M1_DECISIONS.md` | Décisions M1-01 à M1-06 + liste §8 |
| `M1_DECISIONS.md` §M1-01 (autorité) | Créer `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` + étendre `GATE_ASSURANCE_GOVERNANCE.md` |
| `M1_DECISIONS.md` §M1-02 (A2 solo) | `A2_DISTINCT_AGENT_PROXY` + revue trimestrielle |
| `M1_DECISIONS.md` §M1-03 (déclencheurs) | `N=10`, contest_register, 7 fail-closed |
| `M1_DECISIONS.md` §M1-04 (certification.owner) | 3 modes, cadence ≤ 90 j, SLA → SUSPENDED |
| `M1_DECISIONS.md` §M1-05 (non-regression lock) | witnessed_by + test_review à A2 |
| `M1_DECISIONS.md` §M1-06 (CERTIFIED) | 13 conditions, 6 triggers de perte |

## Garde divergence

| Condition | Action |
|---|---|
| Modification impossible sans décision nouvelle | **STOP** + `M2_DEVIATION_FROM_M1.md` |
| Validateur de format refuse une modification | Note dans `05_EXECUTION.md`, pas de forçage |
| Lecture ambiguë d'une décision M1 | STOP + clarification, pas d'inférence |

## Hors-périmètre (re-confirmé)

- Pas de rediscussion des arbitrages M1.
- Pas de modification du niveau A0/A1/A2 ou des contrats de certification.
- Pas d'ajout de nouvelles fonctionnalités.
- Pas de commit/push automatique sans autorisation explicite.

## Definition of done

À la fin du run, un lecteur doit pouvoir répondre OUI à :

1. Les 37 modifications sont implémentées ou explicitement différées avec note de handoff ?
2. Aucune règle M1 n'a été modifiée ?
3. Les anciens workflows sont intacts ?
4. Aucune autorité parallèle n'a été introduite (CR#5) ?
5. L'architecture lint, contract lint et la suite de tests passent ?
6. Une revue indépendante a été effectuée ?

## Handoff

Proceed to `04_PLAN.md`.

FINAL_STATUS (intake) :
```yaml
status: READY
implementation_scope: "M2-01..M2-37"
canon_modification: AUTHORIZED (per source normative unique)
implementation: AUTHORIZED (per source normative unique)
commit_push: PENDING_HUMAN_AUTHORIZATION
```