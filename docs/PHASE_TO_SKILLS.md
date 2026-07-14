---
context_role: phase-mapping
phase: transverse
status: canonical
updated: 2026-07-12
---

# PHASE_TO_SKILLS — Cartographie canonique phase ↔ skill

> **Statut** : canonique pour la cartographie phase↔skill. Single source of truth.
> **Référence agentique** : [`prompts/canonical/02-p-vbb-audit.md`](../prompts/canonical/02-p-vbb-audit.md) et le protocole 7 phases canoniques.

---

## Convention `phase:` dans le frontmatter SKILL.md

| Valeur `phase:` | Phase agentique | Description |
|-----------------|------------------|-------------|
| `0` | Readiness & cadrage | Gate, scope freeze, audit readiness, RICO readiness |
| `01_INTAKE` | INTAKE | Réception et cadrage initial |
| `02_AUDIT` | AUDIT | Production de rapports d'audit (read-only) |
| `03_DECISION` | DECISION | Prise de décision documentée |
| `04_PLAN` | PLAN | Planification détaillée |
| `05_EXECUTION` | EXECUTION_RUN_N | Implémentation d'un run |
| `06_REVIEW` | REVIEW | Review d'un patch |
| `07_CLOSEOUT` | CLOSEOUT | Clôture d'un run |
| `1` | _deprecated_ | Valeur ambiguë, à remplacer par `02_AUDIT` |
| `2` | _deprecated_ | Valeur ambiguë, à remplacer par `02_AUDIT` (audits de fond) |
| `3` | _deprecated_ | Valeur ambiguë |
| `4` | _deprecated_ | Valeur ambiguë |
| `t` | transverse | Skills transverses (Docker, Git, CI, deployment, etc.) |
| `transverse` | transverse | Idem `t` (alias explicite) |

---

## Cartographie actuelle (par phase canonique)

### Phase 0 — Readiness & cadrage

| Skill | Description courte |
|-------|---------------------|
| `0-vbb-audit-readiness` | Gatekeeper audit (peut-on auditer maintenant ?) |
| `0-vbb-rico-readiness` | Gatekeeper MVP start (no code before readiness) |
| `0-vbb-scope-freeze` | Validation du freeze de scope |
| `0-vbb-guide` | Carte de référence Vibebackbone |
| `0-vbb-pilotage` | Routes et règles de triage |
| `0-vbb-standard` | Contrat canonique de skill (frontmatter, validation) |
| `0-vbb-zero-friction` | Micro-tâches FAST-ZERO / FAST-MINIMAL |

### Phase 02_AUDIT — Audits structurels (anciennement « phase 1 »)

| Skill | Description courte |
|-------|---------------------|
| `1-vbb-code-janitor` | Stabilisation non-créative (entropie) |
| `1-vbb-tech-debt` | Diagnostic dette technique |
| `1-vbb-monolith-detector` | Détection patterns monolithiques |
| `1-vbb-conventions` | Harmonisation conventions repo |
| `1-vbb-formatter` | Plan enforcement formatter/linter |
| `1-vbb-intent-decomposer` | Décomposition d'intention produit → plan |
| `1-vbb-adr` | Rédaction d'ADR (Architecture Decision Record) |
| `1-vbb-api-contract-designer` | Design de contrat API pre-implémentation |
| `1-vbb-code-doc-coherence-auditor` | Audit cohérence code ↔ doc |
| `1-vbb-code-doc-gap-integrator` | Intégration gaps doc ↔ code |
| `1-vbb-doc-harmonizer` | Harmonisation markdown context |
| `1-vbb-error-handling-auditor` | Audit cohérence error handling |
| `1-vbb-logic-duplication-detector` | Détection duplication logique métier |
| `1-vbb-pattern-inconsistency-detector` | Détection incohérences de patterns |
| `1-vbb-premature-abstraction-detector` | Détection sur-abus d'abstractions |
| `1-vbb-test-mirage-detector` | Détection faux tests (mock without assertion, etc.) |

### Phase 02_AUDIT — Audits de fond (anciennement « phase 2 »)

| Skill | Description courte |
|-------|---------------------|
| `2-vbb-accessibility` | Audit accessibilité WCAG |
| `2-vbb-analytics` | Audit instrumentation produit |
| `2-vbb-api-auditor` | Audit API vs contrats déclarés |
| `2-vbb-ci` | Audit CI/CD |
| `2-vbb-data-integrity` | Audit invariants métier |
| `2-vbb-db-robustness` | Audit robustesse DB |
| `2-vbb-legal` | Criblage privacy / licensing / RGPD |
| `2-vbb-ops` | Audit opérationnel (logging, observabilité) |
| `2-vbb-performance` | Audit performance / scalabilité |
| `2-vbb-security` | Audit sécurité |
| `2-vbb-spec-validator` | Validation spec ↔ implémentation |
| `2-vbb-systemic-risk` | Audit risques systémiques |

### Phase 03_DECISION — Consolidation risques / décisions

| Skill | Description courte |
|-------|---------------------|
| `3-vbb-risk-register` | Registre consolidé des risques |

### Phase 04_PLAN — Cadrage front / sécurité

| Skill | Description courte |
|-------|---------------------|
| `4-vbb-cognitive-load-optimizer` | Réduction charge cognitive (Pass 3/7 front) |
| `4-vbb-design-system-validator` | Validation design system (Pass 4/7 front) |
| `4-vbb-front-pipeline-reference` | Référence pipeline front 7 passes |
| `4-vbb-interaction-coherence-auditor` | Cohérence interactions (Pass 2/7 front) |
| `4-vbb-micro-interaction-refiner` | Raffinement micro-interactions (Pass 6/7 front) |
| `4-vbb-product-changelog` | Changelog produit human-readable |
| `4-vbb-security-remediation` | Plan remédiation sécurité |
| `4-vbb-user-experience-engine` | Optimisation UX business (Pass 1/7 front) |
| `4-vbb-visual-identity-gatekeeper` | Gatekeeper identité visuelle (Pass 7/7 front) |
| `4-vbb-visual-identity-layer` | Application identité visuelle (Pass 5/7 front) |

### Phase transverse

| Skill | Description courte |
|-------|---------------------|
| `t-vbb-anti-slop-gate` | Quality gate multi-langage (slop detection) |
| `t-vbb-commit-ready` | Package commit + message conventionnel |
| `t-vbb-context-compactor` | Compression contexte run |
| `t-vbb-dependency-mapper` | Cartographie dépendances → ARCHITECTURE.md |
| `t-vbb-deploy-runtime` | Cycle de vie déploiement Docker |
| `t-vbb-docker-audit` | Audit readiness Docker |
| `t-vbb-docker-generate` | Génération infra Docker |
| `t-vbb-git-sync` | Lifecycle git sync (commit, push, merge) |
| `t-vbb-impact-analyzer` | Analyse d'impact changement |
| `t-vbb-index` | Index local textuel (retrieval) |
| `t-vbb-llm-healthcheck` | Healthcheck LLMs déclarés |
| `t-vbb-mode-transition-gate` | Gate DEV → PROD |
| `t-vbb-project-context-init` | Bootstrap gouvernance vibebackbone |
| `t-vbb-session-handoff` | Compression handoff session |
| `t-vbb-status-dashboard` | Dashboard terminal read-only |
| `t-vbb-status-report` | Rapport de statut compact |
| `t-vbb-test-coverage-mapper` | Cartographie couverture test utile |

### Orchestrateur

| Skill | Description courte |
|-------|---------------------|
| `vibebackbone` | Orchestrateur principal (triage + sélection workflow) |

---

## Règle de mise à jour

1. **Toute nouvelle skill** DOIT avoir son `phase:` aligné sur la convention ci-dessus.
2. **Toute modification de `phase:`** doit être tracée dans ce fichier (pas de drift silencieux).
3. **The integer values `phase: 1` and `phase: 2`** are deprecated and must not be used in a new skill.
4. **The `SKILL.md` frontmatter namespace** follows the agentic lifecycle (`02_AUDIT` for all `1-vbb-*` skills).
5. **The `CONTRACT.yaml` routing namespace is distinct:** `routing.phase_scope: phase_1` is the stable catalog-router API for `1-vbb-*` skills. It must not be replaced with `02_AUDIT`.
6. The contract linter blocks drift across these two surfaces.

---

## Pourquoi une cartographie canonique ?

- **Éviter le drift** : sans single source of truth, chaque skill choisirait sa valeur `phase:` arbitrairement.
- **Permettre le routing** : un orchestrateur peut filtrer les skills par phase canonique.
- **Documenter la convention** : les nouveaux contributeurs voient immédiatement quelle valeur utiliser.
- **Tracer les dépréciations** : les anciennes valeurs (`1`, `2`, `3`, `4`) sont listées explicitement comme deprecated, avec leur remplaçant.

---

## Liens

- [`skills/0-vbb-standard/SKILL.md`](../skills/0-vbb-standard/SKILL.md) — frontmatter standard
- [`prompts/canonical/02-p-vbb-audit.md`](../prompts/canonical/02-p-vbb-audit.md) — phase 02 AUDIT
- [`docs/PILOTAGE.md`](PILOTAGE.md) — routes et familles
- [`docs/AGENTIC_RUN_PROTOCOL.md`](AGENTIC_RUN_PROTOCOL.md) — protocole 7 phases
- [`docs/REFERENCE/pre-merge-gate.md`](REFERENCE/pre-merge-gate.md) — 5 vérifications P.R2
