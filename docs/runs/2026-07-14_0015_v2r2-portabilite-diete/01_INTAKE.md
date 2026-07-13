---
run_id: "2026-07-14_0015_v2r2-portabilite-diete"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-code"
started_at: "2026-07-13T22:15:00Z"
ended_at: "2026-07-13T22:22:00Z"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/strategy/vbb-improvements-roadmap/03_PLAN_REDUCTION_V2.md"
  - "docs/audits/tech-debt-20260713-1728.md (TD-105, TD-107)"
artifacts_produced:
  - "01_INTAKE.md"
---

# 01_INTAKE — v2r2-portabilite-diete

## Demande reçue

> GO Brice (2026-07-13) : « le plus important c'est d'abord de boucler le
> ponçage de vibebackbone. fait tout ce qui permet de finaliser » — V2-R2 du
> plan (portabilité + vérité unique + diète boot, CCP requis).

## Reformulation

Deux lots (plan V2 §2). **Lot Core** : purge des chemins morts `~/02_Dev` et
`/Users/bot` des surfaces actives (TD-105) ; réconciliation des entrées
vérifiées de AUDIT_STATUS/TECH_DEBT (TD-107 : QOA-003 résolu par V2-R1,
note PyYAML périmée) ; suppression des compteurs maintenus à la main dans les
fichiers de boot (cause de dérive « 63/64 ») ; dédoublonnage AGENTS/SYSTEM/CLAUDE
(cible boot ≤ ~1 200 mots, actuel 2 156) avec synchronisation de la copie
`distributions/pi/SYSTEM.md`. **Lot état externe** : `~/.claude/CLAUDE.md`
(machine utilisateur, hors repo) — sauvegarde puis remplacement des sections de
gouvernance VibeCodex par un pointeur vers le canon VBB (fin de la double
grammaire) ; la section délégation locale est conservée (infra, pas gouvernance).

## Scope

### Dans le périmètre
- `AGENTS.md`, `SYSTEM.md`, `CLAUDE.md` (boot set — canon, CCP requis)
- `docs/PILOTAGE.md`, `docs/RUNBOOK.md`, `docs/LONG_RUN_RULE.md` (chemins morts)
- `docs/AUDIT_STATUS.md` (QOA-003), `docs/TECH_DEBT.md` (TD-001 PyYAML)
- `distributions/pi/SYSTEM.md` (copie synchronisée — Rule 12)
- `docs/DISTRIBUTIONS.md` §7 (décision Rule 12)
- Hors repo, avec sauvegarde : `~/.claude/CLAUDE.md`

### Hors périmètre
- Toute réduction du GUIDE (hors cible de ce run)
- Le générateur de boot files (ADR-0012 codegen — design seulement, pas d'outillage ici)
- Aucun changement de règle de fond : la diète réorganise et déduplique, elle ne
  supprime aucune exigence canonique

### Dépendances détectées
- ADR : `docs/adr/0030-boot-set-diet-and-portability.md`
- CCP : `docs/runs/2026-07-14_0015_v2r2-portabilite-diete/CANON_CHANGE_PROPOSAL.md`
- V2-R1 livré (preuve de résolution pour clore QOA-003)

## Classification du risque

- **Niveau** : `MODÉRÉ-ÉLEVÉ`
- **Justification** : touche le canon de boot consommé par les quatre agents à
  chaque session — toute perte de règle serait systémique. Mitigation : diète à
  contenu constant (déduplication + pointeurs, zéro exigence supprimée),
  vérification avant/après par liste de règles, CCP tracé.
