---
run_id: "2026-08-02_documentary-skills-dtp-alignment"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-08-02T00:00:00Z"
ended_at: "2026-08-02T00:00:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "POC.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Documentary skills DTP alignment

## Objectif

Aligner les quatre skills ciblées sur C0–C5 et Critical Rule 16, sans exécuter
de nettoyage documentaire.

## Pré-conditions

- Le dépôt Vibe Backbone est accessible sur la branche de travail.
- Le validateur C0–C5 et les tests précédents sont disponibles.
- Le gate d’intégration a produit `CAN_CODE_START=true`.

## Autorisation d’implémentation

```yaml
implementation_authorization:
  status: "AUTHORIZED"
  required_gate_ids: ["documentary-skills-dtp-alignment-pre-implementation"]
  reasons: ["Le gate d’intégration a déclaré CAN_CODE_START=true; le périmètre exclut toute remédiation documentaire."]
```

## Étapes ordonnées

| # | Action | Fichiers cibles | Validation | Rollback |
|---|--------|-----------------|------------|----------|
| 1 | Adapter les quatre contrats de skills | skills/1-vbb-doc-harmonizer, skills/1-vbb-code-doc-coherence-auditor, skills/1-vbb-code-doc-gap-integrator, skills/t-vbb-project-context-init | Tests d’alignement ciblés | Revert du commit local |
| 2 | Vérifier la décision humaine et l’absence d’écriture automatique | tests/test_documentary_skills_dtp_alignment.py | Suite ciblée et non-régression | Revert du commit local |
| 3 | Documenter les preuves et clôturer | docs/runs/2026-08-02_documentary-skills-dtp-alignment/ | Lints et git diff --check | Revert du commit local |

## Critères d'acceptation

- [x] Les quatre skills consomment C0–C5 et préservent UNKNOWN.
- [x] OUI/NON/PLUS_TARD précèdent toute proposition de route.
- [x] Aucune correction documentaire n’est exécutée.
- [x] Les validations applicables passent.

## Plan de rollback global

Annuler le commit local atomique; aucun artefact existant du dépôt n’a été
modifié par le run.

## Risques identifiés

- Risque de contrat skill insuffisamment couvert : mitigé par les tests ciblés,
  la suite complète et les lints.
- Risque d’élargissement silencieux : exclu par le périmètre et le closeout.

## Analyse d’impact

- **Effectuée ?** : NON (justifié : adaptation bornée de contrats de skills,
  sans changement d’architecture, canon ou distribution).
- **Périmètre d’impact** : quatre skills et leurs preuves de run.
- **Risques d’effet de bord** : aucun identifié par les validations exécutées.

## Integration Gate

- ADR : `docs/adr/0004-contract-schema-version-semantics.md` — ACCEPTED.
- POC : `POC.md` — GO.
- `CAN_CODE_START=true`.

## Handoff vers `05_EXECUTION`

Première action : appliquer les adaptations minimales puis exécuter les
validations prévues, sans ouvrir de remédiation documentaire.
