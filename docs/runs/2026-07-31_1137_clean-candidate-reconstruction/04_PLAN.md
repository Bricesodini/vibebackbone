---
run_id: "2026-07-31_1137_clean-candidate-reconstruction"
phase: "04_PLAN"
document_convention: "vbb-doc-v1"
document_version: "1.0"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.1"
adversarial_governance_version: "1.1"
version: "1.0"
type: "run"
visibility: "public"
tags: [run, plan, structured, rr-bk]
relations: []
voie: "STRUCTUREE"
status: "active"
agent: "codex"
started_at: "2026-07-31T11:37:15Z"
ended_at: "2026-07-31T11:37:15Z"
next_phase: "05_EXECUTION"
artifacts_consumed: ["01_INTAKE.md", "POC.md", "docs/audits/integration-integrity-rr-blocker-reconciliation-20260731.md"]
artifacts_produced: ["04_PLAN.md"]
---

# 04_PLAN — clean candidate reconstruction

## Objectif

Produire une branche de pré-candidat techniquement propre, avec corrections RR-BK-02/03/05 bornées et preuves run/SHA exactes.

## Pré-conditions

- Worktree neuf depuis `6b0daf4785d652b23931b80aafba57979e69d9b4`.
- Worktree courant et worktree RR-BK-05 laissés intacts.
- Rapport d’entrée lu; verdict de départ `INTEGRATION_PATH_REQUIRES_RECONSTRUCTION`.

## Autorisation d’implémentation

```yaml
implementation_authorization:
  status: "AUTHORIZED"
  required_gate_ids: ["adr-0051", "poc-clean-candidate-reconstruction"]
  reasons: ["ADR 0051 is ACCEPTED; bounded POC verdict is GO; no publication or certification is authorized."]
```

## Étapes ordonnées

| # | Action | Fichiers cibles | Validation | Rollback |
|---|---|---|---|---|
| 1 | Intégrer vbb-doc-v1 par cherry-pick borné | commits `78e5668`, `cebeed7` | arbre/diff et linter | recréer le worktree depuis base |
| 2 | Extraire RR-BK-03 depuis le worktree sale | dashboard, contrat, tests, corpus/preuves nécessaires | négatif avant, positif après, fail-closed | supprimer le commit atomique |
| 3 | Reconstruire RR-BK-05 | corpus A2-GP-01..03, index, tests | invariant corpus et pytest ciblé | supprimer le commit atomique |
| 4 | Implémenter RR-BK-02 | consommateurs de run/latest et contrat subject | tests d’erreurs de liaison | supprimer le commit atomique |
| 5 | Publier la matrice et les rapports | run artifacts, matrix, candidate subject | tous les rapports même SHA/run | supprimer les artefacts du run |
| 6 | Valider en clone propre | clone temporaire | suite complète, architecture, relations, contracts, corpus, adversarial, CI locale | handoff PARTIAL |

## Critères d’acceptation

- [ ] Branche isolée et status propre avant/après.
- [ ] Commits intégrés atomiquement et provenance documentée.
- [ ] RR-BK-03 verdicté RESOLVED ou NOT_RESOLVED sur le nouveau candidat.
- [ ] RR-BK-05 verdicté RESOLVED/PARTIALLY_RESOLVED/NOT_RESOLVED sans falsifier les findings.
- [ ] RR-BK-02 verdicté RESOLVED/PARTIALLY_RESOLVED/NOT_RESOLVED avec contrat exact.
- [ ] Clone `--no-local` propre, tests/gates exécutés et limites explicites.

## Analyse d’impact

- **Effectuée ?** : `OUI (via t-vbb-impact-analyzer, périmètre manuel borné aux outils, tests, corpus, runs et relations)`.
- **Périmètre d’impact** : dashboard, gates de sujet, corpus obligatoire, preuves de run, `docs/RELATIONS.md` dérivé.
- **Risques d’effet de bord** : sélection de mauvais run/SHA, corpus contradictoire, reprise de fichiers du worktree sale.

## §X.Ybis — Integration Gate

- **ADR référencé** : `docs/adr/0051-adversarial-assurance-dimension.md` — **Status**: ACCEPTED.
- **POC référencé** : `docs/runs/2026-07-31_1137_clean-candidate-reconstruction/POC.md` — `Décision: GO`.
- **CAN_CODE_START?** : `YES`, borné à ce plan; aucune publication/certification.

## Critères d'acceptation

- [ ] Corrections bornées, atomiques et traçables.
- [ ] Corpus invariant et exact-subject tests pass.
- [ ] Clone propre et gates restants explicitement reportés.

## Plan de rollback global

Recréer le worktree depuis `6b0daf4` et rejouer uniquement les commits listés
dans la provenance; ne jamais reprendre le worktree sale.

## Risques identifiés

- Sujet final à rebinder après le commit d’évidence.
- Absence de reviewer externe et re-pilote Pi.
