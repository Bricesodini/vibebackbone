---
run_id: "2026-07-29_0100_m3-remediation-of-a2-findings"
phase: "01_INTAKE"
voie: "STRUCTURED"
status: "ACTIVE"
kind: "M3_REMEDIATION"
posture: "fix in scope, evidence-bound; no M1 deviation"
adversarial_level: "A2"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
linked_subject:
  baseline_commit: "ab21d9a70f03789c623893b200024f9876b7991b"
  baseline_parent: "921a780ccf8299bc37099b377ce4e7d0d8ba2561"
  baseline_adversarial_status: "FAIL_ADVERSARIAL"
  baseline_certification_status: "NOT_CERTIFIED"
  r2_run: "docs/runs/2026-07-28_2300_r2-a2-arbitration-of-a2-findings/"
  a2_run: "docs/runs/2026-07-28_2200_a2-certification-of-m2-bis-bootstrap/"
agent: "primary implementer + delegated subagent (strict writer role)"
started_at: "2026-07-29T01:00:00Z"
ended_at: "2026-07-29T01:30:00Z"
artifacts_consumed:
  - "docs/runs/2026-07-28_2300_r2-a2-arbitration-of-a2-findings/03_M3_SCOPE.md"
  - "docs/runs/2026-07-28_2300_r2-a2-arbitration-of-a2-findings/02_FINDING_ARBITRATION.md"
  - "docs/runs/2026-07-28_2300_r2-a2-arbitration-of-a2-findings/06_INDEPENDENT_REVIEW.md"
  - "docs/runs/2026-07-28_2200_a2-certification-of-m2-bis-bootstrap/{01_INTAKE,02_AUDIT,03_DECISION,07_CLOSEOUT}.md"
  - "docs/runs/2026-07-28_1200_m1-adversarial-loop-normative-arbitration/M1_DECISIONS.md"
  - "docs/runs/2026-07-28_1800_r1-r0-findings-normative-arbitration/03_DECISION.md"
  - "docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md"
  - "docs/GATE_ASSURANCE_GOVERNANCE.md"
  - "docs/adr/0051-adversarial-assurance-dimension.md"
  - "tools/vbb-adversarial-gate.py"
  - "tools/vbb-loop-closure-check.py"
  - "docs/templates/{01_INTAKE,07_CLOSEOUT}.md.template"
  - "tests/test_a2_proxy.py, test_attacker_identity_disclosure.py, test_gate_check_level.py, test_prompt_language.py, test_backward_compat_v1_0.py, etc."
artifacts_produced:
  - "01_INTAKE.md (this file)"
  - "02_FAILS_BEFORE.md"
  - "03_REMEDIATION.md"
  - "04_PASSES_AFTER.md"
  - "05_TEST_REPORT.md"
  - "06_INDEPENDENT_REVIEW.md"
  - "07_CLOSEOUT.md"
---

# 01_INTAKE — M3 Remediation of A2 Findings

## Verdict baseline

```bash
$ git rev-parse HEAD
ab21d9a70f03789c623893b200024f9876b7991b

$ git log --oneline -3
ab21d9a feat(adversarial): deploy v1.1 operational integration
921a780 feat(adversarial): bootstrap assurance governance v1.1
75953fc docs(run): correct publication record in adversarial design closeout
```

✅ Baseline HEAD == `ab21d9a70f03789c623893b200024f9876b7991b`.
✅ Two prior commits intact: `921a780` + `ab21d9a`.
✅ Working tree contient uniquement les runs A2/R2 non trackés + ce run M3.

## Scope M3 (locked)

### Items à implémenter (12)

| ID | Finding | Sév. | Type | Dépendances |
|---|---|---|---|---|
| M3-01 | ADVR-A2-14 | S1 | M3_CODE+M3_TEST | — |
| M3-02 | ADVR-A2-01 | S1 | M3_CODE+M3_TEST+M3_TEMPLATE | M3-01 |
| M3-03 | ADVR-A2-02 | S2 | M3_DOC+M3_NORM_MIN | — |
| M3-04 | ADVR-A2-05 | S2 | M3_CODE+M3_TEST | M3-01 |
| M3-05 | ADVR-A2-07 | S2 | M3_CODE+M3_TEST | M3-01 |
| M3-06 | ADVR-A2-09 | S2 | M3_TEST+M3_DOC | — |
| M3-07 | ADVR-A2-10 | S2 | M3_TEST | — |
| M3-08 | ADVR-A2-06 | S3 | M3_TEST | — |
| M3-09 | ADVR-A2-03 | S3 | M3_CODE+M3_TEST | M3-01 |
| M3-10 | ADVR-A2-08 | S3 | M3_DOC+M3_NORM_MIN | — |
| M3-11 | ADVR-A2-13 | S3 | M3_TEST+M3_DOC | — |
| M3-12 | ADVR-A2-11 | S2 | M3_TEST | M3-02 |

### Items NO_CHANGE (2)

| ID | Finding | Sév. | Action |
|---|---|---|---|
| M3-13 | ADVR-A2-04 | S3 | FAUX_POSITIF — aucun correctif |
| M3-14 | ADVR-A2-12 | S3 | CHOIX_ASSUMÉ R1 — aucun correctif |

### Items hors scope (0)

| Type | Compte |
|---|---|
| Claude Skills discovery | DEFERRED, hors M3 |
| M1 deviations | 0 |
| M1 re-arbitration | 0 |

## Engagements

1. **Aucune modification hors scope** :
   - `distributions/claude/setup.sh` non modifié
   - `docs/DISTRIBUTIONS.md` non modifié
   - Tests de distribution non modifiés
   - Les deux commits antérieurs (`921a780`, `ab21d9a`) immuables
2. **Preuves tripartites** : chaque finding confirmé a `fails-before` reproduit, correctif minimal, `passes-after` vérifié.
3. **Un seul commit local** à la fin.
4. **Aucun push** pendant M3.
5. **Aucune déviation M1** (M1-01..M1-06 conservés tels quels).
6. **Aucun nouveau vocabulaire normatif** au-delà du canon.
7. **Cohérence** : sortie humaine / JSON / exit code identiques.
8. **Compatibilité v1.0/v1.1** : la v1.0 reader ne consomme pas silencieusement la v1.1.

## Méthodologie

```
Pour chaque item M3-NN :
1. Écrire le test fails-before (qui DOIT échouer sur la baseline).
2. Vérifier que le test échoue (capture preuve).
3. Appliquer la correction minimale.
4. Vérifier que le test passe (capture preuve).
5. Vérifier qu'aucun test connexe n'a régressé.
6. Documenter la fermeture (preuves dans 04_PASSES_AFTER).
```

### Tests fails-before obligatoires par item

Voir `02_FINDING_ARBITRATION.md` §A — chaque item a une liste
exhaustive de tests fails-before. M3 ajoute **d'abord** ces
tests, puis applique le correctif.

## Verrouillage d'ordre

L'ordre d'exécution suit strictement R2 :

```
M3-01 → M3-02 → M3-03 → M3-04 → M3-05 → M3-06 → M3-07 →
M3-08 → M3-09 → M3-10 → M3-11 → M3-12 → M3-13 (NO_CHANGE) →
M3-14 (NO_CHANGE)
```

Tout item dépendant ne peut être traité qu'après fermeture de
son ou ses dépendances. M3-01 est la **racine** du M3 (le
validateur doit pouvoir déballer le bloc `adversarial:` avant
tout check).

## Sortie

M3 ne peut pas attribuer `PASS_ADVERSARIAL` ou `CERTIFIED`.
M3 peut uniquement conclure que les remédiations sont **prêtes
à être réévaluées**. La campagne initiale reste immuable :

```
initial_campaign:
  adversarial_status: FAIL_ADVERSARIAL
  checkpoint_aggregation: "0 S0 + 2 S1 + 6 S2 + 6 S3"
  audited_commit: "ab21d9a70f03789c623893b200024f9876b7991b"
```

Le prochain sujet audité sera le **nouveau commit M3**, sur
lequel une nouvelle campagne A2 devra être lancée.

## Règle du testeur mirror

Pour éviter que les tests ne reproduisent l'implémentation :

1. **Mutations de champs** : tester avec valeurs mutées
   (espaces, chaînes vides, types incorrects).
2. **Combinaisons invalides** : tester au moins 2 combinaisons
   hostiles par finding.
3. **Données partielles** : tester chaque champ omis
   individuellement.
4. **Types incorrects** : tester `null`, listes, dicts imbriqués.
5. **Cohérence des sorties** : tester que text/JSON/exit code
   racontent la même histoire.

## Validation à l'entrée de M3

| Vérification | Résultat |
|---|---|
| HEAD == `ab21d9a70f03789c623893b200024f9876b7991b` | ✅ |
| Working tree clean (sauf runs antérieurs) | ✅ |
| Aucun commit créé par M3 | ✅ à confirmer en fin |
| Aucun push | ✅ à confirmer en fin |
| Scope Claude Skills enregistré | ✅ DEFERRED, hors scope |
| Items NO_CHANGE M3-13/M3-14 confirmés | ✅ |
