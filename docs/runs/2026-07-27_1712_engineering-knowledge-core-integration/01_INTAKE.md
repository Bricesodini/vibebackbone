---
run_id: "2026-07-27_1712_engineering-knowledge-core-integration"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
knowledge_governance_version: "1.0"
agent: "codex"
started_at: "2026-07-27T15:12:21Z"
ended_at: "2026-07-27T15:16:00Z"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/runs/2026-07-27_1612_engineering-knowledge-governance/07_CLOSEOUT.md"
  - "docs/runs/2026-07-27_1612_engineering-knowledge-governance/CANON_CHANGE_PROPOSAL.md"
  - "docs/runs/2026-07-27_1612_engineering-knowledge-governance/06_REVIEW_RUN_02.md"
  - "docs/adr/0049-engineering-knowledge-governance.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — Engineering knowledge Core integration

## Demande reçue

Intégrer dans Vibe Backbone Core la proposition approuvée de gouvernance de la
connaissance d'ingénierie, avec son principe directeur, ses validations
techniques, ses tests d'intégration et sa propagation aux quatre distributions.

## Cible post-audit

- **Findings** : `KNO-001` à `KNO-007`.
- **Comportement** : un run qualifié effectue un Knowledge Harvest ; toute
  promotion traverse audit, revue indépendante et décision humaine.
- **Liée à ADR** :
  `docs/adr/0049-engineering-knowledge-governance.md` (`ACCEPTED`).
- **POC source** :
  `docs/runs/2026-07-27_1612_engineering-knowledge-governance/POC.md` (`GO`).

## Scope

### Dans le périmètre

- Autorité canonique et principe de capitalisation gouvernée.
- Maturité, preuves, rôles, frontières et non-régression.
- Routage, protocole, prompts audit/décision/revue/closeout et templates.
- Enforcement rétrocompatible du Knowledge Harvest.
- Architecture, navigation et décision de propagation distributions.
- Tests, revue indépendante, P.R2 et closeout.

### Hors périmètre

- Nouveau skill spécialisé de capitalisation.
- Capitalisation d'un apprentissage concret de Backbone Know.
- Toute règle technologique ou propre à un projet.
- Modification du run non suivi
  `2026-07-26_1701_i1-i2-normative-remediation`.

## Classification

- **Route** : `STRUCTUREE`.
- **Risque** : élevé, changement Core multi-surface.
- **Mode** : `DISTRIBUTION`.

## Pré-check d'exécution

- Skill routeur concerné : `vibebackbone`.
- Contrats lus : `skills/vibebackbone/CONTRACT.yaml`, `skills/INDEX.yaml`.
- État audit : `KNO-GOV-001 READY_FOR_HUMAN_DECISION`, désormais approuvé.
- Worktree : le run I1/I2 préexistant est hors périmètre et reste intact.

## Handoff

Passer à `04_PLAN.md`, puis exécuter seulement si les gates automatique et
manuel sont `PASS`.
