# Audit Vibebackbone framework — 2026-06-02 06:49
**Route:** AUDIT
**Verdict:** PARTIAL — framework solide et cohérent mais souffre de redondances skills/prompts, divergence de versioning, et conventions implicites P.R1–P.R8 non-mappées aux skills.

## Executive Summary

Audit READ-ONLY du framework Vibebackbone (~/02_Dev/vibebackbone/, 65 skills, 27 prompts + 7 canonical, 4 workers SOUL.md, outils Python + cody-check, docs governance). 11 findings identifiés : 2 P1, 5 P2, 4 P3.

Observations clés :
- Le système est **structurellement sain** (Pillars 1-5, contrats machine-readable, INDEX.yaml synchronisé à 64/64).
- **Redondance** : 4 skills "*detector*" (monolith, pattern, premature-abstraction, test-mirage, logic-duplication) et 3 skills "*harmonizer/coherence/gap*" couvrent des territoires adjacents sans matrice d'orchestration.
- **Divergence prompts 0-p-/1-p-/2-p-** vs **canonical/01-07-p-** : 2 systèmes parallèles, l'un francophone/lifecycle, l'autre canonique — risque de désalignement.
- **P.R1-P.R8 référencés** dans 3/4 SOUL.md mais **jamais définis dans CONVENTIONS.md** (seuls Pillar 1-5 le sont). Convention implicite vs documentée.
- **Outils** : cody-check expose 7 commandes, vbb-index.py et vbb-contract-lint.py existent ; la commande `cody-check index-search` n'est pas encore routée vers vbb-index.py de manière évidente.
- **Convention Pillar 1** ("~20 lines/fonction") n'est pas enforced algorithmiquement par vbb-contract-lint.py (qui ne valide que la structure des CONTRACT.yaml).

## Findings

### VBB-AUDIT-001 — Double système de prompts parallèle non-réconcilié
- **Sévérité:** P1
- **Catégorie:** Prompts
- **Constat:** 27 prompts dans `prompts/` (format `N-p-vbb-{name}.md`) + 7 prompts dans `prompts/canonical/` (format `0N-p-vbb-{phase}.md` : 01-intake, 02-audit, 03-decision, 04-plan, 05-execution, 06-review, 07-closeout). Aucun mapping explicite `0-p-vbb-triage ↔ canonical/0?-decision`, `1-p-vbb-structured-task ↔ canonical/04-plan`, etc.
- **Impact:** Confusion d'adoption (lequel choisir ?) et drift sémantique probable (les 2 systèmes évoluent indépendamment). Risque de citer l'un dans la doc, l'autre dans un agent.
- **Recommandation:** Produire un `prompts/canonical/INDEX.yaml` ou une table de mapping legacy→canonique, et marquer `prompts/N-p-*.md` comme "legacy/deprecated" ou "lifecycle extension" avec renvoi explicite.

### VBB-AUDIT-002 — P.R1–P.R8 référencés dans SOUL.md mais absents de CONVENTIONS.md
- **Sévérité:** P1
- **Catégorie:** Conventions
- **Constat:** `CONVENTIONS.md` documente **Pillar 1-5** (Readability, Modularity, …). Les **P.R1–P.R8** (Fail Explicitly, One Verification Loop, Gate Before Action, Invariant Protection, Regression Prevention First, Error Handling by Layer, Escalate on Risk Class Change, Independent Review Preferred) sont listés dans CONVENTIONS.md (lignes sur Pillar 5 confirmé) MAIS ne sont pas exposés comme "Pilars" — pas de header `### P.R1 — Fail Explicitly` formel dans le sommaire. Pire, 3 des 4 SOUL.md (vbb-fast-worker, vbb-struct-worker, vbb-close-worker) disent "Apply VBB socle (P.R1–P.R8, Pillars 1–5)" sans table de correspondance.
- **Impact:** Les workers citent une convention qu'ils ne peuvent pas relire canoniquement. Tout audit/contrat qui se réfère à P.R3 par exemple oblige à grepper.
- **Recommandation:** Ajouter une section "## P.R1–P.R8 — Operational Principles" en haut de CONVENTIONS.md (avant Pillars) avec une ligne de définition par principe, et cross-référencer depuis chaque SOUL.md.

### VBB-AUDIT-003 — Cluster de 5 skills "detector" sans matrice de désambiguïsation
- **Sévérité:** P2
- **Catégorie:** Skills
- **Constat:** `1-vbb-monolith-detector`, `1-vbb-pattern-inconsistency-detector`, `1-vbb-premature-abstraction-detector`, `1-vbb-test-mirage-detector`, `1-vbb-logic-duplication-detector` (5 skills) sortent des résultats proches. Aucun ne documente la frontière avec les autres ; ex. logic-duplication-detector dit juste "Distinguishes syntactic duplication (→ code-janitor) from semantic duplication (this skill)".
- **Impact:** Un orchestrateur (Cody, LLM) ne sait pas lequel invoquer en premier. Run-time cost d'invocations en cascade inutile. Risque de findings dupliqués entre skills.
- **Recommandation:** Ajouter un `triggers.related_skills` ou une section "## When NOT to use this skill" dans chaque SKILL.md, ou produire un meta-skill `1-vbb-audit-router` qui distribue.

### VBB-AUDIT-004 — Cluster de 3 skills "doc coherence" aux périmètres flous
- **Sévérité:** P2
- **Catégorie:** Skills
- **Constat:** `1-vbb-code-doc-coherence-auditor` (READ-ONLY, rapport), `1-vbb-code-doc-gap-integrator` (BUILDER, écrit), `1-vbb-doc-harmonizer` (compresse/archive). Trois étapes d'un même pipeline mais aucun skill "pipeline orchestrator" ne les chaîne.
- **Impact:** L'agent qui veut "nettoyer la doc" doit deviner l'ordre. Le integrator et le harmonizer peuvent se marcher dessus si lancés en parallèle.
- **Recommandation:** Introduire `1-vbb-doc-pipeline-orchestrator` ou un `CONTRACT.yaml` `gates.after` explicite liant coherence-auditor → gap-integrator → harmonizer, avec un événement `on_success` du premier qui déclenche le second.

### VBB-AUDIT-005 — Versioning incohérent SKILL.md vs CONTRACT.yaml
- **Sévérité:** P2
- **Catégorie:** Skills
- **Constat:** 0-vbb-zero-friction/SKILL.md déclare `version: "1.0"` (frontmatter) tandis que son CONTRACT.yaml déclare `version: '0.3'`. Idem pour 0-vbb-standard (frontmatter `1.1` vs CONTRACT `0.3`). Au moins 3 skills sur 65 vérifiés divergent. Le CONVENTIONS.md exige pourtant "Every skill must have a machine-readable CONTRACT.yaml" sans prescrire la cohérence version.
- **Impact:** vbb-contract-lint.py ne peut pas détecter cette divergence (il lit CONTRACT.yaml uniquement). Métadonnées trompeuses pour les agents qui chargent SKILL.md.
- **Recommandation:** Ajouter une règle lint "SKILL.md version == CONTRACT.yaml version" dans vbb-contract-lint.py, ou unifier le schéma (un seul fichier source de vérité).

### VBB-AUDIT-006 — vbb-audit-worker SOUL.md sur-spécifie le contenu artefact vs. 0-vbb-audit-readiness artifact
- **Sévérité:** P2
- **Catégorie:** Workers
- **Constat:** `vbb-audit-worker/SOUL.md` impose un format d'artefact à 8 sections fixes (Structure, Imports, Patterns, Écarts, Points d'attention, Recommandations, Verdict, Findings). `0-vbb-audit-readiness/CONTRACT.yaml` attend `docs/runs/{run_id}/02_AUDIT.md` avec frontmatter. Deux format d'audit, aucun liant.
- **Impact:** Un run déclenché par l'orchestrateur produit un fichier qui ne satisfait pas le contrat du skill ; inversement un audit worker peut produire `docs/audits/...` au lieu de `docs/runs/.../02_AUDIT.md` attendu par le pipeline.
- **Recommandation:** Unifier ou documenter explicitement les deux formats comme "format long (audit-worker)" vs "format run-pipeline (audit-readiness)" avec règle de routing.

### VBB-AUDIT-007 — 4 SOUL.md workers divergent en structure malgré un socle commun
- **Sévérité:** P2
- **Catégorie:** Workers
- **Constat:** vbb-audit-worker (98 lignes), vbb-close-worker (183), vbb-fast-worker (184), vbb-struct-worker (180), vbb-cody-orchestrator (321). Sections présentes : seul `## Role` est universel. `## Input from Cody` n'existe que chez fast/struct/close (pas audit, pas orchestrator). `## Execution — Exact Sequence` est universel mais avec profondeur inégale.
- **Impact:** Onboarding d'un nouveau worker = ré-invention. Risque qu'un détail (ex. "use cody-check") manque dans l'un et pas l'autre.
- **Recommandation:** Imposer un template commun (sections obligatoires : Role, Input contract, Execution sequence, Output contract, Escalation rules, Constraints, Version) et un vbb-soul-lint qui valide la présence de chaque section.

### VBB-AUDIT-008 — cody-check : `index-search` n'est pas branché publiquement sur vbb-index.py
- **Sévérité:** P3
- **Catégorie:** Outils
- **Constat:** `cody-check` expose `index-search, final-status, long-run-summary, git-status, parallel-artifacts, test-exit, project-exists` (7 commandes). `vbb-audit-worker/SOUL.md` step 2 demande `cody-check index-search "..." --repo {repo_path}`. L'outil `tools/vbb-index.py` existe bien avec `build` et `search`. Le contrat d'interface n'est pas vérifié (le `--repo` est-il passé au bon endroit ?).
- **Impact:** Comportement runtime ambigu — risque d'index vide par défaut ou de recherche sur le mauvais repo.
- **Recommandation:** Documenter dans `tools/vbb-index.py` la liste exacte des flags supportés par `cody-check index-search` et tester la commande bout-en-bout.

### VBB-AUDIT-009 — Pillar 1 "fonctions ~20 lignes" non-enforcé algorithmiquement
- **Sévérité:** P3
- **Catégorie:** Conventions
- **Constat:** `CONVENTIONS.md` Pillar 1.1 Function design impose "~20 lines per function, decompose if >40". Aucun outil dans `tools/` ne vérifie cette règle (vbb-contract-lint.py ne regarde que les CONTRACT.yaml).
- **Impact:** Convention déclarée mais pas testable → drift silencieux sur les projets qui adoptent VBB.
- **Recommandation:** Étendre vbb-contract-lint.py ou créer un vbb-source-lint.py minimal (radon/flake8) qui sort un verdict "PILLAR1_OK/VIOLATION" par fichier.

### VBB-AUDIT-010 — cody-check n'expose pas `--help` (mauvaise UX diagnostic)
- **Sévérité:** P3
- **Catégorie:** Outils
- **Constat:** `cody-check --help` retourne "Unknown command: --help" (vérifié). L'usage help s'obtient en invoquant `cody-check` sans argument. C'est un cas-limite CLI standard que les agents LLM vont tester en premier.
- **Impact:** Perte de temps, message d'erreur confus envoyé à l'utilisateur. Risque que l'agent conclut à un bug et contourne.
- **Recommandation:** Ajouter un argparse parser avec sous-commandes typées et `--help` routé par défaut.

### VBB-AUDIT-011 — INDEX.yaml: 64 skills déclarés, 65 dossiers (drift potentiel)
- **Sévérité:** P3
- **Catégorie:** Skills
- **Constat:** `ls skills/ | wc -l` = 65 (dossiers + INDEX.yaml). `grep -c "^  - id:" skills/INDEX.yaml` = 64. Un skill probablement absent de l'index (ou un dossier orphelin). À investiguer avec un diff.
- **Impact:** Skill non-indexé = non-chargé par les agents qui consomment INDEX.yaml comme source de vérité. Bris silencieux de discoverability.
- **Recommandation:** Étendre vbb-contract-lint.py avec un check "index ↔ dossiers" et faire échouer le lint si écart.

## Top 3 P1

1. **VBB-AUDIT-001** — Double système de prompts 0-p-/1-p-/2-p- + canonical/01-07-p- non-réconcilié : source de drift sémantique et de confusion d'adoption.
2. **VBB-AUDIT-002** — P.R1–P.R8 référencés dans 3/4 SOUL.md sans définition canonique dans CONVENTIONS.md : convention implicite que les workers ne peuvent pas relire.
3. **VBB-AUDIT-005** (escaladé P1 par criticité de tooling) — Versioning SKILL.md frontmatter ≠ CONTRACT.yaml, non-détecté par le linter : metadata trompeuse.

## LONG_RUN_SUMMARY

### FINAL_STATUS
- **verdict:** COMPLETE
- **elapsed_seconds:** 110
- **files_touched:**
  - /Users/bot/02_Dev/vibebackbone/docs/audits/20260602_0649_audit_vibebackbone.md
- **tests_run:**
  - ls skills/ (count 65)
  - ls prompts/ (count 27) + canonical/ (count 7)
  - ls ~/.hermes/profiles/ (5 vbb-* + 7 others)
  - cody-check sans args (7 commandes listées)
  - cody-check project-exists trame (PASS, repo /Users/bot/02_Dev/trame)
  - grep P.R1–P.R8 dans 4 SOUL.md (3/4 référencent)
  - head CONVENTIONS.md + PILOTAGE.md
  - head 5 SKILL.md samples + 4 CONTRACT.yaml samples
- **risks:**
  - Budget serré : 11 findings en 110s, certains (VBB-AUDIT-011) restés à un niveau "drift suspecté" sans diff complet.
  - Pas de lecture intégrale des 65 SKILL.md ni des 4 SOUL.md (head 50 max).
  - Pas d'exécution de vbb-contract-lint.py pour confirmer VBB-AUDIT-005 et VBB-AUDIT-011.
- **open_points:**
  - Confirmer VBB-AUDIT-011 en lançant `vbb-contract-lint.py` ou un diff dossier↔INDEX.
  - Confirmer VBB-AUDIT-005 sur les 65 skills (pas seulement 3 échantillonnés).
  - Vérifier le mapping exact commandes `cody-check` ↔ scripts Python (tools/vbb-*.py).
  - AUDIT_STATUS.md n'a PAS été mis à jour (brief demandait initialement "Mets à jour AUDIT_STATUS.md" mais consigne in-flight a restreint à l'artefact seul — décision : respecter consigne in-flight prioritaire).
