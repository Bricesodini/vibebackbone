---
name: 0-vbb-standard
description: |
  Defines the canonical Vibebackbone skill contract for Pi.
  Use when creating, adapting, reviewing, or validating any Vibebackbone skill.
  Keywords: skill standard, frontmatter, validation, report template, Pi compatibility,
  skill contract, mode-sensitive, subagent.
version: "1.1"
phase: transverse
token_budget: low
subagent_eligible: false
mode_sensitive: false
---

# Vibebackbone Skill Standard

## ROLE & POSTURE

You are the canonical reference for all Vibebackbone skills.

Your role is to define and validate:

- expected structure
- frontmatter
- reporting format
- hard rules
- Pi compatibility

You do not perform repo audits.
You validate skill design and skill consistency.

## INPUT CONTRACT

**Requis :**

- [ ] Un `SKILL.md` à créer, adapter ou valider

**Optionnels :**

- [ ] Un skill existant
- [ ] Un besoin fonctionnel à transformer en skill
- [ ] Une comparaison entre version Claude / Codex / Pi

**Sources acceptées :** contenu collé, chemin de fichier, description textuelle

## BLOCKING CONDITIONS

- Si aucun skill ni besoin de skill n’est fourni → STOP. Message : "Aucun skill à normaliser ou à valider."
- Si la demande concerne un audit de repo et non un skill → STOP. Message : "Cette ressource définit les standards des skills, pas l’audit d’un projet."

## SCOPE

This skill defines:

- mandatory flat frontmatter
- filesystem path / parent directory ↔ `name` compatibility
- mandatory section layout
- report template
- verdict taxonomy
- severity taxonomy
- subagent brief pattern
- absolute rules
- Pi-oriented routing description quality

### Sections optionnelles (pour skills d'exécution)

- `SUPPORT BOUNDARY` — liste explicite des cas supportés et non supportés

Format canonique de SUPPORT BOUNDARY :

```markdown
## SUPPORT BOUNDARY

Supporté :
- <cas supporté 1>
- <cas supporté 2>

Non supporté (refuser explicitement) :
- <cas non supporté 1> → <raison>
- <cas non supporté 2> → <raison>
```

Règle : tout skill qui écrit dans le repo (phase 1, transverse exécution)
devrait inclure cette section. Les skills de lecture seule (phase 0, 2, 3)
sont exemptés — leur scope est naturellement borné par leur rôle d'audit.

## PROCESS

1. Check skill name format and filesystem path / parent directory compatibility.
2. Check frontmatter completeness.
3. Check required sections.
4. Check whether `mode_sensitive` logic is handled correctly.
5. Check whether the report/output format matches Vibebackbone requirements.
6. Check whether the description is precise enough for Pi routing.
7. Check whether internal references use only canonical skills that exist in the same catalog.
8. Check whether `SUPPORT BOUNDARY` is present for execution skills (recommended, not mandatory yet).
9. Flag any violation against absolute rules.

## OUTPUT CONTRACT

Output must contain:

- compliance status
- missing or invalid sections
- frontmatter issues
- path/name alignment issues
- Pi compatibility issues
- structural fixes required
- optional improvements

## VERDICT RULES

Use:

- `READY` if the skill is compliant
- `PARTIAL` if structurally usable but incomplete
- `BLOCKED` if the skill breaks core Vibebackbone contract
- `UNKNOWN` if evidence is insufficient
