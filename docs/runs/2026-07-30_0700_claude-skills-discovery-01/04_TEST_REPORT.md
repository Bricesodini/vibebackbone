---
run_id: "2026-07-30_0700_claude-skills-discovery-01"
phase: "04_TEST_REPORT"
voie: "STRUCTUREE"
status: "READY"
kind: "DISTRIBUTION_CLAUDE_BUG_FIX"
adversarial_level: "A1"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
scope_id: "CLAUDE-SKILLS-DISCOVERY-01"
agent: "minimax/MiniMax-M3 (publication operator)"
linked_subject:
  schema: "git-commit"
  certified_commit: "c4bb4b63b1e59e67d92acead1371ca6a95cf002a"
  baseline_commit: "b9084e2396f98e37e09c0e2e3bc7313a83d029f3"
started_at: "2026-07-30T07:00:00Z"
ended_at: "2026-07-30T08:30:00Z"
artifacts_consumed:
  - "03_IMPLEMENTATION.md"
artifacts_produced:
  - "04_TEST_REPORT.md (this file)"
---

# 04_TEST_REPORT — Rapport de tests

## Résumé

**16 tests obligatoires**, tous PASS. Les 14 cas requis par le brief
sont couverts + 2 tests sanity.

## Couverture

| # | Cas obligatoire du brief | Test | Status |
|---|---|---|---|
| 1 | Installation dans un $HOME vide | `test_installation_in_empty_home` | ✅ |
| 2 | Création d'un dossier individuel par skill | `test_one_directory_per_skill` | ✅ |
| 3 | Présence de SKILL.md | `test_skill_md_present_in_each_directory` | ✅ |
| 4 | Cible du lien correcte | `test_symlink_target_is_canonical_skill_md` | ✅ |
| 5 | Seconde exécution idempotente | `test_second_run_is_idempotent` | ✅ |
| 6 | Source manquante | `test_missing_source_skill_does_not_crash` | ✅ |
| 7 | Destination utilisateur existante | `test_existing_user_file_at_destination_is_not_overwritten` | ✅ |
| 8 | Lien incorrect préexistant | `test_existing_wrong_target_symlink_is_refused` | ✅ |
| 9 | Lien cassé | `test_broken_symlink_handled_safely` | ✅ |
| 10 | Espaces dans le chemin du dépôt | `test_repo_path_with_spaces` | ✅ |
| 11 | Préservation de settings.json | `test_settings_json_is_preserved` | ✅ |
| 12 | Absence d'utilisation de settings.json.skills | `test_settings_json_skills_key_not_added` | ✅ |
| 13 | Aucun impact sur codex/opencode | `test_no_impact_on_codex_or_opencode_distributions` | ✅ |
| 14 | Désinstallation / procédure de retrait | `test_uninstall_via_rm_rf_does_not_touch_repo` | ✅ |
| 15 | Nombre correct de symlinks | `test_correct_number_of_skill_symlinks` | ✅ |
| 16 | Runner script existe | `test_runner_script_exists` | ✅ |

## Sortie pytest

```
$ python -m pytest tests/test_claude_skills_discovery.py -v

tests/test_claude_skills_discovery.py::test_installation_in_empty_home PASSED
tests/test_claude_skills_discovery.py::test_one_directory_per_skill PASSED
tests/test_claude_skills_discovery.py::test_skill_md_present_in_each_directory PASSED
tests/test_claude_skills_discovery.py::test_symlink_target_is_canonical_skill_md PASSED
tests/test_claude_skills_discovery.py::test_second_run_is_idempotent PASSED
tests/test_claude_skills_discovery.py::test_missing_source_skill_does_not_crash PASSED
tests/test_claude_skills_discovery.py::test_existing_user_file_at_destination_is_not_overwritten PASSED
tests/test_claude_skills_discovery.py::test_existing_wrong_target_symlink_is_refused PASSED
tests/test_claude_skills_discovery.py::test_broken_symlink_handled_safely PASSED
tests/test_claude_skills_discovery.py::test_repo_path_with_spaces PASSED
tests/test_claude_skills_discovery.py::test_settings_json_is_preserved PASSED
tests/test_claude_skills_discovery.py::test_settings_json_skills_key_not_added PASSED
tests/test_claude_skills_discovery.py::test_no_impact_on_codex_or_opencode_distributions PASSED
tests/test_claude_skills_discovery.py::test_uninstall_via_rm_rf_does_not_touch_repo PASSED
tests/test_claude_skills_discovery.py::test_runner_script_exists PASSED
tests/test_claude_skills_discovery.py::test_correct_number_of_skill_symlinks PASSED

========================= 16 passed in 19.97s =========================
```

## Vérifications canoniques (suite complète)

| Vérification | Résultat |
|---|---|
| `pytest tests/` | 381 passed, 1 skipped |
| `bash scripts/vbb-ci-local.sh` | 13 passed, 0 failed (1 warning non-bloquante) |
| `python tools/vbb-architecture.py lint` | 0 error |
| `python tools/vbb-contract-lint.py` | 0 error |
| `ruff check tests/test_claude_skills_discovery.py` | All checks passed |
| `ruff format --check tests/test_claude_skills_discovery.py` | formatted |

## Détails par cas

### Test 7 — Destination utilisateur existante

Le test crée un fichier utilisateur à
`~/.claude/skills/0-vbb-guide/SKILL.md` avec contenu personnalisé, puis
exécute le setup. Le contenu du fichier ne doit **jamais** être
remplacé. Vérification : `user_skill_md.read_text() == user_content`.

### Test 8 — Lien incorrect préexistant

Le test crée un symlink avec une cible invalide vers
`/some/random/wrong/target.md`, puis exécute le setup. Le lien ne doit
**pas** être silencieusement remplacé.

### Test 11 — Préservation de settings.json

Le test crée un `settings.json` avec contenu personnalisé :

```json
{"theme": "dark", "telemetry": false, "custom_key": "user_value"}
```

Après setup, le contenu doit être identique (aucune clé ajoutée,
aucune clé modifiée).

### Test 13 — Aucun impact sur codex/opencode

Le test pré-crée des sentinelles dans `~/.codex/AGENTS.md` et
`~/.config/opencode/opencode.json`, puis vérifie que le setup Claude
n'écrit dans aucun de ces chemins.

## Conclusion

**Tous les tests obligatoires sont PASS.** Le contrat fail-closed est
respecté, l'idempotence est vérifiée, les paramètres utilisateur sont
préservés, et il n'y a aucun impact sur les autres distributions.
