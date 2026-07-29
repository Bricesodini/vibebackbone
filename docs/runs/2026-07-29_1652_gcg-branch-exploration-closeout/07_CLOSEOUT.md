---
run_id: "2026-07-29_1652_gcg-branch-exploration-closeout"
phase: "07_CLOSEOUT"
voie: "CLOTURE"
status: "PARTIAL"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
knowledge_harvest: "OBSERVATION_RECORDED"
kind: "HANDOFF"
subject_kind: "EXPLORATION_BRANCH_CLOSEOUT"
adversarial_level: "A2"
agent: "claude-opus-5 (Claude Code)"
started_at: "2026-07-29T14:52:00Z"
ended_at: "2026-07-29T15:10:00Z"
next_phase: null
artifacts_consumed:
  - "docs/REFERENCE/governance-compatibility-model.md (v2, PROPOSED)"
  - "docs/runs/2026-07-29_1021_adversarial-gate-population/"
  - "docs/runs/2026-07-29_1050_gcg-conceptual-model/"
  - "docs/runs/2026-07-29_1130_gcg-genericity-stress-test/"
  - "docs/runs/2026-07-29_1550_gcg-findings-arbitration/"
artifacts_produced:
  - "01_INTAKE.md"
  - "07_CLOSEOUT.md (this file)"
---

# 07_CLOSEOUT — Branche `feat/governance-compatibility-gate`

> **Kind : `HANDOFF`** — la branche est close comme **phase d'exploration**, pas
> comme proposition prête à intégrer. Le travail est conservé intégralement ;
> rien n'est fusionné en l'état.

## Objectif de la phase et résultat

**Objectif initial** : nommer et outiller le problème que le dépôt avait
rencontré quatre fois sans jamais le nommer — *comment une règle de gouvernance
peut-elle évoluer sans invalider le patrimoine documentaire qui la précède ?*

**Résultat** : le **problème** est confirmé et documenté par mesure. La
**solution** proposée ne l'est pas. Quatre runs, deux revues indépendantes,
36 constats enregistrés, verdict `REQUIRES_REDESIGN`.

**Statut global : `PARTIEL`.** L'exploration a produit ce qu'une exploration doit
produire — une carte du terrain et une raison claire de ne pas construire ici.

Cette clôture est **volontaire et non contrainte** : aucun blocage technique
n'imposait l'arrêt. La décision est de repartir d'une architecture rééquilibrée
plutôt que d'enchaîner les correctifs sur une base dont les entrées ne tiennent
pas.

---

## 1. Concepts validés

Robustes indépendamment de l'implémentation actuelle. Le critère retenu :
**avoir survécu à une tentative délibérée de réfutation par un lecteur
indépendant**, et disposer de plus d'une instance quand la mesure était possible.

### 1.1 `OVERCLAIM` — la revendication positive non soutenue

*Un artefact affirme un verdict positif sans porter la structure qui permettrait
de le valider.*

C'est le résultat le mieux établi de tout le chantier, et le seul qui ait deux
instances **indépendantes** trouvées par mesure :

- règle adverse : `PASS_ADVERSARIAL` sans bloc validable ;
- règle *engineering-knowledge*, sans rapport : `EVIDENCE_LINKED` défini comme
  « preuve liée à un candidat existant » alors qu'aucun registre de candidats
  n'existe et que le validateur ne vérifie que l'appartenance à une énumération.

La seconde instance a été trouvée sur une règle choisie **avant** de savoir ce
qu'on y trouverait, puis re-vérifiée par un relecteur qui n'avait pas lu le
stress test. Elle n'a aucun équivalent dans le canon existant.

Le principe sous-jacent est plus général que GCG : **une omission est inerte, une
fausse affirmation est lue et crue.** Les traiter à la même sévérité range la
seconde dans une file d'attente.

### 1.2 Les trois lectures orthogonales

*Conformité actuelle ≠ dette historique acceptée ≠ certification obtenue.*

Jamais contredit par aucune des deux revues. C'est ce qui a rendu visible le
défaut P0 sur la certification v1.1 publiée, qu'aucun gate ne voyait tant que les
trois lectures étaient confondues en une seule.

Son corollaire — **une certification n'est jamais dérivable d'un verdict de
conformité** — est la seule décision de conception que les deux revues ont
approuvée sans réserve. Il a tenu **même contre son auteur** : la seconde revue
s'en est servie comme étalon pour établir que ma propre table d'équivalences
dérivait une certification d'un code de sortie de sous-processus. Un principe qui
condamne son auteur est un principe qui existe indépendamment de lui.

### 1.3 La séparation observation / qualification / arbitrage

*Aucun composant n'observe, ne juge et ne modifie à la fois.*

Recherché explicitement, aucune fuite de capacité trouvée. Et le point qui la
valide n'est pas qu'elle soit respectée, c'est qu'elle **nomme son propre
manque** : le scanner a besoin d'un jugement qu'on lui refuse, et le modèle
appelle cela *arbitrage* au lieu de le dissimuler dans une heuristique.

Cette discipline dépasse GCG. Elle s'applique à tout instrument de gouvernance,
et l'exploration a montré qu'elle doit aussi s'appliquer à **l'analyste**, pas
seulement à l'outil — voir §5.3.

### 1.4 L'anti-blanchiment comme obligation de conception

*Toute taxonomie d'exception doit être examinée pour son chemin de moindre
effort, pas seulement pour sa complétude.*

Validé **par ses propres échecs**, ce qui est la meilleure preuve disponible :
quatre voies de blanchiment ont été trouvées, trois par des lecteurs autres que
l'auteur, et deux d'entre elles étaient **autorisées par le texte du modèle**,
pas des lacunes de ce texte. Une catégorie qui excuse est une catégorie vers
laquelle on converge.

### 1.5 Le constat de départ — et lui seul

Le dépôt a réinventé « cette règle ne s'applique pas rétroactivement »
**quatre fois** sans jamais la nommer : trois paires de constantes de cutover
(`KNOWLEDGE_`, `ASSURANCE_`, `ADVERSARIAL_`), plus ADR 0033 qui ne scanne que les
lignes ajoutées — la même idée exprimée pour un flux.

**Le besoin est confirmé. Il ne dit rien de la validité de la réponse
apportée.** C'est la distinction que cette clôture existe pour poser.

---

## 2. Concepts fragiles

Intéressants, insuffisamment formalisés. Aucun n'est réfuté ; aucun n'est prêt.

| Concept | Ce qui tient | Ce qui manque |
|---|---|---|
| **La distinction à deux bornes** (`applies_from` vs `enforcement_effective_from`) | l'**observation** que publier une obligation et savoir la vérifier sont deux moments distincts. Aucune attaque n'a porté contre l'idée | aucune corroboration sur une seconde règle : les trois cutovers du dépôt n'ont **qu'une** borne. Une idée jamais instanciée n'est pas montrée résiliente, elle est non falsifiée parce que non testée |
| **La fenêtre de dette** | l'intervalle est observable et se mesure | ce qu'il **autorise** n'est pas formalisé : quelles dispositions, par qui, avec quelle trace. Le texte du modèle permet d'y placer une disposition *de non-dette* qui ne laisse trace dans aucune des trois lectures |
| **Le contrat de population** (`dated`, `immutable`, `enumerable`) | l'intuition est juste : les catégories historiques ont des préconditions | deux termes sur trois sont des **déclarations indécidables**. Déclarer `immutable: true` ouvre la fenêtre de dette, et rien ne peut contredire la déclaration |
| **La coordonnée temporelle d'un artefact** | le modèle a eu raison d'en faire un objet explicite | il a supposé qu'elle existait. Elle n'existe pas : l'identité de run est écrite par l'auteur, et 243 commits sur 244 ne portent aucune signature |
| **`PENDING_LIFECYCLE`** | un run en cours n'est pas un run en échec — la catégorie répond à un vrai besoin | elle est définie sur l'**absence** du porteur de preuve, et une absence se provoque |
| **La largeur de fenêtre comme métrique de qualité de publication** | séduisant, et vrai dans ce dépôt | sur-ajusté : suppose que l'auteur de la règle et son outilleur sont la même équipe à quelques heures d'intervalle. Pour une règle écrite ailleurs, la fenêtre est toujours large et ne signale rien |
| **Le mode dégradé** | la bonne réponse structurelle : une population qui ne qualifie pas **perd** les catégories historiques | jamais exercé, parce que sa condition d'entrée est une déclaration. Un mode dégradé qu'on n'atteint jamais est un mode qui n'existe pas |

---

## 3. Responsabilités mal positionnées

La section la plus utile pour une reprise architecturale. GCG a concentré des
responsabilités qui appartiennent à d'autres couches.

### 3.1 Déclarer une frontière normative → **le canon, pas l'outil**

`enforcement_effective_from` n'existe **que** dans le code
(`vbb-governance-compat.py:105`), sous un commentaire affirmant que les deux
bornes sont lues du canon. Un outil qui définit la frontière qu'il mesure n'est
pas un instrument, c'est une autorité qui s'ignore.

**Devrait quitter GCG** : la valeur, l'unité, le fuseau et l'inclusivité de
chaque borne appartiennent au document canonique de la règle. GCG les lit.

### 3.2 Partitionner l'état d'assurance → **le canon existant, pas une seconde partition**

`ADVERSARIAL_ASSURANCE_GOVERNANCE.md` partitionne déjà la population par
`certification_status`. GCG en a dérivé une seconde, sans règle de préséance
entre un champ **déclaré** et une classification **dérivée**.

**Devrait quitter GCG** : la partition. Ce que GCG ajoute légitimement —
`OVERCLAIM` et la notion de zone non arbitrée — devrait être **proposé au canon
d'assurance**, pas maintenu comme vocabulaire concurrent.

### 3.3 Attester la coordonnée et l'immuabilité → **l'infrastructure du dépôt**

**La responsabilité la plus mal placée du lot.** GCG a besoin de deux faits sur
chaque artefact : où il se situe, et s'il a changé depuis. Il a traité les deux
comme des déclarations parce qu'il n'avait aucun moyen de les établir — et il
n'en a aucun parce que **ce n'est pas sa couche**.

Signer les commits, épingler une empreinte de contenu à la clôture : c'est de
l'infrastructure Core / dépôt. Aucune gouvernance temporelle ne peut être
construite avant que cette couche existe, et aucun modèle ne peut la fabriquer
en la déclarant.

### 3.4 Résoudre l'artefact porteur de preuve → **une couche partagée unique**

Deux résolveurs coexistent : `find_closeout()` avec repli permissif, et un chemin
en dur. Le même run « a » et « n'a pas » de closeout selon le consommateur.

**Devrait quitter chaque consommateur** : la résolution appartient à
`vbb_run_resolution.py` comme source unique, consommée par tous les enforcers.
Aujourd'hui chacun choisit, y compris GCG.

### 3.5 Définir ce qu'est une revendication → **la règle, pas le scanner**

Le prédicat de revendication (`PASS / CERTIFIED / READY / APPROVED`) et le
prédicat de structure validante sont tous deux **choisis par le scanner**. La v2
avait inventé exactement la réparation nécessaire — rendre la résolution
d'artefact déclarée par la règle — et ne l'a pas appliquée au cas qui en avait le
plus besoin.

### 3.6 Épingler un constat → **une couche de registre, pas le closeout**

L'obligation de corpus se déclenche sur le bloc adverse d'un closeout.
Conséquence mesurée dans les deux sens : une revue conduite hors run **échappe**
à l'épinglage, et un run qui déclare un constat **ne peut pas** y échapper même
quand son périmètre lui interdit d'écrire du code. Les deux faces sont des
symptômes du même mauvais placement.

### 3.7 Mesurer ≠ bloquer

GCG a été livré comme *instrument de mesure*, délibérément rouge et non câblé —
ce qui était juste. Mais ses sorties ont la forme d'un gate : `verdict: PASS/FAIL`
et une liste `blocking`. Un instrument de mesure qui émet un verdict bloquant
finit par être câblé pour ce verdict.

**Question de couche, pas de code** : une classification dérivée a-t-elle
autorité pour bloquer, ou seulement pour mesurer ? Elle est posée en §4.

---

## 4. Questions encore ouvertes

Décisions d'architecture réelles. **Aucune solution n'est proposée ici**, et
aucune n'est classée par priorité — l'ordre est celui des dépendances
constatées.

| # | Question |
|---|---|
| **Q1** | Le dépôt doit-il se doter d'un **substrat d'attestation** — signature, épinglage d'empreinte, ou autre — permettant d'établir qu'un artefact est daté et n'a pas changé ? Toute gouvernance temporelle en dépend, et aucune ne peut le créer. |
| **Q2** | Une non-conformité **antérieure à l'outillage** d'une règle doit-elle être excusable ? Le chantier l'a supposé sans jamais le décider. C'est la prémisse de la fenêtre de dette, et elle n'a pas été instruite. |
| **Q3** | Qui a autorité pour **attribuer une disposition** à un artefact, et sur quel ensemble de valeurs ? Reconnaître une dette et attribuer une validité ne sont pas le même acte. |
| **Q4** | Le canon doit-il porter une catégorie pour la **revendication positive non soutenue** ? Le besoin est établi par deux instances indépendantes ; l'emplacement ne l'est pas. |
| **Q5** | Une classification **dérivée** peut-elle bloquer, ou seulement mesurer ? Et quelle préséance avec un statut **déclaré** portant sur le même artefact ? |
| **Q6** | Un constat produit **hors d'un run** doit-il porter une obligation d'épinglage, et à quelle couche ? |
| **Q7** | `adversarial_level: A2` implique-t-il toujours l'obligation d'une campagne, ou existe-t-il un `NOT_REQUIRED` légitime pour un sujet A2 ? *(hérité du run `1021`)* |
| **Q8** | Un run d'**arbitrage normatif** porte-t-il sa propre campagne adverse, ou une attestation dérivée du run qu'il arbitre ? *(hérité du run `1021`)* |
| **Q9** | Le canon doit-il reconnaître un **palier intermédiaire** entre A1 et A2 — l'isolation de contexte sans distinction d'acteur — dont cette exploration a mesuré le rendement ? |
| **Q10** | **P0, indépendant de GCG.** La certification v1.1 publiée est-elle soutenue ? `2026-07-30_0500` revendique `PASS_ADVERSARIAL` et `CERTIFIED` sans bloc validable, et ces champs ont été écrits par le commit `b9084e2` **après** la clôture du run. Cette question porte sur `main` et **survit à l'abandon de cette branche**. |

---

## 5. Enseignements méthodologiques

Ce que l'exploration a appris sur vibebackbone lui-même. Chaque point est adossé
à une mesure de ce chantier, pas à une impression.

### 5.1 Rôle des subagents

**Mesure.** L'auteur a trouvé 8 constats sur son propre modèle. Deux relecteurs
en ont trouvé 23, dont 4 voies de blanchiment et un P0.

**Ce que la mesure dit, et qui n'était pas prévu** : les deux populations de
constats ne sont pas de même nature. L'auteur, testant la **généricité** de son
modèle, a trouvé des **manques de spécification** — applicabilité, unité,
population, schéma. Les relecteurs, testant sa **solidité**, ont trouvé des
**failles exploitables**. Ce ne sont pas deux niveaux de qualité : ce sont deux
axes d'attaque, et l'auteur choisit systématiquement le plus sûr des deux.

Un subagent n'est donc pas un multiplicateur d'effort. C'est **un changement
d'axe d'attaque**, et c'est pour cela qu'il n'est pas substituable par plus de
travail de l'auteur.

### 5.2 Indépendance des contextes

`A2_DISTINCT_AGENT_PROXY` n'a **jamais** été satisfait sur les cinq runs : même
famille de LLM, même prompt système, à chaque fois. Ce qui a été obtenu est une
**isolation de contexte**, et son rendement est mesurable — la seconde revue,
sans accès à la conversation de l'auteur, a réfuté quatre de ses énoncés et
invalidé trois conditions d'arrêt sur dix.

Le canon traite `A2` en binaire : acteur distinct, ou rien. L'observation
suggère qu'il existe un palier utilisable entre les deux. **Ce n'est pas une
conclusion de ce chantier, c'est une question pour le canon adverse** (Q9), et
elle est notée ici parce qu'elle ne serait visible nulle part ailleurs.

Réserve à conserver : l'isolation de contexte a produit beaucoup, et elle n'a
pas produit d'acteur distinct. Aucun `PASS_ADVERSARIAL` n'a été revendiqué, et
aucun ne l'aurait été légitimement.

### 5.3 Séparation entre observation, qualification et arbitrage

Le résultat structurel le plus solide du chantier — **et le plus mal appliqué par
son auteur**.

La séparation a tenu partout où elle était imposée à l'outil. Elle a cédé
immédiatement là où elle n'était imposée qu'à l'analyste : en construisant une
table d'équivalences entre catégories GCG et statuts canoniques, j'ai assimilé
`CURRENT` (un code de sortie) à `CERTIFIED` (treize conditions dont une décision
humaine enregistrée) — c'est-à-dire que **j'ai dérivé une certification d'un
verdict de conformité, dans le document qui poursuit cette dérivation**, sans le
voir.

**Enseignement** : une discipline de séparation appliquée aux outils et pas aux
analystes ne protège rien. L'erreur est invisible depuis l'intérieur, précisément
parce que l'analyste croit connaître la règle.

### 5.4 Gouvernance versus implémentation

Trois symptômes récurrents, tous mesurés :

1. **Spécifier plus n'est pas sécuriser plus.** La v2 du modèle a ajouté trois
   invariants et zéro test : la couverture est passée de 3/8 à 3/11. Le document
   paraissait plus solide en étant mécaniquement aussi fragile.
2. **Un commentaire n'est pas un porteur.** Deux fois dans le même fichier, un
   commentaire affirme exactement ce que le code contredit — sur l'origine des
   bornes, et sur la primauté d'`OVERCLAIM` sur la lecture historique.
3. **Un aveu d'honnêteté est une revendication comme une autre.** Le tableau
   « voici ce que je ne garantis pas » du modèle était faux dans les deux sens.
   Et ma correction l'était aussi, dans le sens de la surestimation. Corriger un
   aveu demande la même vérification qu'une affirmation positive, pas moins.

**Règle dégagée** : un énoncé normatif sans porteur exécutable est une intention.
Le compter comme une garantie est le mécanisme par lequel un canon dérive.

### 5.5 Risques de duplication du canon

GCG a re-dérivé une partition que le canon possédait déjà, et son auteur a
ensuite construit une table qui aggravait la confusion.

**Enseignement en deux temps** :
- avant de nommer un concept, vérifier si le canon le nomme déjà — la question
  ouverte 6 du modèle voyait les *constantes* dupliquées et n'a pas vu le
  *vocabulaire* dupliqué ;
- la duplication se commet le plus facilement **en rédigeant le document qui
  l'interdit**. Critical Rule 5 était citée trois fois dans le document qui la
  violait.

### 5.6 Gestion de l'évolution des règles

Le problème est réel et mesuré : quatre réinventions ad hoc de la
non-rétroactivité, jamais nommées.

Mais l'exploration a déplacé la question. Le chantier a commencé par
« comment excuser le passé ? » et devrait recommencer par **« qu'est-ce que le
dépôt sait établir sur son propre passé ? »**. Sans coordonnée attestée ni
immuabilité attestée, la première question n'a pas de réponse vérifiable — elle
n'a que des réponses déclarées.

**C'est le renversement principal de cette phase**, et la raison de la clôturer
plutôt que de la corriger : les correctifs portaient tous sur la moitié
supérieure d'un édifice dont les fondations n'ont jamais été posées.

---

## 6. État de la branche

### 6.1 Commits

| SHA | Message |
|---|---|
| `7e011f8` | `feat(governance): introduce the Governance Compatibility Gate, red on purpose` |
| `f7e21a3` | `docs(governance): stabilize the compatibility model before implementing it` |
| `5d4fe34` | `test(governance): stress-test the compatibility model, verdict NOT_CANONICAL_YET` |
| `4bfd65e` | `docs(governance): arbitrate the GCG findings, and find a fourth laundering route` |

Base : `6b0daf4` sur `main`. **36 fichiers, +7 430 / −1.** L'unique suppression
est un incrément de `tests/adversarial_corpus/VERSION`.

Branche **non poussée**. Aucun commit sur `main`.

### 6.2 Ce qui est implémenté

| Artefact | Volume | État réel |
|---|---|---|
| `tools/vbb-governance-compat.py` | 325 lignes | fonctionnel, **non câblé** : absent de `vbb-ci-local.sh` et de la CI distante |
| `tests/test_governance_compat_gate.py` | 203 lignes, 8 tests | verts, mais un porteur est **tautologique** et un autre couvre la mauvaise branche de son invariant |
| `tests/adversarial_corpus/CORPUS-S1..S5.py` | 403 lignes | `BEHAVIOUR_PIN` : figent des défauts, ne prouvent aucune correction |
| `tests/adversarial_corpus/conftest.py`, `INDEX.md`, `VERSION` | 62 lignes | fixture et index pour les pins ci-dessus ; `VERSION` 1.1.0 → 1.2.0 |

### 6.3 Ce qui est expérimental

- `docs/REFERENCE/governance-compatibility-model.md` — 525 lignes, statut
  `PROPOSED`, verdict `REQUIRES_REDESIGN`. **Aucun ADR ne l'adosse.**
- Les quatre répertoires de run (`1021`, `1050`, `1130`, `1550`) — matériau
  d'exploration : matrice de disposition, POC, stress test sur quatre règles,
  registre de 36 constats, deux revues indépendantes.
- Le ledger, le *Migration Engine* et le câblage CI : **spécifiés, jamais
  écrits**. C'est la seule bonne nouvelle de l'inventaire.

### 6.4 Ce qui ne doit pas être fusionné en l'état

| Artefact | Motif |
|---|---|
| `tools/vbb-governance-compat.py` | classe `HISTORICAL_VALID` **avant** de tester `OVERCLAIM` : un renommage de répertoire annule la seule catégorie déclarée non migrable. N'implémente qu'une des trois sources d'applicabilité de l'enforcer qu'il enveloppe, donc **structurellement plus permissif** que lui. Porte deux commentaires qui affirment le contraire de ce que le code fait |
| `docs/REFERENCE/governance-compatibility-model.md` | `REQUIRES_REDESIGN`. Deux concepts centraux reposent sur des propriétés déclarées que rien n'atteste. Son tableau de couverture est faux dans les deux sens |
| `tests/adversarial_corpus/CORPUS-S1..S5.py` | épinglent le comportement de code qui n'existe que sur cette branche. Fusionnés seuls, ils verrouillent des défauts sans objet ; fusionnés avec l'outil, ils verrouillent des défauts qu'on a décidé de ne pas corriger |
| `tests/test_governance_compat_gate.py` | inséparable de l'outil |

**Aucun des quatre commits n'est fusionnable partiellement**, parce que le
matériau documentaire et le code sont entrelacés dans chacun d'eux.

### 6.5 Ce qui mérite d'être extrait plus tard, sans le code

Ce qui a valeur indépendamment de l'implémentation abandonnée, à reprendre par
une réflexion architecturale ultérieure — **en repartant des concepts, pas des
fichiers** :

- §1 et §3 de ce closeout — les concepts validés et les responsabilités mal
  placées ;
- le registre `1550/02_FINDINGS_REGISTER.md` — 36 constats mesurés, dont une
  majorité porte sur le **canon** et non sur GCG ;
- les mesures reproductibles : quatre réinventions de la non-rétroactivité,
  14 closeouts mutés sur 157, 243 commits non signés sur 244, 75 runs sur 164
  dont l'identité diverge de leur `started_at`.

### 6.6 Dettes connues

| Dette | Nature | Portée |
|---|---|---|
| **`Q10` — le P0 sur la certification v1.1 publiée** | fait établi sur `main`, découvert par cette branche | **survit à la branche.** Enregistré uniquement dans des répertoires de run non fusionnés — voir §6.7 |
| **`GCG-36` non épinglé** | constat P0 `CONFIRMED` sans entrée de corpus | porte sur du code de branche ; disparaît si la branche est abandonnée |
| **9 dispositions de connaissance positives sans section Harvest** | fait mesuré sur `main` | **survit à la branche.** Leur qualification dépend d'une décision non prise |
| **`G7`** — le hook pre-commit exige la clôture complète en annonçant valider les sections du plan | défaut d'outillage sur `main` | différé par décision explicite, antérieur à cette branche |
| **5 pins de corpus écrits sous une contrainte « aucun code »** | l'obligation de corpus est en amont de toute contrainte de périmètre qu'un run se donne | révèle un défaut de couche (§3.6), pas une faute du run |
| **`AUD-F8`** — `TEMPORAL_PROVENANCE.md` obsolète, la dashboard relabellise des artefacts neufs en preuve historique | risque OPEN au registre du dépôt | antérieur, propriétaire distinct, **directement lié à `Q1`** |
| **Voie `CLOTURE` et symétrie des versions** | défaut d'outillage sur `main`, constaté en clôturant | `validate_*_governance` exige que `adversarial_governance_version` soit déclaré dans `01_INTAKE.md` **et** `07_CLOSEOUT.md`, ou dans aucun — or `CLOTURE` est définie comme n'exigeant pas d'intake. Un run de clôture post-cutoff ne peut donc pas déclarer sa version adverse sans ajouter un artefact que sa voie ne requiert pas. Ce run a ajouté l'intake ; le défaut reste entier. Non arbitré ici |

### 6.7 Une dette de clôture, à trancher

`docs/AUDIT_STATUS.md` déclare `PARTIAL — P0/P1 closed and revalidated`. C'est
inexact depuis le run `1021` : le P0 sur la certification v1.1 publiée (`Q10`)
est ouvert et n'y figure pas.

J'ai commencé à l'y inscrire, puis **annulé la modification** : inscrite sur une
branche qui ne doit pas être fusionnée, elle disparaîtrait avec elle, et
mélangerait un fait vrai de `main` avec un chantier explicitement mis de côté.

**À trancher** : `Q10` doit atteindre `docs/AUDIT_STATUS.md` par un chemin qui ne
dépend pas de cette branche — un correctif documentaire direct sur `main`. Ce
closeout ne le fait pas, parce qu'il porterait alors une modification hors de son
périmètre déclaré. Le point est nommé plutôt que réglé en silence.

---

## Scoped quality pass

`N/A (docs-only)` — ce closeout ne touche aucun code produit. Aucun fichier de
code n'est modifié, ajouté ou supprimé par ce run.

## ASSURANCE_STATUS

```yaml
ASSURANCE_STATUS:
  schema_version: "1.1"
  subject: "feat/governance-compatibility-gate closed as an exploration phase, 4bfd65e -> closeout SHA"
  gate_results:
    - gate_id: "exploration-branch-closure"
      gate_family: "OTHER"
      checkpoint: "CLOSEOUT"
      subject: "the branch is closed as exploration, not proposed for integration"
      verdict: "PASS"
      evidence:
        - "4 commits, 36 files, +7430/-1, unpushed, no commit on main"
        - "no code, no model change and no new concept produced by this closeout"
        - "every artifact judged non-mergeable is named with its reason (§6.4)"
      reasons:
        - "closure is voluntary: no technical blocker forced it"
    - gate_id: "vbb-governance-compat"
      gate_family: "CERTIFICATION"
      checkpoint: "CLOSEOUT"
      subject: "post-cutoff run population against adversarial 1.1"
      verdict: "FAIL"
      evidence:
        - "exit 2, current conformance 2/16"
      reasons:
        - "the instrument stays red and unwired; it is not merged and its verdict is not laundered"
  implementation_authorization:
    status: "NOT_AUTHORIZED"
    required_gate_ids:
      - "vbb-gate-check-adr-poc-integration"
    reasons:
      - "no implementation is authorized: the branch is closed as exploration"
      - "the tool, the model, the tests and the corpus pins are declared non-mergeable in §6.4"
  implementation_status: "ABANDONED"
  conformity_status: "NOT_APPLICABLE"
  adversarial_status: "FINDINGS_OPEN"
  certification_status: "NOT_CERTIFIED"
  final_status: "HANDOFF"
```

## Bloc adverse

```yaml
adversarial:
  level: "A2"
  campaign_ref: "docs/runs/2026-07-29_1550_gcg-findings-arbitration/04_INDEPENDENT_ARBITRATION_REVIEW.md"
  corpus_version: "1.2.0"
  exploration_performed: true
  surfaces_declared:
    - "the closeout as a place to rehabilitate an abandoned model"
    - "the validated-concepts section as a way to smuggle the mechanism back in"
    - "the open questions as disguised proposals"
    - "the branch state as an understated inventory of what must not merge"
  surfaces_unexplored:
    - "no third review was conducted on this closeout itself"
    - "the 14 findings of 2026-07-28_2200 (Q-inherited, never instructed)"
    - "any rule set outside this repository"
  residual_uncertainty: |
    This closeout judges concepts produced by its own author, after two reviews
    established that the author is systematically more generous toward the core
    than the evidence supports. §1 was written against that known bias — the
    two-bound distinction, the chantier's most attractive idea, is placed in
    §2 Fragile and not in §1 Validated. That placement is the main thing a
    third reader should challenge.
  defender_identity:
    agent: "claude-opus-5 (Claude Code)"
    llm: "claude-opus-5"
    system_prompt_version: "claude-code-2026-07"
  attacker_identity:
    agent: "claude-opus-5 (Claude Code, isolated subagent a2f715163e55cc42e, run 1550)"
    llm: "claude-opus-5"
    system_prompt_version: "claude-code-2026-07"
    session: "7d41772d-7943-4130-8c25-55882072a2b2"
  findings: []
  verdict: "FINDINGS_OPEN"
  non_claim: |
    No PASS_ADVERSARIAL is claimed, and none was claimed on any of the five runs
    of this chantier. A2_DISTINCT_AGENT_PROXY was never satisfied: attacker and
    defender shared the LLM family and the system prompt every time. What was
    obtained is context isolation, whose yield is measurable and is reported as
    such in §5.2, not as a substitute for a distinct actor.

    `findings: []` is deliberate. This closeout conducts no campaign: it records
    the outcome of campaigns run elsewhere. The 36 findings live in
    docs/runs/2026-07-29_1550_gcg-findings-arbitration/02_FINDINGS_REGISTER.md,
    which remains their durable carrier and is preserved by this branch.
  certification:
    status: "NOT_CERTIFIED"
  certification_blocker: |
    A2 requires an actor distinct by LLM family, system prompt and
    provider-or-human. None was available across the whole chantier. The subject
    is in any case abandoned, not certified: an abandoned exploration carries no
    certifiable claim.
```

## Vérification P.R2

| # | Commande | Résultat |
|---|---|---|
| 1 | `vbb-architecture.py lint` | PASS — 0 error, 0 warning, 11 blocks |
| 2 | `vbb-architecture.py graph --write` | `docs/RELATIONS.md` régénéré, **identique** |
| 3 | `vbb-contract-lint.py` | PASS — 0 error, 1 warning non bloquant (`F12`) |
| 4 | `vbb-loop-closure-check.py <run_id> --strict` | voir §Vérification finale |
| 5 | `python -m pytest tests/ -q` | PASS — 447 passed, 1 skipped |
| 5 | `bash scripts/vbb-ci-local.sh` | PASS — 16 passed, 0 failed, 0 warnings |
| 5b | `vbb-adversarial-gate.py <run_id> --strict` | FAIL attendu — `adv-a2-distinct`, même famille de LLM |
| 5b | `python -m pytest tests/adversarial_corpus/ -q` | PASS — 18 passed |
| — | `vbb-governance-compat.py --strict` | FAIL — exit 2, `2/17`, **non blanchi** |
| — | credentials gate | PASS — 0 finding |

Ce run entre à son tour dans la population qu'il mesure et s'y classe
`CURRENT_NONCOMPLIANCE`, faute d'acteur A2 distinct — comme les cinq runs du
chantier. `2/16` → `2/17` : le dénominateur monte, le numérateur non. **C'est le
dernier artefact que cette branche ajoute à sa propre mesure, et il n'améliore
rien.** L'instrument mesure sa propre clôture et la juge non conforme, ce qui est
le comportement correct.

## Knowledge Harvest

Trois candidats, tous en `OBSERVATION`. Aucun promu — la promotion exige le
parcours d'ADR 0049.

1. **Un auteur et un lecteur indépendant n'attaquent pas le même axe.** L'auteur
   testant la généricité de son modèle trouve des manques de spécification ; un
   lecteur indépendant trouve des failles exploitables. Ce ne sont pas deux
   niveaux de rigueur mais deux axes, et l'auteur choisit systématiquement le
   plus sûr. Un subagent n'est donc pas substituable par davantage de travail de
   l'auteur. *Portée : mesuré sur un chantier, cinq runs, deux revues.*

2. **Une discipline de séparation appliquée aux outils et pas aux analystes ne
   protège rien.** Le principe « une certification n'est jamais dérivable d'un
   verdict de conformité » était implémenté, testé, et violé par son auteur dans
   une table d'analyse — invisible depuis l'intérieur, précisément parce que
   l'auteur croyait connaître la règle.

3. **Un besoin confirmé ne valide pas la réponse qu'on lui apporte.** Le dépôt a
   réinventé la non-rétroactivité quatre fois : le problème est réel et mesuré.
   Cela n'a jamais rien dit de la validité du modèle proposé, et la confusion
   entre les deux est ce qui a maintenu le chantier ouvert quatre runs de plus
   qu'il n'aurait fallu.

Portée : observations d'un chantier sur un dépôt. Pas des règles canoniques.

## Session recommandée ensuite

**Aucun run de reprise de GCG.** La séquence de dix runs proposée en
`1550/06_RESUMPTION_SEQUENCE.md` est **caduque** : elle organisait la réparation
d'un modèle que cette clôture met de côté. Elle reste lisible comme inventaire de
ce qu'il aurait fallu réparer.

Ce qui reste ouvert et **ne dépend pas de GCG** :

1. **`Q10`** — statuer sur la certification v1.1 publiée, et l'inscrire au
   registre de `main` (§6.7). Indépendant, P0, antérieur à cette branche.
2. **`Q1`** — décider si le dépôt se dote d'un substrat d'attestation. C'est la
   fondation dont l'absence a clos cette phase ; toute reprise architecturale la
   suppose.
3. Les questions `Q2` à `Q9`, dans l'ordre que fixera cette réflexion.

## FINAL_STATUS

```yaml
FINAL_STATUS: HANDOFF
reason: |
  La phase d'exploration est close proprement : le travail est conservé
  intégralement, rien n'est fusionné, et ce qui ne doit pas l'être est nommé
  avec son motif. Ce qui manque n'est pas du travail sur GCG — c'est une
  décision d'architecture (Q1) qui précède le modèle et qu'aucun correctif
  n'aurait pu produire. COMPLETE serait faux : dix questions restent ouvertes,
  dont une P0 qui porte sur `main` et survit à cette branche.
implementation_complete: false
verification_complete: true
adversarial_certification: false
next_action: |
  Ne pas rouvrir GCG. Traiter Q10 (certification v1.1 publiée) par un chemin
  indépendant de cette branche, puis instruire Q1 (substrat d'attestation) comme
  décision d'architecture. La branche `feat/governance-compatibility-gate` reste
  en l'état, non poussée et non fusionnée, comme trace d'exploration.
```
