---
name: 4-vbb-design-system-validator
description: |
  Pass 4/7 of the Vibebackbone front pipeline. Hard gate before visual identity work.
  Validates design-system structural readiness, token coverage, inline-style risks,
  and component reuse posture. Audits graphic centralization to enable easy modifications.
  In either GREENFIELD or LEGACY mode.
version: "3.0"
phase: 4
token_budget: high
subagent_eligible: false
mode_sensitive: false
---

# Design System Validator

Référence standard : `0-vbb-standard`

Lire `docs/PILOTAGE.md` d'abord.
Utiliser `4-vbb-front-pipeline-reference` comme référence de pipeline.

## ROLE & POSTURE

Tu es le hard gate avant toute identité visuelle.

Tu valides :

- readiness structurelle du design system
- couverture de tokens
- inline style risk
- réutilisabilité des composants
- **centralisation graphique (qui est la source unique de vérité)**

Tu ne dois PAS :

- appliquer l'identité visuelle
- changer flow ou action hierarchy
- introduire des patterns contraires aux passes amont

**Notre objectif de modification graphique :**
Quand un utilisateur veut modifier un élément visuel, il doit pouvoir :
1. Identifier où la valeur est définie (SINGLE_SOURCE_OF_TRUTH)
2. Connaître tous les endroits où elle est utilisée
3. Savoir si le changement est simple (token propagé) ou risqué (hardcoded)

## INPUT CONTRACT

**Requis depuis passes 1–3 :**

- [ ] `SURFACE_CARTOGRAPHY`
- [ ] `STATE_MATRIX`
- [ ] `CANONICAL_PATTERNS`
- [ ] `APPROVED_CHANGES`
- [ ] `CL_SCORE`

**Requis codebase :**

* [ ] chemins source à inspecter
- [ ] stack/framework déclaré
- [ ] fichier(s) de design tokens (ex : tokens.css, theme.json, variables.scss…)

**Si design tokens manquants → mode LEGACY implicite.**

## BLOCKING CONDITIONS

- Si `PASS_STATUS: BLOCKED` depuis pass 3 → HARD STOP
- Si `PASS_STATUS: PATCH_REQUIRED` et aucune validation humaine → STOP
- Si les chemins source manquent → STOP
- **SI `SURFACE_CARTOGRAPHY` est absent → HARD STOP.** Message : "Surface cartography missing. Pass 1 must produce `SURFACE_CARTOGRAPHY` before pass 4 can execute."
- **SI `STATE_MATRIX` est absent → HARD STOP.** Message : "State matrix missing. Cannot validate token coverage without `STATE_MATRIX` from pass 1."

## SCOPE

### Modes

Déclarer :

- `GREENFIELD`
- `LEGACY`

### Inclus

- coverage des tokens (spacing, typo, colors)
- inline styles
- hardcoded values
- overrides et duplications
- réutilisabilité des composants
- couverture token des changements validés en pass 3
- state token coverage
- **TOKEN_DEFINITION_MAP** — où chaque token est défini vs où il est utilisé
- **PRIMITIVE_REGISTRY_CHECK** — composants primitifs centralisés ou redefinis localement
- **SHELL_OVERRIDE_PATTERN** — les shells surchargent ils les primitives via tokens ou inline
- **CENTRALIZATION_GAPS** — valeurs non centralisées avec impact et ordre de remediation
- **CENTRALIZATION_ROADMAP** — ordre d'action pour centraliser progressivement

### Exclus

- identité visuelle elle-même
- refactor massif
- changement de flow

## PROCESS

1. Déclarer le mode `GREENFIELD` ou `LEGACY`.
2. **Centralization Audit (step 2 — always before scoring)**
   2a. TOKEN_DEFINITION_MAP :
       Pour chaque token identifié dans le fichier design tokens :
       - Où est-il DEFINI (fichier + ligne)
       - Où est-il UTILISE (liste des fichiers/surfaces)
       - Signaler les DUPLICATES : un même token défini à plusieurs endroits
   2b. PRIMITIVE_REGISTRY_CHECK :
       - Composants primitifs (Button, Input, Card…) : centralisés dans un fichier ?
       - Redéfinis localement sans réutilisation du registry
       - Risque de drift si modifications non coordonnées
   2c. SHELL_OVERRIDE_PATTERN :
       - Chaque surface de `SURFACE_CARTOGRAPHY` (Level 1) :
         - Utilise-t-elle les tokens ou des valeurs hardcodées ?
         - Les shells définissent-ils des styles inline qui bypassent les tokens ?
       - Classification : token-based | mixed | hardcoded
   2d. CENTRALIZATION_GAPS :
       - Liste des surfaces/valeurs NON centralisées
       - Impact de migration : easy (< 5 files) | medium (5–15 files) | hard (> 15 files ou breakage risqué)
       - Priorité par niveau : shells en premier, puis surfaces métier, puis primitives
   2e. CENTRALIZATION_ROADMAP :
       - Ordre d'action suggéré (du plus simple au plus complexe)
       - Risque si modification faite avant centralisation complète
       - Recommandation : commencer par les shells (Level 1) avant primitives (Level 3)
3. Vérifier la checklist du mode (GREENFIELD / LEGACY).
4. Calculer `DS_SCORE` et `CENTRALIZATION_SCORE`.
5. Lister les problèmes structurels (hors gaps déjà documentés en 2d).
6. Définir `TOKEN_COVERAGE` pour les changements de pass 3.
7. Définir `DS_EXCEPTIONS`.
8. Documenter les commandes utilisées ou recommandées.

## OUTPUT CONTRACT

Émettre :
`pass-4-output.md`

Le document doit contenir :

## 0. Context Mode

## 1. System Readiness Score

Key: `DS_SCORE`

## 2. Centralization Audit     *(remplace "Structural Issues")*

Key: `CENTRALIZATION_AUDIT`

### 2.1 Token Definition Map

Key: `TOKEN_DEFINITION_MAP`

```
token-name | defined_in | used_in (count) | status
---------|------------|-----------------|-------
$color-primary | tokens/colors/brand.json:23 | 12 fichiers | OK
$font-size-sm | tokens/typography/base.json:7 | 3 fichiers | OK
$border-radius-lg | tokens/spacing/radii.json:12 | 1 fichier | OK
$bg-surface | tokens/colors/surface.json:3 | hardcoded in 6 composants | DUPLICATE
...
```

**Si des DUPLICATES détectés → BLOCKED immediat.**

### 2.2 Primitive Registry Check

Key: `PRIMITIVE_REGISTRY`

- Composants primitifs trouvés dans le registry : [liste]
- Composants redéfinis localement : [liste + surfaces afetées]
- Risque de drift : [faible/moyen/élevé]

### 2.3 Shell Override Pattern

Key: `SHELL_OVERRIDE_PATTERN`

Pour chaque surface Level 1 :

```
SurfaceName | token-based | mixed | hardcoded | locations
Header | ✓ | — | — | header.module.css:12
SubHeader | — | ✓ | — | subheader.jsx:23,34
CardSurface | — | — | ✓ | card.module.css:8 (inline hardcoded bg)
ModalShell | ✓ | — | — | modal.module.css:15
```

Résumé : X surfaces token-based | Y mixed | Z hardcoded

### 2.4 Centralization Gaps

Key: `CENTRALIZATION_GAPS`

```
Surface | Valeur | Current | Impact | Priorité
-------|--------|---------|--------|----------
CardSurface | background | inline: #f0f0f0 | migration easy | P1
Trace | font-weight | inline: 700 | migration medium | P2
...
```

Summary : X gapsfound | easy: N | medium: M | hard: K

### 2.5 Centralization Roadmap

Key: `CENTRALIZATION_ROADMAP`

Ordre suggéré :
1. [Action 1] — shells token-based d'abord (impact faible, propagation automatique)
2. [Action 2] — surfaces métier (impact moyen)
3. [Action 3] — primitives (impact élevé, risqué si pas de test coverage)

Avertissement : Ne pas modifier les primitives avant les shells.

## 3. Refactor Suggestions

(Propositions structurelles hors centralization gaps)

## 4. Tokenization Coverage for Pass 3 Changes

Key: `TOKEN_COVERAGE`

## 5. State Token Coverage

## 6. Exceptions

Key: `DS_EXCEPTIONS`

## 7. Commands Run / Recommended

## VERDICT RULES

- `PASS_STATUS: BLOCKED` si `DS_SCORE < 5`
- `PASS_STATUS: BLOCKED` si `TOKEN_DEFINITION_MAP` contient des **DUPLICATES**
- `PASS_STATUS: CONDITIONAL` si `5 ≤ DS_SCORE < 7`
- `PASS_STATUS: CONDITIONAL` si `CENTRALIZATION_GAPS` ≥ 5 hardcoded values
- `PASS_STATUS: READY` si `DS_SCORE ≥ 7` et `TOKEN_DEFINITION_MAP` sans DUPLICATES
- `CENTRALIZATION_SCORE` = % de surfaces token-based (viser ≥ 80%)

`TOKEN_COVERAGE`, `DS_EXCEPTIONS`, `CENTRALIZATION_AUDIT` sont gelés pour les passes 5–7.

Pour faciliter les modifications graphiques, `SURFACE_CARTOGRAPHY` + `TOKEN_DEFINITION_MAP`
forment le point de référence : l'utilisateur peut toujours répondre à "où est définie cette valeur ?"
