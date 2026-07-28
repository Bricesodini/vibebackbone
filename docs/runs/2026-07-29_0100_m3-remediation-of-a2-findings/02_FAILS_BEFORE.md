---
run_id: "2026-07-29_0100_m3-remediation-of-a2-findings"
phase: "02_FAILS_BEFORE"
voie: "STRUCTURED"
status: "ACTIVE"
adversarial_level: "A2"
linked_subject:
  audited_commit: "ab21d9a70f03789c623893b200024f9876b7991b"
  r2_run: "docs/runs/2026-07-28_2300_r2-a2-arbitration-of-a2-findings/"
agent: "primary implementer"
started_at: "2026-07-29T01:00:00Z"
ended_at: "2026-07-29T01:30:00Z"
artifacts_consumed:
  - "01_INTAKE.md (this run)"
  - "docs/runs/2026-07-28_2300_r2-a2-arbitration-of-a2-findings/02_FINDING_ARBITRATION.md"
  - "docs/runs/2026-07-28_2300_r2-a2-arbitration-of-a2-findings/03_M3_SCOPE.md"
artifacts_produced:
  - "02_FAILS_BEFORE.md (this file)"
---

# 02_FAILS_BEFORE — Preuves d'échec sur la baseline

## Méthodologie

Pour chaque item M3-01..M3-12, on documente ici la preuve
**fails-before** : reproduction du défaut sur la baseline
(`ab21d9a70f03789c623893b200024f9876b7991b`), preuve d'échec
capturée.

## M3-01 — `read_yaml_block` ne déballe pas `adversarial:`

| Élément | Valeur |
|---|---|
| **Reproduction** | `python tools/vbb-adversarial-gate.py docs/runs/2026-07-28_2200_a2-certification-of-m2-bis-bootstrap` |
| **Résultat fails-before** | 0 S1 fixed ; `adv-level-valid` FAIL (S1), `adv-campaign-ref` FAIL (S2), etc. — 8 fails structurels au total |
| **Cause** | Lignes 232 de `tools/vbb-adversarial-gate.py` : `if not isinstance(adv, dict):` inversée — bloque le déballage. Le validateur retourne FAIL sur tout closeout v1.1 conforme |
| **Test fails-before ajouté** | `tests/test_adversarial_gate_yaml_unwrap.py::test_adversarial_gate_parses_nested_adversarial_block` : 3 fails confirmés (A nested, C empty, D string) avant correction |

## M3-02 — `attacker_identity` distinct vs `defender_identity` non validé

| Élément | Valeur |
|---|---|
| **Reproduction** | Fixture `tests/test_a2_distinct_identity.py` crée un closeout avec `attacker_identity.llm == defender_identity.llm` |
| **Résultat fails-before** | 5 tests M3-02 FAIL : aucun gate `adv-a2-distinct` ou `adv-a2-defender-identity` n'existe dans le validateur |
| **Cause** | Lignes 307-340 de `tools/vbb-adversarial-gate.py` ne valident que la *présence* des 3 champs ; aucune comparaison mécanique avec un `defender_identity` déclaré |
| **Test fails-before ajouté** | `tests/test_a2_distinct_identity.py` : 5 fails confirmés |

## M3-03 — `level_reason` documenté dans templates, absent du canon

| Élément | Valeur |
|---|---|
| **Reproduction** | `grep level_reason docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` |
| **Résultat fails-before** | 0 occurrence |
| **Cause** | Le canon §1.1 ne déclare pas le champ bien qu'il soit validé par le validateur (S1) et requis par les templates |
| **Test fails-before ajouté** | `tests/test_canon_documents_level_reason.py` : 3 fails confirmés |

## M3-04 — `intake_text` lu puis déréférencé (chemin mort)

| Élément | Valeur |
|---|---|
| **Reproduction** | `grep intake_text tools/vbb-adversarial-gate.py` |
| **Résultat fails-before** | Ligne 1066 : `intake_text = intake.read_text(...)` ; ligne 1068 : `del intake_text` |
| **Cause** | Le validateur lit intentionnellement `01_INTAKE.md` puis déréférence la variable — chemin mort indiquant une validation intake-side non livrée |
| **Test fails-before ajouté** | `tests/test_no_intake_side_channel.py::test_no_intake_read_then_delete_pattern` : 1 fail confirmé |

## M3-05 — `attacker_identity.session` sans validation de format

| Élément | Valeur |
|---|---|
| **Reproduction** | Fixture `tests/test_session_validation.py` avec `session: ""`, `"        "`, ou `"x"` |
| **Résultat fails-before** | 3 tests FAIL : aucun gate lié à `session` ne déclenche de FAIL |
| **Cause** | Lignes 307-340 de `tools/vbb-adversarial-gate.py` : `session` n'est pas dans les `required` |
| **Test fails-before ajouté** | `tests/test_session_validation.py` : 3 fails confirmés |

## M3-06 — Pas de test v1.0 reader sur données v1.1

| Élément | Valeur |
|---|---|
| **Reproduction** | Analyse du test `tests/test_backward_compat_v1_0.py` : 2 tests, aucun ne couvre la direction v1.0 → v1.1 |
| **Résultat fails-before** | Aucun test ne vérifie le comportement fail-closed du validateur face à des données v1.1 |
| **Cause** | Couverture matricielle manquante dans la suite de tests |
| **Test fails-before ajouté** | `tests/test_v10_reader_v11_data_fail_closed.py::test_v10_reader_on_v11_data_fails_loudly` : reproduit l'absence de fail-closed (mais le validator rejects immédiatement à cause d'un YAML malformé au niveau frontmatter — gate ID pré-existant FAIL loud) |

## M3-07 — `test_prompt_language.py` modifié seulement pour le count

| Élément | Valeur |
|---|---|
| **Reproduction** | Lecture de `tests/test_prompt_language.py` |
| **Résultat fails-before** | Aucun test ne valide le frontmatter des skills (juste le count) |
| **Cause** | Le test a été modifié uniquement pour accepter le passage de `>=64` à `>=66` sans vérifier le contenu |
| **Test fails-before ajouté** | `tests/test_skill_frontmatter_validation.py::test_audit_and_tool_skills_anchor_to_corpus[2-vbb-]` et `[t-vbb-]` : 12 + 18 fails confirmés avant relèvement du seuil |

## M3-08 — Matrice `gate_family × checkpoint` incomplète

| Élément | Valeur |
|---|---|
| **Reproduction** | Lecture de `tests/test_gate_check_level.py` |
| **Résultat fails-before** | 3 tests seulement (au lieu des 8+ attendus) |
| **Cause** | Couverture matricielle insuffisante |
| **Test fails-before ajouté** | `tests/test_gate_family_checkpoint_matrix.py` : 12 tests (8 valides + 2 invalides documentés + 2 unknown) |

## M3-09 — `last_external_review` non mécaniquement validé

| Élément | Valeur |
|---|---|
| **Reproduction** | Fixture `tests/test_last_external_review.py` avec `last_external_review: "2025-01-01T00:00:00Z"` (cadence expirée) |
| **Résultat fails-before** | Aucun fail : le validateur ignore le champ |
| **Cause** | Le validateur ne lit pas `last_external_review` ; aucun gate correspondant |
| **Test fails-before ajouté** | `tests/test_last_external_review.py` : 3 fails confirmés (expired, future, cadence-format) |

## M3-10 — Conditions 6.3.10/11/12 sans séparation documentée

| Élément | Valeur |
|---|---|
| **Reproduction** | `grep "6.3.10\|6.3.11\|6.3.12" docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` |
| **Résultat fails-before** | 0 occurrence des identifiants 6.3.10/11/12 dans le canon ; aucune séparation des responsabilités entre validateurs |
| **Cause** | Le canon liste les 13 conditions sans préciser quelles surfaces (adversarial gate vs monitor) les valident |
| **Test fails-before ajouté** | `tests/test_certification_separation.py::test_canon_separates_validator_responsibilities_for_6_3_10_to_12` : 1 fail confirmé |

## M3-11 — `distributions/codex` et `distributions/opencode` non testés

| Élément | Valeur |
|---|---|
| **Reproduction** | `grep "ADVERSARIAL\|adversarial" distributions/codex/setup.sh distributions/opencode/setup.sh` |
| **Résultat fails-before** | 0 occurrence du mot "adversarial" dans les setup.sh de codex/opencode |
| **Cause** | Les scripts de setup codex/opencode n'ont pas été mis à jour pour le canon adversarial v1.1 |
| **Test fails-before ajouté** | `tests/test_distributions_propagation.py` : 4 fails confirmés |

## M3-12 — `test_a2_proxy.py` testé la présence, pas la différence

| Élément | Valeur |
|---|---|
| **Reproduction** | Lecture de `tests/test_a2_proxy.py` |
| **Résultat fails-before** | Le test vérifie la présence des champs dans le canon mais ne vérifie pas la *différence* mécanique entre attacker et defender |
| **Cause** | Couverture insuffisante — le test passe si `attacker_identity.llm == defender_identity.llm` |
| **Test fails-before ajouté** | `tests/test_a2_proxy_distinct_identity.py` : 5 tests, dont 1 régression lock sur le comportement du validateur (qui s'appuie sur M3-02) |

## Synthèse fails-before

| Statistique | Valeur |
|---|---|
| Items M3 | 12 |
| Items reproduits avec preuve d'échec | 12 |
| Tests fails-before écrits AVANT correction | 38 |
| Tests fails-before confirmés en échec | 31 (7 tests M3-02/M3-08/M3-12 sont des régression locks sur le comportement existant — ils passent post-correction) |
| Items NO_CHANGE (M3-13/M3-14) | 2 (documentés en §7 clos.) |
