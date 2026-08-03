# Document Model Integration Plan

## Statut

Ce document décrit une architecture d'intégration progressive. Il ne modifie
aucun artefact, ne classe pas le dépôt et ne propose ni migration ni
implémentation.

Fondations utilisées exclusivement : DIM, ontologie documentaire, DGM, DTP et
DTS.

## 1. Couche documentaire

### Documents susceptibles d'évoluer

Les impacts conceptuels concernent les responsabilités suivantes :

- `AGENTS.md` : rappeler le contrat de décision humaine, l'identité des
  artefacts gouvernés et l'interdiction de correction silencieuse ;
- `SYSTEM.md` : préciser la posture d'observation du contrat documentaire au
  démarrage et la distinction entre source, projection et runtime ;
- `docs/CONTEXT.md` : porter l'ancrage documentaire du dépôt et son contrat
  déclaré ;
- `docs/PILOTAGE.md` : router les findings de compatibilité vers le DTP ;
- `docs/DOCUMENT_CONVENTION.md` : relier la convention documentaire à
  l'identité, à la représentation et aux métadonnées observables ;
- `docs/ARCHITECTURE.md` : devenir la source des relations structurées entre
  responsabilités, sources et projections ;
- `docs/DISTRIBUTIONS.md` : expliciter les relations DGM entre source,
  projection, distribution et runtime ;
- `docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md` : préserver l'identité et la
  provenance des connaissances promues ou supersédées ;
- `PROMPTS_ARCHITECTURE.md` : distinguer identité d'un prompt, représentation
  distribuée et relation de consommation.

Il s'agit d'impacts de responsabilité, pas d'une instruction de réécriture.

### Documents à annoter seulement

Les catégories suivantes pourront recevoir les métadonnées ou relations
minimales nécessaires, sans réécrire leur contenu :

- ADR et décisions établissant une autorité ;
- documents canoniques spécialisés ;
- projections distribuées ;
- rapports actifs dont la provenance doit être observable ;
- artefacts de run qui soutiennent une décision.

Une annotation ne transforme jamais un document en autorité.

### Documents restant inchangés

Les preuves historiques, rapports de runs, audits clôturés et documents
conservés comme traces restent inchangés tant qu'aucune décision humaine ne
demande leur traitement. Leur fonction historique n'est pas modifiée par le
nouveau modèle.

Les guides explicatifs et journaux peuvent également rester inchangés lorsque
leur rôle n'exige ni prescription, ni projection, ni déclaration de contrat.

### Documents devenant des projections

Les artefacts explicitement dérivés d'une source doivent être traités comme
projections dans le modèle :

- relations générées de l'architecture ;
- copies de distributions ;
- dashboards et index dérivés ;
- sorties de génération de prompts ;
- vues documentaires calculées.

Une projection doit rester reliée à sa source et ne doit pas devenir une
seconde vérité.

## 2. Couche Skills

Les décisions ci-dessous concernent la responsabilité des skills, pas leur
implémentation immédiate.

| Skill | Décision | Justification d'intégration |
|---|---|---|
| `1-vbb-doc-harmonizer` | ADAPT | Remplacer la classification isolée par une lecture DIM/ontologie/DGM ; préserver les preuves et router les écarts vers le DTP. Il reste non destructif. |
| `1-vbb-code-doc-coherence-auditor` | ADAPT | Comparer les identités et représentations documentaires aux surfaces de code ; distinguer absence, dérive, projection et autorité concurrente. |
| `1-vbb-code-doc-gap-integrator` | ADAPT | Un gap peut produire une représentation proposée, mais ne peut ni créer une identité canonique ni déduire une autorité. Toute écriture reste autorisée séparément. |
| `t-vbb-project-context-init` | ADAPT | Initialiser ou vérifier l'ancrage du contrat documentaire, sans déclarer conformes les fichiers existants ni écraser une autorité. |
| `t-vbb-dependency-mapper` | ADAPT | Utiliser les relations DGM et maintenir `ARCHITECTURE.md` comme source et `RELATIONS.md` comme projection. |
| `t-vbb-index` | ADAPT | Indexer les identités, sources et versions comme informations de recherche, sans interpréter l'index comme autorité. |
| `t-vbb-impact-analyzer` | ADAPT | Calculer les impacts à partir des dépendances DGM, puis produire les entrées nécessaires au DTP avant toute transition. |
| `t-vbb-status-dashboard` | ADAPT | Exposer le contrat du dépôt, les compatibilités, les findings et les inconnues en lecture seule. |
| `t-vbb-session-handoff` | ADAPT | Transmettre l'ancre, les identités concernées, les décisions humaines et les findings ouverts sans transformer la mémoire locale en canon. |

Aucune skill analysée ne nécessite actuellement `SPLIT`, `MERGE`, `RETIRE` ou
`NEW`. Les responsabilités existantes peuvent porter l'intégration par
adaptation ciblée.

## 3. Couche Outils

| Outil | Rôle d'intégration conceptuel | Niveau autorisé |
|---|---|---|
| `tools/vbb-document-convention-lint.py` | Vérifier la cohérence des conventions et des champs observables | Lecture + validation |
| `tools/vbb-architecture.py` | Lire les relations, valider la source d'architecture et produire la projection des relations | Lecture + validation + génération de projection |
| `tools/vbb-index.py` | Rechercher identités, versions, sources et findings | Lecture uniquement ; construction d'index éventuellement dérivée, sans autorité |
| `tools/vbb-status-dashboard.py` | Mesurer l'état du contrat, les versions et les findings | Lecture + validation |
| `tools/vbb-context-compactor.py` | Préserver l'ancre, la provenance et les décisions dans un contexte compact | Lecture uniquement |
| `tools/vbb-gate-check.py` | Contrôler que les décisions et validations requises existent avant une transition | Lecture + validation |

Aucun outil existant n'est désigné pour modifier ou migrer des tags. La
présente intégration ne crée pas de nouvel outil et n'autorise aucune
migration automatique.

## 4. Couche Validation

### Validation DIM

Contrôles :

- identité stable et indépendante du chemin ;
- représentation rattachée à une identité ;
- révision rattachée à la bonne représentation ;
- localisation distincte de l'identité ;
- continuité ou rupture d'identité explicitement justifiée.

Findings typiques : représentation orpheline, révision mal rattachée,
identité dupliquée, localisation présentée comme identité.

### Validation de l'ontologie

Contrôles :

- autorité et périmètre cohérents ;
- cycle de vie et temporalité compatibles ;
- `MULTI_PERIOD` explicite lorsque nécessaire ;
- une seule fonction principale ;
- fonctions secondaires sans création d'autorité ;
- politique de chargement cohérente avec la responsabilité.

Findings typiques : autorité inconnue, fonction contradictoire, temporalité
perdue, politique de chargement non justifiée.

### Validation DGM

Contrôles :

- sources présentes pour les projections ;
- relations de provenance complètes ;
- absence de conflit d'autorité non arbitré ;
- absence de dépendance silencieuse vers un artefact supersédé ;
- cohérence des relations de distribution, référence et implémentation.

Findings typiques : projection orpheline, rupture de provenance, relation
circulaire problématique, conflit d'autorité, distribution divergente.

### Validation DTP

Contrôles :

- ancre documentaire identifiée ;
- chaque finding indépendant d'une décision ;
- décision humaine `OUI`, `NON` ou `PLUS TARD` enregistrée ;
- procédure déterminée seulement après `OUI` ;
- conditions d'arrêt et réversibilité explicites ;
- aucune correction silencieuse.

Findings typiques : remédiation commencée sans décision, changement de canon
non routé, dette différée non enregistrée, migration sans preuve de retour.

### Validation DTS

Contrôles :

- niveau de tag identifiable ;
- version de contrat présente ou explicitement inconnue ;
- champs obligatoires interprétables ;
- héritage traçable ;
- source déclarée pour toute projection ou distribution ;
- compatibilité calculable sans interprétation rétroactive ;
- tag Git relié à un commit et séparé du contrat.

Findings typiques : artefact non tagué dans un dépôt versionné, dimension
inconnue, contrat absent, projection sans source, tag Git confondu avec une
version logicielle, état runtime non comparable.

## 5. Roadmap incrémentale avant implémentation

### Étape 1 — Enveloppe d'intégration

Produire une matrice des impacts sur documents, skills et outils, avec une
ancre et un périmètre explicitement bornés.

Valeur : rend les responsabilités visibles immédiatement.
Réversibilité : aucune modification d'état.

### Étape 2 — Pilote conceptuel borné

Sélectionner un petit noyau représentatif et décrire ses tags, relations et
résultats de compatibilité sans les appliquer au dépôt.

Valeur : fournit un oracle de validation concret.
Réversibilité : le pilote reste un artefact d'analyse.

### Étape 3 — Jeu de findings et décisions

Préparer des cas positifs et négatifs : artefact non tagué, projection
orpheline, conflit d'autorité, runtime divergent, artefact historique.

Valeur : vérifie que DTS, DGM et DTP produisent des décisions humaines
distinctes plutôt que des corrections automatiques.
Réversibilité : aucun artefact courant n'est modifié.

### Étape 4 — Revue d'autorisation

Soumettre le plan, le pilote et les findings à validation humaine. Décider
ensuite séparément si une implémentation limitée peut commencer.

Valeur : empêche qu'un modèle validé conceptuellement soit traité comme une
autorisation de migration.
Réversibilité : arrêt complet possible avant toute écriture.

La roadmap s'arrête ici. Elle ne comprend ni implémentation des tags, ni
annotation du dépôt, ni migration, ni nettoyage documentaire.

## 6. Invariants d'intégration

- Les cinq modèles restent les seules fondations conceptuelles.
- Le tag projette un état ; il ne crée jamais une autorité.
- `ARCHITECTURE.md` reste la source structurée lorsque la responsabilité
  architecture est concernée ; les relations générées restent des projections.
- Les preuves historiques ne deviennent pas des certificats de l'état courant.
- Aucun finding ne vaut décision humaine.
- Aucune skill ne peut contourner le DTP ou Critical Rule 16.
- Toute relation modifiée doit rester traçable dans le DGM.
- Toute validation non exécutée reste non vérifiée.
- Une intégration partielle doit être explicitement distinguée d'un dépôt
  globalement conforme.

## 7. Décisions humaines restantes

- autoriser ou non le pilote concret sur un noyau limité ;
- fixer la première version de contrat documentaire applicable au dépôt ;
- choisir les premières représentations à observer ;
- déterminer quelles sorties générées doivent être validées comme projections ;
- approuver les adaptations futures des skills et outils ;
- définir le seuil à partir duquel une divergence bloque une transition.

Ces décisions sont préalables à toute implémentation et ne sont pas prises par
ce plan.
