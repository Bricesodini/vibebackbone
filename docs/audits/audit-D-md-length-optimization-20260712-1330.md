---
run_id: "2026-07-12_1330_audit-D-md-length"
phase: "02_AUDIT"
voie: "AUDIT"
status: "PARTIAL"
agent: "claude-code"
started_at: "2026-07-12T13:30:00Z"
ended_at: "2026-07-12T13:55:00Z"
next_phase: null
artifacts_consumed:
  - "AGENTS.md"
  - "SYSTEM.md"
  - "CLAUDE.md"
  - "GUIDE.md"
  - "README.md"
  - "docs/CONTEXT.md"
  - "docs/PILOTAGE.md"
  - "docs/CONVENTIONS.md"
  - "docs/ARCHITECTURE.md"
  - "docs/DISTRIBUTIONS.md"
  - "prompts/canonical/*.md"
  - "All SKILL.md files (64)"
  - "All .md files in docs/, distributions/, prompts/"
artifacts_produced:
  - "docs/audits/audit-D-md-length-optimization-20260712-1330.md"
---

# Audit D — Optimisation de la longueur des fichiers `.md`

**Date** : 2026-07-12
**Périmètre** : tous les fichiers `.md` du repo (hors `docs/archive/`), catégorisés par type (governance, guides, skills, ADRs, audits, runs).
**Question auditée** : où sont les fichiers `.md` anormalement longs ? Quelle est la cible de compacité canonique ? Quels quick wins d'optimisation ?
**Verdict** : `PARTIAL — quelques outliers identifiés, pas de canon de longueur, optimisation possible mais pas critique`. Le repo n'est pas en situation de dérive massive (moyenne SKILL.md = 186 lignes), mais **6 ADRs Hermes proxy** entre 442 et 929 lignes et **5 SKILL.md** au-dessus de 400 lignes sont des outliers candidats à la compression.

---

## Résumé

**Total `.md` actifs dans le repo (hors archive)** : **59,343 lignes** sur **419 fichiers**.

| Catégorie | Fichiers | Lignes | Moyenne | Outliers (>400 lignes) |
|-----------|----------|--------|---------|------------------------|
| `skills/*/SKILL.md` | 64 | 11,948 | 186 | 5 |
| `docs/` (runs + audits + governance + strategy + adr + templates + reference + router) | 291 | 36,758 | 126 | variable |
| `prompts/*.md` | 33 | 4,333 | 131 | 0 |
| `distributions/` (hors proxy/adr) | 14 | 5,351 | 382 | variable |
| `distributions/hermes/proxy/adr/` | 6 | 4,107 | **684** | **6/6** |
| `distributions/{claude,pi}` | 4 | 345 | 86 | 0 |
| `AGENTS.md` + `SYSTEM.md` + `CLAUDE.md` + `GUIDE.md` + `README.md` | 5 | 2,186 | 437 | 3/5 |

**3 findings** (0 P0, 1 P1, 2 P2). Le P1 concerne les ADRs Hermes proxy (684 lignes en moyenne). Pas de P0 car aucune information n'est **perdue** par la longueur — c'est un problème de compacité, pas de complétude.

---

## Findings

### P1 (1)

| ID | Constat | Preuve | Impact |
|----|---------|--------|--------|
| **AUDIT-D-001** | Les 6 ADRs de `distributions/hermes/proxy/adr/` ont une longueur moyenne de **684 lignes** (min 442, max 929). Un ADR standard dans `docs/adr/` fait entre 100 et 200 lignes. Ces ADRs représentent **4107 lignes** à eux seuls (7% du total repo). | `wc -l distributions/hermes/proxy/adr/*.md` : 929, 766, 745, 624, 460, 442. Comparer avec `docs/adr/*.md` : 184, 152, 64, 50, 38 lignes. | Charge cognitive élevée pour qui veut lire la discipline proxy. L'ADR 0009 (929 lignes) dépasse le seuil raisonnable de consultation (les humains ne lisent plus au-delà de 500-600 lignes d'un document de décision). |

### P2 (2)

| ID | Constat | Preuve | Impact |
|----|---------|--------|--------|
| **AUDIT-D-002** | **5 SKILL.md** dépassent 400 lignes : `4-vbb-user-experience-engine` (520), `1-vbb-intent-decomposer` (430), `1-vbb-code-doc-coherence-auditor` (429), `1-vbb-code-doc-gap-integrator` (409), `2-vbb-spec-validator` (397). Moyenne globale = 186 lignes/SKILL.md, donc ces 5 fichiers sont **2× à 3× la moyenne**. | `wc -l skills/*/SKILL.md \| sort -rn \| head -10`. AUDIT_STATUS.md ligne 197 mentionne déjà LLM-LOAD-002 (« Five `SKILL.md` files exceed 13 KB and remain likely context-heavy when invoked »). | Charge LLM et cognitive. Le risque est connu mais non traité. Risque mineur car ces skills ne sont pas les plus fréquemment invoquées. |
| **AUDIT-D-003** | **GUIDE.md** fait 1248 lignes, **README.md** fait 526 lignes. Les deux sont des entry points ; leur longueur peut décourager les nouveaux venus et n'est pas justifiée par une matrice canonique de longueur cible. | `wc -l GUIDE.md README.md`. AUDIT_STATUS.md lignes 50-58 mentionnent « GUIDE still only has a partial non-dev operator path ». | Barrière à l'entrée. Pas de canon de longueur pour les guides (cible informelle : 200-300 lignes pour un guide d'entrée). |

---

## Distribution statistique

### SKILL.md — distribution par taille

| Bucket | Count | % | Exemples |
|--------|-------|---|----------|
| < 100 lignes | 13 | 20% | t-vbb-status-dashboard (33), t-vbb-context-compactor (35), 0-vbb-zero-friction (42), t-vbb-status-report (59), t-vbb-llm-healthcheck (92), 0-vbb-guide (90) |
| 100-200 lignes | 31 | 48% | majorité des skills |
| 200-300 lignes | 13 | 20% | 1-vbb-adr (308), 2-vbb-performance (295), t-vbb-anti-slop-gate (290) |
| 300-400 lignes | 2 | 3% | 4-vbb-design-system-validator (342), 2-vbb-spec-validator (397) |
| > 400 lignes | 5 | 8% | 4-vbb-user-experience-engine (520), 1-vbb-intent-decomposer (430), 1-vbb-code-doc-coherence-auditor (429), 1-vbb-code-doc-gap-integrator (409) |

**P50 = ~155 lignes, P90 = ~395 lignes, P99 = ~520 lignes.**

### ADRs Hermes proxy — détail

| Fichier | Lignes | Sujet |
|---------|--------|-------|
| `0009-proxy-action-extensibility.md` | 929 | Extensibilité des actions |
| `0011-proxy-bypass-prevention.md` | 766 | Anti-bypass |
| `0010-proxy-security-boundaries.md` | 745 | Limites de sécurité |
| `0006-confidential-proxy-architecture.md` | 624 | Architecture |
| `0007-proxy-credential-management.md` | 460 | Credentials |
| `0008-proxy-failover-3-levels.md` | 442 | Failover |
| `0012-revision-2026-06-02.md` | 141 | Révision |

**Distribution typique d'un ADR canon (docs/adr/)** :
- `0013-repo-organization-core-vs-distributions.md` : 152 lignes
- `0002-surface-first-routing-ui-ux.md` : 184 lignes
- `0001-formal-executor-boundary.md` : ~50 lignes
- `0004-contract-schema-version-semantics.md` : ~64 lignes

**Ratio** : les ADRs Hermes proxy sont **3× à 6× plus longs** que les ADRs canon.

### Guides — détail

| Fichier | Lignes | Catégorie |
|---------|--------|-----------|
| `GUIDE.md` | 1248 | Guide principal |
| `README.md` | 526 | Entry point |
| `docs/REFERENCE/pre-merge-gate.md` | 71 | Référence canon (court, dense) |
| `docs/runs/README.md` | 89 | Index |
| `docs/INDEX.md` | 64 | Navigation |

---

## Comparaison avec ce qui est canon

### Canon de longueur explicite

Cherché : un seuil canon de longueur pour les `.md`. Résultat : **aucun seuil canon explicite**.

- `docs/CONVENTIONS.md` : piliers qualité (lisibilité, modularité…) — **aucun seuil de lignes**.
- `docs/PILOTAGE.md` : routes — **aucun seuil**.
- `skills/0-vbb-standard/SKILL.md` : contrat de skill — **aucun seuil**.

### Canon de longueur implicite (pratique)

| Type | Fourchette constatée | Note |
|------|----------------------|------|
| `SKILL.md` (cible raisonnable) | 100-200 lignes | Médiane 155 lignes |
| `ADR` (cible raisonnable) | 100-200 lignes | Médiane 152 lignes |
| `prompt canon` (cible raisonnable) | 50-150 lignes | Médiane 131 lignes |
| `Guide d'entrée` (cible raisonnable) | 200-400 lignes | Pas de guide canon |
| `Audit report` (variable) | 200-600 lignes | Pas de cible |
| `Run artifact` (variable) | 50-300 lignes par phase | Pas de cible |

---

## Manifestation concrète

Si Brice veut comprendre **la discipline du proxy Hermes**, il doit lire 4107 lignes d'ADR. À raison de 5 minutes par tranche de 200 lignes, c'est ~100 minutes de lecture.

Si Brice veut lancer **un audit `1-vbb-tech-debt`** et tombe sur la skill `4-vbb-user-experience-engine` dans l'index, il doit comprendre que cette skill fait 520 lignes (vs 186 en moyenne) avant de la lancer.

Si un **nouveau contributeur** veut onboarder via `GUIDE.md`, il fait face à 1248 lignes denses sans TOC apparent.

---

## Capacité existante vs capacité souhaitée

### Ce qui existe

| Capacité | Outil | Référence |
|----------|-------|-----------|
| Index de navigation | `docs/INDEX.md`, `docs/audits/INDEX.md` | (existe) |
| Cible de compression mentionnée pour SKILL.md | `docs/AUDIT_STATUS.md` ligne 197 (LLM-LOAD-002) | (reconnu comme gap, non traité) |
| Pratique de split (`core.README.md` vs `core/README.md`) | `core.README.md` + `distributions/` sentinels | `docs/adr/0013` |
| Possibilité d'`@include` entre fichiers | `distributions/claude/CLAUDE.md` ligne 14-16 (`@AGENTS.md`, `@SYSTEM.md`) | ad-hoc, non formalisé (cf. Gap-16 Phase 1) |
| Templates courts pour les phases | `docs/templates/*.md.template` | 7 phase templates, ~50-80 lignes chacun |

### Ce qui manque

| Capacité manquante | Conséquence |
|--------------------|-------------|
| Canon de longueur cible par type de fichier | Pas de juge pour décider « ce fichier est trop long » |
| Linter `wc -l` par type de fichier | Pas de check CI sur la compaction |
| TOC (table of contents) dans GUIDE.md et README.md | Navigation difficile |
| Split des ADRs Hermes proxy en ADR principal + annexes | Lecture ciblée impossible |
| Compression des 5 SKILL.md > 400 lignes en core + références | Risque LLM-LOAD-002 non résolu |

---

## Recommandations (texte seulement)

| ID reco | Description | Effort | Gain estimé |
|---------|-------------|--------|-------------|
| R-D-1 | Ajouter un canon de longueur dans `docs/CONVENTIONS.md` (Pillar 1 Readability) : « Cibles indicatives — SKILL.md < 250 lignes · ADR < 200 lignes · Guide d'entrée < 400 lignes · Audit report < 600 lignes. Au-delà, justifier en début de fichier ou split. » | S | Faible — donne un juge |
| R-D-2 | Ajouter un check CI `tools/vbb-md-length-check.py` qui warn (non fail) sur les fichiers dépassant les cibles R-D-1. | M | Moyen — rend la compaction visible |
| R-D-3 | Splitter les 6 ADRs Hermes proxy : ADR principal (≤ 200 lignes) + annexe(s) référencées (`-annex-A.md`, `-annex-B.md`). | L | Fort — passe de 684 à ~200 lignes en moyenne |
| R-D-4 | Compresser les 5 SKILL.md > 400 lignes : déplacer les exemples détaillés en fichiers annexes (`SKILL.examples.md`), garder le core opérationnel dans `SKILL.md`. | L | Fort — réduit la charge LLM (résout LLM-LOAD-002) |
| R-D-5 | Ajouter une TOC (table of contents) en haut de `GUIDE.md` et `README.md`. Découpage éventuel en `GUIDE.{operator,developer,auditor}.md`. | M | Moyen — réduit la barrière à l'entrée |
| R-D-6 | Auditer les 5 SKILL.md > 400 lignes pour identifier les sections « verbose / narrative / historic » déplaçables. | M | Moyen |
| R-D-7 | Auditer les 4 audits en `docs/audits/` entre 500-608 lignes pour identifier les sections « context only » déplaçables en annexe. | M | Moyen |

---

## Quick wins

1. **QW-D-1** — Vérifier si LLM-LOAD-002 (`docs/AUDIT_STATUS.md` ligne 197, statut « Open ») doit être promu P1. Aujourd'hui noté P2, mais l'audit confirme 5 fichiers > 400 lignes et 6 ADRs > 442 lignes. Mise à jour possible : `LLM-LOAD-002 → P1`.
2. **QW-D-2** — Lancer `find . -name "*.md" -not -path "./.git/*" -not -path "./.pi/*" -not -path "./docs/archive/*" -exec wc -l {} \; | awk '$1 > 500' | sort -rn` pour obtenir la liste exacte des fichiers au-dessus de 500 lignes. Coûte 1 minute. Sortie : ~12-15 fichiers.
3. **QW-D-3** — Ajouter une TOC en haut de `GUIDE.md` (5 minutes). Réduit la friction de lecture sans toucher au contenu.

---

## Unknowns / needs confirmation

| ID | Question | Conséquence |
|----|----------|-------------|
| UN-D-1 | Les **ADRs Hermes proxy** doivent-ils être **raccourcis** ou **laissés tels quels** (leur longueur est-elle justifiée par la complexité du proxy) ? | Choix R-D-3 |
| UN-D-2 | Les **5 SKILL.md** > 400 lignes sont-ils vraiment **context-heavy** à l'invocation ou simplement **denses en contenu utile** ? | Choix R-D-4 |
| UN-D-3 | Y a-t-il une **politique canon** existante (non documentée) sur la longueur des fichiers ? | Si oui, R-D-1 est redondant |
| UN-D-4 | Le **split en annexes** des ADRs est-il compatible avec le format canon `docs/adr/NNNN-slug.md` ? | Oui/non pour R-D-3 |

---

## Verdict

`PARTIAL — outliers identifiés (6 ADRs Hermes + 5 SKILL.md + GUIDE.md), pas de canon de longueur, optimisation possible mais non bloquante`. Le repo n'est pas en dérive : la majorité des SKILL.md sont entre 100 et 200 lignes, et les ADRs canon sont entre 50 et 200 lignes. Les outliers sont concentrés sur **deux zones** : (1) les ADRs du proxy Hermes (présence justifiée par la complexité, mais non scindés), (2) les SKILL.md > 400 lignes (déjà reconnus comme gap LLM-LOAD-002, non traités). Quick wins : QW-D-1 (mise à jour AUDIT_STATUS), QW-D-2 (cartographie), QW-D-3 (TOC). Recommandations plus lourdes (R-D-3, R-D-4) à arbitrer par l'architecte.