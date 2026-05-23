---
run_id: "2026-05-23_2100_hygiene-lot-f-g"
phase: "01_INTAKE"
voie: "RAPIDE"
status: "READY"
agent: "claude-code"
started_at: "2026-05-23T21:00:00Z"
ended_at: "2026-05-23T21:05:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "docs/runs/2026-05-23_2000_phase2-contracts-lot-5b/07_CLOSEOUT.md"
  - "skills/vibebackbone/docs/PILOTAGE.md"
  - "docs/CONTEXT.md"
  - "docs/AUDIT_STATUS.md"
  - "docs/INDEX.md"
artifacts_produced:
  - "docs/runs/2026-05-23_2100_hygiene-lot-f-g/01_INTAKE.md"
---

# 01_INTAKE — hygiene-lot-f-g

## Contexte

Suite de PR #5 (Lot 5b). Branche `feat/artifact-loop-closure` poussée et
validée. La couverture contrats est à 22/58.

Points ouverts identifiés au closeout PR #5 :

- PILOTAGE.md v2.0 contient 4 noms de skills erronés (préfixe `-p-` résiduel)
  et omet `t-vbb-status-report` des transverses.
- R-005 : `docs/AUDIT_STATUS.md` référence `docs/ADRs/` (majuscule) au lieu
  de `docs/adr/` (minuscule réel).
- `docs/CONTEXT.md` non mis à jour depuis PR #1.
- `docs/vbb-contract-runtime.md` — doc de référence interne non committé,
  flottant à la racine de `docs/`.
- `docs/audits/vbb-runtime/*.json` — traces de runtime non exclues du suivi git.

## Objectif

PR #6 — Lot F+G : hygiène documentaire uniquement.

1. PILOTAGE.md v2.1 — fix noms + add status-report + note couverture 22/58.
2. AUDIT_STATUS.md — R-005 : `docs/ADRs/` → `docs/adr/`.
3. CONTEXT.md — runs récents PR #3–#6 + prochaine action.
4. Archivage `docs/vbb-contract-runtime.md` → `docs/archive/`.
5. `.gitignore` — exclure `docs/audits/vbb-runtime/`.

## Voie

**RAPIDE** — modifications documentaires, zéro impact runtime, zéro contrat de
données, zéro impact prod.

## Scope

- `skills/vibebackbone/docs/PILOTAGE.md` : corrections nomenclature + couverture
- `docs/AUDIT_STATUS.md` : correction chemin R-005
- `docs/CONTEXT.md` : mise à jour runs récents + artefacts
- `docs/archive/vbb-contract-runtime.md` : nouveau (archivage)
- `docs/INDEX.md` : lien mis à jour
- `.gitignore` : exclusion traces runtime
- `docs/adr/README.md` + `docs/audits/README.md` : premier commit
- `docs/runs/2026-05-23_2100_hygiene-lot-f-g/` : run courant

## Hors scope

- Modification du runtime, project-init, schéma CONTRACT.yaml
- Extension INDEX.yaml (couverture déjà à 22/58, exhaustive par rapport aux
  contracts existants)
- Corrections PILOTAGE au-delà des noms de skills
