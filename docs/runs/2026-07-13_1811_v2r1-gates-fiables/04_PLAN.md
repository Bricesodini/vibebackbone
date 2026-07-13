---
run_id: "2026-07-13_1811_v2r1-gates-fiables"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-code"
started_at: "2026-07-13T16:30:00Z"
ended_at: "2026-07-13T16:40:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "POC.md (verdict GO)"
  - "docs/adr/0027-shared-run-resolution-and-canonical-hook-installer.md (ACCEPTED)"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — v2r1-gates-fiables

## Objectif

Fiabiliser les gates locaux : résolution de run unique partagée (TD-101),
installateur de hooks canonique (TD-102), liaison ADR stricte dans le gate
ADR+POC (défaut découvert à la préparation). Réf. : ADR-0027 (ACCEPTED).

## Pré-conditions

- Gate levé : `can_code_start=true` (POC GO, ADR-0027 ACCEPTED, vérif manuelle liaison OK).
- Worktree réconcilié (commits `9f22ca8`, `32a973a`).
- Recommandation `t-vbb-mode-transition-gate` du checker : **écartée** — aucun
  deploy/prod dans ce run (mot-clé détecté dans une citation de l'audit, faux positif).

## Étapes ordonnées

| # | Action | Fichiers | Test associé |
|---|--------|----------|--------------|
| 1 | Module partagé de résolution de runs : `list_runs_by_mtime`, `latest_existing_run`, `latest_closed_run`, `find_closeout` | `tools/vbb_run_resolution.py` (nouveau, helper interne — autorisé par le moratoire reformulé) | `tests/test_run_resolution.py` (noms mixtes, populations distinctes) |
| 2 | Dashboard consomme le module (sélecteur déclaré : **dernier run clôturé**), comportement inchangé | `tools/vbb-status-dashboard.py` | tests existants `test_status_dashboard*.py` (non-régression) |
| 3 | Loop-closure : auto-détection = **dernier run existant** (mtime) via le module, suppression du tri lexical ; normalisation des alias de voie (`STRUCTURED→STRUCTUREE`, `CLOSEOUT→CLOTURE`, `FAST*→RAPIDE*`) | `tools/vbb-loop-closure-check.py` | `tests/test_run_resolution.py` (subprocess `--runs-dir`, cas TD-101) |
| 4 | Gate-check : liaison ADR stricte — référence étiquetée (`Liée à ADR`/`adr_link`/`- ADR :`) prioritaire, sinon première référence explicite, **jamais de bascule globale si une référence explicite existe** ; blockers `ADR_NOT_ACCEPTED` / `ADR_REF_NOT_FOUND` | `tools/vbb-gate-check.py` | `tests/test_gate_check_adr_linkage.py` (non-régression : ADR liée PROPOSED + ADR ACCEPTED tierce → BLOCKED) |
| 5 | Installateur canonique composant les deux hooks testés (pre-commit : framework-gate puis loop-closure ; commit-msg : framework-gate) ; les deux anciens installateurs deviennent des redirections dépréciées | `scripts/install-vbb-hooks.sh` (nouveau), `scripts/install-framework-gate-hook.sh`, `scripts/install-vbb-pre-commit.sh` | `tests/test_install_vbb_hooks.sh` (repo git temporaire) |
| 6 | Rule 12 : check d'impact Core→4 distributions + entrée `docs/DISTRIBUTIONS.md` §Decisions log | `docs/DISTRIBUTIONS.md` | grep références installateurs dans `distributions/` |
| 7 | Pre-merge gate P.R2 (5 vérifications canoniques) + `06_REVIEW` + `07_CLOSEOUT` (CLOSE-FINAL) + SESSION/ACTIVITY_LOG + commit/push | docs du run | pytest complet + lints |

## Critères d'acceptation

- Loop-closure auto-détection sélectionne le dernier run existant par mtime
  (plus jamais le maximum lexical `20260615-usage-audit`).
- `voie: STRUCTURED` accepté (normalisé STRUCTUREE), plus d'erreur `unknown voie`.
- Gate-check résout l'ADR explicitement liée (0027, plus 0026) ; le scénario du
  faux PASS (ADR liée PROPOSED + ADR ACCEPTED tierce) est BLOCKED.
- `.git/hooks/pre-commit` et `commit-msg` installés, composés, exécutables ;
  les deux anciens installateurs redirigent sans perte d'étage.
- Suite pytest complète verte (baseline 133+1 → +11 nouveaux tests) ;
  pre-merge gate P.R2 5/5 PASS.

## Décisions d'implémentation (issues de la POC)

- Chaque consommateur **déclare son sélecteur** : dashboard → dernier run clôturé ;
  loop-closure (mode auto) → dernier run existant ; CI → couvert via les deux outils.
- Les deux populations ne sont jamais supposées identiques (POC critère (b)≠(c) validé).
- Pas de refactor au-delà de l'extraction (ADR-0026) : `main()` 218 lignes n'est pas
  décomposé, seule la logique de sélection change.

## Risques identifiés

- Refactor d'un outil sans test direct (`vbb-loop-closure-check.py`, main 218 L) :
  mitigé par le périmètre limité à la sélection (ADR-0026 : pas de refactor global)
  et les tests subprocess ajoutés.
- Le nouveau pre-commit composé s'applique immédiatement à ce commit même :
  comportement voulu (le gate se teste sur sa propre clôture).
- Dépréciation des installateurs : risque de chemin cassé nul (redirections `exec`).

## Rollback

Modifications additives et localisées ; rollback = `git revert` du commit du run.
Les anciens installateurs restent présents (redirections), aucun chemin utilisateur cassé.
