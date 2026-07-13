---
run_id: "2026-07-13_1717_global-debt-janitor-doc"
phase: "02_AUDIT"
voie: "AUDIT"
status: "PARTIAL"
agent: "codex"
started_at: "2026-07-13T17:20:00+02:00"
ended_at: "2026-07-13T17:36:00+02:00"
next_phase: "03_DECISION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "docs/CONVENTIONS.md"
  - "docs/TECH_DEBT.md"
artifacts_produced:
  - "02_AUDIT.md"
  - "docs/audits/tech-debt-20260713-1728.md"
  - "docs/audits/code-janitor-20260713-1730.md"
  - "docs/audits/code-doc-coherence-20260713-1734.md"
---

# 02_AUDIT — Global maintainability pass

## Verdict global

`PARTIAL` — architecture, contrats, tests et distributions sont lisibles et
verts, mais cinq zones P1 empêchent de qualifier le framework de
maintenance-ready : sélection du run, installation des hooks, portabilité,
executor non caractérisé et liens actifs cassés.

## Rapports

| Passage | Verdict | Résultat principal |
|---|---|---|
| Dette technique | `PARTIAL` | 7 findings, dont 5 P1 bornés |
| Code Janitor | `PARTIAL` | 7 findings ; 25 erreurs Ruff autofixables, signaux structurels isolés |
| Conventions | `PARTIAL` | canon clair, 4 familles de drift mesurées |
| Code↔documentation | `PARTIAL` | 21 écarts groupés, 22 liens actifs actionnables |

## Conventions review

`docs/CONVENTIONS.md` reste la source canonique et n'est pas modifié : toute
évolution exige une proposition et validation humaine. La passe constate :

| ID | Convention | État mesuré | Verdict |
|---|---|---|---|
| CONV-01 | Fonctions ≈20 lignes, décomposer >40 | 36 fonctions >40 lignes dans 13 outils | drift P1 |
| CONV-02 | Naming selon langage | Python dominant `snake_case`, canon `camelCase` ambigu ; `write_closEOUT` atypique | drift P2 |
| CONV-03 | Prompts English-only | 8 prompts portent des marqueurs FR | drift P1 |
| CONV-04 | Traçabilité/liens | 22 liens actifs cassés après exclusions | drift P1 |
| CONV-05 | Architecture source unique | lint 9 blocs, 0/0 ; RELATIONS générée | conforme |
| CONV-06 | Tests algorithmic | pytest 133/1, tests déterministes | conforme |
| CONV-07 | Canon change discipline | ADR 0026 et gate préalable | conforme |

Le document canonique couvre bien principes, décisions et références, mais ne
contient pas de `Drift checklist`, `Migration plan` ni `Unknowns` explicites au
format du skill. Ajouter ces sections serait un changement canonique, donc une
proposition séparée — pas une correction implicite dans cet audit.

## Evidence matrix

| Claim | Evidence | Status |
|---|---|---|
| Baseline fonctionnelle stable | `pytest tests/ -q` → 133 passed, 1 skipped | VERIFIED_FINDING |
| Architecture/contrats cohérents | linters → 0 erreur, 0 warning | VERIFIED_FINDING |
| Gate auto-latest défectueux | loop-closure sans run → ancien run + FAIL | VERIFIED_FINDING |
| Qualité optionnelle non baselinée | Ruff 36, format 26, mypy 48/8 | VERIFIED_FINDING |
| Documentation active cassée | scanner 137 docs / 202 liens / 24 cassés, 22 actionnables | VERIFIED_FINDING |
| Skills et contrats exhaustifs | 64 SKILL.md / 64 CONTRACT.yaml / index 64 | VERIFIED_FINDING |

## Priorités proposées

1. **P1-A — Gate truth** : corriger l'auto-sélection loop-closure et la couvrir.
2. **P1-B — Hook truth** : unifier l'installateur des hooks locaux.
3. **P1-C — Portabilité + liens** : remplacer chemins machine et réparer les
   22 liens actifs.
4. **P1-D — Executor safety** : tests de caractérisation avant Janitor/typing.
5. **P1-E — Status truth** : réconcilier QOA/TECH_DEBT avec les mesures.
6. **P2-A — Safe Janitor** : Ruff safe fixes, puis formatage séparé.
7. **P2-B — Type debt** : mypy module par module, sans gate prématuré.

## Limites

- L'audit n'a modifié ni code, ni canon, ni fichiers utilisateur préexistants.
- Les fichiers non suivis ont été identifiés comme état local, pas analysés comme
  source canonique.
- Les archives/runs historiques ne sont pas soumis aux exigences de fraîcheur.

```yaml
FINAL_STATUS:
  elapsed_seconds: 960
  budget_initial: 180
  progress_emitted: true
  progress_count: 1
  extension_requested: false
  timeout_closeout_emitted: false
  verdict: COMPLETE
  files_touched:
    - docs/runs/2026-07-13_1717_global-debt-janitor-doc/02_AUDIT.md
    - docs/audits/tech-debt-20260713-1728.md
    - docs/audits/code-janitor-20260713-1730.md
    - docs/audits/code-doc-coherence-20260713-1734.md
  tests_run:
    - pytest tests/ -q
    - ruff check tools tests
    - ruff format --check tools tests
    - mypy tools --ignore-missing-imports
    - python tools/vbb-architecture.py lint
    - python tools/vbb-contract-lint.py
  tests_missing:
    - executor direct tests
  risks:
    - GMA-001
    - GMA-002
    - GMA-003
    - GMA-004
  open_points:
    - remediation runs require separate authorization/scope
```
