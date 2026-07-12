# 05_PATCH_SUMMARY — Run 03 Phase frontmatter

**Date** : 2026-07-12
**Route** : FAST-STANDARD
**Fichiers modifiés** : 6 (5 skills + 1 nouveau fichier de cartographie)
**Lignes ajoutées** : ~165 (162 dans `PHASE_TO_SKILLS.md` + ~6 dans les frontmatters skills)

---

## QW-3.1 — Création de `docs/PHASE_TO_SKILLS.md` (cartographie canonique)

**Nouveau fichier** : `docs/PHASE_TO_SKILLS.md`

**Contenu** : cartographie explicite des phases agentiques (0, 01_INTAKE, 02_AUDIT, 03_DECISION, 04_PLAN, 05_EXECUTION, 06_REVIEW, 07_CLOSEOUT, transverse) vers les skills existantes. Inclut :
- Table de convention `phase:` (valeurs canoniques + deprecated)
- Cartographie complète par phase (0, 02_AUDIT phase 1 = audits structurels, 02_AUDIT phase 2 = audits de fond, 03_DECISION, 04_PLAN, transverse, orchestrateur)
- Règle de mise à jour (toute nouvelle skill DOIT aligner son `phase:`, pas de drift silencieux)
- Justification de la cartographie (éviter drift, permettre routing, documenter convention, tracer dépréciations)
- Liens croisés vers les fichiers canoniques

**Lignes** : 162

**Justification** : sans single source of truth, chaque skill choisirait sa valeur `phase:` arbitrairement. Le fichier documente explicitement les valeurs deprecated (`1`, `2`, `3`, `4`) avec leur remplaçant, ce qui empêche la réintroduction silencieuse.

---

## QW-3.2 — Frontmatter `phase: 02_AUDIT` sur 5 skills `1-vbb-*`

Remplacement de `phase: 1` par `phase: 02_AUDIT` dans le frontmatter de :

| Fichier | Avant | Après |
|---------|-------|-------|
| `skills/1-vbb-code-janitor/SKILL.md` | `phase: 1` | `phase: 02_AUDIT` |
| `skills/1-vbb-tech-debt/SKILL.md` | `phase: 1` | `phase: 02_AUDIT` |
| `skills/1-vbb-monolith-detector/SKILL.md` | `phase: 1` | `phase: 02_AUDIT` |
| `skills/1-vbb-conventions/SKILL.md` | `phase: 1` | `phase: 02_AUDIT` |
| `skills/1-vbb-formatter/SKILL.md` | `phase: 1` | `phase: 02_AUDIT` |

**Justification** : la valeur `1` était ambiguë (la "phase 1" du modèle agentique 01-07 inclut en réalité INTAKE, AUDIT, DECISION, PLAN, EXECUTION, REVIEW, CLOSEOUT). La valeur `02_AUDIT` est explicite : ces skills sont des **audits structurels** qui produisent un rapport. Ils correspondent à la phase 02 du modèle agentique canonique (cf. `prompts/canonical/02-p-vbb-audit.md`).

**Note de compatibilité** : la modification est non-rétrocompatible pour les consommateurs qui parsent le frontmatter et s'attendent à un entier. Cependant, aucun outil canonique (`tools/vbb-*.py`) ne parse `phase:` à ce jour. Le seul match `tools/vbb-loop-closure-check.py:72` concerne les phases d'artefacts run (string, ex. `"07_CLOSEOUT"`), pas le frontmatter SKILL.md.

---

## Vérifications

- [x] **`git diff docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md` = vide** ✓
- [x] **Aucun outil canonique ne parse `phase:` comme entier** ✓ (sanity check `grep -rn '"phase"' tools/` confirmé)
- [x] **Tous les 5 skills ont `phase: 02_AUDIT`** ✓
- [x] **`docs/PHASE_TO_SKILLS.md` existe** ✓ (162 lignes)
- [x] **Aucun canon modifié** ✓

---

## Récapitulatif

| Métrique | Valeur |
|----------|--------|
| Fichiers modifiés | 5 (frontmatter) |
| Fichiers créés | 1 (`PHASE_TO_SKILLS.md`) |
| Lignes ajoutées | ~168 |
| Canon touché | 0 |
| Outils créés | 0 |
| ADR créés | 0 |
| Risque | Faible (modification additive, canon intact) |
| Quick wins traités | 2 (QW-3.1, QW-3.2) |
| Findings résolus | AUDIT-B-004 (frontmatter ambigu, pas de cartographie) |