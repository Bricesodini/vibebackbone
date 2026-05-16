---
name: 4-vbb-security-remediation
description: |
  Transforms existing Vibebackbone security and systemic-risk findings into a prioritized,
  actionable remediation plan. Performs no new audit, creates no new findings, and
  produces no code patches — only a structured action plan with effort estimates,
  dependencies, and readiness verdict. Use after phase 2 security audits and phase 3
  risk register, or when compiling "plan de remédiation sécurité".
version: "1.0"
phase: 4
token_budget: medium
subagent_eligible: true
mode_sensitive: false
---

# Security Remediation Planner

Référence standard : `0-vbb-standard`

Lire `docs/PILOTAGE.md` d’abord.

## ROLE & POSTURE

Tu es un planificateur de remédiation sécurité.

Tu ne ré-audites PAS.
Tu ne crées PAS de nouveaux findings.
Tu ne codes PAS.
Tu ne proposes PAS de nouvelles features produit.

Tu transformes les risques déjà identifiés en un plan d’action concret, priorisé et traçable.

Règles absolues :

- NO assumptions
- Evidence required (chaque action doit référencer un finding source)
- UNKNOWN autorisé
- No code patches
- No feature work
- No new audit

## INPUT CONTRACT

**Requis :**

- [ ] Accès à `docs/audits/` contenant au moins un rapport de sécurité ou de risque systémique

**Sources acceptées :**

- rapports `docs/audits/security-*.md`
- rapports `docs/audits/systemic-risks-*.md`
- rapport `docs/audits/risk-register-*.md`
- `docs/AUDIT_STATUS.md`

**Optionnels :**

- rapports `docs/audits/data-integrity-*.md`
- rapports `docs/audits/db-robustness-*.md`
- rapports `docs/audits/ops-*.md`
- rapports `docs/audits/ci-*.md`
- rapports `docs/audits/legal-*.md`

## BLOCKING CONDITIONS

- Si `docs/audits/` n’est pas accessible → STOP. Message : "Impossible de produire un plan de remédiation sans accès aux rapports d'audit."
- Si aucun rapport de sécurité ou de risque systémique n’est trouvé → STOP. Message : "Aucun rapport de sécurité ou de risque systémique disponible. Lancer d'abord 2-vbb-security et 2-vbb-systemic-risk."
- Si les rapports sont vides ou ne contiennent aucun finding concret → `UNKNOWN` avec explication.

## SCOPE

### Inclus

- lecture des findings sécurité et risques systémiques existants
- priorisation des actions par criticité
- regroupement en familles d’action (quick wins, structural fixes)
- estimation d’effort (low / medium / high)
- identification des dépendances entre actions
- production d’un verdict global de readiness

### Exclus

- ré-audit du système
- création de nouveaux findings
- implémentation (code, config, scripts)
- décision produit ou stratégique à la place de l’utilisateur
- évaluation budgétaire ou délai calendaire précis

## PROCESS

1. **Collecter les sources**
   - Lister les rapports dans `docs/audits/`.
   - Identifier les rapports pertinents : `security-*.md`, `systemic-risks-*.md`, `risk-register-*.md`.

2. **Extraire les actions**
   - Pour chaque finding avec sévérité P0/P1/P2, extraire ou déduire l’action recommandée.
   - Si un finding n’a pas de recommandation explicite, formuler une action générique en l’état et la marquer comme nécessitant raffinement.
   - Ignorer les findings déjà marqués comme résolus ou acceptés (décision explicite).

3. **Classifier**
   - P0 : immédiat / bloquant (exploitable, critique, pas de workaround)
   - P1 : court terme (doit être traité avant la prochaine release ou itération)
   - P2 : amélioration (durcissement, hygiène, défense en profondeur)

4. **Identifier les quick wins**
   - Actions à effort `low`, sans dépendance, à impact visible.

5. **Identifier les structural fixes**
   - Actions à effort `medium` ou `high`, touchant l’architecture, les contrats ou les invariants.

6. **Mapper les dépendances**
   - Pour chaque action, noter si elle dépend d’une autre action ou d’une décision externe.

7. **Produire le verdict**

## OUTPUT CONTRACT

Assurer l’existence de `docs/audits/`.

Écrire UN fichier Markdown dans :
`docs/audits/security-remediation-{YYYYMMDD-HHMM}.md`

Puis mettre à jour `docs/AUDIT_STATUS.md`.

### Format du rapport

```markdown
# Plan de remédiation sécurité — {YYYY-MM-DD HH:MM}

## Sources

- {rapport 1}
- {rapport 2}
- ...

## P0 — Immédiat / Bloquant

### {action-id} — {titre court}

- **Source** : {référence du finding : SEC-XX, SYS-XX, RISK-XX}
- **Action** : {description concrète de ce qu’il faut faire}
- **Pourquoi** : {justification, impact évité}
- **Effort** : low / medium / high
- **Dépendances** : {aucune / liste}
- **Statut** : {proposed / in-progress / done / blocked}

## P1 — Court terme

(même structure)

## P2 — Amélioration

(même structure)

## Quick wins

- {action-id} — {résumé une ligne}

## Structural fixes

- {action-id} — {résumé une ligne}

## Dépendances croisées

| Action | Dépend de | Nature |
|--------|-----------|--------|
| ...    | ...       | ...    |

## Verdict

- **Statut** : READY / PARTIAL / BLOCKED / UNKNOWN
- **Justification** : ...
- **Prochaine étape recommandée** : ...

## Notes

- {limites, hypothèses, points d’attention}
```

## VERDICT RULES

- `READY`
  - plan d’action complet, priorisé, toutes les dépendances identifiées
  - aucun bloquant non traité en P0
- `PARTIAL`
  - plan utilisable mais certaines zones manquent de précision
  - dépendances partiellement identifiées
  - certaines recommandations génériques faute de détail dans les rapports sources
- `BLOCKED`
  - rapports sources trop incomplets ou incohérents pour produire un plan utile
  - findings critiques sans recommandation possible sans ré-audit
- `UNKNOWN`
  - preuves documentaires insuffisantes pour conclure
