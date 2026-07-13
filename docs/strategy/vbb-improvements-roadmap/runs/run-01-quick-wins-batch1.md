---
context_role: run-spec
phase: 1-pre-execution
status: ready-to-execute
run_id: 2026-07-12_run01-quick-wins-batch1
route: FAST-STANDARD
updated: 2026-07-12
phase_phase_label: "Run 1 — Quick wins purs #1"
---

# Run 01 — Quick wins purs #1 (FAST-STANDARD)

> **Route** : FAST-STANDARD
> **Effort** : S (~30 min)
> **Risque canon** : aucun
> **Pre-merge gate** : SKIP (route FAST, cf. `docs/REFERENCE/pre-merge-gate.md`)
> **Statut** : `READY — en attente GO Brice`

---

## 1. Goal

Appliquer 4 quick wins purs (5 fichiers), non-canon, sans dépendance externe. Démontre la viabilité de l'approche par runs progressifs.

---

## 2. Input contract

### Required

- [ ] GO Brice sur cette spec
- [ ] `docs/strategy/vbb-improvements-roadmap/00_ROADMAP.md` lu (vue d'ensemble)
- [ ] `docs/strategy/vbb-improvements-roadmap/01_FINDINGS_INDEX.md` lu (référence findings)

### Optional

- [ ] `docs/audits/audit-E-skill-descriptions-20260712-1400.md` (contexte E-002)
- [ ] `docs/audits/audit-C-handoff-closeout-calibration-20260712-1300.md` (contexte C-001)
- [ ] `docs/audits/audit-D-md-length-optimization-20260712-1330.md` (contexte D-003)
- [ ] `docs/audits/audit-A-scope-aware-janitor-20260712-1210.md` (contexte A-003)

---

## 3. Scope

### Included — Quick wins à appliquer

#### QW-1 (AUDIT-E-002) — Documenter non-auto-troncature description

**Fichier** : `skills/0-vbb-standard/SKILL.md`

**Action** : ajouter dans la section PROCESS (ligne ~75-85) une mention explicite :

> "The `description:` field is NOT auto-truncated by any vibebackbone mechanism. It is hand-maintained and validated for **precision** (triggers, keywords) per step 6, not for length. The `setup.sh` → `distributions/codex/setup.sh` codegen pipeline operates on `~/.codex/AGENTS.md` via block replacement (`<!-- vibebackbone:generated:start -->` / `<!-- vibebackbone:generated:end -->`) and does NOT touch skill descriptions."

**Effort** : S (< 5 min).

#### QW-2 (AUDIT-C-001) — Champ `kind: HANDOFF | CLOSEOUT` dans template

**Fichier** : `docs/templates/07_CLOSEOUT.md.template`

**Action** : ajouter dans le frontmatter, après `status:` :

```yaml
kind: "<HANDOFF|CLOSEOUT>"   # HANDOFF if status != READY or next_action != null; CLOSEOUT otherwise
```

Et dans le corps, ajouter une section « Type de closeout » en haut du fichier (après `# 07_CLOSEOUT`):

```markdown
## Type de closeout

**Kind** : HANDOFF | CLOSEOUT

- **HANDOFF** : travail non terminé, reprise attendue. SESSION.md doit contenir des `Actions en cours`.
- **CLOSEOUT** : fin claire du processus. SESSION.md doit être vidé.
```

**Effort** : S (< 10 min).

#### QW-3 (AUDIT-D-003) — TOC dans GUIDE.md et README.md

**Fichiers** :
- `GUIDE.md` (1248 lignes)
- `README.md` (526 lignes)

**Action** : ajouter en haut de chaque fichier (après le frontmatter YAML éventuel, avant la première section `# ...`) une TOC générée automatiquement :

```markdown
## Table of contents

<!-- TOC générée par tools/vbb-md-toc.py (à venir) ou manuellement -->

- [Section 1](#section-1)
- [Section 2](#section-2)
...
```

**Pour Run 1, génération manuelle** (le tool `vbb-md-toc.py` n'existe pas encore). La TOC doit refléter la structure existante (titres `##` et `###`).

**Effort** : M pour GUIDE.md (~15 min, 50+ sections), S pour README.md (~5 min, 15 sections).

**Note** : alternative — utiliser `gh-md-toc` (tool externe) si disponible. Sinon, manuel.

#### QW-4 (AUDIT-A-003) — Premier bloc External Dependencies dans ARCHITECTURE.md

**Fichier** : `docs/ARCHITECTURE.md`

**Action** : ajouter un nouveau bloc YAML `## Bloc: External Dependencies` (avant ou après les 7 blocs existants). Exemple de contenu :

```yaml
id: external-dependencies
type: external
status: active
role: Inventory of out-of-repo dependencies (databases, APIs, third-party services).
responsibilities:
  - Declare external systems the repo depends on
  - Provide canonical references for cross-service discipline
depends_on:
  - governance-core
impacts:
  - impact analysis
  - cross-service coordination
files:
  - docs/ARCHITECTURE.md
contracts: []
tests: []
risks:
  - id: EXT-001
    level: P2
    note: This block is a placeholder. Real external dependencies to be declared in future runs.
```

**Effort** : S (< 5 min). Ce bloc est un **exemple** ; les vraies dépendances seront déclarées en Run 8-11 (multi-service).

---

## 4. Excluded

- ❌ Modification du canon (`docs/CONVENTIONS.md`, `docs/PILOTAGE.md`, `docs/AGENTIC_RUN_PROTOCOL.md`)
- ❌ Création d'outils Python
- ❌ Création d'ADR vibebackbone
- ❌ Production d'un run formel (`docs/runs/{id}/`) — Run 1 est trop petit, géré par ACTIVITY_LOG seul (FAST-STANDARD → ACTIVITY_LOG + 05_PATCH_SUMMARY recommandé)

---

## 5. Process

1. Créer le dossier du run : `mkdir -p docs/runs/2026-07-12_run01-quick-wins-batch1/`
2. Créer `01_INTAKE.md` : copier cette spec dans `docs/runs/2026-07-12_run01-quick-wins-batch1/01_INTAKE.md` (copie pour traçabilité)
3. Appliquer QW-1 : éditer `skills/0-vbb-standard/SKILL.md`
4. Appliquer QW-2 : éditer `docs/templates/07_CLOSEOUT.md.template`
5. Appliquer QW-3 : éditer `GUIDE.md` et `README.md`
6. Appliquer QW-4 : éditer `docs/ARCHITECTURE.md`
7. Vérifier que `vbb-architecture.py lint` passe (sanity check, peut être skip si trop long pour ce run)
8. Vérifier qu'aucun fichier canon n'a été modifié par erreur (`git diff docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md`)
9. Créer `05_PATCH_SUMMARY.md` dans le dossier run
10. Créer `07_CLOSEOUT.md` dans le dossier run
11. Mettre à jour `docs/ACTIVITY_LOG.md` (1 ligne)
12. Git commit
13. (Optionnel) git push

---

## 6. Output contract

### Artefacts à produire

| Fichier | Kind | Description |
|---------|------|-------------|
| `docs/runs/2026-07-12_run01-quick-wins-batch1/01_INTAKE.md` | phase_artifact | Copie de cette spec |
| `docs/runs/2026-07-12_run01-quick-wins-batch1/05_PATCH_SUMMARY.md` | phase_artifact | Résumé des 5 modifications |
| `docs/runs/2026-07-12_run01-quick-wins-batch1/07_CLOSEOUT.md` | phase_artifact | Closeout formel |
| `docs/ACTIVITY_LOG.md` | persistent_state_update | 1 ligne ajoutée |
| `skills/0-vbb-standard/SKILL.md` | source_modified | QW-1 |
| `docs/templates/07_CLOSEOUT.md.template` | source_modified | QW-2 |
| `GUIDE.md` | source_modified | QW-3 (TOC) |
| `README.md` | source_modified | QW-3 (TOC) |
| `docs/ARCHITECTURE.md` | source_modified | QW-4 (External Dependencies) |

### 05_PATCH_SUMMARY structure

```markdown
# 05_PATCH_SUMMARY — Run 01 Quick wins purs #1

**Date** : 2026-07-12
**Route** : FAST-STANDARD
**Fichiers modifiés** : 5

## QW-1 (AUDIT-E-002) — skills/0-vbb-standard/SKILL.md
- Ajout mention "description NOT auto-truncated"
- Lignes ajoutées : ~5

## QW-2 (AUDIT-C-001) — docs/templates/07_CLOSEOUT.md.template
- Ajout champ `kind:` dans frontmatter
- Ajout section "Type de closeout" dans le corps
- Lignes ajoutées : ~10

## QW-3 (AUDIT-D-003) — GUIDE.md + README.md
- TOC ajoutée en haut de chaque fichier
- Lignes ajoutées : ~50 (GUIDE) + ~15 (README)

## QW-4 (AUDIT-A-003) — docs/ARCHITECTURE.md
- Nouveau bloc `## Bloc: External Dependencies`
- Lignes ajoutées : ~25

## Vérifications
- [ ] `git diff docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md` → vide ✓
- [ ] `vbb-architecture.py lint` → (skip si trop long)
- [ ] Aucun fichier généré par `setup.sh` touché
```

### 07_CLOSEOUT structure

```markdown
# 07_CLOSEOUT — Run 01 Quick wins purs #1

**Kind** : CLOSEOUT
**Statut global** : COMPLET
**Date** : 2026-07-12

## Travail effectué
5 fichiers modifiés, 4 quick wins appliqués, ~110 lignes ajoutées.

## Décisions prises
- Aucun canon modifié.
- TOC générée manuellement (tool `vbb-md-toc.py` non encore créé).

## Risques résiduels
- Aucun.

## Points ouverts
- Aucun (Run 1 clos).

## Prochaine session recommandée
**Nécessaire** : Oui (Run 2 : prompts canoniques P.R2)
**Type** : FAST-MINIMAL
**Spec** : `runs/run-02-prompts-pr2.md` (à créer avant exécution)

## Artefacts
docs/runs/2026-07-12_run01-quick-wins-batch1/ → tous présents
```

---

## 7. Verification

### À exécuter avant `07_CLOSEOUT.md`

```bash
# 1. Aucun canon modifié
git diff docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md
# Attendu : vide

# 2. vbb-architecture.py lint passe (sanity check)
python tools/vbb-architecture.py lint
# Attendu : 0 erreur (les 8 blocs existants + nouveau bloc external-dependencies)

# 3. git status liste bien 5 fichiers modifiés + 3 nouveaux
git status --short
# Attendu : M pour 5 fichiers modifiés + ?? pour 3 nouveaux fichiers du run

# 4. ACTIVITY_LOG contient la ligne
grep "Run 01" docs/ACTIVITY_LOG.md
# Attendu : 1 ligne
```

### Pre-merge gate

**SKIP** — route FAST-STANDARD, voir `docs/REFERENCE/pre-merge-gate.md` :
> "Pour les routes **FAST-MINIMAL / FAST-ZERO** : SKIP de la boucle. La closeout doit déclarer la voie explicitement."

Note : la consigne parle de FAST-MINIMAL/FAST-ZERO. FAST-STANDARD est entre les deux ; par prudence, on SKIP aussi pour ce run.

---

## 8. Risques du run

| ID | Risque | Sévérité | Mitigation |
|----|--------|----------|------------|
| R-01-1 | TOC mal formée dans GUIDE.md (50+ sections à lister) | Faible | Générer avec `gh-md-toc` ou manuellement avec soin |
| R-01-2 | Bloc External Dependencies casse `vbb-architecture.py lint` | Faible | Vérifier le format YAML avant commit |
| R-01-3 | Confusion QW-2 `kind` avec un champ frontmatter existant | Faible | `grep "kind:" docs/templates/*.template` avant |

---

## 9. Acceptance criteria

Run 1 est **COMPLET** si :

- ✅ Les 5 fichiers sont modifiés
- ✅ `git diff` ne montre aucun canon modifié
- ✅ `vbb-architecture.py lint` passe (ou skip documenté)
- ✅ `05_PATCH_SUMMARY.md` existe
- ✅ `07_CLOSEOUT.md` existe avec `Kind: CLOSEOUT`
- ✅ `docs/ACTIVITY_LOG.md` contient la ligne
- ✅ git commit effectué (push optionnel)

---

## 10. Liens

- [`../00_ROADMAP.md`](../00_ROADMAP.md) — vue d'ensemble
- [`../01_FINDINGS_INDEX.md`](../01_FINDINGS_INDEX.md) — index des findings
- [`../../../docs/audits/audit-E-skill-descriptions-20260712-1400.md`](../../../docs/audits/audit-E-skill-descriptions-20260712-1400.md) — AUDIT-E-002
- [`../../../docs/audits/audit-C-handoff-closeout-calibration-20260712-1300.md`](../../../docs/audits/audit-C-handoff-closeout-calibration-20260712-1300.md) — AUDIT-C-001
- [`../../../docs/audits/audit-D-md-length-optimization-20260712-1330.md`](../../../docs/audits/audit-D-md-length-optimization-20260712-1330.md) — AUDIT-D-003
- [`../../../docs/audits/audit-A-scope-aware-janitor-20260712-1210.md`](../../../docs/audits/audit-A-scope-aware-janitor-20260712-1210.md) — AUDIT-A-003