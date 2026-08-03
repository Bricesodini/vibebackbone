# Document Identity Model (DIM)

## Statut du document

Ce document est un modèle conceptuel de travail. Il ne modifie aucune
autorité documentaire, ne classe aucun artefact existant et ne définit aucun
format technique.

Verdict : `DOCUMENT_IDENTITY_MODEL_READY`

## 1. Définition de l'identité documentaire

Une identité documentaire est le référent abstrait et stable d'une
responsabilité documentaire gouvernée.

Elle répond à la question :

> Quel artefact conceptuel porte cette responsabilité, indépendamment de la
> manière dont il est stocké, nommé, rendu ou publié ?

Une identité est définie par la continuité de la responsabilité, du périmètre
et du sens gouverné. Elle ne dépend pas d'un fichier particulier.

L'identité possède une continuité propre, mais ses représentations, ses
révisions et ses localisations peuvent changer.

## 2. Distinctions fondamentales

### Identité

Le référent conceptuel stable d'une responsabilité documentaire.

### Représentation

Une expression concrète de l'identité : document Markdown, sortie générée,
copie de distribution, page publiée ou autre support.

Plusieurs représentations peuvent correspondre à une même identité.

### Révision

Un état successif d'une représentation ou du contenu gouverné par une
identité. Une révision peut modifier le contenu, les métadonnées, la portée ou
la relation avec d'autres artefacts, sans créer nécessairement une nouvelle
identité.

### Localisation

L'endroit où une représentation est stockée, exposée ou déployée : chemin,
branche, dépôt, distribution, environnement ou adresse publiée.

Une localisation est une propriété opérationnelle, pas une propriété
d'identité.

Relations simplifiées :

```text
Identité documentaire
  ├── possède plusieurs représentations
  ├── possède une suite de révisions
  └── chaque représentation peut avoir plusieurs localisations
```

## 3. Pourquoi les identifiants physiques ne suffisent pas

Un chemin Git n'est pas une identité : un artefact peut être déplacé,
dupliqué, publié dans une distribution ou généré à un autre emplacement sans
que sa responsabilité change.

Un nom de fichier n'est pas une identité : plusieurs fichiers peuvent porter
le même nom pour des responsabilités différentes, et une même responsabilité
peut changer de nom.

Une version n'est pas une identité : une version décrit un état ou un contrat
à un moment donné. Elle peut évoluer au sein de la même identité et plusieurs
identités peuvent utiliser des séquences de version différentes.

Une représentation générée ne crée jamais une nouvelle identité par le seul
fait qu'elle est générée. Elle reste une projection ou une distribution de
l'identité source, sauf décision explicite établissant une responsabilité
distincte.

## 4. Identité et autorité

L'autorité n'est pas synonyme d'identité.

Une identité peut porter une autorité canonique ou limitée à un périmètre,
mais cette autorité résulte d'une relation gouvernée et vérifiable. Elle ne
résulte ni du nom, ni de la localisation, ni du nombre de copies.

Une révision peut modifier l'autorité applicable, mais uniquement par une
procédure de gouvernance appropriée. Une représentation non autoritative ne
devient pas autoritative parce qu'elle est plus récente, plus complète ou
générée automatiquement.

Une autorité peut également être partagée entre plusieurs identités lorsque
leurs responsabilités sont explicitement disjointes. Deux identités ne doivent
pas prescrire la même responsabilité sans arbitrage explicite.

## 5. Identité et ontologie documentaire

L'ontologie décrit l'état gouverné d'une représentation ou d'une révision dans
un contexte donné :

```text
(
  authority,
  lifecycle,
  temporality,
  primary_function,
  secondary_functions,
  load_policy
)
```

Elle ne remplace pas l'identité.

La même identité peut donc avoir des représentations différentes avec des
politiques de chargement différentes, tout en conservant la même responsabilité
source. Les valeurs doivent toutefois rester cohérentes avec le périmètre de
l'identité et avec la relation source/projection.

Une identité conserve sa continuité lorsque le contenu évolue de manière
gouvernée. Une nouvelle identité est nécessaire lorsque la responsabilité, le
périmètre ou le sens deviennent substantiellement différents.

## 6. Révisions et continuité

Plusieurs révisions appartiennent à une même identité lorsque :

- elles répondent à la même responsabilité ;
- leur périmètre reste compatible ;
- la continuité de gouvernance est traçable ;
- aucune décision n'établit une nouvelle responsabilité.

Une révision ne devient pas une nouvelle identité lorsqu'elle est corrigée,
traduite, reformattée, déplacée, générée ou publiée dans un autre
environnement.

Une nouvelle identité doit être envisagée lorsque :

- la responsabilité est séparée en responsabilités distinctes ;
- le périmètre devient incompatible ;
- le document cesse d'être une représentation de l'autorité source et devient
  une autorité indépendante ;
- une décision de gouvernance établit explicitement une nouvelle identité.

En cas de doute, la continuité ne doit pas être inventée : le cas reste à
arbitrer.

## 7. Référentiel d'invariants

- Une identité est indépendante de ses chemins, noms, versions et supports.
- Une identité possède au moins une représentation gouvernée lorsqu'elle est
  publiée ou utilisée.
- Une représentation générée reste rattachée à son identité source.
- Une localisation ne peut pas, à elle seule, créer une identité.
- Une révision ne peut pas, à elle seule, créer une identité.
- Une fonction secondaire ne crée ni identité ni autorité.
- Une identité ne peut pas avoir deux autorités concurrentes sur le même
  périmètre sans décision documentée.
- Toute rupture de continuité doit être prouvée ou explicitement arbitrée.
- La suppression d'une représentation ne supprime pas automatiquement
  l'identité ni son historique.
- Une identité historique reste distinguable d'une identité active.

## 8. Relation avec le Document Transition Protocol

Le DIM fournit au DTP le référent stable à suivre pendant une transition.

Le DTP utilise l'identité pour :

- comparer des représentations situées à des emplacements différents ;
- détecter les copies concurrentes et les projections divergentes ;
- rattacher les révisions à une continuité ;
- préserver l'historique lors d'un déplacement ou d'un archivage ;
- distinguer changement de représentation et changement de responsabilité.

Le DTP ne peut pas modifier l'identité silencieusement. Une rupture
d'identité est une décision de gouvernance, distincte d'une migration
physique.

## 9. Relation avec les futurs Document Tags

Les futurs tags documentaires pourront rendre observable le contrat d'une
identité et de chacune de ses représentations.

Ils devront distinguer au minimum :

- le référent d'identité ;
- la représentation concernée ;
- la révision applicable ;
- la localisation ;
- les dimensions ontologiques ;
- la relation source, projection ou distribution.

Un tag ne doit pas devenir l'unique source d'autorité. Il décrit et rend
vérifiable une relation déjà gouvernée ; il ne la crée pas.

Le mécanisme futur devra aussi permettre de détecter :

- une représentation sans identité connue ;
- plusieurs identités pour une même responsabilité ;
- une projection sans source ;
- une révision rattachée à la mauvaise identité ;
- une localisation qui prétend être l'autorité sans preuve.

## 10. Résumé conceptuel

```text
Identité = responsabilité documentaire stable
Représentation = expression concrète de cette identité
Révision = état successif d'une représentation ou de son contenu
Localisation = emplacement d'une représentation
Ontologie = état gouverné observé pour une représentation/révision
Autorité = relation gouvernée, non propriété du chemin ou du nom
```

Le modèle permet ainsi de déplacer, générer, publier, réviser ou archiver des
représentations sans perdre la continuité conceptuelle de leur identité.
