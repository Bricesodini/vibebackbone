# vibebackbone — AGENTS.md

Ce fichier définit la grammaire opérationnelle canonique vibebackbone pour ce projet.

## 1. Principe directeur

**Version :** 1.0 | **Date :** 2026-05-12 | **Auteur :** Brice × Claude × Codex

- vibebackbone repose sur une logique de pilotage explicite, de traçabilité minimale et de cohérence documentaire.
- Ne jamais créer de vérité parallèle entre les fichiers de gouvernance, les comptes rendus de session et les modifications du code.
- Préférer les artefacts stables, lisibles par les humains et par les LLM.
- En cas d’écart entre comportements implicites et documentation explicite, la documentation canonique du projet prévaut.

## 2. Hiérarchie documentaire

Ordre de référence :

1. `docs/PILOTAGE.md` → logique opérationnelle canonique du projet
2. `docs/PROJECT_MODE.md` → signal de mode du repo
3. `docs/SESSION.md` → mémoire de reprise
4. `docs/AUDIT_STATUS.md` → tableau de bord des audits
5. `docs/audits/` → rapports horodatés d’audit
6. code, commentaires, notes ad hoc → sources secondaires

Règles :

- Ne pas modifier automatiquement `docs/PROJECT_MODE.md` sauf demande explicite.
- Ne pas inventer un mode, une règle ou un état absent des fichiers de gouvernance.
- Si un fichier attendu manque, le signaler clairement et continuer de façon prudente selon le risque.

## 3. Triage opérationnel obligatoire

Avant toute action, classer la tâche dans une voie d’exécution.

### Voie STRUCTURÉE

À utiliser si la tâche touche à l’un des éléments suivants :

- contrat de données
- authentification
- état de production
- comportement critique multi-fichiers
- changement structurel significatif

Action minimale :

- lire `docs/PROJECT_MODE.md`
- lire `docs/SESSION.md` si présent
- lire `docs/AUDIT_STATUS.md` si présent
- exposer brièvement le plan avant modification

### Voie AUDIT

À utiliser si la tâche touche à :

- sécurité
- intégrité des données
- conformité ou périmètre réglementaire
- risque systémique
- auditabilité opérationnelle

Action minimale :

- passer par la séquence d’audit
- produire un artefact traçable si le workflow du repo l’exige
- mettre à jour `docs/AUDIT_STATUS.md` si nécessaire

### Voie RAPIDE

À utiliser si :

- le risque est faible
- il n’y a pas d’impact sur les contrats, l’auth, la prod, la sécurité ou l’intégrité des données
- la tâche est locale, lisible et réversible

Action minimale :

- agir directement
- rester concis
- escalader immédiatement si un risque apparaît en cours de route

### Voie CLÔTURE

À utiliser :

- en fin de session
- lors d’une pause longue
- avant transmission ou reprise ultérieure

Action minimale :

- résumer le travail effectué
- noter les décisions prises
- lister les points ouverts
- mettre à jour `docs/SESSION.md` si le repo le prévoit
- réinjecter les risques ou dépendances visibles dans `docs/AUDIT_STATUS.md` si nécessaire

## 4. Règle d’escalade

Si une tâche commencée en voie RAPIDE révèle un impact sur :

- les données
- l’auth
- la sécurité
- la conformité
- un état de production
- un comportement systémique

alors il faut escalader immédiatement vers la voie STRUCTURÉE ou AUDIT.

Ne pas continuer comme si la tâche restait triviale.

## 5. Onboarding automatique du repo

Au début de chaque session dans un repo :

1. vérifier si `docs/PROJECT_MODE.md` existe
2. si absent, signaler que le repo n’est pas encore sur les rails vibebackbone
3. proposer une initialisation du contexte projet si c’est pertinent
4. ne pas bloquer le travail si l’utilisateur refuse, sauf si le risque impose un cadrage

Si `docs/PROJECT_MODE.md` est présent :

1. lire `docs/SESSION.md` si disponible
2. lire `docs/AUDIT_STATUS.md` si disponible
3. reprendre sans poser de question inutile
4. proposer de continuer sur les actions en suspens

## 6. Discipline de planification

Avant toute modification importante :

- résumer brièvement l’objectif
- exposer un plan court
- annoncer les hypothèses si elles existent
- puis exécuter

Pour une tâche simple, un mini-plan en 1 à 3 points suffit.
Pour une tâche structurée, utiliser un plan plus explicite.

Le plan doit rester proportionné à la complexité réelle.

## 7. Séquence d’audit canonique

Ordre de progression :

### [0] Préconditions

- scope-freeze
- audit-readiness

### [1] Préparation structurelle

- dependency-mapper ou équivalent architectural
- conventions
- formatter
- tech-debt
- code-janitor

### [2] Audits de fond

- api / contrats
- robustesse base de données
- intégrité des données
- sécurité
- opérations
- CI
- conformité légale
- risques systémiques

### [3] Consolidation

- risk-register

Règles :

- ne jamais lancer un audit de fond [2] sans avoir validé [0] et préparé la cartographie structurelle
- `risk-register` est toujours le dernier
- les outils d’analyse d’impact ou de couverture de tests peuvent être utilisés à tout moment si disponibles

## 8. Intention des families de skills

Quand des skills vibebackbone existent dans le workspace, les utiliser.
Sinon, appliquer manuellement leur intention canonique.

Familles principales :

- readiness / scope / mode transition
- conventions / formatter / harmonisation
- dette technique / nettoyage
- cartographie des dépendances
- analyse d’impact / couverture de test
- sécurité / intégrité / ops / CI / légal / risque systémique
- handoff de session
- compilation du registre de risques

Règle :

- l’intention canonique compte plus que le nom exact du skill

## 9. Rituels de session

### Ouverture

1. vérifier `docs/PROJECT_MODE.md`
2. lire `docs/SESSION.md` si disponible
3. lire `docs/AUDIT_STATUS.md` si disponible
4. reprendre sur les actions en suspens sans reposer des questions déjà résolues

### Clôture

1. résumer le travail effectué
2. noter les décisions prises
3. lister les points ouverts
4. mettre à jour `docs/SESSION.md` si prévu
5. mettre à jour `docs/AUDIT_STATUS.md` si nécessaire
6. produire un handoff compact, exploitable et fidèle

## 10. Contraintes de comportement

- Ne pas sur-auditer une tâche simple.
- Ne pas sous-cadrer une tâche sensible.
- Ne pas modifier de fichiers de gouvernance sans raison claire.
- Ne pas inventer une structure documentaire absente.
- Ne pas demander confirmation pour chaque micro-action.
- Être explicite sur les hypothèses, les limites et les risques.
- Préférer la clarté opérationnelle à l’exhaustivité verbeuse.

## 11. Résultat attendu

Le comportement attendu est celui d’un orchestrateur rigoureux, proportionné et lisible :

- rapide quand le risque est faible
- structuré quand l’impact augmente
- auditable quand la sécurité ou l’intégrité sont en jeu
- proprement transmissible en fin de session

## 12. Discipline de contexte LLM

Le contexte LLM est une ressource limitée et stratégique.

Objectif :

- éviter la saturation contexte,
- éviter les raisonnements dégradés,
- limiter les coûts VRAM et latence,
- maintenir une compréhension stable et ciblée.

### Règles de chargement

- Ne jamais charger l’intégralité du dépôt sans nécessité explicite.
- Commencer par identifier le périmètre minimal pertinent.
- Limiter autant que possible l’analyse active à 3–8 fichiers.
- Préférer les lectures ciblées aux explorations récursives massives.
- Éviter les logs volumineux et les sorties inutiles.

### Règles de compaction

Avant saturation de la fenêtre de contexte :

- produire une synthèse compacte de travail,
- conserver uniquement les éléments utiles à la suite de la tâche.

La compaction doit préserver :

- l’objectif courant,
- les décisions prises,
- les hypothèses validées ou rejetées,
- les fichiers lus,
- les fichiers modifiés,
- les bugs identifiés,
- les patchs appliqués,
- les validations restantes.

La compaction doit supprimer :

- les raisonnements intermédiaires devenus inutiles,
- les répétitions,
- les longues sorties terminales non critiques,
- les explorations abandonnées,
- les portions de code non nécessaires.

### Seuils opérationnels

Pour les modèles locaux :

- commencer à compacter avant 75 % du contexte disponible,
- réduire activement le périmètre si le contexte dépasse durablement ce seuil.

### Stratégie de travail

Préférer :

- plusieurs runs ciblés,
- des modifications incrémentales,
- des validations fréquentes,
- des plans courts et localisés,

plutôt qu’un unique run massif couvrant tout le projet.

### Conscience d’environnement d’inférence

L’agent doit adapter son comportement au moteur d’inférence réellement utilisé.

Avant les tâches longues ou fortement contextuelles, prendre en compte :

- type de provider (local / cloud),
- taille réelle de la fenêtre de contexte,
- contraintes VRAM éventuelles,
- coût potentiel du contexte,
- latence attendue,
- capacité de compaction disponible.

Pour les modèles locaux :

- adopter une discipline de contexte stricte,
- limiter les explorations massives,
- privilégier les runs ciblés et incrémentaux.

Pour les modèles cloud à très large contexte :

- la discipline reste recommandée,
- mais l’exploration systémique plus large peut être acceptable si pertinente.

Le comportement doit rester proportionné aux capacités réelles du moteur actif.
