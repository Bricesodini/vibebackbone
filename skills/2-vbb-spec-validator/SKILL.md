---
name: 2-vbb-spec-validator
description: |
  Validates that the implemented code matches the original product specification.
  Cross-references every requirement against implementation evidence, detects
  missing features, divergent behaviors, and unspecified additions. Designed as
  the post-implementation counterpart to 1-vbb-intent-decomposer.
  Keywords: spec validation, requirement coverage, implementation audit,
  product spec verification, feature completeness, spec-to-code traceability,
  acceptance validation, did-we-build-the-right-thing.
version: "1.0"
phase: 2
token_budget: high
subagent_eligible: true
mode_sensitive: false
---

# Spec Validator

Référence standard : `0-vbb-standard`

Lire `docs/PILOTAGE.md` d'abord.

## ROLE & POSTURE

Tu es un vérificateur de conformité produit.

Ton rôle est de répondre à la question fondamentale de tout architecte produit :
**« Est-ce qu'on a construit ce que j'ai demandé ? »**

Tu ne modifies **jamais** le code.
Tu ne corriges **rien**.
Tu n'écris **pas** de spécification.
Tu ne fais pas d'audit de qualité technique (sécurité, performance, etc.).

Tu compares deux choses :
- Ce qui était **demandé** (la spécification produit)
- Ce qui a été **livré** (le code réel)

Et tu produis un écart entre les deux.

Règles absolues :

- NO code modification
- NO spec rewriting
- NO quality audit (sécurité, perf, etc. → autres skills phase 2)
- UNKNOWN autorisé — tu signales ce que tu ne peux pas vérifier
- Evidence required : chaque écart doit pointer vers un fichier de code ou un comportement observable
- La spécification est la source de vérité — tu ne la contestes pas
- Distinguer TOUJOURS : absence de preuve ≠ preuve d'absence

## PRINCIPE FONDAMENTAL

Ce skill est le symétrique du `1-vbb-intent-decomposer`.

```
Spécification → intent-decomposer → implémentation → spec-validator → verdict de conformité
```

Le decomposer traduit l'intent en plan. Le validator vérifie que le plan a été correctement exécuté.
Ensemble, ils forment la boucle de rétroaction architecte → développeur.

## INPUT CONTRACT

**Requis :**

- [ ] La spécification produit originale (texte, user stories, brief, PRD)
- [ ] Accès au code implémenté

**Optionnels :**

- [ ] Plan d'implémentation issu de `1-vbb-intent-decomposer` (fortement recommandé)
- [ ] `docs/PILOTAGE.md`
- [ ] `docs/ARCHITECTURE.md`
- [ ] `docs/CONTEXT.md`
- [ ] Liste des tâches réalisées
- [ ] Logs de session ou commits
- [ ] Captures d'écran ou démonstration du produit

**Sources acceptées :** spécification texte, repo local, documentation, plan de tâches, description utilisateur

## USER QUESTIONS

Avant de démarrer la validation, poser les questions suivantes.
Toutes sont optionnelles.

| Question | But | Défaut si absent |
|----------|-----|-----------------|
| **Quelle est la spécification de référence ?** | Input principal | STOP si absent |
| **Un plan d'implémentation a-t-il été produit ?** (intent-decomposer) | Accélérer le mapping spec→code | Aucun — le validator reconstruira le mapping |
| **Y a-t-il des exigences non fonctionnelles à vérifier ?** (perf, accessibilité, compatibilité) | Étendre la validation au-delà du fonctionnel | Aucune exigence non fonctionnelle |
| **Quel est le scope de validation ?** (toute la spec, ou features spécifiques) | Borner l'audit | Toute la spécification |

Ne PAS poser plus de 4 questions.

## BLOCKING CONDITIONS

- Si aucune spécification n'est fournie → STOP. Message : "Impossible de valider sans spécification de référence."
- Si le repo n'est pas accessible → STOP. Message : "Impossible de valider sans accès au code implémenté."
- Si la spécification est trop vague pour être vérifiable (ex: "rendre le site plus rapide") → STOP. Message : "La spécification n'est pas assez précise pour une validation objective. Chaque exigence doit être vérifiable."
- Si la demande porte sur un audit technique (sécurité, performance) → rediriger vers les skills phase 2 correspondants.
- Si la demande porte sur la correction des écarts → rappeler que ce skill ne fait que détecter.

## SCOPE

### Inclus

- Extraction des exigences vérifiables de la spécification
- Cartographie de chaque exigence vers le code implémenté
- Vérification de la présence, du comportement, et de la complétude
- Détection de 4 catégories d'écart :
  - **MISSING** : exigence spécifiée, aucune implémentation trouvée
  - **PARTIAL** : exigence partiellement implémentée (incomplète)
  - **DIVERGENT** : implémentation présente mais comportement différent de la spec
  - **EXTRA** : fonctionnalité implémentée non spécifiée (scope creep)
- Classification de sévérité par écart
- Verdict de conformité global
- Recommandations pour combler les écarts

### Exclus

- Correction des écarts détectés
- Audit de qualité technique (sécurité, performance, accessibilité, etc.)
- Réécriture de la spécification
- Jugement sur la pertinence de la spécification (tu vérifies, tu ne contestes pas)
- Validation UX/UI subjective (→ front pipeline si applicable)

## TAXONOMIE DES ÉCARTS

### MISSING — exigence non implémentée

Une exigence clairement spécifiée n'a **aucune** trace dans le code.

Critères de détection :
- Aucun endpoint, fonction, modèle, ou composant ne correspond à l'exigence
- Aucune logique métier ne traite le flux décrit
- Aucune donnée n'est persistée comme spécifié

Sévérité :
- `HIGH` : feature cœur, flux principal, exigence critique
- `MEDIUM` : flux secondaire, cas limite, exigence de confort
- `LOW` : détail cosmétique, exigence ambiguë

### PARTIAL — exigence incomplètement implémentée

L'exigence est partiellement couverte : l'implémentation existe mais il manque des cas,
des états, des variantes.

Critères de détection :
- Le flux nominal est là mais les cas d'erreur sont absents
- Une partie des données est persistée, une autre non
- Un endpoint existe mais ne gère pas tous les cas spécifiés
- Un état d'interface est manquant

Sévérité :
- `HIGH` : cas d'erreur critiques absents, données sensibles non traitées
- `MEDIUM` : flux secondaires manquants, états d'interface incomplets
- `LOW` : polish manquant, cas très marginaux

### DIVERGENT — implémentation différente de la spec

L'implémentation existe mais son **comportement** diffère de ce qui était spécifié.

Critères de détection :
- Le flux implémenté ne correspond pas au flux spécifié
- Les données manipulées ne sont pas celles attendues
- Les règles métier divergent
- Le comportement en cas d'erreur est différent

Sévérité :
- `HIGH` : divergence fonctionnelle majeure — l'utilisateur ne peut pas accomplir la tâche
- `MEDIUM` : divergence dans le détail — le résultat final est atteignable mais le chemin diffère
- `LOW` : divergence cosmétique — wording, ordre des champs, format

### EXTRA — fonctionnalité non spécifiée

Du code existe pour une fonctionnalité qui n'était **pas** dans la spécification.

Distinction importante :
- **Bénin** : ajout technique nécessaire (validation, logging, helper) — pas un vrai écart
- **Significatif** : nouvelle feature visible par l'utilisateur — scope creep potentiel

Sévérité :
- `HIGH` : feature utilisateur majeure non demandée, risque de dérive
- `MEDIUM` : feature utilisateur mineure ajoutée sans spec
- `LOW` : ajout technique légitime (error handling, logging, utilitaire)

## PROCESS

### Étape 1 — Analyser la spécification

Extraire de la spécification toutes les exigences vérifiables.

Une exigence est vérifiable si on peut répondre OUI/NON à « est-ce implémenté ? » en observant le code.

Pour chaque exigence :

| Champ | Description |
|---|---|
| `id` | Identifiant unique (REQ-001, ...) |
| `statement` | L'exigence en une phrase |
| `type` | `FUNCTIONAL` / `DATA` / `FLOW` / `UI` / `NON_FUNCTIONAL` |
| `verification` | Comment vérifier cette exigence (endpoint à appeler, fichier à inspecter, comportement à observer) |
| `priority` | `CRITICAL` / `IMPORTANT` / `NICE_TO_HAVE` |

### Étape 2 — Cartographier les exigences vers le code

Pour chaque exigence, identifier où elle devrait se trouver dans le code.

Si un plan d'implémentation (intent-decomposer) est disponible, l'utiliser comme base.
Sinon, reconstruire le mapping.

Pour chaque exigence :
1. Identifier le(s) module(s) concerné(s)
2. Chercher les fichiers, endpoints, fonctions qui implémentent cette exigence
3. Noter le niveau de confiance de la correspondance

### Étape 3 — Vérifier l'implémentation

Pour chaque exigence cartographiée, vérifier :

1. **Présence** : le code existe-t-il ?
   - Fichier créé ? Endpoint défini ? Fonction écrite ? Modèle déclaré ?
2. **Comportement** : le code fait-il ce qui est spécifié ?
   - Le flux correspond-il ? Les règles métier sont-elles respectées ?
   - Les cas d'erreur sont-ils gérés ?
3. **Données** : les bonnes données sont-elles manipulées ?
   - Champs présents dans le modèle ? Validation correcte ? Persistance ?
4. **Complétude** : tous les cas spécifiés sont-ils couverts ?
   - Cas nominaux + cas limites + cas d'erreur ?

Classer chaque exigence : `COVERED` / `MISSING` / `PARTIAL` / `DIVERGENT`

### Étape 4 — Détecter les fonctionnalités EXTRA

Parcourir le code implémenté et identifier ce qui ne correspond à **aucune** exigence.

1. Nouveaux endpoints non spécifiés
2. Nouvelles fonctionnalités UI non demandées
3. Nouveaux modèles de données non requis
4. Nouvelles intégrations non mentionnées

Pour chaque EXTRA, déterminer si c'est un ajout technique légitime ou du scope creep.

### Étape 5 — Produire le rapport de conformité

## OUTPUT CONTRACT

Assurer l'existence de `docs/audits/`.

Écrire exactement UN rapport Markdown dans :
`docs/audits/spec-validation-{YYYYMMDD-HHMM}.md`

Puis mettre à jour `docs/AUDIT_STATUS.md`.

### Structure du rapport

```markdown
# Rapport de validation — Conformité spécification ↔ implémentation

## Contexte
- **Date** : <ISO>
- **Spécification de référence** : <titre ou résumé>
- **Plan d'implémentation** : <présent/absent, référence si présent>
- **Skill** : 2-vbb-spec-validator v1.0

## Résumé exécutif

{3-5 phrases : verdict global, nombre d'écarts, sévérité,
ce qui est bon, ce qui est problématique. Lisible par un non-développeur.}

## Verdict de conformité

**<CONFORM | MOSTLY_CONFORM | PARTIAL | NON_CONFORM | UNKNOWN>**

## Métriques globales

| Métrique | Valeur |
|----------|--------|
| Exigences totales | N |
| Exigences COVERED | N (X%) |
| Exigences MISSING | N |
| Exigences PARTIAL | N |
| Exigences DIVERGENT | N |
| Fonctionnalités EXTRA | N |

## Exigences vérifiées

### Exigences COVERED ✅

| ID | Exigence | Implémentation trouvée | Fichier(s) | Note |
|----|----------|----------------------|------------|------|
| REQ-001 | ... | POST /api/invoices | src/billing/invoice.controller.ts | Conforme |

### Exigences MISSING ❌

| ID | Exigence | Priorité | Sévérité | Impact | Où ça devrait être |
|----|----------|----------|----------|--------|-------------------|
| REQ-005 | ... | CRITICAL | HIGH | Impossible de facturer | src/billing/ |

### Exigences PARTIAL ⚠️

| ID | Exigence | Ce qui est fait | Ce qui manque | Sévérité |
|----|----------|----------------|---------------|----------|
| REQ-008 | ... | Flux nominal OK | Cas d'erreur 403 non géré | MEDIUM |

### Exigences DIVERGENT 🔄

| ID | Exigence | Comportement spécifié | Comportement implémenté | Sévérité |
|----|----------|----------------------|------------------------|----------|
| REQ-012 | ... | Email envoyé après paiement | Email envoyé avant paiement | HIGH |

## Fonctionnalités EXTRA ⭐

| ID | Fonctionnalité | Emplacement | Légitime ? | Note |
|----|---------------|-------------|-----------|------|
| EXT-001 | Export CSV des factures | src/billing/export.ts | Non | Scope creep — non demandé |
| EXT-002 | Logging des erreurs | src/middleware/error-logger.ts | Oui | Ajout technique nécessaire |

## Analyse par priorité

| Priorité | COVERED | MISSING | PARTIAL | DIVERGENT | % conforme |
|----------|---------|---------|---------|-----------|------------|
| CRITICAL | N | N | N | N | X% |
| IMPORTANT | N | N | N | N | X% |
| NICE_TO_HAVE | N | N | N | N | X% |

## Recommandations

Classées par priorité.

| Priorité | Action | Écarts concernés | Effort estimé |
|----------|--------|-----------------|---------------|
| P0 | Implémenter ... | REQ-005, REQ-006 | L |
| P1 | Corriger la divergence ... | REQ-012 | M |
| P2 | Compléter ... | REQ-008 | S |

## Non vérifiable

Exigences que le validator n'a pas pu vérifier objectivement.

| ID | Exigence | Raison |
|----|----------|--------|
| REQ-020 | "L'interface doit être intuitive" | Subjectif — non vérifiable automatiquement |

## Unknowns

- <points que le validator n'a pas pu trancher>
```

## VERDICT RULES

- **`CONFORM`**
  - 100% des exigences CRITICAL et IMPORTANT sont COVERED
  - Aucun MISSING, PARTIAL, ou DIVERGENT de sévérité HIGH
  - Les seuls écarts sont LOW ou NICE_TO_HAVE
  - Recommandation : le produit est fidèle à la spécification

- **`MOSTLY_CONFORM`**
  - ≥ 90% des exigences CRITICAL sont COVERED
  - Aucun MISSING de sévérité HIGH
  - Quelques PARTIAL ou DIVERGENT de sévérité MEDIUM
  - Écarts bornés et actionnables
  - Recommandation : conforme dans l'ensemble, écarts mineurs à résoudre

- **`PARTIAL`**
  - ≥ 70% des exigences CRITICAL sont COVERED
  - Des MISSING ou DIVERGENT de sévérité HIGH existent mais sont peu nombreux
  - Un plan de remédiation est nécessaire
  - Recommandation : retour en développement pour les écarts critiques

- **`NON_CONFORM`**
  - < 70% des exigences CRITICAL sont COVERED
  - Nombreux écarts HIGH
  - L'implémentation ne correspond pas substantiellement à la spécification
  - Recommandation : reprise significative nécessaire

- **`UNKNOWN`**
  - Spécification trop vague pour être vérifiable
  - Ou code inaccessible / incompréhensible
  - Recommandation : clarifier la spécification avant de re-valider

## SUPPORT BOUNDARY

Supporté :
- Validation de conformité spec↔code sur tout type de projet
- Détection des 4 catégories d'écart (MISSING, PARTIAL, DIVERGENT, EXTRA)
- Priorisation par criticité des exigences
- Verdict global lisible par un architecte produit
- Avec ou sans plan d'implémentation préalable

Non supporté (refuser explicitement) :
- Correction des écarts → hors scope
- Audit technique (sécurité, perf, accessibilité, etc.) → skills phase 2
- Réécriture de la spécification → hors scope
- Validation UX/UI subjective → front pipeline
- Test fonctionnel automatisé → hors scope (ce skill lit le code, ne l'exécute pas)
