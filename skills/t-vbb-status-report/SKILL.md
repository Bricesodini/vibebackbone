---
name: t-vbb-status-report
description: |
  Produces a compact status report from audit artifacts and session context.
  Use when an agent needs to emit a short, actionable report. Minimal skill
  designed to be called by events.on_success.
version: "0.1"
phase: 4
token_budget: low
subagent_eligible: false
mode_sensitive: false
---

# Status Report

Référence standard : `0-vbb-standard`

## ROLE & POSTURE

Tu es un rédacteur de rapport condensé.

Ton rôle est de produire un bilan court et actionnable à partir d'artefacts sources.

Tu ne fais PAS d'audit.
Tu ne fais PAS de recommandations longues.
Tu restitues l'état connu de manière lisible.

## INPUT CONTRACT

**Requis :**

- [ ] Un ou plusieurs artefacts sources (rapports d'audit, contexte, bilans)

**Optionnels :**

- [ ] `docs/SESSION.md`
- [ ] `docs/AUDIT_STATUS.md`

## OUTPUT CONTRACT

### Artefact propre : aucun

- **`outputs.artifact: null`** dans le contrat.
- Status-report produit un rapport inline conversationnel, pas de fichier.
- Sa sortie est typiquement intégrée dans le `07_CLOSEOUT.md` actif par
  le skill qui le chaîne (`t-vbb-session-handoff`, `t-vbb-mode-transition-gate`).

### Contenu obligatoire de la sortie inline

- État global : `PASS` / `PARTIAL` / `FAIL` / `BLOCKED`
- Résumé : 2-3 lignes max
- Findings clés : liste bornée
- Prochaine action explicite

## VERDICT RULES

- `PASS` — tous les signaux sont au vert
- `PARTIAL` — quelques points ouverts mais rien de bloquant
- `FAIL` — anomalies critiques identifiées
- `BLOCKED` — pas assez d'évidence pour conclure