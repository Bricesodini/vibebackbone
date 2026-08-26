---
run_id: "2026-08-26_local-agents-bootstrap"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-08-26T00:00:00+02:00"
ended_at: "2026-08-26T00:00:00+02:00"
next_phase: "05_EXECUTION"
artifacts_consumed: ["01_INTAKE.md", "POC.md", "INTEGRATION_GATE.md"]
artifacts_produced: ["04_PLAN.md"]
---

# 04_PLAN — local-agents-bootstrap

## Objectif

Rendre le contrat opérationnel local observable et obligatoire avant
session/classification, sans mécanisme spécifique à un consommateur ni pouvoir
sur la gouvernance VBB.

## Pré-conditions

- ADR 0055 est `ACCEPTED` et le POC de frontière Git est `GO`.
- Le gate `vbb-gate-check.py` autorise l'implémentation.
- Aucun dépôt consommateur n'est dans le périmètre de mutation.

## Autorisation d'implémentation

```yaml
implementation_authorization:
  status: "AUTHORIZED"
  required_gate_ids: ["LOCAL-AGENTS-ADR-0055", "LOCAL-AGENTS-POC-01"]
  reasons: ["Integration gate passed."]
```

## Étapes ordonnées

| # | Action | Validation |
|---|---|---|
| 1 | Ajouter l'outil Core de discovery | tests isolés sur dépôts temporaires |
| 2 | Ancrer l'ordre de bootstrap dans règles/prompts | tests textuels des entrypoints |
| 3 | Propager aux quatre distributions | test de propagation |
| 4 | Documenter la convention | vérification documentaire |

## Plan de rollback global

Revert du commit dédié : l'ancien bootstrap ne disposait d'aucun contrat local
explicite et aucun état runtime externe n'est modifié.

## Risques identifiés

- Un runtime peut ne pas invoquer le bootstrap Core : les instructions restent
  explicites et la limitation est documentée.
- Un symlink peut viser hors dépôt : le vérificateur le refuse.
- Une règle locale peut tenter d'altérer VBB : elle est non applicable.

## Critères d'acceptation

- [ ] Pas de contrat : continuité historique.
- [ ] Contrat tracked, modifié et untracked : lu et état visible.
- [ ] Sous-dépôt : pas de parent arbitraire.
- [ ] Session et classification suivent la discovery.
- [ ] Aucune référence Studio/Compta.
