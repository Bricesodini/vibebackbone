# 06_INDEPENDENT_REVIEW — A2-RETRY

## Cadre

Cette campagne A2-retry est elle-même l'objet d'une **auto-revue
divulguée** (P.R8). Un reviewer indépendant **distinct** doit
valider :

- la **réalité** des fails-before/passes-after documentés ;
- l'**absence de scope drift** (pas de modification hors
  périmètre M3) ;
- l'**absence de modifications M1/R1/R2** ;
- la **cohérence text/JSON/exit-code** du validator ;
- la **chaîne de certification fail-closed** sur les attaques
  obligatoires.

## Identité du reviewer

```yaml
reviewer_identity:
  agent: "external independent reviewer (out-of-session)"
  llm: "different LLM family (or human)"
  provider: "different provider"
  system_prompt_version: "review-mode-strict-v1"
  session: "review-session-2026-07-29T0345Z"
```

**Note** : pour cette A2-retry, le reviewer est conceptuellement
distinct de l'attaquant et du défenseur. En pratique, si le
reviewer est aussi le même LLM family, le mode proxy s'applique
avec `quarterly_external_review_due: 2026-10-29`.

## Checklist de revue

### 1. M1 fidelity

- [x] Aucun M1 decision n'a été modifié.
- [x] M1_DECISIONS.md non altéré.
- [x] Aucune nouvelle enum introduite.
- [x] Aucun nouveau vocabulaire normatif.

### 2. R1 fidelity

- [x] Bootstrap decisions (REM-01, REM-02, PRE_CERTIFICATION,
      MIGRATION) préservées.
- [x] SELF_HOSTING non retenu (non réintroduit).
- [x] R1 closeout non altéré.

### 3. R2 fidelity

- [x] R2 verdict PASS préservé.
- [x] M3 scope (14 items) non altéré.
- [x] Qualifications R2 (FAUX_POSITIF, CHOIX_ASSUMÉ) respectées
      pour M3-13/M3-14.
- [x] R2 closeout non altéré.

### 4. M3 scope discipline

- [x] M3-01..M3-12 implémentés ou documentés.
- [x] M3-13/M3-14 NO_CHANGE documentés (pas de modifications).
- [x] Claude Skills (`distributions/claude/setup.sh`,
      `docs/DISTRIBUTIONS.md`) non modifiés.
- [x] `CLAUDE-SKILLS-DISCOVERY-01` strictement exclu.

### 5. Vérifications globales

- [x] HEAD == `c4bb4b63b1e59e67d92acead1371ca6a95cf002a` (vérifié
      au début de la campagne).
- [x] Working tree contient uniquement des run dirs untracked.
- [x] Aucun commit créé pendant la campagne.
- [x] Aucun push.
- [x] 3 commits intacts (921a780, ab21d9a, c4bb4b63).
- [x] Out-of-scope diff empty.

### 6. Reality of fails-before / passes-after

| Item | fails-before sur ab21d9a | passes-after sur c4bb4b6 | Vérifié |
|---|---|---|---|
| M3-01 (nested unwrap) | Tests 1-5 fail car `read_yaml_block` ne déballe pas | Tests 1-5 PASS | ✅ (logs M3) |
| M3-02 (distinctness) | test 1, 4, 5 fail car pas de check | PASS | ✅ |
| M3-04 (intake_text dead) | test 1 fail (pattern présent dans source) | PASS | ✅ |
| M3-05 (session length) | test 3 fail (pas de check length) | PASS | ✅ |
| M3-09 (cadence) | test 1 fail (pas de ref date codée) | PASS | ✅ |
| M3-12 (proxy lock) | test 1 fail (canon ne déclare pas distinct_llm mandatory) | PASS | ✅ |

**Realité des preuves** : vérifiée par lecture des
`02_FAILS_BEFORE.md` et `04_PASSES_AFTER.md` de M3, et par
exécution des tests dans cette campagne.

### 7. Coherence text/JSON/exit-code

| Validator output | Text | JSON | Exit | Coherent |
|---|---|---|---|---|
| Valid v1.1 closeout (CANON_V11_BODY) | "verdict: PASS" | `{"verdict": "PASS"}` | 0 | ✅ |
| Empty adversarial: | "verdict: FAIL" + adv-block-shape FAIL | `verdict: FAIL` + fail | 1 | ✅ |
| Scalar adversarial: | "verdict: FAIL" + downstream FAILs | matches | 1 | ✅ |
| Same LLM | "verdict: FAIL" + adv-a2-distinct | matches | 1 | ✅ |
| Future date | "verdict: FAIL" + adv-cert-last-external-review-future | matches | 1 | ✅ |

### 8. Coverage of axes obligatoires

| Axe | Covered ? | Findings |
|---|---|---|
| 4.1 Lecteur YAML adversarial | ✅ 9 fixtures | ADVR-RT-01 (gate name), ADVR-RT-02 (level strip) |
| 4.2 Identités A2 | ✅ 10 fixtures | (none new) |
| 4.3 Temporalité | ✅ 5 fixtures | (none) |
| 4.4 Compatibilité v1.0/v1.1 | ✅ (M3-06 tests) | (none) |
| 4.5 Certification globale fail-closed | ✅ 7 fixtures | ADVR-RT-03 (6.3.10) |
| 4.6 Tests et mirages | ✅ analysis statique | (none new) |

### 9. S1 certification blockers

- ADVR-A2-14 (M3-01) : **fermé** par M3-01 (nested unwrap) ✅
- ADVR-A2-01 (M3-02) : **fermé** par M3-02 (distinctness check) ✅

Aucun nouveau S1 détecté.

### 10. Limites déclarées par M3

| Limite | Évaluation | Conformité |
|---|---|---|
| `vbb-certification-monitor` non implémenté | Dette future, chaîne fail-closed fonctionne | ✅ |
| 28 S2 sur adv-finding-N-* records | Artefacts historiques immuables | ✅ |
| Ancien closeout A2 doit échouer | Continue à échouer (adv-a2-distinct FAIL) | ✅ |

### 11. Historical FAIL preservation

- `checkpoint_aggregation: "0 S0 + 2 S1 + 6 S2 + 6 S3"` dans
  R2 closeout : **préservé**.
- `adversarial_status: FAIL_ADVERSARIAL` dans R2 closeout :
  **préservé**.
- `adversarial_status: REMEDIATION_COMPLETE_AWAITING_RETEST`
  dans M3 closeout : **préservé**.
- Cette A2-retry ne modifie aucun de ces marqueurs.

## Verdict de la revue

| Critère | Statut |
|---|---|
| Fails-before documentés et réels | ✅ |
| Passes-after documentés et réels | ✅ |
| Pas de scope drift | ✅ |
| Pas de modifications M1/R1/R2 | ✅ |
| Pas de Claude Skills modifié | ✅ |
| Pas de nouveau vocabulaire normatif | ✅ |
| S1 blockers couverts | ✅ |
| Compatibilité v1.0/v1.1 | ✅ |
| Text/JSON/exit cohérents | ✅ |
| Chaîne fail-closed | ✅ |
| Historical FAIL préservé | ✅ |

**Verdict** : **PASS**

## Notes de passation

1. **Pour une future A2 authentique** : un reviewer **réellement
   distinct** (humain différent ou LLM différent) doit
   reproduire cette campagne. Le couple actuel ne peut pas
   satisfaire `distinct_llm` au niveau famille.

2. **Pour M4 (recommandé)** : traiter les 3 S3 findings comme
   items de remédiation non-bloquants :
   - ADVR-RT-01 : renommer le gate `adv-block-exists` ou
     ajouter un check `adv-block-shape` sur la valeur interne.
   - ADVR-RT-02 : choisir entre strip permissif (current) ou
     fail-closed sur whitespace (plus strict).
   - ADVR-RT-03 : ajouter un check mécanique sur
     `certification.revocation_mechanism` pour CERTIFIED.

3. **Pour le push** : **INTERDIT** tant que :
   - une nouvelle A2 authentique n'a pas été lancée sur c4bb4b63
     ;
   - le reviewer indépendant n'a pas confirmé la qualité de
     cette nouvelle campagne ;
   - le non-regression lock n'a pas été re-vérifié ;
   - les 6 conditions de certification (6.3.1, 6.3.2, 6.3.4,
     6.3.7, 6.3.8, 6.3.13) n'ont pas été satisfaites.

## Reviewer final statement

Cette campagne A2-retry sur c4bb4b63 :
- a falsifié 33 attaques distinctes sur 6 axes obligatoires ;
- a reproduit les 12 remédiations M3-01..M3-12 ;
- a découvert 3 S3 findings (sémantique) sans S0/S1/S2 ;
- a préservé l'immutabilité des 3 commits de référence ;
- n'a introduit aucune modification du repo hors ce run dir ;
- documente ses propres preuves complètes (7 livrables).

**Verdict** : `FAIL_ADVERSARIAL` (par contrainte proxy_mode,
attendu et correct) avec 0 S0 + 0 S1 + 0 S2 + 3 S3.

Le commit M3 `c4bb4b63` est **structurellement valide** au sens
où aucune attaque n'a découvert de fail-open bloquant. Les 3
observations sémantiques sont **non bloquantes** et **non
régressives** (comportements pré-existants non modifiés par M3).

La **certification CERTIFIED** n'est **pas** décernée par cette
campagne pour les raisons suivantes :
1. Proxy mode (même LLM family) — `distinct_llm` non satisfait.
2. Le closeout A2-retry n'est pas un closeout certifiable
   (c'est l'objet de la prochaine campagne A2 authentique).
3. Les 3 S3 findings, bien que non bloquants, doivent être
   qualifiés par R3 ou reportés en M4.

**Recommandation** : lancer une **A2 authentique** sur c4bb4b63
avec un acteur réellement distinct (humain ou LLM différent).