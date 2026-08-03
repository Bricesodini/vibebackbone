---
run_id: "2026-08-03_f03-revision"
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
  - "docs/runs/2026-08-03_f03-provenance-alignment/06_INDEPENDENT_REVIEW.md"
  - "docs/adr/0053-a2-a3-assurance-alignment.md"
  - "distributions/pi/SYSTEM.md"
  - "SYSTEM.md"
artifacts_produced:
  - "01_INTAKE.md"

adversarial_level:
  level: "A2"
  level_reason: "Révision d’une représentation de gouvernance canon-adjacent après deux findings confirmés."

certification_status:
  declared_status: "PRE_CERTIFICATION"
  transient_reason: "Run borné de correction et contre-vérification de F03-A2-01 et F03-A2-02."
  bootstrapped_at: "2026-08-03T00:00:00Z"
  bootstrapped_by: "codex"
---

# 01_INTAKE — F03-REVISION

## Scope

Dans le périmètre :

- alignement du texte de `distributions/pi/SYSTEM.md` sur ADR-0053 v1.2 ;
- mise à jour de sa métadonnée `updated` à la date de la dernière révision
  gouvernée pertinente ;
- vérification du symlink racine `SYSTEM.md`.

Hors périmètre : ADR, candidat documentaire, DIM, Ontologie, DGM, DTS, DTP,
main, adoption canonique, runtime Pi déployé et toute autre remédiation.

## Autorisation

La mission humaine autorise uniquement ces deux corrections. Aucun push, tag,
merge ou publication n’est autorisé.
