---
run_id: "2026-08-03_f03-provenance-alignment"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.2"
agent: "codex"
started_at: "2026-08-03T00:00:00Z"
ended_at: null
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/adr/0051-adversarial-assurance-dimension.md"
  - "docs/adr/0053-a2-a3-assurance-alignment.md"
  - "docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md"
  - "distributions/pi/SYSTEM.md"
  - "SYSTEM.md"
  - "docs/runs/2026-08-02_canon-adoption-revision/MAIN_INTEGRATION_INVENTORY.md"
artifacts_produced:
  - "01_INTAKE.md"
  - "04_PLAN.md"

adversarial_level:
  level: "A2"
  level_reason: "Le run traite la provenance d’une gouvernance canonique et une décision d’intégration précédemment différée."

certification_status:
  declared_status: "PRE_CERTIFICATION"
  transient_reason: "Validation bornée de F-03 avant toute adoption canonique."
  bootstrapped_at: "2026-08-03T00:00:00Z"
  bootstrapped_by: "codex"
---

# 01_INTAKE — F-03 Provenance Alignment

## Demande reçue

Ouvrir un run STRUCTURED / A2 dédié exclusivement à F-03, appliquer la
représentation de provenance ADR-0051 / ADR-0053, produire les preuves,
rejouer les validations concernées et clôturer F-03.

## Périmètre

Dans le périmètre : la relation de provenance entre ADR-0051, ADR-0053,
`docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md`, et la représentation runtime
`SYSTEM.md` / `distributions/pi/SYSTEM.md`.

Hors périmètre : candidat documentaire, adoption canonique, intégration vers
main, toute autre remédiation, Pi déployé, publication, tag, merge et push.

## Représentation appliquée

- ADR-0051 reste la décision fondatrice historique de la dimension adversariale.
- ADR-0053 porte l’alignement A2/A3 v1.2.
- La gouvernance adversariale v1.2 déclare `adr: "0053"` et précise que 0053
  ne réécrit pas 0051.
- `SYSTEM.md` reste une projection symlinkée de `distributions/pi/SYSTEM.md`
  et consomme la règle v1.2 en renvoyant à ADR-0053.

Cette représentation ne modifie ni le sens historique de 0051 ni le candidat
documentaire.
