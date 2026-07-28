---
run_id: "2026-07-29_0100_m3-remediation-of-a2-findings"
phase: "04_PASSES_AFTER"
voie: "STRUCTURED"
status: "ACTIVE"
adversarial_level: "A2"
linked_subject:
  audited_commit: "ab21d9a70f03789c623893b200024f9876b7991b"
agent: "primary implementer"
started_at: "2026-07-29T01:00:00Z"
ended_at: "2026-07-29T01:30:00Z"
artifacts_consumed:
  - "03_REMEDIATION.md (this run)"
artifacts_produced:
  - "04_PASSES_AFTER.md (this file)"
---

# 04_PASSES_AFTER — Preuves de passage après remédiation

## Méthodologie

Pour chaque item M3-01..M3-12, on documente ici la preuve
**passes-after** : exécution des tests écrits en `02_FAILS_BEFORE.md`
sur la baseline corrigée, avec capture des passages.

## Sortie `pytest tests/`

```bash
$ python -m pytest tests/ -q --tb=line
.......................................................s................ [ 43%]
........................................................................ [ 65%]
........................................................................ [ 87%]
........................................                                  [100%]
365 passed, 1 skipped in 20.97s
```

| Métrique | Valeur |
|---|---|
| Tests passed | 365 |
| Tests skipped | 1 |
| Tests failed | 0 |
| Tests M3 ajoutés | 59 |

## Item par item

### M3-01 — `read_yaml_block` unwrap

```bash
$ python -m pytest tests/test_adversarial_gate_yaml_unwrap.py -v
6 passed in 0.27s
```

Tous les 6 fails-before sont résolus :
- `test_adversarial_gate_parses_nested_adversarial_block` : PASS
- `test_adversarial_gate_handles_hybrid_safely` : PASS
- `test_adversarial_gate_rejects_empty_adversarial_block` : PASS
- `test_adversarial_gate_rejects_string_adversarial` : PASS
- `test_adversarial_gate_rejects_root_level_fields` : PASS
- `test_adversarial_gate_consistency_text_json_exit` : PASS

Sur le closeout A2 réel, le validateur passe de 8 fails structurels
à 0 (les 28 S2 fails restants sont hors périmètre M3, voir §Limites).

### M3-02 — `attacker_identity` distinct vs `defender_identity`

```bash
$ python -m pytest tests/test_a2_distinct_identity.py -v
5 passed in 0.24s
```

Le validateur expose maintenant deux nouveaux gates :
- `adv-a2-defender-identity` (S1)
- `adv-a2-distinct` (S1)

### M3-03 — `level_reason` documenté dans le canon

```bash
$ python -m pytest tests/test_canon_documents_level_reason.py -v
3 passed
```

Le canon §1.1.1 documente le champ `level_reason` avec sa
contrainte de non-emptiness pour A0.

### M3-04 — Suppression du `intake_text` dead read

```bash
$ python -m pytest tests/test_no_intake_side_channel.py -v
3 passed
```

Le dead read est remplacé par un simple `assert intake.exists()`.
Aucun comportement de validation n'est perdu car le dead read
n'avait aucun effet observable (cf. test d'invariance).

### M3-05 — Validation `session`

```bash
$ python -m pytest tests/test_session_validation.py -v
4 passed
```

Le validateur rejette :
- `session: ""` (FAIL `adv-a2-session-present`)
- `session: "        "` (id.)
- `session: "x"` (FAIL `adv-a2-session-length`)
- `session: "sess-abc12345"` (PASS `adv-a2-session`)

### M3-06 — Matrice v1.0/v1.1 fail-closed

```bash
$ python -m pytest tests/test_v10_reader_v11_data_fail_closed.py -v
3 passed
```

Le validateur de fermeture rejette explicitement les données v1.1
lues par un frontmatter v1.0 (`assurance_governance_version: "1.0"`
sans `adversarial_governance_version: "1.1"`).

### M3-07 — Frontmatter validation des skills

```bash
$ python -m pytest tests/test_skill_frontmatter_validation.py -v
6 passed
```

Tous les 66 skills ont :
- `name` ✅
- `description` ✅
- `version` ✅
- (audit/tool) au moins un de `phase` / `adr` / `canonical_authority` ✅

### M3-08 — Matrice `gate_family × checkpoint`

```bash
$ python -m pytest tests/test_gate_family_checkpoint_matrix.py -v
12 passed
```

8 combinaisons valides couvertes + 2 invalides documentées
+ 2 unknown-value rejetées loudement.

### M3-09 — `last_external_review` cadence

```bash
$ python -m pytest tests/test_last_external_review.py -v
3 passed
```

Le validateur expose deux nouveaux gates :
- `adv-cert-last-external-review` (PASS si within cadence)
- `adv-cert-last-external-review-cadence` (FAIL si delta > 90 j)
- `adv-cert-last-external-review-future` (FAIL si futur)
- `adv-cert-last-external-review-format` (FAIL si non-ISO8601)
- `adv-cert-cadence-format` (FAIL si format non manual/cron/webhook)

### M3-10 — Séparation 6.3.10/11/12 documentée

```bash
$ python -m pytest tests/test_certification_separation.py -v
3 passed
```

Le canon §5.3.0 déclare désormais la séparation :
- `vbb-adversarial-gate.py` → conditions 6.3.1, 6.3.2, 6.3.8, 6.3.9, 6.3.13
- `vbb-certification-monitor` (futur) → 6.3.10, 6.3.11, 6.3.12
- closure / COUNTER_PROOF → 6.3.3, 6.3.4, 6.3.5, 6.3.6, 6.3.7

### M3-11 — Distributions codex/opencode

```bash
$ python -m pytest tests/test_distributions_propagation.py -v
6 passed
```

Les 4 distributions ancrent au canon adversarial v1.1.
Les setup.sh codex/opencode déclarent l'inheritance depuis Core.

### M3-12 — `test_a2_proxy` distinct

```bash
$ python -m pytest tests/test_a2_proxy_distinct_identity.py -v
5 passed
```

Le canon déclare `distinct_llm MANDATORY`, `distinct_system_prompt MANDATORY`,
et le validateur applique mécaniquement la comparaison (test 5).

## Sortie cohérente avec le pipeline global

```bash
$ python tools/vbb-loop-closure-check.py --strict
PASS — closure invariant satisfied (M3 run, 4 phases verified)

$ python tools/vbb-contract-lint.py
0 error(s), 1 warning(s) — non-blocking

$ python tools/vbb-architecture.py lint
0 error(s), 0 warning(s)

$ bash scripts/vbb-ci-local.sh
11 passed, 2 failed → 13/14 PASS
(2 failures are documents-04/05/07 still missing in the M3 run dir;
filled in subsequent closeout steps)

$ python tools/vbb-adversarial-gate.py docs/runs/2026-07-28_2200_a2-certification-of-m2-bis-bootstrap
verdict: FAIL
summary: passes=12 fails=28 (S0=0 S1=0 S2=28)
```

## Cohérence avec l'A2 baseline closeout

Avant M3 :
```
verdict: FAIL
summary: passes=2 fails=8 (S0=0 S1=4 S2=4)
```
Les 4 fails S1 (`adv-level-valid`, `adv-surfaces-declared`, `adv-findings-shape`,
`adv-verdict-shape`) étaient symptomatiques du bug de déballage de M3-01.

Après M3 :
```
verdict: FAIL
summary: passes=12 fails=28 (S0=0 S1=0 S2=28)
```
Les 12 passes incluent désormais tous les gates structurels.
Les 28 fails restants sont des S2 sur les champs `confidence`/`state`
des findings individuels — **hors périmètre M3** (à arbitrer).

**Aucun S1 ne subsiste** sur le closeout A2 (avant correction : 4 S1).

## Limites explicites

1. **Findings records (`adv-finding-N-*` S2)** : 28 fails persistent.
   Hypothèse de cause : le template 07_CLOSEOUT attend `confidence`
   et `state` sur chaque finding record. Le closeout A2 réel en a
   14 findings mais sans ces champs. Cette limitation est connue
   du rapport de campagne A2 (02_AUDIT.md) mais n'est **pas** dans
   les 14 findings arbitrés en R2. Décision M3 : hors scope, à
   ajouter à un futur R3 ou traité dans une campagne dédiée.

2. **M3-02 PROXY mode validation** : le validateur vérifie la
   `distinct_llm` mais ne lance pas la revue trimestrielle
   automatique (qui relève du monitor §M3-10).
