---
run_id: "2026-07-27_2145_design-certification-gates-core-integration"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
agent: "codex"
started_at: "2026-07-27T19:45:52Z"
ended_at: "2026-07-27T19:48:00Z"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/runs/2026-07-27_2117_design-certification-gates-governance-audit/07_CLOSEOUT.md"
  - "docs/runs/2026-07-27_2117_design-certification-gates-governance-audit/04_RECOMMENDATION.md"
  - "docs/runs/2026-07-27_2117_design-certification-gates-governance-audit/06_INDEPENDENT_REVIEW.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — Design/Certification gate Core integration

## Demande reçue

Intégrer officiellement les familles de gate `DESIGN` et `CERTIFICATION`,
conserver `PASS/FAIL`, rendre l'autorisation d'implémentation explicite et
fail-closed, préserver les projets existants et garder le Knowledge Harvest au
closeout.

## Cible post-audit

- **Finding cible** : recommandation Option C, run d'audit
  `2026-07-27_2117_design-certification-gates-governance-audit`.
- **Décision humaine** : APPROVED dans la demande ouvrant ce run.
- **Liée à ADR** :
  `docs/adr/0050-design-certification-assurance-schema.md`.
- **Hypothèse POC** : un reader historique peut ignorer `ASSURANCE_STATUS`
  tandis qu'un reader v1 valide les nouveaux invariants sans réécriture.

## Scope

### Dans le périmètre

- Autorité canonique de la taxonomie des gates et du schéma d'assurance v1.
- Pilotage, protocole, architecture, prompts et templates de run/review/closeout.
- Enforcement rétrocompatible et tests de non-régression.
- Propagation Core vers Pi, OpenCode, Codex et Claude via les autorités partagées.
- Revue indépendante, Knowledge Harvest, closeout, commit et push sous PASS.

### Hors périmètre

- Tout projet consommateur, dont Backbone Know.
- Réécriture ou reclassification des runs historiques.
- Nouvelle phase agentique ou déplacement du Knowledge Harvest.
- Le run non suivi préexistant
  `docs/runs/2026-07-26_1701_i1-i2-normative-remediation/`.

## Classification

- **Route** : `STRUCTUREE`.
- **Risque** : élevé, contrat canonique multi-surface.
- **Mode** : `DISTRIBUTION`.

## Handoff

Passer à l'analyse d'impact, au POC et au gate ADR + POC. Aucun changement
comportemental n'est autorisé avant `CAN_CODE_START: YES`.
