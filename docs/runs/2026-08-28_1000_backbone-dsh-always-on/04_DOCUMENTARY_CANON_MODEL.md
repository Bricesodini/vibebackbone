---
context_role: documentary-canon-model
phase: 04_DOCUMENTARY_CANON_MODEL
status: READY
run_id: "2026-08-28_1000_backbone-dsh-always-on"
tier: A2 (touche au modèle documentaire du canon)
adversarial_governance_version: "1.2"
agent: "dsh"
started_at: "2026-08-28T13:30:00Z"
ended_at: "2026-08-28T15:30:00Z"
next_phase: "05_MEMORY_INTEGRATION_MODEL"
artifacts_consumed:
  - "01_CURRENT_STATE.md"
  - "02_HYPOTHESIS.md"
  - "03_ALWAYS_ON_CONTRACT.md"
  - "docs/document-model/DOCUMENT_ONTOLOGY.md"
  - "docs/document-model/DOCUMENT_GRAPH_MODEL.md"
  - "docs/document-model/DOCUMENT_IDENTITY_MODEL.md"
  - "docs/document-model/DOCUMENT_TRANSITION_PROTOCOL.md"
  - "docs/document-model/DOCUMENT_TAG_SPECIFICATION.md"
  - "docs/document-model/DOCUMENT_MODEL_REFERENCE_ARCHITECTURE.md"
  - "docs/MEMORY_AND_HANDOFF.md"
  - "docs/runs/2026-08-26_2105_memory-authority-seam/poc/fixtures/canon/"
artifacts_produced:
  - "04_DOCUMENTARY_CANON_MODEL.md"
depends_on:
  - "Documentary Contract v1.0 (DIM, Ontology, DGM, DTS, DTP)"
  - "ADR 0049 (engineering knowledge lifecycle)"
  - "ADR 0055 §C2 (canon ↔ memory projection)"
  - "MEMORY_AND_HANDOFF.md (3 niveaux de mémoire)"
carried_reservations:
  - "R-E3-1 (transfert vers E5)"
  - "R-E4-1 (auto-surveillance de ce livrable)"
related:
  - "docs/adr/0049-engineering-knowledge-governance.md"
  - "docs/adr/0055-memory-authority-seam.md"
---

# 04_DOCUMENTARY_CANON_MODEL — cinq vues dérivées (pas cinq statuts)

> E4 ne crée **aucun nouveau statut canonique**. Les cinq vues
> (`CURRENT_CANON`, `ACTIVE_DECISIONS`, `SUPERSEDED`,
> `EXPERIMENTAL`, `HISTORICAL`) demandées par le brief §4.4 sont définies
> ici comme **projections** sur des axes ontologiques **déjà**
> canoniques du Documentary Contract v1.0 (DIM, Ontology, DGM, DTS,
> DTP). Aucune métadonnée inventée. Si une vue n'est pas dérivable,
> c'est un **résultat expérimental** (§6), pas un trou à combler
> localement.

## 0. Réserves reportées explicitement

Ces deux réserves ont été posées par la décision utilisateur avant le
lancement d'E4 et doivent rester visibles jusqu'à clôture E9.

### 0.1 `R-E3-1` — transférée à E5

> P-3 = N/A en dégradation ne prouve **pas** qu'une architecture
> cible **sans** Backbone Memory satisfait H1.

- **Champ d'application**. P-3 dans E3 §1 dit que si aucune
  mémoire n'est montée, la propriété devient N/A. La logique de
  cette décision visait à ne pas pénaliser une session
  DSH dont la mémoire est temporairement indisponible (falsif `F6`).
- **Risque identifié**. Tel qu'écrit, ce N/A peut être lu comme une
  réussite de `H1-PERMANENT` pour une configuration cible qui
  n'aurait simplement pas de Backbone Memory. Or le brief §5 fait
  de Backbone Memory une **partie obligatoire de l'expérimentation**.
- **Conséquence pour E4**. E4 ne statue pas ; le modèle
  documentaire dérive la notion de CURRENT_CANON indépendamment
  d'une mémoire montée. La distinction « dégradation vs
  configuration cible » est explicitement portée à `E5 § « Frontière
  F6 / architecture cible »` pour décision.
- **Trace**. R-E3-1 réapparaît dans `05_MEMORY_INTEGRATION_MODEL.md`
  et dans `07_FALSIFICATION_MATRIX.md` (F6 + P-3).

### 0.2 `R-E4-1` — auto-surveillance de ce livrable

> Les cinq vues documentaires sont des projections à dériver et
> falsifier, pas cinq nouveaux statuts canoniques à instaurer.

- **Application continue**. Ce document se vérifie en fin de
  rédaction par les tests T-NEW-1 à T-NEW-4 (§9). Tout ajout de
  champ frontalier non présent dans les autorités existantes
  déclenche une revue immédiate et un rollback.
- **Détection de drift**. Si une section ultérieure (E5, E6, E8)
  propose un nouveau statut autoritaire (par exemple un
  `historical_canon` ou un `experiment_tier`), c'est un drift
  `F-PERM`-adjacent à signaler comme précurseur.

## 1. Inventaire des autorités existantes — ce qui est disponible

E4 vérifie d'abord que les autorités du canon **suffisent en
principe** à dériver les vues, sans ajout.

### 1.1 Documentary Contract v1.0 (declared adopted dans `.vbb/document-convention.yaml`)

| Couche | Fichier | Ce qu'elle fournit — pertinent ici |
|---|---|---|
| Identity (DIM) | `docs/document-model/DOCUMENT_IDENTITY_MODEL.md` | distinction identité / représentation / révision / location (6 invariants) |
| Qualification (Ontology) | `docs/document-model/DOCUMENT_ONTOLOGY.md` | 6 axes orthogonaux : `authority`, `lifecycle`, `temporality`, `primary_function`, `secondary_functions`, `load_policy` |
| Relations (DGM) | `docs/document-model/DOCUMENT_GRAPH_MODEL.md` | 12 relations : `REPRESENTED_BY`, `REVISION_OF`, `LOCATED_AT`, `GENERATED_FROM`/`PROJECTS`, `DISTRIBUTED_TO`, `REFERENCES`, `GOVERNS`, `ESTABLISHED_BY`, `SUPPORTED_BY`, `SUPERSEDES`, `CONFLICTS_WITH` |
| Observability (DTS) | `docs/document-model/DOCUMENT_TAG_SPECIFICATION.md` | fait / compatibilité (`COMPATIBLE` / `MIGRATION_REQUIRED` / `INCOMPATIBLE` / `UNKNOWN`) ; **ne crée pas d'autorité** |
| Transition (DTP) | `docs/document-model/DOCUMENT_TRANSITION_PROTOCOL.md` | 7 phases (`Anchor → Qualify → Detect → Decide → Route → Validate → Publish`) ; définit la décision humaine explicite `OUI` / `NON` / `PLUS TARD` |

La couche Ontology fournit **tout** ce qu'il faut pour dériver les 5
vues. Aucun nouveau champ n'est nécessaire.

### 1.2 ADR qui complètent ou chevauchent

- ADR 0049 (engineering knowledge governance) — `Lifecycle =
  PROPOSED → ACTIVE → TRANSITIONAL → SUPERSEDED → RETIRED`
  l'aligne sur le lifecycle Ontology. Cinq étapes.
- ADR 0055 §C2 — les trois classes d'autorité mémoire
  (`projection`, `candidate`, `working`) n'ont pas vocation à
 Qualifier un artefact du dépôt. Une vue sur le canon ne peut donc
  pas directement récupérer la granularité ADR 0055 (et ne doit
  pas, par ADR 0049).
- ADR 0050, 0051, 0053, 0052, 0054 — déjà dans `tools/vbb-gate-check.py`
  et `.vbb/document-convention.yaml`. Ne couvrent pas la question
  documentaire stricto sensu.

### 1.3 `MEMORY_AND_HANDOFF.md`

Trois niveaux de mémoire (officiel / local / conversation). Indique
implicitement que `docs/CONTEXT.md` est **un** point d'entrée pour
trouver le canon. Ne fournit pas d'axe supplémentaire.

### 1.4 Outil canonique existant — `tools/vbb-architecture.py`

Lit `docs/ARCHITECTURE.md`, expose un graphe, produit
`docs/RELATIONS.md`. **Ne lit pas le frontmatter ontologique par
artefact**. Pourrait être étendu (E5+ considère cela comme lacune
opérationnelle, **pas** comme une nouvelle autorité documentaire).

### 1.5 Conclusion de l'inventaire

Les autorités existantes **suffisent en principe** à dériver 5 vues.
La question qui suit est : les corpus les **expose-t-il** aujourd'hui
? — c'est l'objet de §6. **Aucune lacune d'autorité n'est identifiée**.

## 2. Définitions formelles des cinq vues — projections, pas statuts

Chaque vue est une **projection** (un ensemble dérivé) sur une
combinaison explicite d'axes existants. Une vue **ne confère aucune
autorité** ; elle est le reflet d'une qualification déjà portée par
les axes eux-mêmes. Voici la grammaire canonique de dérivation.

### 2.1 Grammaire commune

```
Vue ::= { artefact | ∃ qualification(artefact) ∧ ∃ relations(artefact) ∧ conditions }

Conditions ::= authority ∈ { CANONICAL, SCOPED_AUTHORITY }
             | lifecycle ∈ { ACTIVE, TRANSITIONAL, SUPERSEDED, RETIRED, PROPOSED }
             | temporality ∈ { CURRENT, PAST, FUTURE, MULTI_PERIOD, UNDATED }
             | primary_function ∈ { NORMATIVE, REFERENCE, EVIDENCE, DECISION_RECORD,
                                      RUN_ARTIFACT, GENERATED, NAVIGATION }
             | ∃ r : DGM_relation(artefact, …)
```

### 2.2 `CURRENT_CANON`

**Définition.** L'ensemble des artefacts **canoniques** et
**courants**.

```
CURRENT_CANON ≜
    { a | authority(a) ∈ {CANONICAL, SCOPED_AUTHORITY}
          ∧ lifecycle(a) ∈ {ACTIVE, TRANSITIONAL}
          ∧ (temporality(a) = CURRENT
             ∨ temporality(a) = MULTI_PERIOD) }
```

**Ce que cette vue n'est pas.** Pas un statut autoritaire. Pas une
promotion. Pas un remplacement. C'est un **reflet**.

### 2.3 `ACTIVE_DECISIONS`

**Définition.** Sous-ensemble de `CURRENT_CANON` restreint aux
artefacts dont la fonction primaire est `DECISION_RECORD` ou
`NORMATIVE` (selon l'ontology, ADR et règle).

```
ACTIVE_DECISIONS ≜
    { a | a ∈ CURRENT_CANON
          ∧ primary_function(a) ∈ {DECISION_RECORD, NORMATIVE} }
```

### 2.4 `SUPERSEDED`

**Définition.** L'ensemble des artefacts **supersédés** par
construction ou par relation.

```
SUPERSEDED ≜
    { a | lifecycle(a) = SUPERSEDED
          ∨ ∃ b : SUPERSEDES(b, a) ∈ DGM
          ∨ superseded_by(a) ≠ ⊥ }
```

Le vocabulaire de l'ontology permet deux modes d'expression :
- déclaratif : `lifecycle(a) = SUPERSEDED` ;
- relationnel : `SUPERSEDES(b, a)` (DGM) ou
  `superseded_by(a) = b` (artefact b prend la suite de a).

Un artefact dans `SUPERSEDED` **est hors** de `CURRENT_CANON`. Il
reste **retrouvable** par la relation inverse — c'est la propriété
demandée dans Hard Case #1.

### 2.5 `EXPERIMENTAL`

**Définition.** L'ensemble des artefacts en **état de
proposition non-promue** ou en **transitional chemin vers
qualification**.

```
EXPERIMENTAL ≜
    { a | lifecycle(a) ∈ {PROPOSED, TRANSITIONAL}
          ∧ authority(a) ∉ {CANONICAL} }
```

**Avertissement ferme.** Cette vue **n'est pas définie par la
récence**. Elle est définie par l'état canonique du cycle de
gouvernance (`Lifecycle=PROPOSED` ou `TRANSITIONAL`) et par
**l'absence** de qualification canonique. Un document d'il y a
deux ans marqué `PROPOSED` est `EXPERIMENTAL` ; un document d'il
y a une heure marqué `ACTIVE` est `CURRENT_CANON`. La
**récence n'est pas un proxy d'autorité** — c'est l'observable
qui protège contre `F3` (brief §12).

### 2.6 `HISTORICAL`

**Définition.** L'ensemble des artefacts **passés** ou
**retirés** du canon.

```
HISTORICAL ≜
    { a | temporality(a) = PAST
          ∨ lifecycle(a) = RETIRED }
```

**Distinction vis-à-vis de `SUPERSEDED`.** Un artefact peut
être à la fois `SUPERSEDED` (lifecycle) et `HISTORICAL`
(temporality), mais pas nécessairement. La nuance respecte
l'orthogonalité des axes.

### 2.7 Orthogonalité des cinq vues

Les cinq vues sont des **projections** sur des combinaisons
distinctes des mêmes axes. Aucune n'ajoute un axe. Une vue
peut être vide sans que le canon ait un problème. Un artefact
peut appartenir à zéro, une ou plusieurs vues (par exemple un
artefact `SUPERSEDED` ET `HISTORICAL`). **Aucune vue n'a
d'autorité propre** ; aucune n'est supérieure ou subalterne à
une autre.

## 3. Anti-invention (R-E4-1 appliquée)

Cette section formalise la contrainte R-E4-1 sous forme de
tests à passer avant publication.

| Test | Énoncé | Pass = OK |
|---|---|---|
| T-NEW-1 | Aucune section ci-dessus ne définit un nouveau champ frontalier (par exemple `historical_tier`, `experiment_class`, `legacy_status`). | ✅ aucun nouveau champ introduit. |
| T-NEW-2 | Chaque vue est une projection sur ≥ 1 axe ontologique existant. | ✅ §2.2 à §2.6 citent leurs axes explicitement. |
| T-NEW-3 | Aucune vue ne crée d'autorité concurrente à ADR 0055 §C4 (cinq dimensions). | ✅ les vues ne sont pas des statuts autoritaires. |
| T-NEW-4 | Si une lacune d'observation est constatée (§6), elle est rapportée comme lacune, **pas** comblée par une nouvelle métadonnée. | ✅ §6 ne propose pas de nouveau champ. |

## 4. Application aux quatre cas difficiles du brief

Test concret, à partir des fixtures POC du vérificateur ADR 0055
et du comportement observé du canon.

### 4.1 Cas #1 — Historiquement canonique mais désormais superseded

- **Fixture disponible** :
  `docs/runs/2026-08-26_2105_memory-authority-seam/poc/fixtures/canon/art_export_v1.md`
  (frontmatter complet : `id`, `lifecycle: canonical`,
  `status: superseded`, `superseded_by: art_export_v2`).
- **Dérivation applique §2.4** : `lifecycle = SUPERSEDED` ⇒
  ∈ `SUPERSEDED`. `status = superseded` confirme. **L'artefact
  appartient à `SUPERSEDED` et **n'appartient pas** à
  `CURRENT_CANON`** (car `lifecycle = SUPERSEDED` est exclu du
  domaine de `CURRENT_CANON`).
- **Retrouvabilité de la chaîne**. Le `superseded_by: art_export_v2`
  permet de naviguer vers le successeur ; `art_export_v2` lui-même
  porte `supersedes: art_export_v1`, ce qui rend la transition
  observable des deux côtés.
- **Verdict** : ✅ la dérivation fonctionne **là où le
  frontmatter est peuplé**.

### 4.2 Cas #2 — Proposition récente non promue

- **Fixture disponible**. Aucun artefact réel du canon observable
  ne porte `lifecycle: PROPOSED` en frontmatter (cf. §6).
- **Dérivation applique §2.5** : si le frontmatter
  `lifecycle = PROPOSED` était peuplé, l'artefact irait dans
  `EXPERIMENTAL`, jamais dans `CURRENT_CANON` (car `PROPOSED ∉
  {ACTIVE, TRANSITIONAL}`).
- **Test de la récence (F3)**. La définition ne tient **pas
  compte** de la date de création. Une proposition d'hier et une
  proposition d'il y a six mois sont toutes deux dans
  `EXPERIMENTAL` tant qu'elles n'ont pas été promues. **Récence
  ≠ autorité**, confirmé.
- **Verdict** : ✅ la définition protège de F3. ⚠️ la
  projection est aveugle tant que le frontmatter `lifecycle` est
  absent.

### 4.3 Cas #3 — Décision active avec documents dérivés stale

- **Contexte**. Une décision canonique (ADR `ACCEPTED`) génère
  des artefacts dérivés (projections, distributions). Si la source
  est supersédée, les dérivés doivent le suivre ou être invalidés.
- **Dérivation**. ADR 0055 §C2 (`projection` n'est pas autoritaire,
  suit la source) + DGM `PROJECTS` (projection a une source
  traçable).
- **Test observable**. Si l'ADR source passe en `lifecycle =
  SUPERSEDED`, alors : `projection` correspondante n'est plus
  `projection` (selon `seam_check.py`, code
  `PROJECTION_STALE_SUPERSEDED`).
- **Confusion autorité / projection**. La décision canonique
  reste **canonique par son artefact**, pas par ses projections.
  Une projection stale n'est qu'un reflet ; elle ne peut pas
  « décider » du statut de la source.
- **Verdict** : ✅ la distinction source/projection est dans le
  canon (ADR 0055 §C1, DGM `PROJECTS`). ⚠️ l'outillage qui
  reconstruit la traçabilité source→projection n'existe pas
  encore (E5 §résultats, hors-périmètre de ce livrable).

### 4.4 Cas #4 — Succession A → B → C

- **Fixture disponible**. Chaîne à deux maillons :
  `art_export_v1` → `art_export_v2` (§4.1). Pas d'exemple à
  trois maillons dans le corpus.
- **Dérivation applique §2.4** : `SUPERSEDEDES(b, a)`
  compositionnable. Si B porte `supersedes: [A]` et C porte
  `supersedes: [B]`, alors A ∈ `SUPERSEDED` (chaîne
  reconstructible).
- **Limitation observée**. Dans le corpus canonique des ADRs,
  `supersedes:` est peu peuplé et `superseded_by:` ne l'est pas
  (cf. §6). Une chaîne A → B → C demanderait une révision
  documentaire systématique que le canon n'opère pas
  actuellement.
- **Verdict** : ✅ la dérivation est correcte par composition. ⚠️
  la reconstruction automatique n'est pas garantie sans pratique
  de tenue du frontmatter.

### 4.5 Synthèse des cas

| Cas | Dérivation correcte ? | Outillage de projection observable ? |
|---|---|---|
| #1 Historiquement canonique désormais superseded | ✅ sur fixtures | ⚠️ partiel sur le reste du canon |
| #2 Récente proposition non promue | ✅ par construction | ⚠️ dépend de `lifecycle` frontmatter |
| #3 Décision active + dérivés stale | ✅ par ADR 0055 §C2 | ⚠️ outillage manquant |
| #4 Succession A → B → C | ✅ compositionnellement | ⚠️ outillage / pratique manquants |

La **définition** des vues est donc correcte et vérifiable sur
fixtures ; **l'observation systématique** dans le canon dépend
d'inventaire de métadonnées que E4 **ne peut pas garantir**.

## 5. Distinction ferme vue ↔ statut autoritaire

C'est la conséquence directe de R-E4-1.

```
Vue       Projection sur axes existants, sans autorité propre.
Statut    Combinaison d'axes, qualifie un artefact, autoritaire.
```

Toute tentative future d'utiliser `CURRENT_CANON` comme **statut**
(synonyme de « ce qui fait autorité ») violerait `NO_PARALLEL_SEMANTIC_AUTHORITY`
(ADR 0055 §C1). Les vues sont **des outils de navigation**, pas
des **primitives de décision**.

Une exception n'est permise que si un ADR la crée explicitement
(par exemple, un ADR qui déclarerait « tout artefact non
CURRENT_CANON est exclu de X ») ; cet ADR reste alors une règle
sur les statuts, pas une promotion des vues au rang de statut.

## 6. Lacunes observées dans le corpus — le résultat expérimental attendu

Le brief dit : « Si les autorités actuelles sont insuffisantes
pour reconstruire ces états, c'est un résultat expérimental
important et potentiellement une lacune à traiter ensuite. » Voici
ce constat.

### 6.1 État du corpus

| Champ ontologique canonique | Population observée |
|---|---|
| `lifecycle:` | 5/5 fixtures POC d'ADR 0055 ; **0** ADRs du canon principal ; **0** autres documents canoniques. |
| `authority:` | **0** documents du corpus portent `authority:` en frontmatter. |
| `temporality:` | **0** documents. |
| `primary_function:` | **0** documents. |
| `load_policy:` | **0** documents. |
| `subject_key:` | 5/5 fixtures POC ; **0** ADRs. |
| `supersedes:` | Présent en YAML dans ADRs, le plus souvent `vide`. |
| `superseded_by:` | **0** occurrences dans tout le canon (non-tracké inclus). |

En outre, deux styles d'ADR coexistent : **style A** (entête
`# ADR 00XX — ... / **Status**: ACCEPTED / **Date**: ...` dans le
corps ; voir ADR 0049) et **style B** (YAML frontmatter
`status: accepted / date: ...` ; voir ADR 0050+). Le Documentary
Contract v1.0 ne déclare pas l'un ou l'autre canonique.

### 6.2 Conséquence directe

Les cinq vues sont **dérivables en principe** à partir des
autorités ; elles ne sont **pas observables systématiquement** à
partir du corpus. Les fixtures POC d'ADR 0055 sont les seuls
exemples complets.

### 6.3 Statut de ces lacunes

Ce sont des **lacunes opérationnelles**, **pas** des lacunes
d'autorité. Le canon possède les axes ; il ne les expose pas dans
le dépôt. C'est un travail documentaire, non un nouveau statut.

**E4 ne propose donc aucune métadonnée nouvelle.** Il documente
les lacunes ; il en confie le traitement à un éventuel run futur,
avec un ADR dédié si la métadonnée devient autoritaire, ou avec
un travail de tenue documentaire si elle reste descriptive.

### 6.4 Lacunes émergentes — celles que cette expérimentation ne ferme pas

| ID | Lacune | Sévérité |
|---|---|---|
| LAC-DOC-1 | Aucune métadonnée ontologique n'est peuplée en dehors des fixtures POC. | Forte |
| LAC-DOC-2 | Aucun marqueur canonique n'indique le `load_policy` d'un document ; `tools/vbb-architecture.py` n'analyse pas ce champ. | Forte |
| LAC-DOC-3 | La translation entre l'in-text `Status:` d'un ADR (style A) et le `lifecycle` ontologique n'est pas déclarée. | Moyenne |
| LAC-DOC-4 | Aucun balayage de la chaîne A → B → C n'existe : un supersession à trois maillons ne peut pas être reconstruit sans script ad hoc. | Moyenne |
| LAC-DOC-5 | Confusion de style A/B d'ADR non résolue par le canon actuel. | Moyenne |
| LAC-DOC-6 | `tools/vbb-architecture.py` ne consomme pas le frontmatter ontologique. | Forte (opérationnelle) |

Ces lacunes **n'autorisent pas** E4 à inventer une nouvelle
métadonnée. Elles sont **documentées comme fait** et renvoyées à
un éventuel ADR futur si elles deviennent bloquantes.

### 6.5 Lien avec E5 et E8

- **E5** doit vérifier que la même rigueur s'applique aux trois
  classes ADR 0055 : `projection`, `candidate`, `working`. Si E5
  trouve qu'une quatrième classe est nécessaire pour absorber
  une lacune documentaire, c'est un drift `F-PERM`.
- **E8** doit confirmer que les cinq vues sont effectivement
  dérivables sur les fixtures réelles de l'expérience D0 → D3.
  Si une vue n'est pas dérivable sans invention, c'est un échec
  partiel à signaler dans le verdict global.

## 7. Contrat observable pour P-1 / C-1 / C-5

E3 §2 a promis qu'un agent P-1 doit pouvoir pointer vers le canon
courant ; C-1 doit naviguer dans le canon ; C-5 doit retrouver la
trace documentaire. Voici ce qu'E4 engage côté canon pour rendre
ces propriétés observables.

### 7.1 P-1 — Canon-awareness

- **Contrat E4** : `docs/CONTEXT.md` reste **un** point d'entrée.
  Il n'est pas modifié par ce run. Le contenu des projections
  `CURRENT_CANON` / `ACTIVE_DECISIONS` est un **complément de
  navigation**, pas un remplacement.
- **Observable** : l'agent qui cite `CONTEXT.md` cite au moins un
  artefact canonique. Si la dérivation est rompue (LAC-DOC-1+),
  c'est une falsif de P-1 côté corpus, **pas** une falsif de
  la définition.
- **Limite assumée** : avec LAC-DOC-1, `CURRENT_CANON` n'est pas
  observable sans projet de tenue documentaire. P-1 reste tenu
  par le pointeur `CONTEXT.md`, pas par la vue.

### 7.2 C-1 — Canon navigation

- **Contrat E4** : la navigation canonique est faisable
  manuellement par lecture des axes ontologiques sur fixtures, et
  manuellement par le pointeur `CONTEXT.md` sur le reste du
  canon. **Pas d'outil dédié** promis par E4. Toute promesse de
  navigation automatique nécessiterait un nouvel outil — c'est
  hors-périmètre et c'est noté en LAC-DOC-6.
- **Mode dégradé acceptable** : C-1-D (E3 §2). Tant que
  `CONTEXT.md` reste joignable, la capacité est **dégradée
  acceptable**.

### 7.3 C-5 — Documentary continuity

- **Contrat E4** : `MEMORY_AND_HANDOFF.md` (officiel, versionné)
  + `docs/runs/<id>/07_CLOSEOUT.md` (officiel, versionné) +
  `docs/SESSION.md` (gitignored) restent les artefacts de
  continuité. E4 ne modifie aucun.
- **Mode dégradé acceptable** : lorsque `docs/SESSION.md`
  gitignored est absent d'une nouvelle session, la continuité
  passe par `docs/CONTEXT.md` + `AUDIT_STATUS.md` (E3 §2).

## 8. Falsifications à porter à `07_FALSIFICATION_MATRIX`

E8 doit observer, sans invention de métadonnées, au minimum les
cas suivants :

| Tag | Scénario | Observation attendue si la définition des vues est correcte |
|---|---|---|
| `F-VIEW-1` (projection technique des cas #1 et #4) | Présenter `art_export_v1.md` et `art_export_v2.md` à un agent : l'agent classe le premier dans `SUPERSEDED` et le second dans `CURRENT_CANON`. | classification correcte sans intervention humaine supplémentaire. |
| `F-VIEW-2` (protection contre F3) | Présenter un document de proposition daté d'hier et un ADR `ACCEPTED` daté d'il y a six mois ; observer la qualification de chaque. | la proposition n'est pas élevée par récence. |
| `F-VIEW-3` (orthogonalité) | Demander à l'agent de donner l'autorité d'une vue (par exemple « qui décide que c'est CURRENT_CANON ? »). | l'agent cite un **axe** (authority, lifecycle), pas la vue elle-même. |
| `F-VIEW-4` (lacune assumée) | Demander à l'agent de citer les 5 vues dans un sous-dossier non-outillé (par exemple un fichier ADR 0030 ancien sans frontmatter). | l'agent ne peut pas dériver automatiquement ; **il qualifie ce qu'il peut observer et signale le reste en UNKNOWN** plutôt que d'inventer. |

`F-VIEW-4` est la falsification la plus importante : elle teste
que la doctrine **n'invente pas** quand elle ne peut pas dériver.

## 9. Handoff vers `05_MEMORY_INTEGRATION_MODEL`

E5 doit recevoir l'arbitrage de R-E3-1 (transféré par §0.1 de
ce livrable) et doit poursuivre les engagements suivants :

1. **Préserver la séparation class / semantic posée en E2 §3** :
   trois classes seulement, sémantique descriptive nullable.
2. **Confirmer la frontière « F6 / architecture cible »**
   (R-E3-1) : rappeler que P-3 = N/A est un scénario de
   dégradation, pas une autorisation d'architecture cible sans
   mémoire.
3. **Tester le candidat `vbbk` au regard des trois classes**, en
   respectant la doctrine ADR 0055, sans inventer de quatrième
   classe.
4. **Documenter l'alignement des projections** sur les trois
   classes : par exemple, comment `seam_check.py` sait lire
   qu'un artefact canon a `subject_key` qui le rend
   `projection`-able.
5. **Reprendre les LAC-DOC-* non résolues ici** sans en faire
   une dépendance bloquante pour E5 : E5 documente celles qui
   touchent à la mémoire, E9 liste celles qui restent ouvertes.

### 9.1 Points de vigilance pour E5

- Si E5 propose une quatrième classe, R-E3-1 doit être réactivée
  **avant** la moindre proposition (c'est un signal de drift
  structurel).
- Si E5 détecte qu'une sémantique **non-canon** est utilisée
  par le kernel `vbbk` comme si elle était autoritaire,
  c'est `F-INVAR` à qualifier en E7/E8.
- Si E5 veut promouvoir `seam_check.py` en
  `tools/vbb-memory-seam-check.py`, c'est un acte de tool
  canonique — il faut vérifier qu'il n'introduit pas d'autorité
  sémantique supplémentaire. La forme POC est déjà neutre ; la
  promotion est **acceptable** tant qu'elle reste dans la ligne
  ADR 0055.

### 9.2 Seuil A

E5 fonctionne en A2 pour toute décision touchant au canon
(classes d'autorité mémoire, projections, falsifications F1–F7).
Il peut fonctionner en A1 pour les protocoles d'expérience et en
A0 pour l'inventaire. Cette répartition est cohérente avec ce
que E3 §0 avait préparé.

## 10. Bornes

- ❌ Aucune nouvelle classe autoritaire (R-E4-1).
- ❌ Aucune promotion automatique d'une sémantique en autorité.
- ❌ Aucune fusion style A / style B des ADRs.
- ❌ Aucun engagement de tenue documentaire (en LAC-DOC-1+, ce
  serait un travail de run séparé).
- ❌ Aucune modification de `docs/document-model/`.
- ❌ Aucune modification de `docs/CONTEXT.md`, `MEMORY_AND_HANDOFF.md`,
  `AUDIT_STATUS.md`.

## 11. Verdict E4

| Champ | Valeur |
|---|---|
| Statut | `READY` |
| `next_phase` | `05_MEMORY_INTEGRATION_MODEL` |
| Résultat expérimental | 5 vues **dérivables en principe** ; **non systématiquement observables** dans le corpus (LAC-DOC-1 à LAC-DOC-6) ; lacunes d'**outillage / tenue**, pas d'autorité |
| Conformité R-E3-1 | ✅ transféré à E5 §0.1 |
| Conformité R-E4-1 | ✅ tests T-NEW-1..4 passés ; aucun nouveau champ autoritaire introduit |
| Hypothèse couverte | H1, par P-1, C-1, C-5 ; LAC-DOC-* documentées comme falsifs potentiels du **mode dégradé**, pas de la définition |
| Pré-requis pour E5 | tous présents : canon ontologique disponible, lacunes assumées, frontière R-E3-1 à arbitrer |
