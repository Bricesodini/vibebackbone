---
run_id: "2026-05-23_1800_artifact-verify-lot-c"
phase: "07_CLOSEOUT"
voie: "RAPIDE"
status: "READY"
agent: "claude-code"
started_at: "2026-05-23T18:00:00Z"
ended_at: "2026-05-23T19:00:00Z"
next_phase: null
artifacts_consumed:
  - "docs/runs/2026-05-23_1700_contracts-artifact-schema-lot-b-d/07_CLOSEOUT.md"
  - "tools/vbb-contract-runtime.py"
  - "docs/runs/README.md"
  - "docs/AGENTIC_RUN_PROTOCOL.md"
  - "skills/t-vbb-commit-ready/CONTRACT.yaml"
  - "skills/t-vbb-commit-ready/SKILL.md"
artifacts_produced:
  - "docs/runs/2026-05-23_1800_artifact-verify-lot-c/01_INTAKE.md"
  - "docs/runs/2026-05-23_1800_artifact-verify-lot-c/05_EXECUTION.md"
  - "docs/runs/2026-05-23_1800_artifact-verify-lot-c/07_CLOSEOUT.md"
  - "tools/vbb-loop-closure-check.py"
  - "tools/vbb-contract-runtime.py"
  - "skills/t-vbb-commit-ready/SKILL.md"
  - "skills/t-vbb-commit-ready/CONTRACT.yaml"
  - "tests/test_loop_closure.py"
  - "scripts/install-vbb-pre-commit.sh"
---

# 07_CLOSEOUT — artifact-verify-lot-c

## Résultat

La vérification mécanique des artefacts est en place. Chaque run peut
désormais être vérifié par `tools/vbb-loop-closure-check.py` : présence
des phases obligatoires selon la voie, frontmatter valide, pas de
placeholders non remplis. Le runtime émet un warning et dégrade en
PARTIAL si un artefact déclaré est manquant. Le hook git bloque le commit
si l'invariant est violé.

Le run PR #3 lui-même passe le check (voie RAPIDE : 01 + 05 + 07) —
premier run conforme à la convention de clôture qu'il instaure.

## Décisions prises

### Invariant de clôture — implémentation

| Voie | Phases vérifiées |
|------|-----------------|
| RAPIDE | 01_INTAKE + 05_EXECUTION + 07_CLOSEOUT |
| STRUCTUREE | 01_INTAKE + 04_PLAN + 05_EXECUTION + 07_CLOSEOUT |
| AUDIT | 01_INTAKE + 02_AUDIT + 03_DECISION + 07_CLOSEOUT |
| CLOTURE | 07_CLOSEOUT (inféré depuis closeout si 01_INTAKE absent) |

### FRONTMATTER_MIN (8 champs)

`run_id`, `phase`, `voie`, `status`, `agent`, `started_at`, `ended_at`,
`artifacts_produced` — délibérément plus court que `frontmatter_required`
du linter (pas de `next_phase` requis pour 07_CLOSEOUT).

### Path pattern resolution dans le runtime

- Contient `{run_id}` → substitution et check.
- Pas de vars → check littéral (ex. `docs/AUDIT_STATUS.md`).
- Autres vars (`{YYYYMMDD-HHMM}`) → skip (non résolvable au runtime).

### Règle `artifact: null`

Skip de toute vérification — aucune warning. Cohérent avec `t-vbb-status-report`.

### Voie CLOTURE auto-inférée

Si `01_INTAKE.md` absent ET `07_CLOSEOUT.md` contient `voie: CLOTURE` →
voie CLOTURE acceptée, seul 07_CLOSEOUT requis.

## Artefacts livrés (9 fichiers)

| # | Fichier | Type |
|---|---------|------|
| 1 | `tools/vbb-loop-closure-check.py` | nouveau |
| 2 | `tools/vbb-contract-runtime.py` | modifié |
| 3 | `skills/t-vbb-commit-ready/SKILL.md` | modifié |
| 4 | `skills/t-vbb-commit-ready/CONTRACT.yaml` | modifié |
| 5 | `tests/test_loop_closure.py` | nouveau |
| 6 | `scripts/install-vbb-pre-commit.sh` | nouveau |
| 7 | `docs/runs/…/01_INTAKE.md` | nouveau |
| 8 | `docs/runs/…/05_EXECUTION.md` | nouveau |
| 9 | `docs/runs/…/07_CLOSEOUT.md` | nouveau |

## Validation

### Loop closure check — tests

```
$ python3 tests/test_loop_closure.py
=== VBB Loop Closure Check — Test Suite ===

Positive tests:
  ✓ RAPIDE run — all 3 phases present
  ✓ STRUCTUREE run — all 4 phases present
  ✓ AUDIT run — all 4 phases present
  ✓ CLOTURE run — only 07_CLOSEOUT required

Negative tests:
  ✓ Missing 07_CLOSEOUT → FAIL
  ✓ STRUCTUREE missing 04_PLAN → FAIL with phase name in output
  ✓ Non-CLOTURE run without 01_INTAKE → FAIL
  ✓ Artifact missing required frontmatter field → FAIL
  ✓ Artifact with <placeholder> values → FAIL
  ✓ Run directory not found → FAIL
  ✓ Unknown voie value → FAIL

Dogfood:
  ✓ PR #3 run passes its own loop-closure check

Results: 12/12 passed, 0 failed
```

### Runtime non régressé

```
$ python3 tools/vbb-contract-runtime.py run --all --dry-run
PASS: 1 | PARTIAL: 5 | BLOCKED/FAIL: 2
```
Identique au baseline pré-PR #3.

### Runtime avec --run-id (artifact check actif)

```
$ python3 tools/vbb-contract-runtime.py run 0-vbb-scope-freeze \
    --run-id "2026-05-23_1700_contracts-artifact-schema-lot-b-d" --dry-run
→ status: PARTIAL
→ warning: ARTIFACT_MISSING — docs/runs/.../02_AUDIT.md
```
Comportement attendu : artefact manquant → PARTIAL + warning (pas BLOCKED).

### Linter non régressé

```
$ python3 tools/vbb-contract-lint.py
VBB Contract Linter — 0 error(s) found
  ✓ All contracts valid
```

### Loop closure check sur runs existants

Les runs PR #1 et PR #2 (voie STRUCTUREE, sans 01_INTAKE ni phases intermédiaires)
**échouent correctement** — comportement attendu. Ces runs ont été produits avant
l'instauration de la convention ; à corriger en PR #5 ou PR #6 (ajout d'01_INTAKE
rétroactif ou changement de voie en CLOTURE pour les runs purement documentaires).

## Règle retenue — signaler tôt, bloquer tard

| Couche | Comportement si artefact manquant |
|--------|----------------------------------|
| Runtime (`--run-id`) | warning ARTIFACT_MISSING + downgrade PASS→PARTIAL |
| Loop-closure-check | exit 1 + rapport lisible |
| Commit-ready (SKILL) | BLOCKED si `vbb-loop-closure-check.py` exit ≠ 0 |
| Pre-commit hook | `git commit` rejeté avec message actionnable |

## Points ouverts pour PR #4 / PR #5

- **Runs PR #1 et PR #2** : voie STRUCTUREE sans phases intermédiaires →
  à corriger (ajouter 01_INTAKE minimal ou changer voie en CLOTURE).
  Tracking : R-006 (nouveau, P3).
- **R-005 (P3)** : `docs/adr/` vs `docs/ADRs/` — harmonisation en PR #6.
- **R-002 (P2)** : couverture contrats 8/58 — PR #5 / Lot 5b.
- Extension loop-closure-check aux phases conditionnelles (`04_PLAN`
  si plan non trivial pour RAPIDE) → hors scope PR #3.
- `scripts/install-vbb-pre-commit.sh` non testé automatiquement
  (test shell en dehors du scope PR #3).

## État pour la prochaine session

- **Branche** : `feat/artifact-loop-closure`
- **Dernier commit** : (à créer après ce closeout)
- **Première action PR #4 (Lot E)** : créer `t-vbb-project-context-init`
  pour le bootstrap projet client.
- **Fichiers à charger** :
  - `tools/vbb-loop-closure-check.py` (outil livré)
  - `docs/runs/README.md` (convention runs)
  - `skills/INDEX.yaml` (liste complète pour PR #5)

## Mise à jour des artefacts agrégés

- [ ] `docs/CONTEXT.md` § Runs récents — ajouter ce run après commit.
- [ ] `docs/AUDIT_STATUS.md` — ajouter R-006 (runs pré-convention non conformes, P3).
- [ ] `docs/SESSION.md` — mise à jour locale au choix de l'utilisateur.
