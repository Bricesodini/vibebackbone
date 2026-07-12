---
context_role: run-spec
phase: 1-pre-execution
status: awaiting-canon-approval
run_id: 2026-07-12_run07-handoff-vs-closeout
route: STRUCTURED
updated: 2026-07-12
---

# Run 07 — HANDOFF vs CLOSEOUT (STRUCTURED)

> **Route** : STRUCTURED
> **Effort** : M (~40 min)
> **Risque canon** : semi — modifie `docs/PILOTAGE.md` (canon des routes), `docs/SESSION_RULES.md`, `prompts/canonical/07-p-vbb-closeout.md`, `.gitignore`
> **Pre-merge gate** : REQUIS (route STRUCTURED, cf. `docs/REFERENCE/pre-merge-gate.md`)
> **CANON_CHANGE_PROPOSAL** : [`./run-07-CANON_CHANGE_PROPOSAL.md`](run-07-CANON_CHANGE_PROPOSAL.md) (**en attente validation humaine**)
> **Statut** : `READY — bloqué en attente d'approbation canon par Brice`

---

## 1. Goal

Rendre la discrimination **HANDOFF vs CLOSEOUT** explicite à tous les niveaux :

1. **Niveau artefact** (déjà fait par Run 1) : champ `kind:` dans `07_CLOSEOUT.md.template` — **déjà livré**.
2. **Niveau prompt** : `07-p-vbb-closeout.md` calcule automatiquement le `kind:`.
3. **Niveau gouvernance** : `SESSION_RULES.md` documente la règle de discrimination.
4. **Niveau archive locale** : `docs/SESSION.history/` archive chaque handoff (non versionné).
5. **Niveau canon (route)** : `PILOTAGE.md` sépare `CLOSEOUT` en `CLOSE-HANDOFF` (paused) et `CLOSE-FINAL` (terminated).

**Politique retenue** (cf. exchange avec Brice) :
- **Distinction logique** (champ frontmatter `kind:`), pas physique (pas de renommage `07_HANDOFF.md`).
- **SESSION.md archivé localement** dans `docs/SESSION.history/{date}.md` (gitignored), pas versionné.

---

## 2. Findings source

| ID | Finding | Fichier | Sévérité |
|----|---------|---------|----------|
| **AUDIT-C-001** | Pas de marqueur explicite `kind: HANDOFF|CLOSEOUT` dans `07_CLOSEOUT.md.template` | `docs/audits/audit-C-handoff-closeout-calibration-20260712-1300.md` | **P1 — RÉSOLU par Run 1 (QW-2)** |
| **AUDIT-C-002** | Route CLOSEOUT dans PILOTAGE.md englobe 3 usages (end/handoff/pause) | idem | P2 |
| **AUDIT-C-003** | SESSION.md pas versionné / archivé | idem | P2 |
| **AUDIT-C-004** (dérivé) | `07-p-vbb-closeout.md` ne calcule pas le kind automatiquement | idem | P2 — implicite |

**Source audit** : [`docs/audits/audit-C-handoff-closeout-calibration-20260712-1300.md`](../../../audits/audit-C-handoff-closeout-calibration-20260712-1300.md)

---

## 3. Modifications

### QW-C-1 — Calcul automatique du kind dans `prompts/canonical/07-p-vbb-closeout.md`

**Modification** : ajout d'une étape 1 dans la section « Rôle » ou nouveau bloc « Étape 1 — Calculer le kind » avant les entrées à lire.

**Contenu à insérer** (avant « ## Entrées à lire ») :

```markdown
## Étape 1 — Calculer le kind

Avant tout autre calcul, déterminer le `kind:` du closeout selon la règle canonique :

- **`CLOSEOUT`** si : `status = READY` ET `next_phase = null` ET toutes les actions critiques du run sont closes.
- **`HANDOFF`** si : au moins une de ces conditions est vraie :
  - `status ≠ READY` (PARTIAL, BLOCKED, UNKNOWN)
  - `next_phase ≠ null` (un run suivant est prévu)
  - des `Actions en cours` non triviales subsistent dans `docs/SESSION.md`
  - le run n'a pas atteint sa cible canon

Annoncer le kind en haut de l'artefact `07_CLOSEOUT.md` :

> **Kind** : `HANDOFF` — travail non terminé, reprise attendue. `docs/SESSION.md` contient des `Actions en cours`.

ou

> **Kind** : `CLOSEOUT` — fin claire du processus. `docs/SESSION.md` doit être vidé après ce closeout.
```

### QW-C-2 — Section « Handoff vs Closeout » dans `docs/SESSION_RULES.md`

**Modification** : ajout d'une section après « Anti-patterns » et avant « Links ».

**Contenu à insérer** :

```markdown
## Handoff vs Closeout

The `07_CLOSEOUT.md` artefact carries an explicit `kind:` field in its frontmatter, distinguishing two semantics:

- **`HANDOFF`** : travail non terminé, reprise attendue. `docs/SESSION.md` (local, gitignored) contains non-trivial `Actions en cours`. The next session should resume from this state.
- **`CLOSEOUT`** : fin claire du processus. `docs/SESSION.md` is emptied (or replaced by a pointer to this closeout) before the run is declared complete.

**Rule of thumb:**

- If the run produced value AND nothing meaningful is left for the next session → `CLOSEOUT`.
- If the run produced partial value AND the next session must resume work → `HANDOFF`.

**Session history archive:** every handoff is mirrored to `docs/SESSION.history/{YYYY-MM-DD}.md` (local, gitignored) before `SESSION.md` is updated for the next session. This preserves continuity across machine reinstalls without leaking session content into the versioned repo.

Canonical reference: [`docs/templates/07_CLOSEOUT.md.template`](../templates/07_CLOSEOUT.md.template) (frontmatter `kind:` field).
```

### QW-C-3 — Archivage SESSION.md dans `.gitignore` + note dans `docs/SESSION.md`

**Modifications** :

1. **`.gitignore`** : ajouter (s'il n'existe pas) :
```
# Local session history (handoff archive, not versioned)
docs/SESSION.history/
```

2. **`docs/SESSION.md`** (gitignored, local) : ajouter en haut du fichier une note :
```markdown
> **Note** : à chaque handoff (kind: HANDOFF), ce fichier est archivé dans `docs/SESSION.history/{YYYY-MM-DD}.md` (gitignored) avant d'être mis à jour pour la prochaine session. Cf. `docs/SESSION_RULES.md` § Handoff vs Closeout.
```

### R-C-5 — Séparation route CLOSEOUT dans `docs/PILOTAGE.md` (CANON_CHANGE_PROPOSAL)

**Modification** : remplacer la ligne « End of session, handoff, pause » par deux routes distinctes dans la table « The 4 route families ».

**État actuel** (PILOTAGE.md ligne 27) :

| **CLOSEOUT** | End of session, handoff, pause | `t-vbb-commit-ready` → git commit → git push → update `SESSION.md` + `CONTEXT.md` | — |

**État proposé** :

| **CLOSE-HANDOFF** | Pause, travail non terminé, reprise attendue | `t-vbb-commit-ready` → git commit → git push → archive `SESSION.md` to `docs/SESSION.history/` → update `SESSION.md` for next session | — |
| **CLOSE-FINAL** | Fin de session, run terminé | `t-vbb-commit-ready` → git commit → git push → empty `SESSION.md` → update `CONTEXT.md` | — |

**Justification** : la discrimination explicite permet à un agent qui reçoit l'une ou l'autre consigne de savoir s'il doit préserver le contexte (handoff) ou vider la mémoire (final).

**Note sur `AGENTIC_RUN_PROTOCOL.md`** : ce fichier référence `07_CLOSEOUT.md` comme artefact canonique de la phase 07. **Pas de modification** — l'artefact reste `07_CLOSEOUT.md` (avec son champ `kind:`), seule la route change.

---

## 4. Excluded

- ❌ Renommage `07_CLOSEOUT.md` → `07_HANDOFF.md` (R-C-2) — UN-C-1/2 : distinction logique uniquement
- ❌ Modification de `07_CLOSEOUT.md.template` — déjà fait par Run 1 (QW-2)
- ❌ Modification de `docs/AGENTIC_RUN_PROTOCOL.md` — la phase 07 reste `CLOSEOUT` (artefact canon), seule la route change
- ❌ Création d'ADR — non requis (changement de routes, pas d'architecture)
- ❌ Création d'outil nouveau (POC) — utilisation d'outils existants (`t-vbb-session-handoff` pour l'archivage)
- ❌ Modification de `docs/CONVENTIONS.md` — le concept HANDOFF/CLOSEOUT est dans `SESSION_RULES.md`, pas dans CONVENTIONS

---

## 5. Process (post-validation canon)

1. **Attente validation** du CANON_CHANGE_PROPOSAL par Brice (porte canon)
2. Modifier `prompts/canonical/07-p-vbb-closeout.md` (QW-C-1)
3. Modifier `docs/SESSION_RULES.md` (QW-C-2)
4. Modifier `.gitignore` + `docs/SESSION.md` (QW-C-3)
5. Modifier `docs/PILOTAGE.md` (R-C-5)
6. Créer artefacts run : `01_INTAKE.md`, `05_PATCH_SUMMARY.md`, `07_CLOSEOUT.md` (kind: `CLOSEOUT`)
7. **Pre-merge gate** (cf. spec §7)
8. Mettre à jour `docs/ACTIVITY_LOG.md`
9. Git commit

---

## 6. Files impact summary

| File | Type | Impact |
|------|------|--------|
| `prompts/canonical/07-p-vbb-closeout.md` | prompt (modif QW-C-1) | +25 lignes (nouvelle section Étape 1) |
| `docs/SESSION_RULES.md` | gouvernance (modif QW-C-2) | +20 lignes (nouvelle section) |
| `.gitignore` | gitignore (modif QW-C-3) | +3 lignes |
| `docs/SESSION.md` | local gitignored (modif QW-C-3) | +5 lignes (note) |
| `docs/PILOTAGE.md` | **canon** (modif R-C-5) | remplace 1 ligne par 2 dans la table |
| `docs/runs/2026-07-12_run07-handoff-vs-closeout/01_INTAKE.md` | artefact | nouveau |
| `docs/runs/2026-07-12_run07-handoff-vs-closeout/05_PATCH_SUMMARY.md` | artefact | nouveau |
| `docs/runs/2026-07-12_run07-handoff-vs-closeout/07_CLOSEOUT.md` | artefact | nouveau (kind: CLOSEOUT) |
| `docs/ACTIVITY_LOG.md` | activity log | +1 ligne |

**Total** : 9 fichiers (5 modifs, 3 nouveaux artefacts, 1 log entry)

---

## 7. Verification (pre-merge gate REQUIS, route STRUCTURED)

```bash
# P.R2 §1 — Lint / format
python tools/vbb-contract-lint.py
# Attendu : 0 erreur, 0 warning

# P.R2 §2 — Type / schema (N/A pour modifications markdown)
python -c "import yaml; yaml.safe_load(open('docs/PILOTAGE.md').read().split('---')[1] if '---' in open('docs/PILOTAGE.md').read() else '')"
# Attendu : pas d'erreur YAML

# P.R2 §3 — Tests (N/A sauf tests YAML)
ls tests/
# Vérifier qu'aucun test ne parse PILOTAGE.md

# P.R2 §4 — Build (N/A, pas de code build)

# P.R2 §5 — Documentation coherence
grep "CLOSE-HANDOFF\|CLOSE-FINAL" docs/PILOTAGE.md  # 2 hits attendus
grep "Étape 1 — Calculer le kind" prompts/canonical/07-p-vbb-closeout.md  # 1 hit
grep "Handoff vs Closeout" docs/SESSION_RULES.md  # 1 hit
grep "SESSION.history" .gitignore  # 1 hit
test -f docs/runs/2026-07-12_run07-handoff-vs-closeout/07_CLOSEOUT.md

# Sanity check : seul PILOTAGE.md est touché parmi les fichiers canon
git diff docs/CONVENTIONS.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md
# Attendu : vide

# Sanity check : AGENTIC_RUN_PROTOCOL.md non touché
git diff docs/AGENTIC_RUN_PROTOCOL.md
# Attendu : vide (la phase 07 reste CLOSEOUT, seule la route change)
```

---

## 8. Acceptance criteria

Run 7 est **COMPLET** si :

- ✅ CANON_CHANGE_PROPOSAL validé par Brice
- ✅ `prompts/canonical/07-p-vbb-closeout.md` : section « Étape 1 — Calculer le kind » ajoutée
- ✅ `docs/SESSION_RULES.md` : section « Handoff vs Closeout » ajoutée
- ✅ `.gitignore` : `docs/SESSION.history/` ignoré
- ✅ `docs/SESSION.md` : note d'archivage ajoutée
- ✅ `docs/PILOTAGE.md` : routes `CLOSE-HANDOFF` et `CLOSE-FINAL` remplacent `CLOSEOUT`
- ✅ `docs/CONVENTIONS.md` / `AGENTIC_RUN_PROTOCOL.md` / `MVP_START_PROTOCOL.md` / `PHASE_TO_SKILLS.md` non modifiés
- ✅ Pre-merge gate (5 P.R2) passé
- ✅ `05_PATCH_SUMMARY.md` + `07_CLOSEOUT.md` créés avec `kind: CLOSEOUT`
- ✅ `docs/ACTIVITY_LOG.md` à jour
- ✅ git commit effectué

---

## 9. Liens

- [`./run-07-CANON_CHANGE_PROPOSAL.md`](run-07-CANON_CHANGE_PROPOSAL.md) — proposition canon (gate obligatoire)
- [`../00_ROADMAP.md`](../00_ROADMAP.md) — vue d'ensemble
- [`../01_FINDINGS_INDEX.md`](../01_FINDINGS_INDEX.md) — index des findings
- [`../../../docs/audits/audit-C-handoff-closeout-calibration-20260712-1300.md`](../../../audits/audit-C-handoff-closeout-calibration-20260712-1300.md) — source AUDIT-C-002/003
- [`../../../docs/PILOTAGE.md`](../../../PILOTAGE.md) — canon des routes (cible R-C-5)
- [`../../../docs/SESSION_RULES.md`](../../../SESSION_RULES.md) — gouvernance sessions (cible QW-C-2)
- [`../../../prompts/canonical/07-p-vbb-closeout.md`](../../../prompts/canonical/07-p-vbb-closeout.md) — prompt closeout (cible QW-C-1)
- [`../../../docs/templates/CANON_CHANGE_PROPOSAL.md.template`](../../../templates/CANON_CHANGE_PROPOSAL.md.template) — template canon