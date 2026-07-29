# Governance Compatibility — modèle conceptuel

**Statut : `PROPOSED` — version 2.** Ce document décrit un modèle soumis à
validation humaine (Critical Rule 9). Il n'est pas canon tant qu'il porte ce
statut, et aucune règle décrite ici n'est opposable avant validation.

Proposition de canon associée :
`docs/runs/2026-07-29_1021_adversarial-gate-population/03_CANON_CHANGE_PROPOSAL.md`
Run de consolidation : `docs/runs/2026-07-29_1050_gcg-conceptual-model/`
Run de stress test : `docs/runs/2026-07-29_1130_gcg-genericity-stress-test/`

## Historique des versions

| Version | Origine | Ce qui a changé |
|---|---|---|
| v1 | run `1050` | modèle initial : trois responsabilités, deux bornes, huit catégories, I1–I8 |
| **v2** | run `1130` — stress test sur 4 règles | §3.4 contrat d'applicabilité · §3.5 unité de frontière · §3.6 contrat de population · §3.7 résolution d'artefact · §6.1 acte multi-règles · I9–I11 |

La v2 ne modifie aucune catégorie et aucun invariant de la v1. Elle **ajoute ce
qui manquait pour appliquer le modèle à une deuxième règle** : le noyau de
classification a résisté au test, sa périphérie d'application non. Constats
détaillés et mesures : `.../1130_gcg-genericity-stress-test/02_STRESS_TEST.md`.

---

## 1. Ce que la capacité résout

Un framework dont la gouvernance évolue produit mécaniquement, à chaque
évolution, un patrimoine documentaire non conforme au canon courant. Sans
modèle, trois issues seulement, toutes mauvaises :

1. réécrire l'historique pour le rendre conforme — falsification ;
2. bloquer tout travail futur sur un passé irréparable — paralysie ;
3. désactiver le contrôle — retour au décoratif.

**Principe fondateur.** Une évolution de la gouvernance ne rend jamais
automatiquement l'historique faux. Le framework distingue explicitement ce qui
était valide sous son canon d'origine, ce qui est migrable sans fabriquer de
preuve, ce qui est en dette, et ce qui est en défaut maintenant.

## 2. Architecture — trois responsabilités séparées

La séparation est structurelle : aucun composant ne doit à la fois observer,
juger et modifier.

```
┌─────────────────────────┐
│  Compatibility Scanner  │  observe, classe, ne modifie jamais
│  (lecture seule)        │  produit → Compatibility Act
└───────────┬─────────────┘
            │  Act (classification + questions ouvertes)
            ▼
┌─────────────────────────┐
│  Arbitration (humain)   │  seule autorité pouvant résoudre UNKNOWN,
│  (décision)             │  accepter une dette, retirer un OVERCLAIM
└───────────┬─────────────┘
            │  Ledger (dispositions arbitrées, justifiées)
            ▼
┌─────────────────────────┐
│  Migration Engine       │  applique les migrations autorisées,
│  (écriture)             │  ne classe jamais, ne décide jamais
└─────────────────────────┘
```

### 2.1 Compatibility Scanner

- **Peut** : lire les artefacts, lire les déclarations de règles, exécuter les
  validateurs existants, lire le ledger, produire un `Compatibility Act`.
- **Ne peut pas** : écrire dans un artefact, écrire dans le ledger, décider
  d'une disposition que le ledger ne contient pas.
- **Invariant** : deux exécutions du scanner sur le même état produisent le même
  acte. Le scanner n'a pas de mémoire et pas de jugement.

État actuel : `tools/vbb-governance-compat.py` est le scanner. Il respecte déjà
la contrainte de lecture seule.

### 2.2 Arbitration

Fonction **humaine**, non automatisable par construction. C'est la seule
autorité qui peut :

- résoudre un `UNKNOWN` en une disposition ;
- accepter une dette historique ;
- statuer sur un `OVERCLAIM` (retrait de la revendication ou production d'une
  attestation dérivée vérifiable) ;
- réviser un niveau de gouvernance déclaré à tort.

Sa sortie est le **ledger** : une table où chaque ligne porte un `run_id`, une
disposition, et une justification opposable. Une ligne sans justification est
invalide.

### 2.3 Migration Engine

- **Peut** : déplacer une information, convertir un format, compléter un champ
  déductible sans ambiguïté depuis un artefact contemporain.
- **Ne peut pas** : inventer un résultat, modifier une certification passée,
  changer un niveau de gouvernance, écrire une migration non inscrite au ledger,
  classer quoi que ce soit.
- **Invariant** : toute écriture du moteur est traçable à une ligne de ledger et
  à un artefact contemporain source. Une migration sans source est un défaut du
  moteur, pas une donnée manquante.

Non implémenté. Ne doit pas l'être avant que le ledger existe.

## 3. Déclaration de règle — le contrat de cutoff

Toute règle de gouvernance datée déclare, dans son document canonique :

```yaml
rule:
  id: "adversarial-assurance"
  version: "1.1"
  applies_from: "2026-07-28_1400"              # identité de run
  enforcement_effective_from: "2026-07-28_2000" # identité de run
  enforcement_evidence:                         # preuve, non normative
    commit: "921a780ccf8299bc37099b377ce4e7d0d8ba2561"
    note: "commit ayant introduit vbb-adversarial-gate.py"
```

### 3.1 Deux bornes, pas une

C'est la distinction centrale du modèle, et elle n'existait pas dans le canon.

- **`applies_from`** — date à partir de laquelle l'obligation existe.
- **`enforcement_effective_from`** — date à partir de laquelle un mécanisme est
  capable de la vérifier.

Elles ne coïncident presque jamais. Une règle est écrite, puis outillée.

### 3.2 La fenêtre de dette

```
   applies_from                enforcement_effective_from
        │                                │
────────┼────────────────────────────────┼──────────────────►
        │      FENÊTRE DE DETTE          │   ZONE DE DÉFAUT
HISTORICAL_VALID                          
        │  obligation existante,         │  obligation existante
        │  vérification impossible       │  ET vérifiable
```

**Un artefact ne peut recevoir une disposition de dette que s'il tombe dans la
fenêtre de dette.** En dehors, jamais. C'est la règle anti-blanchiment, exprimée
en termes de canon plutôt qu'en termes de code.

Corollaire : la fenêtre est **bornée et immuable** une fois la règle publiée.
Elle ne s'élargit pas avec le temps. Un artefact produit aujourd'hui ne pourra
jamais y entrer.

**La fenêtre vide est l'état cible, pas un cas dégénéré** *(v2, amendement A5).*

Une règle livrée avec son vérificateur a `applies_from ==
enforcement_effective_from`, donc une fenêtre nulle, donc aucune dette
admissible. C'est le cas de `engineering-knowledge 1.0` : règle et validateur
publiés dans le même run (`2026-07-27_1712`, commit `ae273b5`).
`adversarial-assurance 1.1` a au contraire une fenêtre de six heures — publiée
à `1400`, outillée à `2000` — et c'est exactement là que se trouvent ses quatre
`UNKNOWN`.

La largeur de la fenêtre **mesure combien de temps le canon a exigé quelque
chose qu'il ne savait pas vérifier**. Ce n'est pas un paramètre technique, c'est
un indicateur de qualité de publication d'une règle. Un canon discipliné produit
des fenêtres vides.

### 3.3 Le commit est une preuve, pas une norme

*(Correction demandée — point 5.)*

`enforcement_effective_from` est une **identité de run déclarée par le canon**.
Le SHA n'apparaît qu'en `enforcement_evidence`, à titre de preuve
d'implémentation.

L'implémentation actuelle dérivait la borne par archéologie git (quel commit a
ajouté le fichier → quel run l'a produit). Cette dérivation était signalée comme
incertitude résiduelle dans le closeout du run `1021` : le mapping avait été
établi par lecture d'artefacts, pas mécaniquement. La déclaration canonique
supprime l'incertitude au lieu de la documenter.

Règle : **une frontière normative n'est jamais dérivée d'un artefact technique.**
Elle est déclarée. Le technique la prouve.

### 3.4 Contrat d'applicabilité — trois sources, jamais une

*(v2, amendement A1 — répare S1.)*

La v1 déterminait l'applicabilité d'une règle à un artefact par **un seul test
temporel** : identité ≥ `applies_from`. Le canon en pratique en utilise trois
(`_knowledge_governance_required`, `vbb-loop-closure-check.py`, et ses jumeaux
assurance et adverse) :

| # | Source | Nature |
|---|---|---|
| 1 | identité de l'artefact ≥ `applies_from` | immuable, lisible sans ouvrir l'artefact |
| 2 | horodatage déclaré (`started_at`) ≥ `applies_from` | contenu de l'artefact |
| 3 | **auto-déclaration** de la version dans l'artefact | volontaire, quelle que soit la date |

**Une règle s'applique dès qu'une source le dit** — union, jamais intersection.
La source 3 est un opt-in ascendant : un artefact antérieur qui se déclare
gouverné l'est, et ne peut pas se rétracter ensuite.

**Invariant I9 en découle directement.** Un scanner qui n'implémente qu'un
sous-ensemble de la disjonction est au plus aussi strict que l'enforcer, et
strictement plus permissif dès qu'une source non implémentée se déclenche. *Un
gate de compatibilité plus permissif que le gate qu'il mesure masque des échecs
au lieu de les qualifier* — l'inverse exact de sa raison d'être.

État : `tools/vbb-governance-compat.py` n'implémente que la source 1. Défaut
enregistré (S1), latent aujourd'hui, **bloquant pour le câblage CI**.

### 3.5 Unité de la frontière — la valeur ne suffit pas

*(v2, amendement A2 — répare S2.)*

La §3.3 exige que la frontière soit déclarée. Nécessaire, insuffisant :
`applies_from: "2026-07-28_1400"` **ne déclare pas un instant** tant que l'unité
n'est pas dite. Une identité de run n'a pas de fuseau intrinsèque, et le corpus
contient les deux conventions — identité en heure locale pour les runs qui
définissent le cutover adverse, identité en UTC pour ceux qu'il gouverne. Deux
heures d'écart, pour une fenêtre large de six.

Toute borne déclare donc :

```yaml
applies_from:
  value: "2026-07-28_1400"
  unit: "run_identity"        # run_identity | utc_instant
  timezone: "Europe/Paris"    # requis si unit == run_identity
```

**Granularité.** Une identité sans composante horaire (`20260615-usage-audit`,
`2026-07-12_run09`) ne dénote pas un instant mais un **intervalle de 24 h**.
Elle est alors traitée comme un intervalle, et la règle fail-closed retient la
borne **la plus inclusive** : l'artefact est réputé gouverné.

### 3.6 Contrat de population — ce sur quoi une règle porte

*(v2, amendement A3 — répare S4.)*

La v1 parlait de « l'artefact » sans jamais dire de quelle classe d'artefacts.
Or la moitié historique du modèle exige trois propriétés que rien ne déclarait :

| Propriété | Signification | Sans elle |
|---|---|---|
| `dated` | chaque membre porte un instant de production | aucune borne n'est comparable |
| `immutable` | un membre est un enregistrement, pas un objet vivant | « conforme au canon de son époque » n'a pas de sens |
| `enumerable` | la population est close et parcourable | il n'y a rien à classer |

```yaml
population:
  kind: "runs"        # runs | skills | contracts | …
  dated: true
  immutable: true
  enumerable: true
```

**Mode dégradé.** Si `dated` ou `immutable` est faux, seules
`CURRENT`, `CURRENT_NONCOMPLIANCE`, `OVERCLAIM` et `PENDING_LIFECYCLE` sont
attribuables. `HISTORICAL_VALID`, `MIGRATION_AVAILABLE`,
`HISTORICAL_NONCOMPLIANCE` et la fenêtre de dette sont **indéfinis**, et
**aucune dette n'est admissible**.

Ce n'est pas une perte. Pour une population mutable, la migration est toujours
disponible : réécrire un skill ne falsifie rien, parce qu'un skill n'est pas un
enregistrement historique. C'est ce qu'a fait ADR 0042 — les douze skills
divergents normalisés en une passe, puis le lint bloque la dérive, zéro dette.

Si `enumerable` est faux, la règle est **hors périmètre GCG**. C'est le cas des
gates de flux (ADR 0033, credentials) : ils gouvernent des transitions, pas des
états. GCG gouverne des états.

### 3.7 Résolution d'artefact — déclarée par la règle

*(v2, amendement A6 — répare S5.)*

« L'artefact porteur de la preuve » doit être résolu par une fonction **déclarée
par la règle**, jamais choisie par le scanner. Deux résolveurs divergents
coexistent aujourd'hui — repli `*CLOSEOUT*.md` d'un côté, chemin en dur
`07_CLOSEOUT.md` de l'autre — et `2026-07-28_1200_m1` (qui contient
`02_CLOSEOUT.md`) est classé « a un closeout » par l'un et « n'en a pas » par
l'autre.

L'enjeu n'est pas cosmétique : `PENDING_LIFECYCLE` s'attribue sur l'**absence**
de l'artefact. Si l'identité de l'artefact dépend du résolveur, une variante de
nommage produit un `PENDING_LIFECYCLE` faux — une violation de I6 par une voie
que la limite stricte de §4.1 ne couvre pas. Cette limite gouverne le *motif* de
la classification ; elle ne gouverne pas la *résolution* de l'artefact.

## 4. Modèle de classification

Huit catégories. Une et une seule par couple (artefact, règle) — **jamais par
artefact seul** : un même artefact peut être `OVERCLAIM` sous une règle et
conforme sous une autre.

La colonne *Population* indique le prérequis de §3.6 : `—` signifie que la
catégorie est toujours attribuable, `D+I` qu'elle exige une population datée et
immuable.

| Catégorie | Condition | Population | Bloquant |
|---|---|---|---|
| `CURRENT` | conforme au canon courant | — | non |
| `HISTORICAL_VALID` | antérieur à `applies_from` | **D+I** | non |
| `MIGRATION_AVAILABLE` | dans la fenêtre de dette, migration déterministe possible depuis artefacts contemporains | **D+I** | non, compté |
| `HISTORICAL_NONCOMPLIANCE` | dans la fenêtre de dette, preuve non reconstructible | **D+I** | non, compté |
| `CURRENT_NONCOMPLIANCE` | postérieur à `enforcement_effective_from`, règle applicable, échec réel | — | **oui** |
| `OVERCLAIM` | revendique un verdict positif sans structure permettant de le valider | — | **oui, immédiat** |
| `UNKNOWN` | dans la fenêtre de dette, aucune disposition arbitrée | **D+I** | **oui, jusqu'à arbitrage** |
| `PENDING_LIFECYCLE` | l'artefact porteur de la preuve n'existe pas encore | — | non |

### 4.1 `PENDING_LIFECYCLE` — et sa limite stricte

*(Renommage demandé — point 6. Ancien nom : `OUT_OF_SCOPE`.)*

Le nom précédent était faux : un run en cours n'est pas hors périmètre, il n'a
pas encore atteint l'étape de son cycle de vie qui produit la preuve.

**Limite stricte, et elle est essentielle.** La catégorie est admissible
uniquement quand **l'artefact qui porterait la preuve n'existe pas encore**.
Elle n'est jamais admissible pour un artefact qui existe et échoue.

Un run clos qui échoue parce qu'il attend une revue indépendante est
`CURRENT_NONCOMPLIANCE`, pas `PENDING_LIFECYCLE`. Sans cette limite, tout run
défaillant se déclare « en attente d'une étape ultérieure » et la catégorie
devient une auto-exemption — le même vecteur de blanchiment que le ledger, sous
un autre nom.

Test de discrimination : *la preuve manque-t-elle parce qu'elle n'a pas encore
été produite, ou parce qu'elle a été produite et est insuffisante ?* Le premier
cas est un cycle de vie ; le second est un défaut.

### 4.2 `OVERCLAIM` — généralisation

*(Généralisation demandée — point 5 de ta liste de validation.)*

`OVERCLAIM` n'est pas propre à la dimension adverse. C'est une propriété
générale, indépendante du jeu de règles :

> Un artefact affirme un verdict positif (`PASS`, `CERTIFIED`, `READY`,
> `APPROVED`) sans porter la structure qui permettrait de le valider.

Elle prime sur toute lecture historique, y compris `HISTORICAL_VALID` :
l'ancienneté ne rend pas une fausse affirmation moins lue ni moins crue. Une
omission est inerte ; une revendication est active.

C'est la seule catégorie **non migrable**. Elle ne se résout que par :

- **retrait** de la revendication, ou
- **attestation dérivée** : lien vérifiable vers un artefact conforme qui porte
  réellement le verdict revendiqué — jamais une recopie du verdict.

Application immédiate hors du sujet adverse : un closeout portant
`status: READY` avec `FINAL_STATUS: HANDOFF` (finding `G3`) relève de cette
définition. Le modèle absorbe R3 du plan de remédiation.

**Seconde instance, trouvée par mesure** *(v2, stress test S6).* Sur la règle
`engineering-knowledge 1.0`, `EVIDENCE_LINKED` est défini comme *« evidence was
linked to an existing candidate »*. Le validateur ne vérifie que l'appartenance
à l'énumération, il ne résout aucun lien ; il n'existe aucun registre de
candidats dans le dépôt ; et neuf runs déclarent une disposition positive sans
section *Knowledge Harvest* dans le corps du closeout.

Forme strictement identique à `PASS_ADVERSARIAL` sans bloc validable, sur une
règle sans rapport. C'est la confirmation la plus forte de la généricité du
modèle : la seconde instance n'a pas été reconduite par analogie, elle a été
**mesurée** sur une règle choisie avant de savoir ce qu'on y trouverait.

## 5. Invariants — ce qui ne doit jamais pouvoir arriver

Ces énoncés sont des propriétés testables, pas des intentions.

| # | Invariant |
|---|---|
| I1 | Une migration ne produit jamais une information absente des artefacts contemporains de l'artefact migré. |
| I2 | Un artefact hors de la fenêtre de dette ne reçoit jamais une disposition de dette, quel que soit le contenu du ledger. |
| I3 | Un niveau de gouvernance n'est jamais abaissé pour obtenir un verdict favorable. |
| I4 | La certification n'est jamais dérivée d'un verdict de conformité. |
| I5 | `OVERCLAIM` n'est jamais migrable, jamais ledgerable, jamais adouci par l'ancienneté. |
| I6 | `PENDING_LIFECYCLE` n'est jamais attribué à un artefact existant qui échoue. |
| I7 | Le scanner n'écrit jamais ; le moteur ne classe jamais. |
| I8 | Une frontière normative est déclarée par le canon, jamais dérivée d'un artefact technique. |
| **I9** | Un scanner de compatibilité n'est jamais plus permissif que l'enforcer qu'il enveloppe : il implémente la disjonction complète des sources d'applicabilité (§3.4). |
| **I10** | Une borne déclare sa valeur **et** son unité. Une borne à granularité jour est un intervalle, résolu vers la lecture la plus inclusive (§3.5). |
| **I11** | La résolution de « l'artefact porteur de la preuve » est déclarée par la règle, jamais choisie par le scanner (§3.7). |

**Couverture exécutable — et il faut la regarder en face.** I2, I4 et I6 sont
couverts par `tests/test_governance_compat_gate.py`. I1, I3, I5, I7, I8 ne
l'étaient pas ; I9, I10 et I11 ne le sont pas davantage. Le ratio passe de 3/8 à
**3/11** : la v2 ajoute trois invariants sans ajouter un seul test, parce que la
contrainte du run de stress test interdisait d'écrire du code.

Un invariant sans porteur exécutable est une intention. La v2 est donc plus
complète comme spécification et **pas plus sûre** comme mécanisme. Toute
canonisation doit traiter cet écart, pas l'hériter.

## 6. Compatibility Act et démarrage de session

### 6.1 Contenu

*(v2, amendement A4 — répare S3. Le schéma v1 était mono-règle : table de
comptage plate et ratio de conformité unique. Deux règles aux populations
différentes — 14 applicables pour l'une, 19 gouvernés pour l'autre — le rendent
insensé, et il ne pouvait pas représenter un artefact `OVERCLAIM` sous une règle
et conforme sous une autre.)*

```yaml
governance_compatibility_act:
  produced_at: "<timestamp>"
  confidence: "HIGH|DEGRADED"

  rules:                                  # une entrée par jeu de règles
    - rule_id: "adversarial-assurance"
      version: "1.1"
      population: {kind: "runs", total: N, applicable: M}
      classification: {CURRENT: n, HISTORICAL_VALID: n, ...}
      readings:
        current_conformance: "n/m"        # jamais agrégé entre règles
        historical_debt: n
        certification: "NOT_DERIVABLE_FROM_THIS_GATE"
      blocking: [...]

  verdict: "PASS|FAIL"                    # OR des bloquants de toutes les règles
  migration_run_recommended: true|false
```

Deux contraintes de forme, et elles sont normatives :

1. **Aucun ratio global.** Des populations différentes ne s'additionnent pas.
   Un « taux de conformité du dépôt » serait un chiffre sans référent —
   précisément le genre de nombre qu'on affiche et qu'on croit.
2. **Le verdict global est un `OR`, pas une moyenne.** Une règle bloquante
   bloque, même si dix autres passent.

Les trois lectures restent orthogonales, **à l'intérieur de chaque règle**.
Aucune n'est dérivable d'une autre, et aucune n'est dérivable d'une autre règle.

### 6.2 Mise en cache — obligatoire

Un scan complet à chaque démarrage de session est intenable : le POC a mesuré
plusieurs secondes pour 13 runs sur une population de 161. L'acte est **mis en
cache**, avec une clé d'invalidation explicite :

```
cache_key = hash(versions de règles déclarées) + hash(liste des run_id)
           + hash(mtime du ledger)
```

Un cache invalide n'est pas une erreur : c'est un recalcul. Un cache absent
produit `confidence: DEGRADED`, pas un blocage — un scanner qui empêche de
travailler est un scanner qu'on désactive.

### 6.3 Le run de migration est proposé, jamais ouvert

L'acte peut porter `migration_run_recommended: true`. Il **ne crée aucun run**.

Ouvrir automatiquement un run contournerait le triage obligatoire et le
protocole plan-first. La décision d'ouvrir un chantier appartient à la session,
pas au scanner.

### 6.4 Points d'intervention

1. démarrage de session gouvernée — lecture de l'acte en cache ;
2. après toute évolution du canon — invalidation forcée, recalcul ;
3. avant toute certification `READY` — l'acte doit être frais et sans bloquant.

## 7. Portée — ce qui est éprouvé et ce qui ne l'est pas

*(v2 — la §7 de la v1 annonçait que « la deuxième règle est celle qui dira si
l'abstraction tient ». Elle l'a dit ; voici ce qu'elle a dit.)*

Le modèle a été éprouvé **sur le papier** contre quatre règles du canon
(`02_STRESS_TEST.md`). **Une seule reste instrumentée** :
`adversarial-assurance 1.1`.

| Composant | Statut | Fondement |
|---|---|---|
| Classification (§4) | **éprouvé** | correct sur `engineering-knowledge 1.0` ; correctement inapplicable sur ADR 0042 et ADR 0033 via §3.6 |
| `OVERCLAIM` | **éprouvé, générique** | seconde instance indépendante trouvée par mesure (§4.2) |
| `applies_from` | **corroboré ×3** | trois cutovers ad hoc préexistants : knowledge `1712`, assurance `2145`, adverse `1400` |
| `enforcement_effective_from`, fenêtre de dette | **non corroboré** | aucun des trois précédents n'a de seconde borne ; éprouvé sur la seule règle A |
| Scanner / Arbitration / Engine | **non contredit, non éprouvé** | aucune migration exécutée ; unique précédent = un run humain (ADR 0042) |
| §3.4–§3.7, §6.1, I9–I11 | **spécifiés, non implémentés** | ajoutés par la v2, sans porteur exécutable |

**Ce que GCG est réellement.** Pas un concept nouveau : la factorisation d'un
mécanisme que le dépôt a réinventé quatre fois de façon ad hoc — trois cutovers
en constantes dupliquées, plus le « ne scanner que les lignes ajoutées » d'ADR
0033. C'est le meilleur argument en faveur du modèle, et la meilleure mesure de
sa modestie.

**Généricité interne seulement.** Les quatre règles appartiennent au même canon,
écrites par la même équipe, dans le même style. Aucune règle externe n'a été
testée.

Aucune extension à une autre dimension n'est autorisée sans nouvelle proposition
de canon.

## 8. Questions ouvertes — non tranchées par ce document

1. **Un run d'arbitrage normatif porte-t-il sa propre campagne adverse**, ou
   consomme-t-il celle du run qu'il arbitre ? (matrice §3.3)
2. **`adversarial_level: A2` implique-t-il toujours l'obligation de campagne**,
   ou existe-t-il un `NOT_REQUIRED` légitime ? (matrice §3.6)
3. **Le `PASS_ADVERSARIAL` de `2026-07-30_0500` est-il dérivable** d'un run
   conforme ? Sinon, une certification publiée doit être révisée. (matrice §3.10)

Ces trois questions bloquent le ledger, donc le moteur de migration, donc le
câblage CI. Elles relèvent de l'arbitration humaine (§2.2).

**Ouvertes par le stress test** *(v2)* :

4. **Les 9 runs déclarant une disposition de connaissance positive sans section
   Knowledge Harvest sont-ils des `OVERCLAIM`** au sens de §4.2, ou la
   disposition est-elle justifiée ailleurs ? Si `OVERCLAIM`, une deuxième règle
   entre en dette et le périmètre d'arbitrage double.
5. **Quelle est l'unité déclarée de l'identité de run** — heure locale ou UTC ?
   Le corpus contient les deux (§3.5). La réponse déplace les bornes de la
   fenêtre de dette adverse de deux heures.
6. **Les trois cutovers existants doivent-ils être migrés vers la déclaration
   §3.4/§3.5**, ou coexister ? Ils sont aujourd'hui dupliqués entre deux outils
   — vérité parallèle en attente de dérive (Critical Rule 5).

## 9. Ce que ce modèle ne fait pas

- Il ne juge pas si une décision de gouvernance est bonne ; il détecte que deux
  surfaces ne peuvent pas être vraies simultanément.
- Il ne remplace pas la revue adverse ; il en mesure la présence.
- Il ne produit aucune certification ; il rend explicite qu'il n'en produit pas.
