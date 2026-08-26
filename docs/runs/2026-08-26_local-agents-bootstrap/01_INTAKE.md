---
run_id: "2026-08-26_local-agents-bootstrap"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
adversarial_governance_version: "1.2"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
agent: "codex"
started_at: "2026-08-26T00:00:00+02:00"
ended_at: "2026-08-26T00:00:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed: ["AGENTS.md", "docs/CONTEXT.md", "docs/PILOTAGE.md", "docs/AUDIT_STATUS.md"]
artifacts_produced: ["01_INTAKE.md"]
---

# 01_INTAKE — local-agents-bootstrap

## Demande reçue

Intégrer un bootstrap générique de contrat opérationnel local `AGENTS.md`,
chargé avant `SESSION.md` et la classification, sans modifier Studio ni les
consommateurs. Il ne modifie pas la gouvernance VBB.

## Scope

Dans le périmètre : Core VBB, quatre adaptateurs, prompts, documentation,
outil de discovery et tests. Hors périmètre : Studio, Compta, runtime,
déploiement et tout dépôt consommateur.

## Classification du risque

- **Niveau** : `ÉLEVÉ`
- **Justification** : le changement touche la gouvernance canonique qui guide
  les agents et les contrats publiés aux distributions.
- **Voie** : `STRUCTUREE`, niveau adversarial `A2`.

## Adversarial level

```yaml
adversarial_level:
  level: "A2"
  level_reason: "Governance canon that gates other work."
```

## Handoff

- ADR : `docs/adr/0055-local-agents-bootstrap.md`
- POC : `docs/runs/2026-08-26_local-agents-bootstrap/POC.md`
- Point de vigilance : ne pas promettre une lecture automatique qu'un runtime
  ne supporte pas; le protocole doit rester portable, explicite et sans pouvoir
  de modifier la logique VBB.
