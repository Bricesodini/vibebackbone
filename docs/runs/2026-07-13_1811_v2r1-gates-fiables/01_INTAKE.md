---
run_id: "2026-07-13_1811_v2r1-gates-fiables"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-code"
started_at: "2026-07-13T16:11:46Z"
ended_at: "2026-07-13T16:30:00Z"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/audits/tech-debt-20260713-1728.md"
  - "docs/strategy/vbb-improvements-roadmap/03_PLAN_REDUCTION_V2.md"
  - "docs/adr/0026-global-maintainability-audit-before-remediation.md"
artifacts_produced:
  - "01_INTAKE.md"
  - "POC.md"
  - "INTEGRATION_GATE.md"
---

# 01_INTAKE — v2r1-gates-fiables

## Demande reçue

> GO conditionnel pour préparer V2-R1 (03_PLAN_REDUCTION_V2.md) : « run STRUCTURED
> limité à la sélection auto du run et à l'installation unique des hooks
> (TD-101 + TD-102) » — priorité déclarée dans SESSION.md (closeout 2026-07-13_1717).
> Aucune exécution avant GO Brice.

## Reformulation

Rendre fiables les deux gates locaux : (1) la résolution du run courant devient une
fonction unique partagée entre dashboard, CI et loop-closure, avec tests des noms
mixtes (TD-101) ; (2) un installateur canonique compose les deux hooks locaux déjà
testés et l'entrée concurrente est dépréciée (TD-102).

## Scope

### Dans le périmètre
- `tools/vbb-loop-closure-check.py` — remplacement de la détection lexicale par la résolution partagée (sélecteur déclaré explicitement)
- `tools/vbb-status-dashboard.py` — extraction de la résolution mtime à deux sélecteurs : « dernier run existant » / « dernier run clôturé » (sans changement de comportement du dashboard)
- `tools/vbb-gate-check.py` — **liaison ADR stricte** : quand une ADR est explicitement référencée, vérifier celle-là, jamais de bascule vers une ADR globale acceptée (défaut observé pendant la préparation de ce run, cf. ADR-0027 décision 3)
- `scripts/install-framework-gate-hook.sh` / `scripts/install-vbb-pre-commit.sh` — convergence vers un installateur canonique + dépréciation
- `tests/` — cas de noms mixtes + reproduction TD-101 + divergence normale des deux sélecteurs + test de l'installateur + **non-régression liaison ADR** (ADR référencée PROPOSED + ADR ACCEPTED tierce → gate BLOCKED)

### Hors périmètre
- TD-103 (ruff/mypy), TD-104 (tests executor), TD-106 (fonctions longues) — backlog V2 §3
- Tout refactor au-delà de l'extraction de la résolution (consigne ADR-0026 : pas de refactor global)
- Aucun canon (CONVENTIONS/PILOTAGE intacts — pas de CCP)

### Dépendances détectées
- Prérequis plan V2 : réconciliation du worktree non propre (lot dédié, hors de ce run — les fichiers non suivis actuels sont préservés)
- ADR : `docs/adr/0027-shared-run-resolution-and-canonical-hook-installer.md` (PROPOSED → ACCEPTED au GO)
- POC : `docs/runs/2026-07-13_1811_v2r1-gates-fiables/POC.md` (DRAFT — exécution au GO)

## Classification du risque

- **Niveau** : `MODÉRÉ`
- **Justification** : outils de gate (comportement de contrôle du framework) et hooks
  git locaux ; pas de données, pas d'auth, pas d'état de production. Route STRUCTURED
  avec gate ADR + POC + intégration avant tout code (AGENTS.md règle 11).
