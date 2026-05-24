# 05_PATCH_SUMMARY_RUN_01 — Lot 1A : Patches appliqués aux 6 contrats critiques

**Date** : 2026-06-10  
**Voie** : STRUCTURÉE

---

## Contexte

Les 6 CONTRACT.yaml ciblés existaient déjà (créés lors de lots précédents). Ce run les a **améliorés** pour aligner chaque contrat avec les spécificités de son SKILL.md respectif.

---

## Patches appliqués

### Skill 2-vbb-security

| Champ | Avant | Après |
|-------|-------|-------|
| `verdict_mapping` | absent | Ajouté : READY→PASS, PARTIAL→PARTIAL, BLOCKED→FAIL, UNKNOWN→PARTIAL |
| `inputs.optional` | PROJECT_MODE, AUDIT_STATUS, CONTEXT | + `config_env` |
| `blocking_conditions` | absent | 3 conditions : no_access, too_partial, no_scope |
| `routing.finding_id_prefix` | absent | `SEC` |
| `routing.excludes` | absent | performance, business_logic, global_architecture |

### Skill 2-vbb-db-robustness

| Champ | Avant | Après |
|-------|-------|-------|
| `verdict_mapping` | absent | Ajouté |
| `inputs.optional` | PROJECT_MODE, AUDIT_STATUS, CONTEXT | + `orm_config`, `raw_queries`, `backup_strategy`, `db_ops_docs` |
| `blocking_conditions` | absent | 3 conditions : no_persistence, partial_schema, business_invariants_redirect |
| `routing.finding_id_prefix` | absent | `DB` |
| `routing.excludes` | absent | business_logic, general_security, global_ops |

### Skill 2-vbb-data-integrity

| Champ | Avant | Après |
|-------|-------|-------|
| `verdict_mapping` | absent | Ajouté (+ NOT_APPLICABLE) |
| `inputs.optional` | PROJECT_MODE, AUDIT_STATUS, CONTEXT | + `models_schemas`, `imports_data`, `recalculation_jobs`, `business_docs` |
| `blocking_conditions` | absent | 3 conditions : no_data, static_system→NOT_APPLICABLE, insufficient_evidence |
| `routing.finding_id_prefix` | absent | `DATA` |
| `routing.excludes` | absent | security, db_robustness, systemic_risk |

### Skill 2-vbb-systemic-risk

| Champ | Avant | Après |
|-------|-------|-------|
| `verdict_mapping` | absent | Ajouté |
| `inputs.optional` | PROJECT_MODE, AUDIT_STATUS, CONTEXT | + `architecture_docs`, `adr_docs`, `relations_docs`, `infra_docs` |
| `blocking_conditions` | absent | 3 conditions : incomplete_map, local_zone, security_redirect |
| `routing.finding_id_prefix` | absent | `SYS` |
| `routing.excludes` | absent | local_security, business_logic_detail, performance_tuning |

### Skill 2-vbb-api-auditor

| Champ | Avant | Afterwards |
|-------|-------|-------|
| `verdict_mapping` | absent | Ajouté |
| `inputs.optional` | PROJECT_MODE, AUDIT_STATUS, CONTEXT | + `openapi_spec`, `api_docs`, `client_examples` |
| `blocking_conditions` | absent | 3 conditions : no_api, no_contract, design_redirect |
| `routing.finding_id_prefix` | absent | `API` |
| `routing.excludes` | absent | general_security, performance_scalability, deep_business_logic |

### Skill 3-vbb-risk-register

| Champ | Avant | Après |
|-------|-------|-------|
| `verdict_mapping` | absent | Ajouté |
| `constraints` | absent | `no_new_findings: true`, `role: consolidator` |
| `inputs.required` | `project_repo` | `audit_reports_access` |
| `inputs.optional` | PROJECT_MODE, AUDIT_STATUS, CONTEXT | + `recent_audit_reports`, `documented_decisions` |
| `blocking_conditions` | absent | 3 conditions : no_audit_access, no_reports, too_heterogeneous |
| `routing.phase_scope` | `[audit, phase_2]` | `[consolidation, phase_3]` |
| `routing.excludes` | absent | new_audit_analysis, new_findings |

---

## Fichiers modifiés

| Fichier | Changement |
|---------|-----------|
| `skills/2-vbb-security/CONTRACT.yaml` | Enrichi : verdict_mapping, blocking_conditions, inputs, finding_id_prefix, excludes |
| `skills/2-vbb-db-robustness/CONTRACT.yaml` | Enrichi : idem + inputs spécifiques DB |
| `skills/2-vbb-data-integrity/CONTRACT.yaml` | Enrichi : idem + NOT_APPLICABLE |
| `skills/2-vbb-systemic-risk/CONTRACT.yaml` | Enrichi : idem + inputs architecture/ADR |
| `skills/2-vbb-api-auditor/CONTRACT.yaml` | Enrichi : idem + inputs OpenAPI |
| `skills/3-vbb-risk-register/CONTRACT.yaml` | Enrichi : idem + constraints, phase_scope corrigé, required input changé |