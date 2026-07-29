---
id: "RUN1-A2-CR-05"
severity: "S0"
confidence: "CONFIRMED"
state: "REMEDIATED_PENDING_COUNTER_PROOF"
---

# RUN1-A2-CR-05 — duplicate critical arguments

## Précondition

Le sujet de certification est transmis aux gates Core avec des options
critiques répétées (`--expected-commit`, `--candidate-id`, `--run-id` ou
`--runs-dir`).

## Reproduction avant correction

```bash
python tools/vbb-loop-closure-check.py RUN_ID \
  --expected-commit OLD_SHA --expected-commit HEAD_SHA --strict --json
```

Le dernier argument gagnait silencieusement (`return_code: 0` lorsque le
dernier SHA était valide). Le même bypass existait pour `--candidate-id` et
dans `tools/vbb-adversarial-gate.py`.

## Correction

La résolution Core inspecte les occurrences avant `argparse` et rejette toute
option sélectrice répétée avec `duplicate_critical_argument`. Les valeurs
identiques, contradictoires, vides puis valides et valides puis vides sont
toutes bloquées. Une occurrence unique conserve le contrat existant.

## Lock de non-régression

```yaml
fails_on_f972ddc: true
passes_after_fix: true
cases:
  - expected_commit_conflicting
  - expected_commit_identical
  - candidate_id_duplicate
  - expected_commit_empty_then_valid
  - expected_commit_valid_then_empty
```

Le lock est exécuté par `tests/test_release_subject_arguments.py`; la
contre-revue A2 indépendante reste requise avant certification.
