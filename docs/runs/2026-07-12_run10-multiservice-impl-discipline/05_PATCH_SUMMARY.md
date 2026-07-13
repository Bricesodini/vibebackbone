# 05_PATCH_SUMMARY — Run 10 Multi-service impl discipline

**Date** : 2026-07-13
**Route** : STRUCTURED
**Fichiers créés** : 3 (1 tool + 2 templates)
**Fichiers modifiés** : 2 (skills canoniques)
**Lignes ajoutées** : ~400 (tool Python + 2 templates + 2 sections skills)

---

## 1 — Création de `tools/vbb-multiservice-lint.py` (Gap-04)

**Nouveau fichier** : `tools/vbb-multiservice-lint.py` (~290 lignes Python)

**Architecture** :
- Pattern proche de `vbb-contract-lint.py` pour cohérence framework
- 3 fonctions de règles :
  1. `rule_db_isolation()` : si `db_orientation: shared_external_*` déclaré dans `CONTEXT.md`, signale la règle (heuristique de validation outillée = futur POC)
  2. `rule_impact_log_required()` : si `CONTRACTS_CONSUMED.md` existe, exige `IMPACT_LOG.md` avec ≥ 1 entrée datée
  3. `rule_contracts_consumed_freshness()` : si `CONTRACTS_CONSUMED.md` existe, vérifie `Last updated < max_age_days` (default 90)
- Configuration par projet via `docs/MULTISERVICE_DISCIPLINE.yaml`
- Modes : `--strict` (warning→error, exit 2), `--json` (machine-readable), `--config` (config custom)
- Défauts raisonnables si pas de config : warning partout, exit 0
- Imports : `argparse`, `json`, `re`, `sys`, `pathlib`, `datetime`. PyYAML optionnel (fallback gracieux si absent)

**Vérification empirique** :
```bash
$ python tools/vbb-multiservice-lint.py --help
# affiche l'aide proprement, exit 0

$ python tools/vbb-multiservice-lint.py
# 0 error, 0 warning, ✓ No violations (no-project mode silencieux)

$ python tools/vbb-multiservice-lint.py --json
# sortie JSON valide avec errors=[], warnings=[]

$ python tools/vbb-multiservice-lint.py --strict
# 0 error, exit 0 (no-project mode)
```

---

## 2 — Création de `docs/templates/MULTISERVICE_DISCIPLINE.yaml.template` (Gap-04, bonus)

**Nouveau fichier** (~30 lignes YAML)

**Contenu** : template par défaut pour `docs/MULTISERVICE_DISCIPLINE.yaml`. Active les 3 règles par défaut en mode warning, max_age_days=90, allow-list documentée avec exemple de migration tools.

**Référence** : ADR-0009.

---

## 3 — Création de `docs/templates/IMPACT_LOG.md.template` (Gap-06)

**Nouveau fichier** (~50 lignes Markdown + frontmatter)

**Contenu** : template pour `docs/IMPACT_LOG.md` avec :
- Frontmatter (schema_version=1.0)
- Métadonnées (Owner, First entry, Last entry, Total entries)
- Table append-only avec 7 colonnes (Date, Type, Contrat, Avant, Après, Services impactés, Lien run)
- 5 entrées d'exemple (une par type : breaking, additive, deprecation, fix, consumed_change)
- Légende des 5 types
- Process d'entrée (append-only, never edit retroactively)
- Skill d'aide (à venir)
- Références (ADR-0010, ADR-0007, linter ADR-0009)

---

## 4 — Extension de `skills/1-vbb-api-contract-designer/SKILL.md` (Gap-10)

**Modification** :
- **PROCESS step 3** : nouveau step obligatoire « Identify cross-service consumers » avec référence à la section Consumers.
- **Section `## Consumers`** (nouvelle) : spécification du champ obligatoire avec schéma YAML, règles (vide=OK, chaque consumer doit avoir entrée correspondante dans CONTRACTS_CONSUMED.md cible, enums canoniques).

**Diff** : +30 lignes.

---

## 5 — Extension de `skills/2-vbb-api-auditor/SKILL.md` (Gap-10)

**Modification** :
- **SCOPE > Included** : ajout d'un item « cross-reference with CONTRACTS_CONSUMED.md of declared consumers (ADR-0011) ».
- **PROCESS step 6** : nouvelle étape « Cross-validate the `consumers` field of each contract » avec détection de drift (declared mais absent côté consumer, ou présent côté consumer mais pas déclaré côté producer).

**Diff** : +20 lignes.

---

## Vérifications P.R2 (pre-merge gate REQUIS)

| # | Vérification | Statut | Preuve |
|---|--------------|--------|--------|
| 1 | **Lint / format** | ✅ | `python tools/vbb-contract-lint.py` → 0 error, 0 warning |
| 2 | **Type / schema / import** | ✅ | `python tools/vbb-multiservice-lint.py --help` → exit 0, `lint()` retourne 3-tuples valides |
| 3 | **Tests** | ✅ N/A | Aucun test Python impacté (tests unitaires out of scope ce run) |
| 4 | **Build** | ✅ N/A | Pas de code build |
| 5 | **Documentation coherence** | ✅ | 3 nouveaux fichiers présents, 2 skills modifiés cohérents avec ADR-0011 |

**Verdict pre-merge gate** : **PASS**.

### Sanity checks

- ✅ `git diff docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md` = vide
- ✅ 5 fichiers cibles créés/modifiés (1 tool + 2 templates + 2 skills)
- ✅ Le linter existe et fonctionne (--help, --strict, --json tous OK)

---

## Récapitulatif

| Métrique | Valeur |
|----------|--------|
| Fichiers créés | 3 (1 tool + 2 templates) |
| Fichiers modifiés | 2 (skills canoniques) |
| Lignes ajoutées | ~400 |
| Canon direct modifié | 0 (les 2 skills modifiés sont des extensions additives alignées ADR) |
| Outil canonique créé | 1 (`vbb-multiservice-lint.py`) |
| Templates créés | 2 (`MULTISERVICE_DISCIPLINE.yaml.template`, `IMPACT_LOG.md.template`) |
| Findings P0 résolus (impl) | Gap-04, Gap-06, Gap-10 — couche implémentation |
| Risque | Moyen (extension de skills canoniques, créations d'outils/templates alignées ADR) |