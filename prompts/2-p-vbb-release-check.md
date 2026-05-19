---
description: Pre-release gate — full product quality audit before shipping to production
---

Évalue si le produit est prêt à être livré en production pour : $@

## Objectif

Le dernier verrou avant de shipper. Ce prompt exécute une vérification
complète de la readiness produit : sécurité, intégrité, ops, légal,
performance, accessibilité, documentation — et donne un GO / NO-GO clair.

C'est le "dernier regard" de l'architecte produit avant livraison.

## Preferred Vibebackbone skills

- `2-vbb-security`
- `2-vbb-systemic-risk`
- `2-vbb-data-integrity`
- `2-vbb-db-robustness`
- `2-vbb-ops`
- `2-vbb-ci`
- `2-vbb-legal`
- `2-vbb-api-auditor`
- `2-vbb-performance`
- `2-vbb-accessibility`
- `2-vbb-analytics`
- `2-vbb-spec-validator`
- `t-vbb-mode-transition-gate`
- `3-vbb-risk-register`

## Skill routing and chaining rule

### Wave 1 — Sécurité & Risques (obligatoire)

Lancer en séquence :

1. `2-vbb-security` — audit de sécurité
2. `2-vbb-systemic-risk` — risques systémiques
3. `2-vbb-data-integrity` — intégrité des données

Si l'un des trois est BLOCKED → NO-GO immédiat.

### Wave 2 — Infrastructure & Ops (obligatoire)

Lancer en séquence : 4. `2-vbb-db-robustness` — robustesse base de données 5. `2-vbb-ops` — readiness opérationnelle 6. `2-vbb-ci` — CI/CD 7. `2-vbb-legal` — conformité légale

### Wave 3 — Qualité produit (obligatoire)

Lancer en parallèle : 8. `2-vbb-api-auditor` — audit API (si applicable) 9. `2-vbb-performance` — performance 10. `2-vbb-accessibility` — accessibilité (si UI) 11. `2-vbb-analytics` — instrumentation 12. `2-vbb-spec-validator` — conformité spec

### Wave 4 — Transition & Consolidation (obligatoire)

13. `t-vbb-mode-transition-gate` — prêt pour PROD ?
14. `3-vbb-risk-register` — registre de risques consolidé

## Required process

1. **Restate** le produit et la release cible.
2. **Wave 1** — Sécurité & risques.
3. **Wave 2** — Infrastructure & ops.
4. **Wave 3** — Qualité produit.
5. **Wave 4** — Transition & consolidation.
6. **Verdict final** : GO / CONDITIONAL_GO / NO_GO.

## Verdict rules

### GO 🟢

- Tous les audits Wave 1 : READY
- Tous les audits Wave 2 : READY ou PARTIAL (avec PARTIAL documentés et acceptés)
- Tous les audits Wave 3 : READY, PARTIAL, ou ADEQUATE
- Mode-transition-gate : READY
- Risk-register : pas de P0 non traité

### CONDITIONAL_GO 🟡

- Wave 1 : READY ou PARTIAL (pas de BLOCKED)
- Wave 2 : au moins un PARTIAL avec risque accepté
- Wave 3 : écarts documentés et plan de remédiation post-release
- Mode-transition-gate : PARTIAL avec acceptation documentée
- L'architecte produit accepte explicitement les risques résiduels

### NO_GO 🔴

- Un BLOCKED dans Wave 1 ou Wave 2
- Mode-transition-gate : BLOCKED
- Risk-register contient des P0 non résolus
- L'architecte refuse de signer les risques résiduels

## Output format

- **Produit / Release**
- **Wave 1 — Sécurité** : security verdict, systemic-risk verdict, data-integrity verdict
- **Wave 2 — Infrastructure** : db-robustness, ops, ci, legal verdicts
- **Wave 3 — Qualité** : api-auditor, perf, a11y, analytics, spec-validator verdicts
- **Wave 4 — Transition** : mode-transition verdict, risque register summary
- **Verdict final** : GO / CONDITIONAL_GO / NO_GO
- **Risques acceptés** : liste si CONDITIONAL_GO
- **Blocages** : liste si NO_GO
- **Prochaine action** : déployer / corriger puis re-check / escalader

---

## Alignement protocole agentique

**Phases correspondantes** : 02_AUDIT (waves 1–3) + 03_DECISION (wave 4 + verdict)

Ce prompt orchestre 14 skills en 4 waves dans une seule session. C'est le prompt le plus lourd du catalogue.

**⚠️ Avertissement de contexte** : si le contexte LLM disponible est inférieur à 200K tokens, ou si le repo est large (>50 fichiers actifs), préférer une exécution par wave dans des sessions séparées :

| Wave | Session dédiée | Prompt canonique |
|------|---------------|-----------------|
| Wave 1 | Session 1 | `canonical/02-p-vbb-audit` + skills security, systemic-risk, data-integrity |
| Wave 2 | Session 2 | `canonical/02-p-vbb-audit` + skills db-robustness, ops, ci, legal |
| Wave 3 | Session 3 | `canonical/02-p-vbb-audit` + skills api-auditor, perf, a11y, analytics, spec-validator |
| Wave 4 | Session 4 | `canonical/03-p-vbb-decision` + mode-transition-gate + risk-register |

**Artefacts attendus** :
- `docs/runs/YYYY-MM-DD_HHmm_slug/02_AUDIT_REPORT.md` — rapport consolidé des waves 1–3
- `docs/runs/YYYY-MM-DD_HHmm_slug/03_DECISION_RECORD.md` — verdict GO/CONDITIONAL_GO/NO_GO + risques acceptés
- `docs/audits/release-check-YYYYMMDD-HHMM.md` — rapport horodaté persistant

**Handoff après verdict** :

- Si GO → créer session `canonical/05-p-vbb-execution` ou procéder au déploiement
- Si CONDITIONAL_GO → créer session `canonical/03-p-vbb-decision` pour documenter les risques acceptés, puis déployer
- Si NO_GO → créer session `canonical/04-p-vbb-plan` pour planifier les corrections, puis re-lancer ce prompt
