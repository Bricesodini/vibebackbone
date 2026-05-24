---
run_id: "2026-06-10_1930_lot1c-ci-audit"
phase: "02_AUDIT"
voie: "AUDIT"
status: "PARTIAL"
agent: "claude-code"
started_at: "2026-06-10T19:30:00Z"
ended_at: "2026-06-10T20:00:00Z"
next_phase: null
artifacts_consumed:
  - "skills/2-vbb-ci/SKILL.md"
  - ".github/workflows/vbb-contracts.yml"
  - ".github/workflows/smoke.yml"
  - "scripts/vbb-ci-local.sh"
artifacts_produced:
  - "docs/audits/ci-20260610-ci-audit.md"
  - "docs/runs/2026-06-10_1930_lot1c-ci-audit/03_AUDIT_FINDINGS.md"
  - "docs/runs/2026-06-10_1930_lot1c-ci-audit/04_RISK_CLASSIFICATION.md"
---

# Audit CI — vibebackbone

**Date** : 2026-06-10  
**Skill** : `2-vbb-ci`  
**Verdict** : PARTIAL

## Résumé

CI existante et fonctionnelle (lint, runtime, 3 test suites, install smoke). Mais invariants importants manquants : permissions, version pinning, cohérence locale/remote, couverture tests négatifs, smoke multi-OS.

## Findings

### P2 (5)

| ID | Constat | Zone |
|----|---------|------|
| CI-001 | Workflows sans permissions block | .github/workflows/ |
| CI-002 | PyYAML non épinglé (pip + requirements.txt) | workflows + requirements.txt |
| CI-004 | Incohérence CI locale vs GitHub (3 divergences) | scripts/ vs .github/ |
| CI-006 | smoke.yml macOS only, pas de matrice Python | .github/workflows/smoke.yml |
| CI-008 | Pas de tests négatifs pour lint/router | tests/ |

### P3 (3)

| ID | Constat | Zone |
|----|---------|------|
| CI-003 | Pas de cache pip | workflows |
| CI-005 | Pas de filtre de branche (runs inutiles) | workflows |
| CI-007 | Matrice Python limitée (3.11 only) | vbb-contracts.yml |

### Croisements

- CI-001 = SEC-009 (audit sécurité)
- CI-002 = SEC-005 (audit sécurité)
- CI-008 = TD-006 + TD-010 (audit dette technique)

## Zones non couvertes (UNKNOWN)

- Exécution réelle sur GitHub Actions (non testée — seul le dry-run local a été vérifié)
- Comportement du runtime sur les runners GitHub (environnement différent)