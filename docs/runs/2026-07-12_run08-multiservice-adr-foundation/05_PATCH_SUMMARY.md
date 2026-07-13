# 05_PATCH_SUMMARY — Run 08 Multi-service ADR foundation

**Date** : 2026-07-12
**Route** : STRUCTURED
**Fichiers créés** : 4 ADR + index + 3 artefacts run
**Lignes ajoutées** : ~900 (ADR substantiels)

---

## 4 ADR créés

### ADR-0005 — DB Orientation (Gap-01)

**Fichier** : `docs/adr/0005-db-orientation-context-extension.md`

**Décision** : ajouter une section `## DB Orientation` typée dans `docs/CONTEXT.md`, parmi l'enum canonique :
- `owned_private`
- `shared_external_owned`
- `shared_external_readonly`
- `polyglot`
- `stateless`

**Justification** : extension pure (pas de canon modifié), permet la dérivation automatique de règles.

**Alternatives rejetées** (3) :
- A — prose libre dans `CONTEXT.md` (impossible à dériver)
- B — fichier `docs/DB_ORIENTATION.md` séparé (dispersion de l'intent)
- C — modifier `CONVENTIONS.md` (mauvais endroit — l'orientation DB est une décision projet, pas une convention de code)

### ADR-0006 — Project Archetype (Gap-02)

**Fichier** : `docs/adr/0006-project-archetype-context-extension.md`

**Décision** : ajouter une section `## Project Archetype` typée dans `docs/CONTEXT.md`, parmi l'enum canonique :
- `frontend_app`
- `api_service`
- `orchestrator`
- `read_only_consumer`
- `worker`
- `library`

**Justification** : extension cohérente avec ADR-0005 (même schéma projet).

**Alternatives rejetées** (3) :
- A — réutiliser `--mode` (sémantique DEV/PROD ≠ type projet)
- B — fichier `docs/ARCHETYPE.yaml` séparé (dispersion)
- C — inférence heuristique (fragile, ne marche pas pour les projets hybrides)

### ADR-0007 — CONTRACTS_CONSUMED canonique (Gap-05, P0)

**Fichier** : `docs/adr/0007-contracts-consumed-canonical-file.md`

**Décision** : créer un nouveau fichier canonique `docs/CONTRACTS_CONSUMED.md` (par projet) documentant structurellement ce que chaque projet consomme (api/db/event), depuis qui, dans quelle version, avec quelle criticité.

**Schema** : table à 6 colonnes (Provider, Type, Endpoint, Version, Criticité, Notes).

**Effet outils** : exploitable par `t-vbb-impact-analyzer`, `vbb-multiservice-lint`, `vbb-multiservice-graph` (futurs).

**Alternatives rejetées** (3) :
- A — prose libre dans `CONTEXT.md`
- B — README.md frontmatter (mélange presentation + architecture)
- C — manifeste technique (`package.json` etc.) — trace libraries, pas services

### ADR-0008 — CONTEXT.md / PROJECT_MODE.md enrichi (Gap-14)

**Fichier** : `docs/adr/0008-context-project-mode-enrichment.md`

**Décision** : modifier le contenu généré par `tools/vbb-project-init.py` pour produire un `CONTEXT.md` et un `PROJECT_MODE.md` structurés avec sections : Project, DB Orientation (cf. ADR-0005), Project Archetype (cf. ADR-0006), Scope (in/out), Contracts Expected, Stack, Stakeholders, Mode, Toolchain, Local-only conventions.

**Lint associé** : `vbb-context-lint.py` (futur) valide la conformité au schéma.

**Alternatives rejetées** (3) :
- A — laisser minimal + surcharger avec fichiers séparés (dispersion)
- B — schéma exhaustif 15+ sections (barrière d'entrée trop haute)
- C — frontmatter YAML de `PROJECT_MODE.md` (mélange stable/cyclique)

---

## Index — `docs/adr/README.md`

**Modification** : ajout d'une table indexe avec les 4 nouveaux ADR (status, date, source gap), plus une section « Conventions » et « Run d'origine ».

---

## Vérifications P.R2 (pre-merge gate REQUIS, route STRUCTURED)

| # | Vérification | Statut | Preuve |
|---|--------------|--------|--------|
| 1 | **Lint / format** | ✅ | `python tools/vbb-contract-lint.py` → 0 error, 0 warning |
| 2 | **Type / schema** | ✅ N/A | ADR = markdown |
| 3 | **Tests** | ✅ N/A | Aucun test ne parse les ADR (out of scope) |
| 4 | **Build** | ✅ N/A | Pas de code build |
| 5 | **Documentation coherence** | ✅ | 4 ADR présents + 4 références dans README.md |

**Verdict pre-merge gate** : **PASS**.

### Sanity checks

- ✅ `git diff docs/CONVENTIONS.md docs/PILOTAGE.md docs/AGENTIC_RUN_PROTOCOL.md docs/MVP_START_PROTOCOL.md docs/PHASE_TO_SKILLS.md` = vide
- ✅ `git diff tools/vbb-contract-lint.py tools/vbb-project-init.py` = vide
- ✅ Chaque ADR a ≥ 2 alternatives rejetées (vérifié : 3 alternatives par ADR)

---

## Récapitulatif

| Métrique | Valeur |
|----------|--------|
| Fichiers créés | 5 (4 ADR + index ADR) |
| Fichiers modifiés | 0 (canon intact) |
| Lignes ajoutées | ~900 |
| Canon touché | 0 |
| Outils créés | 0 |
| Templates créés | 0 (différé à Run 9+) |
| ADR créés | 4 (0005, 0006, 0007, 0008) |
| ADR status initial | ACCEPTED (après validation Brice) |
| Risque | Faible (documents de design seulement, pas d'implémentation) |