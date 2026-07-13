---
run_id: "2026-07-13_1656_retire-hermes"
phase: "07_CLOSEOUT"
voie: "STRUCTUREE"
status: "READY"
kind: "CLOSEOUT"
agent: "codex"
started_at: "2026-07-13T17:14:00+02:00"
ended_at: "2026-07-13T17:15:00+02:00"
next_phase: null
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_AUDIT.md"
  - "03_DECISION.md"
  - "04_PLAN.md"
  - "05_EXECUTION.md"
  - "06_REVIEW.md"
  - "POC.md"
artifacts_produced:
  - "07_CLOSEOUT.md"
---

# 07_CLOSEOUT — Retire Hermes

## Type de closeout

**Kind** : `CLOSEOUT`

## Résultat

Vibebackbone livre désormais un Core commun et quatre adaptateurs officiels :
Pi, OpenCode, Codex et Claude Code. Hermes/Cody, son proxy et ses composants
exclusifs ont été retirés du dépôt courant.

**Evidence** : `setup.sh` déclare exactement quatre providers ; smoke 32/32,
pytest 133 passed / 1 skipped, CI locale 7 PASS / 1 WARN non bloquant.

## Décisions prises

- Limiter le support officiel aux quatre outils demandés, conformément à ADR 0025.
  **Evidence** : demande explicite de Brice, ADR 0025 `ACCEPTED`, POC `GO`.
- Ne pas promouvoir le proxy ni le bypass-lint dans Core.
  **Evidence** : analyse d'impact `READY / BREAKING`, dépendances spécifiques Hermes.
- Préserver les traces historiques et laisser tout état `~/.hermes/` intact.
  **Evidence** : scope du run et diff limité au dépôt Git.

## Artefacts livrés

| Phase | Fichier | Statut |
|---|---|---|
| 01_INTAKE | `docs/runs/2026-07-13_1656_retire-hermes/01_INTAKE.md` | `READY` |
| 02_AUDIT | `docs/runs/2026-07-13_1656_retire-hermes/02_AUDIT.md` | `READY` |
| 03_DECISION | `docs/runs/2026-07-13_1656_retire-hermes/03_DECISION.md` | `READY` |
| 04_PLAN | `docs/runs/2026-07-13_1656_retire-hermes/04_PLAN.md` | `READY` |
| 05_EXECUTION | `docs/runs/2026-07-13_1656_retire-hermes/05_EXECUTION.md` | `READY` |
| 06_REVIEW | `docs/runs/2026-07-13_1656_retire-hermes/06_REVIEW.md` | `READY` |
| 07_CLOSEOUT | `docs/runs/2026-07-13_1656_retire-hermes/07_CLOSEOUT.md` | `READY` |

## Change Set

- Retrait de `distributions/hermes/`, du provider CLI et des tests exclusifs.
- Neutralisation des hooks, outils et règles Core qui dépendaient de Cody.
- Alignement README, guide, architecture, catalogues, ADR, changelog et statut.
- Archivage du plan Cody v2 devenu sans objet.

## Commit Readiness

`READY` : loop closure strict, validation des claims, du plan et de l'audit de
tests passés après rédaction de ce fichier.

## Coherence Check

- Architecture et contrats : 0 erreur, 0 warning.
- Documentation active : quatre providers ; références Hermes restantes
  limitées au retrait explicite ou à l'historique.
- Modifications utilisateur non liées : conservées hors périmètre de staging.

## Points ouverts

- Aucun travail requis pour achever ce retrait.
- Un futur chantier peut ajouter une matrice d'installation réelle pour les
  quatre runtimes, sans rouvrir le support Hermes.

## Remaining Risks

- Les consommateurs externes du proxy supprimé sont inconnus.
- Les runtimes tiers eux-mêmes ne sont pas exécutés par la suite de tests.

## Risques résiduels

- Rupture intentionnelle pour `--provider hermes` et les imports directs du proxy.
- Confusion possible si un lecteur prend un run historique pour la vérité active.

## Statut dette

- **Dette remboursée** : surface Hermes, documentation parallèle et dépendance
  des tests à un chemin externe.
- **Dette acceptée** : historique Hermes conservé pour traçabilité.
- **Dette introduite** : aucune identifiée hors rupture explicitement acceptée.

## Suggested Commit Message

```text
refactor(distributions): support four coding agents

approve: brice
```

## État pour la prochaine session

- **Branche** : `main`
- **Dernier commit avant ce run** : `f2a7f05 docs(audit): close POC methodology remediation`
- **Première action concrète à reprendre** : aucune pour ce run.
- **Fichiers à charger en priorité** : `docs/CONTEXT.md`, ADR 0025, ce closeout.

## Mise à jour des artefacts agrégés

- [x] `docs/CONTEXT.md` aligné et compteur tests mis à jour.
- [x] `docs/AUDIT_STATUS.md` mis à jour avec impact et couverture.
- [x] `docs/SESSION.md` marqué CLOSEOUT, sans reprise requise.

## Next Action

Vérifier le staging ciblé puis créer le commit atomique proposé ci-dessus.
Aucun push n'est requis par cette demande.
