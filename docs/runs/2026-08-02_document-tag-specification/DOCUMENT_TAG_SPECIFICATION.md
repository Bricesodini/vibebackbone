# Document Tag Specification

## Statut du document

Cette spécification définit le contrat conceptuel minimal des tags
documentaires. Elle ne définit ni syntaxe, ni outil, ni convention de nommage
finale.

Elle ne crée aucune autorité et ne modifie aucun artefact existant.

Verdict : `DOCUMENT_TAG_SPECIFICATION_READY`

## 1. Finalité

Un tag documentaire est une projection vérifiable de l'identité documentaire,
de l'ontologie et du graphe documentaire. Il rend observable le contrat d'une
représentation et permet de comparer cet état avec le contrat déclaré par un
dépôt.

Le tag ne remplace ni le contenu, ni les décisions, ni les preuves, ni la
gouvernance applicable.

## 2. Trois niveaux distincts

### 2.1 Tag d'artefact

Il décrit une représentation documentaire particulière et, lorsque nécessaire,
sa révision, sa source et sa localisation.

Il répond à la question :

> Quel est le contrat observable de cette représentation précise ?

### 2.2 Tag d'état documentaire du dépôt

Il décrit le contrat documentaire que le dépôt déclare appliquer à un état
donné.

Il définit le vocabulaire, les dimensions attendues et les règles de
compatibilité. Il ne rend pas automatiquement conformes les artefacts du
dépôt.

### 2.3 Tag Git de publication documentaire

Il associe un état documentaire validé à un commit déterminé. Il constitue une
preuve immuable de publication, sans devenir la source du contrat.

Ces trois niveaux ne doivent pas être confondus :

```text
Tag d'artefact       = contrat d'une représentation
Tag d'état du dépôt  = contrat déclaré par le dépôt
Tag Git documentaire  = preuve d'un état publié et validé
```

## 3. Champs minimaux du tag d'artefact

Le contrat minimal comprend les champs conceptuels suivants.

| Champ | Obligation | Portée et invariant | Absence ou héritage |
|---|---|---|---|
| Identité documentaire | Obligatoire | Référent stable, indépendant du chemin | Ne s'hérite pas implicitement |
| Représentation | Obligatoire | Matérialisation décrite par le tag | Ne s'hérite pas |
| Révision | Obligatoire pour un état publié | État précis de la représentation | Peut être inconnue seulement avec finding |
| Autorité | Obligatoire si l'artefact revendique une prescription | Autorité observée, jamais créée par le tag | Ne s'hérite pas d'un simple chemin |
| Cycle de vie | Obligatoire | `PROPOSED`, `ACTIVE`, `TRANSITIONAL`, `SUPERSEDED` ou `RETIRED` | Ne s'hérite pas silencieusement |
| Temporalité | Obligatoire | Inclut `CURRENT`, `PAST`, `FUTURE`, `MULTI_PERIOD` ou `UNDATED` | Absence = `UNKNOWN` |
| Fonction principale | Obligatoire | Une seule fonction dominante | Ne s'hérite pas |
| Fonctions secondaires | Facultatif | Rôles additionnels sans autorité nouvelle | Peut être vide |
| Politique de chargement | Obligatoire si l'artefact est consommé par un agent | Moment attendu de chargement | Peut être héritée uniquement d'une règle de dépôt explicite |
| Périmètre d'autorité | Obligatoire pour une autorité bornée | Limite fonctionnelle, temporelle ou opérationnelle | Aucun périmètre ne doit être inventé |
| Source | Obligatoire pour une projection ou distribution dérivée | Identité/représentation source vérifiable | Absence d'une source revendiquée = finding bloquant |
| Provenance ou décision fondatrice | Obligatoire pour une autorité ou une transition revendiquée | Relation vers décision, preuve ou run pertinent | Absence = `UNKNOWN` ou finding selon le risque |
| Version du contrat appliqué | Obligatoire pour un artefact déclaré conforme | Contrat documentaire utilisé pour interpréter le tag | Peut être fournie par l'état du dépôt si l'héritage est explicite |

L'héritage est limité aux informations réellement communes et déclarées par
le contrat du dépôt. Il ne peut jamais fournir implicitement une identité, une
autorité, une source ou une décision fondatrice.

## 4. Contrat documentaire du dépôt

Une déclaration conceptuelle telle que :

```text
document_contract_version: <version>
```

signifie que l'état du dépôt reconnaît une version déterminée du contrat
documentaire.

Cette version définit :

- le vocabulaire autorisé ;
- les dimensions ontologiques attendues ;
- les relations du graphe qui doivent être interprétables ;
- les règles de compatibilité entre versions ;
- les conditions qui imposent une migration ou une décision humaine.

Elle ne signifie pas que tous les artefacts sont conformes. La conformité doit
être vérifiée représentation par représentation.

Un dépôt sans version de contrat ne peut pas être assimilé silencieusement au
contrat courant. Son état est `UNKNOWN` jusqu'à ancrage ou décision humaine.

## 5. Compatibilité conceptuelle

La comparaison entre un tag d'artefact et le contrat du dépôt produit l'un des
résultats suivants.

### COMPATIBLE

Le tag est interprétable par le contrat courant et ses relations, dimensions
et invariants sont respectés.

### MIGRATION_REQUIRED

Le tag est suffisamment compris, mais sa représentation doit être adaptée
pour satisfaire le contrat courant. Aucune migration n'est automatique.

### INCOMPATIBLE

Le tag ou la représentation contredit une règle obligatoire du contrat, ou
revendique une relation impossible à satisfaire.

### UNKNOWN

Les informations disponibles ne permettent pas de conclure : version absente,
dimension inconnue, source non vérifiable ou provenance insuffisante.

Cas particuliers :

- artefact sans tag dans un dépôt versionné : `UNKNOWN`, jamais automatiquement
  `COMPATIBLE` ;
- dépôt sans version de contrat : `UNKNOWN` ;
- tag ancien encore interprétable et sémantiquement compatible :
  `COMPATIBLE` ; une mise à niveau de représentation peut néanmoins rester
  recommandée ;
- tag ancien interprétable mais exprimant un contrat retiré ou incomplet :
  `MIGRATION_REQUIRED` ;
- dimension inconnue utilisée par une règle obligatoire : `UNKNOWN` ; si elle
  contredit explicitement le contrat : `INCOMPATIBLE` ;
- projection dont la source est absente : `UNKNOWN` si l'absence n'est pas
  vérifiable, `INCOMPATIBLE` si la projection revendique une source qui ne
  peut pas exister dans le contrat ;
- runtime issu d'une autre version documentaire : comparaison entre son état,
  sa source, sa révision et le contrat courant ; résultat `COMPATIBLE` seulement
  si la compatibilité est démontrée, sinon `MIGRATION_REQUIRED` ou `UNKNOWN`.

Une conclusion `MIGRATION_REQUIRED` ou `INCOMPATIBLE` produit un finding. Elle
ne déclenche aucune correction silencieuse.

## 6. Relation avec Git

Un éventuel tag Git documentaire :

- pointe vers un commit déterminé ;
- atteste qu'un état documentaire a été validé selon une version de contrat ;
- conserve la date, l'ancre et les preuves nécessaires à l'interprétation ;
- ne devient pas la source du contrat ;
- ne se confond pas avec la version du logiciel ;
- ne réinterprète pas rétroactivement les états antérieurs.

Il doit être indépendant du tag logiciel, tout en pouvant lui être associé
dans un tuple de publication lorsque les deux états ont été validés ensemble.

Le nommage final et la politique d'association restent ouverts.

## 7. Invariants

1. Le tag ne crée jamais l'autorité qu'il déclare.
2. L'identité reste indépendante du chemin, du nom et de la localisation.
3. Une projection ou distribution déclare sa source identifiable.
4. Un artefact sans tag n'est jamais assimilé silencieusement au contrat courant.
5. Une version plus récente ne réinterprète pas rétroactivement l'historique.
6. Un tag Git ne remplace ni le contrat du dépôt ni les tags d'artefacts.
7. L'absence ou l'incohérence d'un champ produit un finding, jamais une
   correction automatique.
8. Les décisions humaines de Critical Rule 16 restent obligatoires.
9. Une fonction secondaire ne crée aucune autorité supplémentaire.
10. Une information héritée doit être traçable jusqu'à sa déclaration source.

## 8. Cas d'usage

### 8.1 Dépôt conforme au contrat courant

Le dépôt déclare une version de contrat, les artefacts possèdent des tags
interprétables et les sources sont vérifiables : `COMPATIBLE`.

### 8.2 Dépôt ancien sans version documentaire

Le vocabulaire et les règles applicables ne peuvent pas être déterminés :
`UNKNOWN`. Aucun contrat courant ne doit être appliqué rétroactivement.

### 8.3 Artefact non tagué dans un dépôt versionné

Le dépôt est interprétable, mais l'artefact ne l'est pas suffisamment :
`UNKNOWN`, avec demande de décision avant toute qualification corrective.

### 8.4 Artefact utilisant une version antérieure compatible

La version est ancienne mais ses dimensions et relations restent comprises et
compatibles : `COMPATIBLE`. Une actualisation peut être décidée séparément.

### 8.5 Projection générée avec source cohérente

La projection déclare son identité source, sa révision et sa relation de
génération ; la source correspond à l'état attendu : `COMPATIBLE`.

### 8.6 Projection orpheline

La projection revendique une génération mais sa source est introuvable ou
incohérente : `UNKNOWN` si le diagnostic est incomplet, sinon
`INCOMPATIBLE`.

### 8.7 Runtime déployé depuis un autre état documentaire

Le runtime est comparé à sa source, sa révision et au contrat du dépôt. Une
divergence prouvée donne `MIGRATION_REQUIRED` ou `INCOMPATIBLE`; une relation
non vérifiable donne `UNKNOWN`.

### 8.8 Tag Git documentaire associé à une release logicielle

Le tag Git documentaire atteste l'état documentaire du commit. L'association
à la release logicielle est informative et ne fusionne pas les deux versions.

### 8.9 Dépôt partiellement migré

Les artefacts conformes peuvent être `COMPATIBLE`, tandis que les artefacts
anciens sont `MIGRATION_REQUIRED` ou `UNKNOWN`. Le dépôt ne doit pas être
déclaré globalement conforme tant que le périmètre restant n'est pas explicite.

### 8.10 Artefact historique conservé sous un ancien contrat

L'artefact peut rester interprétable sous son ancien contrat et être conservé
comme preuve historique. Il n'est pas automatiquement incompatible, mais ne
doit pas être présenté comme conforme au contrat courant.

## 9. Pilote minimal pour Vibe Backbone

Le pilote doit être limité à un petit noyau représentatif, sans classement
massif ni migration.

1. Choisir quelques artefacts portant des responsabilités différentes :
   autorité canonique, runtime, projection, preuve et document historique.
2. Définir conceptuellement les tags et la version cible du contrat.
3. Comparer les tags au contrat du dépôt.
4. Produire les résultats `COMPATIBLE`, `MIGRATION_REQUIRED`, `INCOMPATIBLE`
   ou `UNKNOWN`.
5. Vérifier que chaque écart devient un finding indépendant.
6. Vérifier que Critical Rule 16 demande `OUI`, `NON` ou `PLUS TARD` avant toute
   remédiation.
7. Faire valider le pilote humainement avant toute extension au dépôt complet.

Le pilote doit produire une décision sur l'applicabilité du contrat, pas une
nouvelle exploration conceptuelle.

## 10. Décisions humaines restantes

- Choisir la représentation future du tag sans figer encore sa syntaxe.
- Déterminer l'emplacement de la déclaration de contrat du dépôt.
- Définir les versions compatibles et les règles de compatibilité ascendante.
- Décider quelles fonctions documentaires exigent des champs supplémentaires.
- Définir la politique de validation des tags Git documentaires.
- Déterminer la portée exacte d'un tag de dépôt partiellement migré.
- Décider si certains artefacts legacy doivent rester `UNKNOWN` ou être
  explicitement marqués `MIGRATION_REQUIRED`.

Ces décisions ne modifient pas les invariants minimaux de la présente
spécification.
