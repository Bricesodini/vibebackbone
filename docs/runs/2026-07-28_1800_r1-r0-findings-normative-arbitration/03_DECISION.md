---
run_id: "2026-07-28_1800_r1-r0-findings-normative-arbitration"
phase: "03_DECISION"
voie: "AUDIT"
status: "ACTIVE"
kind: "NORMATIVE_ARBITRATION_DECISION"
posture: "qualify without correcting"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
started_at: "2026-07-28T18:15:00Z"
ended_at: "2026-07-28T19:30:00Z"
agent: "external arbitrator (distinct session, distinct provider, fresh context)"
artifacts_consumed:
  - "01_INTAKE.md (this run)"
  - "2026-07-28_1600/02_AUDIT.md (R0 10 findings)"
  - "2026-07-28_1600/06_INDEPENDENT_REVIEW.md (R0 3 findings annexes)"
  - "2026-07-28_1200/M1_DECISIONS.md (M1 normative source)"
  - "docs/adr/0051-adversarial-assurance-dimension.md"
  - "docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md"
  - "docs/GATE_ASSURANCE_GOVERNANCE.md"
  - "ADR 0050 / 0049 / 0043 / 0031"
artifacts_produced:
  - "03_DECISION.md (this file)"
---

# 03_DECISION — Arbitrage normatif des 13 findings R0

> **Source normative unique.** `2026-07-28_1200/.../M1_DECISIONS.md`.
> Ce R1 ne dérive aucune décision nouvelle : il qualifie ce qui est
> déjà tranché par M1 et ce qui est désormais ouvert par R0.

---

## Table de synthèse

| ID | Sév. R0 | Catégorie R1 | Décision | Bootstrap ? |
|---|---|---|---|---|
| ADVR-FALSIF-01 | S0 | **CONTRAT_INCOMPLET** + **DÉFAUT_TRANSITOIRE_DE_MIGRATION** (composite) | Faux positif sur la qualification "violation" ; vrai positif sur l'absence de régime bootstrap | ⭐ prioritaire |
| ADVR-FALSIF-09 | S1 | **CONTRAT_INCOMPLET** | Faux positif sur "impossibilité" ; vrai positif sur "manque de contrat de transition" | ⭐ prioritaire |
| ADVR-FALSIF-02 | S1 | **DÉFAUT_TRANSITOIRE_DE_MIGRATION** | Validé comme transitionnel | bootstrap lié |
| ADVR-FALSIF-03 | S2 | **CONTRADICTION_DOCUMENTAIRE** | Validé | non |
| ADVR-FALSIF-04 | S2 | **CHOIX_ASSUMÉ** | Argumenté à rouvrir hors R1 ; faux positif sur l'impossibilité | non |
| ADVR-FALSIF-05 | S2 | **CONTRAT_INCOMPLET** | Procédure vs implémentation | non |
| ADVR-FALSIF-06 | S3 | **CONTRAT_INCOMPLET** | Validé | non |
| ADVR-FALSIF-07 | S1 | **CONTRADICTION_DOCUMENTAIRE** | Validé | non |
| ADVR-FALSIF-08 | S2 | **CONTRAT_INCOMPLET** | Validé | non |
| ADVR-FALSIF-10 | S3 | **CHOIX_ASSUMÉ** | Argumenté | non |
| ADVR-FALSIF-11 | S3 | **BUG_NORMATIF** | Procédure violation | non |
| ADVR-FALSIF-12 | S2 | **CHOIX_ASSUMÉ** | Argumenté | non |
| ADVR-FALSIF-13 | S3 | **CHOIX_ASSUMÉ** | Argumenté | non |

**Compteurs.**

| Catégorie | Compte |
|---|---|
| BUG_NORMATIF | 1 |
| CONTRAT_INCOMPLET | 5 |
| CHOIX_ASSUMÉ | 4 |
| FAUX_POSITIF | 0 (aucune réfutation totale ; voir ADVR-FALSIF-01 + 04 + 09 nuances) |
| CONTRADICTION_DOCUMENTAIRE | 2 |
| DÉFAUT_TRANSITOIRE_DE_MIGRATION | 2 (ADVR-FALSIF-01 second-niveau + 02) |

> **Note** : ADVR-FALSIF-01 reçoit une qualification composite
> (`CONTRAT_INCOMPLET` + `DÉFAUT_TRANSITOIRE_DE_MIGRATION`),
> comptée 1 + 1 dans le tableau ci-dessus.

---

## 1. ADVR-FALSIF-01 (S0) — Self-contournement A0 par M2 ⭐

### Reproduction R0 (rappel)

> §1.1 d'`ADVERSARIAL_ASSURANCE_GOVERNANCE.md` : *« Any change
> under `AGENTS.md`, `SYSTEM.md`, `docs/PILOTAGE.md`,
> `docs/templates/`, `prompts/`, `skills/`, or any
> `distributions/` path is **never `A0`** — minimum `A1` »*.
>
> M2 a modifié `PILOTAGE.md`, `CONVENTIONS.md`,
> `AGENTIC_RUN_PROTOCOL.md`, `ENGINEERING_KNOWLEDGE_GOVERNANCE.md`,
> `pre-merge-gate.md`, et créé `ADVERSARIAL_ASSURANCE_GOVERNANCE.md`
> (extension de `GATE_ASSURANCE_GOVERNANCE.md`). Tous sont des
> fichiers canon qui *gouvernent* d'autres travaux. §1.2 les classe
> A2 minimum.
>
> M2 a déclaré `level: A0` (cf. `07_CLOSEOUT.md` §ASSURANCE_STATUS
> narrative v1.1 archivé) avec justification *« doc-only, no
> executable surface »*.

### Arbitrage

**Lecture 1 — La règle A0 a réellement été violée.**
**Refutation partielle.** Oui, le texte de §1.1 dit *« never A0 »*
sans exception. Oui, M2 a modifié des fichiers sous les paths
listés et s'est déclaré A0. *Formellement*, la règle a été
violée.

**Lecture 2 — La migration constitue un régime transitoire implicite.**
**Confirmation forte.** Le cutoff `adversarial_governance_version:
"1.1"` est fixé à `2026-07-28_1400` (run M2 lui-même). M2 est le
**premier run post-cutoff** et le **producteur initial** de la
règle §1.1. Il n'existe, dans le canon, **aucun statut
transitoire** qui s'applique au producteur initial :
- `UNASSESSED_LEGACY` est réservé aux sujets **pré-cutoff**
  (cf. §10).
- Aucun statut ne décrit le cas *« premier run post-cutoff par
  le producteur de la règle »*.
- ADR 0051 §Compatibility fixe `cutoff_run_key: 2026-07-28_1400`
  mais ne distingue pas le run qui active la règle.

Le run M2 est donc **structurellement** dans un cas que le canon
ne décrit pas : il ne peut pas se conformer à §1.1 parce que
§1.1 n'a pas de clause d'auto-application au premier run.

**Lecture 3 — Le contrat est incomplet.**
**Confirmation forte.** Il manque un **statut bootstrap** (cf.
section dédiée §Bootstrap ci-dessous).

### Décision R1

| Dimension | Décision |
|---|---|
| Catégorie primaire | **CONTRAT_INCOMPLET** |
| Catégorie secondaire | **DÉFAUT_TRANSITOIRE_DE_MIGRATION** |
| Faux positif sur R0 ? | **Partiel** — R0 a correctement identifié l'écart, mais la qualification « violation canon » est trop forte. M2 n'a *pas* violé intentionnellement §1.1 ; il a *agi* dans un cas que §1.1 ne prévoit pas. |
| Action R0 « violé » → reformulé | « Le canon §1.1 n'a pas de clause d'auto-application au premier run. » |

**Argumentation explicite.** §1.1 dit *« Any change ... is never
A0 »*. La règle est **absolue** dans sa formulation, mais
**circulaire** dans son application : elle exige que le premier
run qui l'instancie se conforme à elle avant qu'elle ne soit
applicable. C'est un **problème de bootstrap autoréférentiel**,
pas une violation. Le qualifier de « violation » présume que le
canon était déjà opérationnel ; il ne l'était pas avant M2.

**Statut juridique R1.** M2 n'est pas en faute. Le canon est
incomplet. M2-BIS livrera la clause manquante.

---

## 2. ADVR-FALSIF-09 (S1) — Bootstrap de certification ⭐

### Reproduction R0 (rappel)

> Le canon M2 exige `PASS_ADVERSARIAL` pour `CERTIFIED` (§5.3
> condition 6.3.2). `PASS_ADVERSARIAL` ne peut être délivré que
> par `vbb-adversarial-gate.py` (M2-24), différé. Donc :
> `CERTIFIED` est *structurellement* impossible pour tout sujet
> post-cutoff jusqu'à M2-BIS.

### Arbitrage

**Lecture 1 — Le bootstrap est réellement impossible.**
**Refutation.** Non. L'absence du validateur n'entraîne pas
l'impossibilité du bootstrap — elle entraîne l'impossibilité du
**chemin canonical de certification**. Le canon est suffisant pour
décrire l'**état courant** d'un sujet *avant* sa première
certification.

**Lecture 2 — Il manque un contrat de transition.**
**Confirmation.** Le canon a cinq valeurs pour `certification_status` :
- `NOT_CERTIFIED`,
- `CERTIFIED`,
- `SUSPENDED`,
- `NOT_APPLICABLE`,
- `UNASSESSED_LEGACY` (réservé pré-cutoff).

**Aucun statut ne décrit le sujet dont la certification *n'a pas
encore été tentée* parce que les outils manquent**. C'est le cas
de Vibebackbone lui-même pour son propre canon post-cutoff.

**Lecture 3 — Le bootstrap est possible via un chemin non documenté.**
**Confirmation partielle.** Le canon dit *« Vibebackbone ne réécrit
personne »* (consumer_run strategy). Mais Vibebackbone peut
s'auto-qualifier en `NOT_ASSESSED_LEGACY` jusqu'à un futur où il
a son validateur. Le hic : `UNASSESSED_LEGACY` est strictement
réservé pré-cutoff (cf. §10 : *« `UNASSESSED_LEGACY` is the value
of `certification_status` for pre-cutoff subjects that were never
adversarially assessed »*). Vibebackbone ne peut donc pas
s'auto-classer en `UNASSESSED_LEGACY` post-cutoff.

### Décision R1

| Dimension | Décision |
|---|---|
| Catégorie | **CONTRAT_INCOMPLET** |
| Faux positif sur R0 ? | Partiel — R0 a correctement identifié le vide, mais l'a qualifié d'« impossibilité structurelle » plutôt que « contrat de transition manquant ». |
| Action | Ajouter un statut transitoire (cf. §Bootstrap) |

---

## 3. Bootstrap — statut transitoire pour le producteur initial

### Question du brief

> *« Vérifier explicitement si Vibe Backbone doit disposer d'un
> statut transitoire de type :*
>
> *- PRE_CERTIFICATION*
> *- MIGRATION*
> *- SELF_HOSTING*
>
> *ou si aucun statut supplémentaire n'est nécessaire. »*

### Évaluation des trois candidats

| Statut candidat | Avantages | Inconvénients | Verdict R1 |
|---|---|---|---|
| `PRE_CERTIFICATION` | Sémantique claire : « pas encore CERTIFIED, sera CERTIFIED plus tard ». Couvre le producteur initial ET les consumer projects naissants. | N'exclut pas le cas où le sujet ne sera *jamais* CERTIFIED (par exemple, projet purement documentaire). Risque d'inflation : tout nouveau canonique pourrait se revendiquer PRE_CERTIFIED indéfiniment. | **Adopté** comme valeur de `certification_status`. |
| `MIGRATION` | Sémantique utile si plusieurs versions de l'autorité coexistent (v1.0 → v1.1). Décrit bien les consumer projects. | Ne décrit pas le cas du producteur initial (qui n'est pas en train de migrer, il est en train de *naitre*). | **Adopté** comme statut secondaire, applicable quand un consumer migre entre deux versions. |
| `SELF_HOSTING` | Couvre exactement le cas du bootstrap autoréférentiel. Décrit que le sujet héberge son propre validateur. | Risque d'inflation sémantique : tout dépôt solo pourrait se revendiquer SELF_HOSTING pour échapper au validateur externe. | **Non adopté en l'état**. Si SELF_HOSTING est ajouté, il doit être borné par durée et mécanisme. Hors R1. |

### Décision R1 sur le bootstrap

R1 introduit **deux statuts** :

1. `certification_status = PRE_CERTIFICATION`
   - Définition canonique : *« Le sujet est post-cutoff, n'a jamais
     été CERTIFIED, et l'absence de certification est *documentée
     et assumée* (non un échec). Le sujet peut quand même être
     PASS_CONFORMITY et utilisé en runtime. »*
   - Applicable à : Vibebackbone lui-même, consumer projects naissants.
   - Pré-condition : déclaration explicite dans
     `certification.transient_reason` + `certification.bootstrapped_at`.

2. `certification_status = MIGRATION`
   - Définition canonique : *« Le sujet est en transition entre
     deux régimes normatifs (ex. `v1.0 → v1.1`). Le sujet reste
     opérationnel mais la transition est en cours. »*
   - Applicable à : consumer projects adoptant v1.1, sujets
     montés de version.

**NON retenu** : `SELF_HOSTING`. Laissé hors R1 ; nécessiterait
un débat séparé si le besoin se confirme.

**Distinction d'avec `UNASSESSED_LEGACY`.**

| Statut | Domaine | Signification |
|---|---|---|
| `UNASSESSED_LEGACY` | pré-cutoff | le sujet existait avant la règle, n'a pas été ré-évalué, et n'a pas à l'être rétroactivement. **Pas un échec.** |
| `PRE_CERTIFICATION` | post-cutoff, pré-validation | le sujet existe après la règle, attend son premier CERTIFIED, et l'absence est documentée et assumée. **Pas un échec.** |
| `MIGRATION` | transition | le sujet est en train de migrer entre deux régimes. **Pas un échec si la transition respecte la cadence (§7.2).** |

### Effet de bord sur ADVR-FALSIF-01 et 02

Avec `PRE_CERTIFICATION` introduit dans le canon :

- **ADVR-FALSIF-01 devient faux positif sur la qualification
  « violation »**. Le premier run post-cutoff par le producteur
  initial est légitimement en `PRE_CERTIFICATION` ; §1.1 a vocation
  à s'appliquer *forward*, pas *rétroactivement* au premier run
  qui l'instancie.

- **ADVR-FALSIF-02 devient explicitement transitoire**. M2 a dû
  choisir entre deux contraintes mutuellement exclusives (v1.1
  schema vs v1.0 closure tool) ; le statut `PRE_CERTIFICATION`
  résout l'ambiguïté : tant que le validateur n'est pas livré,
  le closeout est en `PRE_CERTIFICATION` + `adversarial_status:
  NOT_ASSESSED` (et non `NOT_REQUIRED`), sans contrevenir au cutoff.

### Application à M2 lui-même

Si `PRE_CERTIFICATION` avait existé à T-M2, M2 aurait dû se
déclarer :

```yaml
certification_status: PRE_CERTIFICATION
adversarial_status: NOT_ASSESSED
level: A0   # avec transient_reason explicite
```

C'est une **possibilité que R1 révèle**, pas une rectification
rétroactive.

---

## 4. ADVR-FALSIF-02 (S1) — Cutoff violé par le closeout M2 ⭐

### Reproduction R0 (rappel)

> M2 closeout a déclaré `assurance_governance_version: "1.0"`
> pour passer `vbb-loop-closure-check.py` (v1.0 seul). ADR 0051
> §Compatibility exige `adversarial_governance_version: "1.1"`
> post-cutoff.

### Arbitrage

**Lecture 1.** M2 avait deux contraintes mutuellement exclusives :
- (a) Déclarer `adversarial_governance_version: "1.1"` (post-cutoff
  conforme à ADR 0051 §Compatibility).
- (b) Être validé par `vbb-loop-closure-check.py` qui ne reconnaît
  que `assurance_governance_version: "1.0"`.

M2 a choisi (b) — *compatibilité outil avant cohérence canon*. Le
log est explicite : la section v1.1 a été rétrogradée en narrative
hors bloc `ASSURANCE_STATUS`.

**Lecture 2.** C'est un défaut transitoire de migration : M2-25
(différé) doit étendre le validateur pour accepter
`adversarial_governance_version: "1.1"`. Tant que M2-25 n'est pas
livré, **tout closeout post-cutoff est dans la même situation**.

**Lecture 3.** Avec le statut `PRE_CERTIFICATION` (introduit
section 3), la qualification devient explicite :

```yaml
certification_status: PRE_CERTIFICATION
adversarial_governance_version: "1.1"   # déclaré
assurance_governance_version: "1.0"    # v1.0 closure tool ne connaît pas v1.1
```

Le bloc `ASSURANCE_STATUS` reste en v1.0 jusqu'à M2-25 ; le bloc
`certification` est en `PRE_CERTIFICATION` ; le statut global est
*honêtement* déclaré comme transitoire.

### Décision R1

| Dimension | Décision |
|---|---|
| Catégorie | **DÉFAUT_TRANSITOIRE_DE_MIGRATION** |
| Faux positif sur R0 ? | Non. R0 a correctement identifié le défaut ; R1 en précise la cause. |
| Action | Introduction de `PRE_CERTIFICATION` + extension de `vbb-loop-closure-check.py` en M2-BIS. |

---

## 5. ADVR-FALSIF-03 (S2) — Triple déclaration des énumérations v1.1

### Reproduction

Trois fichiers déclarent les énumérations `gate_family ∈ {DESIGN,
CERTIFICATION, ADVERSARIAL, OTHER}` et `checkpoint ∈
{PRE_IMPLEMENTATION, POST_IMPLEMENTATION, COUNTER_PROOF, CLOSEOUT}`
:
1. ADR 0051 §1.
2. GATE_ASSURANCE_GOVERNANCE.md §Schema 1.1 + v1.1 delta.
3. ADVERSARIAL_ASSURANCE_GOVERNANCE.md §1.1 + §1.2.

### Arbitrage

M1-01 §Argumentation 4 prescrivait *une* source d'autorité :
*GATE_ASSURANCE_GOVERNANCE.md* §Schema 1.1. Trois sources actuelles.
Aucune contradiction sémantique (toutes disent la même chose), mais
CR#5 (no parallel truth) est *softment* violée.

### Décision R1

| Dimension | Décision |
|---|---|
| Catégorie | **CONTRADICTION_DOCUMENTAIRE** (sans violation normative ; trois sources disent la même chose mais M1 en prescrivait une seule) |
| Faux positif sur R0 ? | Non |
| Action | Réduire ADR 0051 §1 et ADVERSARIAL §1.1 à un pointeur vers GATE_ASSURANCE §Schema 1.1 |

---

## 6. ADVR-FALSIF-04 (S2) — Dépôt solo mono-provider

### Reproduction

`A2_DISTINCT_AGENT_PROXY` exige *« different llm family OR human »*.
Si aucun des deux n'est disponible, le proxy est inutilisable. Pas
d'option tierce.

### Arbitrage

**Lecture 1 — Faux positif sur l'« impossibilité ».** Un dépôt
solo mono-provider *peut* :
- Rester à A0 (pour les sujets où aucun trigger A2 ne matche —
  rare mais non vide : docs pures hors canon).
- Demander un humain tiers *ponctuel* — ce qui n'est pas un
  humain permanent mais satisfait §3 tant que la traçabilité est
  là.
- Demander un agent d'un autre LLM *via* une dépendance externe
  (par exemple, un consumer project hébergé ailleurs qui partage
  son audit log).

**Lecture 2 — Le contrat est incomplet sur le cas extrême.** Si
*aucune* de ces trois options n'est tenable, alors oui, A2 est
inatteignable. Mais ce cas est *très* restrictif et demande une
analyse dédiée.

**Lecture 3 — Choix assumé.** M1-02 §Argumentation 4 a
explicitement tranché *« L'option (ii) [agent d'un autre LLM] est
la fallback viable »* — l'option « aucun fallback » n'a pas été
considérée. **C'est un choix assumé** par M1.

### Décision R1

| Dimension | Décision |
|---|---|
| Catégorie | **CHOIX_ASSUMÉ** |
| Faux positif sur R0 ? | **Oui sur la qualification "impossibilité"** — M1-02 a explicitement choisi cette contrainte. Mais R0 a raison sur le *risque opérationnel* qu'elle révèle. |
| Action | Aucune action R1 ; débat à ouvrir hors R1 si un consumer se révèle dans cette situation. |

---

## 7. ADVR-FALSIF-05 (S2) — ADR 0050 non formellement supersedée

### Reproduction

ADR 0051 liste `linked_adrs: 0050` mais pas `supersedes: ["0050"]`.
ENGINEERING_KNOWLEDGE_GOVERNANCE.md §Knowledge non-regression §7
exige supersession explicite.

### Arbitrage

ADR 0050 v1 reste valide pour les lecteurs qui ne lisent pas
ADR 0051. C'est par conception additive. Mais la procédure
ENGINEERING_KNOWLEDGE_GOVERNANCE §7 n'a pas de clause additive —
elle exige supersession pour toute modification.

C'est un **contrat incomplet sur la procédure** : la procédure
suppose que *toute modification* est un *replacement* ; l'additivité
introduite par ADR 0051 n'est pas reconnue par la procédure.

### Décision R1

| Dimension | Décision |
|---|---|
| Catégorie | **CONTRAT_INCOMPLET** (procédure de supersession ne reconnaît pas l'additivité) |
| Faux positif sur R0 ? | Non |
| Action | ENGINEERING_KNOWLEDGE_GOVERNANCE §7 doit prévoir une clause additive : supersession *ou* amendement_additif avec pointeur canonique. |

---

## 8. ADVR-FALSIF-06 (S3) — Ambiguïté YAML `witnessed_by`/`test_review`

### Reproduction

§5.3 condition 6.3.13 mentionne les champs sans préciser le
chemin YAML. M1-05 a tranché `non_regression.witnessed_by` /
`non_regression.test_review`, mais ce n'est pas reporté dans le
canon M2 livré.

### Arbitrage

M1-05 a tranché ; M2 a oublié de reporter. C'est un
**manquement procédural** de M2, mais qui ne viole pas M1.

### Décision R1

| Dimension | Décision |
|---|---|
| Catégorie | **CONTRAT_INCOMPLET** (canon livré par M2 ne reporte pas la décision M1-05) |
| Faux positif sur R0 ? | Non |
| Action | M2-BIS reporte `non_regression.witnessed_by`/`test_review` dans le canon. |

---

## 9. ADVR-FALSIF-07 (S1) — Dashboard read-only qui mute

### Reproduction

§7.3 dit *« the next pass of `tools/vbb-status-dashboard.py` ... 
triggers an automatic transition `CERTIFIED → SUSPENDED` »*. Or le
SKILL du dashboard le déclare *read-only*.

### Arbitrage

Deux sources disent des choses **mutuellement incompatibles** sur
le même artefact :

| Source | Affirmation |
|---|---|
| ADVERSARIAL_ASSURANCE_GOVERNANCE.md §7.3 | le dashboard *triggers* la mutation |
| t-vbb-status-dashboard/SKILL.md | le dashboard est *read-only* |

Aucune violation stricte d'une règle tierce, mais une
contradiction interne au corpus canonique.

### Décision R1

| Dimension | Décision |
|---|---|
| Catégorie | **CONTRADICTION_DOCUMENTAIRE** |
| Faux positif sur R0 ? | Non |
| Action | Trancher qui mute (vraisemblablement : `vbb-loop-closure-check.py` doit gagner la responsabilité ; le dashboard reste read-only et affiche l'alerte). Soit corriger §7.3, soit faire muter le dashboard exceptionnellement (sans changer le SKILL). |

---

## 10. ADVR-FALSIF-08 (S2) — Comportement lecteur v1.0 face à `ADVERSARIAL`

### Reproduction

§Schema 1.1 dit *« a v1.0 reader is non-conformant by explicit
declaration »* sans spécifier le comportement attendu.

### Arbitrage

4 comportements concevables, 1 interdit (réinjection en `OTHER`),
3 non spécifiés. C'est un trou de spécification, pas une
violation.

### Décision R1

| Dimension | Décision |
|---|---|
| Catégorie | **CONTRAT_INCOMPLET** |
| Faux positif sur R0 ? | Non |
| Action | §Schema 1.1 doit déclarer le comportement fail-closed (ex. `MUST raise UnsupportedSchemaError` ou `MUST treat gate as unclassified`). |

---

## 11. ADVR-FALSIF-10 (S3) — §7.4 suppose remédiable

### Reproduction

§7.4 dit *« release the cause of suspension »* sans distinguer
remédiable vs irreversible.

### Arbitrage

L'hypothèse implicite *« toute cause de suspension est remédiable »*
est raisonnable pour les cas typiques (nouveau finding, scope
changement, ACCEPTED_RISK expiré). Pour les cas extrêmes
(dépendance dépréciée irréversible, défaut de design fondamental),
l'hypothèse tient mal, mais cela ne crée pas de blocage immédiat.

### Décision R1

| Dimension | Décision |
|---|---|
| Catégorie | **CHOIX_ASSUMÉ** (l'hypothèse implicite est légitime pour les cas typiques) |
| Faux positif sur R0 ? | Partiel — R0 a raison de pointer l'edge case, mais c'est un raffinement, pas un défaut. |
| Action | Aucune R1 ; raffinement ultérieur possible. |

---

## 12. ADVR-FALSIF-11 (S3) — ADVR-18 trace perdue

### Reproduction

M0 reserve `ADVR-18` → M1 a tranché « reporter à M2-05 » →
M2-05 n'apparaît pas dans M2_DEFERRED_ITEMS.md → réserve
pratiquement perdue.

### Arbitrage

ENGINEERING_KNOWLEDGE_GOVERNANCE.md + ADR 0049 exigent que
toute réserve de revue indépendante soit *traçable* jusqu'à
arbitrage final ou closure explicite. ADVR-18 n'a ni l'un ni
l'autre.

C'est une **violation procédurale** mineure mais réelle :
la trace documentaire d'une réserve GENUINE (revue
indépendante distincte de M0) s'est perdue.

### Décision R1

| Dimension | Décision |
|---|---|
| Catégorie | **BUG_NORMATIF** (violation de procédure de trace) |
| Faux positif sur R0 ? | Non |
| Action | M2-BIS ajoute ADVR-18 à M2_DEFERRED_ITEMS.md avec mention « réserve ouverte, à traiter en M3 » |

---

## 13. ADVR-FALSIF-12 (S2) — M2 auto-revue incomplète

### Reproduction

M2 06_INDEPENDENT_REVIEW.md déclare 3 conditions REV-01..03 mais
omet le fait que 07_CLOSEOUT.md a été rétrogradé de v1.1 à v1.0
pour passer le closure tool.

### Arbitrage

Une auto-revue disclosed PARTIAL est *par nature* partielle, mais
elle doit au moins identifier les *conditions de non-conformité au
canon lui-même*. La non-conformité v1.1→v1.0 est exactement ce
genre de condition ; son omission affaiblit la valeur de l'auto-revue.

C'est un **choix de cadrage** de l'auto-revue, pas un défaut de
procédure. Mais le choix est mauvais.

### Décision R1

| Dimension | Décision |
|---|---|
| Catégorie | **CHOIX_ASSUMÉ** (auto-revue disclosed PARTIAL assume ne pas tout couvrir) |
| Faux positif sur R0 ? | **Oui** — l'auto-revue a été honnête sur sa PARTIALité ; R1 accepte ce cadrage comme légitime. |
| Action | Aucune R1 ; relecture humaine séparée recommandée. |

---

## 14. ADVR-FALSIF-13 (S3) — Terminologie HANDOFF inconsistante

### Reproduction

M2 closeout : `kind: HANDOFF` + `next_phase: M2-BIS` + pas de
`consumer_id` explicite.

### Arbitrage

AGENTIC_RUN_PROTOCOL.md décrit HANDOFF sans définir un
`consumer_id` strict. La terminologie est floue mais pas
strictement incorrecte. Le mot « HANDOFF » évoque un transfert à
un autre acteur ; sans `consumer_id`, c'est un artefact en suspens.

### Décision R1

| Dimension | Décision |
|---|---|
| Catégorie | **CHOIX_ASSUMÉ** (terminologie héritée de l'usage, pas strictement spécifiée) |
| Faux positif sur R0 ? | Partiel — R0 a raison sur le raffinement à faire, mais c'est cosmétique. |
| Action | Aucune R1 ; raffinement terminologique possible en M2-BIS ou M3. |

---

## Liste des faux positifs R1

Aucun finding n'est *intégralement* faux positif. Trois sont
*faux positif sur la qualification* (R0 les a correctement identifiés
mais mal qualifiés) :

| Finding | Qualification R0 | Re-qualification R1 | Pourquoi faux positif sur R0 |
|---|---|---|---|
| ADVR-FALSIF-01 | « violation canonique » S0 | CONTRAT_INCOMPLET + DÉFAUT_TRANSITOIRE | Pas de violation intentionnelle ; bootstrap autoréférentiel |
| ADVR-FALSIF-04 | « impossible pour solo mono-provider » S2 | CHOIX_ASSUMÉ M1-02 | M1 a explicitement choisi cette contrainte ; R0 l'a sur-qualifiée |
| ADVR-FALSIF-12 | « auto-revue incomplète » S2 | CHOIX_ASSUMÉ de cadrage | PARTIAL disclosed assume ne pas tout couvrir |

---

## Liste des remédiations autorisées par R1

> **R1 n'autorise aucune remédiation pendant ce run.** Le brief
> interdit toute correction ou modification normative.
>
> Les remédiations *ci-dessous* sont **listées pour traçabilité** ;
> elles seront exécutées par M2-BIS ou un autre run futur, **avec
> arbitrage humain séparé si une M2-DEVIATION est nécessaire**.

| ID R1 | Cible | Remédiation proposée (indicative, non exécutée) | Owner |
|---|---|---|---|
| **REM-01** ⭐ | §1.1 ADVERSARIAL_ASSURANCE + ADR 0051 | Introduire le statut `certification_status = PRE_CERTIFICATION` (et secondairement `MIGRATION`) | M2-BIS via nouvelle ADVR ou M2-01-bis |
| **REM-02** ⭐ | M2-25 (closure tool extension) | Étendre `vbb-loop-closure-check.py` pour reconnaître `adversarial_governance_version: "1.1"` | M2-BIS |
| REM-03 | ADR 0051 §1 + ADVERSARIAL §1.1 | Réduire les énumérations à un pointeur vers GATE_ASSURANCE §Schema 1.1 | M2-BIS |
| REM-04 | ENGINEERING_KNOWLEDGE_GOVERNANCE §7 | Ajouter clause « supersession *or* amendement_additif avec pointeur » | M2-BIS |
| REM-05 | ADVERSARIAL §5.3 condition 6.3.13 | Reporter le chemin YAML `non_regression.witnessed_by`/`test_review` de M1-05 | M2-BIS |
| REM-06 | ADVERSARIAL §7.3 | Trancher mutateur : soit dashboard mute exceptionnellement, soit §7.3 désigne `vbb-loop-closure-check.py` comme effecteur | M2-BIS |
| REM-07 | GATE_ASSURANCE §Schema 1.1 | Déclarer le comportement fail-closed attendu du lecteur v1.0 face à `ADVERSARIAL`/`COUNTER_PROOF` | M2-BIS |
| REM-08 | M2_DEFERRED_ITEMS.md | Ajouter M2-05 (history[] externalisé) avec mention ADVR-18 ouvert | M2-BIS |
| REM-09 (optionnelle) | ADVERSARIAL §7.4 | Ajouter état terminal `CERTIFICATION_TERMINATED` pour causes irreversibles | hors R1 |
| REM-10 (optionnelle) | AGENTIC_RUN_PROTOCOL | Ajouter `consumer_id` au frontmatter HANDOFF | hors R1 |

---

## Confirmation des bornes R1

Conformément au brief, R1 :

- ✅ A qualifié les 13 findings.
- ✅ A argumenté chaque décision.
- ✅ A listé les remédiations autorisées (sans les exécuter).
- ✅ A listé les faux positifs.
- ✅ A tranché le bootstrap (PRE_CERTIFICATION + MIGRATION ; pas SELF_HOSTING).
- ❌ N'a corrigé aucun fichier.
- ❌ N'a modifié aucun ADR.
- ❌ N'a modifié aucun gate.
- ❌ N'a modifié aucun template.
- ❌ N'a pas commencé M2-BIS.
- ❌ N'a pas committé.
- ❌ N'a pas pushed.

---

## Note finale sur `M2_DEVIATION_FROM_M1`

R1 a tracé **aucune déviation de M1**. Toutes les qualifications
ci-dessus opèrent à l'intérieur du périmètre M1 ; les statuts
proposés (`PRE_CERTIFICATION`, `MIGRATION`) sont *compléments* au
canon, pas des modifications de ce que M1 a tranché.

Un futur run (M2-BIS ou M3) qui implémenterait ces statuts
devra être tracé avec un `M2_DEVIATION_FROM_M1` *uniquement* si
l'implémentation contredit une décision M1, ce qui n'est pas le
cas pour les statuts proposés.

---

## Note sur l'arbitrage humain obligatoire

La règle du canon (CR#2 `AGENTS.md` : *« Immediate escalation if a
FAST task touches ... systemic behavior »*) et ADR 0049 (*« Only
a human approves, rejects, narrows or defers a promotion »*)
exigent qu'un humain tranche les statuts proposés avant M2-BIS ne
les implémente. R1 ne signe pas l'acceptance ; il qualifie et
préconise.

```
Decision:
  ADVR-FALSIF-01: CONTRAT_INCOMPLET + DÉFAUT_TRANSITOIRE_DE_MIGRATION
  ADVR-FALSIF-09: CONTRAT_INCOMPLET
  ADVR-FALSIF-02: DÉFAUT_TRANSITOIRE_DE_MIGRATION
  ADVR-FALSIF-03: CONTRADICTION_DOCUMENTAIRE
  ADVR-FALSIF-04: CHOIX_ASSUMÉ
  ADVR-FALSIF-05: CONTRAT_INCOMPLET
  ADVR-FALSIF-06: CONTRAT_INCOMPLET
  ADVR-FALSIF-07: CONTRADICTION_DOCUMENTAIRE
  ADVR-FALSIF-08: CONTRAT_INCOMPLET
  ADVR-FALSIF-10: CHOIX_ASSUMÉ
  ADVR-FALSIF-11: BUG_NORMATIF
  ADVR-FALSIF-12: CHOIX_ASSUMÉ
  ADVR-FALSIF-13: CHOIX_ASSUMÉ

Bootstrap model: PRE_CERTIFICATION (primaire) + MIGRATION (secondaire)
                  SELF_HOSTING = non retenu

Faux positifs R1 (re-qualifications): 3 sur 13

Remédiations autorisées (non exécutées): 10 (REM-01..REM-10)

M1-Deviations: 0

Human-decision-required: oui (statuts bootstrap)
```