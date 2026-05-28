# ADR-0002 — Surface-first routing for UI/UX requests

**Status**: Accepted
**Date**: 2026-05-28
**Last updated**: 2026-05-28
**Deciders**: vibebackbone governance

---

## Contexte

Lors de demandes d'audit UI/UX ou de cohérence visuelle sur un projet, l'agent Vibebackbone routait directement vers `4-vbb-design-system-validator` (pass 4) dès la détection du mot-clé "UI" ou "design".

**Exemple de comportement，观察é :**
- Requête : "audit UI/UX cohérence / centralisation graphique Trame"
- Routage : `4-vbb-design-system-validator` (pass 4)
- Résultat : analyse tokens/styles/primitives sans cartographie des surfaces produit

L'agent descendant immédiatement au niveau implémentation (tokens, composants primitifs) sans jamais produire la cartographie systémique des surfaces (Header, SubHeader, CardSurface, ModalShell, etc.).

---

## Problème

**Écart de niveau d'analyse :**

| Comportement | Niveau |
|---|---|
| Produit | Analyse tokens/primitives |
| Attendu | Cartographie systémique des surfaces → state matrix → tokens |

**Root cause identifiée :**
1. L'orchestrator ne contenait pas de rule de priorité "surface first"
2. `4-vbb-front-pipeline-reference` n'imposait pas ENGINE_ONLY comme mode par défaut pour les demandes UI/UX
3. `4-vbb-design-system-validator` ne bloquait pas si `SURFACE_CARTOGRAPHY` manquait
4. `4-vbb-user-experience-engine` ne produisait pas explicitement `SURFACE_CARTOGRAPHY` en premier
5. Pass 4 ne produisait pas d'audit centralisation — l'utilisateur ne savait pas où modifier les valeurs

---

## Décision

Toute demande portant sur la cohérence UI/UX, l'architecture visuelle, la centralisation graphique ou la modification graphique facilitée doit entrer en mode `ENGINE_ONLY` et passer par le pipeline front complet à partir du pass 1.

**Règle systémique Phase 1 :**
1. L'orchestrator détecte le trigger UI/UX et force `ENGINE_ONLY`
2. Pass 1 produit `SURFACE_CARTOGRAPHY` en premier (step 0 obligatoire)
3. `SURFACE_CARTOGRAPHY` + `STATE_MATRIX` sont gelés comme préconditions pour pass 4
4. Pass 4 bloque HARD si ces préconditions sont absentes

**Règle systémique Phase 2 :**
5. Pass 4 produit `CENTRALIZATION_AUDIT` avec TOKEN_DEFINITION_MAP
6. L'utilisateur peut répondre à "où est définie cette valeur ?" grâce à TOKEN_DEFINITION_MAP
7. CENTRALIZATION_ROADMAP guide l'ordre de migration pour faciliter les modifications graphiques

**Comportement attendu après modification :**
```
Request: "audit UI/UX / centralisation graphique Trame"
→ ENGINE_ONLY mode
→ Pass 1: Surface Cartography (Header, SubHeader, CardSurface…)
→ Pass 2 → 3 → 4
→ Pass 4: CENTRALIZATION_AUDIT
         - TOKEN_DEFINITION_MAP ("$bg-surface DEFINI tokens.json:23, UTILISÉ 12x")
         - CENTRALIZATION_GAPS ("cardSurface background inline, migration easy")
         - CENTRALIZATION_ROADMAP ("commencer par les shells")
         → L'utilisateur sait : où → quoi → comment
```

---

## Modifications appliquées

### Phase 1 — Routing surface-first

#### 1. `vibebackbone/SKILL.md` (orchestrator)
- Ajout de `UI/UX ENGINE_ONLY RULE` en PROCESS
- Détection de triggers: cohérence UI/UX, architecture visuelle, design system, surface cartography
- Routing direct vers `4-vbb-user-experience-engine` (pass 1)
- Emission de la séquence pipeline complète (pass 1 → 7)

#### 2. `4-vbb-front-pipeline-reference/SKILL.md`
- `VISUAL_ONLY` interdit sans `SURFACE_CARTOGRAPHY` valide
- Détection automatique de `ENGINE_ONLY` pour les demandes UI/UX
- Validation que pass 1 produira `SURFACE_CARTOGRAPHY` avant progression

#### 3. `4-vbb-design-system-validator/SKILL.md` (Phase 1 seulement)
- `SURFACE_CARTOGRAPHY` ajouté aux INPUT CONTRACT requis
- 2 HARD STOP blocks : absent SURFACE_CARTOGRAPHY / absent STATE_MATRIX

#### 4. `4-vbb-user-experience-engine/SKILL.md`
- Step 0 "Surface Mapping" rendu obligatoire en premier
- OUTPUT: section 0 `SURFACE_CARTOGRAPHY` avec structure Level 1/2/3
- `STATE_MATRIX` linké explicitement aux surfaces cartographiées
- Verdict `BLOCKED` si `SURFACE_CARTOGRAPHY` incomplet

### Phase 2 — Centralization Audit (2026-05-28)

#### 3'. `4-vbb-design-system-validator/SKILL.md` (v3.0)
- Section 2 remplacée par `CENTRALIZATION_AUDIT` complet :
  - 2.1 TOKEN_DEFINITION_MAP
  - 2.2 PRIMITIVE_REGISTRY_CHECK
  - 2.3 SHELL_OVERRIDE_PATTERN
  - 2.4 CENTRALIZATION_GAPS
  - 2.5 CENTRALIZATION_ROADMAP
- Fichier design tokens ajouté aux INPUT requis (mode LEGACY implicite si absent)
- VERDICT_RULES renforcé :
  - BLOCKED si TOKEN_DEFINITION_MAP contient des DUPLICATES
  - CONDITIONAL si CENTRALIZATION_GAPS ≥ 5 hardcoded values
- `CENTRALIZATION_SCORE` (% surfaces token-based, viser ≥ 80%)

#### 3''. `4-vbb-design-system-validator/CONTRACT.yaml` (v1.0)
- Inputs requis: `surface_cartography`, pas seulement `repo_access`
- Blocking rules explicites
- Routing triggers: `graphic centralization audit`, `token definition map`, `single source of truth`
- Outputs requis alignés: `centralization_audit`, `token_definition_map`, `centralization_gaps`, `centralization_roadmap`

---

## Conséquences

**Positive :**
- L'agent ne peut plus produire de tokens/styles avant cartographie des surfaces
- L'utilisateur peut répondre à "où est définie cette valeur ?" (TOKEN_DEFINITION_MAP)
- CENTRALIZATION_ROADMAP guide l'ordre de migration
- Pass 4 agit comme hard gate avec préconditions + audit de centralisation
- Le pipeline est respecté : pass 1 → 2 → 3 → 4

**Négative / risque à surveiller :**
- Ralentissement perçu si l'utilisateur veut une réponse rapide sur les tokens
- Risque de verbose si la codebase est déjà cartographiée

**Mitigations :**
- `SURFACE_CARTOGRAPHY` peut être produit une seule fois et réutilisé via gel de pass 1
- Si la codebase est riche, la cartographie peut être inférée automatiquement depuis l'inspection
- Phase 3 (nouveau skill `4-vbb-ui-architecture-centralization`) est prevue si régression constatée

---

## Non-décision

**4-vbb-ui-architecture-centralization n'est pas créé pour l'instant.**

**Raison :** Pass 1 produit déjà `SURFACE_CARTOGRAPHY` après Phase 1. La modification de l'existant est fonctionnellement suffisante.

**Conditions de création ultérieure :**
- Si le test de régression (même demande utilisateur) montre encore une réponse tokens-first
- Si le besoin de cartographie surfacique existe sans passer par le pipeline UX complet
- Si un entry point distinct "graphic architecture only" est demandé explicitement

---

## Condition de réouverture

**Si le test de régression échoue :**
- Même demande → l'agent produit encore du code/tokens sans cartographie surfacique
- Action : créer `4-vbb-ui-architecture-centralization` comme couche filtrage intermédiaire
- Action : ajouter un hard block "surface-first" dans l'orchestrator avec message explicite

**Test de régression :**
```
Input: "audit UI/UX cohérence / centralisation graphique Trame"
Vérification:
  1. Output contient SURFACE_CARTOGRAPHY avant toute mention de token
  2. SURFACE_CARTOGRAPHY liste les surfaces par nom sémantique (Header, SubHeader…)
  3. Pas de token/style/patch avant que la cartographie soit produite
  4. Pass 4 est en HARD STOP si SURFACE_CARTOGRAPHY manque
  5. Pass 4 produit TOKEN_DEFINITION_MAP avec au moins une entrée
  6. Pass 4 produit CENTRALIZATION_ROADMAP avec au moins une action
```

---

## Références

- Skill modifié : `skills/vibebackbone/vibebackbone/SKILL.md`
- Skill modifié : `skills/vibebackbone/4-vbb-front-pipeline-reference/SKILL.md`
- Skill modifié : `skills/vibebackbone/4-vbb-design-system-validator/SKILL.md` (v3.0)
- Skill modifié : `skills/vibebackbone/4-vbb-design-system-validator/CONTRACT.yaml` (v1.0)
- Skill modifié : `skills/vibebackbone/4-vbb-user-experience-engine/SKILL.md`
- Pipeline ref : `docs/PILOTAGE.md`

---

_v0.2 — 2026-05-28 — Phase 2: Centralization Audit added_
