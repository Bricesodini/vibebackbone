---
run_id: "2026-07-14_1040_credentials-enforcement-audit"
phase: "04_PLAN"
voie: "AUDIT"
status: "READY"
agent: "codex"
started_at: "2026-07-14T10:41:00+02:00"
ended_at: "2026-07-14T10:42:00+02:00"
next_phase: "02_AUDIT"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Credentials enforcement audit

## Objectif

Qualifier la posture réelle du credentials gate et produire des exigences de
remédiation testables sans modifier l'enforcement dans ce run.

## Pré-conditions

- Worktree propre et `main` synchronisé avec `origin/main`.
- ADR 0027 acceptée pour l'architecture des hooks canoniques.
- POC synthétique GO pour la méthode d'audit sans secret réel.
- Aucun credential réel utilisé dans les vérifications.

## Étapes ordonnées

| # | Action | Fichiers cibles | Validation | Rollback |
|---|---|---|---|---|
| 1 | Audit readiness + scope freeze | gouvernance et architecture | verdicts READY | retirer rapports du run |
| 2 | Cartographier les contrôles | hooks, installer, CI, tests | trust boundary map | audit read-only |
| 3 | Tester avec fixtures factices temporaires | index Git temporaire/repo temp | exit codes observés | supprimer temp |
| 4 | Classifier findings | rapport security | traces complètes | audit read-only |
| 5 | Produire décision de suite | 03_DECISION.md | actions bornées | audit read-only |

## Critères d'acceptation

- [ ] Readiness et scope freeze explicites.
- [ ] Contrôle local, CI et bypass cartographiés.
- [ ] Aucun secret réel créé ou indexé.
- [ ] Findings avec OBSERVATION → SIGNAL → VÉRIFICATION → FINDING.
- [ ] Prochain run séparé et conditionné à une décision durable.

## Plan de rollback global

Supprimer uniquement les nouveaux artefacts d'audit ; aucune surface exécutable
n'est modifiée.

## Risques identifiés

- Faux sentiment de sécurité si le hook log-only est confondu avec un scanner.
- Faux positifs si une future politique se limite à des regex trop générales.
- Bypass Git local inhérent à `--no-verify`, à traiter comme trust boundary.

## Analyse d'impact

- **Effectuée ?**: OUI, limitée à la cartographie read-only de
  `governance-core`, `contract-tooling`, hooks et CI.
- **Périmètre d'impact**: commit local, installation des hooks, validation CI.
- **Effets de bord**: aucun dans ce run read-only.

## Integration Gate

- **ADR référencée**: `docs/adr/0027-shared-run-resolution-and-canonical-hook-installer.md`
- **Statut attendu**: ACCEPTED
- **Verdict**: PASS
- **POC référencé**: `POC.md`, verdict GO
- **CAN_CODE_START**: YES — autorise l'audit read-only, pas une implémentation.
