# Document Graph Model (DGM)

## Statut du document

Ce document définit un modèle conceptuel générique. Il ne classe aucun
artefact existant, ne définit aucun format technique et ne modifie aucune
gouvernance.

Verdict : `DOCUMENT_GRAPH_MODEL_READY`

## 1. Objet du modèle

Le Document Graph Model décrit les relations entre identités documentaires,
leurs représentations, leurs révisions, leurs autorités, leurs preuves et
leurs usages.

Le graphe répond à la question :

> Quelles relations doivent rester vraies lorsque des artefacts sont révisés,
> générés, distribués, déplacés, validés ou remplacés ?

Le graphe n'est pas un inventaire de fichiers. Il représente des relations
gouvernées, avec une provenance et un niveau de confiance explicites.

## 2. Niveaux du graphe

Les nœuds sont répartis en trois niveaux qui ne doivent pas être confondus.

### 2.1 Graphe des identités

Il décrit la continuité conceptuelle des responsabilités documentaires.

Nœuds principaux :

- `DOCUMENT_IDENTITY` : responsabilité documentaire stable ;
- `AUTHORITY` : autorité applicable à une responsabilité ou à un périmètre ;
- `SCOPE` : périmètre fonctionnel, temporel ou opérationnel ;
- `DECISION` : décision qui établit, borne, modifie ou clôt une autorité ;
- `CONTRACT` : obligation ou interface documentaire explicitement gouvernée.

### 2.2 Graphe des représentations

Il décrit les matérialisations et leurs états.

Nœuds principaux :

- `REPRESENTATION` : expression concrète d'une identité ;
- `REVISION` : état successif d'une représentation ;
- `LOCATION` : emplacement ou environnement d'une représentation ;
- `PROJECTION` : représentation dérivée ou générée depuis une source ;
- `DISTRIBUTION` : représentation fournie à un consommateur ou runtime ;
- `RUNTIME_ARTIFACT` : artefact effectivement installé ou déployé.

### 2.3 Graphe de provenance et de validation

Il décrit pourquoi une relation ou une décision peut être tenue pour fondée.

Nœuds principaux :

- `EVIDENCE` : élément observable soutenant une affirmation ;
- `RUN_ARTIFACT` : résultat d'une exécution gouvernée ;
- `FINDING` : écart ou observation qualifiée ;
- `VALIDATION` : résultat d'un contrôle ou d'une revue ;
- `DECISION_RECORD` : trace durable d'une décision humaine ou gouvernée.

Une même décision peut être liée au graphe des identités et au graphe de
provenance, mais ces deux rôles restent distincts.

## 3. Principes de direction et de cardinalité

Les relations sont orientées. Une relation inverse peut être exposée pour la
lecture, mais elle ne constitue pas nécessairement une seconde relation
indépendante.

Les cardinalités sont exprimées comme suit : `1`, `0..1`, `1..n`, `0..n`.

Une relation obligatoire signifie qu'elle doit être vérifiable pour le type de
nœud concerné, non qu'elle doit être représentée par un mécanisme technique
particulier.

## 4. Famille identité et matérialisation

### REPRESENTED_BY

```text
DOCUMENT_IDENTITY --REPRESENTED_BY--> REPRESENTATION
```

- Cardinalité : `1` vers `1..n` ; une identité publiée possède au moins une
  représentation.
- Obligatoire : oui pour une identité publiée, facultatif pendant une phase
  de conception non publiée.
- Transitive : non.
- Symétrique : non.
- Autorité : aucune création d'autorité ; la représentation hérite seulement
  du rattachement déclaré.
- Migration : permet de déplacer ou multiplier une représentation sans
  changer l'identité.
- Validation : vérifie qu'une représentation n'est pas orpheline.

### REVISION_OF

```text
REVISION --REVISION_OF--> REPRESENTATION
```

- Cardinalité : `1` vers `1`.
- Obligatoire : oui pour toute révision gouvernée.
- Transitive : la chaîne historique peut être parcourue, mais la relation
  elle-même n'est pas transitive.
- Symétrique : non.
- Autorité : aucune nouvelle autorité par elle-même.
- Migration : préserve l'ordre et la continuité des états.
- Validation : vérifie l'appartenance de la révision à la bonne identité.

### LOCATED_AT

```text
REPRESENTATION --LOCATED_AT--> LOCATION
```

- Cardinalité : `1` vers `0..n`.
- Obligatoire : obligatoire pour une représentation publiée ou déployée.
- Transitive : non.
- Symétrique : non.
- Autorité : une localisation ne devient jamais l'identité ni l'autorité.
- Migration : un changement de localisation ne change pas l'identité.
- Validation : vérifie l'écart éventuel entre état publié, local et runtime.

### PART_OF

```text
NŒUD --PART_OF--> NŒUD_COMPOSITE
```

- Cardinalité : `0..n` vers `0..n`.
- Obligatoire : seulement lorsque la composition est gouvernée.
- Transitive : généralement oui pour rechercher l'appartenance globale, mais
  l'appartenance directe doit rester distinguable.
- Symétrique : non.
- Autorité : aucune, sauf si le périmètre composite est explicitement
  autoritatif.
- Migration : une scission ou fusion doit préserver les liens de composition.
- Validation : détecte les nœuds sans parent attendu ou les cycles de
  composition interdits.

## 5. Famille autorité et gouvernance

### GOVERNS

```text
AUTHORITY --GOVERNS--> DOCUMENT_IDENTITY | CONTRACT
```

- Cardinalité : `1` vers `1..n` dans son périmètre.
- Obligatoire : oui pour une autorité active.
- Transitive : non ; l'autorité ne se propage pas à travers une simple
  référence.
- Symétrique : non.
- Autorité : relation normative principale du graphe.
- Migration : tout déplacement de l'autorité exige la conservation du
  périmètre et de la décision qui le justifie.
- Validation : recherche les responsabilités sans autorité et les conflits de
  périmètre.

### BOUNDED_BY

```text
AUTHORITY --BOUNDED_BY--> SCOPE
```

- Cardinalité : `1` vers `1..n`.
- Obligatoire : oui lorsque l'autorité n'est pas globale.
- Transitive : non.
- Symétrique : non.
- Autorité : limite l'autorité ; elle ne l'étend pas.
- Migration : le périmètre doit être conservé ou explicitement redéfini.
- Validation : détecte deux autorités couvrant le même périmètre sans arbitrage.

### ESTABLISHED_BY

```text
AUTHORITY --ESTABLISHED_BY--> DECISION | DECISION_RECORD
```

- Cardinalité : `1` vers `1..n`.
- Obligatoire : oui pour une autorité nouvellement créée ou modifiée.
- Transitive : non.
- Symétrique : non.
- Autorité : rend la base décisionnelle traçable ; la décision n'autorise pas
  automatiquement d'autres responsabilités.
- Migration : rattache toute modification d'autorité à son acte fondateur.
- Validation : détecte les autorités sans décision ou gouvernance identifiable.

### IMPLEMENTS

```text
RUNTIME_ARTIFACT --IMPLEMENTS--> CONTRACT | DOCUMENT_IDENTITY
```

- Cardinalité : `0..n` vers `1` ou plusieurs contrats explicitement disjoints.
- Obligatoire : seulement pour un artefact qui revendique une conformité.
- Transitive : non.
- Symétrique : non.
- Autorité : l'implémentation ne modifie pas le contrat.
- Migration : un changement d'implémentation doit être vérifié contre le
  contrat source.
- Validation : vérifie que le runtime ne prétend pas implémenter un contrat
  absent, supersédé ou incompatible.

## 6. Famille provenance et dérivation

### DERIVED_FROM

```text
REPRESENTATION | REVISION --DERIVED_FROM--> REPRESENTATION | REVISION
```

- Cardinalité : `0..n` vers `0..n`.
- Obligatoire : oui pour une dérivation revendiquée.
- Transitive : la provenance peut être parcourue transitivement, mais chaque
  lien direct doit rester conservé.
- Symétrique : non.
- Autorité : ne crée pas d'autorité ni de nouvelle identité.
- Migration : impose de préserver la chaîne de provenance ou d'enregistrer sa
  rupture.
- Validation : détecte une origine absente ou une dérivation circulaire
  problématique.

### GENERATED_FROM

```text
PROJECTION --GENERATED_FROM--> REPRESENTATION | REVISION
```

- Cardinalité : `1` vers `1..n` lorsque plusieurs sources sont explicitement
  combinées.
- Obligatoire : oui pour toute projection générée.
- Transitive : la chaîne source peut être suivie ; la relation directe n'est
  pas transitive.
- Symétrique : non.
- Autorité : la projection n'est jamais une autorité indépendante par défaut.
- Migration : toute régénération doit rester rattachée à la même source ou
  déclarer une nouvelle relation.
- Validation : détecte les projections orphelines et les projections
  divergentes de leur source.

### PROJECTS

```text
PROJECTION --PROJECTS--> DOCUMENT_IDENTITY | REPRESENTATION
```

- Cardinalité : `1` vers `1..n`.
- Obligatoire : oui pour expliquer le périmètre de la projection.
- Transitive : non.
- Symétrique : non.
- Autorité : la projection expose une autorité ; elle ne la crée pas.
- Migration : permet de recalculer l'impact d'une modification de la source.
- Validation : vérifie que le contenu projeté reste dans le périmètre autorisé.

### SUPPORTED_BY

```text
FINDING | DECISION | VALIDATION --SUPPORTED_BY--> EVIDENCE | RUN_ARTIFACT
```

- Cardinalité : `0..n` vers `0..n` ; obligatoire pour une affirmation qui
  revendique une preuve.
- Transitive : non.
- Symétrique : non.
- Autorité : la preuve soutient une décision ou un constat, mais ne devient
  pas normative.
- Migration : la preuve doit rester retrouvable ou être explicitement
  remplacée par une preuve équivalente.
- Validation : détecte les constats et décisions non rattachés.

### VALIDATED_BY

```text
DOCUMENT_IDENTITY | REPRESENTATION | RELATION --VALIDATED_BY--> VALIDATION
```

- Cardinalité : `0..n` vers `0..n`.
- Obligatoire : selon le niveau de validation revendiqué.
- Transitive : non.
- Symétrique : non.
- Autorité : une validation confirme un état contrôlé ; elle ne crée pas de
  canon.
- Migration : toute relation affectée doit être revalidée si son objet change.
- Validation : détecte les certifications attachées au mauvais état.

## 7. Famille consommation et propagation

### REFERENCES

```text
REPRESENTATION | REVISION | PROMPT --REFERENCES--> DOCUMENT_IDENTITY |
REPRESENTATION | CONTRACT
```

- Cardinalité : `0..n` vers `0..n`.
- Obligatoire : seulement lorsqu'une dépendance de lecture est revendiquée.
- Transitive : non par défaut ; une référence indirecte ne doit pas être
  traitée comme une autorité directe.
- Symétrique : non.
- Autorité : aucune création d'autorité.
- Migration : une référence cassée ou redirigée doit être signalée.
- Validation : détecte les références vers des identités retirées ou
  supersédées sans justification.

### DISTRIBUTED_TO

```text
REPRESENTATION | PROJECTION --DISTRIBUTED_TO--> DISTRIBUTION | LOCATION |
RUNTIME_ARTIFACT
```

- Cardinalité : `0..n` vers `0..n`.
- Obligatoire : oui pour une représentation déclarée comme distribuée.
- Transitive : non.
- Symétrique : non.
- Autorité : la distribution reste subordonnée à l'identité source.
- Migration : impose de vérifier les consommateurs affectés et l'état
  réellement déployé.
- Validation : détecte une distribution divergente de sa source ou un runtime
  sans provenance.

### COMPATIBLE_WITH

```text
NŒUD --COMPATIBLE_WITH--> NŒUD
```

- Cardinalité : `0..n` vers `0..n`.
- Obligatoire : non.
- Transitive : non ; la compatibilité ne se propage pas automatiquement.
- Symétrique : oui, sauf qualification directionnelle explicite.
- Autorité : aucune.
- Migration : permet d'identifier une transition sans supposer une identité
  commune.
- Validation : vérifie que la compatibilité déclarée respecte les périmètres.

### CONFLICTS_WITH

```text
NŒUD --CONFLICTS_WITH--> NŒUD
```

- Cardinalité : `0..n` vers `0..n`.
- Obligatoire : non ; obligatoire lorsqu'un conflit est détecté.
- Transitive : non.
- Symétrique : oui.
- Autorité : ne tranche pas le conflit.
- Migration : bloque la transition lorsqu'il affecte une autorité, une
  dépendance critique ou une provenance.
- Validation : signale les autorités concurrentes et les états incompatibles.

## 8. Famille évolution temporelle

### SUPERSEDES

```text
REVISION | AUTHORITY | REPRESENTATION --SUPERSEDES--> REVISION | AUTHORITY |
REPRESENTATION
```

- Cardinalité : `0..n` vers `0..n`.
- Obligatoire : non ; obligatoire pour revendiquer un remplacement historique.
- Transitive : la chaîne historique peut être parcourue, mais chaque
  supersession directe doit rester traçable.
- Symétrique : non.
- Autorité : la nouvelle version peut devenir applicable selon sa gouvernance,
  mais la relation seule ne suffit pas.
- Migration : conserve l'ancien état et son historique.
- Validation : détecte les références actives vers un état supersédé.

### REPLACES

```text
REPRESENTATION | AUTHORITY --REPLACES--> REPRESENTATION | AUTHORITY
```

- Cardinalité : `0..n` vers `0..n`.
- Obligatoire : non.
- Transitive : non par défaut.
- Symétrique : non.
- Autorité : indique une substitution opérationnelle ; elle ne prouve pas à
  elle seule que le nouveau nœud est canonique.
- Migration : exige une vérification explicite de la continuité, de la
  portée et des dépendances.
- Validation : signale une substitution ambiguë ou sans décision.

`SUPERSEDES` décrit principalement une évolution historique. `REPLACES`
décrit principalement une substitution opérationnelle. Ils ne doivent pas
être utilisés comme synonymes.

## 9. Erreurs de graphe détectables

- projection orpheline : `GENERATED_FROM` absent ou source introuvable ;
- représentation sans identité : `REPRESENTED_BY` manquant ;
- autorité sans décision : `ESTABLISHED_BY` absent ou non vérifiable ;
- référence circulaire problématique : cycle dans une dépendance qui exige
  une source préalable ;
- dépendance vers un artefact supersédé sans justification ;
- distribution divergente de sa source ;
- preuve non rattachée à un finding, une décision ou une validation ;
- remplacement ambigu : absence de portée, de décision ou de continuité ;
- conflit d'autorité sur un même périmètre ;
- localisation prétendant constituer une identité ;
- révision rattachée à la mauvaise identité ;
- rupture de provenance dans une chaîne de génération ou de distribution ;
- relation de composition cyclique lorsqu'elle est interdite ;
- certification attachée à une révision différente de celle contrôlée.

L'absence d'une relation n'est jamais, à elle seule, la preuve d'une
indépendance. Elle doit être qualifiée comme absence de preuve ou comme
relation non applicable.

## 10. Exemples conceptuels

### 10.1 Une identité canonique avec plusieurs représentations

```text
I1 --REPRESENTED_BY--> R1-source
I1 --REPRESENTED_BY--> R1-distribution
R1-source --LOCATED_AT--> L-git
R1-distribution --LOCATED_AT--> L-runtime
```

Les représentations partagent l'identité `I1`. La distribution ne devient pas
une autorité concurrente.

### 10.2 Une représentation générée depuis une source canonique

```text
P1 --GENERATED_FROM--> R1-source
P1 --PROJECTS--> I1
```

Si la source change, `P1` doit être régénérée ou signalée comme divergente.

### 10.3 Une distribution consommant une représentation source

```text
D1 --DISTRIBUTED_TO--> Runtime-A
D1 --GENERATED_FROM--> R1-source
```

Le runtime consomme une représentation rattachée à `I1`; il n'établit pas un
nouveau canon.

### 10.4 Un ADR établissant une nouvelle autorité

```text
Authority-A --ESTABLISHED_BY--> Decision-A
Authority-A --GOVERNS--> I1
Authority-A --BOUNDED_BY--> Scope-A
Decision-A --SUPPORTED_BY--> Evidence-A
```

La décision rend l'autorité traçable. Le texte de l'ADR n'est pas
automatiquement une seconde autorité indépendante.

### 10.5 Une révision supersédant une ancienne

```text
Rev-2 --REVISION_OF--> Representation-1
Rev-2 --SUPERSEDES--> Rev-1
Rev-1 --LOCATED_AT--> Archive
```

`Rev-1` reste disponible pour l'historique et la provenance.

### 10.6 Une preuve soutenant une décision

```text
Finding-1 --SUPPORTED_BY--> Run-1
Decision-1 --SUPPORTED_BY--> Evidence-1
```

La preuve soutient la décision, mais n'acquiert aucune fonction normative.

### 10.7 Deux autorités concurrentes

```text
Authority-A --GOVERNS--> I1
Authority-B --GOVERNS--> I2
Authority-A --BOUNDED_BY--> Scope-X
Authority-B --BOUNDED_BY--> Scope-X
Authority-A --CONFLICTS_WITH--> Authority-B
```

Le graphe signale un conflit. Il ne choisit pas silencieusement l'autorité
la plus récente.

### 10.8 Déplacement sans changement d'identité

```text
I1 --REPRESENTED_BY--> R1
R1 --LOCATED_AT--> Old-Location
R1 --LOCATED_AT--> New-Location
```

Le changement de localisation ne crée ni `I2` ni une nouvelle autorité.

### 10.9 Scission de responsabilité

```text
I-old --PART_OF--> Responsibility-Old
I-new-a --PART_OF--> Responsibility-A
I-new-b --PART_OF--> Responsibility-B
Decision-split --SUPPORTED_BY--> Evidence-split
```

La scission crée de nouvelles identités seulement parce que les
responsabilités deviennent distinctes et sont établies comme telles.

### 10.10 État publié, local et runtime divergents

```text
Published-R --LOCATED_AT--> Published
Local-R --LOCATED_AT--> Local
Runtime-R --LOCATED_AT--> Runtime
Published-R --COMPATIBLE_WITH--> Local-R
Local-R --CONFLICTS_WITH--> Runtime-R
```

Ces nœuds doivent être comparés par leur identité, leur révision et leur
provenance, jamais par leur seule localisation.

## 11. Relations avec les autres modèles

### DIM

Le DIM fournit les identités, la continuité entre révisions et la distinction
entre représentation et localisation. Le DGM ajoute les relations entre ces
objets et les nœuds de gouvernance, de consommation et de preuve.

### Ontologie documentaire

L'ontologie qualifie les représentations, révisions, projections et autres
nœuds documentaires selon l'autorité, le cycle de vie, la temporalité, les
fonctions et la politique de chargement.

Elle ne transforme pas une relation de graphe en autorité.

### DTP

Le DTP utilise le DGM pour calculer les impacts d'une dérive ou d'une
transition : représentations dépendantes, projections à régénérer, décisions
à revalider, preuves à conserver et runtimes à comparer.

Le DGM décrit les dépendances ; le DTP organise leur qualification, la décision
humaine et les validations. Le graphe ne déclenche pas seul une migration.

### Futurs Document Tags

Les tags pourront projeter une partie du graphe : identité, relation source,
révision, autorité, périmètre, fonction, provenance et statut de projection.

Un tag ne doit jamais devenir la source unique du graphe. Il peut être absent,
obsolète, mal placé ou contredit par une décision et ses preuves. L'autorité
doit rester vérifiable par les relations et leurs sources gouvernées.

## 12. Questions ouvertes

Le DGM ne tranche pas :

- le stockage du graphe ;
- la représentation des relations dans les dépôts ;
- les relations obligatoires selon la fonction documentaire ;
- la fédération de graphes entre plusieurs dépôts ;
- le traitement détaillé des relations avec les runtimes ;
- le niveau d'automatisation de la validation ;
- le versionnement du graphe lui-même ;
- la conservation d'une relation supprimée dans chaque environnement ;
- les règles d'identité pour les agrégats multi-sources ;
- le protocole de résolution d'un conflit entre graphes faisant autorité.

Ces sujets nécessitent des décisions ultérieures et ne sont pas des éléments
de cette formalisation conceptuelle.
