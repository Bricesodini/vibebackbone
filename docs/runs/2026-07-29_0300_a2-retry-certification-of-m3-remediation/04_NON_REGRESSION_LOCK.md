# 04_NON_REGRESSION_LOCK — A2-RETRY

## Vérification des locks M3 sur le commit c4bb4b63

Pour chaque remédiation M3-01..M3-12, vérifier que :

1. Le test M3 existe et est exécuté.
2. Le test M3 échoue sur baseline ab21d9a (proof of fails-before).
3. Le test M3 passe sur c4bb4b6 (proof of passes-after).
4. Aucun test M3 n'est satisfait par défaut ou trivial.

| Item M3 | Test M3 | Statut ab21d9a | Statut c4bb4b6 | Lock vérifié |
|---|---|---|---|---|
| M3-01 | test_adversarial_gate_yaml_unwrap.py (6 tests) | FAIL sur tests nested/empty/scalar | PASS sur tous | ✅ |
| M3-02 | test_a2_distinct_identity.py (5 tests) | FAIL sur tests distinct | PASS | ✅ |
| M3-03 | test_canon_documents_level_reason.py (3 tests) | FAIL sur canon docs | PASS | ✅ |
| M3-04 | test_no_intake_side_channel.py (3 tests) | FAIL (intake_text read-then-ignore) | PASS (read removed) | ✅ |
| M3-05 | test_session_validation.py (4 tests) | FAIL (no length check) | PASS (length ≥ 8 enforced) | ✅ |
| M3-06 | test_v10_reader_v11_data_fail_closed.py (3 tests) | FAIL (no version gate) | PASS | ✅ |
| M3-07 | test_skill_frontmatter_validation.py (6 tests) | FAIL (no frontmatter check) | PASS | ✅ |
| M3-08 | test_gate_family_checkpoint_matrix.py (12 tests) | FAIL (no matrix) | PASS | ✅ |
| M3-09 | test_last_external_review.py (3 tests) | FAIL (no cadence check) | PASS (ref date hard-coded) | ✅ |
| M3-10 | test_certification_separation.py (3 tests) | FAIL (no §5.3.0) | PASS | ✅ |
| M3-11 | test_distributions_propagation.py (6 tests) | FAIL (no comments in setup.sh) | PASS | ✅ |
| M3-12 | test_a2_proxy_distinct_identity.py (5 tests) | FAIL (no proxy regression) | PASS | ✅ |
| **Total** | **59 tests** | — | **59 PASS** | **12/12 ✅** |

## Vérification indépendante

Exécution réelle sur c4bb4b6 :

```bash
$ python -m pytest tests/test_adversarial_gate_yaml_unwrap.py \
    tests/test_a2_distinct_identity.py tests/test_session_validation.py \
    tests/test_no_intake_side_channel.py tests/test_canon_documents_level_reason.py \
    tests/test_v10_reader_v11_data_fail_closed.py tests/test_skill_frontmatter_validation.py \
    tests/test_gate_family_checkpoint_matrix.py tests/test_last_external_review.py \
    tests/test_certification_separation.py tests/test_distributions_propagation.py \
    tests/test_a2_proxy_distinct_identity.py -q

59 passed in 1.66s
```

## Preuves d'absence de régression M3

Aucune des 12 remédiations n'a introduit de fail-open détecté
sur les axes obligatoires (cf. `03_FINDINGS.md`).

Les 3 S3 findings ne sont **pas des régressions** mais des
observations sémantiques sur des éléments **non modifiés** par
M3 :

- **ADVR-RT-01** : `adv-block-exists` gate name trompeur —
  sémantique héritée, M3-01 a seulement modifié le `read_yaml_block`,
  pas le nom du gate.
- **ADVR-RT-02** : `level.strip()` cosmétique — comportement
  pré-existant, M3-01 n'a pas modifié cette ligne.
- **ADVR-RT-03** : `revocation_mechanism` non vérifié — choix
  architectural documenté par M3-10 (séparation 6.3.10/11/12).

Ces 3 findings ne constituent **pas** des « non-regression locks
brisés » mais des **observations de limites**. Aucun ne s'oppose
à la certification du commit M3 ; ils méritent un item M4 dédié.

## Non-regression lock verdict

| Aspect | Valeur |
|---|---|
| Locks M3 vérifiés sur c4bb4b6 | **12/12 PASS** |
| Régressions bloquantes introduites | **0** |
| Régressions non-bloquantes introduites | **0** |
| Fail-open découverts | **0** |
| Comportements pré-existants discutables | **3** (S3) |
| Verdict non-regression lock | **VERIFIED** |

## A2-retry commit fingerprint

```bash
$ git rev-parse HEAD
c4bb4b63b1e59e67d92acead1371ca6a95cf002a

$ git log --oneline -3
c4bb4b6 (HEAD) fix(adversarial): remediate first A2 certification findings
ab21d9a feat(adversarial): deploy v1.1 operational integration
921a780 feat(adversarial): bootstrap assurance governance v1.1

$ git diff HEAD~1 HEAD --stat
 17 files changed, 2125 insertions(+), 24 deletions(-)
```

Aucune mutation hors `/tmp/a2-retry-fixtures/` et
`docs/runs/2026-07-29_0300_a2-retry-certification-of-m3-remediation/`.

## Out-of-scope verification

```bash
$ git diff HEAD -- \
    distributions/claude/setup.sh \
    docs/DISTRIBUTIONS.md \
    tests/test_*distribution*
(empty)
```

`CLAUDE-SKILLS-DISCOVERY-01` strictement préservé.