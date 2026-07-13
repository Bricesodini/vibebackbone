# INTEGRATION_GATE — 2026-07-13_1811_v2r1-gates-fiables

**Run**: docs/runs/2026-07-13_1811_v2r1-gates-fiables/
**Date**: 2026-07-13
**Voie**: STRUCTUREE
**Statut gate**: **BLOCKED — état préparé, attendu avant GO** (calculé par `tools/vbb-gate-check.py`)

> Rappel P.R3 — "Gate Before Action" : aucun code n'est écrit tant que
> les trois cases `## Gates` ne sont pas toutes validées.

## ADR Status

- **ADR référencé** : docs/adr/0027-shared-run-resolution-and-canonical-hook-installer.md
- **Statut attendu** : `ACCEPTED`
- **Statut observé** : `PROPOSED` (à passer `ACCEPTED` au GO Brice)
- **Verdict** : **BLOCKED** sur 0027. ⚠️ Le checker retourne `adr_present_and_accepted=true`
  en basculant sur l'ADR-0026 (ACCEPTED, citée en artefact consommé) : c'est un
  **défaut confirmé**, désormais intégré au périmètre de ce run (ADR-0027 décision 3
  — liaison ADR stricte + test de non-régression). Tant que le checker n'est pas
  corrigé, la règle manuelle prévaut : le gate ADR de ce run n'est PASS que si
  **0027 = ACCEPTED**, sans égard à la sortie du checker sur ce point.

## POC Status

- **POC référencé** : docs/runs/2026-07-13_1811_v2r1-gates-fiables/POC.md
- **Verdict attendu** : `GO`
- **Verdict observé** : `PENDING` (test défini, lecture seule, **non exécuté** — consigne « aucune exécution avant GO »)
- **Verdict gate** : BLOCKED (`POC_VERDICT_ABSENT`)

## Gates

- [ ] **ADR_REQUIRED? → Y** — 0027 doit passer `ACCEPTED` au GO Brice
- [ ] **POC_REQUIRED? → Y** — exécuter le test POC (lecture seule, < 5 min) et inscrire le verdict
- [ ] **CAN_CODE_START? → NO** — attendu `YES` après les deux étapes ci-dessus

## Calcul automatique — sortie du 2026-07-13T16:11Z (préparation)

```bash
python tools/vbb-gate-check.py docs/runs/2026-07-13_1811_v2r1-gates-fiables --json
```

```json
{
  "intake_present": true,
  "adr_required": true,
  "adr_present_and_accepted": true,
  "poc_required": true,
  "poc_present_and_go": false,
  "can_code_start": false,
  "blockers": ["POC_VERDICT_ABSENT"],
  "mode_transition": {"recommended": true, "skill": "t-vbb-mode-transition-gate"},
  "exit_intent": "FAIL"
}
```

Note : la recommandation `t-vbb-mode-transition-gate` est déclenchée par un mot-clé
de l'intake ; ce run ne touche ni deploy ni production — recommandation à écarter
explicitement au 04_PLAN.

## Séquence de levée du gate (au GO Brice)

1. Réconcilier le worktree non propre (prérequis plan V2 §2 — lot dédié, fichiers non suivis préservés).
2. Exécuter le test POC (3 commandes lecture seule) → inscrire verdict + LONG_RUN_SUMMARY.
   Attendu : divergence TD-101 reproduite ; dernier run **existant** = `1811` (ce run) ;
   dernier run **clôturé** = `1717` — populations distinctes, identité non requise.
3. Si GO : passer ADR-0027 à `ACCEPTED`.
4. Relancer `vbb-gate-check` → attendu `can_code_start=true`, 0 blocker — **et vérifier
   manuellement que l'ADR résolue est bien 0027** (règle de liaison stricte, applicable
   tant que le checker n'est pas corrigé par ce run).
5. Ouvrir `04_PLAN.md` (aucun code avant).

## Handoff

- **Si CAN_CODE_START = YES** → `04_PLAN.md` → `05_EXECUTION.md` → `06_REVIEW` → `07_CLOSEOUT` (`CLOSE-FINAL`)
- **Si CAN_CODE_START = NO** → STOP (état actuel, volontaire, en attente GO Brice)
