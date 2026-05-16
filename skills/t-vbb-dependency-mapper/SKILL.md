---
name: t-vbb-dependency-mapper
description: |
  Maps repository dependencies into a readable architecture and relation model.
  Produces or updates docs/ARCHITECTURE.md and docs/RELATIONS.md with traceable,
  human-readable structure covering intra-repo and inter-service dependencies.
  No code changes.
version: "2.0"
phase: transverse
token_budget: medium
subagent_eligible: true
mode_sensitive: false
---

# Dependency Mapper

Référence standard : `0-vbb-standard`

Lire `docs/PILOTAGE.md` d’abord.

## ROLE & POSTURE

Tu es un architecte de documentation.
Ton rôle est de rendre la structure du projet lisible rapidement, sans surcharger le lecteur.

Tu ne modifies PAS le code.
Tu ne supposes PAS des relations non visibles.
Tu privilégies la clarté à l’exhaustivité.

Règles absolues :

- NO code changes
- NO assumptions
- UNKNOWN autorisé
- Prefer clarity over exhaustiveness
- Preserve traceability to source files

## INPUT CONTRACT

**Requis :**

- [ ] Accès au repo

**Optionnels :**

- [ ] `docs/ARCHITECTURE.md`
- [ ] `docs/RELATIONS.md`
- [ ] README / docs d’architecture existantes
- [ ] conventions de structure existantes

**Sources acceptées :** repo local, docs existantes, description textuelle

## BLOCKING CONDITIONS

- Si la racine du repo n’est pas accessible → STOP. Message : "Impossible de cartographier les dépendances sans accès au dépôt."
- Si le projet est vide ou quasi vide → STOP. Message : "La cartographie est prématurée : le dépôt ne contient pas encore de structure exploitable."
- Si seule une partie locale du système est visible, ne pas extrapoler les dépendances globales ; marquer `UNKNOWN`.

## SCOPE

### Inclus

- modules cœur
- features
- submodules
- hooks / events
- utilities
- services externes
- dépendances inter-repo si visibles
- relations intra-repo et inter-service

### Exclus

- audit sécurité
- dette technique profonde
- changements de code
- design de nouvelles abstractions

## PROCESS

1. Scanner la structure du projet.
2. Identifier les unités significatives et les classer.
3. Construire un arbre lisible des composants majeurs.
4. Identifier les relations observables :
   - utilise
   - dépend de
   - déclenche
   - expose
   - persiste dans
   - consomme
5. Distinguer :
   - intra-repo
   - inter-service / externe
6. Si `docs/ARCHITECTURE.md` existe déjà, préserver le current truth et mettre à jour seulement les nœuds affectés.
7. Produire ou mettre à jour `docs/ARCHITECTURE.md` et `docs/RELATIONS.md`.

## OUTPUT CONTRACT

Créer ou mettre à jour :

- `docs/ARCHITECTURE.md`
- `docs/RELATIONS.md`

Le résultat doit :

- rester lisible en moins de 60 secondes
- distinguer intra-repo et inter-service
- référencer les sources observables
- signaler les zones ambiguës comme `UNKNOWN`

## VERDICT RULES

- `READY`
  - structure principale lisible et relations majeures documentées
- `PARTIAL`
  - cartographie utile mais partielle, avec zones d’ombre bornées
- `BLOCKED`
  - structure trop floue ou dépôt trop embryonnaire pour produire une cartographie utile
- `UNKNOWN`
  - visibilité insuffisante sur les dépendances pour conclure proprement
