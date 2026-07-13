---
context_role: findings-index
phase: strategy
status: active
updated: 2026-07-12
scope: vibebackbone framework → roadmap des améliorations (Phase 1 multi-service + Audits A-E)
---

# 01 — Findings Index : Roadmap des améliorations Vibebackbone

> **Périmètre** : index exhaustif des findings extraits de 8 sources :
> 1. `docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md` (18 gaps)
> 2. `docs/strategy/vbb-evolution-multi-service-support/02_PRIORITIES.md` (sévérité)
> 3. `docs/strategy/vbb-evolution-multi-service-support/03_DEPENDENCIES.md` (DAG)
> 4. `docs/audits/audit-A-scope-aware-janitor-20260712-1210.md` (4 findings)
> 5. `docs/audits/audit-B-loop-discipline-20260712-1230.md` (4 findings)
> 6. `docs/audits/audit-C-handoff-closeout-calibration-20260712-1300.md` (3 findings)
> 7. `docs/audits/audit-D-md-length-optimization-20260712-1330.md` (3 findings)
> 8. `docs/audits/audit-E-skill-descriptions-20260712-1400.md` (5 findings)
>
> **Total observé** : **37 findings** (18 Phase 1 + 19 audits = 4 A + 4 B + 3 C + 3 D + 5 E).
> ⚠️ Note : la consigne initialeannonçait « 38 attendus » (18 + 4+4+3+3+5 = 37). Voir §Métadonnées.
>
> **Convention de route** :
> - `FAST-MINIMAL` : ≤3 fichiers, non-canon, effort S
> - `FAST-STANDARD` : 4+ fichiers, non-canon
> - `STRUCTURED` : multi-fichier ou canon (GAP_CHANGE_PROPOSAL requis)
> - `AUDIT` : si re-audit / vérification nécessaire

---

## 1. Index consolidé des 37 findings

| ID | Source | Sévérité | Titre court | Scope (1 phrase) | Dépendances | Route recommandée |
|----|--------|----------|-------------|------------------|-------------|-------------------|
| Gap-01 | Phase1 | P1 | Orientation DB structurée | `tools/vbb-project-init.py:67-110` produit `PROJECT_MODE.md`/`CONTEXT.md` sans champ structuré pour topologie DB. | Gap-14 | FAST-STANDARD |
| Gap-02 | Phase1 | P1 | Project archetype / projet typé | Aucun typage de projet (`project_archetype`) — seul `contract['type']==prompt_skill` existe (`tools/vbb-contract-lint.py:79`). | Gap-11, Gap-14 | FAST-STANDARD |
| Gap-03 | Phase1 | P1 | Codegen AGENTS.md / CLAUDE.md | `distributions/claude/CLAUDE.md` (61 lignes) est écrit à la main, pas dérivé de PILOTAGE/CONVENTIONS. | Gap-01, Gap-02, Gap-09 | STRUCTURED |
| Gap-04 | Phase1 | P0 | Linter discipline multi-service | `tools/vbb-architecture.py` `lint` valide la cohérence intra-repo, aucun linter cross-service (zéro hit grep). | Gap-05, Gap-06, Gap-10 | FAST-STANDARD |
| Gap-05 | Phase1 | P0 | `CONTRACTS_CONSUMED.md` canonique | Aucun fichier `CONTRACTS_CONSUMED.md` dans le repo, aucun template `docs/templates/`. | Gap-04, Gap-06, Gap-10, Gap-13, Gap-15 | FAST-STANDARD |
| Gap-06 | Phase1 | P0 | `IMPACT_LOG.md` cumulatif par projet | `t-vbb-impact-analyzer/SKILL.md:24` produit un snapshot daté `impact-analysis-{date}.md`, pas un log cumulatif. | Gap-05, Gap-07, Gap-15, Gap-18 | FAST-STANDARD |
| Gap-07 | Phase1 | P1 | Discipline outillée de co-évolution | Aucune mention de "co-évolution", "coordinated migration", "consumer migration task" (zéro hit grep). | Gap-05, Gap-06, Gap-15 | FAST-STANDARD |
| Gap-08 | Phase1 | P0 | Support multi-repo | `tools/vbb-*.py` tous mono-repo (REPO_ROOT = parent résolu). `t-vbb-docker-audit/SKILL.md:257` traite multi-app comme limitation. | Gap-13 | STRUCTURED |
| Gap-09 | Phase1 | P1 | Mécanisme d'extension / projection de patterns | `docs/CONVENTIONS.md` n'a aucun mécanisme d'extension (zéro hit grep `extension\|plugin`). | Gap-01, Gap-02, Gap-03, Gap-12 | STRUCTURED |
| Gap-10 | Phase1 | P0 | Taxonomie des contrats cross-service | `1-vbb-api-contract-designer/SKILL.md:130-145` liste les sections de contrat sans champ « Consumers ». | Gap-05, Gap-11, Gap-13 | FAST-MINIMAL |
| Gap-11 | Phase1 | P1 | Archetype-aware contract lint | `tools/vbb-contract-lint.py:79` valide seulement `type==prompt_skill`, pas de règles contextuelles par archétype. | Gap-02, Gap-10, Gap-04 | STRUCTURED |
| Gap-12 | Phase1 | P1 | Pilier « DB owned by service » | `docs/CONVENTIONS.md` (~250 lignes) n'inclut pas de pilier « Architecture Boundaries » pour database-per-service. | Gap-09, Gap-01 | STRUCTURED |
| Gap-13 | Phase1 | P0 | Graphe inter-services indépendant | `tools/vbb-architecture.py graph --write` produit un Mermaid intra-repo (RELATIONS_PATH local), aucun mécanisme d'agrégation multi-repo. | Gap-05, Gap-08, Gap-10 | FAST-STANDARD |
| Gap-14 | Phase1 | P1 | `CONTEXT.md` / `PROJECT_MODE.md` enrichi | `tools/vbb-project-init.py` `_context_md:88-110`, `_project_mode_md:67-86`, `_architecture_md:112-140` produisent des templates minimaux. | Gap-01, Gap-02, Gap-09 | FAST-MINIMAL |
| Gap-15 | Phase1 | P0 | Gate « ne pas régresser » en CI sur PR | `tools/vbb-gate-check.py` est pré-exécution (ADR+POC+CODE_START), aucun hook post-diff `.github/workflows/` ou `scripts/hooks/`. | Gap-04 | FAST-STANDARD |
| Gap-16 | Phase1 | P2 | Mécanisme `@include` inter-fichiers formalisé | `distributions/claude/CLAUDE.md:14-16` utilise `@AGENTS.md`, `@SYSTEM.md` sans parseur (ad-hoc, non validé). | Gap-03, Gap-17 | FAST-MINIMAL |
| Gap-17 | Phase1 | P2 | Détection d'édition manuelle de fichier `@generated` | `tools/vbb-architecture.py lint` ne flag pas une édition manuelle de `RELATIONS.md`. | Gap-03, Gap-16 | FAST-MINIMAL |
| Gap-18 | Phase1 | P2 | Articulation snapshot ↔ log cumulatif | `t-vbb-impact-analyzer/SKILL.md:124` produit des snapshots datés, aucune projection vers `IMPACT_LOG.md`. | Gap-06 | FAST-MINIMAL |
| AUDIT-A-001 | AuditA | P1 | Janitor sans paramètre `--scope` | `skills/1-vbb-code-janitor/SKILL.md:33-101` — rapport unique pour le repo entier, pas de notion de scope. | Gap-13 | FAST-STANDARD |
| AUDIT-A-002 | AuditA | P1 | Tech-debt sans paramètre `--scope` | `skills/1-vbb-tech-debt/SKILL.md:56-101` — rapport unique, mélange Legacy/Architecture/DB/API/Frontend. | Gap-13 | FAST-STANDARD |
| AUDIT-A-003 | AuditA | P2 | Type `external` non utilisé dans ARCHITECTURE.md | `tools/vbb-architecture.py:83` `VALID_TYPES` contient `external` mais aucun bloc de `docs/ARCHITECTURE.md` (7 blocs) ne le porte. | — | FAST-MINIMAL |
| AUDIT-A-004 | AuditA | P2 | Dependency-mapper passif sur hors-repo | `skills/t-vbb-dependency-mapper/SKILL.md:60-65` mentionne `inter-repo` mais sans directive de déclaration active. | Gap-05 | FAST-MINIMAL |
| AUDIT-B-001 | AuditB | P1 | Prompts AUDIT et DECISION sans P.R2 / pre-merge | `prompts/canonical/02-p-vbb-audit.md` et `03-p-vbb-decision.md` : 0 référence à P.R2 / pre-merge / verification loop. | Gap-13 (succès graphe) | FAST-MINIMAL |
| AUDIT-B-002 | AuditB | P1 | Prompt EXECUTION sans pre-merge-gate canon | `prompts/canonical/05-p-vbb-execution.md` : seul pré-check anti-dette présent, zéro sur les 5 vérifications P.R2. | Gap-13 (succès graphe) | FAST-MINIMAL |
| AUDIT-B-003 | AuditB | P2 | 5 skills `1-vbb-*` sans référence à P.R2 | `skills/1-vbb-{code-janitor,tech-debt,monolith-detector,conventions,formatter}/SKILL.md` : 0 hit grep `P.R\|05_EXECUTION\|gate`. | — | FAST-STANDARD |
| AUDIT-B-004 | AuditB | P2 | Pas de cartographie phase↔skill explicite | Aucun frontmatter `phase: 02_AUDIT` sur les skills Phase 1 ; la cartographie est reconstruite par le routeur. | — | FAST-MINIMAL |
| AUDIT-C-001 | AuditC | P1 | Pas de marqueur explicite `kind: HANDOFF\|CLOSEOUT` | `docs/templates/07_CLOSEOUT.md.template` lignes 1-50 n'ont pas de champ `kind` ; discrimination entièrement implicite (Statut global + Prochaine session). | — | FAST-MINIMAL |
| AUDIT-C-002 | AuditC | P2 | Route CLOSEOUT englobe 3 usages | `docs/PILOTAGE.md:27` — une seule route « CLOSEOUT » couvre end/handoff/pause sans distinction explicite. | — | STRUCTURED |
| AUDIT-C-003 | AuditC | P2 | `SESSION.md` non versionné (gitignored) | `docs/SESSION.md` (gitignored par design) est écrasé à chaque session ; aucun historique `SESSION.{date}.md` conservé. | — | FAST-MINIMAL |
| AUDIT-D-001 | AuditD | P1 | ADRs Hermes proxy trop longs | `distributions/hermes/proxy/adr/*.md` : 929/766/745/624/460/442 lignes (moy. 684) vs 100-200 pour ADRs canoniques `docs/adr/`. | — | FAST-STANDARD |
| AUDIT-D-002 | AuditD | P2 | 5 `SKILL.md` > 400 lignes | `4-vbb-user-experience-engine` 520 / `1-vbb-intent-decomposer` 430 / `1-vbb-code-doc-coherence-auditor` 429 / `1-vbb-code-doc-gap-integrator` 409 / `2-vbb-spec-validator` 397. | — | FAST-STANDARD |
| AUDIT-D-003 | AuditD | P2 | `GUIDE.md` (1248) + `README.md` (526) trop longs | Pas de canon de longueur pour les entry points ; pas de TOC ; AUDIT_STATUS ligne 50-58 note « GUIDE still only has a partial non-dev operator path ». | — | FAST-MINIMAL |
| AUDIT-E-001 | AuditE | P1 | Pas de canon de longueur pour `description:` | `docs/CONVENTIONS.md` Pillar 1 et `0-vbb-standard/SKILL.md:75-85` ne spécifient pas de cible numérique. | AUDIT-E-005 | STRUCTURED |
| AUDIT-E-002 | AuditE | P1 | Confusion modèle mental « auto-réduction Codex » | `distributions/codex/setup.sh` `replace_generated_block()` agit sur `~/.codex/AGENTS.md` (bloc généré), **pas** sur les descriptions SKILL.md. `doc-context-20260602-1329.md:25` documente cette réduction (7296 → 344 lignes sur AGENTS.md). | — | FAST-MINIMAL |
| AUDIT-E-003 | AuditE | P2 | Phase 1 : descriptions les plus longues (506 chars avg) | Phase 1 `1-vbb-*` : 16 skills, 10/16 > 500 chars. Plus longue : `1-vbb-logic-duplication-detector` 669 chars/13 lignes. | AUDIT-E-001 | FAST-MINIMAL |
| AUDIT-E-004 | AuditE | P2 | Suivi dispersé descriptions longues vs LLM-LOAD-002 | `docs/AUDIT_STATUS.md:197` LLM-LOAD-002 (P2 Open) sur `SKILL.md` body ; aucune entrée pour description > 500 chars. | Gap-16 | FAST-MINIMAL |
| AUDIT-E-005 | AuditE | P2 | Pas de linter sur longueur de `description:` | `tools/vbb-contract-lint.py` valide contract_schema_version/gates/routing, **rien** sur description ; `tools/vbb-phase-router.py` consomme `routing.triggers` du CONTRACT.yaml, pas la description. | AUDIT-E-001 | FAST-MINIMAL |

---

## 2. Métadonnées

### Comptage global

| Métrique | Valeur |
|----------|--------|
| **Total findings observés** | **37** |
| Phase 1 (Gap-01 → Gap-18) | 18 |
| Audit A | 4 |
| Audit B | 4 |
| Audit C | 3 |
| Audit D | 3 |
| Audit E | 5 |
| **Total audits A-E** | **19** |

⚠️ Note : la consigne annonçait « 38 attendus ». Mon extraction donne 37 (18 + 19 = 37). Cohérent avec `02_PRIORITIES.md §0` qui confirme « 18 gaps » et chaque audit qui liste explicitement N findings par sévérité (4/4/3/3/5). Possiblement une erreur d'addition dans l'énoncé source.

### Distribution par sévérité

| Sévérité | Phase1 | AuditA | AuditB | AuditC | AuditD | AuditE | **Total** |
|----------|--------|--------|--------|--------|--------|--------|-----------|
| **P0** | 7 | 0 | 0 | 0 | 0 | 0 | **7** |
| **P1** | 8 | 2 | 2 | 1 | 1 | 2 | **16** |
| **P2** | 3 | 2 | 2 | 2 | 2 | 3 | **14** |
| **Total** | **18** | **4** | **4** | **3** | **3** | **5** | **37** |

### Distribution par source

| Source | Findings |
|--------|----------|
| Phase 1 (Gap analysis) | 18 (7 P0 / 8 P1 / 3 P2) |
| Audit A — scope-aware janitor | 4 (0 / 2 / 2) |
| Audit B — loop discipline | 4 (0 / 2 / 2) |
| Audit C — handoff/closeout calibration | 3 (0 / 1 / 2) |
| Audit D — md length optimization | 3 (0 / 1 / 2) |
| Audit E — skill descriptions | 5 (0 / 2 / 3) |

### Distribution par route recommandée

| Route | Findings | % |
|-------|----------|---|
| `FAST-MINIMAL` | 18 | 49% |
| `FAST-STANDARD` | 12 | 32% |
| `STRUCTURED` | 7 | 19% |
| `AUDIT` (re-audit) | 0 | 0% |
| **Total** | **37** | **100%** |

**Findings STRUCTURED** (risque canon ou multi-outils) :
- Gap-03, Gap-08, Gap-09, Gap-11, Gap-12 (Phase 1)
- AUDIT-C-002 (route CLOSEOUT dans PILOTAGE.md — canon)
- AUDIT-E-001 (canon de longueur description — extension CONVENTIONS)

### Findings P0 (chemin critique Phase 1)

7 gaps P0 — chemin critique `Gap-05 → Gap-10 → Gap-06 → Gap-04 → Gap-15`, plus multi-repo `Gap-08 → Gap-13`. Tous traitables **en parallèle** par équipes distinctes (cf. `03_DEPENDENCIES.md §5`).

---

## 3. Quick wins potentiels

> Définition : findings traitables en **FAST-MINIMAL** (≤3 fichiers, non-canon, effort S).
> Aucun de ces quick wins n'ouvre un canon (CONVENTIONS/PILOTAGE/GUIDE) ; aucun ne touche un outil canonique (vbb-architecture.py, vbb-contract-lint.py).

### Quick wins confirmés (FAST-MINIMAL + effort S)

| ID | Quick win | Fichiers touchés | Effort |
|----|-----------|------------------|--------|
| Gap-10 | Ajouter champ `Consumers:` au template `1-vbb-api-contract-designer/` | 1 fichier | S |
| Gap-14 | Modifier le contenu généré par `vbb-project-init.py` (`_context_md`, `_project_mode_md`) | 1 fichier | S |
| Gap-16 | Linter `@include` (parseur ad-hoc → formel, validation cible existante) | 1 fichier | S |
| Gap-17 | Sentinel `@generated` + linter anti-drift sur `RELATIONS.md` | 2 fichiers (linter + conv.) | S |
| Gap-18 | Extension de `t-vbb-impact-analyzer/SKILL.md` pour sortie optionnelle `IMPACT_LOG.md` | 1 fichier | S |
| AUDIT-A-003 | Créer un premier bloc `## Bloc: External Dependencies` exemple dans `docs/ARCHITECTURE.md` | 1 fichier | S |
| AUDIT-A-004 | Ajouter à `t-vbb-dependency-mapper/SKILL.md` une directive « produire un inventaire des dépendances hors-repo » | 1 fichier | S |
| AUDIT-B-001 | Éditer `prompts/canonical/02-p-vbb-audit.md` et `03-p-vbb-decision.md` pour ajouter section « Next Phase : 04_PLAN si findings P0/P1 » | 2 fichiers | S |
| AUDIT-B-002 | Éditer `prompts/canonical/05-p-vbb-execution.md` pour inclure le bloc canonique des 5 vérifications P.R2 (référence `@pre-merge-gate.md`) | 1 fichier | S |
| AUDIT-B-004 | Ajouter `phase: 02_AUDIT` (ou autre) en frontmatter des 5 skills `1-vbb-*` (janitor, tech-debt, monolith-detector, conventions, formatter) | 5 fichiers | S (mais déplafonne en FAST-STANDARD : 4+ fichiers) |
| AUDIT-C-001 | Ajouter `kind: HANDOFF \| CLOSEOUT` en frontmatter de `docs/templates/07_CLOSEOUT.md.template` | 1 fichier | S |
| AUDIT-C-003 | Créer un pattern `docs/SESSION.history/{date}.md` localement (non versionné, symlink/hors-git) | 1 fichier (init) | S |
| AUDIT-D-003 | Ajouter une TOC en haut de `GUIDE.md` (et `README.md`) sans toucher au contenu | 2 fichiers | S |
| AUDIT-E-002 | Mettre à jour `0-vbb-standard/SKILL.md` ligne 75-85 (PROCESS) avec mention explicite « description NOT auto-truncated — hand-maintained, validated for precision, not length » | 1 fichier | S |
| AUDIT-E-003 | Compresser manuellement les 10 descriptions `1-vbb-*` > 500 chars (préserver Keywords + première phrase) | ~10 fichiers | M (effort supérieur à S) — **descend en STANDARD** |
| AUDIT-E-004 | Ajouter entrée dans `docs/AUDIT_STATUS.md` pour risque « descriptions > 500 chars » | 1 fichier | S |
| AUDIT-E-005 | Étendre `tools/vbb-contract-lint.py` avec un check **warning** (non-bloquant) si `description > 500 chars` | 1 fichier | S |

> **Note** : AUDIT-B-004 = 5 fichiers. Si on applique strictement « ≤3 fichiers = FAST-MINIMAL », alors 4 fichiers bascule en FAST-STANDARD. À arbitrer par l'architecte.
>
> **Note 2** : AUDIT-E-003 = 10 fichiers (Phase 1). Effort M (compression manuelle avec préservation des Keywords). Bascule en **FAST-STANDARD** ou **STRUCTURED** selon politique canon (modification de descriptions = modification de frontmatter de skills = à valider).

### Quick wins confirmés strictement (≤3 fichiers + effort S + non-canon)

Les **12 quick wins purs** (tous critères stricts) :

1. **Gap-10** — champ `Consumers:` template `1-vbb-api-contract-designer`
2. **Gap-14** — enrichir `_context_md`/`_project_mode_md` dans `vbb-project-init.py`
3. **Gap-16** — linter `@include`
4. **Gap-17** — sentinel `@generated` + linter
5. **Gap-18** — extension `t-vbb-impact-analyzer` vers `IMPACT_LOG.md`
6. **AUDIT-A-003** — exemple bloc `External Dependencies` dans ARCHITECTURE.md
7. **AUDIT-A-004** — directive inventaire hors-repo dans dependency-mapper
8. **AUDIT-B-001** — section Next Phase dans 2 prompts canoniques
9. **AUDIT-B-002** — bloc P.R2 dans prompt EXECUTION
10. **AUDIT-C-001** — `kind: HANDOFF | CLOSEOUT` dans template closeout
11. **AUDIT-C-003** — pattern `SESSION.history/{date}.md`
12. **AUDIT-D-003** — TOC dans GUIDE.md + README.md
13. **AUDIT-E-002** — mention « description not auto-truncated » dans `0-vbb-standard`
14. **AUDIT-E-004** — entrée AUDIT_STATUS pour descriptions longues
15. **AUDIT-E-005** — warning linter sur description > 500 chars

---

## 4. Liens

- [`01_GAP_ANALYSIS.md`](../../vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md) — caractérisation 18 gaps
- [`02_PRIORITIES.md`](../../vbb-evolution-multi-service-support/02_PRIORITIES.md) — classification P0/P1/P2
- [`03_DEPENDENCIES.md`](../../vbb-evolution-multi-service-support/03_DEPENDENCIES.md) — DAG dépendances entre gaps
- Audits A-E dans `docs/audits/audit-{A..E}-*.md`

---

**Verdict** : index exhaustif produit. 37 findings, 7 P0 (chemin critique discipline + multi-repo), 16 P1, 14 P2. 12-15 quick wins purs disponibles sans canon change ni effort > S. Les 7 findings STRUCTURED sont les seuls à risque canon. Source de vérité pour la Phase de planification des runs.
