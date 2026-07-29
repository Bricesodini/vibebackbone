---
id: "RUN1-A2-CR-04-LOCAL-CI"
severity: "S0"
confidence: "CONFIRMED"
state: "REMEDIATED_PENDING_COUNTER_PROOF"
---

# RUN1-A2-CR-04-LOCAL-CI — environnement hérité

## Précondition

Un appel direct à `subprocess.run` dans `tests/test_loop_closure.py` héritait
des variables `VBB_*` du shell appelant. Sous un environnement de CI valide,
le test qui devait vérifier l'absence de run explicite recevait implicitement
`VBB_RUN_ID` et produisait un résultat différent.

## Correction

Tous les sous-processus de cette suite construisent désormais un environnement
contrôlé qui retire toute variable `VBB_*`; un test ne reçoit ces variables que
s'il les injecte explicitement. Les appels Git de fixture suivent la même
règle, ce qui rend le lock vérifiable par recherche statique et par exécution.

## Lock de non-régression

```yaml
fails_on_f972ddc: true
passes_after_fix: true
matrices:
  - env_clean
  - env_valid_run_and_sha
  - env_contradictory_run_and_sha
  - env_empty_subject_values
```

Les trois exécutions de la suite complète donnent `464 passed, 1 skipped`;
les différences attendues restent limitées aux gates de certification
explicitement appelés par `scripts/vbb-ci-local.sh`.
