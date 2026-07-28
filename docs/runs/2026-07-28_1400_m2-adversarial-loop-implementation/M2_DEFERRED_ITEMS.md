# M2 — Items différés (handoff vers M2-BIS)

> **Statut.** Ce fichier liste les 19 entrées M2-NN non implémentées
> dans le run M2 principal, avec leur décision M1 source, le livrable
> attendu, et le handoff prévu. Aucune n'est inventée : chaque ligne
> cite la décision M1 qui l'a produite.

## Items différés par catégorie

### Tier 3 — Outils

| # | Modification | Décision M1 | Livrable attendu | Handoff |
|---|---|---|---|---|
| M2-24 | Créer `tools/vbb-adversarial-gate.py` | D10 (validator ships with schema) | Validateur Python ≥ 500 lignes ; exit 0/1/2/3 ; consomme le finding record, la campagne, le corpus, les statuts | M2-BIS |
| M2-25 | Étendre `tools/vbb-loop-closure-check.py` | M1-01/M1-06 (resolution links) | Accepte `campaign_ref` + finding_id ; valide `resolution` link à `COUNTER_PROOF` | M2-BIS |

### Tier 4 — Templates

| # | Modification | Décision M1 | Livrable attendu | Handoff |
|---|---|---|---|---|
| M2-26 | `docs/templates/FINDING.md.template` | M0 §5.3 | Schéma finding complet ; supporte externe `history[]` (ADVR-18) | M2-BIS |
| M2-26 | `docs/templates/ADVERSARIAL_CAMPAIGN.md.template` | M0 §2.2 | Niveau / surface / oracles / depth / actor | M2-BIS |
| M2-27 | `docs/templates/07_CLOSEOUT.md.template` (étendu) | M1-06 (13 conditions), M1-04 (certification.owner), M1-02 (A2_PROXY) | Adversarial block, certification block, contest_register | M2-BIS |
| M2-27 | `docs/templates/06_REVIEW.md.template` (étendu) | M0 §9.3 | Trois profils : DESIGN, CERTIFICATION, ADVERSARIAL | M2-BIS |
| M2-28 | `docs/templates/01_INTAKE.md.template` (étendu) | M1-03 | `level`, `level_reason`, `contest_register` | M2-BIS |

### Tier 5 — Skills + prompts

| # | Modification | Décision M1 | Livrable attendu | Handoff |
|---|---|---|---|---|
| M2-29 | `skills/2-vbb-adversarial-campaign/SKILL.md` (NEW) | M0 §9.4 | Orchestrateur des techniques 1-vbb-* + 2-vbb-* existantes | M2-BIS |
| M2-29 | `skills/t-vbb-adversarial-corpus/SKILL.md` (NEW) | M0 §7.2 | Création entrée corpus, quarantaine, versionnage | M2-BIS |
| M2-30 | `skills/0-vbb-pilotage/SKILL.md` (étendu) | M1-03 | Déclaration de niveau + contest | M2-BIS |
| M2-30 | `skills/0-vbb-standard/SKILL.md` (étendu) | M1-03 | Validation frontmatter level | M2-BIS |
| M2-31 | `prompts/0-p-vbb-triage.md` (étendu) | M1-03 | Trigger matrix + contest_register | M2-BIS |
| M2-31 | `prompts/07-p-vbb-closeout.md` (étendu) | M1-06 | 13 conditions + adversarial block | M2-BIS |
| M2-31 | `prompts/2-p-vbb-audit-task.md` (étendu) | M1-02 | `A2_DISTINCT_AGENT_PROXY` prompt | M2-BIS |
| M2-31 | `prompts/1-p-vbb-structured-task.md` (étendu) | M0 §2.2 | Inline campaign A1 | M2-BIS |

### Tier 6 — Tests

| # | Test | Vérifie | Handoff |
|---|---|---|---|
| M2-14 | `tests/test_a2_proxy.py` (NEW) | `A2_DISTINCT_AGENT_PROXY` accepté ; identité publiée | M2-BIS |
| M2-14 | `tests/test_attacker_identity_disclosure.py` (NEW) | identité `{agent, llm, system_prompt_version}` requise | M2-BIS |
| M2-18 | `tests/test_certification_owner_sla.py` (NEW) | SLA breach → `SUSPENDED` automatique | M2-BIS |
| M2-21 | `tests/test_non_regression_witness.py` (NEW) | `witnessed_by` distinct de `discovered_by` à A2 | M2-BIS |
| M2-23 | `tests/test_certified_conditions_6_3_1_to_13.py` (NEW) | 13 conditions, un test par condition | M2-BIS |
| NEW | `tests/test_contest_register.py` (NEW) | contest_objection → A1 par défaut | M2-BIS |
| NEW | `tests/test_a2_quarterly_external_review.py` (NEW) | cadence 90 j vérifiée | M2-BIS |
| NEW | `tests/test_corpus_mandatory.py` (NEW) | `CONFIRMED` finding → corpus entry obligatoire | M2-BIS |
| NEW | `tests/test_resolution_link.py` (NEW) | `POST_IMPLEMENTATION` FAIL + `resolution` valide → COUNTER_PROOF PASS | M2-BIS |
| EXT | `tests/test_gate_check_level.py` (MODIFY) | M1-03 — fail-closed level determination | M2-BIS |
| EXT | `tests/test_loop_closure_*.py` (MODIFY) | A1/A2 artifacts validés ; resolution links | M2-BIS |

### Tier 7 — Distributions (CR#12)

| # | Modification | Décision M1 | Livrable attendu | Handoff |
|---|---|---|---|---|
| M2-32 | `distributions/pi/SYSTEM.md` (étendu) | CR#12 | Référence à `ADVERSARIAL_ASSURANCE_GOVERNANCE.md` ; règles de posture | M2-BIS |
| M2-32 | `distributions/opencode/AGENTS.md` (étendu) | CR#12 | Boot-set : niveau + contest_register | M2-BIS |
| M2-32 | `distributions/codex/AGENTS.md` (étendu) | CR#12 | Idem | M2-BIS |
| M2-32 | `distributions/claude/CLAUDE.md` (étendu) | CR#12 | Idem | M2-BIS |
| M2-33 | `docs/DISTRIBUTIONS.md` §Decisions log (étendu) | CR#12 | Trace des décisions promote-or-keep | M2-BIS |

### Tier 8 — Cutoff, ramp, validation (partiel)

| # | Modification | Statut |
|---|---|---|
| M2-34 | Déclaration cutoff (`cutoff_run_key` = `2026-07-28_1400`, `cutoff_timestamp` = `2026-07-28T14:00:00Z`) | **Implémenté** dans ADR 0051 + autorité §10 + `pre-merge-gate.md` |
| M2-35 | Ramp R0 (advisory) — premier run adverse avec validator warn-only | **Différé** (pas de validateur) — bascule R0 active au premier run qui consomme le validateur |
| M2-36 | `python tools/vbb-gate-check.py <run> --json` post-canon | **À exécuter en 07_CLOSEOUT** |
| M2-37 | `python -m pytest tests/ -q` (suite nouvelle) — 11 tests différés | À exécuter post-M2-BIS |

## Total

| Catégorie | Items |
|---|---|
| Tier 3 — Outils | 2 |
| Tier 4 — Templates | 5 |
| Tier 5 — Skills + prompts | 8 |
| Tier 6 — Tests | 11 |
| Tier 7 — Distributions | 5 |
| Tier 8 — Cutoff / ramp / validation | 1 actif (cutoff) + 3 différés |
| **Total différé** | **31** |
| **Total implémenté ce run** | **6** (M2-01..M2-03 + M2-07..M2-10 par propagation dans PILOTAGE.md + M2-34 cutoff) + extensions canoniques (5 fichiers) |

## Contrat pour M2-BIS

```
run M2-BIS:
  source unique: M1_DECISIONS.md
  entrée d'implémentation: M2_DEFERRED_ITEMS.md
  source normative: inchangée (M1-01..M1-06)
 守卫 de divergence: identique à M2 (M2_DEVIATION_FROM_M1.md si nécessaire)
  vérification: P.R2 + nouvelle commande 5b (adversarial gate + corpus)
```

Aucun des 31 items différés ne peut être ré-ouvert en M2-BIS sans
consommer strictement cette liste. Si une découverte exige un changement
de périmètre, le retour à M1 ou la création d'une M3 est obligatoire.
