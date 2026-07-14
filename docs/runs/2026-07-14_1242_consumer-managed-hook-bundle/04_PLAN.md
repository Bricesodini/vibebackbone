---
run_id: "2026-07-14_1242_consumer-managed-hook-bundle"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T12:51:00+02:00"
ended_at: "2026-07-14T12:54:00+02:00"
next_phase: "POC"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_AUDIT.md"
  - "docs/adr/0034-consumer-managed-runtime-assets.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Consumer managed hook bundle

## Objectif

Rendre `--install-hook` autonome et fidèle, tout en établissant une frontière
de refresh vérifiable qui ne touche jamais aux documents projet.

## Pré-conditions

- ADR 0034 ACCEPTED après `Go` humain.
- Analyse d'impact READY / CONDITIONAL.
- POC GO et `vbb-gate-check` PASS obligatoires avant code produit.

## Étapes ordonnées

| # | Action | Fichiers cibles | Validation | Rollback |
|---|---|---|---|---|
| 1 | Prototyper preflight + manifeste + installation réelle | `POC.md`, harness temporaire | 6/6 cas | supprimer harness |
| 2 | Passer l'Integration Gate | `INTEGRATION_GATE.md` | `can_code_start=true` | STOP |
| 3 | Implémenter bundle et flags | `tools/vbb-project-init.py` | tests ciblés | revert outil |
| 4 | Étendre les tests | `tests/test_project_init.py` | cas fresh/refresh/conflit/force | revert tests |
| 5 | Aligner skill, prompt et architecture | docs/skills/prompt ciblés | lints/liens | revert docs |
| 6 | Fermer les risques bornés | AUDIT_STATUS + run | preuves ciblées | rouvrir findings |
| 7 | Exécuter P.R2 | cinq commandes canoniques | 5/5 PASS | HANDOFF si échec |

## Critères d'acceptation

- [ ] Bundle source transitif complet et préflighté avant écriture.
- [ ] Manifeste déterministe sans chemin absolu ni donnée sensible.
- [ ] Refresh inchangé idempotent.
- [ ] Personnalisation préservée + exit 1 + aucune copie partielle.
- [ ] Hook étranger préservé sans `--overwrite-hook`.
- [ ] Erreur installateur dans `errors`, jamais dans `skipped`.
- [ ] Documents projet personnalisés préservés.
- [ ] Quatre distributions explicitement évaluées.

## Plan de rollback global

Retirer la logique de bundle et le manifeste, restaurer l'ancien chemin de copie
et rouvrir SEC-CRED-005/TER-001. Aucun dépôt consommateur réel n'est modifié par
ce run ; les POC utilisent uniquement des répertoires temporaires.

## Risques identifiés

- Préflight incomplet produisant un bundle mixte.
- Fichier historique sans manifeste confondu avec une cible VBB.
- Override trop large réintroduisant l'overwrite implicite.
- Dépendance PyYAML non disponible chez un consommateur.

## Analyse d'impact

- **Effectuée ?**: oui, `02_AUDIT.md` et rapport timestampé.
- **Périmètre d'impact**: Contract Tooling, CLI init, hooks locaux, manifeste,
  quatre distributions héritières.
- **Effets de bord**: migration explicite des assets historiques sans provenance.

## Integration Gate

- **ADR référencée**: `docs/adr/0034-consumer-managed-runtime-assets.md`
- **Statut attendu**: ACCEPTED
- **POC référencé**: `POC.md`
- **Verdict attendu**: GO
- **CAN_CODE_START**: YES — gate PASS à 12:59, voir `INTEGRATION_GATE.md`.
