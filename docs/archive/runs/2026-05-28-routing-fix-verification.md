# Routing Fix Verification — UI/UX Signal Test

**Purpose**: Verify that the UI/UX ENGINE_ONLY routing rule is properly triggered.
**Date**: 2026-05-28
**Status**: PENDING

---

## Trigger phrases that MUST route to ENGINE_ONLY pipeline

| Phrase | Expected behavior | Skill to invoke |
|--------|------------------|-----------------|
| UI/UX (in any request context) | ENGINE_ONLY → pass 1 | `vibebackbone` orchestrator → `4-vbb-user-experience-engine` |
| "cohérence UI/UX" | ENGINE_ONLY → pass 1 | `vibebackbone` |
| "architecture visuelle" | ENGINE_ONLY → pass 1 | `vibebackbone` |
| "centralisation graphique" | ENGINE_ONLY → pass 1 | `vibebackbone` |
| "design system" | ENGINE_ONLY → pass 1 | `vibebackbone` |
| "optimiser" + "logiques" + "modifications graphiques" | ENGINE_ONLY → pass 1 | `vibebackbone` |
| "modifications graphiques" alone | ENGINE_ONLY → pass 1 | `vibebackbone` |
| "audit surface" + "Trame" | ENGINE_ONLY → pass 1 | `vibebackbone` |

---

## Test protocol

### Step 1 — Test in a clean Pi session

Open a new Pi session and send this exact request:

```
Quels skills vas-tu utiliser pour cette demande, et pourquoi ?

"Analyse toute la partie UI/UX et vois comment optimiser les logiques
pour faciliter les modifications graphiques en centralisant le maximum de choses."
```

### Step 2 — Expected response

Before proceeding, Pi must:
1. Invoke `vibebackbone` orchestrator skill
2. Detect ENGINE_ONLY trigger
3. Emit routing decision: `ENGINE_ONLY (front pipeline, passes 1–7)`
4. Name `4-vbb-user-experience-engine` as first skill
5. Name `4-vbb-front-pipeline-reference` as companion read
6. Emit full pipeline sequence: pass 1 → 2 → 3 → 4 → 5 → 6 → 7
7. NOT proceed directly to token or primitive analysis

### Step 3 — Verification checklist

- [ ] `vibebackbone` skill invoked
- [ ] `ENGINE_ONLY` mode declared
- [ ] `4-vbb-user-experience-engine` named as primary
- [ ] `SURFACE_CARTOGRAPHY` mentioned as required first deliverable
- [ ] Direct token/primitive proposal ABSENT from initial response
- [ ] Full 7-pass sequence outlined

### Step 4 — Pass/fail criteria

**PASS**: All 6 checklist items verified before any analysis begins.

**FAIL**: Any of the following without prior routing:
- Direct token proposal ($color-primary, $spacing-md)
- Direct primitive proposal (Button, Badge, Tooltip)
- "migrate to design system" without SURFACE_CARTOGRAPHY
- Single-skill response without pipeline sequence

---

## Files modified in this routing fix

| File | Change |
|------|--------|
| `AGENTS.md` | Added rule 9: UI/UX routing discipline |
| `SYSTEM.md` | Added UI/UX routing rule in Session behavior |
| `skills/vibebackbone/SKILL.md` | Expanded ENGINE_ONLY triggers + companion reads |
| `prompts/0-p-vbb-triage.md` | Added ENGINE_ONLY path + UI/UX shortcut + fixed path vocabulary (QUICK→FAST, CLÔTURE→CLOSEOUT) |
| `docs/runs/routing-fix-verification.md` | Test protocol artifact (this file) |

**Total: 5 files changed**

---

## Robustness issues found during verification pass

| File | Line | Issue found | Fixed |
|------|------|------------|-------|
| `prompts/0-p-vbb-triage.md` | ALL | Used `QUICK` and `CLÔTURE` instead of `FAST` and `CLOSEOUT`; lacked ENGINE_ONLY path; `0-vbb-pilotage` was only route, `vibebackbone` skill never invoked early enough | YES — rewrote with corrected path vocabulary + ENGINE_ONLY + UI/UX shortcut |

---

## Root cause summary

**Problem**: Pi executed UI/UX analysis directly without invoking `vibebackbone` orchestrator.

**Root cause**: The orchestrator skill contained the ENGINE_ONLY rule but the boot-level `AGENTS.md` had no equivalent rule. Pi did not know to treat UI/UX requests as routing decisions rather than execution decisions. Additionally, `prompts/0-p-vbb-triage.md` used wrong path vocabulary and had no ENGINE_ONLY entry point.

**Fix**: Four-way reinforcement:
1. `AGENTS.md` rule 9 — boot-level imperative
2. `SYSTEM.md` session behavior — session-start gate
3. `skills/vibebackbone/SKILL.md` — expanded trigger detection + companion reads
4. `prompts/0-p-vbb-triage.md` — ENGINE_ONLY path + UI/UX shortcut + correct path vocabulary

---

## Final diff summary

```
AGENTS.md                    |  3 ++-
SYSTEM.md                   |  1 +
prompts/0-p-vbb-triage.md   | 45 ++++++++++++++++++++++++++++---------------
skills/vibebackbone/SKILL.md | 15 ++++++++++++---
4 files changed, 45 insertions(+), 19 deletions(-)
(untracked: docs/runs/routing-fix-verification.md)
```
