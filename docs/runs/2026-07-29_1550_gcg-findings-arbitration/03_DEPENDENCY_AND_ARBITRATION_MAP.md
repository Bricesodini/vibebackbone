---
run_id: "2026-07-29_1550_gcg-findings-arbitration"
phase: "03_DEPENDENCY_AND_ARBITRATION_MAP"
voie: "STRUCTUREE"
status: "PARTIAL"
kind: "GOVERNANCE_FINDINGS_ARBITRATION"
agent: "claude-opus-5 (Claude Code)"
started_at: "2026-07-29T13:50:00Z"
ended_at: null
artifacts_consumed:
  - "02_FINDINGS_REGISTER.md"
artifacts_produced:
  - "03_DEPENDENCY_AND_ARBITRATION_MAP.md (this file)"
---

# 03_DEPENDENCY_AND_ARBITRATION_MAP — GCG-ARB-01

## 1. Principe d'ordonnancement

> **Révisé après revue indépendante** (`04_INDEPENDENT_ARBITRATION_REVIEW.md`).
> Le graphe est réordonné (D4 ne précède plus D1/D2 — l'ordre initial était
> circulaire), §3.6 est réécrite, §3.9 corrigée, §4.1 complétée d'une quatrième
> voie, la divergence V3 retirée comme résolue, et **§7 réécrite
> intégralement**. Les énoncés réfutés sont conservés en citation.

Le registre contient 36 constats. Ils ne sont pas 36 problèmes : ce sont
**8 décisions ouvertes** et leurs conséquences. Le graphe ci-dessous ordonne par
*ce qui doit être décidé*, pas par gravité.

Deux règles d'ordonnancement, dérivées du registre :

1. **Une correction technique dont la sémantique dépend d'une décision ouverte
   est invalide, même si elle est correcte.** Elle ne peut être qu'un ajustement
   aux contre-exemples connus — le risque nommé par la mission.
2. **Une décision qui peut retirer le périmètre passe avant celles qui le
   supposent.** Réparer le mécanisme d'un modèle qui duplique un canon existant
   est du travail perdu, quelle que soit la qualité de la réparation.

## 2. Graphe de décisions

```
   SANS DÉCISION    ┌─────────────────────────────────────────┐
   PRÉALABLE        │ GCG-36  quatrième voie de blanchiment    │
                    │ la règle existe (§4.2), le code ne la    │
                    │ suit pas — à réparer et à mesurer        │
                    └─────────────────────────────────────────┘
                              │ conditionne la PREUVE de D0
                    ┌─────────▼───────────────────────────────┐
   INDÉPENDANT      │ D0  la certification v1.1 publiée        │
   URGENT           │     est-elle soutenue ?                  │
                    │     GCG-26 · GCG-27                      │
                    └─────────────────────────────────────────┘

   FONDATIONS       ┌────────────────────────┐  ┌────────────────────────┐
   (rien de         │ D1  coordonnée         │  │ D2  population et      │
    temporel        │     attestée           │  │     immuabilité        │
    n'a de sens     │  GCG-02·10·13          │  │  GCG-01·21·17·35       │
    avant)          └───────┬────────────────┘  └───────┬────────────────┘
                            └──────────┬─────────────────┘
                                       ▼
   PÉRIMÈTRE        ┌─────────────────────────────────────────┐
   (déterminée      │ D4  réconciliation déclaré / dérivé      │
    par D1·D2)      │     avec certification_status            │
                    │     GCG-11 · GCG-34 · (GCG-12)           │
                    └────────────────┬────────────────────────┘
                                     ▼
                    ┌─────────────────────────────────────────┐
   FRONTIÈRES       │ D3  déclaration canonique des deux      │
                    │     bornes : valeur, unité, inclusivité │
                    │     GCG-09 · 08 · 18 · 33 · (12)        │
                    └────────────────┬────────────────────────┘
                                     ▼
   PRÉDICATS        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
   (voies 1 à 3     │ D5 prédicat  │ │ D6 ensemble  │ │ D7 absence   │
    de blanchiment) │ de revendic. │ │ ledgerable   │ │ du porteur   │
                    │ GCG-06·07·20 │ │ GCG-04       │ │ GCG-05       │
                    │      ·28     │ │              │ │              │
                    └──────────────┘ └──────────────┘ └──────────────┘
                                     ▼
   TOTALITÉ         ┌─────────────────────────────────────────┐
                    │ GCG-14 + GCG-03 — réparation conjointe   │
                    │ obligatoire (voir §4.1)                  │
                    └─────────────────────────────────────────┘

   HORS GRAPHE      GCG-15 · GCG-19 — résolveur de closeout : décidables
                    aujourd'hui, à coût normatif nul (voir §4.2)

   TRANSVERSAL      D8  épinglage des constats produits hors run — GCG-25 · C4
                    D12 poursuite du chantier sans acteur A2 — GCG-29
```

> **Réordonné après revue (RA-F-G).** Le graphe initial plaçait D4 **avant**
> D1/D2, « par économie ». C'était circulaire, et le texte de §3.6 le disait
> lui-même : les trois apports propres de GCG dépendent de la fenêtre de dette,
> donc de D1 et D2 ; et §7.3 concluait que sans réponse à D1/D2 le verdict
> devient `DUPLICATES_EXISTING_CANON`, qui **est** la réponse B de D4. Une
> décision déterminée par deux autres ne peut pas les précéder.

Hors graphe, sans dépendance : GCG-22, GCG-23, GCG-24 — corrections
documentaires et de couverture, exécutables dès qu'un run est autorisé à
modifier le modèle. Elles ne conditionnent rien et ne sont conditionnées par
rien, **sauf** que publier un ratio de couverture corrigé n'a de sens qu'après
D1–D7, puisque le jeu d'invariants peut changer.

## 3. Vérification des relations exigées par la mission

La mission demande d'examiner neuf relations en particulier. Chacune est
vérifiée, et trois d'entre elles se révèlent différentes de ce qui était attendu.

### 3.1 GCG-14 (ST-S1) ↔ applicabilité et totalité de la classification
**Relation confirmée, et elle est piégeuse.**

GCG-14 est présenté comme une correction mécanique : le scanner n'implémente
qu'une des trois sources d'applicabilité, il suffit d'ajouter les deux autres.
**C'est faux.** Ajouter les sources 2 et 3 rend immédiatement GCG-03 actif : la
table des catégories n'est pas totale sous l'union, et un artefact rendu
applicable par `started_at` mais positionné avant `applies_from` ne tombe dans
aucune catégorie.

Corriger GCG-14 seul remplace un défaut *latent et prouvé par construction* par
un défaut *actif sur une population réelle*. **Les deux doivent être réparés
dans le même run**, et GCG-03 exige D1 (quelle horloge positionne) et D3 (quelle
borne, quelle inclusivité). GCG-14 n'est donc pas mécanique : il est en bout de
chaîne.

### 3.2 GCG-01 et GCG-02 ↔ coordonnée attestée et immuabilité
**Relation confirmée. Ce sont les deux mêmes défauts, sur deux axes.**

Le modèle a besoin de deux faits sur chaque artefact : *où il se situe*
(coordonnée) et *s'il a changé depuis* (immuabilité). Les deux sont aujourd'hui
**déclarés**, aucun n'est **établi**. C'est une seule pathologie, appliquée deux
fois : le modèle traite des propriétés factuelles comme il traite des frontières
normatives.

Conséquence pour l'ordonnancement : D1 et D2 sont indépendants l'un de l'autre
mais **conjointement nécessaires**. Résoudre l'un sans l'autre laisse la fenêtre
de dette ouverte par l'autre bout. Aucune catégorie historique n'a de sens tant
que les deux ne sont pas fermés.

Conséquence de mesure, souvent oubliée : **la réponse à D1 reclasse jusqu'à
148 artefacts**. Aucune écriture de ledger ne peut précéder D1, sous peine
d'enregistrer des dispositions contre des classifications qui vont changer.

### 3.3 GCG-04 ↔ sémantique du ledger et `HISTORICAL_VALID`
**Relation confirmée. La correction apparente est un piège de réparation défensive.**

Retirer `HISTORICAL_VALID` de `LEDGERABLE` est une ligne. Mais cette ligne
**décide** une question de gouvernance que personne n'a tranchée : l'arbitration
humaine peut-elle *attribuer* une validité historique, ou seulement
*reconnaître* une dette ?

- Si elle le peut, la ligne est fausse et il faut à la place rendre la
  disposition **visible** : compter `HISTORICAL_VALID` ledgeré dans une
  quatrième lecture, distincte des 148 classés par la règle.
- Si elle ne le peut pas, la ligne est juste **mais insuffisante** : il faut
  aussi décider si `applicable` doit continuer d'exclure `HISTORICAL_VALID`,
  sinon une disposition légitime reste invisible dans le dénominateur.

Dans les deux cas la réparation touche la sémantique globale, pas une constante.
**Corriger avant D6 est exactement le risque « réparation adaptée aux
contre-exemples connus ».**

### 3.4 GCG-09 et GCG-08 ↔ les deux bornes et leur inclusivité
**Relation confirmée, et elles se ferment ensemble.**

D3 est la décision la mieux formée du lot : elle a une forme évidente (déclarer
au canon les deux bornes avec valeur, unité, fuseau et inclusivité) et elle
ferme d'un coup GCG-09, GCG-08, GCG-18 et GCG-33, et rend GCG-12 exécutable.

Deux pièges à ne pas manquer en la prenant :
1. **Les directions fail-closed sont opposées** aux deux bouts de l'intervalle.
   Inclure `applies_from` est plus strict ; inclure `enforcement_effective_from`
   est plus permissif. I10 donne une résolution unique (« la plus inclusive »)
   pour les deux, ce qui est incohérent. L'inclusivité doit être déclarée
   **borne par borne**.
2. **Une instance vivante est en jeu**, et c'est la plus embarrassante :
   `2026-07-28_2000_m2-bis`, le run qui a livré l'outil d'enforcement, est
   aujourd'hui `UNKNOWN` — donc dans la fenêtre, donc excusable de ne pas porter
   la vérification qu'il a créée. D3 décide de son sort, et la décision ne doit
   pas être prise en regardant ce cas.

### 3.5 GCG-06 ↔ prédicat de revendication et `OVERCLAIM`
**Relation confirmée, avec une contradiction interne à trancher d'abord.**

D5 ne peut pas se réduire à « déclarer le prédicat » tant que GCG-07 n'est pas
résolu : le modèle documente un exemple (`status: READY` + `FINAL_STATUS:
HANDOFF` = `OVERCLAIM`) que sa propre suite de tests contredit (fixture
`NO_BLOCK`, `status: READY`, assertée `HISTORICAL_VALID`). **Les deux ne peuvent
pas être vrais.** Décider le prédicat, c'est décider lequel des deux tombe.

Effet en aval, souvent sous-estimé : D5 conditionne **GCG-28**. Les 9
dispositions de connaissance positives sans section ne sont des `OVERCLAIM` que
si `EVIDENCE_LINKED` compte comme une revendication au sens du prédicat. Sans
D5, on ne peut pas instruire ces 9 cas — on ne peut que les compter.

### 3.6 GCG-11 ↔ vocabulaire canonique d'assurance existant
**Relation confirmée, et c'est la relation qui peut retirer le périmètre.**

Le canon partitionne déjà la même population par `certification_status` :
`UNASSESSED_LEGACY`, `PRE_CERTIFICATION`, `MIGRATION`, `NOT_CERTIFIED`,
`CERTIFIED`, `SUSPENDED`, `NOT_APPLICABLE`.

**Ce n'est pas une duplication de vocabulaire.** Les deux partitions ne portent
pas sur le même type d'objet :

| | Canon `certification_status` | Catégories GCG |
|---|---|---|
| nature | **déclaré** par le sujet | **dérivé** par un scanner |
| granularité | par sujet | par couple *(artefact, règle)* |
| établissement | 13 conditions §5.3.1 pour `CERTIFIED`, dont une décision humaine enregistrée, `witnessed_by ≠ discovered_by`, liage au corpus, cadence ≤ 90 jours | un code de sortie de sous-processus |

Assimiler `CURRENT` (= `gate_exit == 0`) à `CERTIFIED` reviendrait à **dériver
une certification d'un verdict de conformité** — exactement la collapse qu'I4
interdit et que `build_act` empêche en écrivant `NOT_DERIVABLE_FROM_THIS_GATE`
en dur. De même, assimiler `PENDING_LIFECYCLE` à `NOT_APPLICABLE` réintroduit
l'erreur que le modèle §4.1 documente lui-même : un run en cours n'est pas hors
périmètre.

**Le vrai conflit est déclaré vs dérivé, et il est réel.** Un run pré-cutoff
déclarant `certification_status: NOT_CERTIFIED` est **bloquant** sous le canon
et **`HISTORICAL_VALID`, non bloquant** sous GCG. Deux verdicts sur le même
artefact, aucune règle de préséance (Critical Rule 5). Le seul recouvrement
défendable est `HISTORICAL_VALID` ↔ `UNASSESSED_LEGACY`, et encore : l'un est
par sujet adverse, l'autre par couple.

D4 est donc une **réconciliation** — publier une règle de préséance entre un
champ déclaré et une classification dérivée — et non une décision de périmètre.
Elle est **déterminée par D1 et D2**, puisque les trois apports propres de GCG
(`OVERCLAIM`, `HISTORICAL_NONCOMPLIANCE`, `UNKNOWN`) dépendent tous de la
fenêtre de dette.

> **Réécrite après revue (RA-F-B).** La version initiale produisait une table
> de correspondance concluant à **« cinq catégories sur huit dupliquent le
> canon »**, et tirait de ce chiffre l'ordonnancement D4 → D1/D2 et le second
> pilier du verdict §7.2. La table assimilait des classifications dérivées à
> des statuts déclarés ; la ligne `CURRENT ↔ CERTIFIED` commettait, dans le
> document qui les poursuit, la dérivation de certification qu'I4 interdit.
> **Le chiffre « 5/8 » est retiré.** Ce qui survit est GCG-11 tel qu'écrit au
> registre — la vérité parallèle déclaré/dérivé — dont l'instance est réelle.

### 3.7 GCG-22 ↔ crédibilité de la couverture annoncée
**Relation confirmée, et l'effet est plus large que le constat.**

Le tableau §5 est faux dans les deux sens et l'un de ses trois porteurs est
tautologique. L'effet n'est pas d'avoir trois lignes fausses : c'est que
**l'aveu de couverture était l'argument de crédibilité du document**. Un
document qui dit « voici ce que je ne garantis pas » achète de la confiance sur
cette phrase. Si le décompte est faux, la confiance est achetée sans provision.

Conséquence d'ordonnancement : GCG-22 est indépendant et corrigeable
immédiatement, **mais republier un ratio avant D1–D7 est prématuré**, puisque le
jeu d'invariants lui-même va changer. La correction juste, à court terme, est de
retirer le ratio, pas d'en publier un autre.

### 3.8 GCG-28 ↔ dispositions positives de connaissance
**Relation confirmée, avec une réserve que le stress test avait déjà posée.**

3 des 9 cas sont vérifiés par énumération complète, 6 par balayage de titres
seul. La disposition pourrait être justifiée ailleurs qu'en section dédiée. La
confiance reste `PLAUSIBLE`.

Double dépendance : instruire ces 9 cas exige D5 (est-ce une revendication ?) et
révèle, si la réponse est oui, qu'**une seconde règle entre en dette** — ce qui
double le périmètre d'arbitrage humain et change l'échelle de tout le chantier.
C'est le seul constat dont la résolution peut *augmenter* la charge d'arbitrage
au lieu de la réduire.

### 3.9 GCG-26 / GCG-27 ↔ toute revendication actuelle de certification
**Relation confirmée, et GCG-27 change la nature du problème.**

GCG-26 seul se lisait comme une omission de preuve : une revendication dont on
ne sait pas si elle est dérivable de `2026-07-30_0100`. GCG-27 établit que les
champs `verdict: PASS`, `adversarial_status: PASS_ADVERSARIAL` et
`certification_status: CERTIFIED` ont été **écrits par un commit postérieur à la
clôture du run**, en direction positive.

Ce n'est plus « la preuve manque » mais « le verdict a été écrit hors du moment
où il pouvait être établi ». Conséquences :

- **Aucune disposition de dette n'est admissible.** La mutation est postérieure
  à l'enforcement : c'est un défaut de maintenant, réparable maintenant.
- **D0 ne dépend d'aucune autre *décision*** et ne doit pas attendre le modèle.
  Le modèle a servi à rendre le fait visible ; la révision de la certification
  publiée est une question de dépôt, pas de modèle.
- **Mais sa *preuve* dépend de GCG-36.** Renommé sous une identité antérieure à
  `applies_from`, `2026-07-30_0500` cesse d'être un `OVERCLAIM` et devient
  `HISTORICAL_VALID`, non bloquant. La question de dépôt reste indépendante ; la
  classification qui l'a rendue visible ne l'est pas. **GCG-36 doit être réparé
  avant R-0**, faute de quoi le P0 repose sur une classification qu'un renommage
  suffit à faire disparaître.

> **Corrigé après revue (RA-F-A).** La version initiale affirmait sans réserve
> que « D0 ne dépend d'aucune autre décision ». La distinction décision/preuve
> manquait.
- **La contrainte permanente s'applique** : si la revendication n'est pas
  soutenue, c'est la revendication qui tombe. Ne pas fabriquer de bloc adverse
  pour rendre le run vert ; ne pas rétrograder un niveau pour obtenir le vert.

## 4. Ce qui ne peut pas être réparé maintenant

### 4.1 Corrections invalides tant qu'une décision est ouverte

| Correction apparente | Bloquée par | Pourquoi la faire maintenant serait une réparation défensive |
|---|---|---|
| retirer `HISTORICAL_VALID` de `LEDGERABLE` | **D6** | décide silencieusement ce que l'arbitration a le droit d'attribuer |
| réparer le parseur de fences d'`OVERCLAIM` | **D5** | ajuste le code aux deux contre-exemples connus sans déclarer le prédicat |
| définir ce que signifie l'absence du porteur | **D7** | une déclaration positive « ouvert, phase N » remplacerait une absence invérifiable par une **déclaration** invérifiable |
| ajouter les sources 2 et 3 au scanner | **D1, D3** | transforme un défaut latent en défaut actif (§3.1) |
| dériver la coordonnée de la date d'auteur git | **D1** | change la classification de jusqu'à 148 artefacts sans décision |
| corriger la borne `2000` dans le code | **D3** | fige au code une frontière que le canon ne déclare pas — c'est le défaut GCG-09 lui-même |
| republier un ratio de couverture | D1–D7 | le jeu d'invariants va changer |
| écrire le ledger, le Migration Engine, le câblage CI | D1, D2, D3, D6 | enregistrerait des dispositions contre des classifications provisoires |

### 4.2 Corrections exécutables sans décision préalable

Six, et aucune n'est autorisée dans ce run (contrainte C3) :

- **GCG-36** — rétablir la primauté d'`OVERCLAIM` sur la lecture historique. La
  règle est déjà écrite au modèle §4.2 et dans le commentaire du code lui-même ;
  seul l'ordre des branches la contredit. **Priorité la plus haute des six** :
  la preuve du P0 en dépend. La réparation doit publier le nombre d'`OVERCLAIM`
  bloquants nouvellement issus des 148 `HISTORICAL_VALID`.
- **GCG-22** — corriger le tableau §5, ou retirer le ratio (recommandé, §3.7) —
  en tenant compte du fait qu'I5 n'est **pas** couvert (voir la révision du
  constat).
- **GCG-24** — supprimer §6.2 et son cache. La prémisse est au mieux prématurée,
  et les deux contournements disparaissent avec elle.
- **GCG-09, volet code** — le commentaire d'en-tête de
  `vbb-governance-compat.py` affirme que les deux bornes sont lues du canon.
  C'est faux, et une fausse déclaration active dans le code est un défaut
  indépendant de la décision D3. La corriger n'anticipe aucune décision : elle
  restaure l'exactitude d'un aveu.
- **GCG-19** — remplacer le départage par `st_mtime` par un ordre dérivé du
  contenu. Décidable aujourd'hui, à coût normatif nul.
- **GCG-15** — appliquer le résolveur unique déjà spécifié par I11.

> **Complété après revue (RA-F-F).** La version initiale plaçait GCG-19 et
> GCG-15 derrière D7. C'était un mal-regroupement : D7 demande ce que signifie
> **l'absence** du porteur, tandis que GCG-19 départage plusieurs porteurs
> **présents** et que GCG-15 choisit lequel lire. Aucune des trois options de D7
> ne les décide, et les bloquer derrière elle retardait deux corrections
> gratuites. Le registre le disait lui-même — *« ne ferme pas GCG-05 : un
> résolveur déclaré résout toujours vers "absent" »* — sans en tirer la
> conséquence d'ordonnancement.

## 5. Constats qui mettent en cause le périmètre du modèle

Quatre, et il faut les lire ensemble :

1. **GCG-21 + GCG-01** — la seule population instrumentée échoue à `immutable`,
   et `immutable` est une déclaration que rien n'atteste. Par le mode dégradé du
   modèle, 148 classifications `HISTORICAL_VALID` sont indéfinies et **aucune
   dette n'est admissible**.
2. **GCG-35** — l'autre type de population offert (`skills`) n'est pas `dated`.
   En mode dégradé il reste trois catégories utilisables et un
   `PENDING_LIFECYCLE` vide de sens : un linter.
3. **Conséquence conjointe** — *la machinerie distinctive du modèle n'a
   aujourd'hui aucune population valide.* Ce n'est pas une critique de style :
   c'est l'absence de sujet.
4. **GCG-11** — la classification entre en conflit non résolu avec une partition
   canonique existante, sans règle de préséance entre déclaré et dérivé. Les
   trois catégories sans équivalent canonique sont précisément celles qui
   dépendent de la fenêtre de dette, donc du point 3.
5. **GCG-36** — le seul apport propre du modèle qui soit à la fois spécifié
   (§4.2) **et** implémenté, `OVERCLAIM`, ne respecte pas sa propre règle de
   primauté. Un renommage l'annule. Si l'on retire ce qui dépend d'une fenêtre
   de dette sans population valide, et ce qui ne fonctionne pas, il ne reste du
   modèle qu'une spécification.

## 6. Divergences agent principal / revue indépendante

Conservées visibles, non fusionnées (contrainte C7).

| # | Point | Revue indépendante | Agent principal | Statut |
|---|---|---|---|---|
| **V1** | réparation de la coordonnée (GCG-02) | dériver de la date d'auteur git « entre en collision avec la lettre d'I8 » ; I8 doit être amendé | I8 quantifie sur les **frontières normatives** ; la position d'un artefact est un **fait**, pas une frontière — la dérivation est compatible | **ouvert, D1.** La divergence rend la réparation plus accessible qu'annoncé : je la signale comme m'arrangeant. Elle tient parce que les deux énoncés portent sur des objets différents. Elle établit surtout que **l'énoncé d'I8 ne porte pas la distinction** — ce qui est un constat des deux côtés |
| **V2** | §6.2 (GCG-24) | prémisse « réfutée » par la mesure ; supprimer §6.2 | prémisse **prématurée** : le coût scale avec l'ensemble applicable (15/164), pas avec la population | **convergent sur l'action**, divergent sur le motif. §6.2 est supprimée dans les deux lectures |
| **V3** | population de mesure (GCG-10) | 94 closeouts sur 123 en désaccord, écart max 29 h | 74 sur 105, écart max 22,1 h | **RÉSOLU, divergence retirée.** La seconde revue a re-mesuré sous trois résolveurs : les deux résolveurs donnent une population **identique** (106, dont 75 en désaccord). L'écart venait entièrement des identités à granularité jour. Mon attribution à GCG-15 était fausse, et conserver la divergence au lieu de la mesurer était l'apparence de la discipline, non la discipline |
| **V4** | GCG-07 (exemple G3) | §4.2 et la suite de tests ne peuvent pas être vraies ensemble | **concédé sans réserve** — l'exemple est de moi et il est faux tel qu'écrit | **convergent** |
| **V5** | GCG-22 (couverture §5) | faux dans les deux sens, I4 tautologique | **concédé sans réserve**, les trois points re-vérifiés | **convergent** |

## 7. Verdict de viabilité — dérivé

> **Section réécrite intégralement après revue (RA-F-C, RA-F-B, RA-F-D,
> RA-F-J).** La dérivation initiale était incohérente : elle écartait
> `INSUFFICIENT_EVIDENCE` au motif que *« le manque de preuve porte sur
> l'ampleur »* et `REPAIRABLE_CORE` au motif que l'ampleur est inconnue — deux
> éliminations qui ne peuvent pas tenir ensemble. Son second pilier reposait sur
> le chiffre « 5/8 » que RA-F-B a retiré. Sa condition de bascule était
> malformée. Et son élimination d'`ABANDON` n'était reliée ni à GCG-34 ni à
> GCG-36. Le verdict est **reconstruit**, pas maintenu par inertie.

### 7.1 Élimination des verdicts non retenus

- **`INSUFFICIENT_EVIDENCE`** — écarté, sur un motif d'**existence** et non
  d'ampleur. `git log --format='%G?'` retourne `N` sur 243 des 244 commits :
  aucune signature. Les dates d'auteur et de committer sont réglables,
  l'historique est réinscriptible. **Il n'existe aujourd'hui, dans ce dépôt,
  aucun substrat capable d'attester ni la coordonnée d'un artefact ni son
  immuabilité.** Ce n'est pas une inconnue à mesurer : c'est un fait mesuré. Il
  suffit à établir qu'une redéfinition est nécessaire.
- **`REPAIRABLE_CORE`** — écarté, sur le même motif. Ce verdict affirme que le
  noyau tient après des corrections *clairement bornées*. On ne peut pas borner
  une correction dont le substrat n'existe pas. Les deux options que je
  recommandais initialement pour D1 et D2 — dériver de l'historique git —
  **détectent** les deux contre-exemples connus sans **établir** la propriété :
  c'est la définition de la réparation défensive que ce run avait pour charte
  d'empêcher, et elle était dans mes propres recommandations (RA-F-D).
- **`DUPLICATES_EXISTING_CANON`** — écarté comme verdict actuel, mais **il est
  désormais le verdict de repli le plus probable**, et non un cas d'école. Le
  chiffre « 5/8 » est retiré : les deux partitions ne portent pas sur le même
  type d'objet (§3.6). Ce qui subsiste est plus étroit et suffit : sans fenêtre
  de dette exploitable, les trois apports propres de GCG disparaissent, et
  `OVERCLAIM` — dont la généricité est le résultat le mieux établi du chantier —
  n'a pas besoin du modèle pour exister.
- **`ABANDON`** — écarté, **avec une réserve plus lourde qu'initialement
  formulée**. La distinction à deux bornes est la seule idée réellement nouvelle
  et aucune revue n'a porté contre l'idée elle-même. Mais : elle n'est
  corroborée par **aucune seconde règle** (le modèle §7 le concède) ; elle
  s'applique à une population que ce document juge invalide ; et son seul usage
  ajouté — la largeur de fenêtre comme métrique de qualité de publication — est
  contesté par GCG-34. **Une idée jamais instanciée n'est pas montrée résiliente
  par le fait de survivre à une attaque : elle est non falsifiée parce que non
  testée.** L'élimination d'`ABANDON` tient parce que le coût n'est pas démontré
  excessif, pas parce que l'idée aurait fait ses preuves.

### 7.2 Verdict

```
VERDICT: REQUIRES_REDESIGN
```

**Motif dérivé, trois piliers.**

1. **Les entrées du modèle sont déclarées et non établies, et aucun substrat
   d'attestation n'existe dans ce dépôt.** La position d'un artefact (GCG-02) et
   l'immuabilité de la population (GCG-01) sont des déclarations ; les 14
   closeouts mutés (GCG-21) montrent que la seconde est fausse en pratique ; et
   l'absence de signature sur 243 commits montre que le substrat proposé pour
   l'attester n'atteste rien. Toute la moitié temporelle du modèle en dépend.
2. **La primauté d'`OVERCLAIM` sur la lecture historique, énoncée par le modèle
   §4.2 et par l'invariant I5, est fausse dans l'implémentation de référence**
   (GCG-36). La catégorie que le modèle déclare non migrable, non ledgerable et
   immédiatement bloquante s'annule par un renommage. Ce n'est pas un défaut de
   code isolé : c'est le seul apport propre du modèle qui soit à la fois
   spécifié et implémenté, et il ne l'est pas correctement.
3. **La classification entre en conflit non résolu avec une partition canonique
   existante** (GCG-11), sans règle de préséance entre un champ déclaré et une
   classification dérivée.

**Ce que le verdict ne dit pas.** Il ne dit pas que le modèle est faux. Les
trois lectures orthogonales, la définition généralisée d'`OVERCLAIM`, la
séparation Scanner / Arbitration / Migration Engine et la distinction à deux
bornes ont résisté à deux revues isolées qui cherchaient à les réfuter. Ce sont
les *entrées* du modèle et son *implémentation de référence* qui ne tiennent pas.

### 7.3 Condition de bascule, déclarée

Ce verdict devient `REPAIRABLE_CORE` si, et seulement si :

1. **D1** — une coordonnée dérivable d'un fait que l'auteur de l'artefact ne
   choisit pas, **appuyée sur un substrat qui n'existe pas encore** (signature
   des commits, ou empreinte épinglée à la clôture par un mécanisme hors
   d'atteinte de l'auteur), mesurée sur les 164 runs avec le nombre de
   reclassements publié avant décision ;
2. **D2** — l'immuabilité attestée par ce même substrat, **ou** une restriction
   explicite du modèle aux populations où la propriété est imposée ;
3. **GCG-36 réparé**, avec publication du nombre d'`OVERCLAIM` bloquants
   nouvellement issus des 148 `HISTORICAL_VALID`.

Il devient `DUPLICATES_EXISTING_CANON` si D1 ou D2 est sans réponse — c'est-à-dire
si aucun substrat d'attestation n'est créé et si aucune population existante
n'impose les deux propriétés. **En l'état des mesures, c'est la branche vers
laquelle le dépôt penche** : le substrat n'existe pas aujourd'hui, et aucune des
deux populations offertes (runs, skills) ne satisfait le contrat.

D4 est retirée de la condition de bascule : la version initiale y admettait
« une absorption assumée dans le canon existant » comme route vers
`REPAIRABLE_CORE`, alors que l'absorption **est** la définition de
`DUPLICATES_EXISTING_CANON`. La condition était malformée (RA-F-C).

### 7.4 Le test que je m'applique, dans les deux sens

**Première direction, posée initialement** — si le modèle était de quelqu'un
d'autre, écrirais-je `REPAIRABLE_CORE` ? Non : aucune borne n'est connue sur les
corrections de D1 et D2.

**Seconde direction, que la revue m'a reprochée de ne pas poser** — si le modèle
était de quelqu'un d'autre, aurais-je accepté « le noyau a résisté » pour un
mécanisme sans instance corroborante et sans population valide ? **Non.** La
formulation initiale était plus généreuse envers le noyau que le registre ne le
soutient, et la générosité était concentrée sur le composant le moins étayé — la
distinction à deux bornes. §7.1 le corrige : l'idée est **non falsifiée parce que
non testée**, ce qui n'est pas la même chose que résiliente.
