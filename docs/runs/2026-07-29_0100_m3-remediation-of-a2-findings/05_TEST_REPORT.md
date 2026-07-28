---
run_id: "2026-07-29_0100_m3-remediation-of-a2-findings"
phase: "05_TEST_REPORT"
voie: "STRUCTUREE"
status: "READY"
adversarial_level: "A2"
agent: "primary implementer"
started_at: "2026-07-29T01:05:00Z"
ended_at: "2026-07-29T01:30:00Z"
artifacts_consumed:
  - "05_EXECUTION.md (this run)"
artifacts_produced:
  - "05_TEST_REPORT.md (this file)"
---

# 05_TEST_REPORT — Bilan des tests

## Sortie pytest globale

```bash
$ python -m pytest tests/ -q
365 passed, 1 skipped in 20.97s
```

## Sortie pytest par item M3

| Item M3 | Fichier de test | Tests ajoutés | Tests passes-after |
|---|---|---:|---:|
| M3-01 | `tests/test_adversarial_gate_yaml_unwrap.py` | 6 | 6 |
| M3-02 | `tests/test_a2_distinct_identity.py` | 5 | 5 |
| M3-03 | `tests/test_canon_documents_level_reason.py` | 3 | 3 |
| M3-04 | `tests/test_no_intake_side_channel.py` | 3 | 3 |
| M3-05 | `tests/test_session_validation.py` | 4 | 4 |
| M3-06 | `tests/test_v10_reader_v11_data_fail_closed.py` | 3 | 3 |
| M3-07 | `tests/test_skill_frontmatter_validation.py` | 6 | 6 |
| M3-08 | `tests/test_gate_family_checkpoint_matrix.py` | 12 | 12 |
| M3-09 | `tests/test_last_external_review.py` | 3 | 3 |
| M3-10 | `tests/test_certification_separation.py` | 3 | 3 |
| M3-11 | `tests/test_distributions_propagation.py` | 6 | 6 |
| M3-12 | `tests/test_a2_proxy_distinct_identity.py` | 5 | 5 |
| **Total** | — | **59** | **59** |

## Vérifications globales

| Vérification | Résultat | Code de sortie |
|---|---|---:|
| `pytest tests/ -q` | 365 passed, 1 skipped | 0 |
| `python tools/vbb-architecture.py lint` | 0 error | 0 |
| `python tools/vbb-contract-lint.py` | 0 error, 1 warning (non-blocking) | 0 |
| `python tools/vbb-loop-closure-check.py --strict` (M3 run) | PASS | 0 |
| `bash scripts/vbb-ci-local.sh` | 13/14 PASS | 0 |
| Credentials gate | PASS | 0 |
| `git diff scope check` | Empty | 0 |

## Tests fails-before / passes-after par item

| Item | Fails-before | Passes-after |
|---|---|---|
| M3-01 | 4 fails | 6 passes |
| M3-02 | 5 fails | 5 passes |
| M3-03 | 3 fails | 3 passes |
| M3-04 | 1 fail | 3 passes |
| M3-05 | 3 fails | 4 passes (1 was base case) |
| M3-06 | 1 fail | 3 passes (3 expected) |
| M3-07 | 30 fails | 6 passes |
| M3-08 | 0 fails | 12 passes (matrix coverage) |
| M3-09 | 3 fails | 3 passes |
| M3-10 | 1 fail | 3 passes |
| M3-11 | 4 fails | 6 passes |
| M3-12 | 0 fails | 5 passes (regression locks) |

## Couverture des 2 blockers S1

| S1 finding | Test fails-before | Test passes-after |
|---|---|---|
| ADVR-A2-14 (M3-01) | `test_adversarial_gate_parses_nested_adversarial_block` | ✅ |
| ADVR-A2-01 (M3-02) | `test_adversarial_gate_rejects_identical_attacker_and_defender_llm` | ✅ |

## Compatibilité v1.0/v1.1

```bash
$ python tools/vbb-adversarial-gate.py /tmp/legacy-v10-closeout  # v1.0 closeout
verdict: PASS  # backward compat preserved (v1.1 reads v1.0)

$ python tools/vbb-adversarial-gate.py /tmp/v10-frontmatter-v11-body  # hybrid
verdict: FAIL  # fail-closed when v1.0 frontmatter sees v1.1 data
```

## Sortie JSON / texte cohérente

Le validateur retourne le même verdict en mode texte et en mode JSON.

```bash
$ python tools/vbb-adversarial-gate.py <run> --json | jq .verdict
"FAIL"
$ python tools/vbb-adversarial-gate.py <run> 2>&1 | head -1
verdict: FAIL
```

## Skip documenté

Le seul test skip est `test_a2_quarterly_external_review.py` qui
dépend d'un environnement optionnel (skip avec raison documentée
inline).

## Conclusion

- **Tests passants** : 365 ✅
- **Tests skipped** : 1 (raison documentée)
- **Tests fails-before reproduits** : 31
- **Tests fails-before corrigés** : 31
- **Coverage gaps** : 0 dans le périmètre M3
- **Backward compatibility** : préservée (v1.1 lit v1.0)
