---
run_id: "2026-07-14_1150_credentials-enforcement"
phase: "05_EXECUTION"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T12:02:00+02:00"
ended_at: "2026-07-14T12:20:00+02:00"
next_phase: "06_REVIEW"
artifacts_consumed:
  - "04_PLAN.md"
  - "POC.md"
  - "INTEGRATION_GATE.md"
  - "docs/adr/0033-layered-core-credentials-enforcement.md"
artifacts_produced:
  - "05_EXECUTION.md"
  - "../../audits/test-coverage-20260714-1210.md"
---

# 05_EXECUTION — Layered Core credentials enforcement

## Résumé

Le contrôle log-only est remplacé par un scanner différentiel Core. Le hook
analyse l'index staged ; GitHub Actions analyse une plage de commits ; les deux
partagent le même moteur et ne journalisent jamais la valeur détectée.

## Actions effectuées

| # | Étape | Statut | Preuve |
|---|---|---|---|
| 1 | ADR + POC + gate | DONE | ADR 0033, POC 11/11, `can_code_start=true` |
| 2 | Scanner Core | DONE | `tools/vbb-credentials-gate.py` |
| 3 | Hook fail-closed | DONE | appel `--staged`, outil absent/finding → exit 1 |
| 4 | CI distante | DONE | checkout complet + appel `--range BASE HEAD` |
| 5 | CI locale | DONE | nouveau check staged, total 9 |
| 6 | Installateur | DONE | préflight explicite du scanner |
| 7 | Couverture | DONE | 16 tests Python + 10 hook + 13 installateur |
| 8 | Canon/architecture | DONE | AGENTS rule 13, CCP, architecture et distributions |

## Comportement livré

- Scanne uniquement les lignes textuelles ajoutées.
- Ignore suppressions, binaires, placeholders et références d'environnement.
- Détecte plusieurs formats high-confidence et les affectations sensibles.
- Autorise un exemple uniquement avec
  `vbb: allow-credential-example reason=<slug>` et affiche un warning.
- Retourne `2` sur erreur Git sans traceback.
- Ne réaffiche jamais le contenu correspondant.

## Écarts au plan

| Écart | Type | Décision |
|---|---|---|
| `vbb-project-init --install-hook` est préexistamment cassé | hors scope consommateur | SEC-CRED-005 ouvert ; aucune copie/ownership improvisée |
| CI GitHub pas encore exécutée sur ce commit | état externe | vérifier après push ; syntaxe YAML et range testés localement |

## Tests / validations passées

- `pytest tests/test_credentials_gate.py -q` — 16 passed.
- `bash tests/test_framework_gate_hook.sh` — 10 passed.
- `bash tests/test_install_vbb_hooks.sh` — 13 passed.
- Workflow YAML chargé et step credentials vérifié.
- Python compile, Bash syntax et architecture lint : PASS.
- Full suite intermédiaire : 168 passed, 1 skipped avant les deux derniers cas.

## Fichiers principaux modifiés

- Tool : `tools/vbb-credentials-gate.py`.
- Entrées : hook, CI locale et workflow GitHub.
- Tests : module credentials, hook framework, installateur.
- Vérité : AGENTS, ADR, architecture, distributions, audits et run.

## Handoff vers `06_REVIEW`

- Rejouer la suite globale avec 170 tests attendus.
- Vérifier le diff staged avec le nouveau gate lui-même.
- Maintenir SEC-CRED-005 hors de la clôture Core.
