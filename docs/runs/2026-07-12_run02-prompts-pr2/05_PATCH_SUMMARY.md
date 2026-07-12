# 05_PATCH_SUMMARY — Run 02 Prompts P.R2

**Date** : 2026-07-12
**Route** : FAST-MINIMAL
**Fichiers modifiés** : 3
**Lignes ajoutées** : ~30

---

## QW-2.1 (AUDIT-B-001) — `prompts/canonical/02-p-vbb-audit.md`

**Modification** : ajout d'une section `## Next phase` immédiatement avant `## Handoff`. La section explicite la mécanique de transition vers `03_DECISION` : ouverture du fichier suivant, règle "1 session = 1 rôle", contenu consommé par la phase suivante.

**Diff** :
```diff
 ## Handoff
 
 **Phase suivante : 03_DECISION (nouvelle session obligatoire)**
 ...
 Si verdict `BLOCKED` : signaler explicitement que le cycle ne peut continuer avant résolution.
+
+---
+
+## Next phase
+
+After `02_AUDIT` completes, transition explicitly to `03_DECISION` by opening
+[`prompts/canonical/03-p-vbb-decision.md`](03-p-vbb-decision.md) in a **new session**
+(rule: 1 session = 1 role — AUDIT and DECISION are distinct roles).
+
+The decision phase consumes this audit report (typically
+`docs/runs/{id}/02_AUDIT_REPORT.md` and/or the persistent
+`docs/audits/{type}-{date}.md`) and produces a verdict (`READY` / `PARTIAL` /
+`BLOCKED` / `UNKNOWN`) plus a chosen route family (`RAPIDE` / `STRUCTUREE` /
+`AUDIT` / `CLOTURE`).
```

**Lignes ajoutées** : 11

**Justification** : la section `## Handoff` existante parle de "transmission à un humain / nouvelle session" (artefacts, points de vigilance). La nouvelle section `## Next phase` parle de **mécanique d'enchaînement** (quel fichier ouvrir, quel artefact est consommé, quelle règle de séparation des rôles s'applique). Les deux sont complémentaires et non redondantes.

---

## QW-2.2 (AUDIT-B-001) — `prompts/canonical/03-p-vbb-decision.md`

**Modification** : ajout d'une section `## Next phase` symétrique, pointant vers `04-p-vbb-plan.md`.

**Diff** :
```diff
 ## Handoff
 
 **Phase suivante : 04_PLAN**
 ...
 - Dépendances critiques
+
+---
+
+## Next phase
+
+After `03_DECISION` completes, transition explicitly to `04_PLAN` by opening
+[`prompts/canonical/04-p-vbb-plan.md`](04-p-vbb-plan.md) in a **new session**
+(rule: 1 session = 1 role — DECISION and PLAN are distinct roles; the planner
+must not be the decider).
+
+The plan phase consumes the decision record (typically
+`docs/runs/{id}/03_DECISION_RECORD.md`) and produces a structured
+implementation plan (typically `04_PLAN.md` or `04_FIX_PLAN.md`) with
+chunked, testable units, dependencies, and risks flagged **before any
+code is written**.
```

**Lignes ajoutées** : 13

---

## QW-2.3 (AUDIT-B-002) — `prompts/canonical/05-p-vbb-execution.md`

**Modification** : ajout d'une section `## Pre-merge gate (P.R2)` entre `## Critères d'acceptation` et `## Handoff`. La section référence canoniquement `docs/REFERENCE/pre-merge-gate.md` (sans dupliquer le contenu des 5 vérifications) et donne un rappel condensé.

**Diff** :
```diff
 ## Critères d'acceptation
 
 L'EXECUTION est complète si :
 ...
 - ✅ L'artefact `05_PATCH_SUMMARY_RUN_N.md` est créé dans `docs/runs/`
 
+---
+
+## Pre-merge gate (P.R2)
+
+Before declaring the run complete and proceeding to commit, the executor MUST
+pass the **5 canonical P.R2 verifications** defined in
+[`docs/REFERENCE/pre-merge-gate.md`](../../docs/REFERENCE/pre-merge-gate.md).
+Do not duplicate the verification list here — refer to the canonical reference
+for the exact commands and the `--strict` exit-code behavior.
+
+Quick reminder (see canonical reference for full detail):
+
+1. **Lint / format** — code matches repo conventions
+2. **Type / schema** — types and schemas are consistent
+3. **Tests** — affected tests pass
+4. **Build** — affected build artefacts compile / package
+5. **Documentation coherence** — affected docs match the change
+
+If any P.R2 verification fails, the implementation is **NOT** complete. The
+executor must either fix and re-verify, or escalate via
+[`02-p-vbb-audit.md`](02-p-vbb-audit.md) (route `AUDIT`) before declaring
+the run done.
+
+---
+
 ## Handoff
```

**Lignes ajoutées** : 21

**Justification** : la règle « ne pas dupliquer le contenu canonique » est respectée — les 5 vérifications sont rappelées par titre uniquement, le détail (commandes, exit codes `--strict`) reste dans `docs/REFERENCE/pre-merge-gate.md`.

---

## Vérifications

- [x] **`git diff HEAD docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md` = vide** ✓
- [x] **Lien inter-prompt `04-p-vbb-plan.md` existe** ✓
- [x] **Référence relative `../../docs/REFERENCE/pre-merge-gate.md` depuis `prompts/canonical/` est correcte** ✓
- [x] **Aucun outil généré, aucun ADR créé, aucun canon modifié** ✓

---

## Récapitulatif

| Métrique | Valeur |
|----------|--------|
| Fichiers modifiés | 3 |
| Lignes ajoutées | ~45 |
| Canon touché | 0 |
| Outils créés | 0 |
| ADR créés | 0 |
| Risque | Faible (modifications additives dans 3 prompts guides) |