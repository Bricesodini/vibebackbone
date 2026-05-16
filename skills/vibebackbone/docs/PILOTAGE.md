## Usage par agent

Ce document est la **source de vérité** du pilotage vibebackbone pour le catalogue canonique
présent sous `skills/vibebackbone/`.

Il est utilisé par un orchestrateur, par exemple le skill `vibebackbone`, pour :

- classer une tâche dans une voie
- appliquer la règle de triage
- appliquer la règle d'escalade
- sélectionner les skills appropriés

Ce document ne doit pas être exécuté comme un audit ou comme une action métier.

Si un skill de lecture ou de routage diverge de ce document, `skills/vibebackbone/docs/PILOTAGE.md`
prévaut.

---

# PILOTAGE OPÉRATIONNEL - vibebackbone

**Version :** 2.0 | **Date :** 2026-05-13 | **Auteur :** Brice × Claude × Codex
**Statut :** Couche opérationnelle canonique - complète la base sans la modifier

---

## Principe

La base canonique vibebackbone reste inchangée.
Ce document définit la grille de décision opérationnelle utilisée pour router une tâche
vers le bon niveau de traitement, sans ambiguïté sur le degré de risque attendu.

Le pilotage doit rester lisible, stable et compatible avec Pi :

- les voies sont exclusives au moment du triage initial
- l'escalade est immédiate dès qu'un risque supérieur apparaît
- aucun skill absent du catalogue canonique ne doit être cité
- le catalogue doit refléter les chemins physiques réellement présents

---

## Canonical Ordering

### Socle fondamental

1. `vibebackbone`
2. `0-vbb-standard`
3. `0-vbb-guide`
4. `0-vbb-pilotage`

### Phase 0

1. `0-vbb-audit-readiness`
2. `0-vbb-scope-freeze`

### Phase 1

1. `1-vbb-code-janitor`
2. `1-vbb-conventions`
3. `1-vbb-formatter`
4. `1-p-vbb-tech-debt`
5. `1-vbb-monolith-detector`
6. `1-vbb-logic-duplication-detector`
7. `1-vbb-pattern-inconsistency-detector`
8. `1-vbb-error-handling-auditor`
9. `1-vbb-premature-abstraction-detector`
10. `1-vbb-test-mirage-detector`
11. `1-vbb-intent-decomposer`
12. `1-vbb-code-doc-coherence-auditor`
13. `1-vbb-code-doc-gap-integrator`
14. `1-vbb-doc-harmonizer`
15. `1-vbb-api-contract-designer`
16. `1-vbb-adr`

### Phase 2

1. `2-vbb-security`
2. `2-vbb-systemic-risk`
3. `2-vbb-data-integrity`
4. `2-vbb-db-robustness`
5. `2-vbb-ops`
6. `2-vbb-ci`
7. `2-vbb-legal`
8. `2-vbb-api-auditor`
9. `2-vbb-spec-validator`
10. `2-vbb-performance`
11. `2-vbb-accessibility`
12. `2-vbb-analytics`

### Phase 3

1. `3-p-vbb-risk-register`

### Transverses

1. `t-vbb-impact-analyzer`
2. `t-vbb-project-context-init`
3. `t-vbb-mode-transition-gate`
4. `t-vbb-test-coverage-mapper`
5. `t-p-vbb-session-handoff`
6. `t-vbb-commit-ready`
7. `t-vbb-docker-audit`
8. `t-vbb-docker-generate`
9. `t-vbb-anti-slop-gate`
10. `t-p-vbb-git-sync`

### Phase 4

1. `4-vbb-product-changelog`
2. `4-vbb-security-remediation`

### Pipeline front

1. `4-vbb-front-pipeline-reference`
2. `4-vbb-user-experience-engine`
3. `4-vbb-interaction-coherence-auditor`
4. `4-vbb-cognitive-load-optimizer`
5. `4-vbb-design-system-validator`
6. `4-vbb-visual-identity-layer`
7. `4-vbb-micro-interaction-refiner`
8. `4-vbb-visual-identity-gatekeeper`

---

## Les 4 voies

### 1 Voie rapide

**Usage :** modifications locales, lecture, vérification, harmonisation documentaire,
corrections mécaniques, reformatage, préparation de commit.

**Règle :** pas d'audit si le risque est faible. Agir directement.

**Skills naturels :**

- `1-vbb-doc-harmonizer`
- `1-vbb-code-janitor` (passe légère)
- `t-vbb-commit-ready`

### 2 Voie structurée

**Usage :** architecture, logique métier, dépendances, contrats de données, contrat API,
contexte de session, bootstrap documentaire.

**Règle :** lire `docs/PROJECT_MODE.md`, `docs/SESSION.md`, `docs/AUDIT_STATUS.md` avant d'agir
quand ces fichiers existent et sont pertinents.

**Skills naturels :**

- `t-vbb-dependency-mapper`
- `t-vbb-impact-analyzer`
- `1-p-vbb-tech-debt`
- `1-vbb-monolith-detector`
- `1-vbb-logic-duplication-detector`
- `1-vbb-pattern-inconsistency-detector`
- `1-vbb-error-handling-auditor`
- `1-vbb-premature-abstraction-detector`
- `1-vbb-test-mirage-detector`
- `1-vbb-conventions`
- `1-vbb-formatter`
- `1-vbb-intent-decomposer`
- `1-vbb-code-doc-coherence-auditor`
- `1-vbb-code-doc-gap-integrator`
- `1-vbb-api-contract-designer`
- `1-vbb-adr`
- `4-vbb-product-changelog`
- `t-vbb-project-context-init`
- `t-vbb-mode-transition-gate`

### 3 Voie audit

**Usage :** sécurité, risques systémiques, intégrité des données, robustesse DB, ops,
CI/CD, légal, consolidation finale, couverture de tests critique, déploiement infrastructure.

**Règle :** rapport horodaté obligatoire dans `docs/audits/`, mise à jour de
`docs/AUDIT_STATUS.md` à l'issue quand le format du skill l'exige.

**Skills naturels :**

- `0-vbb-audit-readiness`
- `0-vbb-scope-freeze`
- `2-vbb-security`
- `2-vbb-systemic-risk`
- `2-vbb-data-integrity`
- `2-vbb-db-robustness`
- `2-vbb-ops`
- `2-vbb-ci`
- `2-vbb-legal`
- `2-vbb-api-auditor`
- `2-vbb-spec-validator`
- `2-vbb-performance`
- `2-vbb-accessibility`
- `2-vbb-analytics`
- `3-p-vbb-risk-register`
- `t-vbb-test-coverage-mapper`
- `t-vbb-docker-audit`
- `t-vbb-docker-generate`
- `t-vbb-deploy-runtime`

**Note :** Ces 3 skills forment le pipeline Docker vibebackbone :
- `t-vbb-docker-audit` est un skill de lecture seule (voie audit).
- `t-vbb-docker-generate` est un skill d'exécution (voie structurée si dev, audit si staging/prod).
- `t-vbb-deploy-runtime` est un skill de cycle de vie avec gates d'intégrité (voie audit).
Ils sont conçus pour être chaînés via le prompt `4-p-vbb-deploy-docker`.
Pour un déploiement dev-only, `docker-generate` + `deploy-runtime` peuvent être rétrogradés en voie structurée.

### ④ Voie clôture

**Usage :** fin de session, handoff, préparation de reprise, préparation de commit,
synchronisation git finale.

**Règle :** déclencheur temporel ou de packaging, pas une escalade de risque.

**Skills naturels :**

- `t-p-vbb-session-handoff`
- `t-vbb-commit-ready`
- `t-p-vbb-git-sync`

**Note :** Le cycle de clôture typique est :
1. `t-p-vbb-session-handoff` → compresser le contexte
2. `t-vbb-commit-ready` → préparer le commit package
3. `t-p-vbb-git-sync` → exécuter le cycle git (commit, push, merge main)

---

## Règle de triage

Appliquer dans cet ordre à chaque nouvelle tâche :

```text
1. Touche à un contrat de données, de l'auth, à un contrat API, ou à un état de production ?
   → Voie structurée minimum

2. Touche à la sécurité, à l'intégrité des données, à la robustesse DB, à un périmètre réglementaire, ou au déploiement infrastructure (Docker, containers) ?
   → Voie audit (pipeline `t-vbb-docker-audit` → `t-vbb-docker-generate` → `t-vbb-deploy-runtime`)

3. Aucune des deux conditions ?
   → Voie rapide

4. Fin de session ou préparation de reprise / commit ?
   → Voie clôture (déclencheur temporel, indépendant des règles 1-3)
```

---

## Règle d'escalade

Si une tâche commencée en voie rapide révèle en cours d'exécution un impact sur un contrat
de données, de l'auth, d'un contrat API, de la sécurité, de la robustesse DB ou de la conformité,
escalader immédiatement vers la voie correspondante.

Ne jamais terminer en voie rapide si le risque a changé.

---

## Règle de cascade verdict × environnement

Cette règle s'applique à TOUS les skills vibebackbone, quel que soit le pôle (audit ou exécution).
Elle définit ce qu'un verdict de skill signifie pour le skill aval qui le consomme.

| Verdict | Dev | Staging | Prod |
| --- | --- | --- | --- |
| **READY** | Continuer | Continuer | Continuer |
| **PARTIAL** | Continuer avec avertissement | Continuer si confirmation utilisateur | **BLOQUER** - requiert résolution ou acceptation explicite documentée |
| **BLOCKED** | Arrêt immédiat | Arrêt immédiat | Arrêt immédiat |
| **UNKNOWN** | Continuer si confirmation utilisateur | **Arrêter** - trop risqué | **Arrêter** - trop risqué |

Règles complémentaires :

- Si un skill aval reçoit un verdict PARTIAL d'un skill amont en cible staging, il DOIT
  demander confirmation à l'utilisateur avant de continuer.
- Si un skill aval reçoit un verdict PARTIAL en cible prod, il DOIT refuser de continuer.
  L'utilisateur peut forcer en acceptant explicitement le risque, mais cette acceptation
  DOIT être documentée dans `docs/AUDIT_STATUS.md`.
- Si un verdict UNKNOWN est reçu en cible staging ou prod, le skill aval DOIT arrêter.
  L'utilisateur doit fournir les informations manquantes ou le contexte suffisant.
- Un skill BLOCKED ne peut jamais être contourné, quel que soit l'environnement.

Cette règle est la traduction opérationnelle du principe vibebackbone :
"Fail open = fail dangerous - quand le système hésite, il refuse."

---

## Correspondance voies ↔ skills

| Voie | Skills vibebackbone |
| --- | --- |
| **Rapide** | `1-vbb-doc-harmonizer`, `1-vbb-code-janitor` (passe légère), `t-vbb-anti-slop-gate` (contrôle qualité rapide), `t-vbb-commit-ready` |
| **Structurée** | `t-vbb-dependency-mapper`, `t-vbb-impact-analyzer`, `1-p-vbb-tech-debt`, `1-vbb-monolith-detector`, `1-vbb-logic-duplication-detector`, `1-vbb-pattern-inconsistency-detector`, `1-vbb-error-handling-auditor`, `1-vbb-premature-abstraction-detector`, `1-vbb-test-mirage-detector`, `1-vbb-conventions`, `1-vbb-formatter`, `1-vbb-intent-decomposer`, `1-vbb-code-doc-coherence-auditor`, `1-vbb-code-doc-gap-integrator`, `1-vbb-api-contract-designer`, `1-vbb-adr`, `4-vbb-product-changelog`, `t-vbb-project-context-init`, `t-vbb-mode-transition-gate` |
| **Audit** | `0-vbb-audit-readiness`, `0-vbb-scope-freeze`, `2-vbb-security`, `2-vbb-systemic-risk`, `2-vbb-data-integrity`, `2-vbb-db-robustness`, `2-vbb-ops`, `2-vbb-ci`, `2-vbb-legal`, `2-vbb-api-auditor`, `2-vbb-spec-validator`, `2-vbb-performance`, `2-vbb-accessibility`, `2-vbb-analytics`, `3-p-vbb-risk-register`, `t-vbb-test-coverage-mapper`, `t-vbb-docker-audit`, `t-vbb-docker-generate`, `t-vbb-deploy-runtime` |
| **Clôture** | `t-p-vbb-session-handoff`, `t-vbb-commit-ready`, `t-p-vbb-git-sync` |

---

## Note d'intégration avec la base canonique

Ce document ne remplace ni ne modifie aucun skill existant.
Il s'intercale comme couche de décision **avant** l'exécution.

```text
1. Lire docs/SESSION.md        → contexte de la session
2. Appliquer la règle de triage → identifier la voie
3. Sélectionner le skill        → dans la voie identifiée
4. Exécuter                     → selon les instructions du skill
```

La base canonique (les `SKILL.md` du dossier `skills/vibebackbone/`) reste la référence
d'exécution. Ce document est la règle de sélection, pas la règle d'exécution.

---

## Compatibilité Claude / Codex / Pi

Ce document est rédigé pour être lu identiquement par Claude, Codex et Pi.
La règle de triage est exprimée en termes de risque et de niveau de traitement,
sans dépendre d'un agent particulier.

Chaque agent applique ensuite ses propres mécanismes d'exécution dans la voie sélectionnée.

---

_vibebackbone Pilotage v2.0 - Brice × Claude × Codex · 2026-05-13_
