---
run_id: "2026-07-12_1210_audit-A-scope-aware-janitor"
phase: "02_AUDIT"
voie: "AUDIT"
status: "PARTIAL"
agent: "claude-code"
started_at: "2026-07-12T12:10:00Z"
ended_at: "2026-07-12T12:35:00Z"
next_phase: null
artifacts_consumed:
  - "skills/1-vbb-code-janitor/SKILL.md"
  - "skills/1-vbb-tech-debt/SKILL.md"
  - "skills/1-vbb-monolith-detector/SKILL.md"
  - "skills/t-vbb-dependency-mapper/SKILL.md"
  - "tools/vbb-architecture.py"
  - "docs/ARCHITECTURE.md"
  - "docs/TECH_DEBT.md"
  - "docs/audits/tech-debt-20260610-tech-debt-audit.md"
artifacts_produced:
  - "docs/audits/audit-A-scope-aware-janitor-20260712-1210.md"
---

# Audit A — Scope-aware janitor / tech-debt (audit des compétences)

**Date** : 2026-07-12
**Périmètre** : compétences `1-vbb-code-janitor`, `1-vbb-tech-debt`, et outils complémentaires (monolith-detector, dependency-mapper, architecture-source).
**Question auditée** : les audits janitor / tech-debt supportent-ils une analyse **scope par scope** (par exemple : un business scope `proxy`, un business scope `architecture-source`, un business scope `distributions` ; plus généralement, des sous-ensembles du repo délimités par un périmètre métier ou technique) avec à la fois une option globale et une option par scope ? Et permettent-ils d'extraire au préalable les **dépendances hors repo** (liens entre différentes bases de données, services externes, etc.) ?
**Verdict** : `PARTIAL` — des fondations existent (ARCHITECTURE.md, type `external`, dependency-mapper), mais **aucun mécanisme** ne ferme la boucle « extraction dépendances hors repo + extraction scopes métier → janitor/tech-debt scopés ».

---

## Résumé

Les compétences `1-vbb-code-janitor` et `1-vbb-tech-debt` produisent **un seul rapport Markdown** pour l'ensemble du repo (`code-janitor-{YYYYMMDD-HHMM}.md` et `tech-debt-{YYYYMMDD-HHMM}.md`). Elles ne supportent ni paramètre `--scope` ni paramètre `--include-external`. Elles ne savent pas distinguer « dette technique du bloc architecture-source » de « dette technique du bloc distributions/hermes/proxy ». Conséquence : un rapport tech-debt sur vibebackbone lui-même mélange des findings de natures très différentes (scripts shell, code Python, gouvernance Markdown, ADRs, contrats), ce qui nuit à l'actionnabilité.

**4 findings** (0 P0, 2 P1, 2 P2). Le **Gap P1-A1** (absence de scope-by-scope) est le blocage principal pour un audit actionnable sur les distributions (Hermes) ou sur les blocs ARCHITECTURE futurs.

---

## Findings

### P1 (2)

| ID | Constat | Zone | Preuve |
|----|---------|------|--------|
| **AUDIT-A-001** | `1-vbb-code-janitor` ne supporte pas de notion de **scope** (ni paramètre CLI, ni champ dans le rapport). Toutes les findings sont regroupées en un seul rapport pour le repo entier. | `skills/1-vbb-code-janitor/SKILL.md` lignes 33-50 (Input Contract), 60-68 (Scope), 99-101 (Output Contract : "ONE Markdown report"). Aucune mention de `--scope`, de `bounded_context`, de `subdomain`, de `module`. | SKILL.md ligne 99-101 |
| **AUDIT-A-002** | `1-vbb-tech-debt` ne supporte pas non plus de notion de **scope**. Le rapport mélange Legacy residue + Architecture + DB + API + Frontend + Test + Ops sans les rattacher à un périmètre opérationnel ou métier. Sur un repo à N blocs, c'est illisible. | `skills/1-vbb-tech-debt/SKILL.md` lignes 56-69 (Audit dimensions), 99-101 (Output Contract : "ONE Markdown report"). Idem : zéro hit `scope`, `business`, `bounded`, `subdomain`, `module`. | SKILL.md ligne 99-101 |

### P2 (2)

| ID | Constat | Zone | Preuve |
|----|---------|------|--------|
| **AUDIT-A-003** | Le type `external` existe dans `VALID_TYPES` (architecture) mais n'a aucune ligne dédiée dans `docs/ARCHITECTURE.md` (vérifié : zéro bloc `## Bloc: External` ou similaire). Conséquence : aucun bloc ARCHITECTURE ne déclare formellement une dépendance hors-repo. | `tools/vbb-architecture.py` ligne 83 (VALID_TYPES contient "external"). `docs/ARCHITECTURE.md` : 7 blocs, aucun ne porte `type: external`. | tools/vbb-architecture.py:83 + ARCHITECTURE.md |
| **AUDIT-A-004** | `t-vbb-dependency-mapper` mentionne "inter-repo dependencies if visible" mais **ne fournit pas** de mécanisme pour les **déclarer** activement. La ligne 60-65 ("inter-repo dependencies if visible") est conditionnelle. | `skills/t-vbb-dependency-mapper/SKILL.md` ligne 60-65. Aucune directive pour construire ou maintenir un registre de dépendances hors-repo. | SKILL.md:60-65 |

---

## Zones analysées

| Zone | Statut | Notes |
|------|--------|-------|
| `1-vbb-code-janitor` SKILL.md | ✅ Analysé en entier | Pas de scope ; rapport unique ; pas d'option `--external` |
| `1-vbb-tech-debt` SKILL.md | ✅ Analysé en entier | Pas de scope ; rapport unique ; pas de notion de sous-domaine |
| `1-vbb-monolith-detector` SKILL.md | ✅ Analysé (lignes 1-100) | Heuristiques H1-H7 sur **fichiers**, pas sur scopes. Peut être limité à un sous-arbre via glob, mais pas via scope sémantique. |
| `t-vbb-dependency-mapper` SKILL.md | ✅ Analysé en entier | Mentionne `inter-repo` mais ne le rend pas first-class |
| `tools/vbb-architecture.py` | ✅ Analysé (lignes 1-200) | Type `external` existe (ligne 83) mais aucun bloc ne l'utilise |
| `docs/ARCHITECTURE.md` | ✅ Analysé en entier | 7 blocs, 0 `type: external`, 0 champ `scope` |
| `docs/TECH_DEBT.md` | ✅ Analysé en entier | Registre ; pas de groupement par scope |
| Audit existant : `tech-debt-20260610-tech-debt-audit.md` | ✅ Analysé (lignes 1-80) | Liste findings par "Zone" (setup.sh, skills/, etc.) — groupement par **emplacement** mais pas par **scope métier** |

---

## Capacité existante vs capacité souhaitée

### Ce qui existe

| Capacité | Outil | Référence |
|----------|-------|-----------|
| Lister les blocs ARCHITECTURE avec `type: external` (mais aucun bloc ne le fait) | `tools/vbb-architecture.py` | ligne 83 |
| Distinguer intra-repo / inter-service dans la cartographie | `t-vbb-dependency-mapper` | SKILL.md ligne 60-65 |
| Grouper les findings tech-debt par **zone** (emplacement dans le repo) | `1-vbb-tech-debt` | pratique de l'audit 2026-06-10 |
| Isoler un sous-arbre du repo via `glob` ou `monolith-detector` | `1-vbb-monolith-detector` | heuristique H1 |
| Avoir un registre de dette technique indexé | `docs/TECH_DEBT.md` | (existe) |

### Ce qui manque

| Capacité manquante | Pourquoi c'est bloquant |
|--------------------|--------------------------|
| **Déclarer** les dépendances hors-repo (lien cross-DB, services externes) dans `docs/ARCHITECTURE.md` via des blocs dédiés `type: external` | Sans déclaration, l'audit ne peut pas savoir quelles dépendances existent hors repo |
| **Déclarer** des scopes métier dans `docs/ARCHITECTURE.md` (ex : `scope: proxy`, `scope: distributions`, `scope: governance`) | Sans scope, l'audit ne peut pas grouper par périmètre métier |
| **Paramétrer** `1-vbb-code-janitor` et `1-vbb-tech-debt` avec `--scope <name>` pour produire un rapport scopé | Sans paramètre, l'audit est global-only |
| **Paramétrer** `--include-external` ou `--exclude-external` pour traiter ou non les blocs externes | Sans option, l'audit inclut par défaut tout le scope du repo |
| **Sortie** : rapport scopé qui produit un fichier `tech-debt-{scope}-{date}.md` distinct | Sans fichier distinct, on ne peut pas comparer les scopes entre eux |

---

## Manifestation concrète

Si Brice demande aujourd'hui « fais-moi un janitor sur **uniquement** le bloc `distributions/hermes/proxy/` » :
1. Aucune option native. Le janitor va scanner tout le repo.
2. Même si on lance le janitor depuis `distributions/hermes/proxy/`, le skill n'a pas de notion de scope.
3. Le rapport va inclure des findings sur `setup.sh`, `docs/CONTEXT.md`, etc. — non pertinents pour le périmètre demandé.

Même chose pour « fais-moi un tech-debt sur **uniquement** la dette DB cross-service » :
1. Impossible : la skill tech-debt ne sait pas ce qu'est une « dette DB cross-service » sans scope sémantique.

---

## Recommandations (texte seulement — pas d'implémentation dans cet audit)

| ID reco | Description | Effort | Pré-requis |
|---------|-------------|--------|-----------|
| R-A-1 | Ajouter un champ optionnel `scope` aux blocs `## Bloc:` de `docs/ARCHITECTURE.md` (ex : `scope: proxy`, `scope: distributions`, `scope: governance`). Le bloc devient adressable par scope. | S | Aucun |
| R-A-2 | Ajouter un type `external` aux blocs ARCHITECTURE pour les dépendances hors-repo. Prévoir un sous-champ `external.kind: database | api | filesystem | service | third-party`. | S | R-A-1 |
| R-A-3 | Étendre `1-vbb-code-janitor` avec un paramètre `--scope <name>` (optionnel). Si fourni, ne scanner que les fichiers sous `files:` des blocs portant ce scope. Sortie : `code-janitor-{scope}-{date}.md`. | M | R-A-1 |
| R-A-4 | Étendre `1-vbb-tech-debt` avec `--scope <name>` et `--include-external` (bool). Sortie : `tech-debt-{scope}-{date}.md`. | M | R-A-1, R-A-2 |
| R-A-5 | Étendre `vbb-architecture.py lint` pour valider que tout bloc `type: external` a un sous-champ `external.kind` et `external.target` (URL ou nom canonique). | S | R-A-2 |
| R-A-6 | Mettre à jour `t-vbb-dependency-mapper` pour **produire** un inventaire des dépendances hors-repo (pas seulement les rendre visibles si elles existent déjà). | M | R-A-2 |

---

## Liens avec l'évolution en cours

Ce audit est complémentaire à `docs/strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md` :

| Gap Phase 1 | Lien |
|--------------|------|
| Gap-13 (graphe inter-services indépendant) | AUDIT-A-001/A-002 sont les prérequis : sans scopes, pas de graphe agrégé actionnable |
| Gap-05 (CONTRACTS_CONSUMED canonique) | AUDIT-A-003 est un précédent : si on ne déclare pas les externals, on ne déclarera pas les contrats consommés |
| Gap-09 (mécanisme d'extension) | AUDIT-A-001/A-002 peuvent être résolus **comme extensions** (paramètre optionnel), pas comme canon change |

---

## Quick wins

1. **QW-A-1** — Créer un premier bloc `## Bloc: External Dependencies` dans `docs/ARCHITECTURE.md` avec un ou deux `external.kind: database` à titre d'exemple. Coûte 5 minutes, démontre la capacité. Pré-requis à R-A-2.
2. **QW-A-2** — Lancer `1-vbb-tech-debt` aujourd'hui sur **uniquement** `distributions/hermes/proxy/` (avec l'option "scope by directory" actuelle = `glob`) et noter le temps d'analyse / bruit généré. Mesure de la friction actuelle.
3. **QW-A-3** — Documenter dans `docs/TECH_DEBT.md` une **section "Scopes connus"** listant les scopes métier que Brice souhaite voir distingués (proxy, distributions, governance, tools, ...). Prépare R-A-1.

---

## Unknowns / needs confirmation

| ID | Question | Conséquence si non-répondu |
|----|----------|----------------------------|
| UN-A-1 | Quels **scopes métier** Brice veut-il voir distingués ? (proposition : `governance`, `distribution`, `tools`, `tests`, `docs`, `skills`, `prompts` — mais à confirmer) | Recommandations R-A-1..R-A-6 à re-prioriser |
| UN-A-2 | Brice veut-il un mécanisme `--scope` (paramètre CLI) ou un fichier de configuration `docs/SCOPES.yaml` (déclaratif) ? | Choix d'implémentation |
| UN-A-3 | Les "dépendances hors repo" sont-elles uniquement des DB ou aussi des API externes / services tiers / filesystems ? | Forme du champ `external.kind` |
| UN-A-4 | Le scope doit-il être **par projet** (un seul projet) ou **multi-projet** (plusieurs projets vibebackbone-compatible dans un workspace) ? | Toucherait ADR 0013 (Core vs Distribution) et Gap-08 (multi-repo) |

---

## Verdict

`PARTIAL — besoin réel confirmé, capacité partielle, plan d'évolution clair mais non implémenté`.

- **P1 immédiat** : AUDIT-A-001 / AUDIT-A-002 (absence de scope-by-scope).
- **P2 préparation** : AUDIT-A-003 / AUDIT-A-004 (extraction dépendances hors-repo).
- **Quick wins** : QW-A-1 / QW-A-2 / QW-A-3 pour démontrer la capacité avant tout ADR.
- **Dépendances** : couplage avec `vbb-evolution-multi-service-support` Phase 2 (Gap-09 extension + Gap-13 graphe inter-services).