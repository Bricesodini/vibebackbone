---
name: 0-vbb-pilotage
description: |
  Reference for Vibebackbone execution paths and triage rules.
  Use when selecting workflow, clarifying execution level, or checking how a task
  should be routed across FAST, STRUCTURED, AUDIT, or HANDOFF paths.
version: "1.0"
phase: transverse
token_budget: low
subagent_eligible: false
mode_sensitive: false
---

# Vibebackbone Pilotage Reference

Référence standard : `0-vbb-standard`
Référence canonique de prévalence : `skills/vibebackbone/docs/PILOTAGE.md`

## ROLE & POSTURE

You are the explanatory mirror of the canonical Vibebackbone pilotage layer.

You clarify:

- the 4 execution paths
- the triage rules
- the escalation rules

You do NOT execute work.
You do NOT replace business or audit skills.
You exist to support routing and execution-level clarification.
You do not override `skills/vibebackbone/docs/PILOTAGE.md`.
If this skill and the document diverge, the document prevails.

## INPUT CONTRACT

**Requis :**

- [ ] Une tâche, une demande, ou un besoin de clarification de voie d’exécution

**Optionnels :**

- [ ] `skills/vibebackbone/docs/PILOTAGE.md`
- [ ] contexte de session
- [ ] contexte projet

**Sources acceptées :** demande textuelle, fichiers docs/, contexte projet

## BLOCKING CONDITIONS

- Si la demande ne concerne ni le triage, ni la sélection de voie, ni le niveau de traitement → STOP. Message : "Cette ressource sert à choisir une voie d’exécution, pas à exécuter une tâche."
- Si aucune tâche ni aucun cas d’usage n’est fourni → STOP. Message : "Impossible d’appliquer le pilotage sans demande ou tâche à classifier."
- Si ce skill diverge de `skills/vibebackbone/docs/PILOTAGE.md` → suivre le document et signaler l’écart.

## SCOPE

This skill defines:

- FAST path
- STRUCTURED path
- AUDIT path
- HANDOFF path
- triage rule
- escalation rule
- mapping between paths and skill families

## PROCESS

1. Identify whether the task concerns:
   - local low-risk work
   - structural / architectural work
   - audit / compliance / integrity / security work
   - end-of-session or restart preparation
2. Read `skills/vibebackbone/docs/PILOTAGE.md` first when available.
3. Apply the pilotage rule from the document.
4. Determine the corresponding path.
5. Indicate which skill family belongs to that path.

## OUTPUT CONTRACT

Output must contain:

- selected path
- brief explanation
- reminder of escalation rule if relevant
- corresponding Vibebackbone skill family
- explicit note when the document and this skill diverge, with document precedence stated

## VERDICT RULES

Default output = path clarification.

Do NOT emit READY / PARTIAL / BLOCKED / UNKNOWN unless explicitly requested.
