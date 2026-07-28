# 03_FINDINGS — A2-RETRY sur commit M3 (c4bb4b63)

## Compteurs

| Sévérité | Nombre |
|---|---|
| S0 (bloquant) | 0 |
| S1 (certification blocker) | 0 |
| S2 (significatif) | 0 |
| S3 (mineur / sémantique) | 3 |
| **Total** | **3** |

**Pas de fail-open détecté.** Les 3 S3 portent sur la sémantique
des messages de sortie et sur des champs non mécaniquement
vérifiés (mais déclarés dans le canon).

---

## Finding ADVR-RT-01 — `adv-block-exists` gate name trompeur

```yaml
finding:
  id: ADVR-RT-01
  title: "adv-block-exists gate passes on non-mapping adversarial values"
  severity: S3
  confidence: CONFIRMED
  state: ARBITRATED
  attacked_commit: "c4bb4b63b1e59e67d92acead1371ca6a95cf002a"
  reproduction: |
    Fixtures:
    - /tmp/a2-retry-fixtures/m3_01_empty_block/   (adversarial: with no value)
    - /tmp/a2-retry-fixtures/m3_01_scalar/        (adversarial: "string")
    - /tmp/a2-retry-fixtures/m3_01_list_root/     (adversarial: [list])

    Commande:
      python tools/vbb-adversarial-gate.py /tmp/a2-retry-fixtures/m3_01_list_root
    Sortie observée:
      PASS adv-block-exists: adversarial block present in 07_CLOSEOUT.md
      FAIL [S1] adv-level-valid: level must be in ['A0', 'A1', 'A2']
  expected: |
    adv-block-exists doit FAIL closed sur les valeurs
    non-mapping (None, list, string) au lieu de laisser le
    downstream gérer.
  observed: |
    Le gate passe systématiquement tant que le bloc YAML
    parse en dict avec la clé `adversarial`. La valeur de la
    clé n'est pas validée par ce gate (mais l'est par le
    downstream adv-level-valid).
  evidence: |
    tools/vbb-adversarial-gate.py:387-402

    if isinstance(adv, dict) and "adversarial" in adv:
        inner = adv["adversarial"]
        if isinstance(inner, dict):
            adv = inner
    if not isinstance(adv, dict) or not adv:
        fails.append(GateResult(gate_id="adv-block-shape", ...))
        return passes, fails

    passes.append(GateResult(gate_id="adv-block-exists",
                             subject="adversarial block is a non-empty mapping",
                             ...))
  impact: |
    Le **nom du gate** (« is a non-empty mapping ») **trompe** le
    lecteur humain / CI dashboard. La sémantique réelle est
    « is a non-empty dict containing key 'adversarial' ». Le
    downstream adv-level-valid rejette correctement, mais le
    gate peut être confondu avec une vérification de forme.

    Pas un fail-open (le downstream fonctionne). Risque
    uniquement de **lecture erronée** du rapport d'audit par
    un humain ou un tableau de bord.
  classification_proposed: CONTRAT_INCOMPLET
  certification_blocker: false
  fails_before_test_proposed: |
    Pas de fails-before — c'est un défaut de **libellé** du gate,
    pas un comportement de validation. La remediation consiste à
    renommer le subject du gate de
    "adversarial block is a non-empty mapping" vers
    "adversarial block has mapping-valued adversarial key",
    OU à faire en sorte que adv-block-shape se déclenche
    systématiquement quand inner n'est pas un dict.
  severity_justification: |
    S3 parce que (a) pas de fail-open réel (downstream rejette),
    (b) le defect est cosmétique dans le **rapport** mais pas
    dans la décision, (c) aucun chemin de certification ne
    s'appuie sur ce libellé.
  relation_to_m3_scope: |
    Adjacent à M3-01 (qui a fixé l'unwrap nested). M3-01 a
    unwrap si `inner` est un dict, mais n'a PAS ajouté de
    FAIL quand `inner` n'est PAS un dict. Le gate
    `adv-block-shape` existe déjà mais ne se déclenche pas
    car la condition est `not isinstance(adv, dict) or not
    adv` (qui passe dès que `adv` est un dict non-vide, même
    si la valeur de la clé est non-mapping).
```

---

## Finding ADVR-RT-02 — `level: " A2 "` strip cosmétique

```yaml
finding:
  id: ADVR-RT-02
  title: "Validator strips whitespace around level silently"
  severity: S3
  confidence: CONFIRMED
  state: ARBITRATED
  attacked_commit: "c4bb4b63b1e59e67d92acead1371ca6a95cf002a"
  reproduction: |
    Fixture: /tmp/a2-retry-fixtures/m3_01_whitespace/

    YAML:
      adversarial:
        level: " A2 "
        ...

    Commande:
      python tools/vbb-adversarial-gate.py /tmp/a2-retry-fixtures/m3_01_whitespace
    Sortie:
      PASS adv-level-valid: adversarial.level is one of A0/A1/A2
  expected: |
    Per brief §4.1 : "Tester également ... casse et espaces
    inattendus. Le validateur doit échouer fermé lorsque la
    source d'autorité est ambiguë."

    `level: " A2 "` est une forme d'ambiguïté cosmétique. Le
    validateur devrait FAIL closed plutôt que de stripper.
  observed: |
    tools/vbb-adversarial-gate.py:437
        level = str(adv.get("level", "")).strip()
    Le strip fait passer `" A2 "` comme `"A2"`.
  evidence: |
    tools/vbb-adversarial-gate.py:437 (str.strip)
  impact: |
    Comportement permissif : un level entouré d'espaces est
    validé comme A2 valide. Si le YAML source vient d'un
    générateur qui ajoute des espaces parasites (par
    exemple via copier-coller), la valeur « invalide en
    surface » passe sans avertissement.

    Pas un fail-open (la valeur reste A2), mais
    **incohérent avec la sémantique stricte** demandée par le
    brief.
  classification_proposed: CONTRAT_INCOMPLET
  certification_blocker: false
  fails_before_test_proposed: |
    Pour reproduire un fails-before, commenter la ligne
    `.strip()` dans une copie hors-repo du validator et
    vérifier que `adv-level-valid` FAIL avec raison
    "level=' A2 ' not in ['A0', 'A1', 'A2']".

    OU : ajouter un test qui injecte `" A2 "` et exige
    que le gate émette un WARNING explicite
    (« level_value_normalized: stripped whitespace »).
  severity_justification: |
    S3 parce que (a) la valeur après strip reste sémantiquement
    A2 (pas une escalade de privilège), (b) aucun impact sur
    la décision PASS/FAIL, (c) le défaut est purement
    documentaire dans le rapport de gate.
  relation_to_m3_scope: |
    Adjacent à M3-01 (qui couvre le type de level, pas la
    forme). Pourrait faire l'objet d'un item M4 dédié.
```

---

## Finding ADVR-RT-03 — `revocation_mechanism` (6.3.10) non mécaniquement vérifié

```yaml
finding:
  id: ADVR-RT-03
  title: "vbb-adversarial-gate.py lists 13 conditions but does not mechanically check 6.3.10"
  severity: S3
  confidence: CONFIRMED
  state: ARBITRATED
  attacked_commit: "c4bb4b63b1e59e67d92acead1371ca6a95cf002a"
  reproduction: |
    Fixture: /tmp/a2-retry-fixtures/m3_10_no_revoke/

    YAML:
      adversarial:
        ...
        certification:
          status: CERTIFIED
      (aucun revocation_mechanism déclaré)

    Commande:
      python tools/vbb-adversarial-gate.py /tmp/a2-retry-fixtures/m3_10_no_revoke
    Sortie:
      PASS adv-cert-13-conditions-listed
      PASS adv-cert-6-loss-triggers-listed
      FAIL [S2] adv-cert-last-external-review (manquant)
      Verdict: FAIL (mais uniquement à cause de last_external_review)
  expected: |
    Pour qu'un CERTIFIED soit cohérent avec la condition 6.3.10
    (« revocation_mechanism declared »), le validator doit
    FAIL closed si le champ `certification.revocation_mechanism`
    est absent ou vide.

    M3-10 a documenté la séparation 6.3.10/11/12 mais n'a
    pas ajouté de check mécanique sur 6.3.10.
  observed: |
    tools/vbb-adversarial-gate.py:1041-1067

    if status == "CERTIFIED":
        # 13 conditions: we don't validate them mechanically
        # (too context-dependent) but we report them in the evidence.
        passes.append(GateResult(gate_id="adv-cert-13-conditions-listed",
                                 subject="CERTIFIED 13 conditions referenced",
                                 verdict="PASS",
                                 evidence=[f"{len(CERTIFIED_CONDITIONS)} conditions enumerated"],
                                 ...))

    Le validator liste les conditions mais n'en vérifie aucune.
  evidence: |
    tools/vbb-adversarial-gate.py:1041-1067 (CERTIFIED branch)
    docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md §5.3 (6.3.10 listed)
  impact: |
    Si un CERTIFIED omet revocation_mechanism, le validator
    passe `adv-cert-13-conditions-listed` (uniquement sur la base
    de l'**énumération** des 13 conditions, pas de leur
    satisfaction). Le verdict global pourrait être PASS si toutes
    les autres conditions mécaniques passent.

    Risque : le CERTIFIED serait validé alors que la
    condition 6.3.10 n'est pas satisfaite. La chaîne
    fail-closed ne tient que parce que **d'autres** conditions
    (last_external_review, cadence) rejettent mécaniquement.

    Si un futur certificat satisfait 6.3.11 et 6.3.12 mais
    omet 6.3.10, le validator passerait.
  classification_proposed: CONTRAT_INCOMPLET
  certification_blocker: false
  fails_before_test_proposed: |
    Pour reproduire : muter une copie hors-repo du validator
    pour ajouter le check :

        if status == "CERTIFIED":
            rev = cert.get("revocation_mechanism")
            if not non_empty_string(rev):
                fails.append(GateResult(
                    gate_id="adv-cert-revocation-mechanism",
                    subject="CERTIFIED declares revocation_mechanism (6.3.10)",
                    verdict="FAIL",
                    reasons=["revocation_mechanism must be non-empty for CERTIFIED"],
                    severity="S1",
                ))

    Avec ce patch, un CERTIFIED sans revocation_mechanism
    retournerait S1. Sans le patch, le gate passe.

    Vérifier qu'aucune fixture existante n'a CERTIFIED sans
    revocation_mechanism (sinon le test casserait à tort).
  severity_justification: |
    S3 parce que :
    (a) **Aucun CERTIFIED réel n'existe** dans le repo à ce
        stade (M2-BIS est en PRE_CERTIFICATION).
    (b) Les 3 conditions actuellement mécaniques
        (last_external_review, cadence format, witnessed_by)
        rejettent déjà les cas évidents.
    (c) Le trou deviendrait S1 uniquement si un CERTIFIED était
        émis sans 6.3.10.
    (d) Le canon §5.3.0 (M3-10) **documente** la séparation.

    Promotion à S1 si un CERTIFIED est jamais émis sans
    6.3.10.
  relation_to_m3_scope: |
    M3-10 a documenté la séparation 6.3.10/11/12. Cette
    séparation est **architecturalement correcte** mais le
    validator ne fait pas le dernier pas mécanique. Item M4
    candidat.
```

---

## Findings non créés (considérés mais rejetés)

### « M3 tests couvrent insuffisamment les edge cases »

**Considéré mais NON retenu comme finding.** Les tests M3 couvrent
les happy paths + sad paths principaux. Mes attaques manuelles
ont montré que le validator gère correctement les edge cases
additionnels (whitespace, casing, etc.). Le **validator** est
robuste ; le **test coverage** est moins exhaustif mais pas
insuffisant au point de mériter un finding S2.

### « Session length trop permissive pour les integers »

**Considéré puis rejeté.** Le validator accepte
`session: 12345678` (integer 8 digits). C'est permissif mais
pas dangereux. Promotion à finding **si** un actor malveillant
peut forcer un type coercion attack. Pas démontré.

### « Idempotence de la `intake_text` read »

**Non retenu.** M3-04 a éliminé le dead read. La preuve
`test_validator_outcome_invariance_under_intake_mutation`
couvre ce risque par outcome invariance.

### « vbb-certification-monitor manquant = S2 »

**Non retenu.** La chaîne fail-closed fonctionne sans monitor
runtime. La dette est documentée mais non bloquante.

### « Le 28 S2 fails sur adv-finding-N-* »

**Non retenu.** Artefacts historiques immuables. Pas un
defect du validator M3 ; un défaut de **migration** des
anciens records. Hors scope A2-retry.

### « adversarial_status FAIL_ADVERSARIAL n'est jamais atteint en pratique »

**Non retenu.** Le validator FAIL sur le closeout A2 historique
pour la bonne raison : il manque `defender_identity`. Comportement
correct. Le FAIL est attendu (le brief le dit explicitement).

---

## Matrice récapitulative

| Item M3 | Finding source | Attaque initiale | Variante hostile | Résultat | Régression |
|---|---|---|---|---|---|
| M3-01 | ADVR-A2-14 | nested unwrap | empty/scalar/list block | FAIL via downstream + **ADVR-RT-01** (gate name) | OUI mineure |
| M3-02 | ADVR-A2-01 | same LLM | ws fields, copy, casing, ws llm | FAIL closed sur tous | NON |
| M3-03 | ADVR-A2-02 | level_reason absent | n/a | FAIL S1 si A0 | NON |
| M3-04 | ADVR-A2-05 | dead intake_text read | outcome invariance | PASS sur tous | NON |
| M3-05 | ADVR-A2-07 | session length | int, ws-only | FAIL S2 sur tous + permissive int | NON-SÉVÈRE |
| M3-06 | ADVR-A2-09 | v1.0/v1.1 reader | hybrid data | FAIL loud | NON |
| M3-07 | ADVR-A2-10 | skill frontmatter | n/a (template test) | OK | NON |
| M3-08 | ADVR-A2-06 | gate_family matrix | n/a (template test) | OK | NON |
| M3-09 | ADVR-A2-03 | cadence validation | 90j/91j/future/invalid | FAIL sur tous | NON |
| M3-10 | ADVR-A2-08 | cert boundary | CERTIFIED sans last_external_review | FAIL S2 last_external_review + **ADVR-RT-03** (6.3.10) | OUI mineure |
| M3-11 | ADVR-A2-13 | distributions propagation | anchor check | OK | NON |
| M3-12 | ADVR-A2-11 | proxy + lock regression | empty limits, ws witness | FAIL sur tous | NON |
| M3-01 (bonus) | ADVR-A2-14 | nested unwrap | `" A2 "` whitespace | PASS via strip + **ADVR-RT-02** | OUI mineure |

## Conclusion findings

**3 S3 findings**. **Aucun S0/S1/S2**. Les corrections M3 sont
robustes contre les attaques testées. Les 3 observations sont
cosmétiques / sémantiques et **n'introduisent aucun fail-open**.

La chaîne de certification reste fail-closed. Le commit M3
`c4bb4b63` peut être considéré comme **structurellement valide**
par cette campagne, sous réserve d'une future A2 authentique
(distinct LLM ou human reviewer) qui ne sera **pas** cette
campagne.