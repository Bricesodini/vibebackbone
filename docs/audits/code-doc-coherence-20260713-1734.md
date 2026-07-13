---
date: 2026-07-13
scope: active tracked code and documentation
skill: 1-vbb-code-doc-coherence-auditor
verdict: PARTIAL
---

# Code-Doc Coherence Audit

## Context

- **Date** : 2026-07-13
- **Scope** : dépôt suivi ; docs racine, `docs/*.md`, `docs/REFERENCE/`, skills,
  prompts et README de distributions. Archives, audits et runs historiques sont
  inventoriés comme historique mais exclus des claims de fraîcheur.
- **Refactored zones** : retrait Hermes, setup/distributions, hooks et gates.
- **Skill** : `1-vbb-code-doc-coherence-auditor` v1.0

## Global verdict

**PARTIAL**

La majorité des paires Core↔docs est cohérente, notamment architecture,
contrats, setup et quatre adaptateurs. Des liens cassés et statuts actifs
obsolètes touchent toutefois le boot, les skills de maintenance et les gates.

## Quantitative summary

| Category | HIGH | MEDIUM | LOW | Total |
|---|---:|---:|---:|---:|
| MISSING | 0 | 3 | 2 | 5 |
| OBSOLETE | 3 | 4 | 0 | 7 |
| STALE | 2 | 4 | 1 | 7 |
| REDUNDANT | 0 | 1 | 0 | 1 |
| ORPHAN | 0 | 1 | 0 | 1 |
| **Total** | **5** | **13** | **3** | **21** |

Le scanner a parcouru 137 documents actifs, 202 liens locaux et détecté 24
liens non résolus, dont 22 actionnables après exclusion d'un placeholder de
template et d'un lien dans la mémoire locale `SESSION.md`.

## Code inventory

| ID | Name | Path | Type | Surface | Refactoring priority |
|---|---|---|---|---|---|
| U-001 | Setup router | `setup.sh`, `setup-lib.sh`, `core/setup.sh` | script | CLI install/uninstall/dry-run | yes |
| U-002 | Architecture tool | `tools/vbb-architecture.py` | script | lint/graph | no |
| U-003 | Context compactor | `tools/vbb-context-compactor.py` | script | compact run | no |
| U-004 | Contract lint | `tools/vbb-contract-lint.py` | script | lint contracts | no |
| U-005 | Contract runtime | `tools/vbb-contract-runtime.py` | script | run/test-all/validate | no |
| U-006 | Executor | `tools/vbb-executor.py` | module/CLI | state machine and artifact writes | yes |
| U-007 | Gate check | `tools/vbb-gate-check.py` | script | ADR/POC integration gate | yes |
| U-008 | Index | `tools/vbb-index.py` | script | build/search/status | no |
| U-009 | LLM healthcheck | `tools/vbb-llm-healthcheck.py` | script | provider checks | no |
| U-010 | Loop closure | `tools/vbb-loop-closure-check.py` | script | phase invariant | yes |
| U-011 | Multi-service lint | `tools/vbb-multiservice-lint.py` | script | 3 rules | no |
| U-012 | Phase router | `tools/vbb-phase-router.py` | script | route selection | no |
| U-013 | Project init | `tools/vbb-project-init.py` | script | scaffold/install hook | yes |
| U-014 | Review-tier POC | `tools/vbb-review-threshold-poc.py` | experimental script | advisory tier | no |
| U-015 | Status dashboard | `tools/vbb-status-dashboard.py` | script | current health | yes |
| U-016 | Framework hooks | `scripts/hooks/` | script/contract | pre-commit + commit-msg | yes |
| U-017 | Hook installers | `scripts/install-*.sh` | script | local Git install | yes |
| U-018 | Claude adapter | `distributions/claude/` | feature | Claude setup | yes |
| U-019 | Codex adapter | `distributions/codex/` | feature | Codex setup | yes |
| U-020 | Pi adapter | `distributions/pi/` | feature | Pi setup | yes |
| U-021 | OpenCode adapter | `distributions/opencode/` | feature | OpenCode setup | yes |
| U-022 | Skills catalog | `skills/*/{SKILL.md,CONTRACT.yaml}` | contract catalog | 64 skills | no |
| U-023 | Prompt library | `prompts/` | command catalog | 33 prompts | no |
| U-024 | LLM configuration | `config/local_llm_models.yaml` | config | local provider matrix | no |

Total: 24 unités documentables regroupant toute la surface exécutable suivie.

## Documentation inventory

| ID | File | Title | Type | Intent | Code refs |
|---|---|---|---|---|---|
| D-001 | `README.md` | Product entry | guide | standalone/code-linked | setup, distributions, tools |
| D-002 | `GUIDE.md` | Operational guide | guide | code-linked | gates, setup, tools |
| D-003 | `AGENTS.md`, `SYSTEM.md` | Boot grammar | governance | code-linked | prompts, gate, P.R2 |
| D-004 | `docs/CONTEXT.md` | Persistent router | architecture | standalone | canonical docs/ADRs |
| D-005 | `docs/PILOTAGE.md` | Route canon | governance | code-linked | gate and routes |
| D-006 | `docs/ARCHITECTURE.md`, `docs/RELATIONS.md` | Architecture | architecture | code-linked | tools/distributions/tests |
| D-007 | `docs/CONVENTIONS.md` | Quality canon | governance | code-linked | linters/tests/review |
| D-008 | `docs/RUNBOOK.md`, `docs/DEPLOYMENT.md` | Operations | runbook | code-linked | setup/gates |
| D-009 | `docs/DISTRIBUTIONS.md`, `distributions/*/README.md` | Adapters | feature | code-linked | four setup scripts |
| D-010 | `docs/AUDIT_STATUS.md`, `docs/TECH_DEBT.md` | Status | other | code-linked | tests/tools/risks |
| D-011 | `docs/INDEX.md`, `skills/INDEX.yaml` | Catalogs | glossary | code-linked | docs/skills/contracts |
| D-012 | `docs/REFERENCE/pre-merge-gate.md` | P.R2 | runbook | code-linked | CI/tool commands |
| D-013 | `docs/LLM_PROVIDERS.md` | Provider config | config | code-linked | LLM config/tool |
| D-014 | `docs/runs/`, `docs/audits/`, `docs/adr/` | Historical evidence | decision/audit | standalone | snapshots at date |
| D-015 | `skills/*/SKILL.md` | Skill manuals | module | code-linked | contracts/prompts/gates |
| D-016 | `prompts/` | Entrypoints | guide | code-linked | phases/skills |

Total: 16 familles documentaires, 533 fichiers Markdown suivis.

## Detected discrepancies

### MISSING — Code without documentation

| ID | Code unit | Path | Type | Severity | Priority | Note |
|---|---|---|---|---|---|---|
| M-01 | Executor test contract | `tools/vbb-executor.py` | module | MEDIUM | yes | documenté architecturalement, mais aucune doc de comportement/test de caractérisation |
| M-02 | Hook installation truth | `scripts/install-*.sh` | scripts | MEDIUM | yes | aucune procédure active ne tranche quel installateur est canonique |
| M-03 | LLM healthcheck operations | `tools/vbb-llm-healthcheck.py` | script | MEDIUM | no | skill/config existent, RUNBOOK ne décrit pas résultat/échecs |
| M-04 | Multi-service lint operations | `tools/vbb-multiservice-lint.py` | script | LOW | no | ADR/strategy disponibles, peu de doc active opérateur |
| M-05 | Review threshold POC | `tools/vbb-review-threshold-poc.py` | script | LOW | no | correctement advisory, mais uniquement documenté dans stratégie POC |

### OBSOLETE — Obsolete documentation

| ID | Document | Broken reference | Severity | Note |
|---|---|---|---|---|
| O-01 | `SYSTEM.md` | `../docs/REFERENCE/pre-merge-gate.md` | HIGH | depuis la racine, le lien sort du dépôt |
| O-02 | 5 skills Phase 1 | `../../../prompts/...` et `../../../REFERENCE/...` | HIGH | 15 liens cassés dans conventions, janitor, tech-debt, formatter, monolith |
| O-03 | `docs/CONTEXT.md` | `docs/adr/0002...`, `docs/adr/0003...` | HIGH | préfixe `docs/` dupliqué depuis `docs/` |
| O-04 | `docs/SESSION_RULES.md` | `../templates/07_CLOSEOUT.md.template` | MEDIUM | devrait rester sous `docs/templates/` |
| O-05 | `docs/CONVENTIONS.md` | `../REFERENCE/pre-merge-gate.md` | MEDIUM | une occurrence correcte coexiste avec une occurrence cassée |
| O-06 | `docs/AUDIT_STATUS.md` | `../audits/...` ×2 | MEDIUM | références sortent de `docs/` |
| O-07 | boot/runbook | `~/02_Dev` et `/Users/bot` | MEDIUM | chemins existants seulement sur certaines machines |

### STALE — Out-of-sync documentation

| ID | Document | Code unit | Divergence | Severity | Note |
|---|---|---|---|---|---|
| S-01 | `docs/AUDIT_STATUS.md` QOA-003 | loop closure | marqué resolved, reproduction FAIL | HIGH | source active contredit exécutable |
| S-02 | install scripts/comments | hooks | coexistence décrite mais activation Git incomplète | HIGH | nom non standard non exécuté automatiquement |
| S-03 | `docs/LONG_RUN_RULE.md` | pilotage | déclare le détail skill comme source canonique | MEDIUM | `docs/PILOTAGE.md` est canon |
| S-04 | `docs/AUDIT_STATUS.md` QOA-008 | architecture/tests | reste Open | MEDIUM | bloc distribution-setup + smoke présents |
| S-05 | `docs/AUDIT_STATUS.md` compteurs | tests/contracts/prompts | plusieurs snapshots dans surface active | MEDIUM | contexte courant 133/1, inventaire 64/64/33 |
| S-06 | `docs/TECH_DEBT.md` TD-001/TD-003 | env/runs | hypothèses anciennes | MEDIUM | PyYAML installé ; contexte ne liste plus les deux runs |
| S-07 | `docs/CONVENTIONS.md` | Python/prompts | camelCase ambigu + English-only non respecté | LOW | code Python snake_case, 8 prompts avec marqueurs FR |

### REDUNDANT — Redundant documentation

| ID | Documents | Overlap | Severity | Note |
|---|---|---|---|---|
| R-01 | `scripts/install-framework-gate-hook.sh`, `scripts/install-vbb-pre-commit.sh` | contrat d'installation concurrent | MEDIUM | ce n'est pas seulement documentaire : deux vérités opérationnelles |

### ORPHAN — Documentation without code

| ID | Document | Doc type | Intent | Severity | Note |
|---|---|---|---|---|---|
| P-01 | `docs/runs/routing-fix-verification.md` | verification | unclear/pending | MEDIUM | artefact loose, toujours PENDING, suivi par QOA-006 |

## Action recommendations

| Priority | Action | Targeted discrepancies | Recommended skill | Effort |
|---|---|---|---|---|
| P0 | Réparer sélection de run + vérité hook | S-01, S-02, R-01 | STRUCTURED + tests | M |
| P1 | Corriger les 22 liens/chemins actifs | O-01..O-07 | `1-vbb-code-doc-gap-integrator` ou FAST-STANDARD | S |
| P1 | Réconcilier statut et dette | S-03..S-06 | `1-vbb-doc-harmonizer` ciblé | S |
| P1 | Caractériser executor et hooks | M-01, M-02 | tests structurés | M |
| P2 | Documenter outils secondaires | M-03..M-05 | `1-vbb-code-doc-gap-integrator` | S |

## Healthy zones

| Code unit | Document | Note |
|---|---|---|
| Architecture linter + source | `docs/ARCHITECTURE.md`, `RELATIONS.md` | 9 blocs, lint vert, projection régénérable |
| 64 skills/contracts | `skills/INDEX.yaml`, skill docs | 64/64/64, contract lint vert |
| Setup + four adapters | README/GUIDE/DEPLOYMENT/distribution README | ensemble officiel cohérent et smoke couvert |
| Contract runtime | architecture + P.R2 | dry-run déterministe 43/19/2 |
| Test suite | CONTEXT + test files | 133 passed, 1 skipped |

Total: 5 familles cohérentes majeures.

## Unknowns / uncertainties

- Les documents non suivis du worktree peuvent être des brouillons légitimes ;
  ils ne sont pas classés comme vérité active.
- Le scanner valide l'existence des chemins Markdown, pas la sémantique de
  chaque ancre ni les exemples historiques.
- Les 424 fichiers sous `docs/` incluent de nombreux snapshots intentionnels ;
  leur contenu n'est pas réécrit par définition.

```yaml
FINAL_STATUS:
  elapsed_seconds: 420
  budget_initial: 180
  progress_emitted: true
  progress_count: 1
  extension_requested: false
  timeout_closeout_emitted: false
  verdict: COMPLETE
  files_touched:
    - docs/audits/code-doc-coherence-20260713-1734.md
  tests_run:
    - active markdown local-link scan
    - python tools/vbb-architecture.py lint
    - python tools/vbb-contract-lint.py
  tests_missing:
    - semantic anchor validation
  risks:
    - O-01
    - O-02
    - S-01
    - S-02
  open_points:
    - untracked drafts intentionally excluded
```
