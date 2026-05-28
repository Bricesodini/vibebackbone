# ADR-0003 — GRAPHIC_PROPAGATION_MAP: Propagation Architecture First

## Status

Accepted: 2026-05-28

## Context

### Problème identifié

Le pipeline front Vibebackbone avait un **biais systémique** :

Le système dérivait trop rapidement vers :
- Button wrappers
- Card registry
- design tokens
- composants primitifs
- migration technique

alors que l'objectif utilisateur était :
**FACILITER LES FUTURES MODIFICATIONS GRAPHIQUES**

Le pipeline confondait :
- **A. DESIGN SYSTEM CREATION** (créer tokens, registries, primitives)
- **B. GRAPHIC CENTRALIZATION / PROPAGATION ARCHITECTURE** (identifier où les changements se propagent)

### Conséquence

Les propositions étaient orientées "construction" plutôt que "maintenance".
L'utilisateur ne savait pas :
- où modifier une valeur pour propager un changement
- quelles surfaces héritent de quelles autres
- quels composants sont des faux centres de contrôle
- où se situe la dette de propagation

## Decision

### 1. Distinction explicite A vs B

| | A. DESIGN SYSTEM CREATION | B. PROPAGATION ARCHITECTURE |
|--|--------------------------|---------------------------|
| Objectif | Créer de nouveaux tokens/registries | Identifier les points de contrôle visuel |
| Quand | Pass 4+ (optionnel, downstream) | Pass 1 (obligatoire, upstream) |
| Livrables | Button/Card/Badge registries | GRAPHIC_PROPAGATION_MAP |
| Priorité | LOW (downstream) | HIGH (upstream) |

### 2. ORDRE OBLIGATOIRE DE PRIORITÉ (non négociable)

```
1. SURFACE_PROPAGATION_POINTS
2. SHARED_VISUAL_ANCHORS
3. SHELL_CONSISTENCY
4. LAYOUT_INHERITANCE
5. THEME_PROPAGATION
6. PRIMITIVE_REGISTRIES
7. TOKEN_REFINEMENT
```

Les étapes 1–5 = **PROPAGATION ARCHITECTURE** (Pass 1)
Les étapes 6–7 = **DESIGN SYSTEM CREATION** (Pass 4+)

### 3. Nouveau livrable obligatoire : GRAPHIC_PROPAGATION_MAP

Produit en **step 0bis** de Pass 1, **AVANT** surface cartography standard.

Structure :
- `0.1 Propagation Points` : points de contrôle réel vs faux centres
- `0.2 Visual Inheritance Chains` : comment les styles se transmettent
- `0.3 Change Impact Map` : si je change X, qu'est-ce qui change
- `0.4 Propagation Debt` : où le changement est difficile aujourd'hui
- `0.5 Canonical Answer` : réponse canonique attendue

### 4. HARD RULE anti-dérive

**BLOCKED** si la réponse propose, **AVANT** GRAPHIC_PROPAGATION_MAP + SHELL_PROPAGATION_ANALYSIS :
- Button wrappers / registries
- Card registry
- Badge registry
- Primitives (Button, Input, etc.)
- Token expansion
- Migration design system

→ **GENERIC_DESIGN_SYSTEM_RESPONSE** → PASS_STATUS: BLOCKED

### 5. Priorité canonique

```
Propagation Architecture > Component Abstraction
```

## Consequences

### Positives

- Le pipeline produira d'abord une cartographie de propagation
- L'utilisateur saura où modifier pour propager un changement
- Les faux centres de contrôle seront identifiés
- La dette de propagation sera documentée
- Les propositions seront orientées maintenance, pas construction

### Négatives

- Pass 1 est plus long (step 0bis supplémentaire)
- Les propositions "design system" sont bloquées jusqu'à propagation map complète

### Artefacts modifiés

| Artefact | Action | Version |
|----------|--------|---------|
| `skills/4-vbb-user-experience-engine/SKILL.md` | Updated avec GRAPHIC_PROPAGATION_MAP | 2.3 |
| `skills/4-vbb-user-experience-engine/CONTRACT.yaml` | Updated outputs + blocking_rules | 0.3 |
| `skills/4-vbb-front-pipeline-reference/SKILL.md` | Updated gates + SEPARATION table | 2.2 |

## Verification

1. Pass 1 doit produire GRAPHIC_PROPAGATION_MAP AVANT surface cartography
2. Proposer "Button registry" avant propagation map → BLOCKED
3. Proposer "tokens $color-primary" sans propagation map → BLOCKED
4. GRAPHIC_PROPAGATION_MAP doit contenir propagation points + inheritance chains + debt

## Canonical Example

**BON :**
> "HeaderShell est le vrai point de propagation visuelle ; les Cards héritent de 4 chemins divergents ; modifier le radius aujourd'hui casserait 11 surfaces."

**MAUVAIS :**
> "Créons un Button registry, un Card registry, et définissons $color-primary."

**Résultat MAUVAIS :** GENERIC_DESIGN_SYSTEM_RESPONSE → PASS_STATUS: BLOCKED