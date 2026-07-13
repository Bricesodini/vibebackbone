---
context_role: run-spec
phase: 1-pre-execution
status: ready-to-execute
run_id: 2026-07-12_run10-multiservice-impl-discipline
route: STRUCTURED
updated: 2026-07-12
---

# Run 10 — Multi-service implementation: Gap-04/06/10

> **Route** : STRUCTURED
> **Effort** : L (~60 min — nouvel outil canonique + 2 templates + 2 skills modifiés)
> **Risque canon** : moyen — modifie 2 skills canoniques (`1-vbb-api-contract-designer`, `2-vbb-api-auditor`), crée 1 outil canonique
> **Pre-merge gate** : REQUIS (route STRUCTURED)
> **ADR de référence** : Run 9 (ADR-0009, 0010, 0011 — tous ACCEPTED)
> **Statut** : `READY — prêt à exécuter sur GO utilisateur`

---

## 1. Goal

Implémenter concrètement les 3 ADR produits par Run 9 :
- **Gap-04** : créer `tools/vbb-multiservice-lint.py` + `docs/templates/MULTISERVICE_DISCIPLINE.yaml.template`
- **Gap-06** : créer `docs/templates/IMPACT_LOG.md.template`
- **Gap-10** : étendre `skills/1-vbb-api-contract-designer/SKILL.md` et `skills/2-vbb-api-auditor/SKILL.md` pour intégrer le champ `consumers`

---

## 2. ADR source

| ADR | Source | Action |
|-----|--------|--------|
| [ADR-0009](../../../adr/0009-multiservice-lint-discipline.md) | Gap-04 | Créer `tools/vbb-multiservice-lint.py` + `MULTISERVICE_DISCIPLINE.yaml.template` |
| [ADR-0010](../../../adr/0010-impact-log-cumulative.md) | Gap-06 | Créer `docs/templates/IMPACT_LOG.md.template` |
| [ADR-0011](../../../adr/0011-cross-service-contract-taxonomy.md) | Gap-10 | Étendre `1-vbb-api-contract-designer` + `2-vbb-api-auditor` |

---

## 3. Modifications (5 fichiers)

### 3.1 — Création de `tools/vbb-multiservice-lint.py` (Gap-04)

**Nouveau fichier** (~200-300 lignes Python).

**Architecture** :
- Lit `docs/MULTISERVICE_DISCIPLINE.yaml` si présent (config par projet)
- Applique 3 familles de règles :
  1. **DB isolation** (warning par défaut) : si `db_orientation: shared_external_*`, grep imports pour interdire accès direct DB cross-service
  2. **IMPACT_LOG à jour** (warning) : si `CONTRACTS_CONSUMED.md` existe, vérifier que `IMPACT_LOG.md` existe avec ≥ 1 entrée
  3. **CONTRACTS_CONSUMED à jour** (warning) : vérifier `Last updated < 90 jours`
- Modes : `--strict` (exit 2 si violation), `--json` (machine-readable)
- Pattern proche de `vbb-contract-lint.py` pour cohérence framework

### 3.2 — Création de `docs/templates/MULTISERVICE_DISCIPLINE.yaml.template` (Gap-04, bonus)

**Nouveau fichier** (~30 lignes).

**Contenu** : template par défaut pour `docs/MULTISERVICE_DISCIPLINE.yaml`. Valeurs par défaut : warning partout, max_age_days=90, allow-list vide.

### 3.3 — Création de `docs/templates/IMPACT_LOG.md.template` (Gap-06)

**Nouveau fichier** (~50 lignes).

**Contenu** : template pour `docs/IMPACT_LOG.md`. Frontmatter + table append-only 7 colonnes + légende + process d'entrée (référence skill `t-vbb-impact-log-update` à créer dans un futur Run).

### 3.4 — Extension de `skills/1-vbb-api-contract-designer/SKILL.md` (Gap-10)

**Modification** : ajout du champ `consumers` dans la section OUTPUT CONTRACT (ajout d'un exemple + mention obligatoire). Le champ est obligatoire (peut être liste vide).

**Diff attendu** :
- Section `## OUTPUT CONTRACT` : ajout d'un bloc `consumers:` dans l'exemple de `CONTRACT.yaml`
- Section `## PROCESS` : ajout d'une étape « Identify consumers »
- Section `## VALIDATION LOOP` : ajout du check `consumers defined (peut être [])`

### 3.5 — Extension de `skills/2-vbb-api-auditor/SKILL.md` (Gap-10)

**Modification** : ajout de la vérification de cohérence `consumers` ↔ `CONTRACTS_CONSUMED.md` des services cibles.

**Diff attendu** :
- Section `## SCOPE` : ajout d'un item « validate cross-reference with CONTRACTS_CONSUMED.md »
- Section `## PROCESS` : ajout d'une étape « cross-validate consumers against consumed contracts »

---

## 4. Excluded

- ❌ Création de la skill `t-vbb-impact-log-update` (ADR-0010, futur Run)
- ❌ Création de `CONTRACTS_PROVIDED.md` symétrique (ADR-0011 futur)
- ❌ Modification de `tools/vbb-project-init.py` (ADR-0008, autre Run)
- ❌ Création de `vbb-context-lint.py` (ADR-0008, autre Run)
- ❌ Hook CI pour `--strict` (Gap-15, futur Run)
- ❌ Tests Python pour `vbb-multiservice-lint.py` (out of scope ce run, TODO dans le code)

---

## 5. Files impact summary

| File | Type | Impact |
|------|------|--------|
| `tools/vbb-multiservice-lint.py` | **nouveau tool canonique** | ~250 lignes Python |
| `docs/templates/MULTISERVICE_DISCIPLINE.yaml.template` | nouveau template | ~30 lignes |
| `docs/templates/IMPACT_LOG.md.template` | nouveau template | ~50 lignes |
| `skills/1-vbb-api-contract-designer/SKILL.md` | modification skill canon | +30 lignes |
| `skills/2-vbb-api-auditor/SKILL.md` | modification skill canon | +20 lignes |
| `docs/runs/2026-07-12_run10-multiservice-impl-discipline/{01_INTAKE,05_PATCH_SUMMARY,07_CLOSEOUT}.md` | artefacts | nouveaux |
| `docs/ACTIVITY_LOG.md` | log | +1 ligne |

**Total** : 8 fichiers (1 nouveau tool + 2 nouveaux templates + 2 skills modifiés + 3 artefacts + 1 log entry)

---

## 6. Verification (pre-merge gate REQUIS, route STRUCTURED)

```bash
# P.R2 §1 — Lint (ne doit pas casser les contracts existants)
python tools/vbb-contract-lint.py
# Attendu : 0 erreur, 0 warning

# P.R2 §2 — Test du nouveau tool (smoke test)
python tools/vbb-multiservice-lint.py --help
# Attendu : exit 0, aide affichée
python tools/vbb-multiservice-lint.py
# Attendu : 0 violation (pas de MULTISERVICE_DISCIPLINE.yaml dans ce repo = no-project mode silencieux)

# P.R2 §3 — Tests (N/A, tests unitaires out of scope)

# P.R2 §4 — Build (N/A, pas de code build)

# P.R2 §5 — Documentation coherence
ls tools/vbb-multiservice-lint.py docs/templates/MULTISERVICE_DISCIPLINE.yaml.template docs/templates/IMPACT_LOG.md.template
# Attendu : 3 fichiers présents
grep -c "consumers" skills/1-vbb-api-contract-designer/SKILL.md skills/2-vbb-api-auditor/SKILL.md
# Attendu : > 0 hits chacun

# Sanity check : canon non lié intact
git diff docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md
# Attendu : vide
```

---

## 7. Acceptance criteria

Run 10 est **COMPLET** si :

- ✅ `tools/vbb-multiservice-lint.py` créé et exécutable (`--help` marche, `--strict` marche)
- ✅ `docs/templates/MULTISERVICE_DISCIPLINE.yaml.template` créé
- ✅ `docs/templates/IMPACT_LOG.md.template` créé
- ✅ `skills/1-vbb-api-contract-designer/SKILL.md` : champ `consumers` ajouté (PROCESS + OUTPUT CONTRACT + VALIDATION LOOP)
- ✅ `skills/2-vbb-api-auditor/SKILL.md` : cross-ref avec `CONTRACTS_CONSUMED.md` ajouté (SCOPE + PROCESS)
- ✅ `python tools/vbb-contract-lint.py` toujours 0 erreur / 0 warning (pas de régression)
- ✅ Aucun canon non lié touché
- ✅ Pre-merge gate (5 P.R2) passé
- ✅ `05_PATCH_SUMMARY.md` + `07_CLOSEOUT.md` créés avec `kind: CLOSEOUT`
- ✅ `docs/ACTIVITY_LOG.md` à jour
- ✅ git commit effectué

---

## 8. Liens

- [`../00_ROADMAP.md`](../00_ROADMAP.md) — vue d'ensemble
- [`../../../docs/adr/0009-multiservice-lint-discipline.md`](../../../adr/0009-multiservice-lint-discipline.md) — ADR Gap-04
- [`../../../docs/adr/0010-impact-log-cumulative.md`](../../../adr/0010-impact-log-cumulative.md) — ADR Gap-06
- [`../../../docs/adr/0011-cross-service-contract-taxonomy.md`](../../../adr/0011-cross-service-contract-taxonomy.md) — ADR Gap-10
- [`../../../tools/vbb-contract-lint.py`](../../../tools/vbb-contract-lint.py) — pattern de référence pour le nouveau tool
- [`../../../skills/1-vbb-api-contract-designer/SKILL.md`](../../../skills/1-vbb-api-contract-designer/SKILL.md) — cible modification Gap-10
- [`../../../skills/2-vbb-api-auditor/SKILL.md`](../../../skills/2-vbb-api-auditor/SKILL.md) — cible modification symétrique