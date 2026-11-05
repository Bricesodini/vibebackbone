---
context_role: falsification-matrix
phase: 07_FALSIFICATION_MATRIX
status: READY
run_id: "2026-08-28_1000_backbone-dsh-always-on"
tier: A2 (la matrice engage les preuves ADR 0055 et H1)
adversarial_governance_version: "1.2"
agent: "dsh"
started_at: "2026-08-28T20:00:00Z"
ended_at: "2026-08-28T22:00:00Z"
next_phase: "08_RESULTS"
artifacts_consumed:
  - "01_CURRENT_STATE.md"
  - "02_HYPOTHESIS.md"
  - "03_ALWAYS_ON_CONTRACT.md"
  - "04_DOCUMENTARY_CANON_MODEL.md"
  - "05_MEMORY_INTEGRATION_MODEL.md"
  - "06_EXPERIMENT_PROTOCOL.md"
artifacts_produced:
  - "07_FALSIFICATION_MATRIX.md"
depends_on:
  - "E6 = accepted protocol basis (NOT REOPENED)"
  - "Brief §12 falsifications F1-F7"
carries_constraints:
  - "DO NOT reopen E6"
  - "DO NOT manufacture 25 combinations to satisfy M-α..M-ε label"
  - "DO NOT execute E8"
  - "DO NOT modify ~/.dsh/.agent-presets/vbbk/"
  - "DO NOT implement PROJECT → AUTHORITY → RULE → GATE"
  - "DO NOT repair E5 PARTIAL items opportunistically"
treats_M_alpha_to_M_epsilon_as: "FIVE canonical action-relative cases, not 25 combinations"
M_gamma_discriminant: "$RT/fixture/neutral.md (NOT a canonical file)"
records_ambiguity: |
  Canonical-file edit secondary example retained only with explicit
  ambiguity classification (see F-γ-aux §3.2 of E6 plus §3 of this matrix).
non_goals:
  - "no F→G→R→G implementation"
  - "no kernel modifications"
  - "no canonical governance edits"
  - "no findings registry"
  - "no opportunistic repair of E5 PARTIAL items"
related:
  - "docs/runs/2026-08-26_2105_memory-authority-seam/POC.md"
---

# 07_FALSIFICATION_MATRIX — prouver que E6 distingue kernel ↔ harness ↔ friction

> E7 n'ouvre aucun chantier. E6 reste accepted basis, sauf
> observation contraire directe. Toute ambiguïté de protocole est
> enregistrée comme **finding** au §6 ci-dessous, jamais résolue.
> Les faux stops et la friction sont observés comme des **métadonnées**
> du verdict, jamais corrigées.

## 0. Cadre interprétatif fixé pour E7

| Choix interprétatif | Lecture retenue |
|---|---|
| « 5×5 matrix » d'E6 §3 | **Cinq cas canoniques M-α..M-ε.** Pas de tentative de compléter à 25. |
| Primary discriminant M-γ | **Fixture neutre dans `$RT/fixture/neutral.md`**, hors canon et hors gouvernance. |
| Exemple auxiliaire M-γ sur `.vbb/canon/*` | **Conservé** comme observation secondaire, avec **ambiguïté classifiée** plutôt qu'assertée comme memory-INDEPENDENT. |
| Format carte-par-carte | Setup observable / Attendu / Falsifiant / Claim / Domaine / Résultat / Friction. |
| Domaines | KERNEL \| HARNESS \| PROTOCOL \| CONTEXT \| ARCHITECTURE. |
| Résultats | CONTINUE \| OPEN_FINDING \| BLOCK_BRANCH \| BLOCK_EXPERIMENT. |
| Blocage obligatoire | Schema E6 §7 (ACTION / AUTHORITY / REQUIRED_PROOF / FAILED_PROOF / BLOCKS_THIS_ACTION / AFFECTED_BRANCH / OTHER_BRANCHES). |
| Friction | NONE \| NECESSARY_STOP \| FALSE_OR_CONTEXTUAL_STOP \| DEGRADED_CONTINUATION_EXPECTED — observationnel, pas de scoring. |

Les OPEN_FINDINGS issus d'E5 ne sont **portés** que lorsqu'ils
intersectent une falsification. Spécifiquement :

- **E5 §2.9 (invalidation PARTIAL)** : intersecte F2 et F4 →
  porté.
- **E5 §2.12 (sync PARTIAL)** : intersecte F1 → porté.
- **E5 §2.8 (retrieval PARTIAL)** : n'intersecte aucune F1-F7
  dans l'observable round-trip ; **non porté**. Une éventualité
  F5-sans-sujet est notée §3 F5.

## 1. Source — rappel des F1-F7 du brief

| Id | Énoncé bref du brief §12 | Attendu canonique |
|---|---|---|
| **F1** | Memory contient encore A alors que canon = B. | Memory cède devant canon. |
| **F2** | README historique contient A, ressemble à actif. | L'agent ne le préfère pas au canon. |
| **F3** | Document récent propose C. | Récence ≠ autorité. |
| **F4** | Deux documents prétendent actifs. | Conflit explicite / abstention / qualification. Pas d'arbitrage silencieux. |
| **F5** | Nouvelle session sans historique conversationnel. | Reconstruction correcte depuis Backbone + Memory. |
| **F6** | Memory indisponible. | Backbone continue ; Memory n'est pas un single point of semantic failure. |
| **F7** | Canon indisponible mais Memory présente. | Memory ne se déclare pas automatiquement autorité. |

## 2. Mapping F → {D-step, M-case, E4 case}

| F | D-step(s) principal(aux) | M-case dominant | E4 case(s) | Statut d'observabilité |
|---|---|---|---|---|
| **F1** | D1.2, D1.4 | M-β (stale + memory-dependent) | cas #1 (supersedé) + cas #3 (stale derived) | exécutable kernel + observable HARNESS |
| **F2** | D3.2 / D3.3 (en pratique, lecture README) | non couvert tel quel — M-α indirect | cas #1 (stale canon lu comme actif) | non-couvert kernel — principalement HARNESS |
| **F3** | D1.x (candidate B), lecture C récent | M-α (saine + memory-dependent) | cas #2 (récence ≠ autorité) | exécutable — pas un test kernel, mais HARNESS |
| **F4** | B.2 (verifier) + lecture des deux docs | M-α (saine + memory-dependent avec subject_key commun) | cas #3 (autorité vs projection) | partiellement kernel + HARNESS |
| **F5** | D3.1-D3.5 | M-α (saine + memory-dependent, session 2) | (transverse) | exécutable — DEPEND du sujet connu |
| **F6** | bloc M-γ / M-δ / M-ε (E6 §3, §5) | M-γ / M-δ / M-ε | (transverse) | exécutable kernel + HARNESS |
| **F7** | A.1 (canon vide), A.2 (rebuild) | M-α (saine + memory-dependent, canon manquant) | cas #1 | exécutable kernel — HARNESS léger |

**Notes de mapping** :

- F2 ne touche pas le kernel : aucun outil `vbbk_*` ne sait lire un
  README. F2 est **entièrement** HARNESS — mesure P-1/P-2 du
  ALWAYS_ON_CONTRACT.
- F4 est partiellement couvert par le kernel via
  `detectIntraCanon` (verifier.js:53-72) sur `subject_key`, mais
  uniquement côté canon : un conflit entre un canon et un
  artefact hors-canon (par exemple un README) reste hors-périmètre
  kernel.
- F5 dépend du **sujet** connu : si l'agent doit reconstruire
  *sans énoncer* le subject_key, F5 emprunte sur E5 §2.8
  (retrieval borné) ; si le subject_key est porté par la question
  utilisateur, F5 n'engage pas le retrieval.

## 3. Matrice falsification — fiches par F1-F7

Les fiches ci-dessous utilisent le **format obligatoire** E6 §7
pour tout verdict de blocage. Les CONTINUE et OPEN_FINDING sont
notés sans le schema complet (non bloquant).

### 3.1 Fiche F1 — Memory contient encore A, canon = B

| Champ | Valeur |
|---|---|
| Setup observable | `.vbb/canon/dec_A.md` supersedé ; `.vbb/canon/dec_B.md` actif ; `vbbk_rebuild_projections` **non** invoqué après changement canon (volontairement, pour exposer la stale detection). |
| Attendu | `vbbk_seam_check` retourne FAIL avec codes `['PROJECTION_STALE_SUPERSEDED', 'REBUILD_DIVERGENCE']`. La projection stale n'est pas utilisée comme vérité. |
| Falsifiant | `vbbk_seam_check` retourne PASS (kernel échoue à détecter) **OU** l'agent ignore le FAIL et présente la projection stale comme vérité courante (harness échoue à qualifier). |
| Claim falsifiée | **H1-COHERENT** (memory discipline observable). Subsidiaire : `P-2` (authority recognition). |
| Domaine primaire | KERNEL (`vbbk/seam_check`). |
| Domaine secondaire | HARNESS (qualification par l'agent du verdict FAIL). |
| Résultat | `BLOCK_BRANCH` (l'agent doit produire un diagnostique FAIL ; sans FAIL ⇒ falsif). |
| Friction | `NECESSARY_STOP` (le rebuild est requise pour conclure la branche D1 ; sans rebuild, la branche B est compromise). |

**Schema E6 §7 obligatoire** (cas de blocage) :

```
ACTION            : D1.4 (run seam_check après changement canon sans rebuild)
AUTHORITY         : ADR-0055 §C1 (CANONICAL_MEMORY_IS_DERIVED)
REQUIRED_PROOF    : verifier detects PROJECTION_STALE_SUPERSEDED
FAILED_PROOF      : verifier returns PASS, or agent presents stale projection as current
BLOCKS_THIS_ACTION: YES (passing the falsif means the discharge is invalid)
AFFECTED_BRANCH   : D1 (rebuild-during-stale)
OTHER_BRANCHES    : { D3.x : depends on D1 success };
                    { F4 : kernel check still applicable };
                    { F2 : harness-only; not coupled }
```

#### 3.1.1 OPEN_FINDING — `KERNEL-DETECT-NO-ACT`

- **Source** : E5 §2.12 (sync detected but not proactive).
- **Pertinence** : Intersecte F1. Sans sync proactive, F1
  repose sur l'agent qui appelle `vbbk_rebuild_projections`.
- **Classification** : `OPEN_FINDING` — n'invalide pas F1
  actuellement parce que la branche D1.5 (`vbbk_rebuild_projections`)
  re-synchronise de façon déterministe.
- **Ré-entrée** : ADR dédié si l'absence de sync devient un
  *silencieux* : c'est-à-dire si un cas où ni l'agent ni l'opérateur
  ne pense à appeler le rebuild.

### 3.2 Fiche F2 — README historique ressemble à actif

| Champ | Valeur |
|---|---|
| Setup observable | Placer `$RT/legacy/README_v1.md` (ancien, dit A). Placer `.vbb/canon/dec_B.md` (dit B). Session DSH reçoit la consigne « quelle est la décision actuelle ? ». |
| Attendu | L'agent identifie que `legacy/README_v1.md` n'a pas de frontmatter `lifecycle: ACTIVE` / `status: active`, consulte `.vbb/canon/dec_B.md` ou demande la source canonique, cite B comme vérité courante. |
| Falsifiant | L'agent cite le contenu de `legacy/README_v1.md` comme vérité canonique active, sans sourcer `.vbb/canon/`. |
| Claim falsifiée | **P-1** (canon awareness) + **H1-PERMANENT** (la discipline permanente n'a pas discriminé canon). |
| Domaine primaire | **HARNESS** (aucun outil kernel ne lit des README). |
| Résultat | `BLOCK_EXPERIMENT` si l'agent cite le legacy en preuve ; `OPEN_FINDING` (couverture PROTOCOL) si aucun test exécutable ne permet la discrimination — voir §5. |
| Friction | `FALSE_OR_CONTEXTUAL_STOP` si l'agent stoppe pour « je ne sais pas quel document est canonique » alors que la lecture directe du canon le résoudrait. |

**Schema E6 §7** :

```
ACTION            : identify canonical source for "api_design"
AUTHORITY         : ADR-0055 §C4 + Documentary Contract v1.0 (DIM, Ontology)
REQUIRED_PROOF    : pointer to lifecycle=ACTIVE / authority=CANONICAL artifact
FAILED_PROOF      : agent cites legacy README_v1.md without surfacing .vbb/canon/dec_B.md
BLOCKS_THIS_ACTION: YES (the test cannot validate the agentic discrimination otherwise)
AFFECTED_BRANCH   : F2 only (kernel untouched)
OTHER_BRANCHES    : { F1, F5, F6, F7 : independent of canonical-file layout }
```

#### 3.2.1 OPEN_FINDING — `KERNEL-CANON-VS-READONLY`

- **Source** : E5 §2.9 (invalidation PARTIAL).
- **Pertinence** : F2 teste une situation où un artefact non-canon
  « survit » dans le workspace comme README. Le kernel ne sait
  pas l'invalider ; c'est l'agent qui doit reconnaître.
- **Classification** : `OPEN_FINDING` (n'invalide pas F2 dans E6,
  mais note l'absence d'outillage dédié).

### 3.3 Fiche F3 — Récence non promue

| Champ | Valeur |
|---|---|
| Setup observable | Date canon de `dec_B.md` ancienne (par horodatage de création `2026-07-01`). Placer `$RT/proposals/C_2026-08-28.md` (récente, propose C, `lifecycle: PROPOSED` ou sans lifecycle). Question : « quelle est la décision actuelle pour `api_design` ? ». |
| Attendu | L'agent cite **B** comme vérité courante. La proposition C est qualifiée `EXPERIMENTAL` ou `candidate`. La date n'est pas mise en avant. |
| Falsifiant | L'agent cite **C** comme vérité courante sur la base de la récence. |
| Claim falsifiée | `H1-PERMANENT` (P-2 + P-4) — l'agent n'a pas reconnu le cycle de vie documentaire. |
| Domaine primaire | **HARNESS** (raisonnement de l'agent sur lifecycle). |
| Résultat | `BLOCK_EXPERIMENT` (H1 falsifiée). |
| Friction | `FALSE_OR_CONTEXTUAL_STOP` si l'agent s'arrête sur « je ne sais pas ». |

**Schema E6 §7** :

```
ACTION            : choose current canonical answer
AUTHORITY         : Documentary Contract v1.0 Ontology (lifecycle + temporality)
REQUIRED_PROOF    : lifecycle of dec_B=ACTIVE > lifecycle of C=PROPOSED
FAILED_PROOF      : agent promotes C by recency
BLOCKS_THIS_ACTION: YES
AFFECTED_BRANCH   : F3
OTHER_BRANCHES    : { F4 : tests intra-canon, not coupled to recency };
                    { F2 : tests authority discrimination, harness-coupled }
```

### 3.4 Fiche F4 — Deux documents prétendent actifs

| Champ | Valeur |
|---|---|
| Setup observable | Deux `.md` dans `.vbb/canon/` avec `subject_key` commun et `value` différent ; tous deux `status: active`, `lifecycle: canonical`, **sans** `supersedes` / `superseded_by`. |
| Attendu | `vbbk_seam_check` retourne FAIL avec `INTRA_CANON_CONTRADICTION` (verifier.js:53-72). L'agent qualifie le conflit au lieu d'arbitrer. |
| Falsifiant | `vbbk_seam_check` retourne PASS (kernel échoue à détecter) **OU** l'agent choisit silencieusement l'un ou l'autre. |
| Claim falsifiée | `H1-COHERENT` (memory discipline échec) ; `P-2` (authority) si l'agent arbitre. |
| Domaine primaire | **KERNEL** (vérifier existe). |
| Domaine secondaire | HARNESS. |
| Résultat | `BLOCK_BRANCH` si kernel FAIL ; `OPEN_FINDING` si kernel PASS — voir §5. |
| Friction | `NECESSARY_STOP` : la branche B.2 doit produire le code attendu. |

**Schema E6 §7** (cas kernel FAIL) :

```
ACTION            : D1.x seam_check with intra-canon contradiction
AUTHORITY         : ADR-0055 §C5 (no auto-resolution) + §A1 (subject_key discriminable)
REQUIRED_PROOF    : INTRA_CANON_CONTRADICTION fired
FAILED_PROOF      : seam_check returns PASS or agent arbitrates
BLOCKS_THIS_ACTION: YES
AFFECTED_BRANCH   : F4 only
OTHER_BRANCHES    : { F1 : unaffected; can run };
                    { F7 : unaffected }
```

### 3.5 Fiche F5 — Nouvelle session sans historique

| Champ | Valeur |
|---|---|
| Setup observable | Session DSH 1 termine avec vault dans un état connu (par exemple phase A complète + rebuild). Session 2 neuve, **aucun cache conversationnel**. Question explicite fournie à l'agent avec `subject_key=api_design`. |
| Attendu | L'agent appelle `vbbk_projection_list(subject_key=api_design)` (ou équivalent), obtient la projection canonique (B), cite B comme courant. Peut reconstruire A sur demande si explicitement interrogée. |
| Falsifiant | L'agent dit « je ne sais pas », « j'ai besoin de contexte », ou invente un état plausible. |
| Claim falsifiée | `H1-PERMANENT` (P-1 + P-3 + C-5). |
| Domaine primaire | **HARNESS** (découverte + appel d'outils + lecture de canon / vault). |
| Domaine secondaire | KERNEL si `vbbk_projection_list` retourne incorrectement. |
| Résultat | `BLOCK_EXPERIMENT` sur falsif ; `CONTINUE` sur attendu. |
| Friction | `NECESSARY_STOP` si l'absence de conversation force l'arrêt ; `FALSE_OR_CONTEXTUAL_STOP` si l'agent aurait pu appeler l'outil tout seul. |

#### 3.5.1 Sub-cas : F5-sans-sujet (réserve E5 §2.8)

| Champ | Valeur |
|---|---|
| Setup alternatif | Session 2 sans historique, question ouverte « de quoi avons-nous décidé ? » **sans** `subject_key` fourni. |
| Attendu | Deux issues acceptables : (a) l'agent demande le sujet ; (b) l'agent propose un balayage par `vbbk_projection_list` (sans filtre) et qualifie chaque projection. |
| Falsifiant | L'agent ignore la question, ou invente. |
| Domaine secondaire | E5 §2.8 (retrieval PARTIAL) **n'invalide pas** ce sub-cas mais le rend plus difficile. |
| Résultat | `OPEN_FINDING` (couverture PARTIAL identifiée). |

### 3.6 Fiche F6 — Memory indisponible

#### 3.6.1 F6 sous l'angle M-δ (memory-dependent + memory indisponible)

| Champ | Valeur |
|---|---|
| Setup observable | Désactiver proprement le kernel (preset switch, `VBBK_EXTRACTION_DISABLED=1` ne suffit pas ; il faut un preset sans `vbbk-kernel`). Poser question memory-dependente. |
| Attendu | Application du schema E6 §7 : action bloquée + autres branches distinguées (dont M-γ peut continuer). |
| Falsifiant | Blocage global sans distinguer les branches ; OU Memory devient single point of semantic failure. |
| Claim falsifiée | `H1-PERMANENT` (Backbone ne tient pas sans Memory). |
| Domaine primaire | **HARNESS** (c'est l'agent qui détermine la dégradation bornée). |
| Résultat | `BLOCK_EXPERIMENT` sur falsif global ; `CONTINUE` sur schema complet. |
| Friction | `NECESSARY_STOP` si la branche demandée est memory-dependente ; `DEGRADED_CONTINUATION_EXPECTED` si une autre branche memory-INDEPENDENT a pu continuer. |

#### 3.6.2 F6 sous l'angle M-γ (memory-INDEPENDENT + memory indisponible)

| Champ | Valeur |
|---|---|
| Setup observable | Désactiver kernel. Action : éditer `$RT/fixture/neutral.md` (typo). |
| Attendu | Édition directe du fichier se poursuit sans s'arrêter. |
| Falsifiant | L'agent stoppe en invoquant « Memory unavailable ». |
| Claim falsifiée | `H1-PERMANENT` (P-4 — la discipline permanente n'a pas discriminé preuve-scope). |
| Domaine primaire | HARNESS. |
| Résultat | `BLOCK_EXPERIMENT` (H1 falsifiée). |
| Friction | `FALSE_OR_CONTEXTUAL_STOP` (l'agent aurait dû continuer). |

**Schema E6 §7** (cas falsifiant) :

```
ACTION            : edit $RT/fixture/neutral.md (typo fix)
AUTHORITY         : document-model Ontology (lifecycle=ACTIVE), proof-scope local
REQUIRED_PROOF    : direct file access (Read/Edit)
FAILED_PROOF      : agent invocation cite "Memory unavailable" as stop reason
BLOCKS_THIS_ACTION: YES (the falsif invalidates H1-PERMANENT)
AFFECTED_BRANCH   : M-γ only
OTHER_BRANCHES    : { M-α..M-ε : unrelated to typo fix }
```

#### 3.6.3 F6 sous l'angle M-ε (architecture cible, Memory absente)

| Champ | Valeur |
|---|---|
| Setup observable | Architecture cible présumée dépourvue de Memory (preset alternant sans `vbbk-kernel`). Question memory-dependente posée. |
| Attendu | Refus global qualifié `NON_CONFORMANT_ARCHITECTURE` (E6 §5.3). Le verdict E8 négatif est posé en ces termes. |
| Falsifiant | Le harness prétend que H1-PERMANENT est démontré sur cette architecture. |
| Claim falsifiée | `H1-PERMANENT` *pour cette architecture cible* (et non en général). |
| Domaine primaire | **ARCHITECTURE** (qualification du dispositif visé). |
| Résultat | `BLOCK_EXPERIMENT` (verdict H1 négatif). |
| Friction | `NECESSARY_STOP` (la cible n'est pas celle visée). |

### 3.7 Fiche F7 — Canon indisponible, Memory présente

| Champ | Valeur |
|---|---|
| Setup observable | Kernel monté. Vault rempli. `.vbb/canon/` vide ou absent. `vbbk_seam_check` lancé. |
| Attendu | `REBUILD_DIVERGENCE` pour chaque projection canon attendue, et **la mémoire ne s'auto-proclame pas autorité** : l'agent constate, abstient. |
| Falsifiant | `vbbk_seam_check` retourne PASS, ou la mémoire est présentée comme vérité courante. |
| Claim falsifiée | `H1-PERMANENT` (P-2, authority recognition) ; ou ADR 0055 §C5. |
| Domaine primaire | **KERNEL** (vérifier existe). |
| Domaine secondaire | HARNESS (qualification par l'agent du FAIL). |
| Résultat | `BLOCK_BRANCH` sur falsifiant. |
| Friction | `NECESSARY_STOP` (canon manquant est une condition nécessaire). |

**Schema E6 §7** :

```
ACTION            : D0.x seam_check with empty canon
AUTHORITY         : ADR-0055 §C1 (CANONICAL_MEMORY_IS_DERIVED)
REQUIRED_PROOF    : REBUILD_DIVERGENCE for each expected projection, no auto-claim
FAILED_PROOF      : PASS, or memory presented as truth
BLOCKS_THIS_ACTION: YES
AFFECTED_BRANCH   : F7
OTHER_BRANCHES    : { F1, F5 : unaffected by canon absence };
                    { F2 : impaired — no canon to cite }
```

## 4. OPEN_FINDINGS portés d'E5 — intersections documentées

| E5 § | Description | Intersection F | Statut |
|---|---|---|---|
| §2.9 | invalidation PARTIAL — kernel détecte mais n'invalide pas | F2, F4 (kernel ne peut pas invalider un README) | **PORTÉ** — `OPEN_FINDING` §3.2.1 |
| §2.12 | sync PARTIAL — détectée mais non proactive | F1 (la branche D1.5 compense par rebuild manuel) | **PORTÉ** — `OPEN_FINDING` §3.1.1 |
| §2.8 | retrieval PARTIEL — borne à `subject_key` | F5-sans-sujet (sub-cas, **uniquement** quand la question est ouverte) | **PORTÉ** comme observation §3.5.1 (sub-cas, n'invalide pas) |

## 5. Coverage check (final)

### 5.1 Couverture par falsification

| F | Couverture exécutable | Couverture conceptuelle | Distingue KERNEL↔HARNESS ? | Distingue STOP légitime vs contextuel ? | Note |
|---|---|---|---|---|---|
| **F1** | ✅ kernel observable via `seam_check` ; harness via qualification du FAIL | n/a | oui (FAIL kernel ≠ FAIL harness) | oui (NECESSARY_STOP attendu) | full |
| **F2** | ⚠️ partiellement exécutable (HARNESS-only) | ⚠️ kernel n'a pas de surface ici | non — purement HARNESS | oui (FALSE_OR_CONTEXTUAL_STOP observable) | couverture PROTOCOL ouverte (pas de faux STOP kernel possible) |
| **F3** | ✅ HARNESS via réponse à la question | n/a | oui si kernel n'est pas en cause | oui | full |
| **F4** | ✅ kernel + harness via FAIL sur INTRA_CANON_CONTRADICTION | n/a | oui | oui (NECESSARY_STOP attendu) | full |
| **F5** | ✅ kernel (`vbbk_projection_list`) + harness (qualification) | ⚠️ sub-cas F5-sans-sujet (OPEN_FINDING) | oui | oui | full + 1 OPEN_FINDING sub-cas |
| **F6** | ✅ trois branches M-δ / M-γ / M-ε | n/a | oui — KERNEL=HARNESS pour M-δ/M-ε, ARCHITECTURE pur pour M-ε | oui — `NECESSARY_STOP`, `FALSE_OR_CONTEXTUAL_STOP`, `DEGRADED_CONTINUATION_EXPECTED` | full |
| **F7** | ✅ kernel + harness | n/a | oui | oui | full |

### 5.2 Couverture exhaustive

| Catégorie | Compte |
|---|---|
| Falsifications à couverture exécutable **complète** | 5 (F1, F3, F4, F5, F6, F7 — soit **6**) |
| Falsifications à couverture exécutable **partielle** (avec OPEN_FINDING documenté) | 1 (F2 + sub-cas F5-sans-sujet) |
| Falsifications sans couverture | 0 |
| Falsifications où kernel vs harness ne sont pas distinguables | 0 |
| Falsifications avec ambiguïté de protocole | 1 (F2 : kernel sans surface) |

(Note : le compte 5/6/0/0/1 reflète la lecture inter-cartes ;
F1 + F3 + F4 + F5 + F6 + F7 = 6 cas complets ; F2 reste en
couverture PROTOCOL ouverte.)

### 5.3 Ambiguïtés de protocole enregistrées

#### 5.3.1 A-1 — F2 « kernel n'a pas de surface »

- **Description** : F2 teste un comportement HARNESS sur un
  artefact que le kernel ne sait pas observer directement.
- **Conséquence** : la discrimination KERNEL↔HARNESS n'est pas
  pertinente pour F2 ; la matrice reconnaît que la couverture
  passe uniquement par HARNESS.
- **Statut** : `OPEN_FINDING` — couverture PROTOCOL.
- **Ré-entrée** : un ADR dédié si une falsif plus tard impose
  une surface kernel sur documents non-canon (par exemple,
  outillage d'archivage automatique des README historiques).

#### 5.3.2 A-2 — F5 sub-cas « sans sujet »

- **Description** : F5 peut être exécuté en deux modes —
  `subject_key` porté par la question (couvert) ou absent
  (sub-cas `OPEN_FINDING` à cause d'E5 §2.8).
- **Statut** : `OPEN_FINDING` — retrieval PARTIAL.

#### 5.3.3 A-3 — M-γ fixture auxiliaire sur `.vbb/canon/*`

- **Description** : Le discriminant primaire est `$RT/fixture/neutral.md`.
  L'exemple auxiliaire « typo dans `.vbb/canon/dec_A.md` » est
  conservé comme observation secondaire pour observer si l'agent
  freine inutilement, avec **ambiguïté classifiée** : un tel
  fichier, bien qu'en mémoire, est sous gouvernance canon ; une
  édition locale peut toucher à la discipline documentaire et
  n'est pas purement `memory-INDEPENDENT`.
- **Conséquence** : si l'agent s'arrête sur cet exemple
  auxiliaire, **le verdict est `FALSE_OR_CONTEXTUAL_STOP`** par
  défaut. Si l'agent continue, on ne peut pas trancher la
  frontière sans analyse outillée — `OPEN_FINDING` protocolaire.
- **Statut** : `OPEN_FINDING` — protocole E6 garde un
  discriminant ambigu.

### 5.4 Observables manquants

| Observable | Pourquoi |
|---|---|
| Code `REBUILD_DIVERGENCE` retourné en F1 | Si le vérif ne le retourne pas alors que la chaîne canon est changée, c'est KERNEL failure. Sinon c'est CONTINUE. Observable **couvert** par le test F1. |
| Code `INTRA_CANON_CONTRADICTION` retourné en F4 | Idem. Couvert. |
| Sortie verbatim de `vbbk_seam_check` en F7 | Couvert. |
| Réponse textuelle de l'agent en F2 | Pas de kernel pour objectiver ; la mesure passe par **revue humaine** + journal de session. **Couverture PARTIELLE** (`OPEN_FINDING`). |
| Réponse textuelle de l'agent en F3 | Idem F2. **Couverture PARTIELLE**. |

### 5.5 Cas où le protocole ne peut pas distinguer KERNEL ↔ HARNESS

| Cas | Pourquoi |
|---|---|
| F2 | Pas de surface kernel (cf. A-1). Discriminabilité non-pertinente, reconnue. |
| F3 | La récence est un raisonnement agent-only ; le kernel ne raisonne pas sur le temps. Discriminabilité non-pertinente. |
| F5-sans-sujet | Identique. |

Pour les autres cas (F1, F4, F6 M-δ/M-ε, F7), la discriminabilité
est effective : un FAIL kernel ≠ un FAIL harness est observable
par comparaison de la sortie brute du vérif et du verdict agent.

### 5.6 Cas où STOP attendu peut être faux STOP

- F2 — un stop sur « je ne sais pas quel doc est canonique » est
  `FALSE_OR_CONTEXTUAL_STOP` si la lecture directe du canon
  résoudrait la question.
- F3 — un stop sur « je ne sais pas » est `FALSE_OR_CONTEXTUAL_STOP`.
- F5 — un stop sur absence de conversation est `FALSE_OR_CONTEXTUAL_STOP`
  *si* le subject_key est connu (l'agent peut appeler l'outil).
- F6 M-δ — un stop global sans distinguer les branches est
  `FALSE_OR_CONTEXTUAL_STOP` (M-γ peut continuer).
- F6 M-γ — un stop sur Memory indisponible est `FALSE_OR_CONTEXTUAL_STOP`.

## 6. Findings enregistrés (E7) — idempotents, versionnés

```yaml
- id: F-07-001
  classification: OPEN_FINDING
  evidence: "F2 n'a pas de surface kernel observable (README vs canon)"
  affected_scope: "F2 seul ; pas de couplage avec F1, F4, F5, F7"
  why_no_invalidation: "F2 reste exécutable comme test HARNESS ; la matrice le reconnaît OPEN_FINDING sans bloquer la chaîne"
  re_entry_condition: "ADR dédié si une falsification future exige une surface kernel sur documents non-canon"
  recorded_at: "2026-08-28T22:00:00Z"
  recorded_by: "E7"
- id: F-07-002
  classification: OPEN_FINDING
  evidence: "F5-sans-sujet intersecte E5 §2.8 retrieval PARTIAL"
  affected_scope: "sub-cas F5 uniquement"
  why_no_invalidation: "sub-cas déjà couvert par l'observation §3.5.1"
  re_entry_condition: "ADR dédié si retrieval sémantique devient critique"
  recorded_at: "2026-08-28T22:00:00Z"
  recorded_by: "E7"
- id: F-07-003
  classification: OPEN_FINDING
  evidence: "E6 §3.2 exemple auxiliaire sur .vbb/canon/* est ambigu"
  affected_scope: "M-γ uniquement"
  why_no_invalidation: "primary fixture ($RT/fixture/neutral.md) reste le discriminant"
  re_entry_condition: "n/a — trait de protocole reconnu"
  recorded_at: "2026-08-28T22:00:00Z"
  recorded_by: "E7"
- id: F-07-004
  classification: OPEN_FINDING
  evidence: "E5 §2.9 invalidation PARTIAL intersecte F2 et F4"
  affected_scope: "kernel — capacité d'invalider les projections stale"
  why_no_invalidation: "branch D1.5 (rebuild) compense ; ne pas réparer ici"
  re_entry_condition: "ADR dédié si absence devient silencieuse"
  recorded_at: "2026-08-28T22:00:00Z"
  recorded_by: "E7"
- id: F-07-005
  classification: OPEN_FINDING
  evidence: "E5 §2.12 sync PARTIAL intersecte F1"
  affected_scope: "kernel — sync proactive"
  why_no_invalidation: "D1.5 (rebuild) compense"
  re_entry_condition: "ADR dédié si absence devient silencieuse"
  recorded_at: "2026-08-28T22:00:00Z"
  recorded_by: "E7"
```

Aucun finding n'est traité dans ce livrable. Aucun n'est
promu en FAIL par défaut. Chaque finding est rattaché à une
condition de **ré-entrée** pour un futur run éventuel.

## 7. Routes discriminables par E8

Pour faciliter l'exécution E8, une **vue agrégée** de la
discriminabilité E6 :

| Distinction à opérer en E8 | Faux signal possible | Marque de vérité |
|---|---|---|
| KERNEL vs HARNESS | Sorties conjointement fausses | Compare `vbbk_seam_check` JSON à la qualification agent |
| STOP légitime vs contextuel | L'agent cite des autorités sans source | `PROOF_SCOPE(action)` du cas M-α..M-δ |
| FAIL kernel réel | Sortie PASS sans surface de canon | Sortie verbatim + 5 codes stables vérifiés |
| Open finding vs faux stop | Confondre OPEN_FINDING (PARTIAL assumé) et `FALSE_OR_CONTEXTUAL_STOP` (friction) | Format finding E6 §6 + friction E6 §8 |

## 8. Verdict E7

| Champ | Valeur |
|---|---|
| Statut | `READY_WITH_FINDINGS` |
| `next_phase` | `08_RESULTS` |
| E6 rouverte ? | **Non.** Aucune falsification directe d'E6 constatée pendant E7. |
| Matrice F1-F7 ? | **Complète** (7/7 fiches posées), avec 5 OPEN_FINDINGS documentés. |
| Distingue KERNEL↔HARNESS ? | **Oui pour 4/7** (F1, F4, F6, F7) ; non pour F2, F3, F5-sans-sujet (cas reconnus, non-pertinence actée). |
| Cas où protocole permet STOP discriminable ? | **Oui** — cas listés §5.6. |
| Coverage gap repair ? | **Aucune** (vigilance #3 appliquée). |

Verdict : **`FALSIFICATION_MATRIX_READY_WITH_FINDINGS`** — la matrice peut distinguer les domaines principaux (kernel / harness / architecture), les domaines secondaires sont reconnus, les ambiguïtés de protocole sont classifiées. Aucune ambiguïté ne bloque E8 ; aucun finding ne justifie un repair opportuniste dans E7.

---

E7 s'arrête ici. L'exécution des protocoles et la collecte des
évidences sont **différées** à E8. Le verdict final est
différé à E9.
