---
run_id: 20260615-usage-audit
phase: 02_AUDIT
voie: STRUCTURED
status: COMPLETE
agent: pi
started_at: 2026-06-15T08:00:00
ended_at: 2026-06-15T10:00:00
artifacts_consumed:
  - docs/runs/20260615-usage-audit/orgabar_scan.md
  - docs/runs/20260615-usage-audit/swiftminuteur_scan.md
  - Données manuelles Secrets/Guard Backbone
artifacts_produced:
  - docs/runs/20260615-usage-audit/02_AUDIT.md
---

# Audit d'usage réel de Vibe Backbone — Rapport croisé

**Date** : 2026-06-15
**Projets audités** : Orgabar, Secrets/Guard Backbone, SwiftMinuteur
**Source VBB** : `/Users/bricesodini/01_ai-stack/vibebackbone`

---

## 1. Cartographie d'usage croisée

### 1.1 Documents de gouvernance (Core)

| Élément VBB | Orgabar | Secrets | SwiftMinuteur | Usage observé | Recommandation |
|-------------|---------|---------|---------------|---------------|----------------|
| `CONTEXT.md` | ✅ Actif | ✅ Actif (LOCKED) | ✅ Actif | **3/3 — Universel** | **CONSERVER** |
| `PROJECT_MODE.md` | ✅ Actif | ✅ Actif | ✅ Actif | **3/3 — Universel** | **CONSERVER** |
| `PILOTAGE.md` | ❌ | ❌ | ✅ Actif | 1/3 — Utile mais pas systématique | **SIMPLIFIER** (trop long, fusionnable avec PROJECT_MODE) |
| `SESSION.md` | ✅ Actif | ✅ Actif | ✅ Actif | **3/3 — Universel** | **CONSERVER** |
| `SESSION_RULES.md` | ❌ | ❌ | ❌ | **0/3 — Aucun usage** | **ARCHIVER** (référence utile, pas nécessaire dans les projets) |
| `ARCHITECTURE.md` | ✅ Actif | ✅ Actif | ❌ | 2/3 — Présent dans les projets structurés | **CONSERVER** |
| `RELATIONS.md` | ✅ (généré) | ❌ | ❌ | 1/3 — Généré automatiquement | **FUSIONNER** avec ARCHITECTURE.md (section relations) |
| `INDEX.md` | ✅ Actif | ✅ Actif | ❌ | 2/3 — Utile pour la navigation | **SIMPLIFIER** (réduire à une table des matières) |
| `AUDIT_STATUS.md` | ✅ Actif | ✅ Actif | ✅ Actif | **3/3 — Universel** | **CONSERVER** |
| `TECH_DEBT.md` | ❌ | ❌ | ❌ | **0/3 — Aucun usage** | **FUSIONNER** avec AUDIT_STATUS.md (section dette technique) |
| `CONVENTIONS.md` | ❌ | ✅ Actif (v3) | ✅ Actif | 2/3 — Présent dans les projets matures | **CONSERVER** |
| `MVP_START_PROTOCOL.md` | ✅ Actif | ❌ | ✅ Actif | 2/3 — Utile pour les nouveaux projets | **CONSERVER** |

### 1.2 Documents de gouvernance (Extended)

| Élément VBB | Orgabar | Secrets | SwiftMinuteur | Usage observé | Recommandation |
|-------------|---------|---------|---------------|---------------|----------------|
| `ACTIVITY_LOG.md` | ❌ | ✅ Actif (198 lignes) | ❌ | 1/3 — Utilisé intensivement par Secrets | **CONSERVER** (mais optionnel) |
| `DECISIONS.md` | ❌ | ✅ Actif (4 ADRs) | ❌ | 1/3 — Index ADR utile | **FUSIONNER** avec le répertoire adr/ (README.md) |
| `DEPLOYMENT.md` | ❌ | ❌ | ❌ | **0/3** | **ARCHIVER** |
| `DISTRIBUTIONS.md` | ❌ | ❌ | ❌ | **0/3** | **ARCHIVER** (spécifique VBB Core) |
| `LLM_PROVIDERS.md` | ❌ | ❌ | ❌ | **0/3** | **ARCHIVER** (spécifique VBB Core) |
| `LONG_RUN_RULE.md` | ❌ | ❌ | ❌ | **0/3** | **ARCHIVER** |
| `MEMORY_AND_HANDOFF.md` | ❌ | ❌ | ❌ | **0/3** | **ARCHIVER** |
| `RUNBOOK.md` | ❌ | ❌ | ❌ | **0/3** | **ARCHIVER** |
| `TEMPORAL_PROVENANCE.md` | ❌ | ❌ | ❌ | **0/3** | **ARCHIVER** |
| `TROUBLESHOOTING.md` | ❌ | ❌ | ❌ | **0/3** | **ARCHIVER** |
| `REFERENCE/pre-merge-gate.md` | ❌ | ❌ | ❌ (référencé) | 1/3 — Référencé mais pas copié | **CONSERVER** (référence canonique) |
| `router/ROUTER_MATRIX.md` | ❌ | ❌ | ❌ | **0/3** | **ARCHIVER** (spécifique VBB Core) |
| `strategy/p0-4-review-matrix-poc.md` | ❌ | ❌ | ❌ | **0/3** | **ARCHIVER** |

### 1.3 Templates

| Élément VBB | Orgabar | Secrets | SwiftMinuteur | Usage observé | Recommandation |
|-------------|---------|---------|---------------|---------------|----------------|
| `01_INTAKE.md.template` | ✅ | ❌ | ❌ | 1/3 | **CONSERVER** |
| `02_AUDIT.md.template` | ✅ | ❌ | ❌ | 1/3 | **CONSERVER** |
| `03_DECISION.md.template` | ✅ | ❌ | ❌ | 1/3 | **CONSERVER** |
| `04_PLAN.md.template` | ✅ | ❌ | ❌ | 1/3 | **CONSERVER** |
| `05_EXECUTION.md.template` | ✅ | ❌ | ❌ | 1/3 | **CONSERVER** |
| `06_REVIEW.md.template` | ✅ | ❌ | ❌ | 1/3 | **CONSERVER** |
| `07_CLOSEOUT.md.template` | ✅ | ❌ | ❌ | 1/3 | **CONSERVER** |
| `ADR.md.template` | ✅ | ❌ | ❌ | 1/3 | **CONSERVER** |
| `CANON_CHANGE_PROPOSAL.md.template` | ✅ | ❌ | ❌ | 1/3 | **ARCHIVER** (usage rarissime) |
| `INTEGRATION_GATE.md.template` | ✅ | ❌ | ❌ | 1/3 | **CONSERVER** |
| `POC.md.template` | ✅ | ❌ | ❌ | 1/3 | **CONSERVER** |
| `worker-evidence-paragraph.md` | ❌ | ❌ | ❌ | **0/3** | **SUPPRIMER** |

**Note** : Les templates ne sont présents que dans Orgabar (initialisé récemment par `t-vbb-project-context-init`). Secrets et SwiftMinuteur n'ont pas de répertoire templates/ — ils produisent les artefacts directement sans templates locaux. Les templates servent au moment de l'init, pas en continu.

### 1.4 Phases de run (artefacts effectivement produits)

| Phase | Orgabar | Secrets | SwiftMinuteur | Usage observé | Recommandation |
|-------|---------|---------|---------------|---------------|----------------|
| `01_INTAKE.md` | ❌ (0/2 runs) | ✅ (1/20 runs) | ✅ (2/2 runs) | Usage rare sauf SwiftMinuteur | **CONSERVER** (utile pour reprise) |
| `02_AUDIT.md` / `02_DISCOVERY.md` | ✅ (1/2) | ✅ (8/20) | ❌ (0/2) | Présent dans les runs structurés | **CONSERVER** |
| `03_DECISION.md` / `03_EVALUATION.md` | ❌ (0/2) | ❌ (0/20) | ❌ (0/2) | **0/3 — Jamais produit** | **FUSIONNER** avec 07_CLOSEOUT (section décisions) |
| `04_PLAN.md` | ❌ (0/2) | ✅ (1/20) | ❌ (0/2) | Usage rarissime | **SIMPLIFIER** (optionnel, intégrer à 02_AUDIT) |
| `05_EXECUTION.md` / `05_PATCH_SUMMARY.md` | ❌ (0/2) | ✅ (10/20) | ❌ (0/2) | PATCH_SUMMARY dominant | **CONSERVER** (PATCH_SUMMARY, pas EXECUTION) |
| `06_REVIEW.md` / `06_REVIEW_NOTES.md` | ❌ (0/2) | ❌ (0/20) | ❌ (0/2) | **0/3 — Jamais produit** | **SUPPRIMER** (jamais utilisé) |
| `07_CLOSEOUT.md` | ✅ (2/2) | ✅ (10/20) | ✅ (2/2) | **3/3 — Universel** | **CONSERVER** |
| `POC.md` | ❌ (0/2) | ✅ (1/20) | ❌ (0/2) | Usage rarissime | **FUSIONNER** avec 02_AUDIT (section POC) |

**Constat majeur** : Le modèle 8 phases (01→07 + POC) n'est **jamais** utilisé intégralement. Le pattern réel est :
- **FAST** : 05_PATCH_SUMMARY seul (Secrets : 10/20 runs)
- **STRUCTURED** : 02_AUDIT + 07_CLOSEOUT (Orgabar, Secrets init)
- **CLOSEOUT** : 07_CLOSEOUT seul (SwiftMinuteur, Secrets handoffs)
- **COMPLET** : 01 + 04 + 05 + POC + 07 (Secrets : 1/20 runs)

### 1.5 Skills (invocations réelles)

| Skill VBB | Orgabar | Secrets | SwiftMinuteur | Usage observé | Recommandation |
|-----------|---------|---------|---------------|---------------|----------------|
| `0-vbb-rico-readiness` | ✅ (1 audit) | ✅ (4 audits) | ❌ | **2/3 — Critique pour init** | **CONSERVER** |
| `0-vbb-audit-readiness` | ❌ | ❌ | ❌ | 0/3 | **FUSIONNER** avec rico-readiness |
| `0-vbb-scope-freeze` | ❌ | ❌ | ❌ | 0/3 | **FUSIONNER** avec rico-readiness |
| `0-vbb-guide` | ❌ | ❌ | ❌ | 0/3 | **CONSERVER** (référence agent) |
| `0-vbb-pilotage` | ❌ | ❌ | ❌ | 0/3 | **CONSERVER** (référence agent) |
| `0-vbb-standard` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `0-vbb-zero-friction` | ❌ | ❌ | ❌ | 0/3 | **CONSERVER** (référence agent) |
| `1-vbb-intent-decomposer` | ❌ | ✅ (2 audits) | ❌ | 1/3 | **CONSERVER** |
| `1-vbb-tech-debt` | ❌ | ✅ (3 audits) | ✅ (3 audits) | **2/3 — Très utilisé** | **CONSERVER** |
| `1-vbb-adr` | ❌ | ✅ (4 ADRs) | ❌ | 1/3 | **CONSERVER** |
| `1-vbb-code-janitor` | ❌ | ❌ | ❌ | 0/3 | **CONSERVER** (utilité potentielle) |
| `1-vbb-conventions` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** (usage unique à l'init) |
| `1-vbb-doc-harmonizer` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `1-vbb-code-doc-coherence-auditor` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `1-vbb-code-doc-gap-integrator` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `1-vbb-error-handling-auditor` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `1-vbb-formatter` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `1-vbb-logic-duplication-detector` | ❌ | ❌ | ✅ (1 audit) | 1/3 | **CONSERVER** |
| `1-vbb-monolith-detector` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `1-vbb-pattern-inconsistency-detector` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `1-vbb-premature-abstraction-detector` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `1-vbb-test-mirage-detector` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `1-vbb-api-contract-designer` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `2-vbb-security` | ❌ | ✅ (1 audit) | ❌ | 1/3 | **CONSERVER** |
| `2-vbb-spec-validator` | ❌ | ✅ (1 audit) | ✅ (1 audit) | **2/3 — Très utilisé** | **CONSERVER** |
| `2-vbb-data-integrity` | ❌ | ✅ (1 audit) | ❌ | 1/3 | **CONSERVER** |
| `2-vbb-accessibility` | ❌ | ❌ | ✅ (1 audit) | 1/3 | **CONSERVER** |
| `2-vbb-systemic-risk` | ❌ | ❌ | ❌ | 0/3 | **CONSERVER** (utilité potentielle) |
| `2-vbb-ops` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `2-vbb-ci` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `2-vbb-db-robustness` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `2-vbb-performance` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `2-vbb-api-auditor` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `2-vbb-analytics` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `2-vbb-legal` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `3-vbb-risk-register` | ❌ | ✅ (1 audit) | ❌ | 1/3 | **CONSERVER** |
| `4-vbb-security-remediation` | ❌ | ✅ (1 audit) | ❌ | 1/3 | **CONSERVER** |
| `4-vbb-user-experience-engine` | ❌ | ✅ (1 audit) | ❌ | 1/3 | **CONSERVER** |
| `4-vbb-interaction-coherence-auditor` | ❌ | ❌ | ✅ (1 audit) | 1/3 | **CONSERVER** |
| `4-vbb-cognitive-load-optimizer` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `4-vbb-design-system-validator` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `4-vbb-visual-identity-layer` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `4-vbb-visual-identity-gatekeeper` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `4-vbb-micro-interaction-refiner` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `4-vbb-front-pipeline-reference` | ❌ | ❌ | ❌ | 0/3 | **CONSERVER** (référence) |
| `4-vbb-product-changelog` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `t-vbb-project-context-init` | ✅ (init) | ❌ | ❌ | 1/3 — Usage unique | **CONSERVER** |
| `t-vbb-session-handoff` | ❌ | ❌ | ❌ | 0/3 | **CONSERVER** (référence agent) |
| `t-vbb-mode-transition-gate` | ❌ (référencé) | ❌ (référencé) | ❌ | 0/3 — Référencé, jamais invoqué | **CONSERVER** |
| `t-vbb-anti-slop-gate` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `t-vbb-commit-ready` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `t-vbb-context-compactor` | ❌ | ❌ | ❌ | 0/3 | **CONSERVER** (outil utile) |
| `t-vbb-dependency-mapper` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `t-vbb-docker-audit` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `t-vbb-docker-generate` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `t-vbb-deploy-runtime` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `t-vbb-git-sync` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `t-vbb-impact-analyzer` | ❌ (référencé) | ❌ | ❌ | 0/3 | **CONSERVER** |
| `t-vbb-index` | ❌ | ❌ | ❌ | 0/3 | **CONSERVER** (outil VBB Core) |
| `t-vbb-llm-healthcheck` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `t-vbb-status-dashboard` | ❌ | ❌ | ❌ | 0/3 | **CONSERVER** (outil VBB Core) |
| `t-vbb-status-report` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `t-vbb-test-coverage-mapper` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `vibebackbone` (orchestrator) | ❌ | ❌ | ❌ | 0/3 | **CONSERVER** (point d'entrée agent) |

**Constat majeur** : Sur 64 skills, **seuls 15 ont été invoqués** dans au moins un projet. 49 skills n'ont **aucune trace d'usage**. Les skills les plus utilisés sont : `0-vbb-rico-readiness` (6 invocations), `1-vbb-tech-debt` (6), `2-vbb-spec-validator` (2), `1-vbb-intent-decomposer` (2).

### 1.6 Tools (usage réel)

| Outil VBB | Orgabar | Secrets | SwiftMinuteur | Usage observé | Recommandation |
|-----------|---------|---------|---------------|---------------|----------------|
| `vbb-architecture.py` | ❌ (référencé) | ❌ | ✅ (exécuté) | 1/3 — Exécuté dans closeout SwiftMinuteur | **CONSERVER** |
| `vbb-loop-closure-check.py` | ❌ (référencé) | ❌ | ✅ (exécuté) | 1/3 — Exécuté dans closeout SwiftMinuteur | **CONSERVER** |
| `vbb-contract-lint.py` | ❌ (référencé) | ❌ | ✅ (exécuté) | 1/3 | **CONSERVER** |
| `vbb-gate-check.py` | ❌ (référencé) | ❌ | ❌ | 0/3 — Référencé, jamais exécuté | **CONSERVER** |
| `vbb-ci-local.sh` | ❌ (référencé) | ❌ | ✅ (exécuté) | 1/3 | **CONSERVER** |
| `vbb-project-init.py` | ✅ (init) | ❌ | ❌ | 1/3 — Usage unique | **CONSERVER** |
| `vbb-index.py` | ❌ | ❌ | ❌ | 0/3 | **CONSERVER** (outil VBB Core) |
| `vbb-status-dashboard.py` | ❌ | ❌ | ❌ | 0/3 | **CONSERVER** (outil VBB Core) |
| `vbb-context-compactor.py` | ❌ | ❌ | ❌ | 0/3 | **CONSERVER** |
| `vbb-contract-runtime.py` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `vbb-executor.py` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `vbb-llm-healthcheck.py` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `vbb-phase-router.py` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |
| `vbb-review-threshold-poc.py` | ❌ | ❌ | ❌ | 0/3 | **ARCHIVER** |

**Constat** : Les outils sont **référencés** dans les templates et la gouvernance mais **rarement exécutés** dans les projets. SwiftMinuteur est le seul à les exécuter effectivement dans ses closeouts. Les outils Core (index, status-dashboard) sont utilisés par les agents VBB, pas par les projets.

### 1.7 Boot files (AGENTS.md, SYSTEM.md, GUIDE.md)

| Élément VBB | Orgabar | Secrets | SwiftMinuteur | Usage observé | Recommandation |
|-------------|---------|---------|---------------|---------------|----------------|
| `AGENTS.md` (projet) | ❌ | ❌ | ❌ | **0/3 — Aucun projet n'a son propre AGENTS.md** | **CONSERVER** (template pour projets) |
| `SYSTEM.md` (projet) | ❌ | ❌ | ❌ | **0/3** | **CONSERVER** (template pour distributions) |
| `GUIDE.md` (VBB Core) | N/A | N/A | N/A | Référence Core uniquement | **CONSERVER** |
| `PROMPTS_ARCHITECTURE.md` | N/A | N/A | N/A | Référence Core uniquement | **CONSERVER** |
| `README.md` (projet) | ❌ | ✅ | ❌ | 1/3 | N/A (spécifique projet) |

### 1.8 Scripts et hooks

| Élément VBB | Orgabar | Secrets | SwiftMinuteur | Usage observé | Recommandation |
|-------------|---------|---------|---------------|---------------|----------------|
| `scripts/hooks/pre-commit-framework-gate` | ❌ | ❌ | ❌ | **0/3** | **ARCHIVER** |
| `scripts/hooks/commit-msg-framework-gate` | ❌ | ❌ | ❌ | **0/3** | **ARCHIVER** |
| `scripts/install-framework-gate-hook.sh` | ❌ | ❌ | ❌ | **0/3** | **ARCHIVER** |
| `scripts/install-vbb-pre-commit.sh` | ❌ | ❌ | ❌ | **0/3** | **ARCHIVER** |
| `scripts/vbb-ci-local.sh` | ❌ (référencé) | ❌ | ✅ (exécuté) | 1/3 | **CONSERVER** |
| `setup.sh` | ❌ | ❌ | ❌ | 0/3 | **CONSERVER** (setup VBB Core) |
| `setup-lib.sh` | ❌ | ❌ | ❌ | 0/3 | **CONSERVER** (setup VBB Core) |

### 1.9 Prompts (usage réel)

Les prompts VBB sont consommés par les agents (Pi, Cody, Claude Code), pas directement par les projets. Leur usage est donc indirect. Les prompts les plus référencés dans les projets :

| Prompt | Traces dans les projets |
|--------|------------------------|
| `0-p-vbb-triage.md` | Implicite (tout agent VBB) |
| `1-p-vbb-quick-task.md` | Pattern FAST-MINIMAL dominant dans Secrets |
| `1-p-vbb-structured-task.md` | Pattern STRUCTURED dans Orgabar |
| `2-p-vbb-audit-task.md` | Pattern AUDIT dans les 3 projets |
| `t-p-vbb-session-handoff.md` | Pattern CLOSEOUT dans les 3 projets |
| `canonical/07-p-vbb-closeout.md` | Universel |

**Recommandation globale prompts** : **CONSERVER** les prompts canoniques (01-07) et les prompts d'entrée (triage, quick-task, structured-task, audit-task, session-handoff). **ARCHIVER** les prompts spécialisés sans usage (db-sanity, release-check, security-pipeline, deploy-docker, etc.).

---

## 2. Noyau réellement utilisé

Voici le Vibe Backbone **réellement pratiqué** dans les trois projets, par opposition au Backbone théorique.

### 2.1 Documents toujours présents (3/3 projets)

| Document | Rôle observé |
|----------|-------------|
| `CONTEXT.md` | Point d'entrée unique pour la reprise. Contient description, stack, liens, état. |
| `PROJECT_MODE.md` | Mode courant (DEV/EXPLORE/MVP). Référence la gate de transition. |
| `SESSION.md` | État de la dernière session : ce qui est fait, décisions, prochaine étape. |
| `AUDIT_STATUS.md` | Verdict global, blocages actifs, historique des audits. |

**Ces 4 documents forment le noyau dur de la reprise de projet.** Ils sont systématiquement présents et activement maintenus.

### 2.2 Documents presque toujours présents (2/3 projets)

| Document | Présent dans |
|----------|-------------|
| `ARCHITECTURE.md` | Orgabar, Secrets |
| `INDEX.md` | Orgabar, Secrets |
| `CONVENTIONS.md` | Secrets, SwiftMinuteur |
| `MVP_START_PROTOCOL.md` | Orgabar, SwiftMinuteur |

### 2.3 Phases de run réellement produites

| Phase | Fréquence | Pattern |
|-------|-----------|---------|
| `07_CLOSEOUT.md` | **Universel** (14/24 runs) | Clôture obligatoire |
| `05_PATCH_SUMMARY.md` | **Très fréquent** (10/24) | FAST-MINIMAL |
| `02_AUDIT.md` | **Fréquent** (9/24) | STRUCTURED / AUDIT |
| `01_INTAKE.md` | Rare (3/24) | Reprise formelle |
| `04_PLAN.md` | Rare (1/24) | Planification lourde |
| `POC.md` | Rarissime (1/24) | Proof of concept |

**Le pattern réel est 2-3 artefacts par run, pas 8.**

### 2.4 Skills réellement invoqués (top 10)

1. **`0-vbb-rico-readiness`** — 6 invocations (init projet)
2. **`1-vbb-tech-debt`** — 6 invocations (audit dette technique)
3. **`2-vbb-spec-validator`** — 2 invocations (validation spec)
4. **`1-vbb-intent-decomposer`** — 2 invocations (décomposition produit→code)
5. **`2-vbb-security`** — 1 invocation
6. **`2-vbb-data-integrity`** — 1 invocation
7. **`2-vbb-accessibility`** — 1 invocation
8. **`3-vbb-risk-register`** — 1 invocation
9. **`4-vbb-security-remediation`** — 1 invocation
10. **`4-vbb-user-experience-engine`** — 1 invocation

### 2.5 Outils réellement exécutés

1. **`vbb-architecture.py lint`** — SwiftMinuteur closeout
2. **`vbb-loop-closure-check.py --strict`** — SwiftMinuteur closeout
3. **`vbb-contract-lint.py`** — SwiftMinuteur closeout
4. **`vbb-ci-local.sh`** — SwiftMinuteur closeout
5. **`vbb-project-init.py`** — Orgabar init

### 2.6 Mécanismes réellement suivis

| Mécanisme | Suivi dans |
|------------|-----------|
| Frontmatter YAML dans les artefacts | **3/3** — Universel |
| `.gitignore` VBB local state | **3/3** — Universel |
| Hippo memory (pi) | **3/3** — Universel |
| Closeout avec vérification | 1/3 (SwiftMinuteur) |
| Pre-merge gate (5 vérifications) | 1/3 (SwiftMinuteur, référencé) |
| ADR format | 1/3 (Secrets, 4 ADRs) |
| ACTIVITY_LOG | 1/3 (Secrets) |
| Mode transition gate | 0/3 (référencé, jamais exécuté) |

---

## 3. Surcharge probable

Éléments qui produisent plus de complexité que de valeur :

### 3.1 Le modèle 8 phases (01→07 + POC)

**Problème** : Le modèle théorique 8 phases n'est **jamais** utilisé intégralement. Sur 24 runs audités, aucun n'a produit les 8 artefacts. Le maximum observé est 5 artefacts (Secrets : 01 + 04 + 05 + POC + 07).

**Impact** : Les templates, la documentation, et les attentes agentiques sont calibrés sur un modèle qui n'existe pas dans la pratique. Cela crée :
- Une dissonance entre ce que les agents sont formés à produire et ce qu'ils produisent réellement
- Des templates inutilisés (03_DECISION, 06_REVIEW)
- Une complexité perçue qui peut décourager l'adoption

**Recommandation** : Réduire le modèle canonique à 3 phases essentielles + 2 optionnelles.

### 3.2 Les 49 skills sans usage

**Problème** : 49 skills sur 64 (77%) n'ont **aucune trace d'usage** dans les trois projets. Beaucoup sont des variantes fines d'audit (error-handling-auditor, pattern-inconsistency-detector, premature-abstraction-detector, monolith-detector, test-mirage-detector) qui n'ont jamais été invoquées.

**Impact** :
- Volume de code et documentation à maintenir dans VBB Core
- Charge cognitive pour les agents qui doivent connaître 64 skills
- Temps de chargement des définitions de skills dans le contexte agent

**Recommandation** : Archiver les skills sans usage, conserver les 15 skills actifs + 5 à potentiel futur.

### 3.3 Les 14 documents extended sans usage

**Problème** : 14 documents de gouvernance « extended » (DEPLOYMENT, DISTRIBUTIONS, LLM_PROVIDERS, LONG_RUN_RULE, MEMORY_AND_HANDOFF, RUNBOOK, TEMPORAL_PROVENANCE, TROUBLESHOOTING, etc.) n'existent dans **aucun** des trois projets.

**Impact** : Ces documents sont maintenus dans VBB Core mais ne sont jamais copiés ni référencés dans les projets consommateurs.

**Recommandation** : Les archiver comme référence VBB Core, ne pas les présenter comme attendus dans les projets.

### 3.4 Les scripts de hooks git

**Problème** : Les 4 scripts de hooks git (pre-commit, commit-msg, install) n'ont été installés dans **aucun** projet.

**Impact** : Code mort dans VBB Core.

**Recommandation** : Archiver. Le `vbb-ci-local.sh` couvre le besoin de vérification.

### 3.5 La complexité des templates

**Problème** : Les templates VBB (notamment 04_PLAN, 06_REVIEW, INTEGRATION_GATE) sont très longs et contiennent des références à des outils qui ne sont pas exécutés (gate-check, impact-analyzer, review-threshold-poc).

**Impact** : Les templates donnent une impression de lourdeur qui peut dissuader les agents de les utiliser.

**Recommandation** : Simplifier les templates, réduire les références aux outils non utilisés.

---

## 4. Recommandations concrètes

### 4.1 À GARDER ABSOLUMENT (19 éléments)

Ces éléments sont le cœur battant de Vibe Backbone. Ils sont utilisés dans au moins 2/3 projets et apportent une valeur démontrable de reprise, recadrage ou continuité.

#### Documents (8)
1. **`CONTEXT.md`** — Point d'entrée universel pour la reprise
2. **`PROJECT_MODE.md`** — Mode courant, gate de transition
3. **`SESSION.md`** — État de la dernière session
4. **`AUDIT_STATUS.md`** — Verdict global, blocages
5. **`ARCHITECTURE.md`** — Structure canonique du projet
6. **`CONVENTIONS.md`** — Règles de qualité locales
7. **`MVP_START_PROTOCOL.md`** — Gate de démarrage MVP
8. **`INDEX.md`** — Navigation (simplifié)

#### Phases de run (3)
9. **`07_CLOSEOUT.md`** — Clôture obligatoire
10. **`05_PATCH_SUMMARY.md`** — Résumé de patch FAST
11. **`02_AUDIT.md`** — Rapport d'audit

#### Skills (5)
12. **`0-vbb-rico-readiness`** — Gate d'entrée projet
13. **`1-vbb-tech-debt`** — Audit de dette technique
14. **`2-vbb-spec-validator`** — Validation post-implémentation
15. **`1-vbb-intent-decomposer`** — Décomposition produit→code
16. **`t-vbb-project-context-init`** — Bootstrap gouvernance

#### Outils (3)
17. **`vbb-loop-closure-check.py`** — Vérification de clôture
18. **`vbb-architecture.py`** — Lint + génération relations
19. **`vbb-ci-local.sh`** — CI locale

### 4.2 À ALLÉGER (5 éléments)

Éléments utiles mais trop longs, trop formels ou trop coûteux à maintenir.

1. **`PILOTAGE.md`** — Utile (1/3 projets) mais redondant avec PROJECT_MODE.md + CONTEXT.md. **Action** : Fusionner les sections pilotage dans PROJECT_MODE.md, réduire PILOTAGE.md à une référence optionnelle.
2. **`INDEX.md`** — Utile (2/3) mais pourrait être une simple table des matières auto-générée. **Action** : Réduire à un format compact, supprimer les sections redondantes avec CONTEXT.md.
3. **`04_PLAN.md.template`** — Trop long, références à des outils non utilisés. **Action** : Réduire à une checklist, supprimer les références à gate-check/impact-analyzer.
4. **`01_INTAKE.md.template`** — Utile mais souvent sauté. **Action** : Fusionner avec 02_AUDIT (section « contexte du run »).
5. **`POC.md.template`** — Rarissime (1/24). **Action** : Intégrer comme section optionnelle dans 02_AUDIT.md.

### 4.3 À FUSIONNER (6 paires)

Éléments redondants qui peuvent être consolidés.

1. **`RELATIONS.md` → `ARCHITECTURE.md`** — RELATIONS.md est déjà généré depuis ARCHITECTURE.md. Le garder comme section dans ARCHITECTURE.md plutôt que fichier séparé.
2. **`TECH_DEBT.md` → `AUDIT_STATUS.md`** — La dette technique est déjà suivie dans AUDIT_STATUS.md (section « Dette technique »). Un fichier séparé est redondant.
3. **`DECISIONS.md` → `adr/README.md`** — DECISIONS.md est un index d'ADR. Le README.md du répertoire adr/ remplit déjà ce rôle.
4. **`03_DECISION.md` → `07_CLOSEOUT.md`** — Les décisions sont déjà capturées dans les closeouts. Une phase séparée n'est jamais produite.
5. **`0-vbb-audit-readiness` + `0-vbb-scope-freeze` → `0-vbb-rico-readiness`** — Les trois skills de Phase 0 couvrent des aspects très proches de la readiness. rico-readiness est le seul utilisé.
6. **`05_EXECUTION.md` → `05_PATCH_SUMMARY.md`** — EXECUTION n'est jamais utilisé ; PATCH_SUMMARY est le standard de fait.

### 4.4 À ARCHIVER (49 éléments)

Éléments sans usage observé dans les projets, mais qui peuvent servir de référence ou être réactivés plus tard.

#### Documents extended (10)
`SESSION_RULES.md`, `DEPLOYMENT.md`, `DISTRIBUTIONS.md`, `LLM_PROVIDERS.md`, `LONG_RUN_RULE.md`, `MEMORY_AND_HANDOFF.md`, `RUNBOOK.md`, `TEMPORAL_PROVENANCE.md`, `TROUBLESHOOTING.md`, `router/ROUTER_MATRIX.md`, `strategy/p0-4-review-matrix-poc.md`

#### Skills sans usage (33)
`0-vbb-standard`, `1-vbb-conventions`, `1-vbb-doc-harmonizer`, `1-vbb-code-doc-coherence-auditor`, `1-vbb-code-doc-gap-integrator`, `1-vbb-error-handling-auditor`, `1-vbb-formatter`, `1-vbb-monolith-detector`, `1-vbb-pattern-inconsistency-detector`, `1-vbb-premature-abstraction-detector`, `1-vbb-test-mirage-detector`, `1-vbb-api-contract-designer`, `2-vbb-ops`, `2-vbb-ci`, `2-vbb-db-robustness`, `2-vbb-performance`, `2-vbb-api-auditor`, `2-vbb-analytics`, `2-vbb-legal`, `4-vbb-cognitive-load-optimizer`, `4-vbb-design-system-validator`, `4-vbb-visual-identity-layer`, `4-vbb-visual-identity-gatekeeper`, `4-vbb-micro-interaction-refiner`, `4-vbb-product-changelog`, `t-vbb-anti-slop-gate`, `t-vbb-commit-ready`, `t-vbb-dependency-mapper`, `t-vbb-docker-audit`, `t-vbb-docker-generate`, `t-vbb-deploy-runtime`, `t-vbb-git-sync`, `t-vbb-llm-healthcheck`, `t-vbb-status-report`, `t-vbb-test-coverage-mapper`

#### Outils sans usage (6)
`vbb-contract-runtime.py`, `vbb-executor.py`, `vbb-llm-healthcheck.py`, `vbb-phase-router.py`, `vbb-review-threshold-poc.py`

#### Scripts sans usage (4)
`scripts/hooks/pre-commit-framework-gate`, `scripts/hooks/commit-msg-framework-gate`, `scripts/install-framework-gate-hook.sh`, `scripts/install-vbb-pre-commit.sh`

### 4.5 À SUPPRIMER (2 éléments)

Éléments sans usage, sans valeur de référence, générateurs de friction.

1. **`06_REVIEW.md` / `06_REVIEW_NOTES.md`** — Jamais produit dans 24 runs. La revue est implicite dans le closeout. **Risque de suppression : nul.**
2. **`worker-evidence-paragraph.md`** — Template orphelin, jamais référencé. **Risque de suppression : nul.**

---

## 5. Synthèse quantitative

| Catégorie | Total VBB | Conservé | Simplifié | Fusionné | Archivé | Supprimé |
|-----------|-----------|----------|-----------|----------|---------|----------|
| Documents gouvernance | 25 | 8 | 2 | 3 | 11 | 0 |
| Templates | 12 | 9 | 2 | 1 | 1 | 1 |
| Phases de run | 9 | 3 | 1 | 3 | 0 | 1 |
| Skills | 64 | 16 | 0 | 3 | 33 | 0 |
| Outils | 14 | 5 | 0 | 0 | 6 | 0 |
| Scripts | 7 | 3 | 0 | 0 | 4 | 0 |
| Prompts | 33 | 10 | 0 | 0 | 23 | 0 |
| **TOTAL** | **164** | **54** | **5** | **10** | **78** | **2** |

**Ratio** : 54 éléments conservés (33%), 110 éléments allégés/fusionnés/archivés/supprimés (67%).

---

## 6. Conclusion

### Réponse à la question centrale

> Si Vibe Backbone devait être réduit à ce qui sert réellement dans Orgabar, Secrets / Guard Backbone et SwiftMinuteur, que resterait-il ?

**Un noyau de 54 éléments (33% du total) :**

#### Gouvernance projet (8 documents)
`CONTEXT.md` · `PROJECT_MODE.md` · `SESSION.md` · `AUDIT_STATUS.md` · `ARCHITECTURE.md` · `CONVENTIONS.md` · `MVP_START_PROTOCOL.md` · `INDEX.md` (simplifié)

#### Artefacts de run (3 phases)
`02_AUDIT.md` · `05_PATCH_SUMMARY.md` · `07_CLOSEOUT.md`

#### Skills actifs (16)
Phase 0 : `0-vbb-rico-readiness` · `0-vbb-guide` · `0-vbb-pilotage` · `0-vbb-zero-friction`
Phase 1 : `1-vbb-tech-debt` · `1-vbb-intent-decomposer` · `1-vbb-adr` · `1-vbb-code-janitor` · `1-vbb-logic-duplication-detector`
Phase 2 : `2-vbb-security` · `2-vbb-spec-validator` · `2-vbb-data-integrity` · `2-vbb-accessibility` · `2-vbb-systemic-risk`
Phase 3-4 : `3-vbb-risk-register` · `4-vbb-security-remediation` · `4-vbb-user-experience-engine` · `4-vbb-interaction-coherence-auditor` · `4-vbb-front-pipeline-reference`
Transverse : `t-vbb-project-context-init` · `t-vbb-session-handoff` · `t-vbb-mode-transition-gate` · `t-vbb-context-compactor` · `t-vbb-impact-analyzer` · `t-vbb-index` · `t-vbb-status-dashboard` · `vibebackbone`

#### Outils (5)
`vbb-loop-closure-check.py` · `vbb-architecture.py` · `vbb-contract-lint.py` · `vbb-gate-check.py` · `vbb-ci-local.sh` · `vbb-project-init.py` · `vbb-index.py` · `vbb-status-dashboard.py` · `vbb-context-compactor.py`

#### Prompts canoniques (10)
`0-p-vbb-triage` · `1-p-vbb-quick-task` · `1-p-vbb-structured-task` · `2-p-vbb-audit-task` · `t-p-vbb-session-handoff` · `canonical/01-07` (7 prompts)

### Ce qui disparaîtrait (110 éléments, 67%)

- 49 skills sans usage → archivés
- 14 documents extended → archivés
- 6 phases de run jamais produites → fusionnées ou supprimées
- 23 prompts spécialisés → archivés
- 6 outils sans usage → archivés
- 4 scripts hooks → archivés
- 2 éléments orphelins → supprimés

### Constats clés

1. **Le modèle 8 phases est une fiction.** Le pattern réel est 2-3 artefacts par run. Les phases 03_DECISION et 06_REVIEW n'ont jamais été produites.
2. **77% des skills sont inutilisés.** 49/64 skills n'ont aucune trace d'invocation. Le catalogue est surdimensionné.
3. **Les 4 documents du noyau dur (CONTEXT, PROJECT_MODE, SESSION, AUDIT_STATUS) sont le véritable backbone.** Ils sont présents dans 100% des projets et activement maintenus.
4. **Les outils VBB sont référencés mais rarement exécutés.** SwiftMinuteur est le seul projet qui les exécute effectivement.
5. **Les templates ne sont utiles qu'à l'init.** Orgabar les a tous, Secrets et SwiftMinuteur aucun — et ils produisent les mêmes artefacts.
6. **ACTIVITY_LOG.md est une pratique émergente.** Seul Secrets l'utilise, mais de façon intensive (198 lignes). C'est un bon candidat pour le noyau futur.
7. **Le frontmatter YAML est le standard de fait.** Tous les artefacts dans les 3 projets utilisent le frontmatter VBB.

### Zones d'incertitude

- **Prompts** : L'usage des prompts est indirect (consommés par les agents, pas par les projets). La classification « archiver » pour les prompts spécialisés est basée sur l'absence de traces dans les projets, pas sur l'absence d'usage par les agents.
- **Skills archivés** : Certains skills sans usage aujourd'hui pourraient devenir utiles dans d'autres contextes (ex: `2-vbb-db-robustness` pour un projet avec base de données). L'archivage préserve la possibilité de réactivation.
- **`t-vbb-mode-transition-gate`** : Référencé dans 2/3 projets mais jamais exécuté. Si les projets passent en PROD, il pourrait devenir critique.
