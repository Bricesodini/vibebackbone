---
run_id: "2026-07-13_1902_v2r3-audits-scopes"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-code"
started_at: "2026-07-13T17:02:00Z"
ended_at: "2026-07-13T17:10:00Z"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/audits/audit-A-scope-aware-janitor-20260712-1210.md"
  - "docs/strategy/vbb-improvements-roadmap/03_PLAN_REDUCTION_V2.md"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — v2r3-audits-scopes

## Demande reçue

> GO Brice (2026-07-13) sur la roadmap V2 — V2-R3 « Audits scopés » : paramètre
> `scope` pour `1-vbb-code-janitor`, `1-vbb-tech-debt`, `2-vbb-db-robustness` +
> protocole d'itération par petits scopes (inventaire → passes → registre
> consolidé). Demande de fond exprimée par Brice : « les scopes sont souvent très
> larges […] faire plusieurs janitor ou audit dette technique, db-health avec
> plusieurs itérations avec des petits scopes (avoir le choix de la granularité) ».

## Reformulation

Donner aux trois skills anti-slop un paramètre `scope` documenté (global par
défaut, périmètre restreint sur demande) et un protocole d'itération canonique
unique pour enchaîner des passes par petit scope et consolider les verdicts.
Ferme AUDIT-A-001 et AUDIT-A-002 (orphelins de l'ancienne roadmap).

## Scope

### Dans le périmètre
- `skills/1-vbb-code-janitor/SKILL.md` — section « Scope parameter » (le CONTRACT.yaml expose déjà `scope_filter` optionnel, jamais documenté dans le prompt)
- `skills/1-vbb-tech-debt/SKILL.md` — idem (`scope_filter` déjà dans le CONTRACT.yaml)
- `skills/2-vbb-db-robustness/SKILL.md` + `CONTRACT.yaml` — idem, avec ajout de `scope_filter` aux inputs optionnels du contrat
- `docs/REFERENCE/scoped-audit-protocol.md` (nouveau, reference-only) — protocole d'itération : inventaire des scopes → passes successives → registre consolidé ; source unique citée par les 3 skills (pas de duplication)
- `docs/DISTRIBUTIONS.md` §7 — check d'impact Core→4 distributions (Rule 12)

### Hors périmètre
- AUDIT-A-003 / A-004 (bloc `external`, registre hors-repo) — backlog
- Aucun nouvel élément de catalogue (moratoire V2 : le paramètre `scope` est l'exception unique déclarée)
- Aucun canon (CONVENTIONS/PILOTAGE intacts — le protocole est `reference-only`, comme `pre-merge-gate.md`)
- Aucun changement des autres skills Phase 1 (monolith-detector, etc.) — extension ultérieure si le protocole fait ses preuves

### Dépendances détectées
- ADR : `docs/adr/0028-scoped-audit-protocol.md`
- Inventaire de scopes : blocs de `docs/ARCHITECTURE.md` (9 blocs) comme source par défaut, chemins/labels métier acceptés

## Classification du risque

- **Niveau** : `MODÉRÉ`
- **Justification** : modifie le contrat de trois skills du catalogue (surface
  consommée par les quatre agents) ; additif et rétro-compatible (défaut = global,
  comportement actuel). Route STRUCTURED avec gate ADR+POC+intégration.
