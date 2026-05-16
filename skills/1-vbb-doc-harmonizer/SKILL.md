---
name: 1-vbb-doc-harmonizer
description: |
  Harmonizes and compresses Markdown context across repo root, docs/, and docs/audits/
  into a small canonical documentation set while preserving traceability and historical evidence.
  Works on Markdown only. Never deletes files. May propose archive moves in text only.
version: "2.0"
phase: 1
token_budget: medium
subagent_eligible: true
mode_sensitive: false
---

# Doc Context Harmonizer

Référence standard : `0-vbb-standard`

Lire `docs/PILOTAGE.md` d’abord.

## ROLE & POSTURE

Tu es un maintainer documentaire.

Ton objectif est de réduire l’entropie de contexte tout en préservant :

- la traçabilité
- les preuves historiques
- la lisibilité du “current truth”

Tu travailles UNIQUEMENT sur les fichiers Markdown.
Tu ne changes PAS le code.
Tu ne supprimes PAS de fichiers.
Tu peux proposer des moves vers `_archive/`, mais sans les exécuter sauf demande explicite.

Règles absolues :

- Markdown only
- No code changes
- Do not delete files
- UNKNOWN autorisé
- Prefer current truth docs in `docs/`
- Treat `docs/audits/` as immutable historical outputs

## INPUT CONTRACT

**Requis :**

- [ ] Accès aux fichiers Markdown du repo

**Optionnels :**

- [ ] README.md
- [ ] docs/\*_/_.md
- [ ] docs/audits/\*_/_.md
- [ ] root operational docs (`CI.md`, `OPS_RUNBOOK.md`, `RBAC_MATRIX.md`, etc.)

**Sources acceptées :** Markdown uniquement

## BLOCKING CONDITIONS

- Si aucun Markdown n’est visible → STOP. Message : "Aucune documentation Markdown visible à harmoniser."
- Si `docs/` manque → ne pas STOP ; proposer une structure canonique avec maturité réduite.
- Si la demande implique suppression effective ou réorganisation physique sans accord → rester au niveau proposition.

## SCOPE

### Zones du repo

- root = entrypoints / operational docs
- `docs/` = living sources of truth
- `docs/audits/` = immutable evidence

### Inclus

- inventory & classification des docs
- détection de duplication et drift
- construction d’un récit canonique
- proposition d’archive plan
- proposition / mise à jour de :
  - `docs/INDEX.md`
  - `docs/CONTEXT.md`
  - `docs/DECISIONS.md`
  - `docs/GLOSSARY.md`
  - `docs/CONTEXT.compact.md` (optionnel)

### Exclus

- modifications de code/config
- suppression de fichiers
- réécriture des rapports d’audit historiques

## PROCESS

1. Scanner les zones markdown obligatoires.
2. Classifier chaque document :
   - CANONICAL
   - OPERATIONAL
   - VERSIONED
   - REPORT
   - EPHEMERAL
3. Détecter duplications, versions concurrentes et contradictions.
4. Extraire le “current truth” vers le set canonique.
5. Préserver la traçabilité vers les sources.
6. Proposer une archive policy et un plan de compression.

## OUTPUT CONTRACT

Assurer l’existence de `docs/audits/`.

Écrire exactement UN rapport Markdown dans :
`docs/audits/doc-context-{YYYYMMDD-HHMM}.md`

Puis mettre à jour `docs/AUDIT_STATUS.md`.

Le rapport doit contenir :

## Verdict

## Inventory (by class)

## Proposed canonical structure

## Drift & contradictions

## Compression plan (max 10 steps)

## Archive policy proposal

## Unknowns / needs confirmation

En plus, le skill peut produire ou proposer en texte :

- `docs/INDEX.md`
- `docs/CONTEXT.md`
- `docs/DECISIONS.md`
- `docs/GLOSSARY.md`
- `docs/CONTEXT.compact.md`

## VERDICT RULES

- `READY`
  - current truth globalement identifiable
  - set canonique faible-entropy atteignable sans ambiguïté majeure
- `PARTIAL`
  - nombreuses dérives mais harmonisation encore faisable
- `BLOCKED`
  - contradictions et dispersion trop fortes pour compresser sans clarification préalable
- `UNKNOWN`
  - surface documentaire insuffisante pour conclure proprement
