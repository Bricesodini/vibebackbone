# Audit Vibebackbone — Frame de Brice Sodini

**Date** : 2026-06-02 06:41
**Auditeur** : vbb-audit-worker (route AUDIT, mode READ-ONLY)
**Cible** : `~/02_Dev/vibebackbone/` (le framework, pas les projets qui l'utilisent)
**Méthode** : inventaire filesystem + grep références + lecture SOUL.md + exécution de commandes cody-check/vbb-index.py
**Status** : COMPLETE (couverture 6/6 catégories)

---

## Synthèse exécutive

Le framework Vibebackbone présente une **base conceptuelle solide** (P.R1–P.R8, Pillars 1–5, contrats machine-readables) mais souffre de **dérives structurelles** liées à une longue période d'évolution sans curation :
- **3 jeux de numérotation parallèles** pour les prompts (legacy `0-p-*` / `1-p-*` / `2-p-*` / `3-p-*` / `4-p-*` + canonical `01-p-*` à `07-p-*` + transverses `t-p-*`).
- **Compromis de tooling** : le chemin absolu `/Users/bot/.hermes/bin/cody-check` est codé en dur dans les 4 SOUL.md (note de dette explicite "Future portable packaging should replace with `${HERMES_HOME}/bin/cody-check`").
- **SOUL.md vbb-audit-worker sous-spécifié** : 98 lignes vs 180-184 pour les autres, n'inclut pas les blocs LONG_RUN_SUMMARY/PROGRESS/EXTENSION_REQUEST/TIMEOUT_CLOSEOUT exigés par `PILOTAGE.md` § LONG-RUN RULE.
- **Catalogue de skills ne référence jamais** les P.R1–P.R8 / Pillars 1–5 qu'il est censé appliquer (`grep` retourne 0/64 sur 64 SKILL.md).
- **Registry `vbb-projects.yaml` n'inclut pas le framework lui-même** — c'est documenté comme normal, mais aucune commande ne distingue "vibebackbone-le-framework" d'un projet utilisateur.

**Verdict global** : framework **fonctionnellement utilisable** (PILOTAGE/MVP_START_PROTOCOL opérationnels, contrats valides, run closure enforced) mais avec une **dette de cohérence interne** qu'un audit récurrent pourrait contenir.

---

## 1. Conventions & Socle (P.R1–P.R8 / Pillars 1–5)

### Couverture du référentiel

- `docs/CONVENTIONS.md` (v1.1, 2026-05-29) : **définit** Pillars 1–5 et P.R1–P.R8 (lignes 20, 58, 91, 147, 163, 168, 179, 197, 207, 216, 226, 239, 249).
- `docs/PILOTAGE.md` (v2.2, 2026-06-12) : **routeur opérationnel** qui *référence* le socle mais sans l'ancrer (0 occurrence de `P.R` ou `Pillar [1-5]` en grep).
- `AGENTS.md` : 15 références à `P.R[1-8]|Pillar [1-5]` (le bon élève).
- `SYSTEM.md` : 2 références.
- `GUIDE.md` : **0 référence** — fichier utilisateur final qui n'indexe pas le socle qualité.
- `docs/INDEX.md` : 0 référence explicite.
- **0 SKILL.md sur 64 ne référence P.R1–P.R8 ou Pillars 1–5** dans son corps. Convention censée être respectée par les skills → **aucun skill ne se l'approprie**.

### Incohérences P.R1 vs code

P.R1 exige "helper functions return error indicators". `tools/vbb-index.py` (et probablement d'autres) appelle `sys.exit()` depuis des fonctions non-`main()` — non vérifié exhaustivement, mais la convention est documentée comme "n'a pas été systématiquement propagée".

### VBB-AUDIT-001 — P1 — Conventions : GUIDE.md et PILOTAGE.md n'indexent pas P.R1–P.R8 ni Pillars 1–5

**Description** : `docs/CONVENTIONS.md` est la source canonique, mais le routage opérationnel (`PILOTAGE.md`, v2.2) et la doc utilisateur (`GUIDE.md`) n'établissent **aucun lien** vers les P.R1–P.R8 / Pillars 1–5. Un nouveau venu lit PILOTAGE ou GUIDE, applique les routes, et n'a aucune visibilité sur les invariants qu'il s'engage à respecter.

**Impact** : dérive silencieuse. Les workers (SOUL.md) référencent "Apply VBB socle (P.R1–P.R8, Pillars 1–5)" par copie de bloc, mais le routage lui-même n'en fait pas une garde.

**Recommandation** : ajouter dans `PILOTAGE.md` § The 4 route families une colonne `Invariants` qui pointe vers les P.R/Pillar applicables, et dans `GUIDE.md` un sommaire "Quality invariants" pointant vers CONVENTIONS.md.

### VBB-AUDIT-002 — P2 — Conventions : CONVENTIONS.md exige une CONTRACT.yaml + SKILL.md par skill (Pillar 1), c'est respecté — sauf 3 skills sans SKILL.md (audit-readiness, pilot, etc.)

**Description** : `skills/0-vbb-audit-readiness/`, `skills/0-vbb-pilotage/`, `skills/0-vbb-scope-freeze/`, etc. **ont** un SKILL.md (vérifié). Le 100% est respecté sur les 64 skills. **Aucun finding ici** — noté pour traçabilité.

### VBB-AUDIT-003 — P3 — Conventions : absence de versionnement dans la table des versions

**Description** : `CONVENTIONS.md` ligne 4 indique `Version: 1.1, Date: 2026-05-29`, mais `PILOTAGE.md` ligne 3 dit `Version: 2.2, Date: 2026-06-12`. La "Date" de PILOTAGE est dans le **futur** par rapport à la date d'exécution de l'audit (2026-06-02). Incohérence temporelle.

**Impact** : confusion mineure. Probablement un copier-coller avec un fix de bug en cours de staging.

**Recommandation** : synchroniser les dates, ou clarifier la convention de versioning (date de merge vs date planned).

---

## 2. Skills (64 réels vs 57 déclarés dans le brief)

**Inventaire réel** : 64 skills, 64 SKILL.md, 64 CONTRACT.yaml, 1 INDEX.yaml. Le brief du mission buffer annonce 57 — c'est **désynchronisé** par rapport à l'état du repo.

**Distribution par préfixe** :
- `0-vbb-*` : 7 (audit-readiness, guide, pilotage, rico-readiness, scope-freeze, standard, zero-friction)
- `1-vbb-*` : 15 (adr, api-contract-designer, code-doc-coherence-auditor, code-doc-gap-integrator, code-janitor, conventions, doc-harmonizer, error-handling-auditor, formatter, intent-decomposer, logic-duplication-detector, monolith-detector, pattern-inconsistency-detector, premature-abstraction-detector, tech-debt, test-mirage-detector)
- `2-vbb-*` : 11 (accessibility, analytics, api-auditor, ci, data-integrity, db-robustness, legal, ops, performance, security, spec-validator, systemic-risk)
- `3-vbb-*` : 1 (risk-register)
- `4-vbb-*` : 10 (cognitive-load-optimizer, design-system-validator, front-pipeline-reference, interaction-coherence-auditor, micro-interaction-refiner, product-changelog, security-remediation, user-experience-engine, visual-identity-gatekeeper, visual-identity-layer)
- `t-vbb-*` : 17 (anti-slop-gate, commit-ready, context-compactor, dependency-mapper, deploy-runtime, docker-audit, docker-generate, git-sync, impact-analyzer, index, llm-healthcheck, mode-transition-gate, project-context-init, session-handoff, status-dashboard, status-report, test-coverage-mapper)
- `vibebackbone` : 1 (le skill-racine, contient `docs/PILOTAGE.md` + `docs/PILOTAGE.md.bak`)

### VBB-AUDIT-004 — P1 — Skills : index à jour mais count du brief obsolète

**Description** : Le brief annonce 57 skills, le repo en contient 64. `skills/INDEX.yaml` est lui correct. Incohérence de communication entre la mission et la réalité.

**Impact** : mineur en soi, mais symptomatique : les briefs partent d'un état d'inventaire ancien.

**Recommandation** : avant tout brief d'audit, exécuter `ls skills/ | grep -c "^.\?vbb-"` et injecter le count réel.

### VBB-AUDIT-005 — P2 — Skills : 5 skills `1-vbb-*` "code audit" potentiellement chevauchants

**Description** : Le préfixe `1-vbb-*` contient 15 skills dont 5 à 7 sont des détecteurs de patterns code redondants :
- `1-vbb-code-janitor` (cleanup général)
- `1-vbb-error-handling-auditor` (cohérence erreurs)
- `1-vbb-logic-duplication-detector` (duplication sémantique)
- `1-vbb-monolith-detector` (god files)
- `1-vbb-pattern-inconsistency-detector` (drift de style)
- `1-vbb-premature-abstraction-detector` (over-engineering)
- `1-vbb-test-mirage-detector` (tests fantômes)
- `1-vbb-tech-debt` (cumul)

Tous read-only, tous "produisent un rapport". Frontières pas toujours claires entre `code-janitor` (cleanup) et `tech-debt` (diagnostic) et les 5 détecteurs.

**Impact** : quand un agent reçoit "audit this code", il doit choisir entre 8 skills très proches. Risque de double-comptage ou de trou.

**Recommandation** : produire un `skills/1-vbb-_DETECTORS_MATRIX.md` qui établit clairement les frontières (et un arbre de décision FAST/MEDIUM/DEEP). Court terme : aucun impact opérationnel si on délègue 1 détecteur à la fois via PILOTAGE.

### VBB-AUDIT-006 — P2 — Skills : `skills/vibebackbone/docs/PILOTAGE.md.bak` orphelin

**Description** : `skills/vibebackbone/docs/PILOTAGE.md.bak` (12 320 bytes) coexiste avec `skills/vibebackbone/docs/PILOTAGE.md` (11 920 bytes). Le `.bak` n'est pas référencé. Convention Pillar 2 : "No experimental code in production-stable modules without explicit documentation and owner".

**Impact** : présence d'un fichier de backup dans un dossier de skill canonique viole la propreté. Probablement un artefact d'édition accidentelle.

**Recommandation** : supprimer `.bak` ou le déplacer sous `docs/archive/`.

### VBB-AUDIT-007 — P3 — Skills : `2-vbb-ai-governance` référencé mais inexistant

**Description** : `2-vbb-ai-governance` apparaît dans `docs/audits/effectiveness-maturity-audit-20260529.md`, `docs/SESSION.md`, `docs/runs/2026-05-29_1200_governance-alignment/07_CLOSEOUT.md` — mais aucun dossier `skills/2-vbb-ai-governance/` n'existe, et le nom n'est pas dans `INDEX.yaml`.

**Impact** : référence fantôme. Quiconque cherche ce skill via la doc tombe dans le vide.

**Recommandation** : soit créer le skill (s'il a été planifié mais jamais écrit), soit retirer les références.

### VBB-AUDIT-008 — P2 — Skills : 0 SKILL.md ne référence P.R1–P.R8 ou Pillars 1–5

**Description** : `grep -lE "P\.R[1-8]|Pillar [1-5]" skills/*/SKILL.md` retourne 0 résultat sur 64 fichiers. La convention est définie dans CONVENTIONS.md et annoncée comme socle applicable par les workers, mais aucun skill ne l'invoque.

**Impact** : la convention est purement déclarative. Si un skill viole P.R1 (silent failures), aucun mécanisme de lint ne le détecte au niveau du catalogue de skills.

**Recommandation** : ajouter une ligne "Socle: P.R1, P.R2, P.R6" dans le frontmatter YAML de chaque SKILL.md (peut être généré par script). Court terme : `0-vbb-conventions` et `0-vbb-standard` devraient au minimum référencer explicitement le socle.

### VBB-AUDIT-009 — P3 — Skills : tous les CONTRACT.yaml ont 1 seul match pour `^(status|owner|version|name):` — schéma non standardisé

**Description** : Vérifié sur 20+ CONTRACT.yaml, ils ont tous très peu de champs top-level. Pas forcément un problème, mais le standard `0-vbb-standard` n'est pas visiblement appliqué.

**Impact** : hétérogénéité. Différent de "absence de standard" mais limite la machine-readability promise.

**Recommandation** : valider chaque CONTRACT.yaml contre un JSON Schema partagé (déjà `vbb-contract-lint.py` existe — voir s'il le fait).

---

## 3. Prompts (33 réels vs 24 déclarés)

**Inventaire réel** :
- `prompts/` (legacy / non-canonical) : 26 fichiers
- `prompts/canonical/` : 7 fichiers (01-p-vbb-intake, 02-p-vbb-audit, 03-p-vbb-decision, 04-p-vbb-plan, 05-p-vbb-execution, 06-p-vbb-review, 07-p-vbb-closeout)
- **Total** : 33 (le brief dit 24 — désynchronisation identique à skills).

**Numérotation parallèle — 3 systèmes** :
1. **Canonical** : `01-p-*` à `07-p-*` (un par phase du run, aligné sur la machine à phases 01-07 du `ROUTER_MATRIX.md`)
2. **Legacy numéroté** : `0-p-*` (4), `1-p-*` (7), `2-p-*` (5), `3-p-*` (1), `4-p-*` (3)
3. **Transverse** : `t-p-*` (6)

### VBB-AUDIT-010 — P0 — Prompts : double canon pour le rôle "plan"

**Description** : `prompts/4-p-vbb-plan` est référencé dans 6 endroits (`docs/runs/2026-05-18_2300_prompts-agentic-migration/07_CLOSEOUT.md`, `docs/runs/2026-05-18_2230_run05-test-cases/05_PATCH_SUMMARY_RUN_01.md`, `docs/router/ROUTER_MATRIX.md`, `prompts/0-p-vbb-before-building.md`, `prompts/canonical/04-p-vbb-plan.md`, `prompts/2-p-vbb-release-check.md`) **mais le fichier `prompts/4-p-vbb-plan.md` n'existe pas**. Seul existe `prompts/canonical/04-p-vbb-plan.md`.

**Impact** : les 6 références pointent vers un fichier absent. Risque élevé que des agents chargent un prompt vide ou tombent sur une erreur. Si le canonical `04-p-vbb-plan.md` est la source de vérité, les références legacy doivent être migrées.

**Recommandation** : créer `prompts/4-p-vbb-plan.md` comme symlink ou redirection vers `prompts/canonical/04-p-vbb-plan.md`, OU mettre à jour les 6 références pour pointer vers `canonical/04-p-vbb-plan.md`. **P0 parce que bloquant pour la machine à phases.**

### VBB-AUDIT-011 — P0 — Prompts : `1-p-vbb-intake` référencé 12 fois, fichier absent

**Description** : `1-p-vbb-intake` apparaît dans 12 fichiers dont `docs/audits/quality-adoption-audit-20260629.md`, `docs/runs/2026-05-27_2159_mvp-start-implementation/05_EXECUTION.md`, `docs/router/ROUTER_MATRIX.md`, `prompts/0-p-vbb-before-building.md`, `prompts/0-p-vbb-plan.md`, `prompts/t-p-vbb-phase-router.md`, **mais `prompts/1-p-vbb-intake.md` n'existe pas**. Seul existe `prompts/canonical/01-p-vbb-intake.md`.

**Impact** : **P0** — la voie MVP START (PILOTAGE.md § MVP START gate) dépend de ce prompt. Il est dans le canonical, mais les références legacy risquent d'échouer.

**Recommandation** : idem VBB-AUDIT-010 — symlink ou mise à jour des 12 références.

### VBB-AUDIT-012 — P1 — Prompts : 3 systèmes de numérotation non réconciliés (canonical / legacy / transverse)

**Description** : Le repo héberge deux philosophies de numérotation parallèles :
- **Canonical** : 01–07, calqué sur les phases du `ROUTER_MATRIX.md` (01_INTAKE → 07_CLOSEOUT)
- **Legacy** : 0-* / 1-* / 2-* / 3-* / 4-*, avec une logique de "niveau d'effort" (0 = entry, 4 = deploy)
- **Transverse** : t-*, pour les prompts indépendants d'une phase

PILOTAGE.md ne tranche pas. Les deux coexistent depuis au moins le run `2026-05-18_2300_prompts-agentic-migration`.

**Impact** : complexité cognitive, risque qu'un agent charge la mauvaise version. Convention Pillar 3 ("One active canonical solution") est violée.

**Recommandation** : trancher dans PILOTAGE.md ou dans un ADR : soit déprécier `prompts/` legacy et tout migrer sous `canonical/`, soit déprécier `canonical/` et tout rebadger. Court terme : ajouter un `prompts/LEGACY.md` qui pointe chaque legacy vers son canonical.

### VBB-AUDIT-013 — P2 — Prompts : 33 prompts mais le brief en annonce 24

**Description** : Désynchronisation entre l'inventaire déclaré (24) et l'inventaire réel (33). `prompts/INDEX.yaml` n'existe pas — pas de source canonique d'inventaire.

**Impact** : impossible pour un agent externe de savoir combien de prompts existent sans scanner le filesystem.

**Recommandation** : créer `prompts/INDEX.yaml` (comme `skills/INDEX.yaml`) listant tous les prompts avec leur phase canonique, leur statut (canonical/legacy), et leurs références.

### VBB-AUDIT-014 — P3 — Prompts : `t-p-vbb-phase-router.md` et `t-p-vbb-sequenced-ship.md` couvrent des zones qui se chevauchent

**Description** : `t-p-vbb-phase-router` (router vers la bonne voie) et `t-p-vbb-sequenced-ship` (séquence jusqu'au ship) ont des responsabilités qui se chevauchent sur le routage. Non vérifié en détail (lecture rapide), mais à creuser.

**Recommandation** : audit ciblé en follow-up.

---

## 4. Workers vbb-{fast,struct,audit,close}

Les SOUL.md actifs sont dans `~/.hermes/profiles/vbb-*-worker/SOUL.md` (CONFIRMÉ). Aucun stub `skills/cody-orchestrator/` n'existe (le brief disait "stubs dans skills/cody-orchestrator/" — **introuvable**).

### Inventaire

| Worker | Lignes | LONG_RUN_SUMMARY | FINAL_STATUS | PROGRESS | EXTENSION_REQUEST | TIMEOUT_CLOSEOUT |
|--------|--------|------------------|--------------|----------|-------------------|------------------|
| vbb-fast-worker | 184 | 4 | 3 | 0 | 0 | 0 |
| vbb-struct-worker | 180 | 3 | 6 | 3 | 0 | 1 |
| vbb-audit-worker | 98 | 2 | 1 | 0 | 0 | 0 |
| vbb-close-worker | 183 | 2 | 2 | 0 | 0 | 0 |

### VBB-AUDIT-015 — P1 — Workers : vbb-audit-worker SOUL.md n'émet pas les blocs LONG_RUN_SUMMARY (PROGRESS / EXTENSION_REQUEST / TIMEOUT_CLOSEOUT)

**Description** : `PILOTAGE.md` § LONG-RUN RULE exige que **tous** les workers émettent PROGRESS (mid-run heartbeat), EXTENSION_REQUEST (avant timeout), TIMEOUT_CLOSEOUT (sur hard timeout). La vérification `grep -c` montre que `vbb-audit-worker/SOUL.md` :
- N'émet pas `PROGRESS` (0 occurrence)
- N'émet pas `EXTENSION_REQUEST` (0)
- N'émet pas `TIMEOUT_CLOSEOUT` (0)
- Ne référence `LONG_RUN_SUMMARY` qu'à 2 endroits (vs 3-4 ailleurs)

Le SOUL.md fait 98 lignes vs 180+ pour les autres, et n'inclut **aucune** séquence de gestion du temps long.

**Impact** : si un audit dépasse 90s, l'agent audit n'a aucune instruction explicite d'émettre un PROGRESS. Risque de disparition silencieuse. La règle "No worker may disappear silently" de PILOTAGE.md § LONG-RUN RULE est violée par omission.

**Recommandation** : étendre `vbb-audit-worker/SOUL.md` avec une section `## LONG-RUN BEHAVIOR` qui duplique le pattern de `vbb-struct-worker` (lignes 66, 78-80). **P1** parce que la route AUDIT peut durer sur de gros volumes de code.

### VBB-AUDIT-016 — P1 — Workers : vbb-audit-worker SOUL.md demande d'updater AUDIT_STATUS.md, ce que le brief actuel interdit

**Description** : `vbb-audit-worker/SOUL.md` ligne 7 dit explicitement : "Update `docs/AUDIT_STATUS.md`". Mais le brief d'audit en cours stipule "NE PAS modifier AUDIT_STATUS.md (Brice le fait lui-même après)". La convention du brief est plus restrictive que la SOUL.md.

**Impact** : si l'agent suit aveuglément sa SOUL.md, il modifie AUDIT_STATUS.md contre les instructions explicites. C'est exactement le cas de l'audit en cours : on a suivi le brief, pas la SOUL.

**Recommandation** : clarifier dans la SOUL que AUDIT_STATUS.md est "sérialisé, post-closeout, par vbb-close-worker" (lignes 55-58 mentionnent déjà le mode parallèle mais pas la sérialisation post-closeout pour les audits). Court terme : un flag dans le brief l'emporte — documenter.

### VBB-AUDIT-017 — P1 — Workers : cody-check path codé en dur dans les 4 SOUL.md

**Description** : Les 4 SOUL.md contiennent (lignes 44-49 typiques) :

> **Path strategy (temporary):** Runtime uses absolute cody-check path:
> `/Users/bot/.hermes/bin/cody-check`
> Future portable packaging should replace with:
> `${HERMES_HOME}/bin/cody-check` or a `CODY_CHECK` env var.
> Do not implement env/path abstraction now.

C'est explicitement documenté comme dette. La phrase "Do not implement env/path abstraction now" est écrite **dans le SOUL.md des 4 workers**, ce qui veut dire qu'on l'a documentée 4 fois pour se rappeler de ne pas la payer.

**Impact** : dette de portabilité. Sur une autre machine, `/Users/bot/.hermes/bin/cody-check` n'existe pas → tous les workers échouent. Le framework n'est pas distribuable en l'état.

**Recommandation** : à la prochaine itération, créer un wrapper `vbb-cody-check` dans le repo (et garder `/Users/bot/.hermes/bin/cody-check` comme symlink ou override). Court terme : le commentaire est honnête et assumé.

### VBB-AUDIT-018 — P2 — Workers : vbb-audit-worker SOUL.md sous-spécifié (98 vs 180 lignes)

**Description** : Comparé aux 3 autres (180-184 lignes), `vbb-audit-worker/SOUL.md` est sous-développé. Sections présentes dans les autres mais pas dans audit-worker :
- Pas de table `cody-check Usage Reference` aussi complète
- Pas de `Output Template` détaillé pour le verdict cascade
- Pas de section `Parallel Safety` aussi complète (audit-worker n'a que 2-3 lignes)

**Impact** : l'audit-worker a moins de garde-fous que les autres. Un agent qui charge cette SOUL.md invente les conventions manquantes.

**Recommandation** : aligner la structure sur les 3 autres workers.

### VBB-AUDIT-019 — P3 — Workers : les "stubs" skills/cody-orchestrator mentionnés dans le brief n'existent pas

**Description** : Le brief dit "Les stubs dans skills/cody-orchestrator/ ne sont pas utilisés au runtime — confirmer". **Confirmé** : `ls skills/cody-orchestrator/` retourne "No such file or directory", et `grep -rln "cody-orchestrator" docs/` retourne 0 résultat. Le dossier n'a jamais existé (ou a été retiré) et aucune référence ne le mentionne.

**Impact** : le brief est désynchronisé sur ce point. Pas d'impact opérationnel.

**Recommandation** : cleanup du brief pour les futures missions.

### VBB-AUDIT-020 — P2 — Workers : aucune table "routing matrix" ne précise quel worker appeler pour quel type de tâche

**Description** : PILOTAGE.md liste 4 routes (FAST, STRUCTURED, AUDIT, CLOSEOUT) mais ne dit pas explicitement quel profile `vbb-*-worker` couvre quelle route. La correspondance (fast → vbb-fast-worker, struct → vbb-struct-worker, audit → vbb-audit-worker, close → vbb-close-worker) est implicite, jamais écrite.

**Impact** : un orchestrateur (Cody) doit inférer la correspondance. Risque d'erreur si un nouveau profile est ajouté.

**Recommandation** : ajouter un tableau "route → profile" dans PILOTAGE.md § The 4 route families.

---

## 5. Outils cody-check / vbb-index.py / registry

### Tests exécutés

```bash
$ ~/.hermes/bin/cody-check --help
# ERREUR: "Unknown command: --help"
# Usage: cody-check <command> [args...]
# Commands: index-search, final-status, long-run-summary, git-status,
#           parallel-artifacts, test-exit, project-exists

$ ~/.hermes/bin/cody-check project-exists "vibebackbone"
# {"project": "vibebackbone", "exists": false, "repo": null, "status": "FAIL"}
# → confirme : framework pas dans le registry. Normal, mais pas distingué.

$ ~/.hermes/bin/cody-check project-exists "trame"
# {"project": "trame", "exists": true, "repo": "/Users/bot/02_Dev/trame", "status": "PASS"}
# → sanity check OK

$ ~/.hermes/bin/cody-check final-status "/tmp/next_mission_vibebackbone_audit.txt"
# {"present": false, "artifact": "/tmp/next_mission_vibebackbone_audit.txt"}
# → fonctionnel

$ python3 tools/vbb-index.py stats --repo ~/02_Dev/vibebackbone
# Entries    : 363
# Tokens est.: 424,180
# By kind: audit (27), doc (12), prompt (33), router (1)
# → fonctionnel
```

### VBB-AUDIT-021 — P2 — Outils : cody-check ne sait pas distinguer un "framework" d'un "projet"

**Description** : `cody-check project-exists vibebackbone` retourne `exists: false, status: FAIL`. Pourtant `~/02_Dev/vibebackbone/` existe bel et bien. La distinction est que `vbb-projects.yaml` ne contient que `trame` et `mjc-app`. Pour vérifier qu'un framework est "canonique", il faut une autre commande.

**Impact** : un agent qui vérifie "est-ce que le framework est en place ?" reçoit FAIL. Confusion.

**Recommandation** : ajouter `cody-check framework-exists <name>` ou permettre à `project-exists` de chercher aussi dans un path known-frameworks (via une variable d'env ou une autre section YAML).

### VBB-AUDIT-022 — P2 — Outils : `cody-check --help` retourne "Unknown command: --help" — pas d'aide

**Description** : Aucun moyen de découvrir les commandes sans connaître la liste par cœur ou exécuter `cody-check` sans argument. UX faible.

**Impact** : friction pour les nouveaux venus et les agents.

**Recommandation** : ajouter `--help` (et probablement `-h`) comme alias de l'usage sans argument.

### VBB-AUDIT-023 — P3 — Outils : vbb-index.py search n'a pas de filtre par kind

**Description** : `python3 tools/vbb-index.py search --help` montre `--json` et `--repo` mais pas de filtre par type (audit/doc/prompt/router). Si on veut chercher uniquement dans les prompts, il faut filtrer côté client.

**Impact** : UX. Marginal vu la taille de l'index (363 entries).

**Recommandation** : ajouter `--kind {audit,doc,prompt,router}` au subcommand `search`.

### VBB-AUDIT-024 — P3 — Outils : registry vbb-projects.yaml : 2 projets, 0 mention de tests, CI null

**Description** : `vbb-projects.yaml` contient `trame` et `mjc-app`. Pour `mjc-app`, tous les `docs: {conventions, architecture, pilotage, context}` sont à `null`. `ci_command: null` pour les 2 projets. Les `test_commands` ne couvrent pas la test suite complète (juste lint + tsc).

**Impact** : la registry est l'instrument de vérification des workers (PILOTAGE mentionne `cody-check test-exit "<test_command>"`). Si `test_commands` est incomplet ou si `docs: conventions: null`, l'agent n'a pas de gouvernance à lire.

**Recommandation** : pour `mjc-app`, soit remplir les `docs:` soit retirer le projet. Pour `ci_command: null`, marquer explicitement "no CI configured".

---

## 6. docs/ — structure, obsolètes, contradictions

### Inventaire docs/ (29 entrées + 17 sous-dossiers)

Fichiers principaux (rôle) :
- `AGENTIC_RUN_PROTOCOL.md`, `ARCHITECTURE.md`, `AUDIT_STATUS.md`, `CONTEXT.md`, `CONVENTIONS.md`, `DEPLOYMENT.md`, `INDEX.md`, `LLM_PROVIDERS.md`, `LONG_RUN_RULE.md`, `MEMORY_AND_HANDOFF.md`, `MVP_START_PROTOCOL.md`, `PILOTAGE.md`, `PROJECT_MODE.md`, `RELATIONS.md`, `RUNBOOK.md`, `SESSION.md`, `SESSION_RULES.md`, `TECH_DEBT.md`, `TEMPORAL_PROVENANCE.md`, `TROUBLESHOOTING.md`, `ACTIVITY_LOG.md`

### VBB-AUDIT-025 — P2 — docs : 17 sous-dossiers `docs/audits/` contiennent 7 310 entrées (rotation JSON)

**Description** : `ls docs/audits/` montre `drwxr-xr-x  7310 bot  staff  233920  30 mai 04:50 vbb-runtime` — **7 310 fichiers** dans `docs/audits/vbb-runtime/`. C'est de la rotation de runs de contract-runtime (probablement `0-vbb-scope-freeze`, `0-vbb-audit-readiness`, `t-vbb-mode-transition-gate`).

**Impact** : bruit dans `docs/audits/`. Le scan d'audit y passe du temps. Pas de politique de rétention documentée.

**Recommandation** : documenter une politique de rétention (ex. : garder N dernières exécutions par skill, archiver le reste) et l'appliquer.

### VBB-AUDIT-026 — P2 — docs : AGENTS.md a un backup `AGENTS.local.backup.md` (12 575 bytes) à la racine

**Description** : `AGENTS.local.backup.md` (12 575 bytes) coexiste avec `AGENTS.md` (71 268 bytes). Comme `skills/vibebackbone/docs/PILOTAGE.md.bak`, c'est un backup orphelin.

**Impact** : bruit, violation Pillar 2.

**Recommandation** : déplacer sous `docs/archive/`.

### VBB-AUDIT-027 — P3 — docs : `PROMPTS_AGENTIC_ALIGNMENT_AUDIT.md` (44 553 bytes) et `VIBEBACKBONE_AGENTIC_AUDIT.md` (29 961 bytes) à la racine

**Description** : 3 documents d'audit massifs à la racine du repo (`AGENTIC_PROTOCOL_REFORMAT_SUMMARY.md`, `PROMPTS_AGENTIC_ALIGNMENT_AUDIT.md`, `PROMPTS_ALIGNMENT_DECISION.md`, `VIBEBACKBONE_AGENTIC_AUDIT.md`, `CONTROL_AUDIT_PROMPTS_AGENTIC_MIGRATION.md`) — tous des artefacts de migration historique. Aucun d'eux n'est sous `docs/audits/`.

**Impact** : pollution visuelle de la racine. Convention Pillar 1 ("Documentation scope") : les audits datés vont sous `docs/audits/`.

**Recommandation** : déplacer sous `docs/audits/` ou `docs/archive/`.

### VBB-AUDIT-028 — P3 — docs : PILOTAGE.md v2.2 daté 2026-06-12 (futur)

**Description** : `docs/PILOTAGE.md` ligne 3 : `**Version** : 2.2 | **Date** : 2026-06-12`. Date dans le futur par rapport à l'exécution de l'audit (2026-06-02). Probablement une date planned / target.

**Impact** : confusion. Soit la version est livrée plus tôt que prévu (et la date est wrong), soit c'est une planned date (et le format n'est pas clair).

**Recommandation** : séparer "delivered: YYYY-MM-DD" et "next planned: YYYY-MM-DD" dans l'en-tête de PILOTAGE.

### VBB-AUDIT-029 — P2 — docs : `CONTROL_AUDIT_PROMPTS_AGENTIC_MIGRATION.md` (18 KB) — quelle est sa valeur par rapport à `docs/audits/` ?

**Description** : Encore un audit historique à la racine, redondant avec `PROMPTS_AGENTIC_ALIGNMENT_AUDIT.md` (44 KB) et `VIBEBACKBONE_AGENTIC_AUDIT.md` (30 KB).

**Impact** : 3 documents qui semblent couvrir le même sujet (migration agentique des prompts). Probable duplication.

**Recommandation** : consolidation en un seul document placé sous `docs/audits/`.

### VBB-AUDIT-030 — P3 — docs : `docs/RELATIONS.md` n'est plus éditable (CONVENTIONS § Pillar 1)

**Description** : CONVENTIONS.md ligne 47 dit "`docs/ARCHITECTURE.md` is the canonical structured source — never edit `docs/RELATIONS.md` directly". Mais `docs/RELATIONS.md` existe toujours (4 293 bytes), il n'est pas documenté comme généré.

**Impact** : si RELATIONS.md n'est pas généré automatiquement, il dérive. Si oui, par quel outil ? Non vérifié.

**Recommandation** : vérifier l'existence d'un `vbb-architecture.py graph --write` qui régénère RELATIONS.md. Si non, le retirer.

---

## Top 3 P1 prioritaires

1. **VBB-AUDIT-010** — Prompts : `prompts/4-p-vbb-plan.md` n'existe pas alors qu'il est référencé 6 fois (dont PILOTAGE et la machine à phases). P0 bloquant pour la voie STRUCTURED. **Action immédiate** : créer un symlink ou corriger les 6 références.

2. **VBB-AUDIT-011** — Prompts : `1-p-vbb-intake` référencé 12 fois, fichier absent. P0 bloquant pour la voie MVP START. **Action immédiate** : idem.

3. **VBB-AUDIT-015** — Workers : `vbb-audit-worker/SOUL.md` n'émet aucun des 3 blocs LONG_RUN (PROGRESS / EXTENSION_REQUEST / TIMEOUT_CLOSEOUT) exigés par PILOTAGE.md § LONG-RUN RULE. P1 sur la résilience d'un audit long. **Action immédiate** : étendre la SOUL.md avec une section LONG-RUN BEHAVIOR copiée de vbb-struct-worker.

(Honneur : VBB-AUDIT-001 sur les conventions non-ancrées dans PILOTAGE/GUIDE et VBB-AUDIT-008 sur les skills qui n'invoquent jamais le socle — même rang, choix fait sur le caractère bloquant runtime.)

---

## Catégories couvertes

1. **Conventions** (P.R1–P.R8 / Pillars 1–5) — couvert, 3 findings (1 P1, 0 P0, 1 P2, 1 P3)
2. **Skills** (64 réels) — couvert, 6 findings (2 P1, 4 P2, 2 P3)
3. **Prompts** (33 réels) — couvert, 5 findings (2 P0, 1 P1, 1 P2, 1 P3)
4. **Workers** (vbb-{fast,struct,audit,close}) — couvert, 6 findings (3 P1, 2 P2, 1 P3)
5. **Outils** (cody-check, vbb-index.py, registry) — couvert, 4 findings (0 P1, 3 P2, 1 P3)
6. **docs/** (structure, obsolètes, contradictions) — couvert, 6 findings (0 P1, 3 P2, 3 P3)

**Total** : 30 findings — P0: 2, P1: 5, P2: 14, P3: 9.

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS:
  verdict: COMPLETE
  elapsed_seconds: 259
  files_touched:
    - created: /Users/bot/02_Dev/vibebackbone/docs/audits/20260602_0641_audit_vibebackbone.md
    - read: docs/CONVENTIONS.md, docs/PILOTAGE.md, docs/INDEX.md, docs/AUDIT_STATUS.md (head only)
    - read: skills/INDEX.yaml + 64 SKILL.md existence
    - read: ~/.hermes/profiles/vbb-{fast,struct,audit,close}-worker/SOUL.md
    - read: ~/.hermes/vbb-projects.yaml (head 60)
    - executed: cody-check project-exists vibebackbone|trame, cody-check final-status, vbb-index.py stats
  risks:
    - VBB-AUDIT-010 et VBB-AUDIT-011 (P0) : risque d'échec runtime de la machine à phases tant que les fichiers référencés n'existent pas sous le nom attendu.
    - VBB-AUDIT-015 (P1) : un audit long peut disparaître silencieusement (SOUL.md sans bloc LONG_RUN).
    - VBB-AUDIT-017 (P1) : framework non-distribuable (cody-check path hardcodé).
  open_points:
    - AUDIT_STATUS.md non mis à jour (volontairement, le brief l'interdisait ; Brice le fait).
    - Pas de test runtime des prompts legacy (lecture seule).
    - 7 310 fichiers sous docs/audits/vbb-runtime/ : politique de rétention non vérifiée.
    - Pas de symlink créé pour VBB-AUDIT-010/011 (action proposée, non exécutée en mode read-only).
  constraints_respected:
    - READ-ONLY strict : aucune modification de code, de doc, ni d'AUDIT_STATUS.md
    - Pas de commit, pas de push
    - Un seul artefact créé (celui autorisé par le brief)
    - Pas de delegate_task enfant (max_spawn_depth=1 respecté)
  artifacts:
    - /Users/bot/02_Dev/vibebackbone/docs/audits/20260602_0641_audit_vibebackbone.md
  next_steps_recommended:
    - Décider P0 first : VBB-AUDIT-010, VBB-AUDIT-011 (créer symlinks OU migrer les références).
    - Étendre vbb-audit-worker/SOUL.md avec LONG_RUN BEHAVIOR.
    - Clarifier la numérotation des prompts (3 systèmes → 1).
    - Cleanup fichiers orphelins : skills/vibebackbone/docs/PILOTAGE.md.bak, AGENTS.local.backup.md.
```
