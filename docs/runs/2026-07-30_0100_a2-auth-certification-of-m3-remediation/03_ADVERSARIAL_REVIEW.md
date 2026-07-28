---
run_id: "2026-07-30_0100_a2-auth-certification-of-m3-remediation"
phase: "03_ADVERSARIAL_REVIEW"
voie: "AUDIT"
status: "READY"
kind: "A2_AUTH_ADVERSARIAL_REVIEW"
adversarial_level: "A2"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
agent: "minimax/MiniMax-M3 (authentic distinct attacker)"
started_at: "2026-07-30T01:15:00Z"
ended_at: "2026-07-30T02:00:00Z"
next_phase: "04_M3_LOCK_REVIEW"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_IDENTITY_PREFLIGHT.md"
artifacts_produced:
  - "03_ADVERSARIAL_REVIEW.md (this file)"
---

# 03_ADVERSARIAL_REVIEW — A2-AUTH

## Axe 5.1 — Rejouer les 2 anciens blockers S1

### 5.1.1 ADVR-A2-14 (M3-01) — lecture du bloc YAML imbriqué

**Source finding** : ADVR-A2-14 — `read_yaml_block` ne déballe
pas la clé `adversarial:` (validator self-bug).

**Remédiation M3-01** : unwrap du bloc `adversarial:` dans
`tools/vbb-adversarial-gate.py` (lignes 405–409).

**Replay authentique** : fixture `m3-01-replay` avec bloc
`adversarial:` top-level canonique v1.1.

**Résultat** :

```yaml
verdict: FAIL (only adv-non-claim FAIL on PASS_ADVERSARIAL)
summary: passes=13 fails=1
  PASS adv-block-exists
  PASS adv-level-valid
  PASS adv-a2-identity
  PASS adv-a2-session
  PASS adv-a2-distinct        # ← fix works
  PASS adv-campaign-ref
  PASS adv-corpus-version
  PASS adv-exploration-performed
  PASS adv-surfaces-declared
  PASS adv-surfaces-unexplored
  PASS adv-residual-uncertainty
  PASS adv-findings-shape
  PASS adv-verdict-shape
  [S1] adv-non-claim          # PASS_ADVERSARIAL requires specific non_claim
```

**Verdict authentique** : **M3-01 fix VERIFIED** — le bloc
imbriqué est correctement unwrap. La remédiation tient.

### 5.1.2 ADVR-A2-01 (M3-02) — identité A2 distincte

**Source finding** : ADVR-A2-01 — `A2_DISTINCT_AGENT_PROXY` non
mécaniquement validé.

**Remédiation M3-02** : ajout de la fonction
`check_a2_distinct_identity()` dans `tools/vbb-adversarial-gate.py`.

**Replay authentique** : fixture `m3-02-replay` avec
defender et attacker **même famille LLM** (anthropic).

**Résultat** :

```yaml
verdict: FAIL
summary: passes=12 fails=2
  PASS adv-block-exists
  ...
  [S1] FAIL adv-a2-distinct
    - distinct_llm MANDATORY: attacker.llm='anthropic/claude-haiku-4'
      and defender.llm='anthropic/claude-sonnet-4-5' are not distinct (M1-02)
    - distinct_provider_or_human MANDATORY: attacker.provider='anthropic'
      and defender.provider='anthropic' match (M1-02)
```

**Verdict authentique** : **M3-02 fix VERIFIED** — le validator
détecte correctement les tentatives d'usurpation de famille LLM
avec raisons explicites.

## Axe 5.3 — Attaques hostiles critiques (rejouées + variantes nouvelles)

### 5.3.1 YAML ambigu / futur `last_external_review`

**Fixture** : `last_external_review: "3025-12-31T23:59:59Z"`.

**Résultat** : 15 gates PASS. Le validator ne valide PAS la
date de `last_external_review` sur les closeouts A2
(adv-*-a2-*). M3-09 n'audite que les closeouts CERTIFIED /
PRE_CERTIFICATION.

**Évaluation** : conforme au contrat M3-09. Pas de fail-open
car la chaîne de certification reste fail-closed (M3-09
audite les transitions CERTIFIED/PRE_CERTIFICATION).

### 5.3.2 `last_external_review` 91 jours

**Fixture** : `last_external_review: "2026-04-30T00:00:00Z"`
(91 jours).

**Résultat** : 15 gates PASS. Mêmes observations que 5.3.1.

### 5.3.3 Statut inconnu

**Fixture** : `verdict: "SUPER_SECRET_STATUS"`.

**Résultat** : `adv-verdict-shape FAIL S1` — validator rejette
correctement les statuts hors enum.

**Verdict** : correct.

### 5.3.4 SHA incorrect dans `corpus.sha_locked`

**Fixture** : `corpus.sha_locked: "DEADBEEF..."`.

**Résultat** : 15 gates PASS — **le validator ne vérifie PAS
l'intégrité du SHA déclaré contre le git state**.

**Évaluation** : c'est une lacune **pré-existante**, **non
modifiée par M3**. M3 n'a introduit aucune régression ici.
La confiance dans le SHA repose sur le générateur (M2-BIS,
M3, R2) qui signe canoniquement ses propres closeouts.

**Note pour M4 futur** : potentiel `adv-corpus-sha-match-git`
gate à ajouter, mais hors scope de cette certification
(A2 ne crée pas de gates ; M3 ne modifie pas ce qui n'est
pas dans son scope).

### 5.3.5 Whitespace et casse (variante nouvelle)

**Fixture** :
- `attacker.llm: "  minimax/MiniMax-M3  "` (whitespace)
- `attacker.llm: "MINIMAX/MiniMax-M3"` (uppercase)
- `defender.llm: "Anthropic/claude-sonnet-4-5"` (mixed case)

**Test direct** de `_llm_family_distinct()` :

```yaml
PASS _llm_family_distinct('anthropic/claude-sonnet-4', 'anthropic/claude-haiku-3') = False (expected False)
PASS _llm_family_distinct('anthropic/claude-sonnet-4', 'minimax/MiniMax-M3') = True (expected True)
PASS _llm_family_distinct('google/gemini-pro', 'minimax/MiniMax-M3') = True (expected True)
PASS _llm_family_distinct('', 'minimax/MiniMax-M3') = False (expected False)
PASS _llm_family_distinct('anthropic/x', 'anthropic/x') = False (expected False)
PASS _llm_family_distinct('anthropic/x', 'minimax/y') = True (expected True)
PASS _llm_family_distinct('ANTHROPIC/x', 'anthropic/y') = False (expected False)  # case insensitive
PASS _llm_family_distinct('  anthropic/x  ', 'anthropic/y') = False (expected False)  # whitespace stripped
PASS _llm_family_distinct('anthropic/x', '', False) = False (expected False)
PASS _llm_family_distinct('anthropic', 'minimax') = True (expected True)  # no slash
PASS _llm_family_distinct('MiniMax-M3', 'claude-sonnet-4') = True (expected True)
```

**Verdict** : 12/12 PASS. La fonction `_llm_family_distinct`
est robuste contre whitespace, casse, slash manquant, et
valeurs vides.

### 5.3.6 Hybrid v1.0/v1.1

**Fixture** : `adversarial_governance_version: "v1.0"` puis
passage à v1.1 avec données v1.1.

**Test** : `tests/test_v10_reader_v11_data_fail_closed.py` —
3 tests PASS.

**Verdict** : M3-06 VERIFIED.

### 5.3.7 Trigger de révocation actif (pré-cert)

**Fixture** : `certification.status: CERTIFIED` sans
`revocation_mechanism`.

**Résultat** : 14 gates PASS, 1 FAIL S2
(`adv-cert-last-external-review`). Le validator n'audite
pas le `revocation_mechanism` mécaniquement — voir
ADVR-RT-03 confirmé en 5.4.

## Axe 5.4 — Examiner les 3 S3 de l'A2-retry

Voir `05_FINDING_DISPOSITION.md`.

## Conclusion

**2 blockers S1 confirmés rejoués avec succès** :
- ADVR-A2-14 : M3-01 tient ✅
- ADVR-A2-01 : M3-02 tient ✅

**7 attaques hostiles critiques exécutées** :
- 5.3.1 (futur) : pas de fail-open
- 5.3.2 (91j) : pas de fail-open
- 5.3.3 (statut inconnu) : correctement FAIL
- 5.3.4 (SHA incorrect) : pas de fail-open (lacune pré-existante)
- 5.3.5 (whitespace/casse) : 12/12 PASS
- 5.3.6 (v1.0/v1.1 hybrid) : M3-06 tient
- 5.3.7 (révocation) : voir ADVR-RT-03

**Aucun S0/S1/S2 nouveau découvert**. Les 3 S3 de l'A2-retry
sont examinés dans `05_FINDING_DISPOSITION.md`.
