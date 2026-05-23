---
run_id: "2026-05-23_1800_artifact-verify-lot-c"
phase: "05_EXECUTION"
voie: "RAPIDE"
status: "READY"
agent: "claude-code"
started_at: "2026-05-23T18:05:00Z"
ended_at: "2026-05-23T18:40:00Z"
next_phase: "07_CLOSEOUT"
artifacts_consumed:
  - "tools/vbb-contract-runtime.py"
  - "docs/runs/README.md"
  - "skills/t-vbb-commit-ready/CONTRACT.yaml"
  - "skills/t-vbb-commit-ready/SKILL.md"
artifacts_produced:
  - "tools/vbb-loop-closure-check.py"
  - "tools/vbb-contract-runtime.py"
  - "skills/t-vbb-commit-ready/SKILL.md"
  - "skills/t-vbb-commit-ready/CONTRACT.yaml"
  - "tests/test_loop_closure.py"
  - "scripts/install-vbb-pre-commit.sh"
---

# 05_EXECUTION — artifact-verify-lot-c

## Livrés

### `tools/vbb-loop-closure-check.py` (nouveau)

- Lit voie depuis `01_INTAKE.md` du run (frontmatter `voie`).
- Applique matrice VOIE_REQUIRED_PHASES → liste de phases à vérifier.
- Pour chaque phase : vérifie existence + frontmatter minimal (8 champs) + détection placeholders.
- Voie CLOTURE : inférée depuis `07_CLOSEOUT.md` si `01_INTAKE.md` absent.
- CLI : `<run_id>` positionnel, `--run-id`, env `VBB_RUN_ID`, `--runs-dir` (tests).
- Exit 0 = PASS, Exit 1 = FAIL.

### `tools/vbb-contract-runtime.py` (étendu)

- Nouvelle fonction `_resolve_path_pattern(pp, run_id)` : substitue `{run_id}`, skip les patterns à autres vars (`{YYYYMMDD-HHMM}`), passe les chemins sans vars.
- Nouvelle fonction `check_artifact_existence(skill_id, contract, run_id)` : vérifie artifact primary + secondary_artifacts résolus. Règle `artifact: null` → skip.
- `execute_contract()` accepte `run_id=None` ; si fourni à depth=0 → ajoute warnings + downgrade PASS→PARTIAL.
- CLI `--run-id` ajouté.

### `skills/t-vbb-commit-ready/SKILL.md` (étendu)

- PROCESS étape 4 : appel explicite à `vbb-loop-closure-check.py`, BLOCKED si exit ≠ 0.
- Section `OUTPUT CONTRACT → Vérification mécanique` mise à jour (supprimé "à venir en PR #3").

### `skills/t-vbb-commit-ready/CONTRACT.yaml` (commentaire mis à jour)

- Note `PR #3 (Lot C): tools/vbb-loop-closure-check.py enforces this invariant.`

### `tests/test_loop_closure.py` (nouveau)

12 tests (4 positifs + 7 négatifs + 1 dogfood) — voir § Validation.

### `scripts/install-vbb-pre-commit.sh` (nouveau)

Installe `.git/hooks/pre-commit` : tire le run_id depuis le premier chemin
`docs/runs/{slug}/` dans les fichiers staged, puis appelle
`vbb-loop-closure-check.py`. BLOCKED si exit ≠ 0.

## Décisions d'exécution

- **FRONTMATTER_MIN** : `{run_id, phase, voie, status, agent, started_at, ended_at, artifacts_produced}` — délibérément plus court que `frontmatter_required` du linter (pas de `next_phase` requis pour 07_CLOSEOUT).
- **Placeholder detection** : `val.startswith("<") and val.endswith(">")` — convention chevrons existante.
- **Voie CLOTURE auto-inférée** : si `01_INTAKE.md` absent ET `07_CLOSEOUT.md` contient `voie: CLOTURE` → voie CLOTURE acceptée.
- **Secondary artifacts à timestamp** (`{YYYYMMDD-HHMM}`) : skip au runtime (non résolvables depuis run_id). Seuls les chemins contenant `{run_id}` ou sans vars sont vérifiés.
