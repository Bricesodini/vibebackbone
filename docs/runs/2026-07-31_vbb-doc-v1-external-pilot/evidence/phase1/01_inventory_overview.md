# Phase 1 — Inventaire documentaire Backbone Know

> Capturé le 2026-07-31 dans le worktree `/Users/bricesodini/02_dev/backbone-know-pilot`
> (branche `pilot/vbb-doc-v1-external`, SHA `661b240`).
> Point de vue : mainteneur externe qui découvre `vbb-doc-v1` sans
> historique. Sources autorisées uniquement : `docs/DOCUMENT_CONVENTION.md`,
> documentation publique référencée, modèle d'adoption, linter canonique.

## 1. Structure documentaire d'ensemble

```
docs/
├── adr/                       # 17 ADR (ADR-0001..ADR-0017)
├── audits/                    # ~82 audits (3 formats coexistants)
├── benchmarks/                # ~73 sous-répertoires générés (t12*, model-lab)
├── engineering/               # BACKBONE_IMPLEMENTATION_PLAYBOOK + VBB_CORE_TOOLING + README
├── gates/                     # Manifestes YAML (I2_IMPLEMENTATION_GATE.yaml)
├── model-lab/                 # Données d'expérimentation
├── research-formulas/         # HYPOTHESES_F_V0.yaml + PHASE_2A_FRAME + TRACEABILITY_MATRIX
├── runs/                      # ~140 sous-répertoires de runs (formats multiples)
├── templates/                 # 01..07 + ADR + IMPACT_LOG + CANON_CHANGE_PROPOSAL
├── *.md (racine, ~33 fichiers)
│   ├── Méta : CONTEXT, PROJECT_MODE, INDEX, DECISIONS, AUDIT_STATUS, RELATIONS, ARCHITECTURE
│   ├── Produit : PRODUCT_BRIEF, V1_PRODUCT_SCOPE, PRODUCT_SEMANTIC_REQUIREMENTS_V1
│   ├── Contrats : VBB_GATE_CONTRACT_V1, INFRASTRUCTURE_GATE_CONTRACT_V1, API_CONTRACTS_V1, V1_TEST_STRATEGY
│   ├── Implémentation : IMPLEMENTATION_PLAN_V1, CREATE_ENTITY_IMPLEMENTATION_AUTHORIZATION
│   ├── Modèle : KNOWLEDGE_MODEL_V1, KNOWLEDGE_MODEL
│   ├── Recherche : POC_STRATEGY, POC_SYS_001_SYSTEM_HYPOTHESIS, RESEARCH_CONSOLIDATION_V1
│   ├── Incréments : I1_*, I2_* (7 fichiers I1 + 9 fichiers I2)
│   └── Phase : P06_CLOSEOUT_AND_PRODUCT_IMPLICATIONS
```

Total : **1524 fichiers `.md`** dans `docs/`. La majorité (benchmarks, model-lab, runs/<id>/generated) sont des **artefacts générés** ; leur statut canonique est `historical` ou à exclure du scope d'adoption.

## 2. Familles de documents et leur(s) format(s)

### 2.1 Méta-documents (racine de `docs/`)

Frontmatter canonique observé :

```yaml
---
context_role: <rôle>           # 15+ valeurs distinctes
phase: <état/cycle>            # transverse | pre_implementation | phase_0 | research-phase-1-closeout | VBB_V2_ALIGNED_BASELINE | ...
status: <statut>               # active | frozen | ACCEPTED | normative | ready | FROZEN | frozen_with_open_questions | generated | closed | planned | completed_design_only
version: <vN | vN.M | "1.0">   # optionnel
updated: <YYYY-MM-DD>          # optionnel
---
```

`RELATIONS.md` ajoute `source: ARCHITECTURE.md`.

`AUDIT_STATUS.md` ajoute `context_role: audit-status`.

`DECISIONS.md` n'a **pas de frontmatter** (table d'indexation Markdown).

### 2.2 ADR (`docs/adr/*.md`)

**Aucun frontmatter**. Format :

```markdown
# ADR-NNNN : Titre

**Date** : YYYY-MM-DD
**Status** : ACCEPTED | PROPOSED | REJECTED | SUPERSEDED
**Decider(s)** : Brice Sodini
**Supersedes** / **Superseded by** : NNNN | aucun
```

Convention : `NNN-slug.md` (kebab-case, NNN sans padding strict).

### 2.3 Audits (`docs/audits/*.md`)

**Trois formats cohabitent** :

**Format A — `kind: audit_report`**
```yaml
---
kind: audit_report
skill: <vbb-skill-id>
scope: <slug>
paths: [..]              # fichiers audités
status: READY | BLOCKED  # uppercase
date: YYYY-MM-DD
---
```

**Format B — `audit_type`**
```yaml
---
audit_type: "data-integrity"
scope: "<scope>"
status: "BLOCKED"
verdict: "INVALID_RUN"
date: "YYYY-MM-DD"
results_sha256: "<sha>"
---
```

**Format C — minimal**
```yaml
---
context_role: adversarial-audit
run_id: "<id>"
audited_commit: "<sha>"
phase: "<phase>"
status: "COMPLETED_FAIL"
verdict: "FAIL"
---
```

Les noms de fichiers utilisent deux conventions : `<skill>-<slug>-YYYYMMDD-HHMM.md`
(format A/B) et `YYYY-MM-DD_<slug>.md` (format C, aligné sur la convention runs vbb-doc-v1 §6).

### 2.4 Runs (`docs/runs/*/`)

Frontmatter canonique observé :

```yaml
---
run_id: "<YYYY-MM-DD_HHmm_slug>"
phase: "<NN_***>"
voie: "STRUCTUREE" | "AUDIT" | "RAPIDE" | "CLOTURE"  # français
route: "STRUCTUREE" | "AUDIT"                         # anglais (depuis v1.1)
status: "READY" | "PARTIAL" | "BLOCKED" | "UNKNOWN" | "FROZEN"  # uppercase + FROZEN hors-domaine
agent: "codex" | "pi" | ...
started_at: "<ISO8601>"
ended_at: "<ISO8601>"
next_phase: "<NN_***>"
artifacts_consumed: [...]
artifacts_produced: [...]
knowledge_governance_version: "1.0" | "1.1"
adversarial_level: "A0" | "A1" | "A2"   # depuis v1.1
attacker_identity:                      # depuis v1.1, A2_DISTINCT_AGENT_PROXY
  agent: "..."
  llm: "..."
  system_prompt_version: "..."
  distinct_actor: "..." | "A2_DISTINCT_AGENT_PROXY"
  external_review_eligibility: "ELIGIBLE" | "INELIGIBLE"
---
```

Sous-répertoires :
- Préfixés `YYYY-MM-DD_HHmm_` : runs datés, format conforme vbb-doc-v1 §6.
- Préfixés `_` : runs spéciaux (playbooks, alignment, preimplementations).
- Phases (legacy) : `01_INTAKE..07_CLOSEOUT`, mais aussi `01_SCOPE..09_*` (variante playbook).

### 2.5 Templates (`docs/templates/*.md.template`)

11 templates. Tous au format `01..07_*.md.template` + `ADR.md.template` + `CANON_CHANGE_PROPOSAL.md.template` + `IMPACT_LOG.md.template`.

**Pas de frontmatter** — le contenu des placeholders est `<...>`.

### 2.6 Gates (`docs/gates/`)

`I2_IMPLEMENTATION_GATE.yaml` — manifeste YAML, pas Markdown.

### 2.7 Engineering / Research-formulas

Frontmatter partiel ou absent. Plutôt considérés comme documents de référence métier.

## 3. Vocabulaire propre à Backbone Know — cartographie vbb-doc-v1

### 3.1 Types vbb-doc-v1 manquants ou ambigus

| Concept BK | Observé | Cartographie vbb-doc-v1 | Friction |
|---|---|---|---|
| `kind: audit_report` | Format A audits | `type: audit_report` | OK |
| `kind: poc-report` | POC_SYS_001 | `type: run_artifact` (un POC est un run) | PROJECT_SPECIFIC |
| `audit_type: "data-integrity"` | Format B audits | `type: audit_report` (le contenu du rapport importe, pas `audit_type`) | PROJECT_SPECIFIC |
| `context_role: <rôle>` | méta-docs | `type: reference` + `tags: [project:role:<rôle>]` | PROJECT_SPECIFIC |
| `increment: I1` / `I2` | méta-docs produit | `tags: [project:increment:I1]` | PROJECT_SPECIFIC |
| `phase: <cycle projet>` | méta-docs | `tags: [project:phase:<cycle>]` | PROJECT_SPECIFIC |

### 3.2 Statuts hors-domaine vbb-doc-v1

`vbb-doc-v1` §4 définit des domaines stricts par type. Statuts observés
dans BK qui ne mappent à aucun domaine :

| Statut BK | Type BK | Cartographie proposée | Friction |
|---|---|---|---|
| `active` | ref/gov/adoption | `active` | OK |
| `draft` | ref/gov/adoption | `draft` | OK |
| `deprecated` | ref/gov/adoption | `deprecated` | OK |
| `frozen` | ref/gov/adoption | `frozen` | OK |
| `READY` / `BLOCKED` / `PARTIAL` / `UNKNOWN` | run_artifact/audit_report | `ready` / `blocked` / `partial` / `unknown` (lowercase) | PROJECT_SPECIFIC (casse) |
| `ACCEPTED` / `PROPOSED` / `REJECTED` / `SUPERSEDED` | adr/decision_record | `accepted` / `proposed` / `rejected` / `superseded` (lowercase) | PROJECT_SPECIFIC (casse) |
| `FROZEN` (run) | run_artifact | HORS DOMAINE — un run n'est pas `frozen` | CONTRACT_AMBIGUITY |
| `generated` (RELATIONS.md) | référence générée | HORS DOMAINE | CONTRACT_AMBIGUITY |
| `completed_design_only` (POC_SYS_001) | poc-report | HORS DOMAINE | CONTRACT_AMBIGUITY |
| `closed` (P06) | research-closeout | HORS DOMAINE | CONTRACT_AMBIGUITY |
| `planned` (POC_STRATEGY) | poc-strategy | HORS DOMAINE | CONTRACT_AMBIGUITY |
| `normative` (API_CONTRACTS_V1) | api-contract | HORS DOMAINE | CONTRACT_AMBIGUITY |
| `frozen_with_open_questions` (RESEARCH) | research | HORS DOMAINE | CONTRACT_AMBIGUITY |

**Conséquence** : un mainteneur externe doit **deviner** la cartographie pour 8+ statuts
composés/spéciaux. Le contrat ne propose pas de guidance explicite (LINTER_GAP).

### 3.3 Vocabulaire de tags BK

BK n'utilise pas de tags explicites ; les classes sont implicites via
`context_role`, `phase`, `kind`, `audit_type`. Cartographie suggérée :

| BK | vbb-doc-v1 |
|---|---|
| `context_role: moc` | `tags: [project:role:moc]` |
| `context_role: project-mode` | `tags: [project:role:project-mode]` |
| `context_role: index` | `tags: [project:role:index]` |
| `context_role: audit-status` | `tags: [project:role:audit-status, audit]` |
| `context_role: architecture-relations` | `tags: [project:role:architecture-relations, architecture]` |
| `context_role: canonical-architecture` | `tags: [project:role:canonical-architecture, architecture]` |
| `context_role: product-scope` | `tags: [project:role:product-scope]` |
| `context_role: api-contract` | `tags: [project:role:api-contract, contract]` |
| `context_role: implementation-plan` | `tags: [project:role:implementation-plan, architecture]` |
| `context_role: product-brief` | `tags: [project:role:product-brief]` |
| `context_role: increment-baseline` | `tags: [project:role:increment-baseline]` |
| `context_role: research-closeout` | `tags: [project:role:research-closeout]` |
| `context_role: poc-strategy` | `tags: [project:role:poc-strategy, research]` |
| `context_role: research-consolidation` | `tags: [project:role:research-consolidation, research]` |
| `context_role: adversarial-audit` | `tags: [project:role:adversarial-audit, audit]` |
| `kind: poc-report` | `tags: [project:kind:poc-report]` |
| `audit_type: data-integrity` | `tags: [project:audit-type:data-integrity, audit]` |

**Conséquence** : le vocabulaire de BK peut rester **comme extension
namespacée `project:`**. Aucun effacement forcé n'est nécessaire.

### 3.4 Vocabulaire de phase / cycle / voie

- `phase` (BK) cycle projet : `transverse`, `pre_implementation`, `phase_0`,
  `research-phase-1-closeout`, `VBB_V2_ALIGNED_BASELINE`. Cartographie :
  `tags: [project:phase:<valeur>]`.
- `phase` (run-level BK) numéro d'étape : `01_INTAKE`, `02_AUDIT`, etc.
  Cartographie : dimension conservée (le contrat vbb-doc-v1 §3 ne l'interdit
  pas pour `run_artifact`).
- `voie` (BK) vs `route` (VBB) : synonymes informels. Cartographie : la
  dimension `route` existe déjà dans `02_AUDIT_REPORT.md.template` du VBB
  (cf. `docs/templates/`), donc aligner sur `route`.

### 3.5 Vocabulaire agent / LLM (depuis v1.1)

BK utilise déjà `agent`, `adversarial_level`, `attacker_identity`. Cartographie
identique : dimensions conservées hors frontmatter canonique vbb-doc-v1.

## 4. Documents représentatifs sélectionnés pour Phase 2

| # | Catégorie vbb-doc-v1 | Fichier BK | Justification |
|---|---|---|---|
| 1 | Document public principal | `docs/PRODUCT_BRIEF.md` | Entrée projet, phase_0, active, audience publique |
| 2 | Document d'architecture/référence | `docs/ARCHITECTURE.md` | Source canonique d'architecture, transverse, active |
| 3 | Document opérationnel | `docs/VBB_GATE_CONTRACT_V1.md` | Contrat de gate, ACCEPTED, opérationnel runtime |
| 4 | Document expérimental/recherche | `docs/POC_SYS_001_SYSTEM_HYPOTHESIS.md` | POC, `kind: poc-report`, `completed_design_only` |
| 5 | Document historique/déprécié | `docs/RELATIONS.md` | `status: generated` (fichier dérivé automatique), pas un frontmatter actif typique |

## 5. Contradictions, doublons et inclassables

### 5.1 Doublons

- `KNOWLEDGE_MODEL.md` (16 KB) et `KNOWLEDGE_MODEL_V1.md` (15 KB) : versions successives, à clarifier.
- `ARCHITECTURE.md` vs `RELATIONS.md` (généré) — RELATIONS est explicitement dérivé.
- ADR `0009` (runtime vertical slice v1) et ADR `0011..0013` (I1, I2 entity, I2 UpdateEntity) — séquence cohérente mais à tracer.

### 5.2 Inclassables directs (sans ajout de namespace)

- `RELATIONS.md` (`status: generated`) : n'a pas d'équivalent vbb-doc-v1 §2 ni §4. Solution proposée : `type: reference` + `status: frozen` (c'est figé car généré) + `tags: [project:role:architecture-relations, architecture, project:source:generated]` + relation vers `ARCHITECTURE.md`.
- ADR sans frontmatter : doit gagner un frontmatter conforme (champ obligatoire manquant).
- Audits aux trois formats : ne peuvent pas tous migrer sans perte ; il faut choisir entre préserver `kind`/`audit_type` comme tag namespacés OU comme métadonnée hors-convention.

### 5.3 Éléments difficiles à classer

- `phase` run-level (`01_INTAKE`..`09_*`) : le contrat ne le définit pas formellement comme champ obligatoire, juste comme "required" pour run_artifact. La sémantique locale (numéro d'étape de processus) n'est pas spécifiée.
- `voie` vs `route` : deux clés pour la même idée. Le contrat ne précise pas laquelle est canonique pour vbb-doc-v1.
- Statuts composés (`frozen_with_open_questions`, `completed_design_only`) : le contrat ne propose pas de mécanisme d'extension de domaine (un namespace `project:status:` ?).

## 6. Ordre de lecture réel observé

D'après `INDEX.md` et la pratique des runs VBB :

1. `PRODUCT_BRIEF.md` (entrée projet)
2. `CONTEXT.md` (MOC, routeur)
3. `PROJECT_MODE.md` (mode DEV/PROD)
4. `INDEX.md` (catalogue)
5. `V1_PRODUCT_SCOPE.md`, `PRODUCT_SEMANTIC_REQUIREMENTS_V1.md` (périmètre V1)
6. `ARCHITECTURE.md` (source canonique archi)
7. `RELATIONS.md` (projection générée)
8. `API_CONTRACTS_V1.md`, `VBB_GATE_CONTRACT_V1.md`, `INFRASTRUCTURE_GATE_CONTRACT_V1.md` (contrats)
9. `TECHNICAL_SPECIFICATION_I1.md` / `TECHNICAL_SPECIFICATION_I2.md` (spécifications incréments)
10. `IMPLEMENTATION_PLAN_V1.md` (plan global)
11. `audits/` et `runs/` (évidence)

Cet ordre **contredit partiellement** l'ordre canonique vbb-doc-v1 §7 :

| vbb-doc-v1 §7 | BK observé |
|---|---|
| 1. adoption declaration | absent (à créer) |
| 2. this contract | absent (à créer) |
| 3. project context and mode | (3) mais pas premier |
| 4. pilotage/routing | pas matérialisé en doc |
| 5. architecture and conventions | (6) |
| 6. active decision/ADR and audit evidence | `DECISIONS.md` + ADR (8) |
| 7. run artifacts and closeout | `runs/` (11) |
| 8. historical/archive material only as evidence | pas isolé |

→ **Friction DOCUMENTATION_GAP** : l'ordre canonique vbb-doc-v1 §7 n'est pas
imposé par un mécanisme technique. BK le satisfait **approximativement**
parce que la pratique le suit, mais un mainteneur découvrant les deux
univers en parallèle n'a pas de garantie qu'ils coïncident.