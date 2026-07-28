---
run_id: "2026-07-28_1200_m1-adversarial-loop-normative-arbitration"
phase: "01_INTAKE"
voie: "AUDIT"
status: "READY"
kind: "ARBITRATION_RUN"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
agent: "external arbitrator (distinct session, distinct provider)"
started_at: "2026-07-28T12:00:00Z"
next_phase: "M1_DECISIONS"
artifacts_consumed:
  - "docs/runs/2026-07-28_1002_adversarial-loop-governance-design/* (M0 outputs)"
  - "docs/GATE_ASSURANCE_GOVERNANCE.md"
  - "docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md"
  - "docs/adr/0049-engineering-knowledge-governance.md"
  - "docs/adr/0050-design-certification-assurance-schema.md"
  - "docs/PILOTAGE.md"
artifacts_produced:
  - "01_INTAKE.md"
  - "M1_DECISIONS.md"
  - "02_CLOSEOUT.md"
---

# 01_INTAKE — M1 Arbitrage normatif de la boucle adversariale

## Mandat

Transformer le dossier de design M0 (`2026-07-28_1002_*`) en **six décisions
normatives** explicites. Ce run est un run d'arbitrage — il rend des
décisions mais n'écrit ni les ADR, ni le schéma, ni les templates, ni les
prompts.

## Entrées

| # | Source | Rôle |
|---|---|---|
| E1 | `2026-07-28_1002/01_INTAKE.md` … `04_DESIGN_DOSSIER.md` | Dossier de design validé (v0.2) |
| E2 | `2026-07-28_1002/05_MIGRATION_STRATEGY.md` | Phasage M0→M6, ramp R0→R2 |
| E3 | `2026-07-28_1002/06_INDEPENDENT_REVIEW.md` | Auto-revue (PARTIAL independence divulguée) |
| E4 | `2026-07-28_1002/08_INDEPENDENT_REVIEW_DISTINCT_ACTOR.md` | Revue indépendante (GENUINE — COND-01 levée) |
| E5 | `2026-07-28_1002/CANON_CHANGE_PROPOSAL.md` | Proposition de changement canon |
| E6 | `docs/GATE_ASSURANCE_GOVERNANCE.md`, ADR 0049, ADR 0050 | Canon de référence |

## Hors-périmètre (re-confirmé)

- Aucune modification de template, gate, prompt, ADR, ou document normatif.
- Aucune écriture d'ADR définitive (≠ proposition).
- Aucune implémentation du schéma 1.1, du validateur
  `vbb-adversarial-gate.py`, des templates, ou des skills adversariaux.
- Aucun commit, aucun push.

## Décisions à rendre

| ID | Objet | Cible |
|---|---|---|
| M1-01 | Autorité canonique | COND-05 |
| M1-02 | Contrat de repli `A2` pour dépôt solo | COND-04 |
| M1-03 | Déclencheurs (N, « contestée ») | ADVR-14, ADVR-16 |
| M1-04 | `certification.owner` | ADVR-13 |
| M1-05 | Non-regression lock | ADVR-17 |
| M1-06 | Statut `CERTIFIED` | ADVR-11, ADVR-13, M1-04 |

## Définition de done

À la fin du run, un lecteur doit pouvoir répondre OUI à toutes les
questions suivantes :

1. Pour chaque décision M1-01 à M1-06, existe-t-il une **option unique
   retenue** avec **arguments** et **impacts** ?
2. Le split d'autorité (M1-01) est-il tranché sans canon dupliqué (CR#5) ?
3. Le contrat solo (M1-02) est-il applicable *au dépôt Vibebackbone lui-même* ?
4. Les déclencheurs (M1-03) sont-ils opérationnellement applicables ?
5. Le mécanisme de `certification.owner` (M1-04) est-il exécutable ?
6. Le non-regression lock (M1-05) corrige-t-il le biais de confirmation ?
7. Le statut `CERTIFIED` (M1-06) reste-t-il cohérent avec ADR 0050 ?
8. La liste des modifications M2 est-elle prête à être consommée ?

## Handoff

Proceed to `M1_DECISIONS.md` pour les arbitrages.

FINAL_STATUS (intake) :

```yaml
status: READY
arbitration_scope: "M1-01..M1-06"
canon_modification: NONE
implementation: NONE
```