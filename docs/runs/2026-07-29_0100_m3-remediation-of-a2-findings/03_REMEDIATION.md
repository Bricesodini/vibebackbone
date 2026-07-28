---
run_id: "2026-07-29_0100_m3-remediation-of-a2-findings"
phase: "03_REMEDIATION"
voie: "STRUCTURED"
status: "ACTIVE"
adversarial_level: "A2"
linked_subject:
  audited_commit: "ab21d9a70f03789c623893b200024f9876b7991b"
agent: "primary implementer"
started_at: "2026-07-29T01:00:00Z"
ended_at: "2026-07-29T01:30:00Z"
artifacts_consumed:
  - "02_FAILS_BEFORE.md (this run)"
artifacts_produced:
  - "03_REMEDIATION.md (this file)"
---

# 03_REMEDIATION — Corrections appliquées

## Stratégie

Pour chaque item M3-NN, la correction est appliquée **après** la preuve
fails-before documentée en `02_FAILS_BEFORE.md`. Toutes les corrections
sont **minimales** : un seul changement atomique par finding, sans
élargir le périmètre.

## Inventaire des changements

### Outils (`tools/`)

| Fichier | Lignes | Action | Item M3 |
|---|---|---|---|
| `tools/vbb-adversarial-gate.py` | 169-180 | `read_yaml_block` accepte toute ligne `marker:` (avec ou sans valeur), pas seulement `marker` exact | M3-01 |
| `tools/vbb-adversarial-gate.py` | 215-260 | Déballage explicite de `adversarial:` imbriqué + rejet du bloc vide | M3-01 |
| `tools/vbb-adversarial-gate.py` | 415-540 | Nouvelle fonction `check_a2_distinct_identity` validant la différence mécanique entre attacker et defender | M3-02 |
| `tools/vbb-adversarial-gate.py` | 495-540 | Ajout `session` aux A2 disclosures : non-empty + length ≥ 8 | M3-05 |
| `tools/vbb-adversarial-gate.py` | 1075-1180 | Nouvelle branche dans `check_certification_status` : validation `last_external_review` (ISO8601 UTC, cadence ≤ 90 j, pas futur) + cadence format check (manual/cron/webhook) | M3-09 |
| `tools/vbb-adversarial-gate.py` | 1115-1130 | Suppression du dead read `intake_text = intake.read_text(...)` ; remplacé par `assert intake.exists()` | M3-04 |

### Templates (`docs/templates/`)

| Fichier | Action | Item M3 |
|---|---|---|
| `docs/templates/07_CLOSEOUT.md.template` | Ajout `defender_identity`, `distinct_llm`, `distinct_system_prompt`, `distinct_provider_or_human`, `a2_proxy_mode` blocks | M3-02 |

### Canon (`docs/`)

| Fichier | Action | Item M3 |
|---|---|---|
| `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` | §1.1.1 : ajout d'une sous-section `level_reason` field (mandatory for A0) | M3-03 |
| `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` | §5.3.0 : ajout de la séparation des responsabilités entre validateurs (adversarial-gate vs monitor vs closure) | M3-10 |

### Distributions (`distributions/`)

| Fichier | Action | Item M3 |
|---|---|---|
| `distributions/codex/setup.sh` | Ajout commentaire en tête : "Adversarial governance (M3-11): ...inherits v1.1 from Core via AGENTS.md" | M3-11 |
| `distributions/opencode/setup.sh` | Ajout commentaire en tête : "Adversarial governance (M3-11): ...inherits v1.1 from Core via AGENTS.md" | M3-11 |

### Tests (`tests/`)

| Fichier | Tests | Item |
|---|---|---|
| `tests/test_adversarial_gate_yaml_unwrap.py` | 6 nouveaux tests | M3-01 |
| `tests/test_a2_distinct_identity.py` | 5 nouveaux tests | M3-02 |
| `tests/test_canon_documents_level_reason.py` | 3 nouveaux tests | M3-03 |
| `tests/test_no_intake_side_channel.py` | 3 nouveaux tests | M3-04 |
| `tests/test_session_validation.py` | 4 nouveaux tests | M3-05 |
| `tests/test_v10_reader_v11_data_fail_closed.py` | 3 nouveaux tests | M3-06 |
| `tests/test_skill_frontmatter_validation.py` | 6 nouveaux tests | M3-07 |
| `tests/test_gate_family_checkpoint_matrix.py` | 12 nouveaux tests | M3-08 |
| `tests/test_last_external_review.py` | 3 nouveaux tests | M3-09 |
| `tests/test_certification_separation.py` | 3 nouveaux tests | M3-10 |
| `tests/test_distributions_propagation.py` | 6 nouveaux tests | M3-11 |
| `tests/test_a2_proxy_distinct_identity.py` | 5 nouveaux tests | M3-12 |

**Total : 59 nouveaux tests** + 6 fixes de validateur/template/canon.

## Conformité M1

| Décision M1 | Statut M3 |
|---|---|
| M1-01 authority split strict | ✅ inchangé |
| M1-02 A2_DISTINCT_AGENT_PROXY | ✅ renforcé par M3-02 + M3-12 |
| M1-03 triggers | ✅ inchangé |
| M1-04 certification.owner SLA | ✅ implémenté partiellement par M3-09 (validation cadence + last_external_review) ; séparation monitor documentée en M3-10 |
| M1-05 non-regression lock | ✅ inchangé |
| M1-06 CERTIFIED 13 conditions | ✅ séparation documentée en M3-10 |

**Aucune déviation M1** — toutes les corrections opèrent strictement
à l'intérieur des décisions M1 ratifiées.

## Conformité R1

| Décision R1 | Statut M3 |
|---|---|
| PRE_CERTIFICATION + MIGRATION ratifiés | ✅ inchangé |
| SELF_HOSTING non retenu | ✅ inchangé |
| R1 §3 (CHOIX_ASSUMÉ PRE_CERTIFICATION sans expiration) | ✅ préservé via M3-14 NO_CHANGE |

## Conformité R2

| Item R2 | Statut M3 |
|---|---|
| Qualifications 1..14 | ✅ confirmées en `02_FINDING_ARBITRATION.md` |
| Sévérités confirmées/révisées | ✅ préservées |
| Bloquants certification | ✅ fermés (ADVR-A2-14 par M3-01 ; ADVR-A2-01 par M3-02) |
| Items NO_CHANGE (M3-13/M3-14) | ✅ documentés en §7 |
| Scope Claude Skills exclus | ✅ `distributions/claude/setup.sh`, `docs/DISTRIBUTIONS.md`, tests de distribution — **non modifiés** |

## Garde-fous

- **Aucun amend/rebase/squash/reset destructif** sur les commits existants.
- **Aucun push** pendant M3.
- **Aucune modification hors scope** détectée par `git diff` (cf. vérifications globales).
- **Aucun nouveau vocabulaire normatif** ajouté.
- **Aucune déviation M1**.

## Limite explicite

- Le validateur `vbb-adversarial-gate.py` continue de reporter 28 S2 fails
  sur les findings individuels du closeout A2 (`adv-finding-N-confidence`,
  `adv-finding-N-state`). Ces fails ne sont **pas** dans le périmètre M3 ;
  ils relèvent soit (a) d'un défaut de template (les findings A2 doivent
  déclarer `confidence` et `state`), soit (b) d'une découverte nouvelle à
  arbitrer en R3. **Décision M3 : hors scope**, à traiter dans un run
  ultérieur après ré-arbitrage humain.
