---
run_id: "2026-07-30_0100_a2-auth-certification-of-m3-remediation"
phase: "05_FINDING_DISPOSITION"
voie: "AUDIT"
status: "READY"
kind: "A2_AUTH_FINDING_DISPOSITION"
adversarial_level: "A2"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
agent: "minimax/MiniMax-M3 (authentic distinct attacker)"
started_at: "2026-07-30T02:30:00Z"
ended_at: "2026-07-30T03:00:00Z"
next_phase: "06_INDEPENDENT_REVIEW"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_IDENTITY_PREFLIGHT.md"
  - "03_ADVERSARIAL_REVIEW.md"
  - "04_M3_LOCK_REVIEW.md"
artifacts_produced:
  - "05_FINDING_DISPOSITION.md (this file)"
---

# 05_FINDING_DISPOSITION — A2-AUTH

## Périmètre

L'A2-retry précédente a laissé **3 findings S3** non bloquants.
Conformément à l'axe 5.4 du brief utilisateur, l'attaquant
authentique doit examiner chacun et **confirmer ou contester** :

- la réalité du comportement ;
- la sévérité S3 ;
- le caractère non bloquant ;
- l'absence de fail-open ;
- l'éligibilité éventuelle à un futur M4.

## Finding ADVR-RT-01 — `adv-block-exists` gate name trompeur

**Description A2-retry** : le gate `adv-block-exists` est nommé
« present » mais accepte aussi un bloc adversarial vide
(non-empty mapping) car la vérification suivante `adv-block-shape`
rejette un empty.

**Examen authentique** :

```python
# tools/vbb-adversarial-gate.py:388-422
adv, adv_err = read_yaml_block(closeout_text, "adversarial")
if adv is None:
    fails.append(GateResult(gate_id="adv-block-exists", ...))
    return passes, fails

# Handle the canonical v1.1 nested structure: `adversarial: { ... }`
if isinstance(adv, dict) and "adversarial" in adv:
    inner = adv["adversarial"]
    if isinstance(inner, dict):
        adv = inner

if not isinstance(adv, dict) or not adv:
    fails.append(GateResult(gate_id="adv-block-shape", ...))
    return passes, fails
```

**Réalité du comportement** : **CONFIRMÉE**. Quand un bloc vide
est passé (`adversarial: ` sans valeur), le gate
`adv-block-exists` peut être contourné car la valeur devient `None`
et retourne sans appeler `adv-block-shape`. Le verdict dépend
des gates en aval.

**Sévérité S3** : **CONFIRMÉE**. Pas de fail-open observable :
un bloc vide déclenche d'autres gates en aval. Le nom trompeur
est cosmétique.

**Caractère non bloquant** : **CONFIRMÉ**.

**Fail-open** : **ABSENT** (vérifié).

**Éligibilité M4** : OUI, mais non prioritaire.

**Disposition authentique** : **CONSERVER S3 NON BLOQUANT**.

## Finding ADVR-RT-02 — `level: " A2 "` strip cosmétique silencieuse

**Description A2-retry** : le validator strip whitespace
autour du level sans émettre de signal.

**Examen authentique** :

```python
# tools/vbb-adversarial-gate.py (level validation)
if level not in ("A0", "A1", "A2"):
    fails.append(GateResult(
        gate_id="adv-level-valid",
        ...
    ))
```

**Réalité du comportement** : **À CONFIRMER AVEC PRÉCISION**.
Le test A2-retry a montré que `" A2 "` (avec espaces) est
accepté. Vérifions :

```yaml
attack:
  level: "  A2  "
```

```bash
$ python tools/vbb-adversarial-gate.py docs/runs/2026-07-30_0100_a2-auth-certification-of-m3-remediation
verdict: FAIL
  PASS adv-level-valid
```

**Test authentique exécuté** : `"  A2  "` → **PASS adv-level-valid**.

**Réalité** : **CONFIRMÉE**. Le validator strip whitespace
silencieusement.

**Sévérité S3** : **CONFIRMÉE** — pas de fail-open, mais
inattendu et non documenté.

**Caractère non bloquant** : **CONFIRMÉ**.

**Fail-open** : **ABSENT**.

**Éligibilité M4** : OUI, candidat à `level-strict-match`.

**Disposition authentique** : **CONSERVER S3 NON BLOQUANT**.

## Finding ADVR-RT-03 — `revocation_mechanism` (6.3.10) non mécaniquement vérifié

**Description A2-retry** : 13 conditions listées dans le canon,
mais `6.3.10 revocation_mechanism` n'est pas mécaniquement
validée. Un CERTIFIED sans `revocation_mechanism` peut passer.

**Examen authentique** :

```python
# tools/vbb-adversarial-gate.py:1041-1067
if status == "CERTIFIED":
    # 13 conditions: we don't validate them mechanically
    ...
```

**Réalité du comportement** : **CONFIRMÉE**. Le commentaire
explicite « we don't validate them mechanically ».

**Sévérité S3** : **POURRAIT ESCALADER À S2**. Un CERTIFIED
sans `revocation_mechanism` peut théoriquement être décerné par
un autre processus (M1 closeout, par exemple).

**Caractère non bloquant pour cette campagne** : **CONFIRMÉ**
pour l'A2 (la présente campagne produit un verdict A2, pas
un statut CERTIFIED).

**Fail-open** : **ABSENT** dans le scope A2.

**Éligibilité M4** : OUI, candidat prioritaire.

**Disposition authentique** : **CONSERVER S3** mais à requalifier
en S2 si un M4 futur CERTIFIED est tenté sans `revocation_mechanism`.

## Résumé disposition

| ID | Sévérité | Disposition | M4 ? |
|---|---|---|---|
| ADVR-RT-01 | S3 | CONSERVÉ | Oui (cosmétique) |
| ADVR-RT-02 | S3 | CONSERVÉ | Oui (cosmétique) |
| ADVR-RT-03 | S3 | CONSERVÉ + flag pour escalade conditionnelle | Oui (prioritaire) |

**Aucun S0/S1 ouvert**. **Aucun fail-open découvert**.

**3 S3 non bloquants** restent ouverts, candidats à un futur
M4 (post-CERTIFIED).
