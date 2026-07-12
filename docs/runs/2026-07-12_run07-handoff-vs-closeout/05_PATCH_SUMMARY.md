# 05_PATCH_SUMMARY — Run 07 HANDOFF vs CLOSEOUT

**Date** : 2026-07-12
**Route** : STRUCTURED
**Fichiers modifiés** : 5 (PILOTAGE.md canon, 07-p-vbb-closeout.md, SESSION_RULES.md, .gitignore, SESSION.md)
**Fichiers créés** : 1 (CCP) + 3 artefacts run + ACTIVITY_LOG entry
**Lignes ajoutées** : ~70 (canon split + prompt + gouvernance + gitignore)
**CANON_CHANGE_PROPOSAL** : status `APPROVED` (validation Brice 2026-07-12)

---

## R-C-5 — Séparation route CLOSEOUT dans `docs/PILOTAGE.md`

**Modification** : remplacement de la ligne unique `**CLOSEOUT**` (ligne 53 du tableau "The 4 route families") par deux routes distinctes.

**Avant** :

```markdown
## The 4 route families

...

| **CLOSEOUT** | End of session, handoff, pause | `t-vbb-commit-ready` → git commit → git push → update `SESSION.md` + `CONTEXT.md` | — |
```

**Après** :

```markdown
## The 5 route families

...

| **CLOSE-HANDOFF** | Pause, travail non terminé, reprise attendue | `t-vbb-commit-ready` → git commit → git push → archive `SESSION.md` to `docs/SESSION.history/` → update `SESSION.md` for next session | — |
| **CLOSE-FINAL** | Fin de session, run terminé | `t-vbb-commit-ready` → git commit → git push → empty `SESSION.md` → update `CONTEXT.md` | — |
```

**Triage rule mis à jour** (ligne 67) :

```markdown
4. End of session ? → CLOSE-HANDOFF (paused, reprise attendue) or CLOSE-FINAL (terminated): t-vbb-commit-ready → git commit → git push → update SESSION.md (archive if HANDOFF, empty if FINAL) → update CONTEXT.md
```

**Note** : `TIMEOUT_CLOSEOUT` (lignes 122, 124, 159, 174) est conservé — c'est un concept différent (bloc YAML pour timeout), pas une route famille.

**Note** : `07_CLOSEOUT.md` (artefact de la phase 07, voir AGENTIC_RUN_PROTOCOL.md) garde son nom canonique. Seule la **route** change ; l'**artefact** reste.

---

## QW-C-1 — Étape 1 dans `prompts/canonical/07-p-vbb-closeout.md`

**Modification** : ajout d'une section « Étape 1 — Calculer le kind » avant « ## Entrées à lire » (ligne 44).

**Contenu ajouté** :

```markdown
## Étape 1 — Calculer le kind

Avant tout autre calcul, déterminer le `kind:` du closeout selon la règle canonique (cf. `docs/SESSION_RULES.md` § Handoff vs Closeout) :

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

**Lignes** : +21

---

## QW-C-2 — Section « Handoff vs Closeout » dans `docs/SESSION_RULES.md`

**Modification** : ajout d'une nouvelle section entre « Anti-patterns » (ligne 25) et « Links » (ligne 49).

**Contenu ajouté** :

```markdown
## Handoff vs Closeout

The `07_CLOSEOUT.md` artefact carries an explicit `kind:` field in its frontmatter, distinguishing two semantics:
...
```

**Lignes** : +17

---

## QW-C-3 — Archivage SESSION.md dans `.gitignore` + note dans `docs/SESSION.md`

**Modifications** :

1. **`.gitignore`** : ajout d'une ligne sous `docs/SESSION.md` / `docs/SESSION.*.md` :
```
# Local session history archive (handoff snapshots, per-machine)
docs/SESSION.history/
```

2. **`docs/SESSION.md`** (gitignored) : ajout d'une note en haut du fichier :
```markdown
> **Note** : à chaque handoff (kind: HANDOFF), ce fichier est archivé dans `docs/SESSION.history/{YYYY-MM-DD}.md` (gitignored) avant d'être mis à jour pour la prochaine session. Cf. `docs/SESSION_RULES.md` § Handoff vs Closeout.
```

---

## Vérifications P.R2 (pre-merge gate REQUIS, route STRUCTURED)

| # | Vérification | Statut | Preuve |
|---|--------------|--------|--------|
| 1 | **Lint / format** | ✅ | `python tools/vbb-contract-lint.py` → 0 error, 0 warning |
| 2 | **Type / schema** | ✅ N/A | Modifications markdown uniquement |
| 3 | **Tests** | ✅ N/A | Aucun test ne parse PILOTAGE.md ou SESSION_RULES.md |
| 4 | **Build** | ✅ N/A | Pas de code build |
| 5 | **Documentation coherence** | ✅ | Tous les grep checks passent (cf. spec §7) |

**Verdict pre-merge gate** : **PASS** (5 P.R2 vérifications vertes ou N/A justifié).

---

## Détails des vérifications

- ✅ `grep "CLOSE-HANDOFF" docs/PILOTAGE.md` → 2 hits (tableau + triage rule)
- ✅ `grep "CLOSE-FINAL" docs/PILOTAGE.md` → 2 hits (tableau + triage rule)
- ✅ `grep "## The 5 route families" docs/PILOTAGE.md` → 1 hit (titre mis à jour)
- ✅ `grep "Étape 1 — Calculer le kind" prompts/canonical/07-p-vbb-closeout.md` → 1 hit
- ✅ `grep "## Handoff vs Closeout" docs/SESSION_RULES.md` → 1 hit
- ✅ `grep "SESSION.history" .gitignore` → 1 hit
- ✅ `grep "SESSION.history" docs/SESSION.md` → 1 hit
- ✅ `git diff docs/CONVENTIONS.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md` → empty
- ✅ `grep -rn '"CLOSEOUT"' tools/` → 3 hits (string constants pour `voie:` RAPIDE/STRUCTUREE/AUDIT/CLOSEOUT — concept différent de route, conservé)

---

## Récapitulatif

| Métrique | Valeur |
|----------|--------|
| Fichiers modifiés | 5 (PILOTAGE.md canon + 4 non-canon) |
| Fichiers créés | 4 (CCP + 3 artefacts run) |
| Lignes ajoutées | ~70 |
| Canon touché | 1 fichier (PILOTAGE.md, split route families) |
| Outils créés | 0 |
| ADR créés | 0 |
| Quick wins traités | 3 (QW-C-1, QW-C-2, QW-C-3) |
| Findings résolus | AUDIT-C-002 (route split), AUDIT-C-003 (archive convention), AUDIT-C-004 dérivé (auto-calcul kind) |
| Risque | Semi (canon modifié, additif, back-compat au niveau artifact) |