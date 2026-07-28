---
run_id: "2026-07-28_2000_m2-bis-adversarial-loop-bootstrap-deployment"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "ACTIVE"
kind: "BOOTSTRAP_DEPLOYMENT_PLAN"
posture: "consume-rem01-rem02-m2-deferred"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
started_at: "2026-07-28T20:15:00Z"
ended_at: "2026-07-28T20:30:00Z"
agent: "external implementer (distinct session, distinct provider)"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Plan d'exécution M2-BIS

## Objectif

Implémenter la bootstrap `PRE_CERTIFICATION` + `MIGRATION`
(ratifiée R1) et consommer les 31 entrées de
`M2_DEFERRED_ITEMS.md` (M2-23..M2-37) en respectant strictement
les bornes du brief (pas de SELF_HOSTING, pas de déviation M1,
pas de modification A0/A1/A2, compatibilité ascendante v1.0
préservée).

## Pré-conditions

| Pré-condition | Statut |
|---|---|
| R1 `03_DECISION.md` finalisé | ✅ (REM-01, REM-02 ratifiés) |
| M2 `M2_DEFERRED_ITEMS.md` complet | ✅ (31 entrées) |
| M2 `07_CLOSEOUT.md` (HANDOFF PARTIAL) | ✅ |
| Tests M2 verts (255 passed) | ✅ |
| v1.1 closure validator (extended) | ✅ (REM-02 closed) |
| v1.1 adversarial validator (NEW) | ✅ (M2-24 closed) |

## Approche : exécution par tiers

8 tiers ordonnés par dépendance logique :

| Tier | Contenu | Dépendance |
|---|---|---|
| 1 | Bootstrap canon (REM-01) | aucun — fondation |
| 2 | Outillage (REM-02 + M2-24) | Tier 1 (reconnaît les statuts) |
| 3 | Templates (M2-26..28) | Tier 1 (utilise les statuts) |
| 4 | Skills (M2-29, M2-30) | Tier 3 (utilise les templates) |
| 5 | Prompts (M2-31) | Tier 4 (référence les skills) |
| 6 | Tests (11 tests) | Tier 2 (teste le validator) |
| 7 | Distributions (CR#12) | Tier 1 (référence l'autorité) |
| 8 | Cutoff / ramp / validation | Tous les tiers |

## Étapes ordonnées

| # | Étape | Livrable |
|---|---|---|
| 1 | Étendre `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §11 + `docs/GATE_ASSURANCE_GOVERNANCE.md` §Schema 1.1 | 2 fichiers canon étendus (REM-01) |
| 2 | Étendre `tools/vbb-loop-closure-check.py` + créer `tools/vbb-adversarial-gate.py` | 1 outil étendu, 1 outil NEW (REM-02 + M2-24) |
| 3 | Créer/étendre 5 templates (FINDING, ADVERSARIAL_CAMPAIGN, 01, 06, 07) | 5 templates (M2-26..28) |
| 4 | Créer/étendre 4 skills (2 NEW, 2 étendus) | 4 skills (M2-29..30) |
| 5 | Étendre 4 prompts | 4 prompts (M2-31) |
| 6 | Ajouter 11 fichiers de tests (51 NEW cases) | 51 tests ajoutés (M2-23) |
| 7 | Étendre 2 distributions + DISTRIBUTIONS.md | 5 fichiers (M2-32, M2-33, CR#12) |
| 8 | Valider cutoff/ramp/validation (M2-34..37) | CI local 14/14 PASS, pytest 306 PASS |

## Critères d'acceptation

| Critère | Test |
|---|---|
| `vbb-architecture.py lint` PASS | obligatoire |
| `vbb-contract-lint.py` PASS | obligatoire |
| `vbb-loop-closure-check.py` PASS | obligatoire (étendu v1.1) |
| `vbb-adversarial-gate.py` opérationnel | obligatoire (NEW) |
| `pytest tests/ -q` PASS | obligatoire (306 passed, 1 skipped) |
| `bash scripts/vbb-ci-local.sh` PASS | obligatoire (14/14) |
| Aucun fichier hors périmètre | obligatoire (excl. `docs/runs/2026-07-26_1701_i1-i2-normative-remediation/`) |
| Aucun secret/credentials | obligatoire (credentials gate) |
| Aucun commit automatique | obligatoire |
| Compatibilité ascendante v1.0 | obligatoire (`test_backward_compat_v1_0.py`) |

## Plan de rollback global

| Niveau | Action |
|---|---|
| Tier 1 (canon) | `git restore docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md docs/GATE_ASSURANCE_GOVERNANCE.md docs/AGENTIC_RUN_PROTOCOL.md docs/CONVENTIONS.md docs/ENGINEERING_KNOWLEDGE_GOVERNANCE.md docs/PILOTAGE.md docs/REFERENCE/pre-merge-gate.md docs/adr/0051-adversarial-assurance-dimension.md` |
| Tier 2 (outils) | `git restore tools/vbb-loop-closure-check.py && rm tools/vbb-adversarial-gate.py` |
| Tier 3-7 (déploiement) | `git restore templates, skills, prompts, distributions, docs/DISTRIBUTIONS.md` |
| Tests | `git restore tests/` |
| Run evidence | `git restore docs/runs/` (si pas encore commit) |
| Si commit 1 fait : `git reset --hard HEAD^` | revenir avant le bootstrap canon |
| Si commit 2 fait : `git reset --hard HEAD~2` ou `git reset --hard sha_commit_1` (substituer le SHA réel) | annuler l'opération complète |
| Si besoin partiel : `git revert sha_commit_1` ou `git revert sha_commit_2` (substituer les SHA réels) | créer un commit d'annulation |

## Vérifications P.R2

Avant chaque transition de tier, vérification :
- `vbb-architecture.py lint`
- `vbb-architecture.py graph --write`
- `vbb-contract-lint.py`
- `vbb-loop-closure-check.py` (étendu à Tier 2)
- `pytest tests/ -q`

## Risques identifiés

| Risque | Mitigation |
|---|---|
| Oubli d'une entrée M2_DEFERRED | Trace par tier ; vérif croisée avec `M2_DEFERRED_ITEMS.md` |
| Introduction accidentelle d'un statut hors R1 | Garde : scope strict à `PRE_CERTIFICATION`, `MIGRATION`, et statuts M1 existants |
| Casse de compatibilité ascendante | Tests dédiés (Tier 6, test_backward_compat_v1_0.py) |
| Échec du validator (REM-02) sur les runs existants | Fallback v1.0 strict si version < 1.1 |

## Livrables

- 8 tiers implémentés.
- 11 tests NEW ou MODIFY.
- 5 fichiers canoniques étendus (REM-01).
- 2 outils étendus (REM-02 + M2-24).
- 5 templates (NEW ou étendus).
- 4 skills (2 NEW, 2 étendus).
- 4 prompts (étendus).
- 5 fichiers de distributions (CR#12).
- 1 entrée `docs/DISTRIBUTIONS.md` §Decisions log.
- 1 closeout structuré.
- 1 proposition de commit.