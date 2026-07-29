---
run_id: "2026-07-29_1550_gcg-findings-arbitration"
phase: "05_DECISIONS_REQUIRED"
voie: "STRUCTUREE"
status: "PARTIAL"
kind: "GOVERNANCE_FINDINGS_ARBITRATION"
agent: "claude-opus-5 (Claude Code)"
started_at: "2026-07-29T13:50:00Z"
ended_at: null
artifacts_consumed:
  - "02_FINDINGS_REGISTER.md"
  - "03_DEPENDENCY_AND_ARBITRATION_MAP.md"
artifacts_produced:
  - "05_DECISIONS_REQUIRED.md (this file)"
---

# 05_DECISIONS_REQUIRED — GCG-ARB-01

**Aucune décision n'est prise dans ce document.** Là où l'analyse technique
oriente clairement, une recommandation est écrite et **marquée comme telle** ;
là où le choix est de gouvernance, l'agent s'abstient et le dit. Une
recommandation n'est pas une décision : rien ci-dessous n'est appliqué.

Treize décisions. Trois seulement sont bloquantes pour toute reprise (D0, D4,
puis D1/D2).

---

## D0 — La certification v1.1 publiée est-elle soutenue ?
**P0 · aucune dépendance · ferme GCG-26, GCG-27 · autorité : humaine**

`2026-07-30_0500_final-publication-of-v1.1-certification` déclare
`adversarial_status: PASS_ADVERSARIAL` et `certification_status: CERTIFIED` sans
bloc adverse validable, **et** ces champs ont été écrits par un commit
postérieur à la clôture du run (`b9084e2`), en direction positive.

**Ce qui doit être établi avant toute option** : le `PASS_ADVERSARIAL` est-il
dérivable de `2026-07-30_0100` (seul run conforme au gate), avec un lien
vérifiable ?

| Option | Conséquence |
|---|---|
| **A** — attestation dérivée explicite | exige un lien vérifiable vers le run source, pas une recopie du verdict. La certification survit, sa base est nommée |
| **B** — la revendication n'est dérivable d'aucun run conforme | la revendication tombe, `certification_status` est révisé, **la certification v1.1 publiée est touchée** |
| **C** — ne rien faire | une certification publiée reste appuyée sur des champs écrits après clôture. Non tenable, listé pour être écarté explicitement |

**Interdit** — fabriquer un bloc adverse pour rendre le run vert ; rétrograder un
niveau pour obtenir le vert ; traiter la mutation post-clôture comme de la dette
historique (elle est postérieure à l'enforcement).

**Position de l'agent** — abstention sur A/B : trancher exige d'instruire la
dérivabilité, ce qui n'a pas été fait ici. **C est à écarter**, et c'est le seul
point sur lequel je me prononce.

---

## D1 — Qu'est-ce que la position d'un artefact ?
**P0 · bloquante · ferme GCG-02, GCG-10, GCG-13 · conditionne GCG-03, GCG-14 · autorité : humaine + canon**

La coordonnée qui décide de chaque classification est aujourd'hui l'identité de
run, c'est-à-dire un nom que l'auteur du run écrit. Mesuré :
`2026-07-30_0500` et `_0100` ont été commités ~30 h **avant** leur identité
déclarée. `docs/AUDIT_STATUS.md:124` porte un finding OPEN disant que ce
mécanisme relabellise des artefacts neufs en preuve historique.

**Fait qui contraint toutes les options** : `git log --format='%G?'` retourne
`N` sur 243 des 244 commits — **aucune signature**. Les dates d'auteur et de
committer sont réglables (`git commit --date`, `GIT_COMMITTER_DATE`) et
l'historique est réinscriptible. **L'historique git de ce dépôt n'est pas un
substrat d'attestation.**

| Option | Conséquence |
|---|---|
| **A** — coordonnée dérivée de la date d'auteur du premier commit ajoutant l'artefact | **détecte** le renommage de répertoire, **n'établit** rien : la date reste réglable par l'auteur. Réparation défensive |
| **B** — identité vérifiée contre l'historique git à la clôture, divergence bloquante | même limite qu'A. Détecte les deux contre-exemples connus, n'établit pas la propriété |
| **C** — restreindre le modèle aux populations où la coordonnée est imposée par le système | véritable attestation. **Aucune population de ce dépôt ne qualifie aujourd'hui** |
| **E** — **créer le substrat** : signature des commits, ou épinglage d'empreinte à la clôture par un mécanisme hors d'atteinte de l'auteur | seule voie vers A ou B au sens fort. Coût non évalué |
| **D** — statu quo | le corollaire de §3.2 reste faux et le modèle reste réfutable par un renommage |

**Recommandation retirée.** La version initiale recommandait « **A ou B** ».
La revue de l'arbitrage a établi (RA-F-D) qu'aucune des deux n'est une
attestation dans ce dépôt : elles détectent les contre-exemples connus sans
établir la propriété — **c'est-à-dire exactement la réparation défensive que ce
run avait pour charte d'empêcher, présente dans mes propres recommandations.**
J'applique le test déclaré-vs-établi à GCG-01 et GCG-02 avec force, puis je ne
l'appliquais pas à mes propres remèdes.

**Position révisée** — seules **C** et **E** ferment le défaut. **D est à
écarter.** A et B restent recevables comme mesures de **détection** transitoires,
à condition d'être nommées ainsi et non présentées comme des attestations.

**Limite de D1 elle-même** (RA-F-K) : même tranchée, D1 n'atteint que le
**positionnement**. Les sources 2 (`started_at`) et 3 (auto-déclaration) de
§3.4 restent écrites par l'auteur par conception. L'union est fail-closed, donc
ce n'est pas un trou — mais la formulation « une coordonnée que l'auteur ne
choisit pas » n'est atteignable que pour la position dans la fenêtre.

*Divergence V1 avec la première revue (§`03`.6), toujours ouverte : I8 quantifie-t-il
sur les frontières seules ? Elle décide si A/B sont recevables même comme
détection.*

---

## D2 — Sur quelle population le modèle opère-t-il, et comment l'immuabilité est-elle établie ?
**P0 · bloquante · ferme GCG-01, GCG-21, GCG-17, GCG-35 · autorité : humaine**

`immutable` est un booléen déclaré. Le déclarer ouvre la fenêtre de dette.
Mesuré : 14 closeouts sur 164 ont plus d'un commit, dont un dont le verdict a
été écrit après clôture. Par le mode dégradé du modèle lui-même, 148
classifications `HISTORICAL_VALID` sont indéfinies.

| Option | Conséquence |
|---|---|
| **A** — attester par empreinte de contenu épinglée à la clôture, **par un mécanisme hors d'atteinte de l'auteur** | l'immuabilité devient vérifiable ; le mécanisme n'existe pas et son coût n'est pas évalué |
| **B** — dériver de l'historique git (un closeout muté après clôture est détecté) | **détection, pas attestation** — l'historique est réinscriptible et non signé. Produit néanmoins la liste des 14 runs mutés, qui est l'entrée de toute autre option |
| **C** — restreindre explicitement le modèle aux populations où l'immuabilité est **imposée**, pas déclarée | véritable attestation ; **il pourrait ne rester aucune population** |
| **D** — statu quo | le prérequis reste une case à cocher qui déverrouille l'excuse |

**Recommandation révisée.** La version initiale recommandait « **B en premier** »
sans qualifier sa nature. B est une **mesure**, pas une attestation (RA-F-D) :
elle produit la liste des 14 closeouts mutés, ce qui est utile et suffisant pour
ouvrir le sujet, mais elle ne rend pas `immutable` vérifiable. **B d'abord comme
instrument de mesure ; A ou C pour clore le défaut. D est à écarter.**

**Ce que l'agent ne tranche pas** : le sort des 14 closeouts mutés. C'est une
décision de gouvernance, pas une conséquence technique.

*Divergence W2 avec la revue de l'arbitrage : elle conclut que l'absence de
substrat rend `DUPLICATES_EXISTING_CANON` quasi acquis ; je soutiens qu'un
substrat peut être créé (option A, ou signature des commits) et que le coût n'a
été évalué par personne. Ma position réduit la portée de son constat — je la
signale comme telle.*

---

## D3 — Où les deux bornes sont-elles déclarées, avec quelle unité et quelle inclusivité ?
**P1 · ferme GCG-09, GCG-08, GCG-18, GCG-33 · rend GCG-12 exécutable · autorité : canon**

`enforcement_effective_from` n'est déclaré **nulle part** au canon. La borne
`2000` n'existe qu'à `tools/vbb-governance-compat.py:105`, sous un commentaire
affirmant que les deux bornes sont lues du canon. I8 est violé en direct par la
règle phare du modèle.

Ce que la décision doit produire, en une seule écriture canonique :

1. la valeur de `applies_from` et celle de `enforcement_effective_from` ;
2. leur unité et leur fuseau — le canon déclare déjà
   `cutoff_timestamp: "2026-07-28T14:00:00Z"`, le code a perdu le fuseau ;
3. **l'inclusivité, borne par borne.** Les directions fail-closed sont
   **opposées** aux deux bouts : inclure `applies_from` est plus strict, inclure
   `enforcement_effective_from` est plus permissif. I10 donne une résolution
   unique pour les deux, ce qui est incohérent ;
4. le sort de `2026-07-28_2000_m2-bis` — aujourd'hui dans la fenêtre, donc
   excusable de ne pas porter la vérification qu'il a lui-même livrée.

**Recommandation de l'agent** — décision de forme claire, à prendre **sans
regarder le cas `m2-bis`**, puis à lui appliquer. Décider l'inclusivité en
fonction de son effet sur ce run serait choisir la règle pour obtenir le
résultat.

---

## D4 — Quelle préséance entre un statut déclaré et une classification dérivée ?
**P1 · déterminée par D1 et D2 · ferme GCG-11, éclaire GCG-34 · autorité : humaine**

> **Reformulée après revue (RA-F-B, RA-F-G).** La version initiale posait la
> question comme « vocabulaire nouveau ou refactor ? », la plaçait **avant**
> D1/D2, et l'appuyait sur un comptage — « 5 catégories sur 8 dupliquent » — que
> la revue a retiré : les deux partitions ne portent pas sur le même type
> d'objet. La question réelle est plus étroite, et l'ordre était circulaire.

`docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md:574-584` partitionne la même
population par un champ **déclaré** ; GCG produit une classification **dérivée**,
par couple *(artefact, règle)*. Aucune règle de préséance n'existe entre les
deux. Instance réelle : un run pré-cutoff déclarant
`certification_status: NOT_CERTIFIED` est **bloquant** sous le canon et
**`HISTORICAL_VALID`, non bloquant** sous GCG.

| Option | Conséquence |
|---|---|
| **A** — le déclaré prime ; le dérivé est un instrument de mesure sans autorité | cohérent avec `NOT_DERIVABLE_FROM_THIS_GATE` et avec I4 ; GCG ne peut jamais bloquer seul |
| **B** — le dérivé prime lorsqu'il est plus strict ; le déclaré ne peut qu'aggraver | fail-closed ; exige que la règle de préséance soit canonique et testée |
| **C** — absorber GCG dans le canon d'assurance : y ajouter `OVERCLAIM` et la fenêtre de dette | supprime le conflit ; le modèle devient un amendement d'ADR 0051, pas un pilier, et l'ADR 0052 disparaît |
| **D** — deux vocabulaires sans préséance | **état actuel**, Critical Rule 5 |

**Abstention de l'agent.** C'est une décision d'architecture de gouvernance.
Je note seulement que **D est l'état actuel et n'est pas un choix** : il est ce
qui se produit si la décision n'est pas prise. Et que C devient d'autant plus
attractive que D1 et D2 restent sans réponse, puisque les trois apports propres
de GCG dépendent tous de la fenêtre de dette.

---

## D5 — Qu'est-ce qu'une revendication, et qu'est-ce que la structure qui la valide ?
**P1 · ferme GCG-06, GCG-07, GCG-20 · conditionne GCG-28 · autorité : canon**

`OVERCLAIM` repose sur deux prédicats que **le scanner choisit** : quel
vocabulaire compte comme revendication (`PASS / CERTIFIED / READY / APPROVED`,
liste générique), et ce qu'est la structure qui la valide (`^adversarial:$` sur
texte brut). La v2 a rendu la *résolution d'artefact* déclarée par la règle
(A6/I11) et a laissé ces deux-là au scanner.

**Contradiction à trancher d'abord** : l'exemple G3 de §4.2 (`status: READY` +
`FINAL_STATUS: HANDOFF` = `OVERCLAIM`) et la fixture de test `NO_BLOCK`
(`status: "READY"`, assertée `HISTORICAL_VALID`) ne peuvent pas être vrais
ensemble. Décider le prédicat, c'est décider lequel des deux tombe.

| Option | Conséquence |
|---|---|
| **A** — chaque règle déclare son vocabulaire de revendication et sa structure de validation | symétrique d'I11, cohérent avec la v2. L'exemple G3 tombe : aucune règle de readiness ne déclare de population |
| **B** — un vocabulaire de revendication global au canon | plus simple, mais `READY` devient une revendication partout, ce qui casse la fixture `NO_BLOCK` et probablement d'autres |

**Recommandation de l'agent** — **A**, parce que c'est la réparation que la v2 a
déjà inventée pour le problème jumeau et qu'elle n'a pas appliquée ici. Et
**concession** : l'exemple G3 est de moi, il est faux tel qu'écrit, et sous A il
disparaît.

**Effet en aval à ne pas manquer** : sans D5, les 9 dispositions de connaissance
positives (GCG-28) ne peuvent pas être instruites — seulement comptées. Si D5
les qualifie de revendications, **une seconde règle entre en dette** et le
périmètre d'arbitrage humain double.

---

## D6 — L'arbitration peut-elle attribuer une disposition non-dette ?
**P1 · ferme GCG-04 · autorité : humaine**

`LEDGERABLE` inclut `HISTORICAL_VALID` ; `historical_debt` ne le somme pas ;
`applicable` l'exclut. Un run en échec **dans** la fenêtre, plus une ligne de
ledger `HISTORICAL_VALID`, donne `verdict: PASS`, `historical_debt: 0`,
`blocking: []` et disparaît du dénominateur. **Aucune des trois lectures ne le
voit.** Les 4 `UNKNOWN` actuels sont les premiers clients.

I2 interdit une disposition **de dette hors** de la fenêtre. Rien n'interdit une
disposition **de non-dette dedans**, et §2.2 autorise l'arbitration à « résoudre
un `UNKNOWN` en une disposition » sans restreindre l'ensemble cible.

| Option | Conséquence |
|---|---|
| **A** — l'arbitration ne peut que **reconnaître une dette**, jamais **attribuer une validité** | `LEDGERABLE` se réduit à deux valeurs. Reste à décider si `applicable` doit cesser d'exclure `HISTORICAL_VALID`, sinon une disposition légitime reste invisible |
| **B** — elle peut attribuer une validité, mais la disposition devient **visible** | exige une quatrième lecture : `HISTORICAL_VALID` **ledgeré** compté à part des 148 classés par la règle |
| **C** — statu quo | la voie de blanchiment la plus propre du modèle reste ouverte, sans trace |

**Abstention de l'agent sur A/B** — c'est une question de gouvernance sur ce que
l'arbitrage humain a le droit de faire, et je n'ai pas autorité pour la trancher.
**C est à écarter.** Je note que la correction d'apparence mécanique (retirer une
valeur d'un ensemble en code) *est* la décision A prise silencieusement : c'est
l'exemple le plus net du registre d'une décision normative déguisée en
correction technique.

---

## D7 — Que signifie l'absence du porteur de preuve ?
**P1 · ferme GCG-05 · autorité : canon**

> **Périmètre corrigé après revue (RA-F-F).** La version initiale rattachait
> aussi GCG-15 et GCG-19 à cette décision. Mal-regroupement : D7 demande ce que
> signifie **l'absence** du porteur ; GCG-19 départage plusieurs porteurs
> **présents** (`st_mtime`) et GCG-15 choisit lequel lire. Aucune des trois
> options ci-dessous ne les décide, et les y rattacher retardait deux
> corrections gratuites. Les deux sont sortis vers `03` §4.2.

`PENDING_LIFECYCLE` est attribué quand l'artefact porteur n'existe pas : non
bloquant **et** exclu de `applicable`. Renommer `07_CLOSEOUT.md` en
`07_CLOSE-OUT.md` fait basculer un run bloquant vers cette catégorie. §4.1 pose
un test sur le **motif** de l'absence ; le scanner n'observe que le **fait**.
Déclarer le résolveur (I11) règle les variantes de nommage, pas l'absence.

| Option | Conséquence |
|---|---|
| **A** — l'absence du porteur est **bloquante par défaut** ; `PENDING_LIFECYCLE` exige une déclaration positive du run (« ouvert, phase N ») | fail-closed. Un run ouvert doit se déclarer ouvert au lieu d'être deviné |
| **B** — l'absence reste non bloquante mais **compte dans `applicable`** | plus faible : la voie reste ouverte, elle devient seulement visible |
| **C** — statu quo | l'absence provoquée reste une sortie gratuite |

**Recommandation retirée.** La version initiale recommandait **A** comme « seule
option cohérente avec la posture fail-closed ». La revue a établi (RA-F-F) que A
remplace une **absence invérifiable** par une **déclaration invérifiable** :
« ouvert, phase N » est une affirmation de motif que le scanner ne peut pas
davantage contrôler. Le basculement du défaut vers *bloquant* reste un gain
réel ; l'échappatoire survit sous forme déclarée. Je n'avais pas retourné sur ma
propre recommandation l'instrument du registre — GCG-01, *« un booléen déclaré
que rien n'atteste »*.

**Position révisée** — **A reste préférable à B et C**, mais doit être qualifiée :
elle déplace le défaut, elle ne le ferme pas. Une fermeture exige que la
déclaration d'ouverture soit **vérifiable** (par exemple : absence de closeout
**et** présence d'un artefact de phase postérieur au dernier commit du run).
**C est à écarter.**

---

## D8 — Comment épingle-t-on un constat produit hors d'un run ?
**P2 · ferme GCG-25, éclaire GCG-C4 · autorité : humaine**

L'obligation de corpus se déclenche sur les findings `CONFIRMED` **déclarés dans
le bloc adverse d'un closeout**. Les 12 constats de la revue indépendante n'ont
été déclarés dans aucun closeout : ils ne portent aucune obligation d'épinglage
et rien n'empêche qu'ils changent en silence.

Symétriquement, le seul moyen de les épingler est de les déclarer dans un
closeout — ce qui force à écrire du code, exactement le mécanisme qui a fait
dévier le stress test (`A5`, GCG-C4). Les deux faces du même défaut : **une
revue échappe à l'épinglage, un run ne peut pas y échapper.**

| Option | Conséquence |
|---|---|
| **A** — une revue indépendante produit un run, donc un closeout, donc l'obligation | cohérent, mais rend toute revue coûteuse et couplée au code |
| **B** — l'obligation de corpus se déclenche sur un **registre de constats**, pas sur un closeout | découple constat et code ; exige un artefact canonique nouveau |
| **C** — statu quo | les constats de revue restent non épinglés ; ce registre est leur seul porteur |

**Abstention.** Ce run ne déclare pas les 12 constats dans son bloc adverse et
le dit explicitement au closeout : il ne conduit aucune campagne, il arbitre des
constats produits ailleurs.

---

## D9–D11 — Décisions normatives héritées du run `1021`
**Ouvertes depuis le 2026-07-29, non arbitrées ici · autorité : humaine**

- **D9 (GCG-30)** — un run d'arbitrage normatif doit-il porter sa propre campagne
  adverse, ou une attestation dérivée du run qu'il arbitre ? *Le présent run est
  une instance de la question.*
- **D10 (GCG-31)** — `adversarial_level: A2` implique-t-il toujours l'obligation
  d'une campagne, ou existe-t-il un `adversarial_status: NOT_REQUIRED` légitime
  pour un sujet A2 ? La contradiction de `2026-07-28_2300` est d'origine, pas
  rétroactive.
- **D11 (GCG-32)** — `2026-07-28_2200` : les valeurs `confidence`/`state` des 14
  findings sont-elles **présentes mais hors énumération** (réparation de schéma)
  ou **absentes** (non reconstructible) ? **Fait à établir par inspection avant
  toute option** — la décision dépend d'une mesure qui n'a pas été faite.

---

## D12 — Le chantier progresse-t-il sans acteur A2 distinct ?
**P1 · GCG-29 · autorité : humaine + acteur externe**

Les quatre runs GCG déclarent `A2` sans acteur distinct par famille de LLM.
La revue indépendante du 2026-07-29 a apporté une **isolation de contexte
réelle** — mesurablement productive : 8 constats substantiels que l'auteur avait
manqués, dont 3 voies de blanchiment — mais **pas** une distinction de famille de
modèle.

| Option | Conséquence |
|---|---|
| **A** — obtenir un acteur réellement distinct avant tout ADR | seule voie vers une certification revendicable |
| **B** — poursuivre, en déclarant l'absence à chaque closeout | état actuel ; aucun `PASS_ADVERSARIAL` ne sera jamais revendicable |
| **C** — reconnaître l'isolation de contexte comme un proxy partiel, avec son écart déclaré | exige un amendement canonique de `A2_DISTINCT_AGENT_PROXY` |

**Abstention.** Aucun agent ne peut clore cette décision : elle requiert une
ressource externe.

---

## Tableau — décision normative ou correction technique ?

Les cinq questions exigées par la mission, pour chacun des 35 constats.

Légende : **DN** décision normative requise · **RM** le modèle contient déjà la
règle · **PORTÉE** locale / globale · **DÉF** risque de réparation défensive ·
**NIVEAU** M modèle · C canon · I implémentation.

| ID | DN | RM | PORTÉE | DÉF | NIVEAU | Décision liée |
|---|---|---|---|---|---|---|
| GCG-01 | **oui** | non | globale | — | M | D2 |
| GCG-02 | **oui** | non | globale | — | M + C | D1 |
| GCG-03 | oui | non | globale | **oui** | M | D1, D3 |
| GCG-04 | **oui** | non | globale | **oui** | M + I | D6 |
| GCG-05 | **oui** | non | globale | **oui** | M | D7 |
| GCG-06 | oui | **partiellement** (I11, pour le problème jumeau) | globale | **oui** | M + C | D5 |
| GCG-07 | oui | non | locale | — | M | D5 |
| GCG-08 | oui | non | locale | **oui** | C + I | D3 |
| GCG-09 | oui | **oui** (I8) | locale | — | C + I | D3 |
| GCG-10 | oui | non | globale | — | M + C | D1 |
| GCG-11 | **oui** | non | globale | — | M + C | D4 |
| GCG-12 | non | oui | locale | — | I | D3 (ordre) |
| GCG-13 | oui | non | locale | — | M | D1 |
| GCG-14 | non | **oui** (I9) | locale | **oui** | I | D1, D3 |
| GCG-15 | non | **oui** (I11) | locale | — | I | **aucune** — exécutable |
| GCG-16 | non | **oui** (§6.1) | locale | — | I | — |
| GCG-17 | — | — | — | — | — | superseded par GCG-01 |
| GCG-18 | non | oui | locale | — | I | D3 |
| GCG-19 | non | **oui** (§2.1) | locale | — | I | **aucune** — exécutable |
| GCG-20 | non | non | locale | **oui** | I | D5 |
| GCG-21 | **oui** | non | globale | — | dépôt | D2 |
| GCG-22 | non | oui | locale | — | M | — |
| GCG-23 | non | oui | locale | — | M + tests | — |
| GCG-24 | non | oui | locale | — | M | — |
| GCG-25 | **oui** | non | globale | — | C | D8 |
| GCG-26 | **oui** | **oui** (§4.2) | globale | **oui** | dépôt | D0 |
| GCG-27 | **oui** | non | globale | **oui** | dépôt | D0 |
| GCG-28 | oui | non | locale | — | dépôt | D5 |
| GCG-29 | **oui** | oui | globale | — | C + externe | D12 |
| GCG-30 | **oui** | non | globale | — | C | D9 |
| GCG-31 | **oui** | non | globale | — | C | D10 |
| GCG-32 | **oui** | non | locale | **oui** | dépôt | D11 |
| GCG-33 | non | oui | locale | — | M | D1, D3 |
| GCG-34 | oui | non | locale | — | M | — |
| GCG-35 | **oui** | non | globale | — | M | D2, D4 |
| **GCG-36** | **non** | **oui** (§4.2, I5) | globale | non | I | **aucune** — exécutable, priorité haute |

**Lecture.** 18 constats sur 36 exigent une décision normative. 8 portent un
risque de réparation défensive caractérisé — ce sont ceux dont la correction
technique *existe* et *décide silencieusement* : GCG-03, 04, 05, 06, 08, 14, 20,
26/27, 32. **Aucun ne doit être corrigé avant sa décision.**

**Neuf constats sont des corrections mécaniques** : GCG-12, 15, 16, 18, 19, 22,
23, 24, 36. Cinq sont exécutables immédiatement (GCG-15, 19, 22, 24, 36), quatre
restent subordonnés à l'ordre du graphe.

**GCG-36 est le cas inverse de D6** : là où retirer une valeur d'un ensemble
*serait* une décision normative déguisée, réparer l'ordre des branches de
`classify_run` n'en est pas une — le modèle §4.2 et le commentaire du code
énoncent déjà la règle, seule l'implémentation la contredit. Le registre
contient donc les deux erreurs symétriques, et les distinguer est tout l'objet
de ce tableau.
