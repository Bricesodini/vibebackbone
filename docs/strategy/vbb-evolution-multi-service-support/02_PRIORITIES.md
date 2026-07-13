---
context_role: priorities
phase: strategy
status: active
updated: 2026-07-12
scope: vibebackbone framework → multi-service patterns
phase_phase_label: "Phase 1 — Caractérisation des manques (pas de solution)"
---

# 02 — Priorités : vibebackbone vers support natif des patterns multi-services

> **Périmètre** : ce document classe les 18 gaps identifiés en `01_GAP_ANALYSIS.md` selon trois niveaux (P0/P1/P2), identifie les chemins critiques, et propose une séquence de traitement pour la Phase 2 (proposition de solutions).
>
> **Règle de classification** : P0 = sans lequel le pattern multi-service n'est pas viable · P1 = important mais contournable · P2 = nice-to-have. En cas de doute → P1 par défaut (consigne §8).

---

## 0. Synthèse — classification finale

| Niveau | Gaps | Justification |
|--------|------|---------------|
| **P0 — bloquant** | Gap-04, Gap-05, Gap-06, Gap-08, Gap-10, Gap-13, Gap-15 | Discipline outillée cross-service + multi-repo. Sans ces mécanismes, le pattern database-per-service est non-vérifiable. |
| **P1 — important** | Gap-01, Gap-02, Gap-03, Gap-07, Gap-09, Gap-11, Gap-12, Gap-14 | Typage projet + codegen + co-évolution. Nécessaires pour que le pattern soit utilisable à l'échelle, mais contournables par convention humaine sur un système à 2-3 services. |
| **P2 — nice-to-have** | Gap-16, Gap-17, Gap-18 | Mécanismes transverses (@include, anti-drift, snapshot→log). Améliorations utiles mais non-bloquantes. |

**Total** : 7 P0 + 8 P1 + 3 P2 = **18 gaps** ✓ (cohérent avec §5 de `01_GAP_ANALYSIS.md`).

---

## 1. P0 — Bloquants (chemin critique)

### 1.1 Sous-ensemble disciplinaire (5 gaps interdépendants)

| Gap | Titre | Dépend de | Bloque |
|-----|-------|-----------|--------|
| **Gap-05** | CONTRACTS_CONSUMED canonique | — | Gap-04, Gap-10, Gap-13, Gap-15 |
| **Gap-10** | Taxonomie contrats cross-service | Gap-05 | Gap-04, Gap-11, Gap-13 |
| **Gap-06** | IMPACT_LOG cumulatif | Gap-05 | Gap-04, Gap-07, Gap-15 |
| **Gap-04** | Linter discipline multi-service | Gap-05, Gap-06, Gap-10 | Gap-15 |
| **Gap-15** | Gate « ne pas régresser » en CI | Gap-04 | (rien — c'est le point d'application) |

**Lecture** : ce sous-ensemble forme le tiercé disciplinaire (Gap-05, Gap-06, Gap-10) qui alimente le linter (Gap-04), lequel est enforced en CI (Gap-15). C'est le **noyau dur** de la discipline multi-service.

### 1.2 Sous-ensemble multi-repo (2 gaps interdépendants)

| Gap | Titre | Dépend de | Bloque |
|-----|-------|-----------|--------|
| **Gap-08** | Support multi-repo | — | Gap-13 |
| **Gap-13** | Graphe inter-services indépendant | Gap-05, Gap-08 | (visualisation / compréhension globale) |

**Lecture** : Gap-08 et Gap-13 sont les deux gaps qui rendent le framework viable au-delà d'un seul repo.

### 1.3 Pourquoi P0 (et pas P1) ?

| Gap | Argument pour P0 |
|-----|-------------------|
| Gap-05 | Sans tracking des contrats consommés, il est **impossible** de savoir qui dépend de quoi. Toute la discipline s'effondre. |
| Gap-06 | Sans log cumulatif, la discipline de co-évolution n'a pas de mémoire. On ne peut pas répondre à « cet impact a-t-il été migré ? ». |
| Gap-04 | Sans linter, les 2 gaps précédents sont des intentions, pas des contraintes. |
| Gap-15 | Sans gate CI, le linter n'est pas exécuté systématiquement. |
| Gap-10 | Sans taxonomie consumer, Gap-04 ne peut pas savoir quels contrats sont cross-service. |
| Gap-08 | Sans multi-repo, le pattern database-per-service inter-repos est hors framework. |
| Gap-13 | Sans graphe agrégé, la coordination multi-services est artisanale. |

---

## 2. P1 — Important (chemin de soutien)

### 2.1 Sous-ensemble typage projet (3 gaps)

| Gap | Titre | Dépend de | Bloqué par |
|-----|-------|-----------|-----------|
| **Gap-01** | Orientation DB structurée | — | — |
| **Gap-02** | Project archetype | — | — |
| **Gap-14** | CONTEXT.md / PROJECT_MODE.md enrichi | Gap-01, Gap-02 | — |

**Lecture** : ces 3 gaps peuvent être traités **en parallèle** des P0. Ils sont la fondation sémantique qui permet ensuite Gap-11 (lint archetype-aware) et Gap-03 (codegen AGENTS.md depuis la déclaration d'orientation).

### 2.2 Sous-ensemble codegen & extensions (3 gaps)

| Gap | Titre | Dépend de |
|-----|-------|-----------|
| **Gap-03** | Codegen AGENTS.md / CLAUDE.md | Gap-01, Gap-02, Gap-09 |
| **Gap-09** | Mécanisme d'extension | — |
| **Gap-12** | Pilier « DB owned by service » | Gap-09, Gap-01 |

**Lecture** : Gap-09 est la fondation. Gap-03 et Gap-12 consomment ce mécanisme.

### 2.3 Sous-ensemble discipline co-évolution (2 gaps)

| Gap | Titre | Dépend de |
|-----|-------|-----------|
| **Gap-07** | Discipline outillée de co-évolution | Gap-05, Gap-06 |
| **Gap-11** | Archetype-aware contract lint | Gap-02, Gap-10 |

**Lecture** : Gap-07 et Gap-11 sont les « couches métier » qui rendent les P0 utilisables humainement.

---

## 3. P2 — Nice-to-have (3 gaps)

| Gap | Titre | Dépend de | Bloqué par |
|-----|-------|-----------|-----------|
| **Gap-16** | `@include` formalisé | Gap-03 | — |
| **Gap-17** | Détection édition manuelle de fichier généré | Gap-03 | — |
| **Gap-18** | Articulation snapshot ↔ log cumulatif | Gap-06 | — |

**Lecture** : ces gaps sont des **améliorations** du codegen et de la persistence. Ils peuvent être traités en fin de Phase 2 ou reportés en Phase 3.

---

## 4. Séquence proposée pour la Phase 2 (génération d'ADR vibebackbone par gap majeur)

**Note** : la Phase 2 est hors scope de cette consigne. La séquence ci-dessous est indicative, à valider par l'architecte.

### Étape 1 — Fondations (3 gaps en parallèle)

| Gap | Type de solution attendue | Risque canon |
|-----|---------------------------|--------------|
| Gap-01 | Extension `docs/CONTEXT.md` schema : ajout section `## DB Orientation` typée | Faible (extension, pas canon) |
| Gap-02 | Extension idem : ajout section `## Project Archetype` typée | Faible |
| Gap-05 | Nouveau fichier `docs/CONTRACTS_CONSUMED.md` + template | Faible (nouveau fichier) |

### Étape 2 — Discipline (5 gaps)

| Gap | Type de solution attendue | Risque canon |
|-----|---------------------------|--------------|
| Gap-10 | Extension du template `1-vbb-api-contract-designer` (ajout champ « Consumers ») | Faible |
| Gap-06 | Nouveau fichier `docs/IMPACT_LOG.md` + skill de mise à jour | Faible |
| Gap-09 | Nouveau dossier `docs/extensions/<pattern>/` + mécanisme d'enregistrement | Faible (nouveau dossier) |
| Gap-14 | Modification du contenu généré par `vbb-project-init.py` | Faible (contenu généré, pas canon) |

### Étape 3 — Outillage (3 gaps)

| Gap | Type de solution attendue | Risque canon |
|-----|---------------------------|--------------|
| Gap-04 | Nouveau `tools/vbb-multiservice-lint.py` + `docs/MULTISERVICE_DISCIPLINE.yaml` | Faible (nouvel outil) |
| Gap-08 | Nouveau mécanisme multi-repo : `docs/MULTIREPO.yaml` + adaptations des outils existants | **Moyen** (touche plusieurs outils) |
| Gap-13 | Nouveau `tools/vbb-multiservice-graph.py` | Faible |

### Étape 4 — Gates & co-évolution (3 gaps)

| Gap | Type de solution attendue | Risque canon |
|-----|---------------------------|--------------|
| Gap-15 | Hook CI + `tools/vbb-multiservice-lint.py` branché sur PR | Faible |
| Gap-07 | Skill de coordination + checklist outillée | Faible |
| Gap-11 | Extension de `vbb-contract-lint.py` avec règles contextuelles | Moyen (étend un outil canon) |

### Étape 5 — Codegen & extensions appliquées (3 gaps)

| Gap | Type de solution attendue | Risque canon |
|-----|---------------------------|--------------|
| Gap-03 | Nouveau `tools/vbb-agents-codegen.py` + extension de `setup.sh` | Moyen (touche distribution) |
| Gap-12 | Première extension concrète `docs/extensions/multi-service-database-per-service/` | Faible (extension) |

### Étape 6 — Polish (3 gaps P2)

| Gap | Type de solution attendue | Risque canon |
|-----|---------------------------|--------------|
| Gap-16 | Linter d'@include | Faible |
| Gap-17 | Sentinel `@generated` + détection | Faible |
| Gap-18 | Extension de `t-vbb-impact-analyzer` pour projection vers `IMPACT_LOG.md` | Faible |

**Estimation globale** (à valider) :
- 6 phases × 3-4 gaps = ~18-22 jours ouvrés.
- Risque canon global : **faible-moyen**. Seul Gap-08 (multi-repo) et Gap-11 (extension de linter canon) nécessitent une vigilance sur la rétrocompatibilité.

---

## 5. Critères de succès Phase 2

Pour chaque gap P0 traité en Phase 2, l'ADR vibebackbone produit doit :

1. **Citer la manifestation** dans `01_GAP_ANALYSIS.md` (ce document) avec fichier:ligne.
2. **Spécifier le type de solution** (canon change / extension / nouvel outil).
3. **Évaluer l'impact** sur les fichiers générés existants (RELATIONS.md, AGENTS.md, AUDIT_STATUS.md).
4. **Proposer une migration** (rétrocompatibilité ou version bump explicite).
5. **Lister les risques** et les mitigations.
6. **Être validé par l'architecte** avant implémentation.

---

## 6. Liens

- [`01_GAP_ANALYSIS.md`](01_GAP_ANALYSIS.md) — caractérisation des 18 gaps
- [`03_DEPENDENCIES.md`](03_DEPENDENCIES.md) — graphe de dépendances entre gaps
- [`04_OUT_OF_SCOPE.md`](04_OUT_OF_SCOPE.md) — ce qui est hors périmètre
- [`SESSION.md`](SESSION.md) — état de fin de run, prochaine action

---

**Verdict** : classification P0/P1/P2 validée. 7 P0 identifiés, séquence de traitement proposée pour la Phase 2 (à valider par l'architecte avant déclenchement).
