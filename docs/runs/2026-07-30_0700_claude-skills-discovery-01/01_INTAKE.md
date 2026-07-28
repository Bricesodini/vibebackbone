---
run_id: "2026-07-30_0700_claude-skills-discovery-01"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
kind: "DISTRIBUTION_CLAUDE_BUG_FIX"
adversarial_level: "A1"  # distribution glue fix, not affecting A2-certified governance canon
scope_id: "CLAUDE-SKILLS-DISCOVERY-01"
agent: "minimax/MiniMax-M3 (publication operator)"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
linked_subject:
  schema: "git-commit"
  certified_commit: "c4bb4b63b1e59e67d92acead1371ca6a95cf002a"
  certified_tree: "b304317010f5d3453dbc2fb972a3c0f11b51d192"
  baseline_commit: "b9084e2396f98e37e09c0e2e3bc7313a83d029f3"
started_at: "2026-07-30T07:00:00Z"
ended_at: "2026-07-30T08:30:00Z"
artifacts_produced:
  - "01_INTAKE.md (this file)"
  - "02_FAILS_BEFORE.md"
  - "03_IMPLEMENTATION.md"
  - "04_PLAN.md"
  - "04_TEST_REPORT.md"
  - "05_EXECUTION.md"
  - "05_RUNTIME_VERIFICATION.md"
  - "06_INDEPENDENT_REVIEW.md"
  - "07_CLOSEOUT.md"
---

# 01_INTAKE — CLAUDE-SKILLS-DISCOVERY-01

## 1. Objectif

Corriger la distribution Claude afin que les skills Vibe Backbone
soient réellement découverts par Claude Code.

### Mécanisme cible

`~/.claude/skills/<skill-name>/SKILL.md`

### Mécanisme actuellement utilisé (bug)

`settings.json.skills = ["~/.agents/skills"]` — clé JSON qui n'est
**pas consommée** par Claude Code comme mécanisme de découverte.

Claude Code scanne nativement les répertoires sous `~/.claude/skills/`
et charge chaque `SKILL.md` rencontré. La clé `skills` du
`settings.json` n'a aucun effet.

## 2. Baseline (au démarrage)

```yaml
baseline:
  HEAD: "b9084e2396f98e37e09c0e2e3bc7313a83d029f3"
  origin/main: "b9084e2396f98e37e09c0e2e3bc7313a83d029f3"
  working_tree: clean
  certified_commit: "c4bb4b63b1e59e67d92acead1371ca6a95cf002a"
  certification_status: CERTIFIED
  adversarial_status: PASS_ADVERSARIAL
  canonical_skills_count: 66
```

## 3. Scope autorisé

| Path | Mutable? |
|---|---|
| `distributions/claude/setup.sh` | ✅ YES |
| `docs/DISTRIBUTIONS.md` | ✅ YES |
| `distributions/claude/README.md` | ✅ YES (si nécessaire) |
| `tests/test_claude_skills_discovery.py` | ✅ YES (nouveau) |
| `docs/runs/2026-07-30_0700_claude-skills-discovery-01/**` | ✅ YES |

### Hors scope strict (ne pas toucher)

| Path | Raison |
|---|---|
| `tools/vbb-adversarial-gate.py` | Validator adversarial, immuable |
| `tools/vbb-loop-closure-check.py` | Validator, immuable |
| Contrats adversariaux | Hors scope distribution |
| Templates adversariaux | Hors scope distribution |
| Skills canoniques (`skills/**`) | Hors scope distribution |
| `distributions/codex/**` | Distribution distincte |
| `distributions/opencode/**` | Distribution distincte |
| `distributions/pi/**` | Distribution distincte |
| `docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md` | Canon v1.1 CERTIFIED |
| `docs/GATE_ASSURANCE_GOVERNANCE.md` | Canon v1.1 CERTIFIED |
| ADRs 0049/0050/0051 | Canon immuable |

## 4. Disciplines

- **Pas de modification du commit certifié** `c4bb4b63`
- **Pas de squash** avec les commits certifiés
- **HOME isolé** pour tous les tests — ne jamais toucher `~/.claude` réel
- **Idempotent** : deux exécutions successives → même état
- **Fail-closed** : toute collision mal gérée doit échouer explicitement
- **Réversible** : procédure de retrait documentée
- **Cohérent avec la philosophie M3** : `fails-before → remediation → passes-after`
  pour chaque cas

## 5. Livrables obligatoires

1. `01_INTAKE.md` (ce fichier)
2. `02_FAILS_BEFORE.md` — reproduction du bug avec preuves
3. `03_IMPLEMENTATION.md` — code modifié + rationale
4. `04_TEST_REPORT.md` — résultats des 14 tests obligatoires
5. `05_RUNTIME_VERIFICATION.md` — vérification sur copie contrôlée
6. `06_INDEPENDENT_REVIEW.md` — revue indépendante (distinct actor ou checklist)
7. `07_CLOSEOUT.md` — FINAL_STATUS + synthèse

## 6. Critères d'acceptance (acceptance criteria)

| # | Critère | Status |
|---|---|---|
| 1 | Bug reproduit avant correction (fails-before authentique) | TODO |
| 2 | Symlinks créés sous `~/.claude/skills/<name>/SKILL.md` | TODO |
| 3 | Cible = `<repo>/skills/<name>/SKILL.md` (canonique) | TODO |
| 4 | Idempotent : 2 exécutions → même état | TODO |
| 5 | Fail-closed sur collision mal gérée | TODO |
| 6 | `settings.json.skills` n'est plus ajouté comme mécanisme | TODO |
| 7 | HOME réel non touché | TODO |
| 8 | Aucune régression sur codex/opencode | TODO |
| 9 | Procédure de retrait documentée | TODO |
| 10 | Tous les tests obligatoires (≥14) PASS | TODO |

## 7. Politique Git

- **1 commit séparé** : `fix(claude): install skills through canonical discovery paths`
- Pas de squash avec commits antérieurs
- Pas de push avant validation humaine (closeout H2)
- Le commit certifié `c4bb4b6` reste immuable
- Le tag `vbb-v1.1-adversarial-certified` reste sur `c4bb4b6`

## 8. Risques identifiés

| Risque | Mitigation |
|---|---|
| Écraser un skill utilisateur existant | Fail-closed sur collision fichier |
| Casse d'autres settings Claude | Préservation stricte des clés inconnues |
| Liens cassés en cas de déplacement du repo | Liens absolus + procédure de vérification |
| Création de liens imbriqués | Vérification src hors du `~/.claude` |
| Dérive de la liste des skills | Énumération depuis le répertoire canonique |
| Impact sur codex/opencode | Tests de non-régression sur les 2 distributions |

## 9. Next action

Reproduire le bug dans un HOME isolé pour démontrer `fails-before`
authentique, puis procéder à l'implémentation.
