---
description: Execute a low-risk task in Vibebackbone quick mode
---

Handle this as a Vibebackbone QUICK task unless risk analysis proves otherwise: $@

Objective:
Execute a low-risk task quickly, proportionally, and cleanly.

Preferred Vibebackbone skills:

- `0-vbb-audit-readiness`
- `1-vbb-conventions`
- `1-vbb-formatter`
- `1-vbb-doc-harmonizer`

Skill routing rule:

- Use the first applicable skill in the list as the primary skill path.
- Use `0-vbb-audit-readiness` only as a gate if the task might drift out of QUICK.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. Restate the goal briefly.
2. Verify that the task still qualifies as QUICK.
3. State any relevant governance file if present.
4. Give a very short plan.
5. Execute.
6. If risk increases, stop and escalate immediately.

QUICK criteria:

- low-risk
- local
- reversible
- non-sensitive
- outside auth/data-contract/security/production concerns

Output format:

- Goal
- Why this is QUICK
- Governance used
- Primary skill used
- Supporting skills
- Fallback justification
- Plan
- Action
- Result
- Escalation needed: yes/no

---

## Alignement protocole agentique

**Phases correspondantes** : 01_INTAKE (implicite) + 05_EXECUTION

Ce prompt enchaîne le cadrage et l'exécution en une seule session. Adapté à la voie RAPIDE STANDARD uniquement.

Pour RAPIDE-ZERO et RAPIDE-MINIMAL, utiliser `0-p-vbb-zero-friction` à la place.

**Artefacts attendus** (RAPIDE STANDARD) :
- `docs/runs/YYYY-MM-DD_HHmm_slug/01_INTAKE.md` — objectif + classification RAPIDE (peut être minimal)
- `docs/runs/YYYY-MM-DD_HHmm_slug/05_PATCH_SUMMARY_RUN_01.md` — résumé des changements

Ces fichiers peuvent être courts. L'essentiel est qu'ils existent et soient nommés.

**Handoff vers 07_CLOSEOUT** :

En voie RAPIDE, la review est optionnelle. Après l'exécution :
- Si changement minimal → passer directement à `canonical/07-p-vbb-closeout` ou `t-p-vbb-session-handoff`
- Si changement sensible → créer une session `canonical/06-p-vbb-review`

**Escalade obligatoire** : si en cours d'exécution le risque augmente (auth, données, prod, sécurité) → arrêter immédiatement, documenter dans le patch summary, créer une nouvelle session en voie STRUCTURÉE ou AUDIT.
