---
context_role: dependencies
phase: strategy
status: active
updated: 2026-07-12
scope: vibebackbone framework → multi-service patterns
phase_phase_label: "Phase 1 — Caractérisation des manques (pas de solution)"
---

# 03 — Dépendances : graphe « ce gap doit être traité avant cet autre »

> **Périmètre** : graphe de dépendances entre les 18 gaps identifiés. Chaque arête « A → B » signifie « A doit être traité avant B » (ou « au minimum en parallèle »). Le graphe est lu en **forward** : on commence par les sources, on termine par les sinks.
>
> **Sources** : `01_GAP_ANALYSIS.md` (caractérisation) + `02_PRIORITIES.md` (classification).

---

## 0. Vue d'ensemble — trois clusters de dépendances

```
                              ┌─────────────────────────────┐
                              │   CLUSTER FONDATIONS        │
                              │   (peu de dépendances)      │
                              │                             │
                              │   Gap-01 (orientation DB)   │
                              │   Gap-02 (archétype)        │
                              │   Gap-05 (CONTRACTS_CONSUMED)│
                              │   Gap-08 (multi-repo)       │
                              │   Gap-09 (mécanisme ext.)   │
                              └──────────────┬──────────────┘
                                             │
        ┌────────────────────────────────────┼────────────────────────────────────┐
        │                                    │                                    │
        ▼                                    ▼                                    ▼
┌────────────────────┐         ┌────────────────────────┐         ┌────────────────────────┐
│ CLUSTER DISCIPLINE │         │ CLUSTER OUTILLAGE      │         │ CLUSTER TYPAGE         │
│ (chemin critique)  │         │ (linter + graphes)     │         │ (linters contextuels)  │
│                    │         │                        │         │                        │
│ Gap-10 (consumers) │◄────────│ Gap-04 (lint cross)    │         │ Gap-11 (lint arch.)    │
│ Gap-06 (IMPACT_LOG)│         │ Gap-13 (graphe global) │         │ Gap-12 (pilier DB)     │
└────────┬───────────┘         └────────────┬───────────┘         └────────────┬───────────┘
         │                                  │                                  │
         └──────────────┬───────────────────┴──────────────────────────────────┘
                        ▼
              ┌────────────────────┐
              │   CLUSTER GATES    │
              │   (enforcement)    │
              │                    │
              │   Gap-15 (CI PR)   │
              │   Gap-07 (co-év.)  │
              └─────────┬──────────┘
                        │
                        ▼
              ┌────────────────────┐
              │   CLUSTER CODEGEN  │
              │   (génération)     │
              │                    │
              │   Gap-03 (AGENTS)  │
              └─────────┬──────────┘
                        │
                        ▼
              ┌────────────────────┐
              │   CLUSTER POLISH   │
              │   (P2)             │
              │                    │
              │   Gap-16 (@incl.)  │
              │   Gap-17 (anti-drift)│
              │   Gap-18 (snap→log)│
              └────────────────────┘
```

---

## 1. Liste exhaustive des arêtes (format texte)

Notation : **A → B** signifie « A doit précéder B (ou au moins le rejoindre) ».

### 1.1 Arêtes du Cluster Fondations

- **Gap-01 → Gap-14** (orientation DB → CONTEXT enrichi) — sans orientation, le schéma enrichi n'a pas de sens.
- **Gap-02 → Gap-14** (archétype → CONTEXT enrichi) — idem.
- **Gap-02 → Gap-11** (archétype → lint archetype-aware) — sans archétype, le lint ne peut pas être contextuel.

### 1.2 Arêtes du Cluster Discipline (chemin critique)

- **Gap-05 → Gap-04** (CONTRACTS_CONSUMED → linter cross-service) — le linter valide la cohérence de CONTRACTS_CONSUMED.
- **Gap-05 → Gap-06** (CONTRACTS_CONSUMED → IMPACT_LOG) — l'IMPACT_LOG référence les consommateurs documentés.
- **Gap-05 → Gap-10** (CONTRACTS_CONSUMED → taxonomie consumer) — la taxonomie relie producteur et CONTRACTS_CONSUMED côté consommateur.
- **Gap-05 → Gap-13** (CONTRACTS_CONSUMED → graphe inter-services) — le graphe est construit depuis CONTRACTS_CONSUMED.
- **Gap-06 → Gap-04** (IMPACT_LOG → linter) — le linter vérifie que les modifications de contrat ont mis à jour l'IMPACT_LOG.
- **Gap-06 → Gap-07** (IMPACT_LOG → co-évolution outillée) — la co-évolution peuple l'IMPACT_LOG.
- **Gap-06 → Gap-18** (IMPACT_LOG → articulation snapshot↔log) — l'articulation est l'interface entre l'existant et le nouveau log.
- **Gap-10 → Gap-04** (taxonomie consumer → linter) — le linter utilise la taxonomie pour valider.
- **Gap-10 → Gap-11** (taxonomie consumer → lint archetype-aware) — l'archétype-aware lint vérifie la cohérence consumer.
- **Gap-10 → Gap-13** (taxonomie consumer → graphe) — le graphe annoté producer×consumer.

### 1.3 Arêtes du Cluster Outillage

- **Gap-04 → Gap-15** (linter → gate CI) — le gate applique le linter en CI.
- **Gap-08 → Gap-13** (multi-repo → graphe global) — le graphe global agrège plusieurs repos.

### 1.4 Arêtes du Cluster Typage

- **Gap-09 → Gap-03** (mécanisme d'extension → codegen AGENTS) — le codegen utilise le mécanisme d'extension pour les templates.
- **Gap-09 → Gap-12** (mécanisme d'extension → pilier DB) — le pilier DB est la première extension concrète.
- **Gap-12 → Gap-09** (pilier DB → mécanisme d'extension) — ⚠️ **cycle** : Gap-12 est une extension, mais sa formalisation peut elle-même justifier le besoin du mécanisme Gap-09. Voir §3.

### 1.5 Arêtes du Cluster Gates

- **Gap-07 → Gap-15** (co-évolution → gate CI) — la co-évolution est enforced en CI.
- **Gap-15 → Gap-04** (gate CI → linter) — ⚠️ **cycle** : Gap-15 applique Gap-04, mais Gap-15 ne peut pas exister sans Gap-04. Cycle résolu par co-construction (voir §3).

### 1.6 Arêtes du Cluster Codegen

- **Gap-03 → Gap-16** (codegen AGENTS → @include formalisé) — le codegen produit des fichiers avec @include.
- **Gap-03 → Gap-17** (codegen AGENTS → anti-drift) — le codegen est la source des fichiers « @generated ».

---

## 2. Graphe acyclique projeté (DAG)

Pour éliminer les cycles de §1.4 et §1.5, on « déplie » les cycles en supposant co-construction :

```
RACINES (peuvent démarrer en parallèle)
├── Gap-01  (orientation DB)
├── Gap-02  (archétype)
├── Gap-05  (CONTRACTS_CONSUMED)
├── Gap-08  (multi-repo)
└── Gap-09  (mécanisme d'extension)

NIVEAU 1
├── Gap-14  (CONTEXT enrichi)        ← Gap-01, Gap-02
├── Gap-10  (taxonomie consumer)     ← Gap-05
├── Gap-06  (IMPACT_LOG)             ← Gap-05
└── Gap-12  (pilier DB)              ← Gap-09, Gap-01

NIVEAU 2
├── Gap-11  (lint archetype-aware)   ← Gap-02, Gap-10
├── Gap-04  (linter cross-service)   ← Gap-05, Gap-06, Gap-10
└── Gap-13  (graphe inter-services)  ← Gap-05, Gap-08, Gap-10

NIVEAU 3
├── Gap-07  (co-évolution outillée)  ← Gap-06
└── Gap-15  (gate CI PR)             ← Gap-04

NIVEAU 4
├── Gap-03  (codegen AGENTS)         ← Gap-01, Gap-02, Gap-09
└── Gap-18  (snapshot → log)         ← Gap-06

NIVEAU 5 (P2, polish)
├── Gap-16  (@include formalisé)     ← Gap-03
└── Gap-17  (anti-drift fichiers générés) ← Gap-03
```

---

## 3. Cycles identifiés et résolution

| Cycle | Gaps impliqués | Nature du cycle | Résolution |
|-------|----------------|-----------------|------------|
| Cycle 1 | Gap-09 ↔ Gap-12 | Le pilier DB est une extension, mais sa formalisation peut justifier le besoin d'extensions formelles. | **Co-construction** : Gap-09 (mécanisme) et Gap-12 (premier cas d'usage) sont conçus ensemble en Phase 2. Pas de précédence stricte. |
| Cycle 2 | Gap-04 ↔ Gap-15 | Le gate applique le linter, mais le linter n'a de valeur qu'enforcementé en CI. | **Co-construction** : Gap-04 et Gap-15 sont implémentés ensemble, le gate et le linter partagent le même squelette de configuration. |

**Note** : aucun cycle n'est bloquant pour la Phase 2. Les deux cycles sont des dépendances « soft » où les solutions se renforcent mutuellement.

---

## 4. Chemins critiques

### 4.1 Chemin critique principal (P0 → discipline)

```
Gap-05 → Gap-10 → Gap-04 → Gap-15
                ↘        ↗
                 Gap-06
```

**Lecture** : pour qu'un service soit « discipline-enforced » en CI, il faut :
1. CONTRACTS_CONSUMED existe et est peuplé (Gap-05).
2. La taxonomie producer×consumer est définie (Gap-10).
3. L'IMPACT_LOG est maintenu (Gap-06).
4. Le linter valide la cohérence (Gap-04).
5. La CI bloque les régressions (Gap-15).

**Profondeur critique** : 5 niveaux. C'est le chemin le plus long.

### 4.2 Chemin critique secondaire (P0 → multi-repo)

```
Gap-08 → Gap-13
```

**Lecture** : pour qu'un graphe inter-services existe, il faut d'abord le support multi-repo. Plus court (2 niveaux) mais Gap-08 est **non trivial** (touche plusieurs outils existants).

### 4.3 Chemin tertiaire (P1 → typage)

```
Gap-01 → Gap-14
Gap-02 → Gap-14
```

**Lecture** : pour enrichir le CONTEXT, il faut d'abord définir les champs (orientation + archétype). Court (2 niveaux).

---

## 5. Gaps « parallel-safe » (peuvent être traités simultanément)

- Gap-01, Gap-02 : indépendants, sources du Cluster Fondations.
- Gap-08, Gap-09 : indépendants, sources du Cluster Fondations.
- Gap-16, Gap-17, Gap-18 : indépendants entre eux (P2).

---

## 6. Estimation du chemin critique

| Phase | Gaps | Dépendances internes | Estimation (à valider) |
|-------|------|----------------------|------------------------|
| Fondations | Gap-01, Gap-02, Gap-05, Gap-08, Gap-09 | quasi-indépendantes | 5 jours ouvrés |
| Discipline | Gap-10, Gap-06, Gap-11, Gap-04, Gap-15 | chaîne 5 niveaux | 8 jours ouvrés |
| Outillage | Gap-13 | Gap-08 + Gap-05 | 3 jours ouvrés |
| Typage | Gap-14, Gap-12 | Gap-01, Gap-02, Gap-09 | 3 jours ouvrés |
| Codegen & co-évolution | Gap-03, Gap-07, Gap-18 | Gap-09, Gap-06 | 5 jours ouvrés |
| Polish (P2) | Gap-16, Gap-17 | Gap-03 | 2 jours ouvrés |
| **TOTAL** | **18** | — | **~26 jours ouvrés** |

(Estimation grossière. Phase 2 pourra recalibrer après prototypage des 3 fondations.)

---

## 7. Liens

- [`01_GAP_ANALYSIS.md`](01_GAP_ANALYSIS.md)
- [`02_PRIORITIES.md`](02_PRIORITIES.md)
- [`04_OUT_OF_SCOPE.md`](04_OUT_OF_SCOPE.md)
- [`SESSION.md`](SESSION.md)
