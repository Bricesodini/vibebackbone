---
description: Execute a structured Vibebackbone task with explicit grounding
---

Handle this as a Vibebackbone STRUCTURED task: $@

Objective:
Execute a structured task with explicit grounding, plan, and controlled changes.

Preferred Vibebackbone skills:

- `t-vbb-dependency-mapper`
- `t-vbb-impact-analyzer`
- `t-vbb-test-coverage-mapper`
- `1-vbb-conventions`

Skill routing rule:

- Use the first applicable skill in the list as the primary skill path.
- Use `t-vbb-dependency-mapper`, `t-vbb-impact-analyzer`, `t-vbb-test-coverage-mapper`, and `1-vbb-conventions` only in that order of support.
- Manual fallback is allowed only if a named skill is genuinely absent from the current `[Skills]` list. If you fall back, name the missing skill and why.

Required process:

1. Restate the goal briefly.
2. Confirm why the task is STRUCTURED.
3. State which governance files are available and relevant.
4. Identify the artifact or change type.
5. If this is post-audit implementation, require a concrete finding / target before execution: id, file, skill, or behavior to fix.
6. For skill changes, read the relevant `skills/*/CONTRACT.yaml` and `skills/INDEX.yaml`; do not assume a root `CONTRACT.yaml` exists.
7. Treat `docs/AUDIT_STATUS.md` as the source of truth for the current audit state.
8. List pre-existing untracked files and leave them untouched unless they are explicitly in scope.
9. Produce a short but explicit plan.
10. Execute in a controlled way.
11. Summarize what changed and what remains open.

STRUCTURED triggers:

- data contracts
- authentication
- production state
- important multi-file behavior
- architecture-adjacent structure
- significant implementation flow

Constraints:

- Do not skip the plan.
- Do not claim canonical compliance without governance grounding.
- Keep the result aligned with project documentation.

Output format:

- Goal
- Why this is STRUCTURED
- Governance used
- Artifact type
- Primary skill used
- Supporting skills
- Fallback justification
- Plan
- Action
- Result
- Open points

---

## Alignement protocole agentique

**Phases correspondantes** : 01_INTAKE + 04_PLAN + 05_EXECUTION

Ce prompt enchaîne cadrage, planification et exécution en une session. Adapté à la voie STRUCTURÉE.

**Artefacts attendus** :
- `docs/runs/YYYY-MM-DD_HHmm_slug/01_INTAKE.md` — objectif reformulé + classification STRUCTURÉE
- `docs/runs/YYYY-MM-DD_HHmm_slug/04_FIX_PLAN.md` — plan produit avant exécution
- `docs/runs/YYYY-MM-DD_HHmm_slug/05_PATCH_SUMMARY_RUN_01.md` — résumé des changements

Créer ces trois fichiers dans le dossier de run. Si plusieurs runs : `05_PATCH_SUMMARY_RUN_02.md`, etc.

**Audit optionnel** : si en cours d'exploration un risque inattendu apparaît (sécurité, données, conformité) → interrompre, créer une session `canonical/02-p-vbb-audit`, et reprendre après le verdict.

**Handoff vers 06_REVIEW** :

Après exécution, ne pas reviewer soi-même. Créer une nouvelle session avec `canonical/06-p-vbb-review`.
Transmettre : `05_PATCH_SUMMARY_RUN_N.md` + liste des fichiers modifiés + points non résolus.

**Closeout sequence (à exécuter après approval)** :

1. `t-vbb-commit-ready` → verdict + message de commit conventionnel
2. `git add <fichiers>` → `git commit -m "<message>"` → `git push`
3. Mise à jour de `docs/SESSION.md` (vier ou noter l'état)
4. Mise à jour de `docs/CONTEXT.md` (statut, lien vers run, points ouverts)

> Ne pas s'arrêter après la review. La boucle n'est pas fermée tant que git push n'est pas fait. Pour STRUCTURED, le closeout formel est requis — produire `07_CLOSEOUT.md` avant de commiter.
