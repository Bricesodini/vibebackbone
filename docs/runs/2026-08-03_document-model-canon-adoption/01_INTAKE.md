---
run_id: "2026-08-03_document-model-canon-adoption"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.2"
agent: "codex"
started_at: "2026-08-03T00:40:00+02:00"
ended_at: null
next_phase: "04_PLAN"
artifacts_consumed:
  - "origin/main@067b8ea6e9a7d9bea65a29340bdc38da1361f039"
  - "docs/document-model/*"
  - "docs/runs/2026-08-03_document-model-canon-adoption/05_TRACEABILITY_MATRIX.md"
  - "6983006 docs(document-model): adopt documentary contract v1 foundations"
  - "docs/runs/2026-08-03_document-model-main-integration/07_CLOSEOUT.md"
  - "AGENTS.md"
  - "SYSTEM.md"
  - "docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md"
  - "docs/adr/0053-*"
artifacts_produced:
  - "01_INTAKE.md"

---
# 01_INTAKE — document-model-canon-adoption

## Demande

Adopter localement, sans publication, le Documentary Contract v1.0 et ses six
autorités documentaires consolidées. Les sources de conception antérieures
restent des preuves historiques jusqu'à leur consolidation dans ce run.

## Périmètre

### Dans le périmètre

- six autorités sous `docs/document-model/` ;
- un ADR d'adoption dans la séquence disponible ;
- `.vbb/document-convention.yaml` ;
- références minimales dans INDEX, CONTEXT et ARCHITECTURE ;
- matrice de traçabilité, POC, revue A2 et closeout.

### Hors périmètre

- migration ou classement massif ;
- F-04, F-06 et certification du runtime Pi ;
- changement de DIM, Ontologie, DGM, DTS ou DTP ;
- push, merge, tag ou publication.

## Risque et voie

- **Risque** : `ÉLEVÉ` — adoption d'un contrat documentaire gouvernant des
  artefacts et des agents.
- **Voie** : `STRUCTUREE`.
- **Adversarial** : `A2`, car le sujet est un canon de gouvernance.

```yaml
adversarial_level:
  level: "A2"
  level_reason: "Canon de gouvernance et contrat documentaire publié localement."
```

```yaml
certification_status:
  declared_status: "PRE_CERTIFICATION"
  transient_reason: "Adoption locale préparatoire; aucune certification ni publication."
  bootstrapped_at: "2026-08-03T00:40:00+02:00"
  bootstrapped_by: "codex"
```

## Invariants d'intake

1. Les anciens documents de conception ne deviennent pas canoniques par copie.
2. Les artefacts non qualifiés restent `UNKNOWN`.
3. Les validateurs et skills restent non souverains.
4. Critical Rule 16, ADR-0053 et la gouvernance adversariale v1.2 restent inchangés.
5. Le runtime Pi demeure `NOT_ASSESSED`.
