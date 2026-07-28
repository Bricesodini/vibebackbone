---
run_id: "2026-07-30_0700_claude-skills-discovery-01"
phase: "04_PLAN"
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
  - "01_INTAKE.md"
  - "02_FAILS_BEFORE.md"
  - "03_IMPLEMENTATION.md"
artifacts_produced:
  - "04_PLAN.md (this file)"
---

# 04_PLAN — Plan d'implémentation

## Objectif

Corriger `distributions/claude/setup.sh` pour que les skills Vibe
Backbone soient réellement découverts par Claude Code via
`~/.claude/skills/<skill-name>/SKILL.md`.

## Plan d'action

| Étape | Description | Status |
|---|---|---|
| 1 | Reproduire le bug dans un HOME isolé (fails-before) | ✅ FAIT |
| 2 | Modifier `claude_install_settings_json` (Option A) | ✅ FAIT |
| 3 | Ajouter `claude_install_skill_symlinks` (nouvelle fonction) | ✅ FAIT |
| 4 | Écrire 16 tests obligatoires dans `tests/test_claude_skills_discovery.py` | ✅ FAIT |
| 5 | Tous les tests PASS + Ruff clean | ✅ FAIT |
| 6 | Mettre à jour `docs/DISTRIBUTIONS.md` (nouvelle section) | ✅ FAIT |
| 7 | Revue indépendante (06_INDEPENDENT_REVIEW.md) | ✅ FAIT |
| 8 | Vérifications canoniques (arch lint, contract lint, pytest, CI) | ✅ FAIT |
| 9 | Validation runtime contrôlée (05_RUNTIME_VERIFICATION.md) | ✅ FAIT |
| 10 | Closeout final + commit séparé | TODO |

## Risques et mitigations

| Risque | Mitigation |
|---|---|
| Écraser un fichier utilisateur | fail-closed sur collision fichier |
| Liens cassés | recurse guard + cible absolue |
| Dérive de la liste de skills | énumération depuis `skills/` (pas de manifeste parallèle) |
| Casse `settings.json` utilisateur | préservation stricte, pas de réécriture arbitraire |
| Impact sur codex/opencode | tests de non-régression |
| HOME réel touché | tous les tests utilisent `tmp_path` (jamais `~/.claude`) |

## Architecture de la solution

```
distributions/claude/setup.sh
├── claude_install                      ← entrypoint (orchestrateur)
│   ├── claude_install_settings_json    ← préserve settings.json (sans injecter `skills`)
│   ├── claude_install_claude_md_block  ← gouvernance (inchangé)
│   ├── claude_install_prompt_commands  ← prompts (inchangé)
│   └── claude_install_skill_symlinks   ← NEW — symlinks par skill
```

## Format de la sortie attendue

Pour chaque skill canonique du dépôt (66 skills) :

```
~/.claude/skills/<skill-name>/
└── SKILL.md -> <abs_repo>/skills/<skill-name>/SKILL.md
```

## Conformité aux 5 fail-closed rules du brief

| Règle | Respect |
|---|---|
| Source SKILL.md absente | skip + warning, no crash |
| Nom de skill invalide | jamais accepté (énumération stricte) |
| Destination fichier non géré | fail-closed |
| Destination pointe ailleurs | fail-closed |
| Chemin source hors repo | fail-closed |
| Collision empêche installation sûre | fail-closed |
