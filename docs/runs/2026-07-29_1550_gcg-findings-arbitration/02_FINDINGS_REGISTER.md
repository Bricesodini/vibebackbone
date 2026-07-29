---
run_id: "2026-07-29_1550_gcg-findings-arbitration"
phase: "02_FINDINGS_REGISTER"
voie: "STRUCTUREE"
status: "PARTIAL"
kind: "GOVERNANCE_FINDINGS_ARBITRATION"
agent: "claude-opus-5 (Claude Code)"
started_at: "2026-07-29T13:50:00Z"
ended_at: null
artifacts_produced:
  - "02_FINDINGS_REGISTER.md (this file)"
---

# 02_FINDINGS_REGISTER — GCG-ARB-01

Registre unique des constats du chantier *Governance Compatibility Gate*.
**36 entrées en périmètre d'arbitrage**, **6 entrées portées** (hors arbitrage
de ce run). Aucune entrée n'est fusionnée avec une autre de nature différente ;
aucune n'est rétrogradée.

> **Révision après revue indépendante** (`04_INDEPENDENT_ARBITRATION_REVIEW.md`).
> GCG-36 ajouté (P0, quatrième voie de blanchiment) ; GCG-22 réécrit et sa
> correction **inversée** ; GCG-28 monté à `CONFIRMED` sur le fait ; GCG-10
> réécrit, son explication d'origine réfutée ; dénominateur des closeouts
> corrigé de 164 à 157. Les énoncés réfutés sont conservés en citation, pas
> effacés.

## 1. Espace d'identifiants

Les quatre sources utilisent des numérotations qui se recouvrent. `IR-F8`
(inclusivité de borne) et `AUD-F8` (provenance temporelle) sont deux constats
différents portant le même nom. Le registre renumérote dans un espace unique
`GCG-nn`, et conserve l'identifiant d'origine dans le champ *source*.

| Préfixe source | Origine |
|---|---|
| `ST-Sn` | `docs/runs/2026-07-29_1130_gcg-genericity-stress-test/02_STRESS_TEST.md` §5 |
| `IR-Fn` | première revue indépendante du 2026-07-29, agent isolé (F1–F12) |
| `RA-Fx` | revue indépendante **de l'arbitrage** (F-A … F-K), `04_INDEPENDENT_ARBITRATION_REVIEW.md` |
| `R1021` | `docs/runs/2026-07-29_1021_adversarial-gate-population/` (matrice §3, points ouverts) |
| `R1050` | `docs/runs/2026-07-29_1050_gcg-conceptual-model/07_CLOSEOUT.md` §Points ouverts |
| `AUD-Fn` | `docs/AUDIT_STATUS.md` §Active risks |
| `ARB` | constat né dans ce run |

## 2. Baseline de mesure

Toutes les preuves ci-dessous sont reproductibles à la branche
`feat/governance-compatibility-gate`, commit `5d4fe34`, dépôt non modifié.

```
python tools/vbb-governance-compat.py --json
→ population_total 164 · applicable 15 · current_conformance 2/15
  HISTORICAL_VALID 148 · CURRENT_NONCOMPLIANCE 8 · UNKNOWN 4
  CURRENT 2 · OVERCLAIM 1 · PENDING_LIFECYCLE 1
  historical_debt 0 · certification NOT_DERIVABLE_FROM_THIS_GATE · verdict FAIL
```

## 3. Taxonomie employée — et où elle ne discrimine pas

La taxonomie proposée est employée telle quelle pour 31 entrées sur 35. Elle
échoue sur quatre, et l'échec est instructif :

- **GCG-01** est simultanément `MODEL_FLAW` (le modèle admet un prédicat
  indécidable) et `EVIDENCE_DEFECT` (la population le viole). Le registre le
  **scinde** en GCG-01 et GCG-21 parce que les deux moitiés se réparent à des
  endroits différents — l'une dans le modèle, l'autre dans le dépôt.
- **GCG-04**, **GCG-05**, **GCG-06** sont chacun à la fois `MODEL_FLAW` et
  `OPEN_NORMATIVE_DECISION` : le texte du modèle *autorise* la voie de
  blanchiment, donc la corriger exige de trancher ce que le modèle voulait dire,
  pas de corriger un écart au modèle.

Ce que la taxonomie ne dit pas et qui décide de tout, c'est **qui peut clore**.
Le registre ajoute donc un second axe, `closure_authority` :

| Valeur | Signification |
|---|---|
| `AGENT` | un agent peut clore seul : la règle existe déjà **et** aucune décision ouverte ne conditionne la correction |
| `AGENT_BLOCKED` | l'exécution est mécanique, mais **subordonnée à une décision ouverte** — l'agent tape, il ne décide pas |
| `CANON_CHANGE` | exige une modification d'un document canonique |
| `HUMAN_DECISION` | exige un choix de gouvernance qu'aucun agent n'a autorité pour rendre |
| `EXTERNAL_ACTOR` | exige un acteur réellement distinct |

> **Corrigé après revue (RA-F-H).** La version initiale n'avait pas
> `AGENT_BLOCKED` et affirmait : *« C'est cet axe, et non la nature, qui
> structure `03` »*. C'était faux dans les deux sens — `03` est structuré par
> les décisions D0–D7, et cinq des sept entrées `AGENT` étaient en réalité
> subordonnées à une décision. L'axe confondait **qui exécute** et **qui
> décide**, c'est-à-dire précisément la distinction qu'il devait porter.

## 4. Table de synthèse

| ID | Nature | Grav. | Conf. | Autorité | Source | Résumé |
|---|---|---|---|---|---|---|
| GCG-01 | MODEL_FLAW | P0 | CONFIRMED | HUMAN_DECISION | IR-F1 | `immutable` est un booléen déclaré, indécidable par le modèle |
| GCG-02 | MODEL_FLAW | P0 | CONFIRMED | HUMAN_DECISION | IR-F3 | la coordonnée de l'artefact est un label choisi par son auteur |
| GCG-03 | MODEL_FLAW | P1 | CONFIRMED | CANON_CHANGE | IR-F7 | la table des catégories n'est pas totale sous l'union §3.4 |
| GCG-04 | MODEL_FLAW | P1 | CONFIRMED | HUMAN_DECISION | IR-F2 | le ledger peut attribuer une disposition **non-dette** dans la fenêtre |
| GCG-05 | MODEL_FLAW | P1 | CONFIRMED | HUMAN_DECISION | IR-F5 | `PENDING_LIFECYCLE` est défini sur une absence provocable |
| GCG-06 | MODEL_FLAW | P1 | CONFIRMED | CANON_CHANGE | IR-F6 | les deux prédicats d'`OVERCLAIM` sont choisis par le scanner |
| GCG-07 | MODEL_FLAW | P2 | CONFIRMED | CANON_CHANGE | IR-F6 | l'exemple G3 de §4.2 contredit la fixture `NO_BLOCK` |
| GCG-08 | MODEL_FLAW | P2 | CONFIRMED | CANON_CHANGE | IR-F8 | inclusivité des bornes non déclarée ; I10 unifie deux directions opposées |
| GCG-09 | CANON_CONFLICT | P1 | CONFIRMED | CANON_CHANGE | IR-F4 | `enforcement_effective_from` déclaré nulle part ; I8 violé en direct |
| GCG-10 | CANON_CONFLICT | P2 | CONFIRMED | CANON_CHANGE | IR-F7 · ST-S2 | deux horloges : applicabilité par `started_at`, position par identité |
| GCG-11 | CANON_CONFLICT | P1 | CONFIRMED | HUMAN_DECISION | IR-F11 | vocabulaire parallèle avec la partition `certification_status` |
| GCG-12 | CANON_CONFLICT | P2 | CONFIRMED | AGENT_BLOCKED | ST-S8 | constantes de cutover dupliquées entre deux outils |
| GCG-13 | CANON_CONFLICT | P2 | CONFIRMED | CANON_CHANGE | IR-F3 | le modèle ne cite ni `TEMPORAL_PROVENANCE.md` ni `AUD-F8` |
| GCG-14 | SPECIFICATION_GAP | P1 | CONFIRMED | AGENT_BLOCKED | ST-S1 | le scanner n'implémente qu'une des trois sources d'applicabilité |
| GCG-15 | SPECIFICATION_GAP | P2 | CONFIRMED | **AGENT** | ST-S5 | deux résolveurs de closeout divergent |
| GCG-16 | SPECIFICATION_GAP | P2 | CONFIRMED | AGENT | ST-S3 | l'acte est mono-règle — réparé §6.1, non implémenté |
| GCG-17 | SPECIFICATION_GAP | P2 | CONFIRMED | — | ST-S4 | contrat de population absent en v1 — **superseded par GCG-01** |
| GCG-18 | IMPLEMENTATION_DEFECT | P2 | CONFIRMED | AGENT_BLOCKED | ARB · IR-F8 | bornes `datetime` naïves alors que le canon déclare UTC ; `>` en dur |
| GCG-19 | IMPLEMENTATION_DEFECT | P2 | CONFIRMED | **AGENT** | IR §3 | `find_closeout` départage par `st_mtime` |
| GCG-20 | IMPLEMENTATION_DEFECT | P2 | CONFIRMED | AGENT_BLOCKED | IR-F6 | le prédicat `OVERCLAIM` est aveugle aux fences dans les deux sens |
| GCG-21 | EVIDENCE_DEFECT | P0 | CONFIRMED | HUMAN_DECISION | IR-F1 | 14/157 closeouts mutés ; un closeout clos complété en direction positive |
| GCG-22 | EVIDENCE_DEFECT | P1 | CONFIRMED | AGENT | IR-F10 ⊘ RA-F-A | le tableau de couverture §5 est faux — **et ma correction l'était aussi** |
| GCG-23 | EVIDENCE_DEFECT | P2 | CONFIRMED | AGENT | R1050 · ST | 7 invariants sur 11 sans porteur exécutable |
| GCG-24 | EVIDENCE_DEFECT | P2 | CONFIRMED | AGENT | IR-F9 | la prémisse de §6.2 est réfutée ; le cache crée deux contournements |
| GCG-25 | EVIDENCE_DEFECT | P2 | CONFIRMED | HUMAN_DECISION | ARB | les 12 constats de la revue ne sont épinglés par aucun corpus |
| GCG-26 | ASSURANCE_OVERCLAIM | P0 | CONFIRMED | HUMAN_DECISION | R1021 §3.10 | `2026-07-30_0500` revendique `PASS_ADVERSARIAL` + `CERTIFIED` sans bloc |
| GCG-27 | ASSURANCE_OVERCLAIM | P0 | CONFIRMED | HUMAN_DECISION | IR-F1 · ARB | les champs de verdict de ce closeout ont été écrits **après** clôture |
| GCG-28 | ASSURANCE_OVERCLAIM | P2 | **CONFIRMED** (fait) | AGENT_BLOCKED | ST-S6 · RA-F-I | 9 dispositions de connaissance positives sans section Harvest |
| GCG-29 | ASSURANCE_OVERCLAIM | P1 | CONFIRMED | EXTERNAL_ACTOR | R1021 · R1050 · ST | `A2_DISTINCT_AGENT_PROXY` jamais satisfait sur le chantier |
| GCG-30 | OPEN_NORMATIVE_DECISION | P2 | — | HUMAN_DECISION | R1021 §3.3 | un run d'arbitrage porte-t-il sa propre campagne ? |
| GCG-31 | OPEN_NORMATIVE_DECISION | P2 | — | HUMAN_DECISION | R1021 §3.6 | `A2` implique-t-il toujours obligation de campagne ? |
| GCG-32 | OPEN_NORMATIVE_DECISION | P2 | — | HUMAN_DECISION | R1021 §3.5 | `2026-07-28_2200` : réparation de schéma ou non-reconstructible ? |
| GCG-33 | SPECIFICATION_GAP | P2 | PARTLY_REFUTED | CANON_CHANGE | ST-S2 ⊘ IR-F4 | §3.5 déclare l'unité de la borne ; le canon la déclarait déjà |
| GCG-34 | MODEL_FLAW | P3 | PLAUSIBLE | HUMAN_DECISION | ST-S7 ⊘ IR-F12 | « largeur de fenêtre = qualité de publication » n'est pas générale |
| GCG-35 | MODEL_FLAW | P2 | INFERRED | HUMAN_DECISION | IR-F12 | sur-ajustement au protocole de run de ce dépôt |
| **GCG-36** | MODEL_FLAW + IMPLEMENTATION_DEFECT | **P0** | CONFIRMED | AGENT | RA-F-A | **quatrième voie** : `HISTORICAL_VALID` est testé avant `OVERCLAIM` — un renommage annihile la catégorie non migrable |

`⊘` = le second constat réfute ou conteste tout ou partie du premier.

---

## 5. Registre détaillé — périmètre d'arbitrage

### GCG-01 — `immutable` est un booléen déclaré que rien n'atteste
`MODEL_FLAW` · P0 · CONFIRMED · `HUMAN_DECISION` · source IR-F1 · statut **OPEN**

- **Fait observé** — §3.6 conditionne `HISTORICAL_VALID`, `MIGRATION_AVAILABLE`,
  `HISTORICAL_NONCOMPLIANCE` et la fenêtre de dette à `dated ∧ immutable`.
  `immutable` est renseigné par déclaration dans le contrat de population.
  Aucun mécanisme du modèle ne l'établit ni ne peut le contredire.
- **Preuve** — lecture de `governance-compatibility-model.md` §3.6 ; le champ
  n'a ni source d'attestation ni invariant qui le lie à une mesure.
- **Composant** — modèle §3.6 ; contrat de population.
- **Conséquence** — déclarer `immutable: true` **ouvre la fenêtre de dette**.
  Un prédicat que la déclaration suffit à satisfaire n'est pas une garantie,
  c'est une case à cocher qui déverrouille l'excuse. §3.3/I8 exige qu'une
  frontière soit déclarée et non dérivée ; le modèle applique ici le même geste
  à une **propriété factuelle de stockage**, que la déclaration ne peut pas
  rendre vraie.
- **Arbitrage** — ouvert. Réparation possible seulement en changeant la nature
  du champ (attestation) ou le périmètre du modèle. Voir décision **D2**.

### GCG-02 — la coordonnée de l'artefact est un label choisi par son auteur
`MODEL_FLAW` · P0 · CONFIRMED · `HUMAN_DECISION` · source IR-F3 · statut **OPEN**

- **Fait observé** — tout l'appareil temporel positionne un artefact par son
  identité de run. Dans ce dépôt l'identité n'est pas une mesure : elle est
  écrite par l'auteur du run.
- **Preuve** — `git log --diff-filter=A --date=iso -- docs/runs/2026-07-30_0500_*`
  → premier commit `2026-07-28 19:23`, soit ~30 h **avant** l'identité déclarée.
  Idem `2026-07-30_0100`. Vérifié indépendamment (commit `3d2eeee`).
- **Composant** — modèle §3.2, §3.5 ; `vbb-governance-compat.py` (parsing d'identité).
- **Conséquence** — le corollaire de §3.2, *« un artefact produit aujourd'hui ne
  pourra jamais entrer dans la fenêtre »*, est **faux**. Il suffit de nommer.
  Le même contenu défaillant renommé `2026-07-27_0900_*` devient
  `HISTORICAL_VALID` : non bloquant, exclu du dénominateur, sans ligne de
  ledger, sans arbitrage, sans trace.
- **Point clé** — I8 fixe la provenance de la **frontière** et ne dit rien de la
  provenance de la **coordonnée**. C'est l'asymétrie qui ouvre le trou.
- **Arbitrage** — ouvert. Voir décision **D1**. *Divergence avec la revue*
  consignée en `03` §6 : la revue tient la réparation naturelle (date d'auteur
  git) pour incompatible avec I8 ; je soutiens qu'I8 quantifie sur les
  frontières et non sur les faits, donc que la réparation est compatible — et
  que le besoin même d'argumenter établit que l'énoncé d'I8 est sous-spécifié.

### GCG-03 — la table des catégories n'est pas totale sous l'union §3.4
`MODEL_FLAW` · P1 · CONFIRMED · `CANON_CHANGE` · source IR-F7 · statut **OPEN**

- **Fait observé** — §3.4 rend une règle applicable par l'union de trois sources.
  Un artefact rendu applicable par la source 2 (`started_at`) ou 3
  (auto-déclaration) mais **positionné avant `applies_from`** n'entre dans
  aucune catégorie : ni `HISTORICAL_VALID` (la règle s'applique), ni
  `CURRENT_NONCOMPLIANCE` (exige de dépasser la borne d'enforcement), ni
  `UNKNOWN` / `MIGRATION_AVAILABLE` / `HISTORICAL_NONCOMPLIANCE` (exigent d'être
  *dans* la fenêtre), ni `PENDING_LIFECYCLE` (le porteur existe).
- **Preuve** — lecture croisée §3.4 / §4 ; candidat vivant
  `2026-07-28_1200_m1-adversarial-loop-normative-arbitration`, identité `1200`
  < `1400`, `started_at: "2026-07-28T12:00:00Z"`.
- **Conséquence** — la v2 a introduit la disjonction sans étendre la partition
  qu'elle alimente. Le trou est **conditionnel à la question ouverte 5** du
  modèle (quel fuseau lit l'identité) : le modèle ne peut pas dire lui-même si
  sa table a un trou. C'est cela, le constat.
- **Arbitrage** — ouvert, dépend de **D1** et **D3**.

### GCG-04 — le ledger peut attribuer une disposition non-dette dans la fenêtre
`MODEL_FLAW` + `OPEN_NORMATIVE_DECISION` · P1 · CONFIRMED · `HUMAN_DECISION` · source IR-F2 · statut **OPEN**

- **Fait observé** — `LEDGERABLE = {HISTORICAL_VALID, MIGRATION_AVAILABLE,
  HISTORICAL_NONCOMPLIANCE}` ; `historical_debt` ne somme que les deux
  dernières ; `applicable` exclut `HISTORICAL_VALID`.
- **Preuve** — `tools/vbb-governance-compat.py:83`, `:250-271`. Vérifié.
  Démonstration IR (E2, runs synthétiques en répertoire temporaire) : un run en
  échec **dans** la fenêtre + une ligne de ledger `HISTORICAL_VALID` →
  `verdict: PASS`, `historical_debt: 0`, `blocking: []`, disparition du
  dénominateur de conformité.
- **Conséquence** — **la voie de blanchiment la plus propre du modèle**, et la
  seule qui ne laisse de trace dans aucune des trois lectures : ni dette, ni
  non-conformité, ni comptage. I2 interdit une disposition **de dette hors** de
  la fenêtre ; rien n'interdit une disposition **de non-dette dedans**, et §2.2
  autorise l'arbitration à « résoudre un `UNKNOWN` en une disposition » sans
  restreindre l'ensemble cible. Les 4 `UNKNOWN` actuels sont les premiers
  clients.
- **Arbitrage** — ouvert. La correction évidente (retirer `HISTORICAL_VALID` de
  `LEDGERABLE`) est **une ligne de code et une décision sémantique** : elle
  présuppose que l'arbitration ne peut jamais *attribuer* une validité
  historique, seulement *reconnaître* une dette. Voir **D6**. Corriger avant D6
  serait une réparation défensive.

### GCG-05 — `PENDING_LIFECYCLE` est défini sur une absence provocable
`MODEL_FLAW` + `OPEN_NORMATIVE_DECISION` · P1 · CONFIRMED · `HUMAN_DECISION` · source IR-F5 · statut **OPEN**

- **Fait observé** — renommer `07_CLOSEOUT.md` en `07_CLOSE-OUT.md` fait passer
  un run de `CURRENT_NONCOMPLIANCE` à `PENDING_LIFECYCLE` : non bloquant **et**
  exclu de `applicable`.
- **Preuve** — démonstration IR (E3, répertoire temporaire) ; le dépôt n'a pas
  été modifié. 8 runs `CURRENT_NONCOMPLIANCE` sont des instances disponibles.
- **Conséquence** — §4.1 pose un test de discrimination sur le **motif** de
  l'absence de preuve ; le scanner n'observe que le **fait** de l'absence.
  §3.7/I11 déclare le résolveur, ce qui règle les variantes de nommage mais pas
  l'absence : un résolveur déclaré résout toujours vers « absent ».
- **Point clé** — ce n'est pas une lacune du texte, **c'est ce que le texte
  dit**. La catégorie est définie sur l'absence du porteur.
- **Arbitrage** — ouvert. Voir **D7**.

### GCG-06 — les deux prédicats d'`OVERCLAIM` sont choisis par le scanner
`MODEL_FLAW` · P1 · CONFIRMED · `CANON_CHANGE` · source IR-F6 · statut **OPEN**

- **Fait observé** — §4.2 ne déclare ni (a) quel vocabulaire de revendication
  compte comme « le verdict que la règle gouverne » — la liste
  `PASS / CERTIFIED / READY / APPROVED` est générique — ni (b) ce qu'est « la
  structure permettant de le valider ». Les deux sont aujourd'hui des prédicats
  que le scanner choisit.
- **Preuve** — lecture §4.2 ; `vbb-governance-compat.py` (test `^adversarial:$`
  sur texte brut).
- **Conséquence** — la v2 a rendu la **résolution d'artefact** déclarée par la
  règle (A6/I11) et a laissé le **prédicat de revendication** au scanner. La
  réparation que la v2 a inventée n'a pas été appliquée au cas qui en avait le
  plus besoin. Une revendication ajoutée ou retirée fait basculer une catégorie
  protégée.
- **Arbitrage** — ouvert. Voir **D5**.

### GCG-07 — l'exemple G3 de §4.2 contredit la fixture `NO_BLOCK`
`MODEL_FLAW` · P2 · CONFIRMED · `CANON_CHANGE` · source IR-F6 · statut **OPEN**

- **Fait observé** — §4.2 donne comme exemple travaillé G3 : `status: READY`
  avec `FINAL_STATUS: HANDOFF`, classé `OVERCLAIM`. Les catégories sont
  attribuées par couple *(artefact, règle)*. **Sous quelle règle ?** Aucune règle
  de readiness ne déclare `applies_from`, ni population, ni résolveur. Pendant
  ce temps la fixture `NO_BLOCK` (`tests/test_governance_compat_gate.py:38`)
  porte `status: "READY"` et est assertée `HISTORICAL_VALID` (`:107-116`).
- **Preuve** — lecture croisée modèle §4.2 / suite de tests. Vérifié.
- **Conséquence** — §4.2 et la suite de tests ne peuvent pas être vraies
  ensemble. C'est un contre-exemple que le modèle **ne peut pas exprimer dans
  son propre formalisme** : il documente une classification sans règle porteuse.
- **Arbitrage** — ouvert, dépend de **D5**. *Concession explicite de l'agent
  principal : l'exemple G3 était de moi et il est faux tel qu'écrit.*

### GCG-08 — inclusivité des bornes non déclarée ; I10 unifie deux directions opposées
`MODEL_FLAW` · P2 · CONFIRMED · `CANON_CHANGE` · source IR-F8 · statut **OPEN**

- **Fait observé** — `vbb-governance-compat.py:211` compare par `>` strict.
  §3.5/I10 déclare `unit` et `timezone`, jamais ouvert/fermé. I10 donne en outre
  une résolution unique (« la plus inclusive ») pour un intervalle dont les
  directions fail-closed sont **opposées** : inclure `applies_from` est plus
  strict, inclure `enforcement_effective_from` est plus permissif.
- **Preuve** — `sed -n '211p' tools/vbb-governance-compat.py`. Instance vivante :
  `2026-07-28_2000_m2-bis-adversarial-loop-bootstrap-deployment` — **le run qui
  a livré l'outil d'enforcement** — est classé `UNKNOWN`, donc dans la fenêtre
  de dette, donc éligible à être excusé de ne pas porter la vérification qu'il a
  lui-même créée. Confirmé dans la sortie `--json` §2.
- **Conséquence** — la règle de granularité de §3.5 (« l'artefact est réputé
  gouverné ») est écrite sans condition, ce qui est faux pour une identité à
  granularité jour très antérieure à la borne (`20260615-usage-audit`).
- **Arbitrage** — ouvert, dépend de **D3**.

### GCG-09 — `enforcement_effective_from` n'est déclaré nulle part au canon
`CANON_CONFLICT` · P1 · CONFIRMED · `CANON_CHANGE` · source IR-F4 · statut **OPEN**

- **Fait observé** — le canon déclare `cutoff_run_key: "2026-07-28_1400"` et
  `cutoff_timestamp: "2026-07-28T14:00:00Z"`
  (`docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md:484-485`). La borne `2000` n'existe
  **que** dans le code, à `tools/vbb-governance-compat.py:105`.
- **Preuve** — `grep -rn "enforcement_effective_from" docs/` → aucune occurrence
  hors du fichier de modèle et des runs GCG. Vérifié deux fois.
- **Conséquence** — **I8 est violé en ce moment par la règle phare du modèle**,
  et le commentaire d'en-tête du code (lignes 87-89) affirme le contraire :
  *« Both bounds below are run identities read from the canon »*. C'est
  exactement le défaut que §3.3/I8 prétend avoir corrigé, et §7 présente la
  correction comme faite. Canoniser un invariant que l'implémentation de
  référence enfreint dans son propre commentaire est le mode d'échec que le
  modèle a été écrit pour empêcher.
- **Arbitrage** — ouvert. Voir **D3**. Le commentaire faux est en outre une
  fausse déclaration active dans le code : sa correction est `AGENT`, mais elle
  est bloquée par C3 dans ce run.

### GCG-10 — deux horloges, un choix non déclaré
`CANON_CONFLICT` · P2 · CONFIRMED · `CANON_CHANGE` · source IR-F7 · ST-S2 · statut **OPEN**

- **Fait observé** — §3.4 dit quelle horloge rend une règle **applicable**
  (`started_at` ou identité) ; §3.2 positionne l'artefact dans la fenêtre par
  **identité**. Deux horloges, un choix jamais déclaré.
- **Preuve — mesure résolue après revue :**

  | Résolveur | Mesurés | Désaccord (>1 min) | Écart max |
  |---|---|---|---|
  | `07_CLOSEOUT.md` seul | 106 | **75** | 22,08 h |
  | repli `*CLOSEOUT*.md` | 106 | **75** | 22,08 h |
  | + identités à granularité jour | 123 | 90 | 29,0 h |

- **Conséquence** — **75 runs sur 164, soit 46 %**, positionnent leur identité à
  plus d'une minute de leur `started_at`. Ce n'est pas un cas limite, mais ce
  n'est pas non plus « la majorité du corpus » : c'est une majorité du
  sous-ensemble mesuré.
- **Arbitrage** — ouvert, dépend de **D1**.

> **Réfuté après revue (RA-F-E).** La version initiale conservait deux mesures
> divergentes (74/105 et 94/123) en les déclarant irréductibles, et attribuait
> l'écart à GCG-15 : *« deux résolveurs de closeout ne comptent pas la même
> population »*. **C'était faux.** Les deux résolveurs donnent une population
> identique ; tout l'écart vient de l'inclusion des identités à granularité
> jour, où l'« écart » est un artefact de comparaison entre un intervalle de
> 24 h et un instant — le cas même que GCG-08 et le modèle §3.5 discutent.
> Le reproche est accepté tel quel : *préserver un désaccord est une bonne
> discipline ; le préserver au lieu de le mesurer est l'apparence de la
> discipline.*

### GCG-11 — vocabulaire parallèle avec la partition `certification_status`
`CANON_CONFLICT` · P1 · CONFIRMED · `HUMAN_DECISION` · source IR-F11 · statut **OPEN**

- **Fait observé** — `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md:574-584`
  partitionne **déjà la même population** : `UNASSESSED_LEGACY` (pré-cutoff, non
  bloquant), `PRE_CERTIFICATION`, `MIGRATION`, `NOT_CERTIFIED` (bloquant),
  `CERTIFIED`, `SUSPENDED`, `NOT_APPLICABLE`. §10 énonce déjà la règle
  pré-cutoff. GCG réencode la même partition en 8 catégories, sans aucun mapping.
- **Preuve** — lecture des deux documents. Vérifié.
- **Conséquence** — Critical Rule 5, vérité parallèle. Divergence disponible dès
  aujourd'hui : un run pré-cutoff déclarant `certification_status: NOT_CERTIFIED`
  est **bloquant** sous le canon et `HISTORICAL_VALID` (non bloquant) sous GCG.
  La question ouverte 6 du modèle voit les *constantes* dupliquées ; elle ne voit
  pas le *vocabulaire* dupliqué.
- **Arbitrage** — ouvert. Voir **D4**. C'est la décision qui peut réduire le
  périmètre du modèle à la seule fenêtre de dette.

### GCG-12 — constantes de cutover dupliquées entre deux outils
`CANON_CONFLICT` · P2 · CONFIRMED · `AGENT` · source ST-S8 · statut **CLASSIFIED**

- **Fait observé** — la paire adverse `*_CUTOVER_KEY` / `*_CUTOVER_AT` est
  dupliquée entre `vbb-loop-closure-check.py` et `vbb-adversarial-gate.py`.
  Valeurs identiques aujourd'hui.
- **Preuve** — `grep -rn "CUTOVER_KEY" tools/`.
- **Conséquence** — vérité parallèle en attente de dérive (Critical Rule 5).
- **Arbitrage** — **classé, correction mécanique**, sans décision normative :
  factoriser en une source unique. Bloqué ici par C3 seulement. **Ne pas
  corriger avant D3** : si le canon devient la source déclarée des bornes, la
  factorisation vise le canon et non un module partagé.

### GCG-13 — le modèle ne cite pas le finding actif portant sur son mécanisme central
`CANON_CONFLICT` · P2 · CONFIRMED · `CANON_CHANGE` · source IR-F3 · statut **OPEN**

- **Fait observé** — `docs/AUDIT_STATUS.md:124` porte le finding **`AUD-F8`,
  P2, OPEN** : *« la dashboard étiquette [les runs post-datés] "future-dated
  historical state acknowledged", ce qui relabellise des artefacts neufs en
  preuve historique »*. `docs/TEMPORAL_PROVENANCE.md` (canon, `status: active`)
  prescrit de traiter les répertoires post-datés comme preuve historique
  importée. Le modèle ne cite ni l'un ni l'autre.
- **Preuve** — lecture `docs/AUDIT_STATUS.md` §Active risks ; `grep` du modèle.
- **Conséquence** — le modèle construit son mécanisme central sur un mécanisme
  dont le dépôt sait déjà, par un finding ouvert, qu'il relabellise du neuf en
  historique. Problème de vérité parallèle **en plus** du problème de mécanisme.
- **Arbitrage** — ouvert, se ferme avec **D1**.

### GCG-14 — le scanner n'implémente qu'une des trois sources d'applicabilité
`SPECIFICATION_GAP` · P1 · CONFIRMED · `AGENT` · source ST-S1 · statut **OPEN**

- **Fait observé** — l'enforcer canonique reconnaît trois sources combinées par
  `OR` (`vbb-loop-closure-check.py:216-252`) ; le scanner GCG n'implémente que
  la source 1. Un sous-ensemble d'une disjonction est au plus aussi inclusif.
- **Preuve** — lecture des deux implémentations. **Latent** : vérifié qu'aucun
  run du dépôt ne diverge aujourd'hui.
- **Conséquence** — un gate de compatibilité plus permissif que le gate qu'il
  mesure **masque des échecs**. Bloquant déclaré du câblage CI.
- **Arbitrage** — ouvert. La correction est mécanique (`AGENT`) **mais elle
  ouvre GCG-03** : implémenter les trois sources rend la table non totale. Les
  deux doivent être réparés dans le même run, sinon la correction de GCG-14
  introduit un défaut plus grave que celui qu'elle ferme.

### GCG-15 — deux résolveurs de closeout divergent
`SPECIFICATION_GAP` · P2 · CONFIRMED · `CANON_CHANGE` · source ST-S5 · statut **OPEN**

- **Fait observé** — `find_closeout()` accepte `07_CLOSEOUT.md` puis se rabat
  sur `*CLOSEOUT*.md` (consommé par GCG) ; la règle B utilise le chemin en dur
  `07_CLOSEOUT.md`. Instance réelle :
  `2026-07-28_1200_m1-adversarial-loop-normative-arbitration` porte
  `02_CLOSEOUT.md`.
- **Preuve** — `tests/adversarial_corpus/CORPUS-S5.py` (BEHAVIOUR_PIN, verrouille
  la divergence). Se manifeste aussi dans l'écart de population de GCG-10.
- **Conséquence** — le même run « a » et « n'a pas » de closeout selon le
  consommateur. §3.7/I11 spécifie la réparation ; elle n'est pas implémentée.
- **Arbitrage** — ouvert. Réparation spécifiée, non appliquée. Ne ferme pas
  GCG-05 : un résolveur déclaré résout toujours vers « absent ».

### GCG-16 — l'acte est mono-règle
`SPECIFICATION_GAP` · P2 · CONFIRMED · `AGENT` · source ST-S3 · statut **REPAIRED_IN_MODEL_UNIMPLEMENTED**

- **Fait observé** — le schéma d'acte v1 portait une table de comptage plate et
  un ratio unique ; deux règles aux populations différentes (14 vs 19) ne
  peuvent pas y coexister.
- **Preuve** — ST §5 S3, instance `2026-07-30_0500` simultanément `OVERCLAIM`
  sous la règle A et non conforme sous la règle B.
- **Arbitrage** — **réparé au modèle** (§6.1, amendement A4), **non implémenté**.
  Les deux contraintes de forme (pas de ratio global ; verdict = `OR`) ont
  survécu à la revue indépendante. Reste ouvert côté code uniquement.

### GCG-17 — contrat de population absent en v1
`SPECIFICATION_GAP` · P2 · CONFIRMED · source ST-S4 · statut **SUPERSEDED par GCG-01**

- **Fait observé** — la v1 parlait de « l'artefact » sans déclarer la classe
  d'artefacts gouvernée.
- **Arbitrage** — **superseded, non clos**. La v2 §3.6 a ajouté le contrat
  (`dated`, `immutable`, `enumerable` + mode dégradé). GCG-01 établit que le
  contrat ajouté est inopérant, parce que deux de ses trois termes sont des
  déclarations que rien n'atteste. Le constat d'origine ne disparaît pas : il
  est **absorbé** par un constat plus fort. Conserver la trace évite de croire
  que S4 a été réparé.

### GCG-18 — bornes `datetime` naïves alors que le canon déclare UTC
`IMPLEMENTATION_DEFECT` · P2 · CONFIRMED · `AGENT` · source ARB · IR-F8 · statut **OPEN**

- **Fait observé** — `ADVERSARIAL_APPLIES_FROM = datetime(2026, 7, 28, 14, 0)`
  et `ADVERSARIAL_ENFORCEMENT_EFFECTIVE_FROM = datetime(2026, 7, 28, 20, 0)` sont
  **sans `tzinfo`**, alors que le canon déclare `cutoff_timestamp` avec le
  suffixe `Z`.
- **Preuve** — `sed -n '104,106p' tools/vbb-governance-compat.py`. Mesuré dans
  ce run.
- **Conséquence** — corrobore GCG-33 : la borne canonique porte une unité, la
  borne implémentée l'a perdue. La comparaison `>` opère donc entre deux
  quantités dont aucune ne déclare son fuseau au point de comparaison.
- **Arbitrage** — ouvert, correction mécanique, subordonnée à **D3**.

### GCG-19 — `find_closeout` départage par `st_mtime`
`IMPLEMENTATION_DEFECT` · P2 · CONFIRMED · `AGENT` · source IR §3 (résiduel) · statut **OPEN**

- **Fait observé** — `tools/vbb_run_resolution.py:113` départage les candidats
  par `st_mtime`, qui n'est pas du contenu et n'est pas préservé par un clone.
- **Preuve** — lecture du code (revue indépendante). **Latent** : aujourd'hui
  `2026-05-19_1000_moc-context-strategy` a deux candidats mais aussi le fichier
  canonique, donc le départage ne se déclenche jamais.
- **Conséquence** — non-déterminisme de la classification, contre §2.1. Le
  déterminisme a par ailleurs **survécu** à l'attaque principale de la revue
  (la cadence ≤ 90 jours épingle une date de référence au lieu d'appeler
  `now()`) ; ce résidu est le seul point trouvé.
- **Arbitrage** — ouvert, correction mécanique, dépend de **D7**.

### GCG-20 — le prédicat `OVERCLAIM` est aveugle aux fences dans les deux sens
`IMPLEMENTATION_DEFECT` · P2 · CONFIRMED · `AGENT` · source IR-F6 · statut **OPEN**

- **Fait observé** — l'unique `OVERCLAIM` vivant, `2026-07-30_0500`, n'a **pas**
  d'`adversarial_status` en frontmatter ; le match est une ligne située dans un
  bloc ` ```yaml ` de la prose. Symétriquement, ajouter un bloc `adversarial:`
  encadré fait basculer `OVERCLAIM` → `UNKNOWN`.
- **Preuve** — lecture du closeout ; démonstration IR (E4, temporaire).
  L'enforcer, lui, extrait explicitement les blocs YAML encadrés
  (`vbb-adversarial-gate.py:171-177`), et le run conforme `2026-07-30_0100`
  porte son bloc **dans** un fence : GCG le matche par accident d'ancrage de
  ligne, pas par conception.
- **Conséquence** — le scanner ne distingue pas une revendication de la citation
  d'une revendication. I5 protège le **label** `OVERCLAIM`, pas la **propriété**.
- **Arbitrage** — ouvert. Correction mécanique **mais subordonnée à D5** :
  réparer le parseur sans déclarer le prédicat, c'est ajuster le code aux deux
  contre-exemples connus.

### GCG-21 — la population instrumentée viole `immutable`, mesurément
`EVIDENCE_DEFECT` · P0 · CONFIRMED · `HUMAN_DECISION` · source IR-F1 · statut **OPEN**

- **Fait observé** — **14 des 157 closeouts suivis ont plus d'un commit.** Le
  plus grave est `b9084e2` sur
  `docs/runs/2026-07-30_0500_final-publication-of-v1.1-certification/07_CLOSEOUT.md` :

  ```
  -status: "PENDING_POST_PUSH"     -  verdict: <PASS|FAIL>
  +status: "READY"                 +  verdict: PASS
                                   +adversarial_status: PASS_ADVERSARIAL
                                   +certification_status: CERTIFIED
  ```

- **Preuve** — boucle `git log --oneline -- docs/runs/*/07_CLOSEOUT.md | wc -l`,
  re-mesurée dans ce run : **14**. `git log -p` sur le closeout cité.
  *Dénominateur corrigé après revue (RA-F-K) : `git ls-files` compte **157**
  closeouts suivis ; 164 est le nombre de répertoires de run, pas de closeouts.*
- **Conséquence** — les runs ne sont des enregistrements que de nom. **Par le
  mode dégradé du modèle lui-même**, les 148 classifications `HISTORICAL_VALID`
  actuelles deviennent indéfinies et aucune dette n'est admissible. Combiné à
  GCG-35, la machinerie distinctive du modèle n'a **aujourd'hui aucune
  population valide**.
- **Arbitrage** — ouvert. Voir **D2**. C'est aussi la preuve directe de GCG-27.

### GCG-22 — le tableau de couverture §5 est faux, et ma correction l'était aussi
`EVIDENCE_DEFECT` · P1 · CONFIRMED · `AGENT` · source IR-F10 ⊘ RA-F-A · statut **OPEN**

- **Fait observé, version corrigée** — trois erreurs dans le tableau présenté
  comme le point d'honnêteté du document :
  1. **I6 est listé couvert** alors qu'une seule de ses deux branches l'est
     (GCG-05) ;
  2. **le porteur d'I4** (`tests:137-144`) assert le littéral
     `"NOT_DERIVABLE_FROM_THIS_GATE"` que `build_act` écrit en dur à
     `vbb-governance-compat.py:274` : il ne peut échouer qu'en éditant la
     constante. **Test tautologique**, pas propriété ;
  3. **I5 est listé non couvert, et il doit le rester** —
     `test_overclaim_outranks_the_historical_reading` (`tests:91-104`) construit
     sa fixture à `APPLIES_FROM + 1h`, donc **dans** la fenêtre. Il n'exerce que
     « jamais ledgerable ». La seconde branche d'I5, « jamais adouci par
     l'ancienneté », **n'est pas couverte — et elle est cassée** (GCG-36).
- **Preuve** — lecture croisée modèle §5 / suite de tests / outil, plus la
  démonstration de GCG-36.
- **Conséquence** — « 3/11 » n'est pas le plancher honnête qu'il annonce. Un
  aveu de couverture faux est pire qu'une absence d'aveu : il achète de la
  crédibilité sur une mesure fausse.
- **Arbitrage** — ouvert, correction mécanique.

> **Ma correction initiale était fausse (RA-F-A).** J'affirmais qu'I5 devait
> être listé **couvert**, en citant ce test. La revue a établi que le test
> couvre l'autre branche, et que celle que je citais comme preuve de couverture
> est précisément **la branche cassée**. J'ai donc corrigé un tableau de
> couverture dans le sens de la **surestimation** — le mode d'échec exact que ce
> constat reproche au modèle. La concession initiale (« ce tableau est de moi »)
> vaut deux fois.

### GCG-23 — 7 invariants sur 11 sans porteur exécutable
`EVIDENCE_DEFECT` · P2 · CONFIRMED · `AGENT` · source R1050 · ST · statut **OPEN**

- **Fait observé** — I1, I3, I7, I8 n'avaient pas de porteur ; la v2 a ajouté
  I9, I10, I11 sans porteur. Compte corrigé par GCG-22 : la couverture réelle
  n'est ni 3/8 ni 3/11, elle doit être recomptée.
- **Conséquence** — un invariant sans test est une intention. La v2 est plus
  complète comme spécification et pas plus sûre comme mécanisme — le modèle le
  dit lui-même, avec le mauvais chiffre.
- **Arbitrage** — ouvert. Recompte requis avant toute publication de ratio.

### GCG-24 — la prémisse de §6.2 est réfutée par la mesure
`EVIDENCE_DEFECT` · P2 · CONFIRMED · `AGENT` · source IR-F9 · statut **OPEN**

- **Fait observé** — §6.2 pose : *« Un scan complet à chaque démarrage de session
  est intenable : le POC a mesuré plusieurs secondes pour 13 runs sur une
  population de 161. »* Mesuré, trois scans complets consécutifs sur 163-164
  runs : **0,91 s / 0,68 s / 0,70 s**. Prémisse fausse d'environ un ordre de
  grandeur.
- **Preuve** — `/usr/bin/time -p python tools/vbb-governance-compat.py` ×3
  (revue indépendante), cohérent avec les exécutions de ce run.
- **Conséquence** — le cache inutile achète deux contournements :
  1. `cache_key = hash(versions de règles) + hash(liste de run_id) +
     hash(mtime du ledger)` — **aucun contenu d'artefact, aucune version
     d'outil**. Éditer un closeout (GCG-21 montre que cela arrive) n'invalide
     pas l'acte, alors que §6.4.3 exige un acte **frais** avant tout `READY`.
  2. *« Un cache absent produit `confidence: DEGRADED`, pas un blocage »* :
     l'absence est traitée plus permissivement que l'invalidité. `rm` du cache
     et l'on avance avec un acte sans entrée bloquante.
- **Arbitrage** — ouvert. **Divergence partielle avec la revue**, consignée en
  `03` §6 : la revue conclut « supprimer §6.2 » ; je souscris à la suppression
  mais conteste la formulation « prémisse réfutée » — le coût scale avec
  l'ensemble **applicable** (15/164 aujourd'hui, chacun invoquant un gate en
  sous-processus), pas avec la population. La prémisse est **prématurée**, pas
  simplement fausse. La conclusion opérationnelle est identique et les deux
  contournements disparaissent avec §6.2.

### GCG-25 — les constats de la revue indépendante ne sont épinglés par aucun corpus
`EVIDENCE_DEFECT` · P2 · CONFIRMED · `HUMAN_DECISION` · source ARB · statut **OPEN**

- **Fait observé** — l'obligation de corpus (`ADVERSARIAL_ASSURANCE` §9
  destination 6) est déclenchée par les findings déclarés `CONFIRMED` **dans le
  bloc `adversarial:` d'un closeout** (`tests/test_corpus_mandatory.py:53-70`).
  Les 12 constats de la revue indépendante n'ont été déclarés dans aucun
  closeout : ils ne portent donc **aucune obligation de corpus** et rien
  n'empêche qu'ils changent en silence.
- **Preuve** — lecture de `tests/test_corpus_mandatory.py` §`_confirmed_findings`.
  Mesuré dans ce run.
- **Conséquence** — **une revue conduite hors d'un run échappe à l'épinglage**,
  quelle que soit la qualité de ses constats. Symétriquement, le seul moyen de
  les épingler est de les déclarer dans un closeout, ce qui force à écrire du
  code — exactement le mécanisme qui a fait dévier le stress test (GCG-C4).
- **Arbitrage** — ouvert. Ce run **ne les déclare pas** dans son bloc adverse et
  le dit : il ne conduit aucune campagne, il arbitre des constats produits
  ailleurs. Le registre est leur porteur durable en attendant D8.

### GCG-26 — `2026-07-30_0500` revendique `PASS_ADVERSARIAL` et `CERTIFIED` sans bloc validable
`ASSURANCE_OVERCLAIM` · **P0** · CONFIRMED · `HUMAN_DECISION` · source R1021 §3.10 · statut **OPEN**

- **Fait observé** — le closeout déclare `adversarial_status: PASS_ADVERSARIAL`
  et `certification_status: CERTIFIED` sans porter de bloc `adversarial:`
  validable.
- **Preuve** — `vbb-governance-compat.py --json` → unique `OVERCLAIM` de la
  population, bloquant.
- **Conséquence** — c'est la **certification v1.1 publiée** qui est en cause.
  Deux questions, posées depuis le run `1021` et toujours ouvertes : le
  `PASS_ADVERSARIAL` est-il dérivé de `2026-07-30_0100` (seul run conforme au
  gate) ? Sinon, la revendication tombe et `certification_status` doit être
  révisé.
- **Interdiction reconduite** — ne pas fabriquer de bloc adverse pour rendre ce
  run vert. Si la revendication n'est pas soutenue, **c'est la revendication qui
  tombe**.
- **Arbitrage** — ouvert, P0. Voir **D0**.

### GCG-27 — les champs de verdict de ce closeout ont été écrits après sa clôture
`ASSURANCE_OVERCLAIM` · **P0** · CONFIRMED · `HUMAN_DECISION` · source IR-F1 · ARB · statut **OPEN**

- **Fait observé** — le commit `b9084e2` a fait passer ce même closeout de
  `status: PENDING_POST_PUSH` / `verdict: <PASS|FAIL>` à `status: READY` /
  `verdict: PASS`, en **ajoutant** `adversarial_status: PASS_ADVERSARIAL` et
  `certification_status: CERTIFIED`.
- **Preuve** — `git log -p -- docs/runs/2026-07-30_0500_*/07_CLOSEOUT.md`.
- **Conséquence** — **aggravation de GCG-26 et changement de nature.** GCG-26
  décrit une revendication non soutenue ; GCG-27 établit que la revendication a
  été **insérée après la clôture**, en direction positive. Ce n'est plus une
  omission de preuve : c'est une écriture de verdict hors du moment où le verdict
  pouvait être établi. Aucune disposition de dette n'est admissible pour cela —
  la mutation est postérieure à l'enforcement.
- **Arbitrage** — ouvert, P0, **traité avec GCG-26 et avant tout le reste**.
  Voir **D0**.

### GCG-28 — 9 dispositions de connaissance positives sans section Harvest
`ASSURANCE_OVERCLAIM` · P2 · **CONFIRMED sur le fait** · `AGENT_BLOCKED` · source ST-S6 · RA-F-I · statut **OPEN**

- **Fait observé** — 9 runs déclarent `knowledge_harvest` positif (7
  `EVIDENCE_LINKED`, 2 `OBSERVATION_RECORDED`) sans section *Knowledge Harvest*
  dans le corps du closeout. Le validateur ne vérifie que l'appartenance à
  l'énumération (`vbb-loop-closure-check.py:128`) ; il n'existe aucun registre de
  candidats dans le dépôt.
- **Preuve — mesurée dans ce run après revue** : `grep -ci harvest` sur les 9
  closeouts. **Tous** ne portent le mot qu'en clé de frontmatter ; deux le
  reprennent à l'intérieur d'un bloc YAML. **Aucun ne porte de section Knowledge
  Harvest.** Le fait est établi, non inféré.
- **Conséquence** — si les 9 sont des `OVERCLAIM`, une **seconde règle entre en
  dette** et le périmètre d'arbitrage humain double.
- **Arbitrage** — le **fait** est confirmé ; la **qualification** en `OVERCLAIM`
  reste suspendue à **D5**, qui décide si `EVIDENCE_LINKED` compte comme une
  revendication au sens du prédicat.

> **Corrigé après revue (RA-F-I).** La version initiale laissait ce constat en
> `PLAUSIBLE` et renvoyait son instruction à un run futur, alors que la mesure
> coûte deux commandes. Le reproche est juste : différer une mesure bon marché
> dans un document dont la thèse est « mesurer avant de décider » est
> incohérent. La distinction fait/qualification, elle, était juste et est
> conservée.

### GCG-29 — `A2_DISTINCT_AGENT_PROXY` jamais satisfait sur le chantier
`ASSURANCE_OVERCLAIM` · P1 · CONFIRMED · `EXTERNAL_ACTOR` · source R1021 · R1050 · ST · ARB · statut **OPEN**

- **Fait observé** — les runs `1021`, `1050`, `1130` et le présent run déclarent
  `adversarial_level: A2` sans acteur distinct par famille de LLM. La revue
  indépendante du 2026-07-29 a apporté une **isolation de contexte réelle** mais
  **pas une distinction de famille de modèle**.
- **Preuve** — blocs `certification_blocker` des trois closeouts ; §6 du présent
  closeout.
- **Conséquence** — aucun `PASS_ADVERSARIAL` n'est revendiquable sur ce
  chantier, et aucun ne l'a été. L'écart mesuré entre revue et auteur (8
  constats substantiels manqués par l'auteur, dont 3 voies de blanchiment) est
  un argument **pour** la valeur de l'isolation de contexte, pas un substitut à
  la distinction d'acteur.
- **Arbitrage** — ouvert, `EXTERNAL_ACTOR`. Ne peut être clos par aucun agent.

### GCG-30 — un run d'arbitrage porte-t-il sa propre campagne ?
`OPEN_NORMATIVE_DECISION` · P2 · `HUMAN_DECISION` · source R1021 §3.3 · statut **OPEN**

Le sujet d'un run d'arbitrage est une décision de canon, pas un artefact
attaqué. Le canon ne tranche pas si un tel run doit porter sa propre campagne
adverse ou une attestation dérivée du run qu'il arbitre. **Le présent run est
lui-même une instance de la question.**

### GCG-31 — `A2` implique-t-il toujours obligation de campagne ?
`OPEN_NORMATIVE_DECISION` · P2 · `HUMAN_DECISION` · source R1021 §3.6 · statut **OPEN**

`2026-07-28_2300` déclare **contemporainement** `adversarial_status: NOT_REQUIRED`
tout en portant `adversarial_level: A2`. La contradiction est d'origine, pas
rétroactive. Elle révèle que le canon confond **niveau de criticité du sujet** et
**obligation de conduire une campagne**.

### GCG-32 — `2026-07-28_2200` : réparation de schéma ou non-reconstructible ?
`OPEN_NORMATIVE_DECISION` · P2 · `HUMAN_DECISION` · source R1021 §3.5 · statut **OPEN**

Bloc adverse présent avec 14 findings ; `adv-a2-defender-identity` absent,
`confidence`/`state` invalides sur les 14 (28 échecs). La disposition dépend
d'un fait non encore établi : les valeurs sont-elles **présentes mais hors
énumération** (réparable sans inférence) ou **absentes** (non réparable sans
qualifier après coup) ? **Inspection des 14 findings requise avant décision.**

### GCG-33 — §3.5 déclare l'unité de la borne ; le canon la déclarait déjà
`SPECIFICATION_GAP` · P2 · **PARTLY_REFUTED** · `CANON_CHANGE` · source ST-S2 ⊘ IR-F4 · statut **REDIRECTED**

- **Fait observé** — S2 affirmait qu'une borne déclare sa valeur sans son unité,
  et la v2 a ajouté §3.5 pour y répondre. Or le canon déclare déjà
  `cutoff_timestamp: "2026-07-28T14:00:00Z"` — la borne **a** une unité.
- **Preuve** — `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md:484-485`.
- **Conséquence** — **§3.5 applique sa réparation au côté qui n'en avait pas
  besoin.** Ce qui n'a réellement pas d'unité déclarée, c'est la **coordonnée de
  l'artefact** (GCG-02, GCG-10). Nuance qui subsiste : la borne *implémentée* a
  perdu son fuseau (GCG-18), donc S2 n'est pas entièrement faux — il est mal
  visé.
- **Arbitrage** — **partiellement réfuté, redirigé** vers GCG-02/GCG-18. Conservé
  au registre parce qu'effacer une réfutation d'un constat antérieur est une
  forme de blanchiment documentaire.

### GCG-34 — « largeur de fenêtre = qualité de publication » n'est pas générale
`MODEL_FLAW` · P3 · PLAUSIBLE · `HUMAN_DECISION` · source ST-S7 ⊘ IR-F12 · statut **CONTESTED**

- **Fait observé** — §3.2 lit la largeur de la fenêtre comme un indicateur de
  qualité de publication d'une règle. Cette lecture suppose que l'auteur de la
  règle et son outilleur sont la même équipe, dans le même dépôt, à quelques
  heures d'intervalle.
- **Conséquence** — pour une règle écrite hors du dépôt, la fenêtre est toujours
  large et n'est pas un signal de qualité. Le résultat le plus « positif » du
  stress test est donc le plus dépendant du contexte où il a été obtenu.
- **Arbitrage** — **contesté, non tranché.** Aucune règle externe n'a été testée
  ni par le stress test ni par la revue : le constat est une inférence
  structurelle des deux côtés.

### GCG-35 — sur-ajustement au protocole de run de ce dépôt
`MODEL_FLAW` · P2 · **INFERRED** · `HUMAN_DECISION` · source IR-F12 · statut **OPEN**

- **Fait observé** — trois indices :
  1. `enumerable` signifie en pratique « répertoire sous `docs/runs/` ». Un run
     quitte la population en étant déplacé (`docs/archive/runs/` existe). Aucun
     invariant n'épingle l'étendue de la population ; `enumerable: true` est,
     encore, un booléen déclaré.
  2. Toutes les catégories sauf `CURRENT` / `CURRENT_NONCOMPLIANCE` présupposent
     un artefact avec un document **terminal porteur de verdict** au bout d'un
     cycle **par étapes** — c'est-à-dire le protocole de run de ce dépôt. Pour
     `skills`, offert comme type de population, il n'y a ni date ni cycle : le
     mode dégradé laisse trois catégories utilisables et un `PENDING_LIFECYCLE`
     vide de sens, c'est-à-dire **un linter**.
  3. Combiné à GCG-21 : la machinerie distinctive du modèle a **zéro population
     valide** aujourd'hui.
- **Preuve** — inférence structurelle, non mesurée. Partiellement admis par §7
  du modèle (« généricité interne seulement ») — crédit accordé par la revue.
- **Arbitrage** — ouvert. Décide du périmètre. Voir **D2** et **D4**.

### GCG-36 — quatrième voie : l'ancienneté annihile `OVERCLAIM`
`MODEL_FLAW` + `IMPLEMENTATION_DEFECT` · **P0** · CONFIRMED · `AGENT` · source RA-F-A · statut **OPEN**

- **Fait observé** — `classify_run` teste `identity < ADVERSARIAL_APPLIES_FROM
  → HISTORICAL_VALID` en **ligne 176**, **avant** le test `OVERCLAIM` en
  **ligne 197**. Un closeout revendiquant `PASS_ADVERSARIAL` et `CERTIFIED` sans
  bloc validable, porté par une identité antérieure à `applies_from`, est classé
  `HISTORICAL_VALID` : non bloquant, exclu du dénominateur, sans trace.
- **Preuve** — `sed -n '168,215p' tools/vbb-governance-compat.py`, vérifié par
  l'agent principal. Démonstration de la revue sur trois runs synthétiques en
  répertoire temporaire, corps de closeout identique :

  ```
  2026-07-28_1500_in-window-claims  → OVERCLAIM        blocking=True
  2026-07-27_0900_renamed-claims    → HISTORICAL_VALID blocking=False
  2026-06-01_0900_ancient-claims    → HISTORICAL_VALID blocking=False
  ```

- **Aggravation mesurée par l'agent principal** — le commentaire des lignes
  195-196, immédiatement au-dessus de la branche `OVERCLAIM`, énonce :
  *« An unsupported positive claim outranks every other reading, including the
  historical one. Age does not make a false PASS less believed. »*
  **L'ordre des branches rend ce commentaire faux.** C'est la **deuxième fausse
  déclaration active dans le même fichier**, après celle des deux bornes
  (GCG-09).
- **Conséquence** — le modèle §4.2 et l'invariant I5 affirment tous deux la
  primauté d'`OVERCLAIM` sur la lecture historique. L'implémentation de
  référence la contredit. C'est **la quatrième voie de blanchiment**, et elle
  vise la seule catégorie que le modèle déclare non migrable, non ledgerable et
  immédiatement bloquante.
- **Effets en cascade** :
  - `03` §2 et §4.1 comptaient trois voies ; il y en a quatre.
  - La condition d'arrêt de `R-5` (« échec si une quatrième voie est trouvée »)
    est **remplie avant l'ouverture du run**.
  - La **preuve** du P0 (GCG-26) est atteignable par renommage, même si la
    question de dépôt reste indépendante.
  - GCG-22 est réfuté dans sa direction de correction.
- **Arbitrage** — ouvert. **Correction mécanique et sans décision préalable** :
  le modèle §4.2 énonce déjà la règle, l'implémentation ne la suit pas. Réparer
  ajoutera des `OVERCLAIM` bloquants issus des 148 `HISTORICAL_VALID` actuels ;
  le nombre doit être mesuré et publié.

---

## 6. Entrées portées — hors arbitrage de ce run

Enregistrées pour ne pas les perdre. Aucune n'est arbitrée ici, et aucune n'est
close.

| ID | Source | Fait | Disposition dans ce run |
|---|---|---|---|
| GCG-C1 | R1021 `G7` | le hook pre-commit gate sur la clôture complète en annonçant valider les sections du plan ; un run en cours ne peut être committé sans être clos | **différé par décision explicite de l'utilisateur** vers un run dédié |
| GCG-C2 | R1021 `G8` | `--validate-plan` exige `ended_at` sur le plan d'un run ouvert | porté, non arbitré |
| GCG-C3 | R1050 `G9` | code touché avec `can_code_start=false` — déviation déclarée | porté ; ce run ne la reproduit pas (aucun code écrit) |
| GCG-C4 | ST `A5` | 5 pins de corpus écrits sous une contrainte « aucun code » — l'obligation de corpus est en amont de toute contrainte de périmètre qu'un run se donne | porté ; **lié à GCG-25**, qui en est la face symétrique |
| GCG-C5 | R1021 | R3, R4, R5 du plan de remédiation restent entiers | porté, non arbitré |
| GCG-C6 | AUD-F8 | `TEMPORAL_PROVENANCE.md` obsolète ; la dashboard relabellise des artefacts neufs en preuve historique | **OPEN au registre du dépôt, propriétaire distinct** ; cité par GCG-13, non absorbé |

## 7. Ce que ce registre n'établit pas

- Il ne tranche aucune décision normative. Les 8 décisions sont posées en
  `05_DECISIONS_REQUIRED.md`, aucune n'est prise ici.
- Il ne monte la confiance d'aucun constat. GCG-28 reste `PLAUSIBLE` faute
  d'instruction ; GCG-35 reste `INFERRED` faute de règle externe testée.
- Il ne re-mesure pas les démonstrations E1–E5 de la revue indépendante, qui ont
  été conduites sur des runs synthétiques en répertoire temporaire. Elles sont
  citées comme telles.
- Il ne clôt pas le verdict rouge de `vbb-governance-compat.py`. `2/15` et
  `verdict: FAIL` restent la mesure, et ce run ne la déplace pas.
