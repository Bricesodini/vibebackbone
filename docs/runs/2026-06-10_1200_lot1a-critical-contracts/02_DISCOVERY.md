# 02_DISCOVERY — RUN 02 · Lot 1A : Alignement des 6 contrats critiques

**Date** : 2026-06-10  
**Voie** : STRUCTURÉE

---

## Contexte critique

Les 6 CONTRACT.yaml ciblés **existent déjà**. Ils ont été créés lors de lots précédents (PR #5). Cependant, l'analyse révèle qu'ils sont **trop génériques** : tous les 6 partagent le même squelette template avec des différences minimales (triggers, artefact path). Les spécificités de chaque SKILL.md ne sont pas reflétées.

---

## Analyse par skill

### 1. 2-vbb-security

**SKILL.md spécificités :**
- Inputs requis : Accès au code ou architecture système
- Inputs optionnels : PROJECT_MODE, CONTEXT, config (.env.example, settings)
- Blocking : aucun accès aux points d'entrée → STOP ; système trop partiel → UNKNOWN ; audit sans périmètre → clarification
- Verdicts : READY / PARTIAL / BLOCKED / UNKNOWN
- Scope exclus : performance, business logic, architecture globale
- Finding prefix : pas de préfixe explicite dans SKILL.md

**CONTRACT.yaml actuel :**
- Inputs : `project_repo` (générique) ; optionnels : PROJECT_MODE, AUDIT_STATUS, CONTEXT
- Statuts : PASS / PARTIAL / FAIL / BLOCKED
- Missing : config dans optionnels, blocking conditions, UNKNOWN status

**Écarts identifiés :**
- E-01 : Statuts SKILL.md = READY/PARTIAL/BLOCKED/UNKNOWN vs CONTRACT = PASS/PARTIAL/FAIL/BLOCKED
- E-02 : Input spécifique "config" absent du contrat
- E-03 : Blocking conditions non reflétées dans gates
- E-04 : UNKNOWN status absent du contrat
- E-05 : Scope exclus pas mentionné

---

### 2. 2-vbb-db-robustness

**SKILL.md spécificités :**
- Inputs requis : Accès au schéma DB, migrations, ou couche de persistance
- Inputs optionnels : PROJECT_MODE, ORM config, requêtes raw, stratégie backup/restore, docs exploitation DB
- Blocking : aucune persistence identifiable → STOP ; partial → UNKNOWN ; invariants métier → rediriger vers data-integrity
- Verdicts : READY / PARTIAL / BLOCKED / UNKNOWN
- Finding prefix : `DB-XX`
- Référence standard : `0-vbb-standard`

**CONTRACT.yaml actuel :**
- Inputs : génériques (project_repo, PROJECT_MODE, AUDIT_STATUS, CONTEXT)
- Statuts : PASS / PARTIAL / FAIL / BLOCKED

**Écarts :**
- E-01 : Même écart de statuts (READY→PASS, UNKNOWN manquant, FAIL vs UNKNOWN)
- E-02 : Inputs spécifiques absents (ORM config, raw queries, backup strategy, DB ops docs)
- E-03 : Blocking conditions non reflétées (redirection vers data-integrity)
- E-04 : Pas de mention du prefix de finding DB-XX

---

### 3. 2-vbb-data-integrity

**SKILL.md spécificités :**
- Inputs requis : Accès au code métier ou couche de données
- Inputs optionnels : PROJECT_MODE, modèles/schémas/migrations, imports CSV/OCR/bank, jobs recalcul/correction, documentation métier
- Blocking : aucun code ni modèle → STOP ; système statique → NOT_APPLICABLE ; preuves trop partielles → UNKNOWN
- Verdicts : READY / PARTIAL / BLOCKED / UNKNOWN
- Finding prefix : `DATA-XX`
- Exclus : sécurité (→ security), robustesse DB (→ db-robustness), architecture systémique (→ systemic-risk)

**Écarts :**
- E-01 : Statuts : même écart READY/PARTIAL/BLOCKED/UNKNOWN vs PASS/PARTIAL/FAIL/BLOCKED
- E-02 : Inputs spécifiques absents (imports, recalculs, documentation métier)
- E-03 : Blocking conditions non reflétées (NOT_APPLICABLE pour système statique)
- E-04 : Scope exclus non mentionnés dans routing

---

### 4. 2-vbb-systemic-risk

**SKILL.md spécificités :**
- Inputs requis : Accès au repo ou structure système
- Inputs optionnels : PROJECT_MODE, ARCHITECTURE.md, RELATIONS.md, docs infra/services/workflows, ADR
- Blocking : carte trop incomplète → UNKNOWN ; zone locale sans dépendances → ne pas surconclure ; audit sécurité → rediriger vers security
- Verdicts : READY / PARTIAL / BLOCKED / UNKNOWN
- Finding prefix : `SYS-XX`
- Exclus : vulnérabilités sécurité locales, invariants métier détaillés, tuning performance

**Écarts :**
- E-01 : Même écart de statuts
- E-02 : Inputs spécifiques absents (ARCHITECTURE.md, RELATIONS.md, ADR, docs infra)
- E-03 : Blocking conditions non reflétées

---

### 5. 2-vbb-api-auditor

**SKILL.md spécificités :**
- Inputs requis : Accès au code ou routes API implémentées
- Inputs optionnels : PROJECT_MODE, openapi.yaml, API INDEX.md, documentation API, exemples clients/consommateurs
- Blocking : aucune API ni route → STOP ; aucun contrat explicite → UNKNOWN dominant ; design nouvelle API → rediriger vers api-contract-designer
- Verdicts : READY / PARTIAL / BLOCKED / UNKNOWN
- Finding prefix : `API-XX`
- Exclus : sécurité générale (→ security), performance, logique métier profonde

**Écarts :**
- E-01 : Même écart de statuts
- E-02 : Inputs spécifiques absents (openapi.yaml, API docs, client examples)
- E-03 : Blocking conditions non reflétées (redirection vers api-contract-designer)

---

### 6. 3-vbb-risk-register

**SKILL.md spécificités :**
- Inputs requis : Accès à `docs/audits/`
- Inputs optionnels : AUDIT_STATUS.md, rapports récents phase 0-2, décisions explicites documentées
- Blocking : docs/audits/ pas accessible → STOP ; aucun rapport → STOP ; rapports trop hétérogènes → UNKNOWN
- Verdicts : READY / PARTIAL / BLOCKED / UNKNOWN
- Phase : 3, pas 2
- Rôle : consolidateur, PAS d'audit neuf
- Finding reference : reprend les IDs d'origine (SEC-XX, SYS-XX, etc.)

**Écarts :**
- E-01 : Même écart de statuts
- E-02 : Input clé `docs/audits/` pas dans le contrat (project_repo à la place)
- E-03 : Blocking conditions pas reflétées
- E-04 : Rôle de consolidateur (pas de nouveaux findings) pas mentionné
- E-05 : routing.phase_scope contient "phase_2" alors que le skill est phase 3

---

## Écarts transversaux

Tous les 6 contrats partagent les mêmes problèmes structurels :

| Écart | Description | Gravité |
|-------|-------------|----------|
| **E-trans-01** | Statuts SKILL.md (READY/PARTIAL/BLOCKED/UNKNOWN) ≠ CONTRACT (PASS/PARTIAL/FAIL/BLOCKED) | Haute — terminologie incohérente |
| **E-trans-02** | Inputs spécifiques du SKILL.md non reflétés dans le contrat | Moyenne — perte de spécificité |
| **E-trans-03** | Blocking conditions du SKILL.md non reflétées dans les gates | Moyenne — logique de gate absente |
| **E-trans-04** | Finding prefixes (DB-XX, DATA-XX, SYS-XX, API-XX) non mentionnés | Basse — cosmétique mais utile |
| **E-trans-05** | Scope exclus non mentionnés dans routing | Basse — utile pour la navigation |
| **E-trans-06** | NOT_APPLICABLE pas dans les statuts du contrat (nécessaire pour data-integrity en mode DISTRIBUTION) | Moyenne |

---

## Décision de traitement

### E-trans-01 : Statuts

Le linter et le runtime utilisent PASS/PARTIAL/FAIL/BLOCKED. Les SKILL.md utilisent READY/PARTIAL/BLOCKED/UNKNOWN.

**Décision** : Aligner les contrats en gardant les statuts du runtime (PASS/PARTIAL/FAIL/BLOCKED) + ajouter NOT_APPLICABLE. Ajouter un champ `verdict_mapping` explicite dans le contrat pour documenter l'équivalence :

```yaml
verdict_mapping:
  READY: PASS
  PARTIAL: PARTIAL
  BLOCKED: FAIL  # ou BLOCKED selon sévérité
  NOT_APPLICABLE: NOT_APPLICABLE
```

Cette approche préserve la compatibilité runtime tout en documentant la correspondance avec la terminologie SKILL.md.

### E-trans-02 : Inputs

Enrichir les inputs optionnels avec les entrées spécifiques de chaque SKILL.md.

### E-trans-03 : Blocking conditions

Ajouter un bloc `blocking_conditions` dans chaque contrat reflétant les conditions du SKILL.md.

### E-trans-04 & E-trans-05 : Cosmétiques

Ajouter `finding_id_prefix` et `excludes` dans routing.