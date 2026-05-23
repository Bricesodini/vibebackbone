---
name: t-vbb-session-handoff
description: |
  Compresses the end of a work session into a compact, factual, actionable handoff.
  Updates docs/SESSION.md so the next session can restart quickly and reliably.
  Prioritizes the next concrete step over narrative recap.
version: "2.0"
phase: transverse
token_budget: low
subagent_eligible: false
mode_sensitive: false
---

# Session Handoff

Référence standard : `0-vbb-standard`

Lire `skills/vibebackbone/docs/PILOTAGE.md` d’abord.

## ROLE & POSTURE

Tu es un secrétaire de session.
Ton rôle est de rendre la reprise quasi immédiate.

Tu dois être :

- factuel
- compact
- actionnable
- orienté prochaine étape

Tu ne produis PAS un récit.
Tu ne reformules PAS inutilement.
Tu privilégies la prochaine action concrète.

## INPUT CONTRACT

**Requis :**

- [ ] Conversation courante ou contexte de session

**Optionnels :**

- [ ] `docs/SESSION.md`
- [ ] `docs/CONTEXT.md`
- [ ] `docs/AUDIT_STATUS.md`
- [ ] historique git récent si visible
- [ ] fichiers touchés ou sujets principaux

**Sources acceptées :** conversation, docs/, git récent, description textuelle

## BLOCKING CONDITIONS

- Aucune. Si le contexte est minimal, écrire un `SESSION.md` minimal avec placeholders explicites.

## SCOPE

### Inclus

- ce qui a été fait
- décisions prises
- questions ouvertes
- fichiers/sujets touchés
- prochaine étape explicite
- mise à jour de `docs/SESSION.md`

### Exclus

- récit détaillé de toute la session
- ré-audit
- réécriture complète de `docs/CONTEXT.md` sans raison
- patch code
- préparation du paquet de commit propre et du message de commit (→ `t-vbb-commit-ready`)

## PROCESS

1. Analyser la conversation courante.
2. Lire, si disponible :
   - `docs/SESSION.md`
   - `docs/CONTEXT.md`
   - `docs/AUDIT_STATUS.md`
   - git récent
3. Identifier :
   - actions réalisées
   - décisions prises
   - blocages / questions ouvertes
   - fichiers ou zones concernés
4. Déterminer la prochaine étape la plus concrète.
5. Mettre à jour `docs/SESSION.md`.
6. Si des faits projet nouveaux sont apparus, signaler qu’une mise à jour de `docs/CONTEXT.md` est recommandée.

## OUTPUT CONTRACT

### Artefact principal (phase artifact)

- **Chemin** : `docs/runs/{run_id}/07_CLOSEOUT.md`
- **Template** : [`docs/templates/07_CLOSEOUT.md.template`](../../docs/templates/07_CLOSEOUT.md.template)
- **Kind** : `phase_artifact`
- **Frontmatter requis** : `run_id`, `phase=07_CLOSEOUT`, `voie`, `status`, `agent`, `started_at`, `ended_at`, `artifacts_consumed`, `artifacts_produced`

Le closeout est la mémoire officielle versionnée de fin de run.

### Artefact secondaire

- **Mémoire locale** (`kind: persistent_state_update`) : `docs/SESSION.md`
  - gitignored par design (per-machine handoff state, voir [`docs/MEMORY_AND_HANDOFF.md`](../../docs/MEMORY_AND_HANDOFF.md))
  - doit rester court : contexte courant, ce qui a été fait, décisions prises, questions ouvertes, fichiers / zones touchés, **prochaine étape explicite**

## VERDICT RULES

- `READY`
  - handoff compact, lisible et actionnable
- `PARTIAL`
  - handoff produit mais certaines informations clés restent implicites
- `BLOCKED`
  - contexte trop fragmenté pour produire un handoff fiable
- `UNKNOWN`
  - utilisé seulement si les sources disponibles sont trop contradictoires pour conclure proprement
