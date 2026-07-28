---
run_id: "2026-07-28_1400_m2-adversarial-loop-implementation"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "external implementer"
started_at: "2026-07-28T14:00:00Z"
ended_at: "2026-07-28T14:15:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md (this run)"
  - "M1_DECISIONS.md §M1-01..M1-06 + §8"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Ordre d'exécution M2

## Stratégie

Application des 37 entrées M2-01..M2-37 dans l'ordre de **dépendance
topologique** plutôt que dans l'ordre numérique. Les numéros M2-NN
restent la référence canonique pour la traçabilité ; l'ordre
d'exécution est :

### Tier 1 — Canon fondateur (sans dépendance aval)

- **M2-01** : rédiger `docs/adr/0051-adversarial-assurance-dimension.md` (ADR canonique) — *implémenté*
- **M2-02** : créer `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` (autorité domaine unique) — *implémenté*
- **M2-03** : étendre `docs/GATE_ASSURANCE_GOVERNANCE.md` (schéma 1.1 + COUNTER_PROOF + closure_evaluation) — *implémenté*

### Tier 2 — Canon opérationnel (consomme Tier 1)

- **M2-04..M2-06** : statuts (déjà dans ADR + autorité) — *implémenté par propagation Tier 1*
- **M2-07..M2-10** : déclencheurs + contest_register — *implémenté* (PILOTAGE.md §Triage étendu)
- **M2-11..M2-14** : `A2_DISTINCT_AGENT_PROXY` — *couvert dans autorité* ; *tests différés*
- **M2-15..M2-18** : `certification.owner` — *couvert dans autorité* ; *dashboard test différé*
- **M2-19..M2-21** : non-regression lock (`witnessed_by` + `test_review`) — *couvert dans autorité* ; *test différé*
- **M2-22..M2-23** : `CERTIFIED` 13 conditions — *couvert dans autorité* ; *13 tests différés*
- **CONVENTIONS.md** : P.R5 renforcé — *implémenté*
- **AGENTIC_RUN_PROTOCOL.md** : 3ᵉ profil review — *implémenté*
- **ENGINEERING_KNOWLEDGE_GOVERNANCE.md** : producer depuis findings — *implémenté*
- **pre-merge-gate.md** : corpus check `5b` — *implémenté*

### Tier 3..8 — Outillage, templates, skills, prompts, tests, distribution

Voir `M2_DEFERRED_ITEMS.md` (créé dans ce run). Chaque entrée M2-NN
différée porte : la décision M1 source, le livrable attendu, le numéro
de ticket pour le suivi, et le handoff prévu.

## Vérifications P.R2 (déjà green)

| # | Commande | Résultat |
|---|---|---|
| 1 | `python tools/vbb-architecture.py lint` | PASS — 0 errors, 11 blocks |
| 2 | `python tools/vbb-architecture.py graph --write` | PASS — RELATIONS.md régénéré |
| 3 | `python tools/vbb-contract-lint.py` | PASS — 0 errors |
| 4 | `python tools/vbb-loop-closure-check.py <run> --strict` | PASS (à exécuter ; voir §6 closeout) |
| 5 | `python -m pytest tests/ -q` | PASS — 255 passed, 1 skipped |
| 5b | Adversarial corpus check | **DIFFÉRÉ** (valideur et corpus pas encore créés) |

## Risques

- **DRIFT-M2** (S1) : un futur run modifie le canon fondateur sans
  transiter par M2-DEFERRED ou un nouveau M3.
- **DRIFT-CUTOFF** (S2) : les runs pré-cutoff ne déclarent pas
  `adversarial_governance_version: "1.1"` malgré le cutoff
  `2026-07-28T14:00:00Z`.
- **DRIFT-DISTRIB** (S2) : 4 distributions ne référencent pas la
  nouvelle autorité (CR#12).

Mitigation : tickets ouverts dans `M2_DEFERRED_ITEMS.md`.
