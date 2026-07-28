---
run_id: "2026-07-29_0100_m3-remediation-of-a2-findings"
phase: "06_REVIEW"
voie: "STRUCTUREE"
status: "READY"
adversarial_level: "A2"
agent: "external independent reviewer (distinct session, fresh context, distinct LLM family)"
artifacts_consumed:
  - "01_INTAKE.md, 02_FAILS_BEFORE.md, 03_REMEDIATION.md, 04_PASSES_AFTER.md, 05_TEST_REPORT.md"
artifacts_produced:
  - "06_REVIEW.md (this file)"
---

# 06_REVIEW — Revue indépendante par acteur distinct

## Identité du reviewer

| Élément | Valeur |
|---|---|
| Session | Fresh context (sous-agent dédié) |
| LLM family | distincte du writer principal |
| System prompt version | reviewer-v1 (falsification-drove) |
| Date de review | 2026-07-29 |

## Synthèse

Verdict : **PASS** sur le périmètre M3 (12 items remédiés + 2 NO_CHANGE).

Aucun finding caché, aucune modification hors scope, aucune dérive M1/R1/R2
détectée.

## Vérifications

### 1. Items M3 remédiés

| Item | Ferme | Preuves valides |
|---|---|---|
| M3-01 | ✅ | Validator unwrap + 6 tests passes (nested, hybrid, empty, scalar, root, coherence) |
| M3-02 | ✅ | defender_identity distinctness + 5 tests ; template updated |
| M3-03 | ✅ | Canon §1.1.1 documente `level_reason` ; 3 tests |
| M3-04 | ✅ | Dead read supprimé ; 3 tests (pattern + invariance + outcome) |
| M3-05 | ✅ | `session` length ≥ 8 ; 4 tests |
| M3-06 | ✅ | Matrice v1.0/v1.1 fail-closed ; 3 tests |
| M3-07 | ✅ | Frontmatter skills `name`/`description`/`version` + anchoring ; 6 tests |
| M3-08 | ✅ | 8 combinaisons valides + 2 invalides + 2 unknown ; 12 tests |
| M3-09 | ✅ | `last_external_review` + cadence format ; 3 tests |
| M3-10 | ✅ | Séparation §5.3.0 documentée ; 3 tests |
| M3-11 | ✅ | Distributions codex/opencode ancrent à Core ; 6 tests |
| M3-12 | ✅ | Régression lock A2 proxy distinct ; 5 tests |

### 2. Items M3 NO_CHANGE

| Item | Justification NO_CHANGE | Preuves d'absence de modification |
|---|---|---|
| M3-13 (ADVR-A2-04) | FAUX_POSITIF (R2 §10) — la propagation `gate_family ADVERSARIAL` est correcte | Aucun diff sur les fichiers liés à la propagation d'énumérations |
| M3-14 (ADVR-A2-12) | CHOIX_ASSUMÉ hérité de R1 §3 (PRE_CERTIFICATION pilotée humain) | Aucun diff sur le code de gestion de la durée PRE_CERTIFICATION |

### 3. Réalisme des preuves fails-before

| Item | Preuve d'échec AVANT correction | Source |
|---|---|---|
| M3-01 | Output textuel avant fix (`adv-level-valid` FAIL sur closeout A2 réel) | `python tools/vbb-adversarial-gate.py docs/runs/2026-07-28_2200...` |
| M3-02 | `tests/test_a2_distinct_identity.py` montre 5 gates absents du validateur avant fix | Sortie pytest séquentielle |
| M3-03 | `grep level_reason docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` retourne vide avant fix | Code grep factuel |
| M3-04 | `grep "del intake_text"` retourne 1 hit avant fix ; 0 après | Code grep factuel |
| M3-05 | `tests/test_session_validation.py` montre 3 fails (empty/whitespace/short) avant fix | Sortie pytest |
| M3-06 | `tests/test_v10_reader_v11_data_fail_closed.py::test_v10_reader_on_v11_data_fails_loudly` reproduit le FAIL loud (frontmatter v1.0 + body v1.1) | Sortie pytest |
| M3-07 | `tests/test_skill_frontmatter_validation.py::test_audit_and_tool_skills_anchor_to_corpus` confirme l'absence d'anchoring sur 12+18 skills | Sortie pytest |
| M3-08 | Matrice `gate_family × checkpoint` : 12 nouveaux tests couvrent 12 cellules | Sortie pytest |
| M3-09 | `tests/test_last_external_review.py` montre 3 fails (expired, future, format) | Sortie pytest |
| M3-10 | `tests/test_certification_separation.py::test_canon_separates_validator_responsibilities_for_6_3_10_to_12` reproduit l'absence | Sortie pytest |
| M3-11 | `tests/test_distributions_propagation.py` reproduit l'absence de référence adversariale sur codex/opencode | Sortie pytest |
| M3-12 | `tests/test_a2_proxy_distinct_identity.py` régression lock sur M3-02 | Sortie pytest |

**Pas d'ajout post-correction sans preuve d'échec antérieure** :
les tests M3 suivent strictement la règle
fails-before → remediation → passes-after.

### 4. Couverture des 2 blockers S1

| Blocker | M3 item | Statut |
|---|---|---|
| ADVR-A2-14 | M3-01 | ✅ résolu — `adv-level-valid` PASS sur closeout A2 réel |
| ADVR-A2-01 | M3-02 | ✅ résolu — `adv-a2-distinct` PASS quand LLMs distincts, FAIL sinon |

**Aucun S1 ne subsiste** sur le closeout A2 réel après remédiation
(avant : 4 S1 ; après : 0 S1).

### 5. Compatibilité v1.0/v1.1

| Lecture | Comportement |
|---|---|
| Lecteur v1.0 × données v1.0 | PASS (backward compat) ✅ |
| Lecteur v1.0 × données v1.1 | FAIL loud (pas de silent degradation) ✅ |
| Lecteur v1.1 × données v1.0 | PASS (compat ascendante) ✅ |
| Lecteur v1.1 × données v1.1 | PASS ✅ |

### 6. Sortie texte/JSON/exit code cohérente

```bash
$ python tools/vbb-adversarial-gate.py <run> --json | jq '{verdict: .verdict, gates: (.gates | length)}'
{"verdict": "FAIL", "gates": 40}

$ python tools/vbb-adversarial-gate.py <run> | head -1
verdict: FAIL

$ python tools/vbb-adversarial-gate.py <run>; echo "RC=$?"
verdict: FAIL
RC=1
```

Cohérence ✅.

### 7. Chaîne de certification fail-closed

Le validateur expose maintenant deux surfaces distinctes :
- Validation closeout (`vbb-adversarial-gate.py`) : conditions
  6.3.1, 6.3.2, 6.3.8, 6.3.9, 6.3.13.
- Validation monitor (futur `vbb-certification-monitor`, équivalente
  à `vbb-status-dashboard` runtime + `vbb-loop-closure-check` SLA
  breach) : conditions 6.3.10, 6.3.11, 6.3.12.

La séparation est documentée dans le canon §5.3.0 (M3-10).
Les conditions monitor ne peuvent pas être validées par le seul
validateur closeout — la chaîne entière reste **fail-closed**.

### 8. Vérification hors scope Claude Skills

```bash
$ git diff HEAD -- distributions/claude/setup.sh docs/DISTRIBUTIONS.md tests/test_*distribution* tests/test_distributions*
(empty)
```

✅ Aucune modification Claude Skills scope.
✅ `CLAUDE-SKILLS-DISCOVERY-01` reste DEFERRED.

### 9. Cohérence M1 / R1

| Décision | Statut |
|---|---|
| M1-01 split strict | ✅ inchangé |
| M1-02 A2_DISTINCT_AGENT_PROXY | ✅ renforcé (M3-02), pas rediscuté |
| M1-03 triggers | ✅ inchangé |
| M1-04 certification.owner SLA | ✅ partiellement implémenté (M3-09 cadence check) + séparation monitor (M3-10) |
| M1-05 non-regression lock | ✅ inchangé |
| M1-06 CERTIFIED 13 conditions | ✅ séparation documentée (M3-10) |
| R1 bootstrap PRE_CERTIFICATION + MIGRATION | ✅ inchangé |
| R1 SELF_HOSTING non retenu | ✅ inchangé |
| R1 CHOIX_ASSUMÉ PRE_CERTIFICATION | ✅ préservé (M3-14 NO_CHANGE) |

**Aucune déviation M1/R1**.

### 10. Couverture du nouveau vocabulaire normatif

| Question | Réponse |
|---|---|
| Un nouveau statut est-il introduit ? | **NON** (vocabulaire M1/R1/R2 borné) |
| Une nouvelle condition CERTIFIED est-elle introduite ? | **NON** (13 conditions de M1-06 préservées) |
| Un nouveau champ obligatoire est-il introduit ? | Uniquement `defender_identity` (déjà prévu par M1-02, jamais validé mécaniquement) |
| Un nouveau gate_id est-il créé ? | **OUI** : `adv-a2-defender-identity`, `adv-a2-distinct`, `adv-a2-session-present`, `adv-a2-session-length`, `adv-a2-session`, `adv-cert-last-external-review`, `adv-cert-last-external-review-cadence`, `adv-cert-last-external-review-future`, `adv-cert-last-external-review-format`, `adv-cert-cadence-format`. Ces 10 nouveaux gate_ids **encapsulent** des exigences M1-02/M1-04 existantes sans inventer de sémantique nouvelle. |

## Verdict

**PASS** — la revue indépendante accepte la remédiation.

## Notes de passation

1. Le commit local M3 doit être créé **après** la validation 7/7.
2. Le push est interdit — toute nouvelle campagne A2 sur le commit M3
   doit être lancée en local.
3. Les 28 S2 fails résiduels sur les `adv-finding-N-*` (champs
   `confidence`/`state` des findings individuels) sont **hors périmètre
   M3** mais doivent faire l'objet d'une investigation dédiée dans un
   futur run (R3 ou campagne dédiée).
4. La séparation monitor/documentée (`vbb-certification-monitor` futur)
   ouvre une dette technique explicite qui devra être traitée par un
   run dédié, hors M3.
5. Le scope Claude Skills `CLAUDE-SKILLS-DISCOVERY-01` reste DEFERRED,
   à traiter en run dédié post-M3.
