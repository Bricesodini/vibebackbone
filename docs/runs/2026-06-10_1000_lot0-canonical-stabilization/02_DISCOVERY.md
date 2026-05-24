# 02_DISCOVERY — RUN 01 · Lot 0 : Inventaire réel du repo

**Date** : 2026-06-10  
**Voie** : STRUCTURÉE

---

## 1. Nombre réel de skills

**Définition retenue** : un skill = un dossier contenant un fichier `SKILL.md` sous `skills/`.

**Résultat** : **58 skills**

Détail par phase :

| Phase | Préfixe | Nombre | Liste |
|-------|---------|--------|-------|
| **0 — Readiness & cadrage** | `0-vbb-` | 5 | audit-readiness, guide, pilotage, scope-freeze, standard |
| **1 — Structure & dette** | `1-vbb-` | 16 | adr, api-contract-designer, code-doc-coherence-auditor, code-doc-gap-integrator, code-janitor, conventions, doc-harmonizer, error-handling-auditor, formatter, intent-decomposer, logic-duplication-detector, monolith-detector, pattern-inconsistency-detector, premature-abstraction-detector, tech-debt, test-mirage-detector |
| **2 — Audits de fond** | `2-vbb-` | 12 | accessibility, analytics, api-auditor, ci, data-integrity, db-robustness, legal, ops, performance, security, spec-validator, systemic-risk |
| **3 — Consolidation** | `3-vbb-` | 1 | risk-register |
| **4 — Front-end UX/UI** | `4-vbb-` | 10 | cognitive-load-optimizer, design-system-validator, front-pipeline-reference, interaction-coherence-auditor, micro-interaction-refiner, product-changelog, security-remediation, user-experience-engine, visual-identity-gatekeeper, visual-identity-layer |
| **t — Transverse** | `t-vbb-` | 13 | anti-slop-gate, commit-ready, dependency-mapper, deploy-runtime, docker-audit, docker-generate, git-sync, impact-analyzer, mode-transition-gate, project-context-init, session-handoff, status-report, test-coverage-mapper |
| **Orchestrateur** | `vibebackbone` | 1 | vibebackbone |
| **Total** | | **58** | |

**Contrats mécaniques** : 22 CONTRACT.yaml (22/58 skills contractés, 38%).  
INDEX.yaml référence 22 entrées de contrats.

**Skills sans contrat** : 36.

---

## 2. Nombre réel de prompts

**Résultat** : **32 fichiers prompt** au total

| Catégorie | Nombre | Détail |
|-----------|--------|--------|
| **Canoniques** | 7 | intake, audit, decision, plan, execution, review, closeout |
| **Spécialisés Phase 0** | 3 | before-building, plan, triage |
| **Spécialisés Phase 1** | 7 | doc-feature, legacy-level, post-refacto-coherence, project-init, quick-task, structured-task, tech-debt |
| **Spécialisés Phase 2** | 5 | audit-task, db-sanity, mode-transition, release-check, security-pipeline |
| **Spécialisés Phase 3** | 1 | risk-register |
| **Spécialisés Phase 4** | 3 | after-building, anti-slop, deploy-docker |
| **Spécialisés Transverse** | 6 | branch-policy-check, git-sync, phase-router, sequenced-ship, session-handoff, start-session |
| **Total** | **32** | |

**Décomposition canonique** : 7 canoniques + 24 spécialisés + 1 router = 32.  
Le router (`t-p-vbb-phase-router.md`) est un prompt spécialisé transverse, pas une catégorie à part.

---

## 3. Contradictions documentaires

| # | Fichier | Affirmation | Réalité | Écart |
|---|---------|-------------|---------|-------|
| C-01 | `README.md` ligne 4 | "57 skills" | 58 SKILL.md | **-1** |
| C-02 | `README.md` ligne 4 | "31 prompts" | 32 fichiers | **-1** |
| C-03 | `README.md` ligne 43 | "7 canoniques + 24 spécialisés + 1 router" | 7 canoniques + 25 root-level = 32 | Arithmétique inconsistante (7+24+1=32, pas 31) |
| C-04 | `README.md` ligne 88 | "24 prompts spécialisés" | 25 fichiers root-level | **-1** (router pas listé dans la table) |
| C-05 | `README.md` table t-\* | 12 skills transverses | 13 skills transverses | Manque `t-vbb-status-report` |
| C-06 | `AGENTS.md` ligne 350 | "57 skills · 24 prompts" | 58 skills, 32 prompts | **-1 skill, -8 prompts** |
| C-07 | `SYSTEM.md` ligne 5 | "57 skills · 24 prompts" | 58 skills, 32 prompts | **-1 skill, -8 prompts** |
| C-08 | `GUIDE.md` ligne 82 | "31 PROMPTS" | 32 prompts | **-1** |
| C-09 | `GUIDE.md` ligne 168 | "24 prompts spécialisés" | 25 root-level (24 + router) | Catégorisation ambiguë |
| C-10 | `GUIDE.md` ligne 221 | "Les 24 prompts" | 25 root-level | **-1** |
| C-11 | `CONTEXT.md` ligne 57 | "58 skills" | 58 SKILL.md | ✅ Correct |
| C-12 | `CONTEXT.md` ligne 58 | "24 prompts de session" | 32 prompts total | **-8** |
| C-13 | `INDEX.md` ligne 46 | "Skills (58)" | 58 SKILL.md | ✅ Correct |
| C-14 | `INDEX.md` ligne 47 | "Prompts spécialisés (25)" | 25 root-level fichiers | ✅ Correct si on compte le router comme spécialisé |
| C-15 | `INDEX.md` ligne 48 | "Prompts canoniques (7)" | 7 canonical | ✅ Correct |
| C-16 | `README.md` ligne 35 | "57 skills prêts à injecter" | 58 SKILL.md | **-1** |
| C-17 | `README.md` ligne 62 | "Les 57 skills" | 58 SKILL.md | **-1** |
| C-18 | `GUIDE.md` ligne 88 | "57 SKILLS" | 58 SKILL.md | **-1** |
| C-19 | `GUIDE.md` ligne 220 | "Les 57 skills" | 58 SKILL.md | **-1** |
| C-20 | `AUDIT_STATUS.md` | "8 skills sur 58" | 22 CONTRACT.yaml | Chiffre obsolète dans le texte narratif |
| C-21 | `README.md` arbre | "Phase 0 (5)" | 5 skills | ✅ |
| C-22 | `README.md` arbre | "Phase 1 (16)" | 16 skills | ✅ |
| C-23 | `README.md` arbre | "Phase 2 (12)" | 12 skills | ✅ |
| C-24 | `README.md` arbre | "Phase 3 (1)" | 1 skill | ✅ |
| C-25 | `README.md` arbre | "Phase 4 (10)" | 10 skills | ✅ |
| C-26 | `README.md` arbre | "Transverse (12)" | 13 skills | **-1** (manque status-report) |

### Synthèse des écarts

Deux axes de contradiction :

1. **Skills** : README, AGENTS, SYSTEM, GUIDE annoncent **57** → réalité **58**. CONTEXT et INDEX disent **58** → correct.
2. **Prompts** : README annonce **31**, AGENTS/SYSTEM disent **24**, GUIDE dit **31**, CONTEXT dit **24**, INDEX dit **25 spécialisés + 7 canoniques=32** → réalité **32**.

---

## 4. Skills orphelins / méta

| Skill | Phase déclarée (frontmatter) | Préfixe | Classification proposée |
|-------|------------------------------|---------|------------------------|
| `0-vbb-guide` | `transverse` | `0-` | **Documentation** — carte de référence du système |
| `0-vbb-pilotage` | `transverse` | `0-` | **Documentation** — référentiel des voies d'exécution |
| `0-vbb-standard` | `transverse` | `0-` | **Méta-skill** — standard canonique des skills |
| `vibebackbone` | `transverse` | (aucun) | **Orchestrateur** — triage et routage global |

Ces 4 skills ont un préfixe ou positionnement inattendu (phase `transverse` pour des skills en `0-vbb-*` ou sans préfixe). Ils ne sont pas « orphelins » au sens de non-fonctionnels — ils sont **méta / gouvernance** et doivent être classés comme tels.

Les deux autres cités dans la consigne :
- `0-vbb-audit-readiness` : Phase 0 opérationnelle (gatekeeper) → **non orphelin**
- `0-vbb-scope-freeze` : Phase 0 opérationnelle (gatekeeper) → **non orphelin**

### Anomalie de préfixe

`0-vbb-guide`, `0-vbb-pilotage`, `0-vbb-standard` portent un préfixe `0-` mais ont `phase: transverse`. Ce sont des skills de gouvernance/documentation, pas des gates Phase 0. Le préfixe `0-` est cohérent avec leur rôle de « pré-condition » (lire le guide avant d'agir), mais la phase déclarée `transverse` est technique. À documenter clairement, pas à renommer (interdiction de renommage).

---

## 5. Labels de maturité non prouvés

| Fichier | Ligne | Label | Contexte | Action proposée |
|---------|-------|-------|----------|-----------------|
| `docs/CONTEXT.md` | 48 | "🟢 PRODUCTION-READY + OPENCODE-READY" | Verdict global du projet | Remplacer par verdict conforme à AUDIT_STATUS ("PARTIAL — not yet mechanically audited") |
| `docs/AUDIT_STATUS.md` | 24 | Dénonce le label comme « fossilisée » | Auto-diagnostic déjà présent | ✅ Déjà corrigé textuellement — mais CONTEXT.md pas mis à jour |
| `README.md` | 77 | "production-ready" | Refers to nginx template | ✅ Légitime — c'est le template nginx, pas le projet |
| `README.md` | 4 | "57 skills" (implique complétude) | Chiffre de complétude | Mettre à 58 |

### Labels à traiter

Seul le label `🟢 PRODUCTION-READY` dans `CONTEXT.md` est problématique. Il contredit directement `AUDIT_STATUS.md` qui le qualifie de « fossilisé » et stipule que le verdict réel est `PARTIAL — not yet mechanically audited`.

Aucun autre label de maturité non prouvé (stable, audited, complete) n'a été trouvé dans les frontmatter SKILL.md de manière problématique.

---

## 6. Contrat INDEX.yaml vs réalité

| INDEX.yaml | Fichiers CONTRACT.yaml | Statut |
|------------|------------------------|--------|
| 22 entrées | 22 fichiers | ✅ Cohérent |

La mention dans AUDIT_STATUS « 8 skills sur 58 (14 %) » est obsolète. Le chiffre réel est **22/58 (38 %)**.

---

## 7. Vérifications de cohérence additionnelles

| Vérification | Résultat |
|-------------|----------|
| `find skills -name SKILL.md \| wc -l` | **58** ✅ |
| `find prompts -type f -name "*.md" \| wc -l` | **32** ✅ |
| `find skills -name CONTRACT.yaml \| wc -l` | **22** ✅ |
| Linter contrat `vbb-contract-lint.py` | **0 erreur** ✅ |
| Loop closure check | **PASS** ✅ |
| README table t-vbb-* | **12 noms** (manque status-report) ❌ |
| README tableau arbre | **56 noms explicites** + vibebackbone = 57 annoncé, 58 réel ❌ |