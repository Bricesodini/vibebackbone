---
run_id: "2026-07-31_1137_clean-candidate-reconstruction"
phase: "01_INTAKE"
document_convention: "vbb-doc-v1"
version: "1.0"
type: "run"
visibility: "public"
tags: [run, structured, release-integrity, rr-bk]
relations: []
voie: "STRUCTUREE"
status: "active"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
agent: "codex"
started_at: "2026-07-31T11:37:15Z"
ended_at: "2026-07-31T11:37:15Z"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/audits/integration-integrity-rr-blocker-reconciliation-20260731.md"
  - "docs/AUDIT_STATUS.md"
  - "docs/adr/0051-adversarial-assurance-dimension.md"
artifacts_produced:
  - "01_INTAKE.md"
  - "POC.md"

adversarial_level:
  level: "A2"
  level_reason: "The task changes canonical governance, contracts, corpus integrity, and release gates."
  attacker_identity:
    agent: "Codex"
    llm: "GPT-5"
    system_prompt_version: "codex-desktop-2026-07-31"
  defender_identity:
    agent: "Codex"
    llm: "GPT-5"
    provider: "OpenAI"
    system_prompt_version: "codex-desktop-2026-07-31"
    session: "current-task"
  a2_proxy_mode:
    enabled: true
    limitations: ["No genuinely distinct external reviewer is available in this session; no independent certification claim will be made."]
    quarterly_external_review_due: "2026-10-29T00:00:00Z"

certification_status:
  declared_status: "PRE_CERTIFICATION"
  transient_reason: "Technical pre-candidate reconstruction only; no RC or certification claim."
  bootstrapped_at: "2026-07-31T11:37:15Z"
  bootstrapped_by: "Codex current-task"
---

# 01_INTAKE — clean candidate reconstruction

## Demande reçue

Construire un pré-candidat propre depuis `6b0daf4785d652b23931b80aafba57979e69d9b4`, intégrer la remédiation vbb-doc-v1, committer et valider RR-BK-03, traiter RR-BK-05, lier les gates à un run et un SHA exacts, puis valider en clone propre sans créer de tag, merge ou Release Candidate officielle.

## Reformulation

Reconstruire une branche isolée et traçable à partir de `6b0daf4`, sans reprendre le worktree sale, en intégrant uniquement des corrections bornées et en produisant un verdict de pré-candidat. Les axes RR-BK-01, RR-BK-04 et RR-BK-06 restent ouverts tant que leurs conditions propres ne sont pas satisfaites.

## Scope

### Dans le périmètre

- Branche `codex/rc1-clean-candidate-reconstruction` dans un worktree neuf.
- Intégration atomique de `78e5668` puis `cebeed7` si l’évidence du pilote appartient au jeu de preuves.
- Correction RR-BK-03, corpus et workspace RR-BK-05, contrat exact sujet/run/SHA RR-BK-02.
- Matrice de nomenclature RR-BK-01..06 et rapports liés au sujet exact.
- Clone propre, gates techniques et run de closeout.

### Hors périmètre

- Création ou déplacement de tag, merge, push, publication RC ou certification.
- Réécriture des closeouts historiques.
- Fabrication du verdict Pi ou d’une validation A3 indépendante.
- Résolution globale de RR-BK-01, RR-BK-04 et RR-BK-06 si leurs preuves propres ne peuvent pas être établies.

### Dépendances détectées

- Rapport canonique de réconciliation `INTEGRATION_PATH_REQUIRES_RECONSTRUCTION`.
- Worktree sale `codex/rr-bk-05-readiness-fidelity`, à inspecter et ne jamais reprendre wholesale.
- Commits vbb-doc-v1 `78e5668` et `cebeed7`.
- Disponibilité ultérieure du re-pilote Pi.

## Classification du risque

- **Niveau** : `ÉLEVÉ`
- **Justification** : modification de contrats, gates, corpus de findings confirmés et preuves de release; un faux positif pourrait autoriser une base de release incorrecte.

## Voie recommandée

- **Voie** : `STRUCTUREE`
- **Justification** : travail multi-fichiers, architecture-adjacent, contractuel et explicitement A2.

## Assurance initiale

- **Gates applicables** : `DESIGN`, `CERTIFICATION`, `ADVERSARIAL`, `OTHER` — ADR+POC, architecture, corpus, exact-subject, clean-clone.
- **Checkpoint visé** : `PRE_IMPLEMENTATION` puis `POST_IMPLEMENTATION` et `COUNTER_PROOF`.
- **Implémentation autorisée à l’intake** : `NON` — soumise au gate de ce run.
- **Liée à ADR** : `docs/adr/0051-adversarial-assurance-dimension.md`.
- **POC** : `docs/runs/2026-07-31_1137_clean-candidate-reconstruction/POC.md`.

## Handoff vers `04_PLAN`

- Lire le rapport de réconciliation, les diffs des commits et du worktree RR-BK-05.
- Maintenir les artefacts historiques immuables et borner les fichiers repris.
- Ne conclure `READY` que pour les gates techniques effectivement mesurés.
