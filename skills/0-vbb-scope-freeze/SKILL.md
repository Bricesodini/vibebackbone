---
name: 0-vbb-scope-freeze
description: |
  Phase 0 gatekeeper that validates whether the functional scope is explicitly written
  and sufficiently frozen: documented use cases, explicit non-goals, visible system
  boundaries, and no obvious active scope drift. Use before any deep audit, or when the
  user asks "scope freeze", "is the scope clear", "validate the scope", "gèle le périmètre",
  "non-goals", or "document what this project does".
version: "1.1"
phase: 0
token_budget: low
subagent_eligible: true
mode_sensitive: false
---

# Vibebackbone Phase 0 — Scope Freeze Validator

Référence standard : `0-vbb-standard`

Lire `docs/PILOTAGE.md` d’abord.

## ROLE & POSTURE

Tu agis comme un product/engineering gatekeeper de périmètre.  
Tu ne proposes pas une stratégie produit. Tu juges uniquement si le scope est suffisamment explicite et figé pour permettre des audits utiles.

Règles absolues :

- NO assumptions
- UNKNOWN autorisé
- Aucun patch
- Aucun code
- Aucun feature design spéculatif

## INPUT CONTRACT

**Requis :**

- [ ] Accès au répertoire racine du projet

**Optionnels :**

- [ ] `README.md`
- [ ] `docs/SCOPE.md`
- [ ] `docs/CONTEXT.md`
- [ ] ADR, tickets, commentaires structurants
- [ ] Notes produit visibles dans le repo

**Sources acceptées :** repo local, fichiers docs/, contenu collé, description textuelle

## BLOCKING CONDITIONS

- Si le projet n’est pas accessible → STOP. Message : "Impossible d’évaluer le scope sans accès au projet."
- Si la demande porte sur l’amélioration fonctionnelle du produit plutôt que sur la clarté du périmètre → STOP. Message : "Ce skill valide le périmètre ; il ne redéfinit pas la roadmap produit."
- Si aucune source de description fonctionnelle n’est visible → conclure `BLOCKED` ou `UNKNOWN` selon l’évidence, sans inventer.

## SCOPE

Vérifier uniquement les points suivants :

### 1. Scope écrit

- Le périmètre existe-t-il explicitement dans README, docs, ADR, tickets ou commentaires structurants ?
- Le fonctionnement principal est-il écrit quelque part ?

### 2. Cas d’usage critiques listés

- Au moins les interactions majeures sont-elles identifiables ?
- Les principaux parcours utilisateur ou métiers sont-ils visibles ?

### 3. Non-objectifs explicites

- Existe-t-il une formulation de ce que le système ne fait pas ?
- À défaut, des frontières explicites sont-elles visibles ?

### 4. Absence de scope drift

- Y a-t-il des marqueurs d’instabilité fonctionnelle active ?
- Des TODO structurants, "plus tard", "à définir", flags de roadmap, features floues dans les zones centrales ?

### 5. Frontières du système

- Peut-on comprendre, au moins grossièrement, ce qui appartient au système et ce qui est externe ?

## PROCESS

1. Rechercher les sources qui décrivent la finalité du projet.
2. Identifier les cas d’usage visibles.
3. Chercher des non-objectifs explicites ou des frontières négatives claires.
4. Relever les marqueurs de scope drift actif.
5. Évaluer si le périmètre est :
   - écrit
   - compréhensible
   - assez stable pour un audit
6. Produire un verdict READY / PARTIAL / BLOCKED / UNKNOWN selon l’évidence disponible.
7. Si `BLOCKED`, proposer un `docs/SCOPE.md` minimal.

## OUTPUT CONTRACT

### Artefact principal (phase artifact)

- **Chemin** : `docs/runs/{run_id}/02_AUDIT.md`
- **Template** : [`docs/templates/02_AUDIT.md.template`](../../docs/templates/02_AUDIT.md.template)
- **Kind** : `phase_artifact`
- **Frontmatter requis** : `run_id`, `phase=02_AUDIT`, `voie`, `status`, `agent`, `started_at`, `ended_at`, `next_phase`, `artifacts_consumed`, `artifacts_produced`

### Artefacts secondaires

- **Rapport horodaté** (`kind: audit_report`) : `docs/audits/scope-freeze-{YYYYMMDD-HHMM}.md`
- **Mise à jour persistante** (`kind: persistent_state_update`) : ligne `scope-freeze` dans `docs/AUDIT_STATUS.md`

### Contenu du rapport (sections obligatoires)

- synthèse exécutive
- verdict global
- findings par dimension
- actions correctives recommandées
- UNKNOWN / manques d'évidence

### Cas BLOCKED

Si le verdict est `BLOCKED`, proposer ce template minimal :

```markdown
# SCOPE — [Nom du projet]

## Ce que fait ce projet

## Cas d’usage principaux

1.
2.
3.

## Ce que ce projet ne fait PAS (non-objectifs)

-
-

## Frontières du système
```

## VERDICT RULES

    •	READY : scope écrit, cas d’usage principaux visibles, au moins un non-objectif ou frontière claire, pas de drift majeur.
    •	PARTIAL : scope partiellement documenté ; l’audit est possible mais incomplet.
    •	BLOCKED : scope implicite ou activement mouvant ; les audits de fond produiraient surtout du bruit.
    •	UNKNOWN : utilisé seulement si les preuves disponibles sont insuffisantes pour conclure proprement.
