---
run_id: "2026-07-28_2300_r2-a2-arbitration-of-a2-findings"
phase: "03_M3_SCOPE"
voie: "AUDIT"
status: "ACTIVE"
kind: "M3_PERIMETER_DEFINITION"
posture: "define M3 scope only; do not start M3"
adversarial_level: "A2"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
linked_subject:
  audited_commit: "ab21d9a70f03789c623893b200024f9876b7991b"
  baseline_parent: "921a780ccf8299bc37099b377ce4e7d0d8ba2561"
  adversarial_verdict: "FAIL_ADVERSARIAL"
  checkpoint_aggregation: "0 S0 + 2 S1 + 6 S2 + 6 S3"
agent: "external arbitrator (distinct session, fresh context, distinct LLM family)"
artifacts_consumed:
  - "02_FINDING_ARBITRATION.md (this run)"
  - "docs/runs/2026-07-28_1200/.../M1_DECISIONS.md"
  - "docs/runs/2026-07-28_1800/.../03_DECISION.md"
artifacts_produced:
  - "03_M3_SCOPE.md"
---

# 03_M3_SCOPE — Périmètre M3 fermé et numéroté

> **Posture.** M3 est défini, pas démarré. R2 qualifie, M3
> corrige. Aucun code n'est modifié par R2.

## 0. Règles d'ordonnancement M3

1. **D'abord les reproductions échouantes** — chaque M3-NN
   commence par ajouter les tests fails-before du
   `02_FINDING_ARBITRATION.md` correspondant.
2. **Puis les corrections** — uniquement après que les tests
   fails-before sont écrits et effectivement en état FAIL.
3. **Puis passes-after** — exécution des tests corrects après
   application du correctif.
4. **Aucun finding confirmé n'est clos sans preuve** :
   ```
   fails-before  →  remediation  →  passes-after
   ```

## 1. Périmètre M3 — 14 items

### M3-01 — Corriger le validateur : `read_yaml_block` doit déballer la clé `adversarial:`

| Champ | Valeur |
|---|---|
| **Finding source** | ADVR-A2-14 (S1, BUG_IMPLEMENTATION + COUVERTURE_DE_TEST_INSUFFISANTE) |
| **Composant visé** | `tools/vbb-adversarial-gate.py` lignes 215-237 (`check_adversarial_block`) |
| **Type de changement** | M3_CODE — condition inversée à la ligne 232 |
| **Test fails-before** | `test_adversarial_gate_parses_nested_adversarial_block` (cf. 02_FINDING_ARBITRATION.md §1.A) |
| **Comportement passes-after** | Le validateur retourne `adv["level"] == "A2"` pour un bloc commençant par `adversarial:` ; tous les checks structurels `adv-level-valid`, `adv-surfaces-declared`, etc. retournent PASS. |
| **Critère de fermeture** | `pytest tests/test_adversarial_gate*` ✅ vert + `python tools/vbb-adversarial-gate.py docs/runs/2026-07-28_2200_a2-certification-of-m2-bis-bootstrap` retourne verdict cohérent (text, JSON, exit). |
| **Dépendances** | Aucune. **Item racine** du M3. |
| **Ordre d'exécution** | **1** (doit être corrigé en premier car tout autre check adversarial-gate dépend de ce déballage). |

### M3-02 — Valider l'indépendance `attacker_identity` vs `defender_identity`

| Champ | Valeur |
|---|---|
| **Finding source** | ADVR-A2-01 (S1, CONTRAT_INCOMPLET + COUVERTURE_DE_TEST_INSUFFISANTE) |
| **Composant visé** | `tools/vbb-adversarial-gate.py` lignes 307-340 (validation `attacker_identity`) ; `docs/templates/07_CLOSEOUT.md.template` (exposer `defender_identity`) |
| **Type de changement** | M3_CODE + M3_TEMPLATE + M3_TEST |
| **Test fails-before** | `test_adversarial_gate_rejects_identical_attacker_and_defender_llm` + `test_adversarial_gate_accepts_distinct_llm` (cf. 02_FINDING_ARBITRATION.md §2.A) |
| **Comportement passes-after** | (a) Le validateur FAIL si `attacker_identity.llm == defender_identity.llm` ; (b) PASS si LLMs distincts par family ; (c) `attacker_identity.session` présent et ≥ 8 chars ; (d) `attacker_identity.provider` distinct. |
| **Critère de fermeture** | Les 4 tests M3-02 verts + le contrat A2_DISTINCT_AGENT_PROXY (M1-02) est appliqué mécaniquement. |
| **Dépendances** | M3-01 (le validateur doit pouvoir déballer avant de checker l'identité). |
| **Ordre d'exécution** | **2** |

### M3-03 — Documenter `level_reason` dans le canon

| Champ | Valeur |
|---|---|
| **Finding source** | ADVR-A2-02 (S2, CONTRADICTION_DOCUMENTAIRE) |
| **Composant visé** | `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §3 ou §A0 |
| **Type de changement** | M3_DOCUMENTATION + M3_NORMATIVE_MINIMAL — déclarer le champ `level_reason` comme obligatoire pour A0 dans le canon |
| **Test fails-before** | `test_canon_documents_level_reason_for_a0` (cf. 02_FINDING_ARBITRATION.md §3.A) |
| **Comportement passes-after** | `grep "level_reason" docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` retourne ≥ 1 hit. |
| **Critère de fermeture** | Test unitaire vert + propagation canonique cohérente avec templates. |
| **Dépendances** | Aucune. |
| **Ordre d'exécution** | **3** |

### M3-04 — Supprimer la lecture morte ou implémenter les checks intake-side

| Champ | Valeur |
|---|---|
| **Finding source** | ADVR-A2-05 (S2, BUG_IMPLEMENTATION + COUVERTURE_DE_TEST_INSUFFISANTE) |
| **Composant visé** | `tools/vbb-adversarial-gate.py` lignes 882-887 (`validate_run`) |
| **Type de changement** | M3_CODE — soit supprimer `intake_text = ...; del intake_text`, soit implémenter le bloc `check_intake_adversarial_block` |
| **Test fails-before** | `test_adversarial_gate_validates_intake_adversarial_block` (cf. 02_FINDING_ARBITRATION.md §4.A) |
| **Comportement passes-after** | La cohérence entre `01_INTAKE.adversarial` et `07_CLOSEOUT.adversarial` est vérifiée (identity matching, level matching). |
| **Critère de fermeture** | Test vert + chemin mort supprimé ou checks intake-side implémentés. |
| **Dépendances** | M3-01 (le déballage doit fonctionner). |
| **Ordre d'exécution** | **4** |

### M3-05 — Valider `attacker_identity.session` (format minimal)

| Champ | Valeur |
|---|---|
| **Finding source** | ADVR-A2-07 (S2, BUG_NORMATIF) |
| **Composant visé** | `tools/vbb-adversarial-gate.py` lignes 307-340 |
| **Type de changement** | M3_CODE + M3_TEST — ajouter `session` aux `required` ; appliquer contrainte non-empty + length ≥ 8 |
| **Test fails-before** | `test_adversarial_gate_rejects_empty_session` (cf. 02_FINDING_ARBITRATION.md §5.A) |
| **Comportement passes-after** | `session: ""` ou `session: "x"` FAIL avec sévérité S2. |
| **Critère de fermeture** | Test vert + R1-§4 recordability améliorée. |
| **Dépendances** | M3-01. |
| **Ordre d'exécution** | **5** |

### M3-06 — Tester le rejet du v1.0 reader sur v1.1 data

| Champ | Valeur |
|---|---|
| **Finding source** | ADVR-A2-09 (S2, CONTRAT_INCOMPLET) |
| **Composant visé** | `tests/test_backward_compat_v1_0.py` ; `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §Schema 1.1 |
| **Type de changement** | M3_TEST + M3_DOCUMENTATION |
| **Test fails-before** | `test_v10_reader_on_v11_data_does_not_silently_degrade` (cf. 02_FINDING_ARBITRATION.md §6.A) |
| **Comportement passes-after** | Un v1.0 reader face à `gate_family: ADVERSARIAL` retourne FAIL avec `UnsupportedSchemaError` (pas de dégradation silencieuse en `OTHER`). |
| **Critère de fermeture** | Test vert + canon §Schema 1.1 clarifié. |
| **Dépendances** | Aucune. |
| **Ordre d'exécution** | **6** |

### M3-07 — Valider le frontmatter des skills (test_prompt_language)

| Champ | Valeur |
|---|---|
| **Finding source** | ADVR-A2-10 (S2, COUVERTURE_DE_TEST_INSUFFISANTE) |
| **Composant visé** | `tests/test_prompt_language.py` |
| **Type de changement** | M3_TEST — étendre la validation au frontmatter de chaque skill |
| **Test fails-before** | `test_prompt_language_validates_skill_frontmatter` (cf. 02_FINDING_ARBITRATION.md §7.A) |
| **Comportement passes-after** | Chaque skill déclare `name`, `description`, et (`level` ou `adversarial_level`) si applicable. |
| **Critère de fermeture** | Test vert + couverture de tous les 4 skills `2-vbb-` et `t-vbb-`. |
| **Dépendances** | Aucune. |
| **Ordre d'exécution** | **7** |

### M3-08 — Étendre la matrice `gate_family × checkpoint` (test_gate_check_level)

| Champ | Valeur |
|---|---|
| **Finding source** | ADVR-A2-06 (S3, COUVERTURE_DE_TEST_INSUFFISANTE) |
| **Composant visé** | `tests/test_gate_check_level.py` |
| **Type de changement** | M3_TEST — étendre à ≥ 8 combinaisons |
| **Test fails-before** | `test_gate_family_adversarial_with_pre_implementation_checkpoint` (cf. 02_FINDING_ARBITRATION.md §11.A) |
| **Comportement passes-after** | `ADVERSARIAL × PRE_IMPLEMENTATION` FAIL ; `ADVERSARIAL × COUNTER_PROOF` PASS. |
| **Critère de fermeture** | Test vert + matrice ≥ 8 combinaisons. |
| **Dépendances** | Aucune. |
| **Ordre d'exécution** | **8** |

### M3-09 — Valider `last_external_review` ≤ cadence (M1-04)

| Champ | Valeur |
|---|---|
| **Finding source** | ADVR-A2-03 (S3, CONTRAT_INCOMPLET) |
| **Composant visé** | `tools/vbb-adversarial-gate.py` (validation `last_external_review`) |
| **Type de changement** | M3_CODE + M3_TEST |
| **Test fails-before** | `test_adversarial_gate_validates_last_external_review` (cf. 02_FINDING_ARBITRATION.md §9.A) |
| **Comportement passes-after** | `last_external_review > now - 90 days` FAIL. |
| **Critère de fermeture** | Test vert + cadence validée. |
| **Dépendances** | M3-01. |
| **Ordre d'exécution** | **9** |

### M3-10 — Documenter la séparation 6.3.10/11/12 entre validateurs

| Champ | Valeur |
|---|---|
| **Finding source** | ADVR-A2-08 (S3, CONTRAT_INCOMPLET) |
| **Composant visé** | `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` §5.3 ; `docs/runs/2026-07-28_1200/.../M1_DECISIONS.md` M1-04 |
| **Type de changement** | M3_DOCUMENTATION + M3_NORMATIVE_MINIMAL — déclarer la séparation des responsabilités |
| **Test fails-before** | `test_certification_monitor_rejects_certified_without_revocation_mechanism` (cf. 02_FINDING_ARBITRATION.md §12.A) |
| **Comportement passes-after** | La séparation `vbb-adversarial-gate` ↔ `vbb-certification-monitor` est documentée. |
| **Critère de fermeture** | Test vert + canon clarifié. |
| **Dépendances** | Aucune. |
| **Ordre d'exécution** | **10** |

### M3-11 — Test cross-distribution codex/opencode

| Champ | Valeur |
|---|---|
| **Finding source** | ADVR-A2-13 (S3, CONTRAT_INCOMPLET) |
| **Composant visé** | `tests/test_distributions.py` (ou nouveau `tests/test_distributions_propagation.py`) |
| **Type de changement** | M3_TEST + M3_DOCUMENTATION |
| **Test fails-before** | `test_distributions_consistent_adversarial_handling` (à écrire) — vérifie que les 4 distributions exposent le même comportement face à un input adversarial. |
| **Comportement passes-after** | Test skip avec raison documentée si environnement codex/opencode non disponible localement. |
| **Critère de fermeture** | Test structuré + `docs/DISTRIBUTIONS.md` clarifié. |
| **Dépendances** | Aucune. |
| **Ordre d'exécution** | **11** |

### M3-12 — Test `attacker_identity` distinct (test_a2_proxy renforcée)

| Champ | Valeur |
|---|---|
| **Finding source** | ADVR-A2-11 (S2, COUVERTURE_DE_TEST_INSUFFISANTE) |
| **Composant visé** | `tests/test_a2_proxy.py` |
| **Type de changement** | M3_TEST — étendre la couverture pour vérifier la *différence* réelle |
| **Test fails-before** | Identique à M3-02. |
| **Comportement passes-after** | Test de la différence `attacker_identity.llm` vs `defender_identity.llm`. |
| **Critère de fermeture** | Tests verts. |
| **Dépendances** | M3-02. |
| **Ordre d'exécution** | **12** (post M3-02). |

### M3-13 — `NO_CHANGE` — ADVR-A2-04 (FAUX_POSITIF)

| Champ | Valeur |
|---|---|
| **Finding source** | ADVR-A2-04 (S3, FAUX_POSITIF) |
| **Action** | **Aucun correctif**. La propagation `gate_family ADVERSARIAL` est correcte. M3 conserve le record et le ferme dans la matrice. |
| **Test fails-before** | Aucun. |
| **Critère de fermeture** | Entrée fermée avec note `NO_CHANGE`. |

### M3-14 — `NO_CHANGE` — ADVR-A2-12 (CHOIX_ASSUMÉ)

| Champ | Valeur |
|---|---|
| **Finding source** | ADVR-A2-12 (S3, CHOIX_ASSUMÉ) |
| **Action** | **Aucun correctif**. R1 a tranché explicitement. |
| **Test fails-before** | Aucun. |
| **Critère de fermeture** | Entrée fermée avec note `NO_CHANGE — R1 assumed`. |

## 2. Tableau d'exécution M3

| Ordre | ID | Sév. | Destinations | Dépendances |
|---|---|---|---|---|
| 1 | M3-01 | S1 | M3_CODE + M3_TEST | — |
| 2 | M3-02 | S1 | M3_CODE + M3_TEST + M3_TEMPLATE | M3-01 |
| 3 | M3-03 | S2 | M3_DOCUMENTATION + M3_NORMATIVE_MINIMAL | — |
| 4 | M3-04 | S2 | M3_CODE + M3_TEST | M3-01 |
| 5 | M3-05 | S2 | M3_CODE + M3_TEST | M3-01 |
| 6 | M3-06 | S2 | M3_TEST + M3_DOCUMENTATION | — |
| 7 | M3-07 | S2 | M3_TEST | — |
| 8 | M3-08 | S3 | M3_TEST | — |
| 9 | M3-09 | S3 | M3_CODE + M3_TEST | M3-01 |
| 10 | M3-10 | S3 | M3_DOCUMENTATION + M3_NORMATIVE_MINIMAL | — |
| 11 | M3-11 | S3 | M3_TEST + M3_DOCUMENTATION | — |
| 12 | M3-12 | S2 | M3_TEST | M3-02 |
| 13 | M3-13 | S3 | NO_CHANGE | — |
| 14 | M3-14 | S3 | NO_CHANGE | — |

## 3. Vérification du périmètre M3

| Élément | Compte |
|---|---|
| Items M3 définis | 14 |
| Items S1 | 2 (M3-01, M3-02) |
| Items S2 | 5 (M3-03, M3-04, M3-05, M3-06, M3-07, M3-12) |
| Items S3 | 7 (M3-08, M3-09, M3-10, M3-11, M3-13, M3-14) |
| Items `NO_CHANGE` | 2 (M3-13, M3-14) |
| Items avec dépendances | 5 (M3-02, M3-04, M3-05, M3-09, M3-12) |
| Items sans dépendances | 9 |
| Items `M3_NORMATIVE_MINIMAL` | 2 (M3-03, M3-10) |
| Items `M1_DEVIATION` (=REQUIRES_HUMAN_REARBITRATION) | 0 |

## 4. Sortie de M3 — pré-conditions

Sortie de M3 ne peut être déclarée QUE si :

1. Tous les tests fails-before (M3-01 à M3-12) sont *passants*.
2. La cohérence texte/JSON/exit du validateur est établie
   (M3-01.D).
3. La cohérence canonique/validator est établie (M3-03, M3-10).
4. Aucune déviation M1 n'a été commise (vérifier contre §9.1
   M1_DECISIONS).
5. `python tools/vbb-adversarial-gate.py` retourne un verdict
   cohérent sur un closeout v1.1 canonique.
6. `python tools/vbb-loop-closure-check.py --strict` PASS.
7. `pytest tests/` 100% vert.
8. CI local 14/14 PASS.

## 5. Périmètre EXCLU de M3

### 5.1 Claude Skills discovery (scope indépendant)

| Élément | Valeur |
|---|---|
| **ID** | `CLAUDE-SKILLS-DISCOVERY-01` |
| **Fichier** | `distributions/claude/setup.sh` |
| **Symptôme** | La clé `settings.json 'skills'` est ignorée par Claude Code ; les skills Vibe Backbone ne sont pas découverts. |
| **Fix prévu** | Créer un symlink individuel par skill sous `~/.claude/skills/<name>`. |
| **Règle de propagation** | Claude-only glue ; aucune promotion Core requise, mais entrée obligatoire dans `docs/DISTRIBUTIONS.md` §Decisions log. |
| **Relation aux findings A2** | AUCUNE |
| **Politique de commit** | Commit séparé des remédiations A2. |
| **Statut R2** | **DEFERRED** — ne fait pas partie du M3 ci-dessus. Doit être traité dans un run dédié post-certification. |

R2 enregistre cette action différée **sans modifier** :

- `distributions/claude/setup.sh`
- `docs/DISTRIBUTIONS.md`
- les tests de distribution

### 5.2 M1 deviations

| Type | Compte |
|---|---|
| Deviations M1 proposées en R2 | 0 |
| Items `REQUIRES_HUMAN_REARBITRATION` | 0 |

R2 ne dévie pas de M1. Aucune décision M1 n'est ré-ouverte.
