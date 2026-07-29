# Governance Compatibility — modèle conceptuel

**Statut : `PROPOSED`.** Ce document décrit un modèle soumis à validation
humaine (Critical Rule 9). Il n'est pas canon tant qu'il porte ce statut, et
aucune règle décrite ici n'est opposable avant validation.

Proposition de canon associée :
`docs/runs/2026-07-29_1021_adversarial-gate-population/03_CANON_CHANGE_PROPOSAL.md`
Run de consolidation : `docs/runs/2026-07-29_1050_gcg-conceptual-model/`

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

## 4. Modèle de classification

Sept catégories. Une et une seule par couple (artefact, règle).

| Catégorie | Condition | Bloquant |
|---|---|---|
| `CURRENT` | conforme au canon courant | non |
| `HISTORICAL_VALID` | antérieur à `applies_from` | non |
| `MIGRATION_AVAILABLE` | dans la fenêtre de dette, migration déterministe possible depuis artefacts contemporains | non, compté |
| `HISTORICAL_NONCOMPLIANCE` | dans la fenêtre de dette, preuve non reconstructible | non, compté |
| `CURRENT_NONCOMPLIANCE` | postérieur à `enforcement_effective_from`, règle applicable, échec réel | **oui** |
| `OVERCLAIM` | revendique un verdict positif sans structure permettant de le valider | **oui, immédiat** |
| `UNKNOWN` | dans la fenêtre de dette, aucune disposition arbitrée | **oui, jusqu'à arbitrage** |
| `PENDING_LIFECYCLE` | l'artefact porteur de la preuve n'existe pas encore | non |

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

Les invariants I2, I4 et I6 sont aujourd'hui couverts par
`tests/test_governance_compat_gate.py`. I1, I3, I5, I7, I8 ne le sont pas
encore — ils n'ont pas de porteur exécutable.

## 6. Compatibility Act et démarrage de session

### 6.1 Contenu

```yaml
governance_compatibility_act:
  produced_at: "<timestamp>"
  canon_versions: {adversarial-assurance: "1.1", ...}
  population: {total: N, applicable: M}
  classification: {CURRENT: n, HISTORICAL_VALID: n, ...}
  readings:
    current_conformance: "n/m"
    historical_debt: n
    certification: "NOT_DERIVABLE_FROM_THIS_GATE"
  blocking: [...]
  migration_run_recommended: true|false
  confidence: "HIGH|DEGRADED"
```

Les trois lectures restent orthogonales. Aucune n'est dérivable d'une autre.

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

## 7. Portée actuelle et extension

Le modèle est générique ; **une seule règle est instrumentée** :
`adversarial-assurance 1.1`.

Aucune extension à une autre dimension (design certification, engineering
knowledge, conventions) n'est autorisée sans nouvelle proposition de canon. Un
modèle générique appliqué à une seule règle est un modèle non éprouvé : la
deuxième règle est celle qui dira si l'abstraction tient.

## 8. Questions ouvertes — non tranchées par ce document

1. **Un run d'arbitrage normatif porte-t-il sa propre campagne adverse**, ou
   consomme-t-il celle du run qu'il arbitre ? (matrice §3.3)
2. **`adversarial_level: A2` implique-t-il toujours l'obligation de campagne**,
   ou existe-t-il un `NOT_REQUIRED` légitime ? (matrice §3.6)
3. **Le `PASS_ADVERSARIAL` de `2026-07-30_0500` est-il dérivable** d'un run
   conforme ? Sinon, une certification publiée doit être révisée. (matrice §3.10)

Ces trois questions bloquent le ledger, donc le moteur de migration, donc le
câblage CI. Elles relèvent de l'arbitration humaine (§2.2).

## 9. Ce que ce modèle ne fait pas

- Il ne juge pas si une décision de gouvernance est bonne ; il détecte que deux
  surfaces ne peuvent pas être vraies simultanément.
- Il ne remplace pas la revue adverse ; il en mesure la présence.
- Il ne produit aucune certification ; il rend explicite qu'il n'en produit pas.
