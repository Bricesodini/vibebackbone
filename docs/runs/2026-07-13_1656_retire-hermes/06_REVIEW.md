---
run_id: "2026-07-13_1656_retire-hermes"
phase: "06_REVIEW"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-13T17:13:00+02:00"
ended_at: "2026-07-13T17:14:00+02:00"
next_phase: "07_CLOSEOUT"
artifacts_consumed:
  - "05_EXECUTION.md"
  - "04_PLAN.md"
  - "docs/audits/test-coverage-20260713-1711.md"
artifacts_produced:
  - "06_REVIEW.md"
---

# 06_REVIEW — Retire Hermes

## Périmètre relu

Suppression de la distribution, contrat CLI, hooks locaux, tests, architecture,
catalogues, canon et promesse produit limitée à quatre providers.

## Checklist Definition of Done

- [x] Seuls `claude`, `codex`, `pi`, `opencode` sont acceptés par `setup.sh`.
- [x] `distributions/hermes/` n'existe plus dans l'arbre cible.
- [x] Aucun document actif relu ne présente Hermes/Cody comme supporté.
- [x] Les références conservées sont historiques ou décrivent explicitement le retrait.
- [x] Les validations complètes passent et les changements hors scope restent exclus.

## Points conformes

- Les quatre adaptateurs ne référencent pas Hermes.
- Le retrait est déclaré breaking dans ADR 0025 et le changelog.
- Les règles génériques anciennement formulées autour de Cody sont dans Core.
- `~/.hermes/` est explicitement hors scope et n'a pas été inspecté ni modifié.

## Points à corriger

| Sévérité | Constat | Action requise | Bloquant clôture ? |
|---|---|---|---|
| `LOW` | La CI locale auto-sélectionne un run historique et produit un warning | Valider explicitement ce run avec `--strict` | non |

## Risques de régression

- Consommateurs externes de l'ancien proxy inconnus.
- Installation réelle des quatre outils tiers non couverte par les dry-runs.

## Verdict de clôture

- **GO / NO-GO** : `GO`
- **Conditions** : loop closure strict du run courant avant commit.

## Handoff vers `07_CLOSEOUT`

- **Résultat à acter** : support officiel borné à quatre providers.
- **Points ouverts à reporter** : deux limites externes non bloquantes.

## Déclaration d'auto-review (si applicable)

- [x] **Conflit d'intérêt** : même agent pour exécution et review, conflit reconnu.
- [x] **Artefacts examinés** : diff installateur/hooks/tests, docs canoniques,
  ADR 0025, audit d'impact et cartographie de tests.
- [x] **Contrôles compensatoires** : checklist du plan, scans ciblés, dry-runs,
  lint architecture/contrats, pytest complet et CI locale.
- [x] **Limitations reconnues** : pas de seconde session indépendante ni de
  validation des consommateurs externes.
