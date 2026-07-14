---
run_id: "2026-07-14_1615_ready-risk-reconciliation"
phase: "03_DECISION"
voie: "STRUCTUREE"
status: "ACCEPTED"
date: "2026-07-14"
---

# 03_DECISION — Residual risk disposition

## Decision

Ne pas créer de migration générique. Fermer l'ambiguïté de nom résolue et
accepter explicitement les écarts résiduels avec les bornes suivantes.

| Risk | Decision | Owner | Reopen trigger |
|---|---|---|---|
| GMA-005 naming | Resolved | Python tooling maintainer | Ruff E741 non-zero on supported scope |
| GMA-005 long functions | Accepted | Maintainer of the touched tool | Demonstrated multi-responsibility, testability defect, or regression in a touched function |
| GMA-005 French prompts | Accepted variance | Prompt architecture maintainer | Language-caused routing failure, English-only consumer requirement, or prompt rewrite touching the affected surface |
| SYS-POC-004 | Accepted historical residual | Governance maintainer | Future canon, architecture, or cross-service implementation starts after POC without a linked durable decision |
| SYS-SUB-003 | Accepted conditional residual | Orchestrator maintainer | Next explicit delegation lacks counts, citations, contradiction checks, or output-to-integration diff |
| QA-004 | Accepted LOW | Artifact tooling maintainer | Generator is changed or a new active artifact has ambiguous temporal provenance |
| QA-005 | Accepted LOW | Architecture maintainer | Architecture-impacting skill change is merged without an ADR or explicit non-ADR rationale |

## Rationale

Le plan READY approuvé demande de décider les risques sur preuves et interdit le
refactor par longueur, la traduction sans défaut démontré et les ADR par compte.
Les mécanismes existants couvrent l'action future ; une nouvelle règle canonique
n'est pas nécessaire.

## Consequences

- Aucun P2 ne reste indécidé après publication dans `AUDIT_STATUS.md`.
- Les écarts acceptés restent visibles avec ownership et condition de retour.
- Aucune promesse de conformité linguistique totale n'est formulée.
