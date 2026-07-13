---
context_role: out-of-scope
phase: strategy
status: active
updated: 2026-07-12
scope: vibebackbone framework → multi-service patterns
phase_phase_label: "Phase 1 — Caractérisation des manques (pas de solution)"
---

# 04 — Hors périmètre : ce qui n'est PAS dans cette évolution

> **Périmètre** : ce document liste explicitement ce qui est **hors** du périmètre de l'évolution `vbb-evolution-multi-service-support`. Il sert de garde-fou pour éviter les déviations de scope en Phase 2 et Phase 3.
>
> **Source** : consigne §3 « Ce que tu ne fais pas dans cette phase » + classification des gaps hors-périmètre identifiés pendant l'analyse.

---

## 0. Périmètre strict (rappel de la consigne §3)

La consigne interdit explicitement en Phase 1 :

- ❌ Implémenter une quelconque solution
- ❌ Modifier le canon `CONVENTIONS.md` ou `PILOTAGE.md`
- ❌ Créer des outils (`vbb-orientation-codegen.py`, etc.)
- ❌ Écrire des ADR vibebackbone pour cette évolution
- ❌ Faire évoluer un projet concret (studio-projects, export-engine, compta)

**Ces interdits sont respectés** : la Phase 1 produit 4 documents Markdown de caractérisation + 1 SESSION.md. Aucune ligne de Python modifié, aucun canon touché.

---

## 1. Hors périmètre de l'évolution (toutes phases)

### 1.1 Implémentation runtime multi-services

- ❌ Déployer un système de 4 services coordonnés en production.
- ❌ Choisir une technologie de bus (NATS, Kafka, RabbitMQ, etc.).
- ❌ Définir les protocoles concrets (REST vs gRPC vs GraphQL).
- ❌ Implémenter les contrats API spécifiques à studio-projects, export-engine ou compta.

**Justification** : l'évolution concerne **vibebackbone lui-même** (le framework). Les cas d'usage (studio-projects, etc.) servent à caractériser les manques, pas à être implémentés.

### 1.2 Migration des projets existants

- ❌ Migrer `studio-projects` (ou un sous-projet) vers les patterns multi-service.
- ❌ Migrer `export-engine` ou `compta` vers une nouvelle version de vibebackbone.
- ❌ Convertir un projet mono-service existant en multi-service.

**Justification** : la consigne §3 dit « le run studio-projects utilise ce que vibebackbone **offre déjà**, en attendant les évolutions ». La migration est un acte post-Phase 3, conditionné à la stabilisation des extensions.

### 1.3 Modification du canon existant

- ❌ Ajouter un nouveau pilier **canonique** (P6, P7…) à `docs/CONVENTIONS.md`.
- ❌ Modifier les routes (`PILOTAGE.md`) pour ajouter une voie « MULTI-SERVICE ».
- ❌ Renommer ou restructurer les 5 piliers P1-P5.

**Justification** : tout canon change est lourd (CANON_CHANGE_PROPOSAL.md.template + validation humaine). Les évolutions proposées sont conçues comme **extensions** (`docs/extensions/<pattern>/`), pas comme canon. Voir Gap-09.

### 1.4 Création d'outils dans cette Phase 1

- ❌ `tools/vbb-orientation-codegen.py`
- ❌ `tools/vbb-multiservice-lint.py`
- ❌ `tools/vbb-multiservice-graph.py`
- ❌ `tools/vbb-contracts-consumed.py`

**Justification** : la consigne §3 interdit explicitement la création d'outils dans cette phase. Les outils seront créés en Phase 3, après validation des ADR en Phase 2.

### 1.5 ADR vibebackbone

- ❌ Créer `docs/adr/0014-orientation-db.md`
- ❌ Créer `docs/adr/0015-multiservice-lint.md`
- ❌ Tout ADR vibebackbone lié à cette évolution.

**Justification** : la consigne §3 dit « le déclenchement d'un ADR vibebackbone vient après analyse ». Les ADR seront créés en Phase 2, gap par gap, après validation par l'architecte.

### 1.6 Distribution de l'évolution

- ❌ Mettre à jour `distributions/hermes/setup.sh` ou `distributions/hermes/proxy/` pour cette évolution.
- ❌ Modifier `distributions/pi/SYSTEM.md` ou `distributions/claude/CLAUDE.md` pour coder les nouveaux mécanismes.
- ❌ Déployer la nouvelle version via `setup.sh` chez les providers (Claude, Codex, Pi, Hermes).

**Justification** : la distribution est l'**étape finale**, après stabilisation du Core. Référence : `docs/DISTRIBUTIONS.md` (les Core changes ripple to all distributions).

---

## 2. Hors périmètre du framework vibebackbone (en général)

### 2.1 Patterns non-multi-services

- ❌ Frontend-only patterns (les patterns « front pipeline » `4-vbb-*` sont déjà couverts par les 7 passes, hors sujet ici).
- ❌ Single-binary delivery.
- ❌ Edge / serverless patterns.
- ❌ Data-lake / OLAP patterns (le database-per-service cible OLTP / service-oriented, pas analytique).

**Justification** : la consigne cible explicitement « database-per-service » et « API d'intégration ». Les autres patterns relèvent d'évolutions distinctes.

### 2.2 Outils externes au framework

- ❌ Terraform / Pulumi / Ansible (orchestration infra, hors framework).
- ❌ Kubernetes operators (orchestration runtime, hors framework).
- ❌ Service mesh (Istio, Linkerd, etc.).
- ❌ API gateways (Kong, Ambassador, etc.).

**Justification** : ces outils sont **consommables** par un projet vibebackbone, mais ne sont pas dans le périmètre du framework lui-même. Vibebackbone documente la discipline, pas l'infra.

### 2.3 Sécurité et identité cross-service

- ❌ Implémentation concrète d'OAuth2 client credentials entre services.
- ❌ mTLS automatique.
- ❌ Vault / secret store spécifique.

**Justification** : ces aspects sont **policy** (ce qui doit être respecté), pas **mécanisme** (comment le faire). Vibebackbone peut documenter la policy dans une extension, mais l'implémentation est externe. Référence : ADR 0007 (proxy credential management) déjà existant.

### 2.4 CI/CD multi-repo

- ❌ Orchestration concrète de CI sur N repos (matrix builds, dépendances inter-repos).
- ❌ Release management cross-repo.

**Justification** : ce sont des patterns d'orchestration d'outillage CI, pas des patterns framework. Vibebackbone peut outiller la **discipline** (Gap-15), pas l'outillage CI lui-même.

### 2.5 Observabilité cross-service

- ❌ Tracing distribué (OpenTelemetry, Jaeger, etc.).
- ❌ Métriques cross-service (Prometheus, etc.).
- ❌ Logging agrégé (ELK, Loki, etc.).

**Justification** : Vibebackbone peut tracer des **invariants** (P.R1-P.R8) mais ne fournit pas l'observabilité runtime. Les projets qui en ont besoin choisissent leurs outils.

---

## 3. Pièges classiques à éviter en Phase 2 / Phase 3

### 3.1 « On va juste modifier CONVENTIONS.md, c'est plus simple »

**Risque** : prendre le chemin canon change au lieu de l'extension. **Mitigation** : Gap-09 propose un mécanisme d'extension. Toute modification de CONVENTIONS.md pour cette évolution doit être justifiée et tracée.

### 3.2 « On va juste ajouter un pilier P6 dans CONVENTIONS.md »

**Risque** : confusion entre pilier canon et pattern émergent. **Mitigation** : Gap-12 propose une **extension** `multi-service-database-per-service`, pas un pilier canon. Si P6 est ajouté, c'est par canon change séparé, validé humainement.

### 3.3 « On va juste écrire CONTRACTS_CONSUMED.md à la main pour studio-projects »

**Risque** : traiter un cas d'usage comme généralisation. **Mitigation** : le fichier doit être **outillé** (Gap-05) — pas juste un template copié-collé.

### 3.4 « On peut faire le multi-repo plus tard, l'urgent c'est la discipline »

**Risque** : reporter un P0. **Mitigation** : Gap-08 (multi-repo) et Gap-13 (graphe global) sont P0 dans la classification de §1.1 / §1.2 de `02_PRIORITIES.md`. Ne pas les reporter après les P1.

### 3.5 « On a déjà 5 ADR dans `docs/adr/`, on est bons »

**Risque** : croire que les ADR existants couvrent le sujet. **Mitigation** : les 5 ADR couvrent executor (0001), UI/UX routing (0002), graphic propagation (0003), schema version (0004), Core vs Distribution (0013). Aucun ne traite database-per-service ou co-évolution. Voir §4 de `01_GAP_ANALYSIS.md`.

---

## 4. Ce qui EST dans le périmètre (rappel)

Pour équilibrer, voici ce qui EST dans le périmètre de l'évolution :

### Phase 1 (cette consigne — TERMINÉE)

- ✅ Caractérisation des 15 gaps initiaux + 3 dérivés.
- ✅ Priorisation P0/P1/P2.
- ✅ Graphe de dépendances.
- ✅ Liste de hors-périmètre (ce document).

### Phase 2 (à venir)

- ✅ Proposition de solution pour chaque gap P0/P1 (canon change OU extension OU outil).
- ✅ Production d'un ADR vibebackbone par gap majeur (après validation architecte).
- ✅ Pas d'implémentation.

### Phase 3 (à venir après Phase 2)

- ✅ Implémentation des solutions acceptées.
- ✅ Tests + vérification (P.R2).
- ✅ Documentation (CONVENTIONS.md étendu OU `docs/extensions/<pattern>/`).
- ✅ Distribution via `setup.sh` (si applicable).

### Au-delà de Phase 3 (post-stabilisation)

- ✅ Migration éventuelle de studio-projects vers les nouveaux mécanismes.
- ✅ Rétrofit éventuel d'export-engine et compta.
- ✅ Feedback loop sur les extensions.

---

## 5. Liens

- [`01_GAP_ANALYSIS.md`](01_GAP_ANALYSIS.md)
- [`02_PRIORITIES.md`](02_PRIORITIES.md)
- [`03_DEPENDENCIES.md`](03_DEPENDENCIES.md)
- [`SESSION.md`](SESSION.md)
- Consigne source : `vbb-evolution-multi-service-support` §3 (ce qui ne se fait pas dans cette phase)
