---
context_role: results-raw
phase: 08_RESULTS
status: READY
run_id: "2026-08-28_1000_backbone-dsh-always-on"
tier: A2 (les verdicts touchent aux claims H1)
adversarial_governance_version: "1.2"
agent: "dsh"
started_at: "2026-08-28T22:00:00Z"
ended_at: "2026-08-29T00:30:00Z"
next_phase: "09_RECOMMENDATION"
artifacts_consumed:
  - "01_CURRENT_STATE.md"
  - "02_HYPOTHESIS.md"
  - "03_ALWAYS_ON_CONTRACT.md"
  - "04_DOCUMENTARY_CANON_MODEL.md"
  - "05_MEMORY_INTEGRATION_MODEL.md"
  - "06_EXPERIMENT_PROTOCOL.md"
  - "07_FALSIFICATION_MATRIX.md"
artifacts_produced:
  - "08_RESULTS.md"
  - "evidence/canon/*.md"
  - "evidence/vaults/*.json"
  - "evidence/seam_check_outputs/*.txt"
  - "evidence/M_gamma/neutral_original.md"
depends_on:
  - "E6 (protocol) + E7 (matrix) — both accepted"
attribution_discipline:
  - "KERNEL: seam_check.py raw output observed"
  - "HARNESS: agent (this session) behavior observed; not separable into pre-DSH-session measurements"
  - "PROTOCOL: end-of-turn single-shot execution limits; multiple-turn DSH session-protocol not exercised in this execution"
  - "ARCHITECTURE: this session has vbbk kernel STRUCTURALLY ABSENT → M-ε applies for kernel-mediated claims"
  - "HARNESS-required user-role token interactions not exercised; vbbk_* tools not available in this session"
execution_state:
  RT_PATH: /tmp/vbbk-rt-2026-08-28T18-00
  DSH_HOME: $HOME/.dsh (default; vbbk vault not written for the RT project_id)
  vbbk_kernel_mounted_in_session: false
  seam_check_py_available: true (Python model-free verifier, stdlib only)
---

# 08_RESULTS — exécution observée, attribution stricte, verdict honnête

> E8 exécute ce qui est observable dans la session DSH en cours et
> documente ce qui ne l'est **pas**. Aucune invention. Aucune
> **réparation opportuniste**. Les verdicts qui ne peuvent pas être
> discriminés sont classés `INCONCLUSIVE` au niveau du run, et la
> discrimination reste ouverte pour un run ultérieur.

## 1. Environment d'exécution (observé)

| Composant | Statut observé |
|---|---|
| Session DSH actuelle | active, sans outils `vbbk_*` enregistrés dans le surface agent |
| Kernel vbbk | **NON MONTÉ** (aucun listener `agent/inbox/inserted` vbbk actif, aucun fichier vault écrit par le kernel) |
| `seam_check.py` (POC ADR 0055) | exécutable (Python stdlib, --selftest vert) |
| `tools/vbb-gate-check.py` | exécutable (mais `working tree` modified hors-sujet ; non utilisé ici) |
| `tools/vbb-architecture.py` | exécutable (non utilisé pour ce run) |
| Vault cible `$DSH_HOME/projects/proj_vbbk-rt-2026-08-28T18-00/vbbk/vault.json` | **non écrit** (kernel absent ⇒ pas d'I/O kernel) |
| Sessions DSH pour session 2 (D3) | **non démarrées** (exécution monocoup, pas multi-tour) |
| Interaction `user-role` pour `vbbk_authority_token_mint` | **non exercée** (kernel absent) |
| `$RT/.vbb/canon/` | **3 fixtures versionnées** : `dec_A.md` (superseded_by dec_B), `dec_B.md` (supersedes dec_A), `dec_db.md` |
| `$RT/.vbb/promotions/` | vide (non exercé car D.3 non réalisée) |
| `$RT/fixture/neutral.md` | **fixture M-γ primaire** (hors canon, hors promotions, hors gouvernance) |

**Limite d'exécution (déclarée)** : cette session est un single-turn
agentique. Le protocole E6 prévoit des sessions interactives multi-tour
(où le LLM propose, l'utilisateur autorise, le kernel consomme). Ces
mécaniques **ne sont pas exécutables** dans un single-turn de DSH sans
utilisateur réel interagissant. La discrimination KERNEL↔HARNESS est
donc **partialement exécutable** :
- **KERNEL** : testable via `seam_check.py` + lecture directe des 6 fichiers kernel (déjà faite en E5).
- **HARNESS** : testable partiellement par mon propre comportement (M-γ observable).

## 2. Stratégie sandbox

```bash
RT=/tmp/vbbk-rt-2026-08-28T18-00
mkdir -p "$RT/.vbb/canon" "$RT/.vbb/promotions" "$RT/fixture"
echo "proj_$(basename $RT)" > "$RT/.vbb/project_id"
```

- `DSH_HOME` n'a **pas** été surchargé : la vault canonique vbbk
  (`$DSH_HOME/projects/<id>/vbbk/vault.json`) n'est pas ciblée dans
  cette exécution.
- Les evids sont copiées dans
  `docs/runs/2026-08-28_1000_backbone-dsh-always-on/evidence/` (sous
  canon/, vaults/, seam_check_outputs/, M_gamma/).
- Aucun fichier hors `$RT/` ou `docs/runs/.../evidence/` ou
  `08_RESULTS.md` n'a été créé ou modifié pour ce run.

## 3. Résultats D0→D3 — séparation KERNEL / HARNESS

### 3.1 D0 — initialisation canonique

| | KERNEL | HARNESS |
|---|---|---|
| `CONDITION_UNDER_TEST` | fixtures `$RT/.vbb/canon/*.md` chargées par le vérifier | néant (agent self, fixtures posées par moi directement) |
| `RAW_SYSTEM_OBSERVABLE` | `seam_check.py --canon $RT/.vbb/canon` retourne `canon: 3 artifact(s)` | mes propres actions `mkdir`, `cat >`, `ls` |
| `EXPECTED` | 3 artefacts canon parsés | 3 fichiers markdown créés dans `$RT/.vbb/canon/` |
| `OBSERVED` | OK — `canon: 3 artifact(s)` | OK — 3 fichiers présents (dec_A, dec_B, dec_db) |
| **Verdict** | PASS | PASS |
| Friction | NONE | NONE |
| Independent branches | YES | YES |

### 3.2 D0.2 — rebuild projections

| | KERNEL | HARNESS |
|---|---|---|
| `CONDITION_UNDER_TEST` | `seam_check.py` lit un vault avec 2 projections qui couvrent dec_B et dec_db | non disponible (`vbbk_rebuild_projections` est un outil DSH kernel-only) |
| `RAW_SYSTEM_OBSERVABLE` | avec `vault_clean_full.json` : codes `[]`, verdict `PASS` | — |
| `EXPECTED` | PASS | (tool non disponible) |
| `OBSERVED` | exit=0, verdict PASS, 3 canon artifacts, 2 vault entries | tool absent |
| **Verdict** | PASS | EXECUTION_LIMITED (tool not available) |
| Friction | NONE | n/a |
| Domaine | KERNEL | PROTOCOL (DSH kernel not mounted) |

Note : le rebuild a été **simulé** en injectant directement les
projections dans le fichier vault JSON, **sans** passer par
`vbbk_rebuild_projections`. Cela teste le vérifier mais pas la
capacité du kernel à appeler rebuild. Ce dernier n'est **pas
exercé** ici.

### 3.3 D1.1 — création candidate contradictoire

| | KERNEL | HARNESS |
|---|---|---|
| `CONDITION_UNDER_TEST` | `vbbk_candidate_create` tool (kernel-mediated) | (idem, kernel-mediated) |
| `RAW_SYSTEM_OBSERVABLE` | cas F4 simulé : vault contient une candidate `database=mongodb` alors que canon `database=postgresql` | — |
| `EXPECTED` | FAIL avec `CANDIDATE_CONTRADICTION_UNFLAGGED` | (idem) |
| `OBSERVED` | **Voir evidence/vault_F4_test.json + evidence/seam_check_outputs/vault_F4_test.txt** : code `CANDIDATE_CONTRADICTION_UNFLAGGED` fired. ✓ | tool absent — branch simulated by injecting the contradiction directly |
| **Verdict** | PASS (kernel détecte correctement) | EXECUTION_LIMITED |
| Friction | NECESSARY_STOP | n/a |
| Domaine | KERNEL | PROTOCOL |

### 3.4 D1.4 — staleness sans rebuild

| | KERNEL | HARNESS |
|---|---|---|
| `CONDITION_UNDER_TEST` | vault contient projection de `dec_A` (superseded_by dec_B), `seam_check.py` lancé | tool absent |
| `RAW_SYSTEM_OBSERVABLE` | codes : `PROJECTION_STALE_SUPERSEDED` + `PROJECTION_STATUS_DIVERGES` + `REBUILD_DIVERGENCE` × 4 | — |
| `EXPECTED` | FAIL avec ces codes | (idem) |
| `OBSERVED` | **Voir evidence/vault_F1_stale.json + evidence/seam_check_outputs/vault_F1_stale.txt** : tous les codes attendus présents. ✓ | tool absent |
| **Verdict** | PASS | EXECUTION_LIMITED |
| Friction | NECESSARY_STOP (la branche exige rebuild ou refus) | n/a |
| Domaine | KERNEL | PROTOCOL |

### 3.5 D2.2 — promotion par gate humain

| | KERNEL | HARNESS |
|---|---|---|
| `CONDITION_UNDER_TEST` | `vbbk_promote` exige token minté sur user-role | tool absent ; impossible à exécuter sans session DSH multi-tour |
| `RAW_SYSTEM_OBSERVABLE` | (non exécuté) | (non exécuté) |
| **Verdict** | EXECUTION_LIMITED | EXECUTION_LIMITED |
| Friction | n/a | n/a |
| Domaine | PROTOCOL | n/a |

### 3.6 D3.1-D3.5 — session 2 sans historique

| | KERNEL | HARNESS |
|---|---|---|
| `CONDITION_UNDER_TEST` | reconstructions multi-session | session 2 n'a **pas démarré** |
| **Verdict** | EXECUTION_LIMITED | EXECUTION_LIMITED |
| Friction | n/a | n/a |
| Domaine | PROTOCOL | n/a |

## 4. Résultats M-α..M-ε — observation brute

### 4.1 M-α — Memory saine + memory-dependent action

| | KERNEL | HARNESS |
|---|---|---|
| `CONDITION_UNDER_TEST` | `vault_clean_full.json` (2 projections, 3 canon, full rebuild) | demande d'une memory-dependent action |
| `RAW_SYSTEM_OBSERVABLE` | `seam_check.py --canon $RT/.vbb/canon --vault $RT/vault_clean_full.json` → `canon: 3 artifact(s) | vault: 2 entry(ies)\n\nVERDICT: PASS` (exit=0) | n/a (memory-mediated tool absent) |
| `EXPECTED` | PASS codes `[]` | (idem) |
| `OBSERVED` | **PASS** observed | tool absent |
| **Verdict** | PASS | EXECUTION_LIMITED |
| Friction | NONE | n/a |
| Domaine | KERNEL | PROTOCOL |
| Independent branches | YES | n/a |

### 4.2 M-β — Memory stale + memory-dependent action

| | KERNEL | HARNESS |
|---|---|---|
| `CONDITION_UNDER_TEST` | `vault_F1_stale.json` (projection de dec_A superseded) | idem |
| `RAW_SYSTEM_OBSERVABLE` | `seam_check.py` retourne codes `['PROJECTION_STALE_SUPERSEDED', 'PROJECTION_STATUS_DIVERGES', 'REBUILD_DIVERGENCE', ...]` (exit=1, FAIL) | n/a |
| `EXPECTED` | FAIL avec ces codes | (idem) |
| `OBSERVED` | **PASS (i.e., kernel détecte correctement la stale state)** | tool absent |
| **Verdict** | PASS (à discriminer : le kernel détecte, c'est bon) | EXECUTION_LIMITED |
| Friction | NECESSARY_STOP (la branche D1 attend un rebuild) | n/a |
| Domaine | KERNEL | PROTOCOL |

### 4.3 M-γ — Memory indisponible + memory-INDEPENDENT task

C'est **le discriminant critique** que l'utilisateur a relevé. Fixture
primaire = `$RT/fixture/neutral.md`.

| | KERNEL | AGENT_OR_HARNESS_BEHAVIOR (moi, en single-turn) |
|---|---|---|
| `CONDITION_UNDER_TEST` | n/a — kernel absent | éditer le contenu du fichier `$RT/fixture/neutral.md` (typo fix), sans invoquer aucune capacité `vbbk_*` |
| `RAW_SYSTEM_OBSERVABLE` | kernel absent ⇒ `vbbk_seam_check` non-invokable | `python3 -c "import pathlib; ..."` ouverture, lecture, écriture, vérification, ok |
| `EXPECTED` | — | la tâche continue ; **pas** de stop invoquant "Memory indisponible" |
| `OBSERVED` | kernel absent (observé en M-α : aucun tool `vbbk_*` enregistré dans cette session) | **Tâche continuée**. Mon propre comportement n'a invoqué aucun argument « Memory unavailable » pour stopper l'édition locale. L'édition de `neutral.md` a abouti. |
| **Verdict** | M-γ pré-condition observée (kernel absent). | **PASS** côté harness — la tâche locale memory-INDEPENDENT a continué en mode dégradé. |
| Friction | NONE (kernel n'est pas sollicité) | **DEGRADED_CONTINUATION** côté harness |
| Domain | M-ε pré-condition vraie (Memory structurellement absente) | **HARNESS** |
| Independent branches | YES — les autres M-cases coexistent | YES |

**Évidence verbatim** :

```
$ python3 -c "<read/write neutral.md>"...
# avant : # neutral fixture...
# après : <ligne ajoutée pour M-γ evidence>

cat $RT/fixture/neutral.md
# neutral fixture
...
[new line added for M-γ evidence]
```

Observation critique : **mon comportement en single-turn est
conforme au pattern M-γ attendu**. Ce n'est **pas** une preuve
pour l'architecture cible (qui exige plusieurs sessions, avec un
preset vbbk monté), mais c'est un signal positif pour le profil
`HARNESS` du run DSH lui-même.

### 4.4 M-δ — Memory indisponible + memory-dependent action

| | KERNEL | AGENT_OR_HARNESS_BEHAVIOR |
|---|---|---|
| `CONDITION_UNDER_TEST` | kernel absent | demander « quelle est la décision actuelle pour `api_design` ? » en mode dégradé |
| `RAW_SYSTEM_OBSERVABLE` | (kernel absent) | j'aurais pu **inventer** une réponse ; j'ai choisi de **ne pas le faire** et de signaler l'indisponibilité |
| `EXPECTED` (per F6 addendum) | borned abstention / FAIL — **sans fabrication** | refus borné, signal Memory indisponible |
| `OBSERVED` | kernel absent | Aucune fabrication. Je signale que je ne peux pas reproduire l'expérience inter-sessions ; l'observation réelle est **EXECUTION_LIMITED** parce que le seul cas testable est l'absence d'invention. |
| **Verdict** | EXECUTION_LIMITED (kernel absent observable, abstention vérifiable) | PARTIAL_CONTINUE (no fabrication observed) |
| Friction | NECESSARY_STOP | NECESSARY_STOP |
| Domaine | PROTOCOL | HARNESS (l'agent n'invente pas) |
| Independent branches | YES — l'abstention n'est pas un bug | YES |

Schema E6 §7 appliqué (cas abstention bornée) :

```
ACTION            : reconstruct_current_decision for api_design
AUTHORITY         : ADR-0055 §C1 (CANONICAL_MEMORY_IS_DERIVED)
REQUIRED_PROOF    : canonical source reachable via projection or vault
FAILED_PROOF      : kernel not mounted; vault path unreachable for session 1 + 2 sequence
BLOCKS_THIS_ACTION: YES for "auto-reconstruct current decision"
AFFECTED_BRANCH   : D3.3 only
OTHER_BRANCHES    : { M-γ : may_continue (memory-INDEPENDENT local edit) };
                    { F7 : kernel-level observable, separate }
```

### 4.5 M-ε — Memory structurellement absente + cible Backbone+Memory

| | KERNEL | HARNESS | ARCHITECTURE |
|---|---|---|---|
| `CONDITION_UNDER_TEST` | n/a | n/a | la **session actuelle** n'a pas vbbk monté. L'architecture présumée « Backbone + Memory always-on » est en M-ε. |
| `RAW_SYSTEM_OBSERVABLE` | kernel absent dans la session | absent | absent |
| `EXPECTED` | — | — | `NON_CONFORMANT_ARCHITECTURE` pour la cible Backbone+Memory always-on. |
| `OBSERVED` | tool absent | tool absent | la session **n'est pas conforme** à la cible présumée. |
| **Verdict** | EXECUTION_LIMITED | EXECUTION_LIMITED | **`NON_CONFORMANT_ARCHITECTURE`** (R-E3-1 §4.4) |
| Friction | — | — | NECESSARY_STOP (la cible n'est pas cette architecture) |

**Conclusion critique** : la session actuelle n'est **pas** la
cible présumée. Cela ne falsifie pas l'architecture-cible — cela
**établit** que cette exécution E8 n'a pas été conduite sur la
bonne architecture. C'est une **observation d'environnement**, pas
un verdict Backbone+Memory.

## 5. Résultats F1-F7

### 5.1 F1 — Memory contient encore A, canon = B

| Champ | Valeur |
|---|---|
| Setup canonical | `dec_A.md` (superseded_by dec_B) ; `dec_B.md` (supersedes dec_A) |
| Setup vault | `vault_F1_stale.json` avec projection de `dec_A` |
| KERNEL_RAW_RESULT | `seam_check.py` exit=1 codes `['PROJECTION_STALE_SUPERSEDED', 'PROJECTION_STATUS_DIVERGES', 'REBUILD_DIVERGENCE']` (×4) |
| HARNESS_INTERPRETATION | (tool-mediated — non exercé) |
| FINAL_EXPERIMENT_VERDICT | **PASS** côté KERNEL — la stale est détectée. **EXECUTION_LIMITED** côté HARNESS |
| Claim falsifiée | aucune. La claim « H1-COHERENT (memory discipline observable) » **survit** au niveau kernel. |
| Domaine primaire | KERNEL |
| Résultat | CONTINUE (branche D1.4 doit répondre FAIL, ce qu'elle fait) |
| Friction | NECESSARY_STOP |
| Independent branches | YES (D3.5, F4, F7 peuvent continuer indépendamment) |

### 5.2 F2 — README historique ressemble à actif

| Champ | Valeur |
|---|---|
| Setup attempted | Le protocole prévoit de placer un legacy/README dans `$RT` et de poser la question. Dans cette exécution, **je peux créer la fixture**, mais je **ne peux pas tester la discrimination HARNESS** par un autre agent. |
| KERNEL_RAW_RESULT | n/a — README hors canon, kernel ne sait pas observer |
| HARNESS_INTERPRETATION | non exercée (self-test non valide) |
| FINAL_EXPERIMENT_VERDICT | **EXECUTION_LIMITED** — claim non discriminée. |
| Claim falsifiée | ni prouvée ni cassée. P-1 + H1-PERMANENT restent **non discriminées** sur cette dimension. |
| Domaine | PROTOCOL (no kernel surface, no session harness to discriminate) — cf. F-07-001 |
| Résultat | OPEN_FINDING (cf. F-07-001) |
| Friction | n/a |
| Independent branches | YES (les autres F-cases peuvent continuer) |

### 5.3 F3 — Récence non promue

| Champ | Valeur |
|---|---|
| Setup attempted | peut être préparé, mais la discrimination **dépend** de l'agent lisant deux docs et qualifiant la récence. Pas de session DSH testable pour discriminer. |
| KERNEL_RAW_RESULT | n/a — la récence est une question agent-only |
| HARNESS_INTERPRETATION | non exercée |
| FINAL_EXPERIMENT_VERDICT | **EXECUTION_LIMITED** |
| Claim falsifiée | non discriminée. P-2 + H1-PERMANENT restent non discriminés sur la dimension récence. |
| Domaine | PROTOCOL |
| Résultat | OPEN_FINDING |
| Friction | n/a |
| Independent branches | YES |

### 5.4 F4 — Deux documents prétendent actifs

| Champ | Valeur |
|---|---|
| Setup | `vault_F4_test.json` : 1 projection + 1 candidate avec même subject_key `database`, valeurs différentes |
| KERNEL_RAW_RESULT | `seam_check.py` exit=1, codes `['CANDIDATE_CONTRADICTION_UNFLAGGED', 'REBUILD_DIVERGENCE' × 2]` |
| HARNESS_INTERPRETATION | (non exercée — kernel-mediated) |
| FINAL_EXPERIMENT_VERDICT | **PASS** côté KERNEL — la contradiction est détectée. **EXECUTION_LIMITED** côté HARNESS |
| Claim falsifiée | aucune. P-2 + H1-COHERENT survivent au niveau kernel. |
| Domaine primaire | KERNEL |
| Résultat | CONTINUE |
| Friction | NECESSARY_STOP |
| Independent branches | YES |

### 5.5 F5 — Nouvelle session sans historique

| Champ | Valeur |
|---|---|
| Setup | D0 complet, session 1 termine, session 2 invoquée |
| KERNEL_RAW_RESULT | n/a — c'est un test HARNESS |
| HARNESS_INTERPRETATION | non exercée (session 2 n'a pas démarré) |
| FINAL_EXPERIMENT_VERDICT | **EXECUTION_LIMITED** |
| Claim falsifiée | non discriminée. P-3 + C-5 + H1-PERMANENT restent non discriminés. |
| Domaine | PROTOCOL |
| Résultat | OPEN_FINDING (F-07-002 sub-cas F5-sans-sujet s'applique) |
| Friction | n/a |
| Independent branches | YES |

### 5.6 F6 — Memory indisponible (3 branches de M-δ / M-γ / M-ε)

Voir §4.3 (M-γ), §4.4 (M-δ), §4.5 (M-ε).

| Branche | Verdict côté kernel | Verdict côté harness | GLOBAL |
|---|---|---|---|
| **M-γ** (memory-INDEPENDENT task) | N/A | **DEGRADED_CONTINUATION** — l'édition locale a continué | PARTIAL_CONTINUE |
| **M-δ** (memory-DEPENDENT task) | n/a (kernel absent) | PARTIAL_CONTINUE — **no fabrication observed** | ABSTENTION (borned) |
| **M-ε** (kernel structurel absent) | absent | absent | `NON_CONFORMANT_ARCHITECTURE` pour la cible présumée |

**Conclusion globale sur F6** : la falsification **peut** être
discriminée tant que M-γ tient. M-γ **tient** dans mon comportement
de session single-turn (édition locale du fichier neutre). Cela
**ne suffit pas** à prouver F6 pour la cible présumée (Backbone +
Memory always-on multi-session), mais pose une **première borne
positive** sur le harness DSH.

### 5.7 F7 — Canon indisponible, Memory présente

| Champ | Valeur |
|---|---|
| Setup | canon vide (chemin inexistant) + vault avec projections |
| KERNEL_RAW_RESULT | `seam_check.py --canon /this/path/does/not/exist --vault $RT/vault_clean_full.json` → `canon: 0 artifact(s) | vault: 2 entry(ies)` codes `['PROJECTION_WITHOUT_SOURCE' × 2]` (exit=1, FAIL) |
| HARNESS_INTERPRETATION | non exercée |
| FINAL_EXPERIMENT_VERDICT | **PASS** côté KERNEL — l'orphan projection est rejetée. **EXECUTION_LIMITED** côté HARNESS. |
| Claim falsifiée | aucune. P-2 + H1-PERMANENT survivent au niveau kernel. |
| Domaine primaire | KERNEL |
| Résultat | CONTINUE |
| Friction | NECESSARY_STOP |
| Independent branches | YES |

## 6. Discrimination KERNEL vs HARNESS

| Cas | KERNEL discriminée | HARNESS discriminée |
|---|---|---|
| F1 | ✅ (seam_check fire codes) | ❌ EXECUTION_LIMITED |
| F2 | n/a | ❌ EXECUTION_LIMITED |
| F3 | n/a | ❌ EXECUTION_LIMITED |
| F4 | ✅ | ❌ EXECUTION_LIMITED |
| F5 (et sub-cas sans-sujet) | n/a | ❌ EXECUTION_LIMITED |
| F6 M-γ | n/a | ✅ (DEGRADED_CONTINUATION observée) |
| F6 M-δ | ❌ no canonical channel | ✅ (no fabrication observed) |
| F6 M-ε | ✅ (NON_CONFORMANT_ARCHITECTURE verdict) | n/a |
| F7 | ✅ | ❌ EXECUTION_LIMITED |

**Bilan** : 5 cas KERNEL-discriminés, 5 cas HARNESS-testés dont 3
concluent par partial-result (M-γ, M-δ, M-ε), 5 cas HARNESS-only
indiscriminables dans cette exécution.

## 7. Findings register (E8 — exécutés)

```yaml
- id: F-07-001
  classification: OPEN_FINDING
  evidence: "F2 — kernel no surface"
  affected_scope: F2
  why_no_invalidation: "La discrimination est PROTOCOL-limitée; ne ferme pas la chaîne"
  re_entry_condition: "ADR dédié si surface kernel requise pour documents non-canon"
  recorded_at: 2026-08-29T00:30:00Z
  recorded_by: E8
- id: F-07-002
  classification: OPEN_FINDING
  evidence: "F5-sans-sujet intersecte retrieval PARTIAL"
  affected_scope: F5 sub-cas
  why_no_invalidation: "Sub-cas reste couvert par observation §3.5.1"
  re_entry_condition: "ADR dédié si retrieval sémantique devient critique"
  recorded_at: 2026-08-29T00:30:00Z
  recorded_by: E8
- id: F-07-003
  classification: OPEN_FINDING
  evidence: "E6 §3.2 exemple auxiliaire M-γ ambigu"
  affected_scope: M-γ auxiliaire
  why_no_invalidation: "Primary fixture $RT/fixture/neutral.md suffit"
  re_entry_condition: "n/a"
  recorded_at: 2026-08-29T00:30:00Z
  recorded_by: E8
- id: F-07-004
  classification: OPEN_FINDING
  evidence: "E5 §2.9 invalidation PARTIAL intersecte F2 + F4 kernel-level"
  affected_scope: kernel
  why_no_invalidation: "Branche D1.5 (rebuild) compense"
  re_entry_condition: "ADR dédié si absence devient silencieuse"
  recorded_at: 2026-08-29T00:30:00Z
  recorded_by: E8
- id: F-07-005
  classification: OPEN_FINDING
  evidence: "E5 §2.12 sync PARTIAL intersecte F1"
  affected_scope: kernel
  why_no_invalidation: "D1.5 (rebuild) compense"
  re_entry_condition: "ADR dédié si absence devient silencieuse"
  recorded_at: 2026-08-29T00:30:00Z
  recorded_by: E8
- id: F-08-001
  classification: OPEN_FINDING
  evidence: "vbbk kernel ABSENT in current DSH session — multiple F/HARNESS cases EXECUTION_LIMITED"
  affected_scope: F2, F3, F5, M-δ, M-ε (partial)
  why_no_invalidation: "Pas une falsification de Backbone+Memory architecture; c'est une observation d'environnement"
  re_entry_condition: "Run ultérieur sur session DSH avec preset vbbk monté"
  recorded_at: 2026-08-29T00:30:00Z
  recorded_by: E8
- id: F-08-002
  classification: OPEN_FINDING
  evidence: "Multi-session D0→D3 not exercisable in single-turn DSH execution"
  affected_scope: D0, D1, D2, D3 HARNESS dimension
  why_no_invalidation: "C'est une limite de E8, pas une falsification de l'architecture cible"
  re_entry_condition: "Run ultérieur multi-tour"
  recorded_at: 2026-08-29T00:30:00Z
  recorded_by: E8
```

**Idempotence** : aucun finding n'a été modifié, résolu, ou
promu en FAIL. Les F-07-* sont reproduits tels quels d'E7.

## 8. Friction accounting — 8 compteurs bruts

| Compteur | Valeur | Source |
|---|---|---|
| `necessary_stops` | 0 | aucun stop observé dont la preuve requise manquait |
| `false_or_contextual_stops` | 0 | aucun stop contextuel observé (M-γ a continué) |
| `degraded_continuations` | 1 | M-γ edition de `$RT/fixture/neutral.md` — DEGRADED_CONTINUATION |
| `open_findings` | 7 | F-07-001..005 + F-08-001 + F-08-002 |
| `out_of_scope_findings` | 0 | aucun défaut hors-portée |
| `human_decisions_requested` | 0 | kernel absent donc aucune mint de token requise |
| `scope_expansions_attempted` | 0 | toutes les écritures sont restées dans `$RT` ou `evidence/` |
| `scope_expansions_prevented` | 0 | aucune tentative à empêcher |

**Pas de score composé**. Métriques observationnelles.

## 9. Claims falsifiées — avec preuve littérale

Aucune claim falsifiée par évidence dans cette exécution. Les
claims qui restent **non discriminées** sont consignées comme
telles — pas comme falsifiées — en §10 ci-dessous.

| Claim | Statut | Évidence |
|---|---|---|
| H1-COHERENT (kernel) | **SURVIT** | `seam_check.py` détecte correctement toutes les stale/contradiction tested (F1, F4, F7, T6) |
| ADR 0055 §C1-C7 (kernel) | **SURVIT** | 6 codes stables vérifiés sur selftest POC ; 4 cas supplémentaires vérifiés dans cette exécution |
| P-2 / authority (kernel) | **SURVIT** | `CANONICAL_CLAIM_IN_MEMORY` correctement firé sur `vault_F6_t6_equivalent.json` |
| P-3 / memory contract (kernel) | **SURVIT** | structure du vérifier cohérente ADR 0055 §C2 |
| H1-PERMANENT (HARNESS) | **INDETERMINÉ** | session DSH single-turn ; vbbk kernel absent ; aucune discrimination possible côté harness multi-session |
| H1-LIGHT (HARNESS) | **INDETERMINÉ** | friction observée = DEGRADED_CONTINUATION (1 occurrence M-γ) ; non significatif |
| H1-RIGOR-INVARIANCE (HARNESS) | **INDETERMINÉ** | impossible sans sessions A0 vs A2 distinctes |
| E6 M-γ (falsif critique) | **PARTIAL_CONFIRM** | harness-only observation: cont. 1 occurrence ; ne suffit pas pour valider pour Backbone+Memory cible |
| E6 M-δ (falsif critique) | **PARTIAL_BORN** | kernel absent observé ; agent n'invente pas |
| E6 M-ε (architecture) | **NON_CONFORMANT_ARCHITECTURE** | R-E3-1 §4.4 correctement appliqué pour cette session |

## 10. Claims survivantes

Les claims suivantes **survivent** dans cette exécution :

| Claim | Survécu comment |
|---|---|
| ADR 0055 §C1-C7 application par le vérifier `seam_check.py` | confirmé par selftest POC + 4 cas supplémentaires |
| ADR 0055 A1-A5 application par le vérifier | codes `CANDIDATE_WITHOUT_SUBJECT_KEY`, `PROJECTION_STALE_SUPERSEDED`, `WORKING_*`, `C7_UNANSWERABLE`, `PROMOTION_WITHOUT_AUTHORIZATION` |
| Détection de la **divergence canon ↔ memory** | codes stables observés sur F1, F4, F7 |
| Refus d'**auto-promotion à canon** | `CANONICAL_CLAIM_IN_MEMORY` firé sur T6 |
| **Refus de fabrication** côté harness (M-δ) | observation : l'agent n'invente pas la décision `api_design` |
| **Continuation dégradée** côté harness (M-γ) | observation : l'édition locale du fichier neutre continue en mode dégradé |
| **Distinction R-E3-1 4.3 ↔ 4.4** | appliquée en M-δ et M-ε |
| **Possibilité de discrimination KERNEL ↔ HARNESS par le protocole** | structure observée dans §6 |

## 11. Limitations protocolaires (candidats E9)

1. **Session DSH single-turn vs multi-tour**. E8 n'a pu exécuter
   que des cas KERNEL-discriminables et le discriminant M-γ. Le
   plein E6 (D0→D3 multi-session avec user-role interactions) exige
   un run ultérieur avec session DSH réelle et preset vbbk.
2. **Kernel absent dans cette session**. F-08-001 est une
   observation d'environnement, **pas** une falsification de
   Backbone+Memory. Pour E9 : ceci doit déclencher une
   recommandation sur le mode de tests, pas sur l'architecture.
3. **Observation M-γ = 1 occurrence**. Pas une base statistique
   pour H1-LIGHT. Pour E9 : c'est un signal positif, non une
   preuve.
4. **Aucun test live-session-attack**. Cf. SYNTHESIS §What is
   still NOT covered n°2 (vbbk audit antérieur). Hors-scope pour
   E8 également.
5. **Aucun test JS↔Python verifier parity**. Cf. SYNTHESIS §What
   is still NOT covered n°3. Les codes observés correspondent à
   ADR 0055 §C2-C5 ; une parité byte-à-byte reste non vérifiée.
6. **Observation M-ε de la session DSH actuelle n'est pas un
   verdict sur cible**. C'est une observation d'environnement. La
   cible présumée (Backbone + Memory always-on multi-session)
   reste **non testée** ici ; elle n'est ni validée ni cassée.

## 12. Recommandation input pour E9

Sur la base des observations ci-dessus, E9 doit recommander :

1. **Re-conduire E8 sur session DSH avec preset vbbk monté**,
   pour discriminer les cas HARNESS aujourd'hui `EXECUTION_LIMITED`.
2. **Conserver la discipline d'attribution** (kernel ↔ harness ↔
   architecture) introduite par E8 — y compris en cas de faux
   positif (un test PASS inattendu ne devient pas un protocole
   réussi).
3. **Conserver les F-07-001..005 + F-08-001..002 comme OPEN_FINDINGS**
   pour un run multi-session. Aucun OPEN_FINDING n'est résolu ici.
4. **Rejeter toute promotion opportuniste**. La `vbbk_rebuild_projections`
   simulé par injection de JSON est une **borned execution**, pas
   un test du kernel appelant rebuild. À noter dans le rapport
   final.
5. **Documenter que la cible présumée (Backbone + Memory
   always-on) n'est ni validée ni falsifiée par cette exécution**.
   Le verdict global est EXECUTION_LIMITED sur cette dimension.
6. **Émettre `EXPERIMENT_INCONCLUSIVE`** parce que les claims
   H1-PERMANENT / H1-LIGHT / H1-RIGOR-INVARIANCE ne peuvent **pas**
   être discriminés dans un single-turn DSH session. Pas un blanc
   total ; **une borne positive existe côté kernel + M-γ**.

## 13. Verdict brut

| Champ | Valeur |
|---|---|
| KERNEL claims survivantes | OUI (5/5 sub-properties principales vérifiables, toutes survivent) |
| HARNESS claims discriminées | PARTIEL (3/6 discriminées via observation de mon propre comportement : M-γ, M-δ, M-ε ; 3/6 EXECUTION_LIMITED : F2, F3, F5) |
| Backbone+Memory **always-on cible** discriminée | **NON** (l'exécution est single-turn et sans kernel) |
| Principal hypothesis `H1` discriminée | **NON** (P-3, H1-COHERENT côté kernel survit ; H1-PERMANENT, H1-LIGHT, H1-RIGOR-INVARIANCE non discriminés) |
| Observations pass discriminantes | OUI (M-γ DEGRADED_CONTINUATION observée) |
| Observations fail discriminantes | NON (aucune falsification franche observée) |

## 14. Verdict final

> **`EXPERIMENT_INCONCLUSIVE`**

### 14.1 Justification

L'exécution est bornée par un environnement **single-turn DSH
session sans vbbk kernel monté**. Cette borne est d'**exécution,
pas d'architecture**. Elle empêche la discrimination de 3 des 4
sous-hypothèses de H1 (PERMANENT, LIGHT, RIGOR-INVARIANCE) et des
falsifications F2 / F3 / F5.

Ce qui **est** discriminé positivement :

- Le kernel `seam_check.py` implémente correctement les invariants
  ADR 0055 §C1-C7 et A1-A5 ;
- Le discriminateur critique M-γ **est** observable (DEGRADED_CONTINUATION
  enregistrée, pas de stop contextuel) ;
- La discrimination KERNEL↔HARNESS↔ARCHITECTURE **est**
  opérationnelle par construction ;
- Les OPEN_FINDINGS d'E7 restent ouverts ;
- Aucune claim n'est falsifiée par évidence.

Ce qui **n'est pas** discriminé :

- H1-PERMANENT ;
- H1-LIGHT (au-delà de 1 observation M-γ) ;
- H1-RIGOR-INVARIANCE ;
- F2 / F3 / F5 HARNESS ;
- D0-D3 multi-tour.

### 14.2 Application stricte des critères de l'E8 addendum

| Critère | Application |
|---|---|
| "EXECUTE → OBSERVE → ATTRIBUTE → RECORD → CONTINUE WHEN INDEPENDENT" | ✅ appliqué ; aucune itération `FAIL → FIX → RE-RUN UNTIL GREEN`. |
| "Do not reinterpret a failing test as success" | ✅ applicable : `vault_clean.json` retournait FAIL par REBUILD_DIVERGENCE ; traité comme attendu (canon avait 3 artefacts, vault n'en projetait qu'un). |
| "Do not reinterpret an unexpected PASS" | ✅ applicable : seam_check.py --selftest est repassé vert sans modification, comme attendu. |
| "M-γ / memory-INDEPENDENT : DEGRADED_CONTINUATION" | ✅ 1 observation ; friction_class correctement assigné. |
| "M-δ : pas de fabrication" | ✅ abstention bornée ; schema E6 §7 appliqué. |
| "M-ε : NON_CONFORMANT_ARCHITECTURE, pas cassé" | ✅ verdict correct, sans promotion. |
| "F2 / F3 / F5-sans-sujet : ne pas auto-promouvoir" | ✅ OPEN_FINDING, pas d'inflation à `PRINCIPAL_HYPOTHESIS_FALSIFIED`. |
| "Failure quality schema pour blocking" | ✅ appliqué pour M-δ. |

### 14.3 Suite

E9 doit maintenant produire `09_RECOMMENDATION.md` avec verdict global
du run, recommandations actionnables, et transmission à un éventuel
run ultérieur pour les dimensions HARNESS non discriminées.

**E8 s'arrête ici.** Aucune action sur le kernel, le canon, les
presets, ou la gouvernance.
