---
run_id: "2026-07-14_1242_consumer-managed-hook-bundle"
phase: "03_DECISION"
status: "APPROVED"
agent: "codex"
created_at: "2026-07-14T12:46:00+02:00"
human_validated_by: "Brice — Go explicite"
---
# Canon Change Proposal — Consumer asset ownership

## Current Canon

L'architecture identifie `vbb-project-init.py` comme outil de bootstrap sans
contrat d'ownership séparant vérité projet et assets runtime copiés.

## Problem

Skip empêche le refresh ; overwrite remplace la vérité projet ; le bundle hook
incomplet échoue tout en retournant un succès. Aucun mécanisme ne prouve qu'une
cible copiée est encore identique à l'état géré par VBB.

## Proposed Canon

Les documents bootstrap sont project-owned/generated-once. Les assets runtime
explicitement listés sont VBB-managed ; un manifeste de hashes autorise leur
refresh seulement lorsqu'ils sont inchangés. Toute personnalisation ou origine
inconnue bloque le bundle avant écriture, sauf override dédié.

## Benefits

1. Pas d'écrasement silencieux.
2. Refresh reproductible et idempotent.
3. Installation hook autonome avec erreurs fidèles.

## Risks

1. Manifeste absent sur les anciens consommateurs.
2. Dépendance transitive oubliée dans le bundle.
3. Confusion si le manifeste n'est pas versionné.

## Impact Analysis

### Files

| File | Change type | Description |
|---|---|---|
| `tools/vbb-project-init.py` | MODIFY | bundle géré, manifeste, flags dédiés et erreurs |
| `tests/test_project_init.py` | EXTEND | scénarios ownership et hook réel |
| `docs/ARCHITECTURE.md` | MODIFY | contrat du bloc Contract Tooling |
| `docs/DISTRIBUTIONS.md` | MODIFY | héritage des quatre distributions |

### Modules / Architecture Blocks

| Block | Impact | Action |
|---|---|---|
| Contract Tooling | ownership consommateur | enrichir responsabilités/contrats |
| Governance Core | frontière généré/géré | relier ADR 0034 |

### Skills

| Skill | Change needed | Priority |
|---|---|---|
| `t-vbb-project-context-init` | documenter le comportement de l'outil | P2 |

### Prompts

| Prompt | Change needed | Priority |
|---|---|---|
| `1-p-vbb-project-init.md` | aucun changement : le prompt n'énumère pas la CLI | N/A |

### Tests

| Test | Must pass | Currently passing |
|---|---|---|
| `tests/test_project_init.py` | oui | 19/19 |
| P.R2 canonique | oui | PASS |

## Migration Plan

1. Introduire le manifeste uniquement pour le bundle hook.
2. Considérer toute cible préexistante sans provenance comme conflit.
3. Autoriser l'adoption forcée uniquement par flag explicite.
4. Ne jamais inclure les documents projet dans le bundle géré.

## Backward Compatibility

- [ ] Fully backward compatible — no action required from consumers
- [x] Grace period required — les anciens assets exigent une adoption explicite
- [ ] Breaking change — consumer migration required

## Human Decision

- [x] **Approved** — `Go` explicite de Brice après présentation du choix
- [ ] **Rejected**
- [ ] **Needs revision**

## Verification Loop

- [x] Architecture lint
- [x] Contract lint
- [x] Loop closure strict
- [x] Full pytest
- [x] Local CI
- [x] Architecture graph regenerated
- [x] Documentation links reconciled
- [x] Closeout produced

## Closeout Notes

Migration Core terminée : POC 6/6, 19 tests project-init, P.R2 PASS (178
passed, 1 skipped ; CI locale 9/9). SEC-CRED-005 et la frontière d'ownership
TER-001 sont fermés. Les documents projet restent volontairement hors refresh.

**Final status**: CLOSED — **Closed by**: Codex — **Date**: 2026-07-14
