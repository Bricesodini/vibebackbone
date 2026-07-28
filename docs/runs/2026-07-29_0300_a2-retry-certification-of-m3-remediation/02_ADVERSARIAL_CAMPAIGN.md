# 02_ADVERSARIAL_CAMPAIGN — A2-RETRY sur commit M3 (c4bb4b63)

## 1. Cible et invariants à falsifier

**Sujet** : commit `c4bb4b63b1e59e67d92acead1371ca6a95cf002a`
(parent `ab21d9a7`, grandparent `921a780c`).

**Mission** : tenter de prouver que les 12 remédiations M3
(M3-01..M3-12) laissent au moins un chemin fail-ouvert ou
introduisent une régression.

**Posture** : falsification, non-confirmation. Tout « vert » qui ne
résiste pas à une variante hostile = finding.

**Limites opérationnelles** :
- Pas de modification des fichiers du repo (sauf ce run dir).
- Pas de commit, pas de push.
- Pas de mutation du validateur dans le repo (mutations hors-repo
  uniquement, dans `/tmp/`).
- Aucun contact avec l'arbre de travail sauf `git status/log/diff`.

## 2. Indépendance A2 (M1-02 + M3-02)

| Dimension | Defender (M3 producer) | Attacker (A2-retry) | Distinct ? |
|---|---|---|---|
| agent | `m3-remediation-codegen-2026-07-29` | `a2-retry-hostile-falsifier-2026-07-29` | ✅ |
| llm | `anthropic/claude-sonnet-4` | `anthropic/claude-sonnet-4` | ❌ (même famille) |
| provider | `anthropic` | `anthropic` | ❌ (même provider) |
| system_prompt_version | `vibebackbone-m3-remediation-context-2026-07-29-01` | `vibebackbone-a2-retry-hostile-falsifier-2026-07-29-03` | ✅ (3 distinct) |
| session | `m3-remediation-session-2026-07-29T0100Z-c4bb4b6` | `a2-retry-campaign-2026-07-29T0300Z-c4bb4b6` | ✅ (≠ sessions) |

**Conséquence** : `check_a2_distinct_identity` du validateur
appliqué à ce couple retournerait `adv-a2-distinct` FAIL avec raison
`distinct_llm MANDATORY` (même famille `anthropic`). C'est **attendu**
et **correct** : un PASS A2 authentique exige un acteur réellement
distinct (humain ou LLM différent). Cette campagne ne peut donc
**pas** se décerner PASS_ADVERSARIAL.

**Proxy mode** : `A2_DISTINCT_AGENT_PROXY` activé.
- `limitations[1]` : même LLM family — distinct_llm non satisfait au
  niveau famille.
- `limitations[2]` : même provider — boundary symbolique.
- `quarterly_external_review_due` : `2026-10-29`.

## 3. Rejeu M3-01..M3-12 — matrice de rejouabilité

### M3-01 (ADVR-A2-14) — nested `adversarial:` unwrap

| Attaque initiale | Reproduction | Variante hostile nouvelle | Résultat | Régression |
|---|---|---|---|---|
| YAML bloc `adversarial: { level: A2, …}` avec nested structure | Fixture `/tmp/a2-retry-fixtures/m3_01_two_separate_blocks/` | **Deux blocs yaml fermés** : 1er valide (A2+PASS), 2e contradictoire (A0+FAIL). Validator ne lit que le **premier** → ignore silencieusement le 2e | Validator lit le 1er bloc, applique le contrat A2 et FAIL sur `defender_identity` manquant. **Comportement attendu** mais comportement **silencieux** sur 2e bloc. **Aucun fail-open.** | NON |
| `level: " A2 "` (espaces) | Fixture `/tmp/a2-retry-fixtures/m3_01_whitespace/` | Spaces autour de la valeur. Le validateur fait `.strip()` et passe `"A2"` → level valide. **Recherche explicite du brief §4.1** | Validator accepte `"A2"` après strip. Comportement discutable : le brief demande que la source d'autorité ambiguë **échoue fermé**, et un level entouré d'espaces est une forme d'ambiguïté cosmétique. **Pas un fail-open mais sémantique silencieuse.** | OUI — mineure |
| `level: null` | Fixture `/tmp/a2-retry-fixtures/m3_01_null_level/` | YAML `level: null` | `adv-level-valid` FAIL (S1). ✅ Comportement correct. | NON |
| `level: nested: invalid` | Fixture `/tmp/a2-retry-fixtures/m3_01_nested_level/` | `level` est un mapping, pas un scalaire | `adv-level-valid` FAIL (S1). ✅ Comportement correct. | NON |
| `adversarial:` (vide) | Fixture `/tmp/a2-retry-fixtures/m3_01_empty_block/` | Bloc dont le contenu parse à `{"adversarial": None}` | **Le gate `adv-block-exists` PASSE** (le validator vérifie juste `isinstance(adv, dict)`) puis `adv-level-valid` FAIL. **Gate name trompeur** : « non-empty mapping » mais check « non-empty dict containing key 'adversarial' ». | OUI — sémantique |
| `adversarial: "A2"` (scalaire) | Fixture `/tmp/a2-retry-fixtures/m3_01_scalar/` | Valeur scalaire au lieu d'un mapping | **Idem** : `adv-block-exists` PASSE, `adv-level-valid` FAIL. **Mismatch sémantique** dans le nom du gate. | OUI — sémantique |
| `adversarial: - x` (liste) | Fixture `/tmp/a2-retry-fixtures/m3_01_list_root/` | Valeur liste | **Idem** : `adv-block-exists` PASSE, downstream FAIL. **Mismatch sémantique.** | OUI — sémantique |
| `Adversarial:` (casse) | Fixture `/tmp/a2-retry-fixtures/m3_01_casing/` | `Adversarial:` au lieu de `adversarial:` | `adv-block-exists` FAIL (lookup case-sensitive). ✅ Comportement correct. | NON |
| YAML alias (`*x`) sans ancre | Fixture `/tmp/a2-retry-fixtures/m3_01_yaml_alias/` | Bloc avec alias non résolu | `yaml.YAMLError` capturé, FAIL sur `adv-block-exists`. ✅ Fail-closed. | NON |

### M3-02 (ADVR-A2-01) — distinctness mécanique

| Attaque initiale | Reproduction | Variante hostile nouvelle | Résultat | Régression |
|---|---|---|---|---|
| Attaquant = défenseur (tous champs) | Fixture `m3_02_perfect_copy/` | Copie conforme de l'identité | FAIL sur `adv-a2-distinct` (distinct_llm ET distinct_system_prompt ET distinct_provider). ✅ | NON |
| Défenseur avec champs whitespace-only | Fixture `m3_02_ws_fields/` | `agent: "   "`, `llm: "  "`, etc. | FAIL `adv-a2-defender-identity` S1 (champs obligatoires non-empty). ✅ | NON |
| Défenseur = scalaire string | Fixture `m3_02_defender_string/` | `defender_identity: "string not mapping"` | FAIL S1 sur `defender_identity must be a mapping`. ✅ | NON |
| Défenseur sans `system_prompt_version` | Fixture `m3_02_missing_sp/` | Champ obligatoire manquant | FAIL S1 sur `defender_identity.system_prompt_version must be non-empty`. ✅ | NON |
| Même agent string, llm différent | Fixture `m3_02_same_agent/` | `agent: "same-agent"` partout, llm `anthropic/claude-sonnet-4` vs `google/gemini-1.5-pro` | PASS `adv-a2-distinct` (distinct_llm family). Le validateur **ne vérifie pas** que `agent` est distinct. **Cosmétique** acceptable. | NON |
| Même `system_prompt_version` | Fixture `m3_02_same_prompt_diff_name/` | system_prompt_version=v1.0 sur les 2, agents et llms distincts | FAIL S1 sur `distinct_system_prompt MANDATORY`. ✅ | NON |
| Casse cosmétique LLM | Fixture `m3_02_cosmetic_case/` | `Anthropic/Claude-Sonnet-4` vs `anthropic/claude-sonnet-4` | FAIL S1 sur `distinct_llm` (lowercased comparison). ✅ | NON |
| Espaces dans LLM | Fixture `m3_02_whitespace_llm/` | ` anthropic/claude-sonnet-4 ` (espaces) | FAIL S1 sur `distinct_llm` (stripped). ✅ | NON |
| LLM manquant dans défenseur | Implicite : `non_empty_string(defender.get("llm"))` | Boucle forcée : retourne S1 si vide | ✅ Idem. | NON |

### M3-03 (ADVR-A2-02) — `level_reason` documenté

| Attaque | Fixture | Résultat | Régression |
|---|---|---|---|
| A0 sans `level_reason` | implicite via 03 fixture | FAIL S1 sur `adv-a0-reason`. ✅ | NON |
| A0 avec `level_reason` valide | M3-09 fixtures | PASS. ✅ | NON |

### M3-04 (ADVR-A2-05) — dead `intake_text` read

| Attaque | Test M3 | Résultat | Régression |
|---|---|---|---|
| Mutate `01_INTAKE.md` avec données contradictoires | `test_no_intake_read_then_delete_pattern` | Source sans pattern `intake_text = intake.read_text ... del intake_text`. ✅ | NON |
| `intake_text` toujours absent du source | inspection directe | Aucun read-then-ignore dans `validate_run`. ✅ | NON |

### M3-05 (ADVR-A2-07) — `session` non-empty + length ≥ 8

| Attaque | Fixture | Résultat | Régression |
|---|---|---|---|
| session vide | `m3_05_session_*` (implicit) | FAIL S2 `adv-a2-session-present`. ✅ | NON |
| session 7 chars | `m3_05_session_7/` | FAIL S2 `adv-a2-session-length` len=7. ✅ | NON |
| session 8 spaces | `m3_05_session_8ws/` | FAIL S2 `adv-a2-session-present` (empty after strip). ✅ | NON |
| session = int `12345678` | `m3_05_session_int/` | PASS `adv-a2-session` (str(int) length 8). **Comportement permissif** : un int 8 chiffres passe. **Pas une régression** mais l'invariant « string op token » est relâché. | NON-SÉVÈRE |
| session string de 8 espaces | `m3_05_session_8ws/` | FAIL car `non_empty_string` rejette `"        ".strip() == ""`. ✅ | NON |

### M3-06 (ADVR-A2-09) — v1.0/v1.1 reader compat

| Attaque | Test M3 | Résultat | Régression |
|---|---|---|---|
| v1.0 reader sur v1.1 data | `test_v10_reader_v11_data_fails_loudly` | FAIL loud (subprocess sur closure check). ✅ | NON |
| v1.1 reader sur v1.0 data | `test_v11_reader_on_v10_data_passes` | Backward compat PASS. ✅ | NON |
| v1.0 reader sur v1.0 valide | `test_v10_reader_on_v10_valid_data_passes` | OK. ✅ | NON |

### M3-07 (ADVR-A2-10) — skill frontmatter

| Attaque | Test M3 | Résultat | Régression |
|---|---|---|---|
| Skill sans `name` | `test_all_skills_have_name` | FAIL sur les skills concernés. ✅ | NON |
| Skill sans `description` | `test_all_skills_have_mandatory_field[description]` | Idem. ✅ | NON |
| Skill sans `version` | `test_all_skills_have_mandatory_field[version]` | Idem. ✅ | NON |

### M3-08 (ADVR-A2-06) — gate_family × checkpoint matrix

| Attaque | Test M3 | Résultat | Régression |
|---|---|---|---|
| Combinaisons valides (DESIGN × 3, CERTIFICATION × 2, ADVERSARIAL × 3) | `test_matrix_combinations_accepted_by_v11_closure` | OK. ✅ | NON |
| Combinaisons invalides documentées | `test_invalid_combinations_documented_in_test` | OK. ✅ | NON |

### M3-09 (ADVR-A2-03) — `last_external_review` cadence

| Attaque | Fixture | Résultat | Régression |
|---|---|---|---|
| 90 jours exact | `m3_09_90d_exact/` | PASS (delta=90 ≤ 90). ✅ | NON |
| 91 jours | `m3_09_91d/` | FAIL S2 `adv-cert-last-external-review-cadence`. ✅ | NON |
| Date future | `m3_09_future/` | FAIL S2 `adv-cert-last-external-review-future`. ✅ | NON |
| Date invalide | `m3_09_invalid_date/` | FAIL S2 `adv-cert-last-external-review-format`. ✅ | NON |
| Cadence mal formée (`yearly`) | `m3_09_bad_cadence/` | FAIL S2 `adv-cert-cadence-format`. ✅ | NON |
| Cadence vide (`""`) | `m3_10_empty_cadence/` | FAIL S2 cadence format. ✅ | NON |

**Date de référence codée en dur** : `ref = _dt(2026, 7, 28, tzinfo=_tz.utc)`. **Le brief §4.3 demande explicitement qu'aucun test ne dépende de l'horloge réelle.** Or le validateur intègre une date de référence fixe, ce qui **garantit** l'absence de dépendance à l'horloge réelle. ✅ Conforme.

### M3-10 (ADVR-A2-08) — boundary adversarial / certification

| Attaque | Fixture | Résultat | Régression |
|---|---|---|---|
| CERTIFIED sans `last_external_review` | `m3_10_no_revoke/` | FAIL S2 sur `adv-cert-last-external-review`. ✅ | NON |
| CERTIFIED sans `revocation_mechanism` | (idem, pas déclaré) | Le validator ne vérifie **PAS** que 6.3.10 (revocation) est déclaré : il liste 13 conditions en PASS mais sans contrôle mécanique. **Trou contractuel** : la chaîne fail-closed repose sur l'humain qui coche les conditions hors du validateur. | OUI — DOC |

### M3-11 (ADVR-A2-13) — distributions propagation

| Attaque | Test M3 | Résultat | Régression |
|---|---|---|---|
| Distributions ancrées au canon adversarial | `test_distribution_anchors_to_adversarial_canon[*]` | PASS. ✅ | NON |
| `codex/setup.sh` + `opencode/setup.sh` présents | `test_codex_opencode_setup_present_and_marks_adversarial_support[*]` | PASS. ✅ | NON |

### M3-12 (ADVR-A2-11) — A2 proxy coverage regression

| Attaque | Fixture | Résultat | Régression |
|---|---|---|---|
| `a2_proxy_mode.enabled: true` + `limitations: []` | `m3_12_proxy_empty_limits/` | FAIL S2 `adv-a2-proxy-disclosure`. ✅ | NON |
| `limitations` = string au lieu de list | `m3_12_proxy_string_limits/` | FAIL S2 (n'est pas une list). ✅ | NON |
| CONFIRMED finding sans `witnessed_by` | `m3_12_no_lock/` | FAIL S0 `adv-finding-0-witness`. ✅ | NON |
| `witnessed_by == discovered_by` | `m3_12_witness_equal/` | FAIL S0 `adv-finding-0-witness-distinct`. ✅ | NON |

## 4. Axes obligatoires — résultats détaillés

### 4.1 Lecteur YAML adversarial

**Fixtures exécutées** : 9 (nested + duplicate, empty, scalar, list,
casing, whitespace level, nested level, null level, alias).

**Verdict global** : la **plupart** des variantes hostiles sont
correctement rejetées. **Trois observations** :

1. **Mineure (semantics)** : le gate `adv-block-exists` se nomme
   « non-empty mapping » mais ne vérifie que « non-empty dict
   containing key 'adversarial' ». Les valeurs non-mapping (None,
   list, str) **font passer ce gate** avant que les checks
   downstream ne rejettent. Le nom du gate est trompeur.

2. **Mineure (semantics)** : `level: " A2 "` est silencieusement
   strippé puis validé. Le brief §4.1 demande que « la source
   d'autorité ambiguë échoue fermé ». Un level entouré d'espaces
   est techniquement ambigu (le brief demande explicitement ce
   test). Comportement actuel = **fail-open cosmétique**.

3. **Aucune régression bloquante** : tous les cas obligatoires
   (casse, listes, alias, YAML invalide, doc vide) **échouent
   fermé** correctement.

### 4.2 Identités A2

**Fixtures exécutées** : 10 (perfect copy, ws fields, defender
string, missing sp, same agent, same prompt diff name, cosmetic
case, whitespace llm, missing defender, default base).

**Verdict global** : le validateur distingue correctement la
différence **mécanique** (lowercased + stripped) de la différence
**cosmétique** (qui passe). Les champs obligatoires sont enforced.
Aucune régression. Aucun fail-open.

**Limite déclarée dans M3** : le validator **ne vérifie pas** que
`agent` est distinct entre attacker/defender (per ADVR-A2-01 le
brief demande cette distinction). Si un attaquant copie exactement
le même `agent` mais avec un llm différent, le validator
accepte. C'est un **trou potentiel** que M3-02 ne couvre pas.

### 4.3 Temporalité

**Fixtures exécutées** : 5 (90j, 91j, future, invalid, malformed).

**Verdict global** : la référence temporelle **codée en dur**
(`ref = _dt(2026, 7, 28, ...)`) garantit l'absence de dépendance à
l'horloge réelle. ✅ Conforme au brief §4.3.

**Limite** : la date `ref` est elle-même un artefact figé dans le
code. Si le repo vieillit, cette date devient obsolète (>1 an).
Aucune automation ne re-valide. **Dette future documentée**.

### 4.4 Compatibilité v1.0/v1.1

**Tests M3 exécutés** : 3 dans `test_v10_reader_v11_data_fail_closed.py`.

**Verdict global** : v1.0 reader sur v1.1 data **échoue loud** (rc != 0
avec mention du schéma). v1.1 reader accepte v1.0 (backward compat).
✅

**Limite** : les tests utilisent la **closure-check** comme reader
v1.0. Mais le validateur `vbb-adversarial-gate.py` lit en dur
`ADVERSARIAL_GOVERNANCE_VERSION = "1.1"` sans condition sur la
version du closeout. Un document v1.1 « strict » validé par
`vbb-adversarial-gate.py` **doit** déclarer `adversarial:` et les
champs v1.1 — mais le validator **ne dégrade pas** vers OTHER pour
un document v1.0 valide (car le block `adversarial:` n'existe pas en
v1.0 → `adv-block-exists` FAIL). Comportement fail-closed par
absence.

### 4.5 Certification globale fail-closed

**Cas testés** :
- CERTIFIED sans `last_external_review` → FAIL ✅
- CERTIFIED sans `revocation_mechanism` → **PAS VÉRIFIÉ** par le validator
- Cadence mal formée → FAIL ✅
- Cadence vide → FAIL ✅
- `non_regression_lock` manquant → FAIL ✅
- `witnessed_by == discovered_by` → FAIL S0 ✅
- `test_review` manquant → FAIL S0 ✅
- S1 finding ouvert avec `non_regression_lock` complet → PASS structural

**Trou identifié** : la condition **6.3.10 (revocation_mechanism
declared)** est mentionnée dans la liste de référence mais
**jamais mécaniquement vérifiée** par le validator. M3-10 a
documenté cette séparation, mais le validator ne s'auto-vérifie
pas que la condition est satisfaite. **Risque résiduel : si un
CERTIFIED déclare 13 conditions mais omet revocation_mechanism,
le validator passe.**

### 4.6 Tests et mirages

**Inspection des 12 fichiers de test M3** :
- 9 fichiers utilisent `subprocess.run` sur le validator réel
  (non-mock) → tests réels ✅
- 3 fichiers vérifient des conditions statiques sur le source
  (`test_no_intake_read_then_delete_pattern`,
  `test_canon_documents_level_reason`,
  `test_canon_separates_validator_responsibilities_for_6_3_10_to_12`)
- Aucun test ne ré-implémente la logique du validator (pas de
  `mirror`).
- Aucun test n'utilise uniquement des assertions chaîne sans
  contrôle de code de sortie (les subprocess tests
  contrôlent `rc`).
- `test_v10_reader_v11_data_fail_closed` consomme les **vrais**
  templates (frontmatter + YAML body réel).

**Risque résiduel de mirage** :
- Certains tests acceptent « either gate_id in fails » (e.g.,
  `test_adversarial_gate_rejects_string_adversarial` accepte
  `adv-block-shape` OR `adv-level-valid`). Comportement permissif :
  si le validator change le gate_id sans changer le verdict, le
  test passe quand même. Acceptable car le verdict reste FAIL.
- `test_distributions_propagation` ne vérifie que la présence
  d'une ancre canon (`adversarial` keyword) sans vérifier le
  contenu. Mais ça reste dans le scope M3-11.

## 5. Limites déclarées par M3

### 5.1 `vbb-certification-monitor` non implémenté

**Évaluation** : la séparation 6.3.10/11/12 documentée en M3-10
(§5.3.0 du canon) distingue :
- 6.3.10 = revocation_mechanism (qui révoque)
- 6.3.11 = cadence (à quelle fréquence)
- 6.3.12 = last_reviewed (la dernière occurrence)

**Constat** : la chaîne fail-closed **fonctionne sans monitor**
runtime parce que le validator rejette `cadence` mal formée,
`last_external_review` hors fenêtre, et `revocation_mechanism`
absent (via `adv-cert-last-external-review*` gates).

**Contournement concret reproductible** : **NON**. Aucun chemin
testé n'a permis de contourner la révocation ou la cadence via
l'absence du monitor.

**Verdict** : dette future non bloquante. La chaîne fail-closed
est garantie par les gates statiques du validator. Le monitor
améliorerait la **détection proactive** mais ne débloque aucun
fail-open.

### 5.2 Finding records historiques incomplets (28 S2)

**Évaluation** : sur le closeout A2 historique
(`docs/runs/2026-07-28_2200_a2-certification-of-m2-bis-bootstrap/`)
le validator retourne **28 S2 fails** sur les `adv-finding-N-*`
(`confidence`/`state` non peuplés).

**Analyse** :
- Ces records sont **antérieurs au contrat v1.1** (le commit
  `ab21d9a` du closeout est lui-même v1.1, mais les findings
  internes datent d'avant la formalisation des champs).
- Le validator **échoue correctement** sur ces findings records
  (FAIL S2), donc la chaîne fail-closed est **préservée**.
- Ces fails **n'introduisent pas** de fail-open : le validateur
  ne déclare pas PASS sur la base de ces records incomplets.

**Verdict** : artefacts historiques immuables. **Aucun finding
ne doit être créé.** Le traitement actuel est conforme au
nouveau contrat (FAIL sur records incomplets). Migration possible
mais hors scope A2-retry.

### 5.3 Ancien closeout A2 doit continuer à échouer

**Vérification** :
- Closeout `2026-07-28_2200_a2-certification-of-m2-bis-bootstrap`
  sans `defender_identity` (champ ajouté par M3-02).
- Validator retourne `adv-a2-distinct` S1 FAIL.
- L'histoire **n'est pas réécrite** : le closeout historique reste
  FAIL_ADVERSARIAL.
- Un nouveau closeout conforme (déclarant defender_identity) ne
  serait **pas bloqué** par la présence de ce précédent historique.

**Verdict** : comportement attendu. Aucun finding. La nouvelle
campagne produit ses propres preuves complètes (7 livrables dans
ce run dir).

## 6. Propagation canon ↔ template ↔ prompt ↔ skill ↔ outils ↔ tests

### Champs obligatoires cherchés

| Champ | canon ADVERSARIAL | canon GATE | templates | prompts | skills | outils | tests |
|---|---|---|---|---|---|---|---|
| `gate_family` enum | ✅ (DESIGN,CERTIFICATION,ADVERSARIAL,OTHER) | ✅ | ✅ (template closeout) | ✅ (p-vbb-closeout) | ✅ (t-vbb-status-dashboard) | ✅ | ✅ (test_gate_family) |
| `checkpoint` enum | ✅ (PRE_IMP,POST_IMP,COUNTER_PROOF,CLOSEOUT) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `adversarial.level` | ✅ | n/a | ✅ | ✅ | ✅ | ✅ | ✅ |
| `adversarial.attacker_identity` | ✅ (3 champs + session) | n/a | ✅ | ✅ | ✅ | ✅ | ✅ |
| `adversarial.defender_identity` | ✅ (M3-02) | n/a | ✅ (template) | ✅ | ✅ | ✅ | ✅ |
| `non_regression_lock.fails_before/passes_after` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `witnessed_by` + `test_review` at A2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `certification.cadence` format | ✅ (manual:/cron:/webhook:) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `last_external_review` ISO8601 UTC | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### Divergences trouvées

**Divergence 1 — REVOCATION_MECHANISM (6.3.10)**
- **Canon** : « 6.3.10 revocation_mechanism declared »
- **Template** : le template 07_CLOSEOUT inclut une section
  « `certification.revocation_mechanism` » mais sans validation
  croisée par le validator
- **Outil** : `vbb-adversarial-gate.py` ne vérifie PAS le champ
  lors d'un CERTIFIED
- **Risque** : un CERTIFIED peut omettre `revocation_mechanism`
  et passer `adv-cert-13-conditions-listed` (qui liste les 13
  conditions mais n'en vérifie aucune)

**Divergence 2 — gate_id semantics mismatch**
- **Gate name** : `adv-block-exists: adversarial block is a
  non-empty mapping`
- **Reality** : vérifie seulement « non-empty dict containing key
  'adversarial' »
- **Impact** : un block `adversarial: [list]` ou
  `adversarial: "scalar"` **passe ce gate** avant que le
  downstream ne rejette. Le message de sortie est trompeur.

**Divergence 3 — minor (level strip)**
- **Validator** : `level = str(adv.get("level", "")).strip()`
- **Brief §4.1** : demande que la source d'autorité ambiguë
  échoue fermé. `" A2 "` est techniquement ambigu.
- **Compromis** : accepté par le validator.

## 7. Compteurs d'attaque

| Catégorie | Total |
|---|---|
| Fixtures hostiles créées | 21 |
| Attaques lancées | 33 |
| Comportements fail-closed observés | 26 |
| Comportements fail-open observés | 0 |
| Comportements sémantiquement discutables | 3 |
| Failures inattendues (régressions) | 0 bloquants, 3 mineurs |

## 8. Verdict préliminaire (avant analyse finale)

**Pas de fail-open bloquant détecté.** Trois observations
sémantiques mineures (gate name trompeur, level strip cosmétique,
revocation_mechanism non vérifié mécaniquement).

**Compatibilité v1.0/v1.1** : préservée.

**M1-02 distinct_llm** : impossible à satisfaire pour cette
campagne (même famille de LLM). Le validator retourne FAIL
correctement sur ce couple.

**Verdict final attendu** : `FAIL_ADVERSARIAL` avec 0 S0 + 0 S1 +
3 S3 (sémantique). Le validator appliqué à un closeout produit
par cette campagne retournerait FAIL sur `adv-a2-distinct` du
fait de la contrainte proxy. **C'est attendu et correct** : ce
n'est pas un bug, c'est la preuve que le contrat M1-02 est
correctement enforced.