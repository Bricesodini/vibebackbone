---
run_id: "2026-07-29_0100_m3-remediation-of-a2-findings"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
adversarial_level: "A2"
agent: "primary implementer"
started_at: "2026-07-29T01:00:00Z"
ended_at: "2026-07-29T01:05:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md (this run)"
artifacts_produced:
  - "04_PLAN.md (this file)"
---

# 04_PLAN — Plan d'exécution M3

## Stratégie d'ordonnancement

L'ordre d'exécution suit strictement R2 §1 (`03_M3_SCOPE.md`).

```
M3-01 ─┐ (racine : fix read_yaml_block unwrap)
       ├─→ M3-02 (validates after M3-01 fix)
       ├─→ M3-04 (réutilise le déballage de M3-01)
       └─→ M3-09 (cadence check, dépend du validateur fonctionnel)
M3-03 (doc canon, indépendant)
M3-05 (session validation, dépend de M3-01)
M3-06 (test v1.0/v1.1, indépendant)
M3-07 (skill frontmatter, indépendant)
M3-08 (gate_family × checkpoint matrix, indépendant)
M3-10 (séparation canon, indépendant)
M3-11 (distributions, indépendant)
M3-12 (test attacker_identity distinct, dépend de M3-02)
M3-13 (NO_CHANGE — ADVR-A2-04 FAUX_POSITIF)
M3-14 (NO_CHANGE — ADVR-A2-12 CHOIX_ASSUMÉ)
```

## Plan détaillé (12 items remédiés)

### Item 1 — M3-01 (S1, racine)

| Action | Fichier | Test fails-before |
|---|---|---|
| Modifier `read_yaml_block` pour accepter `marker:` avec ou sans valeur | `tools/vbb-adversarial-gate.py:169-180` | `test_adversarial_gate_parses_nested_adversarial_block` |
| Modifier `check_adversarial_block` pour déballer `{"adversarial": {...}}` | `tools/vbb-adversarial-gate.py:215-260` | `test_adversarial_gate_rejects_empty_adversarial_block` + 4 autres |

### Item 2 — M3-02 (S1, dépend de M3-01)

| Action | Fichier | Test fails-before |
|---|---|---|
| Ajouter `defender_identity` au template | `docs/templates/07_CLOSEOUT.md.template` | (template check est documentaire) |
| Ajouter `check_a2_distinct_identity` au validateur | `tools/vbb-adversarial-gate.py:415-540` | `test_adversarial_gate_rejects_identical_attacker_and_defender_llm` (M3-02.A) |

### Item 3 — M3-03 (S2, indépendant)

| Action | Fichier | Test fails-before |
|---|---|---|
| Ajouter §1.1.1 avec déclaration de `level_reason` | `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` | `test_canon_documents_level_reason_field` |

### Item 4 — M3-04 (S2, dépend de M3-01)

| Action | Fichier | Test fails-before |
|---|---|---|
| Supprimer `intake_text = intake.read_text(...)` ; remplacer par `assert intake.exists()` | `tools/vbb-adversarial-gate.py:1115-1130` | `test_no_intake_read_then_delete_pattern` |

### Item 5 — M3-05 (S2, dépend de M3-01)

| Action | Fichier | Test fails-before |
|---|---|---|
| Ajouter `session` aux `required` + contraintes non-empty + length ≥ 8 | `tools/vbb-adversarial-gate.py:495-540` | `test_adversarial_gate_rejects_empty_session` |

### Item 6 — M3-06 (S2, indépendant)

| Action | Fichier | Test fails-before |
|---|---|---|
| Tests `tests/test_v10_reader_v11_data_fail_closed.py` | `tests/` | 3 tests |

### Item 7 — M3-07 (S2, indépendant)

| Action | Fichier | Test fails-before |
|---|---|---|
| Tests `tests/test_skill_frontmatter_validation.py` | `tests/` | 6 tests |

### Item 8 — M3-08 (S3, indépendant)

| Action | Fichier | Test fails-before |
|---|---|---|
| Tests `tests/test_gate_family_checkpoint_matrix.py` | `tests/` | 12 tests |

### Item 9 — M3-09 (S3, dépend de M3-01)

| Action | Fichier | Test fails-before |
|---|---|---|
| Ajouter branche `last_external_review` dans `check_certification_status` | `tools/vbb-adversarial-gate.py:1075-1180` | `test_adversarial_gate_rejects_expired_external_review` |

### Item 10 — M3-10 (S3, indépendant)

| Action | Fichier | Test fails-before |
|---|---|---|
| Ajouter §5.3.0 au canon avec séparation des responsabilités | `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` | `test_canon_separates_validator_responsibilities_for_6_3_10_to_12` |

### Item 11 — M3-11 (S3, indépendant)

| Action | Fichier | Test fails-before |
|---|---|---|
| Commentaires en tête des setup.sh codex/opencode | `distributions/codex/setup.sh`, `distributions/opencode/setup.sh` | `test_distribution_anchors_to_adversarial_canon[codex/opencode]` |

### Item 12 — M3-12 (S2, dépend de M3-02)

| Action | Fichier | Test fails-before |
|---|---|---|
| Tests `tests/test_a2_proxy_distinct_identity.py` | `tests/` | 5 tests (régression lock) |

## Plan de vérification (M3 §16)

```bash
python tools/vbb-architecture.py lint
python tools/vbb-architecture.py graph --write
python tools/vbb-contract-lint.py
python tools/vbb-loop-closure-check.py --strict
python tools/vbb-adversarial-gate.py docs/runs/2026-07-28_2200_a2-certification-of-m2-bis-bootstrap
pytest tests/ -q
bash scripts/vbb-ci-local.sh
pre-commit credentials gate
git diff scope check
```

## Plan de commit (M3 §18)

| Aspect | Valeur |
|---|---|
| Nombre de commits | 1 |
| Type de message | Conventional commit |
| Prefix | `fix(adversarial)` |
| Title | `remediate first A2 certification findings` |
| Body | Multi-lignes décrivant M3-01..M3-12 + M3-13/M3-14 NO_CHANGE |
| Push | **INTERDIT** pendant M3 |
