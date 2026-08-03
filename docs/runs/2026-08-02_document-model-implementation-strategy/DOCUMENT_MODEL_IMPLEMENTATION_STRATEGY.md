# Document Model Implementation Strategy

## Statut et périmètre

Ce document prépare de futurs runs d'implémentation. Il ne modifie aucun
artefact du dépôt et ne choisit aucune stratégie de publication.

Les seules fondations utilisées sont DIM, l'ontologie documentaire, DGM, DTP,
DTS et le plan d'intégration documentaire. Aucun nouveau modèle, protocole ou
axe ontologique n'est introduit.

## 1. Principes d'implémentation

- construire par petits chantiers indépendants ;
- rendre chaque chantier observable et testable ;
- maintenir une capacité de rollback à chaque étape ;
- séparer détection, validation, décision humaine et remédiation ;
- ne jamais rendre un artefact conforme par inférence silencieuse ;
- ne publier une capacité qu'après validation adaptée à son niveau de risque ;
- conserver les preuves de chaque run sans les confondre avec le canon.

## 2. Chantiers indépendants

| ID | Chantier | Dépendances principales | Peut être reporté |
|---|---|---|---|
| C0 | Contrat d'intégration et interfaces de validation | Fondations conceptuelles validées | Non : prérequis de coordination |
| C1 | Validation DIM | C0 | Non si les autres validateurs sont développés |
| C2 | Validation de l'ontologie | C0 | Non pour une qualification complète |
| C3 | Validation DTS | C0, C1, C2 | Oui, si les tags restent expérimentaux |
| C4 | Validation DGM | C0, C1, C2 | Oui pour un premier pilote sans graphe complet |
| C5 | Adaptation DTP | C1, C2, C3, C4 | Non avant toute transition gouvernée |
| C6 | Adaptation des outils | C1-C5 selon l'outil | Oui par outil et par capacité |
| C7 | Adaptation des skills | Interfaces C1-C5 | Oui par skill |
| C8 | Templates et artefacts de run | C5, décisions de gouvernance existantes | Oui après le pilote |
| C9 | Distributions | C3, C5, C6, C7 | Oui jusqu'à stabilisation du noyau |
| C10 | Workflows et publication | C5-C9 | Oui jusqu'à validation humaine |

Les chantiers sont séparables : un échec d'un chantier ne doit pas invalider
les preuves des autres ni déclencher une migration globale.

## 3. Graphe de dépendances

```text
C0 Interfaces
    ├──> C1 Validation DIM ──────┐
    ├──> C2 Validation Ontologie ├──> C3 Validation DTS ──┐
    └──> C6 Outils ciblés        └──> C4 Validation DGM ──┤
                                                         v
                                                   C5 Adaptation DTP
                                                        ├──> C7 Skills
                                                        ├──> C8 Templates
                                                        └──> C9 Distributions
                                                              |
                                                              v
                                                        C10 Publication
```

### Développement parallèle

- C1 et C2 peuvent commencer en parallèle après C0.
- C4 peut préparer ses contrôles structurels en parallèle de C3, mais son
  verdict complet dépend de l'identité et de l'ontologie.
- C6 peut adapter les outils de lecture et de mesure avant les capacités de
  génération.
- C7 peut préparer les contrats d'appel des skills avant leur activation.
- C8 peut préparer des fixtures de test sans modifier les templates courants.

### Dépendances obligatoires

- C3 ne peut pas conclure sur la compatibilité sans C1 et C2.
- C5 ne peut pas ouvrir une transition sans findings issus de C1-C4.
- C9 ne doit pas propager une capacité non validée vers les distributions.
- C10 ne doit pas déclarer une capacité canonique sans validation humaine.

## 4. MVP par chantier

### C0 — Contrat d'intégration et interfaces

**MVP :** définir les entrées, sorties, verdicts et preuves attendus de chaque
validation à partir de DTS et de la gouvernance existante.

**Valeur :** évite les implémentations incompatibles entre validateurs.

**Réussite :** chaque chantier sait produire un résultat, un finding ou un
statut d'incertitude sans modifier le dépôt.

**Arrêt :** champs ou verdicts impossibles à interpréter sans inventer une
nouvelle règle.

### C1 — Validation DIM

**MVP :** vérifier l'identité, la représentation, la révision et la
localisation sur un noyau réduit.

**Valeur :** rend la continuité documentaire observable indépendamment des
chemins Git.

**Réussite :** les représentations, déplacements et révisions sont distingués.

**Arrêt :** identité ambiguë, rupture non arbitrée ou représentation orpheline.

### C2 — Validation de l'ontologie

**MVP :** vérifier les cinq dimensions, `MULTI_PERIOD`, la fonction principale
et les fonctions secondaires.

**Valeur :** empêche les confusions entre autorité, temporalité et fonction.

**Réussite :** chaque tuple testé est interprétable sans contradiction.

**Arrêt :** valeur inconnue sur une dimension obligatoire ou autorité non
bornée lorsque le périmètre est nécessaire.

### C3 — Validation DTS

**MVP :** comparer un tag d'artefact et un contrat de dépôt sur les quatre
résultats `COMPATIBLE`, `MIGRATION_REQUIRED`, `INCOMPATIBLE`, `UNKNOWN`.

**Valeur :** rend les écarts de contrat mesurables sans migration automatique.

**Réussite :** les cas sans tag, contrat absent, tag ancien, dimension inconnue
et source absente sont distingués.

**Arrêt :** compatibilité impossible à conclure ou héritage non traçable.

### C4 — Validation DGM

**MVP :** contrôler les liens de source, représentation, génération,
distribution, supersession et conflit sur un petit graphe.

**Valeur :** détecte les projections orphelines et ruptures de provenance.

**Réussite :** les relations critiques sont vérifiées sans créer d'autorité.

**Arrêt :** graphe cyclique non qualifié, source absente ou conflit de
responsabilité non arbitré.

### C5 — Adaptation DTP

**MVP :** transformer les résultats des validateurs en findings autonomes et
appliquer le routage `OUI`, `NON`, `PLUS TARD`.

**Valeur :** sépare détection, décision humaine et remédiation.

**Réussite :** aucune action corrective n'est engagée avant décision explicite.

**Arrêt :** procédure de remédiation déduite avant la réponse humaine ou
absence de preuve de réversibilité.

### C6 — Adaptation des outils

**MVP :** ajouter, outil par outil, la lecture ou la validation des contrats et
relations nécessaires, sans génération destructive.

**Valeur :** fournit des mesures reproductibles et bornées.

**Réussite :** sorties déterministes, findings traçables, aucune écriture
implicite.

**Arrêt :** outil incapable de distinguer source et projection ou modifiant un
artefact sans autorisation dédiée.

### C7 — Adaptation des skills

**MVP :** faire consommer aux skills les résultats des validateurs et router
les décisions vers DTP.

**Valeur :** rend le comportement cohérent entre skills sans créer de logique
documentaire parallèle.

**Réussite :** les skills exposent les inconnues et n'inventent ni identité ni
autorité.

**Arrêt :** skill contournant Critical Rule 16, le DTP ou la source canonique.

### C8 — Templates et artefacts de run

**MVP :** préparer les emplacements documentaires nécessaires aux findings,
décisions, validations et preuves des runs.

**Valeur :** rend les résultats rejouables et auditables.

**Réussite :** chaque sortie identifie son contexte, ses entrées et son statut.

**Arrêt :** template qui transforme une preuve en autorité ou impose un
processus non adopté.

### C9 — Distributions

**MVP :** exposer la capacité de lecture du contrat et des projections dans une
distribution pilote, sans la rendre obligatoire.

**Valeur :** vérifie la cohérence entre noyau et runtime.

**Réussite :** le runtime identifie sa source, sa révision et son état de
compatibilité.

**Arrêt :** divergence non observable ou comportement différent du noyau.

### C10 — Workflows et publication

**MVP :** documenter les points de contrôle et les options de publication,
sans activer une publication canonique.

**Valeur :** prépare une adoption maîtrisée.

**Réussite :** une publication peut être distinguée d'une expérimentation et
reste réversible.

**Arrêt :** publication sans validation humaine, commit déterminé ou preuve
associée.

## 5. Validations par chantier

Chaque chantier réutilise les contrôles existants et les niveaux de revue
applicables. Aucun nouveau protocole de validation n'est créé.

| Chantier | Unitaires | Système | Adversarial | Humain |
|---|---|---|---|---|
| C1 DIM | cas d'identité, révision, localisation | cohérence identité-représentation | identité fabriquée depuis un chemin | arbitrage des ruptures |
| C2 Ontologie | tuples valides/invalides | cohérence avec autorités et chargement | fonction secondaire utilisée comme autorité | validation des périmètres |
| C3 DTS | quatre verdicts de compatibilité | comparaison dépôt/artefacts | version récente réinterprétant l'historique | choix du contrat cible |
| C4 DGM | relations et cardinalités | graphe source/projection/distribution | projection orpheline ou autorité concurrente | arbitrage des conflits |
| C5 DTP | routage des réponses humaines | run complet finding-décision | tentative de correction silencieuse | décision `OUI/NON/PLUS TARD` |
| C6 Outils | sorties et erreurs | cohérence inter-outils | outil déclarant une projection comme canon | approbation de chaque capacité d'écriture |
| C7 Skills | contrats d'entrée/sortie | routage entre skills | contournement de Critical Rule 16 | validation du comportement agent |
| C8 Templates | structure et traçabilité | réutilisation dans un run | preuve présentée comme certification | validation des templates |
| C9 Distributions | lecture du contrat | noyau versus runtime | distribution divergente | décision de niveau de publication |
| C10 Workflows | contrôles de publication | état publié/reproductible | publication prématurée | autorisation de publication |

## 6. Risques et rollback

| Chantier | Risques principaux | Rollback minimal |
|---|---|---|
| C0 | interfaces ambiguës, divergence de vocabulaire | abandon des interfaces de travail |
| C1 | fausse continuité ou multiplication d'identités | retirer le verdict et conserver le finding |
| C2 | autorité déduite d'une fonction ou date | invalider la qualification concernée |
| C3 | compatibilité trop permissive ou rétroactive | revenir au résultat `UNKNOWN` et bloquer la migration |
| C4 | provenance incomplète, graphes divergents | retirer la projection calculée, conserver la source |
| C5 | remédiation engagée trop tôt | arrêter le run avant toute écriture et préserver les décisions |
| C6 | écriture implicite, sorties non déterministes | désactiver la capacité d'écriture et revenir au mode lecture |
| C7 | skill contournant le routage humain | retirer l'adaptation du catalogue actif |
| C8 | template introduisant une gouvernance implicite | retirer le template non publié |
| C9 | divergence entre distribution et noyau | désactiver la capacité dans la distribution pilote |
| C10 | publication confondue avec release logicielle | annuler la publication candidate sans réinterpréter l'historique |

Les rollbacks restaurent l'état fonctionnel précédent ; ils ne suppriment pas
les preuves du run ni les décisions déjà prises.

## 7. Options de publication

La stratégie finale reste à choisir après les MVP.

### Expérimental

Capacité limitée à un pilote, à des fixtures et à des utilisateurs désignés.
Elle produit des findings mais ne modifie pas le comportement courant.

### Disponible mais non obligatoire

Capacité installable et utilisable, sans blocage par défaut. Les résultats sont
visibles et les écarts sont routés vers DTP.

### Recommandé

Capacité intégrée aux parcours courants, avec avertissement ou contrôle selon
le risque, mais sans prétendre encore être l'unique autorité.

### Canonique

Capacité intégrée à la gouvernance publiée, avec validation humaine, tests de
régression, propagation aux distributions et état de publication déterminé.

Ces niveaux sont des options d'adoption, pas des décisions prises par la
présente stratégie.

## 8. Conditions de passage entre étapes

Un passage exige :

- les validations prévues exécutées ou explicitement déclarées bloquées ;
- les findings connus et non masqués ;
- les preuves conservées ;
- les risques résiduels acceptés au niveau approprié ;
- une décision humaine lorsqu'une autorité, un contrat ou une publication est
  concerné.

Un échec arrête le chantier concerné sans bloquer artificiellement les
chantiers indépendants.

## 9. Résultat attendu

Cette stratégie permet de transformer progressivement le modèle documentaire
en capacité native de Vibe Backbone, tout en gardant chaque étape :

- indépendante ;
- testable ;
- réversible ;
- traçable ;
- gouvernée par les règles existantes.

La stratégie s'arrête avant toute implémentation.
