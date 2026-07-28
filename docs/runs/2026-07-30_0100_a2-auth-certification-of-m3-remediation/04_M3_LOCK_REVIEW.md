---
run_id: "2026-07-30_0100_a2-auth-certification-of-m3-remediation"
phase: "04_M3_LOCK_REVIEW"
voie: "AUDIT"
status: "READY"
kind: "A2_AUTH_M3_LOCK_REVIEW"
adversarial_level: "A2"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
agent: "minimax/MiniMax-M3 (authentic distinct attacker)"
started_at: "2026-07-30T02:00:00Z"
ended_at: "2026-07-30T02:30:00Z"
next_phase: "05_FINDING_DISPOSITION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_IDENTITY_PREFLIGHT.md"
  - "03_ADVERSARIAL_REVIEW.md"
artifacts_produced:
  - "04_M3_LOCK_REVIEW.md (this file)"
---

# 04_M3_LOCK_REVIEW — A2-AUTH

## Matrice 12 locks M3

| Item | Finding source | Preuve rejouée | Résultat | Avis indépendant |
|---|---|---|---|---|
| **M3-01** | ADVR-A2-14 | `test_adversarial_gate_yaml_unwrap.py` (6/6 PASS) + replay live `adv-a2-distinct` PASS | PASS | **CONFIRMED** — unwrap fonctionne |
| **M3-02** | ADVR-A2-01 | `test_a2_distinct_identity.py` (5/5 PASS) + replay live same-family FAIL avec 2 raisons explicites | PASS | **CONFIRMED** — distinct_llm mécaniquement validé |
| **M3-03** | ADVR-A2-02 | `test_canon_documents_level_reason.py` (3/3 PASS) | PASS | **CONFIRMED** — canon §1.1.1 documente level_reason pour A0 |
| **M3-04** | ADVR-A2-05 | `test_no_intake_side_channel.py` (3/3 PASS) — outcome invariance sous mutation intake | PASS | **CONFIRMED** — pas de read-then-ignore |
| **M3-05** | ADVR-A2-07 | `test_session_validation.py` (4/4 PASS) — empty/whitespace/short/long | PASS | **CONFIRMED** — session ≥ 8 chars |
| **M3-06** | ADVR-A2-09 | `test_v10_reader_v11_data_fail_closed.py` (3/3 PASS) | PASS | **CONFIRMED** — v1.0 reader sur v1.1 data FAIL loud |
| **M3-07** | ADVR-A2-10 | `test_skill_frontmatter_validation.py` (6/6 PASS) | PASS | **CONFIRMED** — 25 skills frontmatter valides |
| **M3-08** | ADVR-A2-06 | `test_gate_family_checkpoint_matrix.py` (12/12 PASS) | PASS | **CONFIRMED** — 4×3 matrix gate_family×checkpoint |
| **M3-09** | ADVR-A2-03 | `test_last_external_review.py` (3/3 PASS) + replay live CERTIFIED/PRE_CERTIFICATION | PASS | **CONFIRMED** — cadence validation 90j max |
| **M3-10** | ADVR-A2-08 | `test_certification_separation.py` (3/3 PASS) | PASS | **CONFIRMED** — 6.3.10/11/12 séparation documentée |
| **M3-11** | ADVR-A2-13 | `test_distributions_propagation.py` (6/6 PASS) — pi/claude/codex/opencode | PASS | **CONFIRMED** — 4 distributions ancrées au canon |
| **M3-12** | ADVR-A2-11 | `test_a2_proxy_distinct_identity.py` (5/5 PASS) | PASS | **CONFIRMED** — proxy + lock regression |

**12/12 locks vérifiés**. Aucun lock ne montre de régression.

## Preuves adversariales supplémentaires (axe 5.2 du brief)

### Live re-execution M3-01..M3-12

```bash
for f in tests/test_adversarial_gate_yaml_unwrap.py \
         tests/test_a2_distinct_identity.py \
         tests/test_canon_documents_level_reason.py \
         tests/test_no_intake_side_channel.py \
         tests/test_session_validation.py \
         tests/test_v10_reader_v11_data_fail_closed.py \
         tests/test_skill_frontmatter_validation.py \
         tests/test_gate_family_checkpoint_matrix.py \
         tests/test_last_external_review.py \
         tests/test_certification_separation.py \
         tests/test_distributions_propagation.py \
         tests/test_a2_proxy_distinct_identity.py; do
  python -m pytest "$f"
done
```

**Résultat global** :

```yaml
total: 59 tests M3-added
passed: 59
failed: 0
skipped: 0
```

## Verdict authentique sur les 12 locks

| Critère | Évaluation |
|---|---|
| Nombre de locks vérifiés | 12/12 |
| Locks PASS sur replay | 12/12 |
| Régression bloquante | 0 |
| Régression mineure | 0 |
| Fail-open | 0 |

**Conclusion** : les 12 locks M3 tiennent sous attaque authentique.
La chaîne de non-régression est solide.
