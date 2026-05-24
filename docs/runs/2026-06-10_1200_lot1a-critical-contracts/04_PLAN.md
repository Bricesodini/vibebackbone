# 04_PLAN — RUN 02 · Lot 1A : Plan d'amélioration des 6 contrats critiques

**Date** : 2026-06-10  
**Voie** : STRUCTURÉE  
**Prérequis** : 02_DISCOVERY.md validé

---

## Constats clés

1. Les 6 CONTRACT.yaml existent déjà — **pas de création de zéro**.
2. Ils sont basés sur un template générique et ne reflètent pas les spécificités de chaque SKILL.md.
3. Le linter impose `PASS_STATUSES = {"PASS", "PARTIAL", "FAIL", "BLOCKED"}` — on ne peut pas ajouter `UNKNOWN` ou `NOT_APPLICABLE` dans le champ `statuses`.
4. La terminologie SKILL.md (READY/PARTIAL/BLOCKED/UNKNOWN) diffère de celle du contrat (PASS/PARTIAL/FAIL/BLOCKED).

## Décisions de conception

### D-C01 : Statuts — Garder PASS/PARTIAL/FAIL/BLOCKED

Le linter exige `statuses ∈ {PASS, PARTIAL, FAIL, BLOCKED}`. On garde ces statuts et on ajoute un champ déclaratif `verdict_mapping` qui documente la correspondance avec les SKILL.md :

```yaml
verdict_mapping:
  READY: PASS
  PARTIAL: PARTIAL
  BLOCKED: FAIL
  UNKNOWN: PARTIAL
  NOT_APPLICABLE: NOT_APPLICABLE
```

- `UNKNOWN` → `PARTIAL` : le skill n'a pas assez d'info pour conclure → PARTIAL est le statut le plus proche.
- `NOT_APPLICABLE` → `NOT_APPLICABLE` : pas dans le statut set, mais documenté pour les cas comme `data-integrity` en mode DISTRIBUTION.

### D-C02 : Inputs — Enrichir les optionnels

Ajouter les inputs spécifiques de chaque SKILL.md dans la section `optional` des contrats.

### D-C03 : Blocking conditions — Ajouter un champ déclaratif

Ajouter un champ `blocking_conditions` au niveau de chaque contrat. Ce n'est pas validé par le linter, mais il documente les conditions du SKILL.md.

### D-C04 : Finding prefixes — Ajouter finding_id_prefix

Ajouter `finding_id_prefix` dans la section `routing` de chaque contrat Phase 2.

### D-C05 : Scope exclus — Ajouter excludes

Ajouter `excludes` dans la section `routing` pour documenter les renvois vers d'autres skills.

### D-C06 : 3-vbb-risk-register — phase_scope correct

Corriger `phase_scope` de `[audit, phase_2]` vers `[consolidation, phase_3]`.

---

## Plan détaillé par contrat

### 2-vbb-security

| Champ | Avant | Après |
|-------|-------|-------|
| `inputs.optional` | PROJECT_MODE, AUDIT_STATUS, CONTEXT | + `config_env` (chemin vers .env.example, settings, etc.) |
| `outputs.statuses` | PASS/PARTIAL/FAIL/BLOCKED | Inchangé (constraint linter) |
| `verdict_mapping` | absent | Ajouté (READY→PASS, etc.) |
| `blocking_conditions` | absent | Ajouté (no code access → STOP, too partial → UNKNOWN mapped to PARTIAL, no scope → clarification) |
| `finding_id_prefix` | absent | `SEC` |
| `routing.excludes` | absent | performance, business-logic, architecture → systemic-risk |
| `secondary_artifacts[0].path_pattern` | `security-{YYYYMMDD-HHMM}.md` | Inchangé |

### 2-vbb-db-robustness

| Champ | Avant | Après |
|-------|-------|-------|
| `inputs.optional` | PROJECT_MODE, AUDIT_STATUS, CONTEXT | + `orm_config`, `raw_queries`, `backup_strategy`, `db_ops_docs` |
| `blocking_conditions` | absent | Ajouté (no persistence → STOP, business logic → redirect data-integrity) |
| `finding_id_prefix` | absent | `DB` |
| `routing.excludes` | absent | business-logic, security, global-ops |
| `verdict_mapping` | absent | Ajouté |

### 2-vbb-data-integrity

| Champ | Avant | Après |
|-------|-------|-------|
| `inputs.optional` | PROJECT_MODE, AUDIT_STATUS, CONTEXT | + `models_schemas`, `imports_data`, `recalculation_jobs`, `business_docs` |
| `blocking_conditions` | absent | Ajouté (no business logic → STOP, static system → NOT_APPLICABLE, too partial → PARTIAL) |
| `finding_id_prefix` | absent | `DATA` |
| `routing.excludes` | absent | security, db-robustness, systemic-risk |
| `verdict_mapping` | absent | Ajouté |

### 2-vbb-systemic-risk

| Champ | Avant | Après |
|-------|-------|-------|
| `inputs.optional` | PROJECT_MODE, AUDIT_STATUS, CONTEXT | + `architecture_docs`, `adr_docs`, `relations_docs`, `infra_docs` |
| `blocking_conditions` | absent | Ajouté (incomplete system map → UNKNOWN mapped to PARTIAL, security audit → redirect security) |
| `finding_id_prefix` | absent | `SYS` |
| `routing.excludes` | absent | local-security, business-logic-detail, performance-tuning |
| `verdict_mapping` | absent | Ajouté |

### 2-vbb-api-auditor

| Champ | Avant | Après |
|-------|-------|-------|
| `inputs.optional` | PROJECT_MODE, AUDIT_STATUS, CONTEXT | + `openapi_spec`, `api_docs`, `client_examples` |
| `blocking_conditions` | absent | Ajouté (no API → STOP, no contract → UNKNOWN→PARTIAL, new API design → redirect api-contract-designer) |
| `finding_id_prefix` | absent | `API` |
| `routing.excludes` | absent | general-security, performance, deep-business-logic |
| `verdict_mapping` | absent | Ajouté |

### 3-vbb-risk-register

| Champ | Avant | Après |
|-------|-------|-------|
| `routing.phase_scope` | `[audit, phase_2]` | `[consolidation, phase_3]` |
| `inputs.required` | `project_repo` | `audit_reports_access` |
| `inputs.optional` | PROJECT_MODE, AUDIT_STATUS, CONTEXT | + `recent_audit_reports`, `documented_decisions` |
| `blocking_conditions` | absent | Ajouté (no audit access → STOP, no reports → STOP, too heterogeneous → PARTIAL) |
| `constraints` | absent | `no_new_findings: true` (consolidateur, pas d'audit neuf) |
| `verdict_mapping` | absent | Ajouté |

---

## Risques de sur-spécification

| Risque | Mitigation |
|--------|------------|
| Trop d'inputs optionnels → l'appelant ne les fournit pas | Tous les inputs ajoutés restent optionnels — le contrat reste exécutable avec seulement project_repo |
| verdict_mapping non validé par le linter | C'est un champ déclaratif, pas exécutoire — acceptable comme documentation |
| blocking_conditions non validé par le linter | Idem — déclaratif, pour documentation et routing futur |
| finding_id_prefix non validé | Déclaratif — acceptable |

## Fichiers à modifier

1. `skills/2-vbb-security/CONTRACT.yaml`
2. `skills/2-vbb-db-robustness/CONTRACT.yaml`
3. `skills/2-vbb-data-integrity/CONTRACT.yaml`
4. `skills/2-vbb-systemic-risk/CONTRACT.yaml`
5. `skills/2-vbb-api-auditor/CONTRACT.yaml`
6. `skills/3-vbb-risk-register/CONTRACT.yaml`
7. `skills/INDEX.yaml` — si nécessaire (ajout d'entrées pour les skills qui y seraient manquants)
8. `docs/AUDIT_STATUS.md` — mise à jour statut des contrats
9. `docs/CONTEXT.md` — mise à jour compteur contrats