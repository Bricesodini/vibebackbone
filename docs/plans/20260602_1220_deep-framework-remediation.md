# Plan de remediation — Deep Framework Audit 2026-06-02 12:08

**Source principale** : `docs/audits/deep-framework-audit-20260602-1208.md`  
**Source de contexte** : `docs/runs/2026-06-02_1208_deep-framework-audit/02_AUDIT.md`  
**Plan adjacent a ne pas dupliquer** : `docs/plans/20260602_0611_audit-remediation.md`  
**Route** : STRUCTURED multi-runs  
**Mode projet** : DISTRIBUTION  
**Verdict source** : `PARTIAL`

## Objectif

Restaurer la confiance operationnelle locale du framework Vibebackbone apres le
deep audit du 2026-06-02, en traitant tous les findings ouverts sans creer une
verite parallele avec le plan d'audit `0649` deja existant.

## Triage

Le plan est STRUCTURED, pas FAST, car les corrections touchent les invariants de
verification, la fermeture des runs, les metadonnees skills/contracts, le
deploiement des prompts et la coherence documentaire. Aucun finding ne demande
un nouvel audit read-only avant planification, mais les P1 doivent etre traites
avant les nettoyages P2/P3.

## Corrections a couvrir

| ID | Severity | Correction cible | Route | Dependances |
|---|---:|---|---|---|
| VBB-DEEP-001 | P1 | Rendre `scripts/vbb-ci-local.sh` reproductible avec l'interpreteur Python actif ou configurable | STRUCTURED | aucune |
| VBB-DEEP-002 | P1 | Corriger/reclasser le dernier run invalide et faire echouer les etats UNKNOWN pertinents | STRUCTURED | VBB-DEEP-001 pour verifier |
| VBB-DEEP-003 | P1 | Clarifier la semantique `SKILL.md version` vs `CONTRACT.yaml.version` et l'encoder | STRUCTURED | decision humaine |
| VBB-DEEP-004 | P2 | Aligner `docs/INDEX.md` sur l'inventaire actif 64 skills | FAST-MINIMAL ou STRUCTURED groupe doc | apres P1 |
| VBB-DEEP-005 | P2 | Nuancer/filtrer l'etat future-date dans les status courants | STRUCTURED | decision de presentation |
| VBB-DEEP-006 | P2 | Supprimer ou archiver `skills/vibebackbone/docs/PILOTAGE.md.bak` | FAST-MINIMAL | aucune |
| VBB-DEEP-007 | P3 | Remplacer les compteurs fixes stale de `CONVENTIONS.md` par une reference dashboard ou donnees regenerees | FAST-MINIMAL | apres inventaire |
| VBB-DEEP-008 | P2 | Reconciler noms courts AGENTS avec prompts deployes/reels | STRUCTURED | recoupe VBB-AUDIT-001 |

## Sequencement recommande

### Run 1 — Verification et fermeture

**Couvre** : VBB-DEEP-001, VBB-DEEP-002  
**Priorite** : P1 bloquante pour la confiance locale  
**Fichiers probables** :

- `scripts/vbb-ci-local.sh`
- `tools/vbb-loop-closure-check.py`
- `tools/vbb-status-dashboard.py`
- `docs/runs/20260602_0817_pr-operational-principles/07_CLOSEOUT.md`
- eventuels artefacts manquants dans `docs/runs/20260602_0817_pr-operational-principles/`

**Actions** :

1. Rendre `PYTHON` configurable et coherent avec l'environnement qui passe les tests.
2. Documenter ou valider la detection des dependances Python avant lancement CI.
3. Reclasser le run `20260602_0817_pr-operational-principles` si c'etait une cloture ad hoc, ou ajouter les artefacts requis si c'etait une voie STRUCTURED/AUDIT.
4. Ajouter une regression test pour eviter qu'un latest run invalide soit presente comme etat acceptable.

**Verification minimale** :

```bash
python tools/vbb-loop-closure-check.py
pytest tests/ -q
bash scripts/vbb-ci-local.sh
```

**Sortie attendue** : local CI PASS et closure invariant restaure.

### Run 2 — Semantique de versioning skills/contracts

**Couvre** : VBB-DEEP-003 et recoupe VBB-AUDIT-005  
**Priorite** : P1, mais depend d'une decision de semantique  
**Decision requise** :

- Option A : `CONTRACT.yaml.version` represente la version du schema de contrat.
- Option B : `CONTRACT.yaml.version` represente la version fonctionnelle du skill.

**Recommendation** : Option A. Renommer ou completer le champ pour lever
l'ambiguite, par exemple `contract_schema_version`, puis documenter que
`SKILL.md version` reste la version fonctionnelle du skill.

**Fichiers probables** :

- `tools/vbb-contract-lint.py`
- `skills/*/CONTRACT.yaml`
- `skills/*/SKILL.md` seulement si la decision impose un alignement direct
- `docs/CONVENTIONS.md`
- `docs/ARCHITECTURE.md` si le contrat change de schema
- `docs/RELATIONS.md` si `ARCHITECTURE.md` change

**Actions** :

1. Formaliser la decision dans un ADR si le schema contractuel change.
2. Encoder la regle dans `vbb-contract-lint.py`.
3. Ajouter un test qui couvre au moins un mismatch explicite.
4. Mettre a jour la documentation de convention.

**Verification minimale** :

```bash
python tools/vbb-contract-lint.py
pytest tests/ -q
```

**Sortie attendue** : divergence de versioning explicable et controlee par le linter.

### Run 3 — Prompts et entrees deployees

**Couvre** : VBB-DEEP-008 et recoupe VBB-AUDIT-001  
**Priorite** : P2, mais fort impact adoption  
**Fichiers probables** :

- `AGENTS.md`
- `SYSTEM.md`
- `setup.sh`
- `prompts/`
- `prompts/canonical/`
- eventuel `prompts/INDEX.yaml`
- eventuel `prompts/canonical/INDEX.yaml`

**Actions** :

1. Inventorier les noms courts annonces : `quick-task`, `structured-task`, `audit-task`, `release-check`, `session-handoff`.
2. Choisir la source de resolution : prompts installes dans `/Users/bot/.agents/prompts/vibebackbone/` ou repo local.
3. Creer une table de mapping nom court -> fichier reel.
4. Ajuster `setup.sh` ou les consignes AGENTS/SYSTEM pour que les noms courts resolvent dans ce workspace.
5. Integrer ou referencer le plan `docs/plans/20260602_0611_audit-remediation.md` pour ne pas doubler le chantier prompts legacy/canonical.

**Verification minimale** :

```bash
find /Users/bot/.agents/prompts/vibebackbone -maxdepth 2 -type f
python tools/vbb-contract-lint.py
pytest tests/ -q
```

**Sortie attendue** : tout nom court annonce par AGENTS a une cible lisible et documentee.

### Run 4 — Hygiene documentaire et artefacts parasites

**Couvre** : VBB-DEEP-004, VBB-DEEP-006, VBB-DEEP-007  
**Priorite** : P2/P3, a faire apres les P1  
**Fichiers probables** :

- `docs/INDEX.md`
- `docs/CONVENTIONS.md`
- `skills/vibebackbone/docs/PILOTAGE.md.bak`
- eventuellement `docs/archive/`

**Actions** :

1. Aligner les compteurs publics sur 64 skills.
2. Supprimer le `.bak` versionne, ou le deplacer dans `docs/archive/` avec justification.
3. Remplacer les compteurs historiques fixes de `CONVENTIONS.md` par une reference au dashboard ou a une commande d'inventaire.
4. Ajouter un check simple si un compteur public est destine a rester statique.

**Verification minimale** :

```bash
python tools/vbb-contract-lint.py
python tools/vbb-status-dashboard.py
pytest tests/ -q
```

**Sortie attendue** : navigation documentaire coherente, sans backup parasite dans les docs de skill canonique.

### Run 5 — Temporal provenance active

**Couvre** : VBB-DEEP-005  
**Priorite** : P2 mitigee, a traiter apres restauration de la verification  
**Fichiers probables** :

- `tools/vbb-status-dashboard.py`
- `docs/TEMPORAL_PROVENANCE.md`
- `docs/AUDIT_STATUS.md`
- eventuels tests dashboard

**Actions** :

1. Ajouter un mode de lecture "date workspace courante" ou une section explicite "future-dated historical state".
2. Eviter que les notes postdatees soient presentees comme etat courant non nuance.
3. Tester que le dashboard rend visible la provenance sans bloquer les runs historiques.

**Verification minimale** :

```bash
python tools/vbb-status-dashboard.py
pytest tests/ -q
```

**Sortie attendue** : dette temporelle toujours acceptee historiquement, mais moins perturbante pour le pilotage local.

## Decision points

| Point | Decision attendue | Recommandation |
|---|---|---|
| Versioning | `CONTRACT.yaml.version` = schema ou skill ? | Schema contractuel, champ renomme/documente |
| Run invalide | Completer ou reclasser `20260602_0817_pr-operational-principles` ? | Reclasser si closeout ad hoc; sinon completer les phases manquantes |
| Prompts | Installer les prompts ou pointer vers le repo local ? | Les deux : setup installe, AGENTS a un fallback repo local explicite |
| Temporal skew | Filtrer les futurs artefacts ou seulement les annoter ? | Annoter dans dashboard, ne pas masquer l'historique |

## Verification finale obligatoire

Apres les runs 1 a 5, executer la boucle P.R2 complete :

```bash
python tools/vbb-architecture.py lint
python tools/vbb-architecture.py graph --write
python tools/vbb-contract-lint.py
python tools/vbb-loop-closure-check.py
pytest tests/ -q
bash scripts/vbb-ci-local.sh
```

## Closeout attendu

Chaque run doit produire :

- un dossier `docs/runs/<date>_<slug>/`
- un `07_CLOSEOUT.md` avec `FINAL_STATUS`
- une mise a jour de `docs/AUDIT_STATUS.md` pour les findings traites
- une mise a jour de `docs/SESSION.md` si la session devient l'etat de reprise
- un commit cible, separe des autres runs

## Ordre resume

1. Run 1 : CI locale + closure invariant.
2. Run 2 : versioning SKILL/CONTRACT.
3. Run 3 : prompts courts et mapping deploye.
4. Run 4 : hygiene documentaire.
5. Run 5 : temporal provenance active.

