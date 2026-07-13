---
run_id: "2026-07-13_1902_v2r3-audits-scopes"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-code"
started_at: "2026-07-13T17:10:00Z"
ended_at: "2026-07-13T17:15:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "docs/adr/0028-scoped-audit-protocol.md (ACCEPTED)"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — v2r3-audits-scopes

## Objectif

Paramètre `scope` documenté pour janitor / tech-debt / db-robustness + protocole
d'itération canonique unique (inventaire → passes par scope → registre consolidé).
Réf. : ADR-0028 (ACCEPTED). Ferme AUDIT-A-001 / AUDIT-A-002.

## Pré-conditions

- Gate levé : `can_code_start=true`, ADR-0028 résolue par liaison stricte,
  `poc_required=false` (aucune hypothèse d'intégration).
- V2-R1 livré (hooks canoniques actifs — ce run passera par eux).

## Étapes ordonnées

| # | Action | Fichiers |
|---|--------|----------|
| 1 | Protocole canonique reference-only : rôle des scopes, inventaire par blocs ARCHITECTURE.md (défaut) ou chemins/labels, nommage des rapports, registre consolidé, règles d'itération | `docs/REFERENCE/scoped-audit-protocol.md` (nouveau) |
| 2 | Section « SCOPE PARAMETER » dans les 3 SKILL.md (comportement avec/sans scope, nommage `{skill}-{scope-slug}-{ts}.md`, tag scope par finding, renvoi au protocole) | `skills/1-vbb-code-janitor/SKILL.md`, `skills/1-vbb-tech-debt/SKILL.md`, `skills/2-vbb-db-robustness/SKILL.md` |
| 3 | Aligner le contrat db-robustness (`scope_filter` en input optionnel, comme les deux autres) | `skills/2-vbb-db-robustness/CONTRACT.yaml` |
| 4 | Rule 12 : impact 4 distributions + entrée Decisions log | `docs/DISTRIBUTIONS.md` |
| 5 | ARCHITECTURE : référencer le protocole dans le bloc adapté + RELATIONS régénéré | `docs/ARCHITECTURE.md`, `docs/RELATIONS.md` |
| 6 | Pre-merge gate P.R2 (5/5) + closeout CLOSE-FINAL + SESSION/ACTIVITY_LOG + commit/push | docs du run |

## Critères d'acceptation

- Les 3 SKILL.md documentent `scope` (optionnel, global par défaut, rétro-compatible)
  et citent `docs/REFERENCE/scoped-audit-protocol.md` (une seule source du protocole).
- `scope_filter` présent dans les 3 CONTRACT.yaml ; `vbb-contract-lint` 0 erreur.
- Le protocole définit : inventaire, passe par scope, registre consolidé, et la
  règle « 1 passe = 1 scope = 1 rapport » avec agrégation P0/P1.
- Pre-merge gate 5/5 PASS ; suite pytest inchangée (aucun outil Python modifié).

## Risques identifiés

- Dérive de duplication (protocole recopié dans les SKILL.md) : mitigé — les
  skills renvoient au chemin canonique, sections courtes (~25 lignes).
- Contrat db-robustness : modification YAML → validée par `vbb-contract-lint`.
- Coût tokens des passes multiples : assumé (décision ADR-0028, c'est l'objectif).

## Rollback

Additif et rétro-compatible (défaut = comportement actuel). `git revert` du commit du run.
