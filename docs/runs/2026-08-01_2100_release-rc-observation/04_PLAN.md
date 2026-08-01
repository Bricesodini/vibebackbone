---
run_id: "2026-08-01_2100_release-rc-observation"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
started_at: "2026-08-01T21:00:00Z"
ended_at: "2026-08-01T21:05:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "01_INTAKE.md"
  - "04_PLAN.md"
  - "05_EXECUTION.md"
  - "07_CLOSEOUT.md"
  - "evidence/raw/*"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
adversarial_level: "A2"
proxy_mode: "A2_DISTINCT_AGENT_PROXY"
agent: "pi-runtime"
---

# 04_PLAN — Plan d'observation

## Objectif

Observation de Vibe Backbone **v1.1.0-rc.2** (V) sur commit
**`3486300f359ff3b51effb007ed950dd48592556f`** (S) avec tag
**`v1.1.0-rc.2`** (T) en conditions réelles, depuis l'état
intégré `b4bedbb` (main), pour décider si la promotion vers
v1.1.0 stable est autorisée.

## Pré-conditions

- Aucune modification du contenu du candidat S
- Aucune correction des 33 dossiers `04_PLAN.md` historiques
- Aucune création de tag stable
- Aucune promotion automatique
- Aucune réouverture de la transition de gouvernance
- Identité RC (V/S/T) immuable
- Worktree `/tmp/vbb-rc2-observe` propre sur `b4bedbb`

## Étapes ordonnées

Les 10 étapes ci-dessous sont exécutées séquentiellement. Chaque étape produit une évidence brute dans `evidence/raw/`.

### Étape 1 — Vérification de l'état immuable

- `git ls-remote origin refs/tags/v1.1.0-rc.2` → object SHA inchangé
- `git ls-remote origin 'refs/tags/v1.1.0-rc.2^{}'` → `3486300` (S)
- `git ls-remote origin refs/heads/main` → `b4bedbb` (intégré)
- `python -c "import vibebackbone; print(vibebackbone.__version__)"` → `1.1.0-rc.2`
- `git show 3486300 --stat | head -20` → diff total inchangé

### Étape 2 — Cycle complet de CI sur main

- Lancement de la CI sur `b4bedbb` (par inspection des commandes
  équivalentes localement, dans la mesure du possible)
- État local : `vbb-loop-closure-check.py --strict` doit passer
- `vbb-architecture.py lint` — 0 errors
- `vbb-contract-lint` — 0 errors (warnings acceptables)
- `pytest tests/`

### Étape 3 — Smoke test projet vierge

- Créer `/tmp/vbb-smoke-empty/`
- Cloner le repo à `b4bedbb`
- `python tools/vbb-project-context-init.py /tmp/vbb-smoke-empty/`
- Vérifier : `docs/PROJECT_MODE.md`, `docs/CONTEXT.md`, etc. créés
- Vérifier : `docs/runs/`, `docs/adr/`, `docs/templates/` créés

### Étape 4 — Smoke test projet existant

- Utiliser un projet existant (idéalement `backbone-know` ou
  réutiliser `/tmp/vbb-rc2-measure` s'il existe)
- S'assurer que les validateurs passent sur ce projet
- `python tools/vbb-status-dashboard.py`

### Étape 5 — Exécution d'un run Vibe Backbone complet

- Run de test FAST-MINIMAL ou FAST-ZERO pour valider création/fermeture
- Vérifier : `01_INTAKE.md`, `05_PATCH_SUMMARY.md` (ou FAST_ZERO), closure
- Test direct dans `/tmp/vbb-rc2-observe/docs/runs/_smoke-test/` (run de test)

### Étape 6 — Comportement des quatre distributions

- `distributions/pi/`, `distributions/opencode/`, `distributions/codex/`, `distributions/claude/`
- Vérifier présence des artefacts minimums : `SYSTEM.md`, `AGENTS.md`, `run-preamble.md`
- Vérifier `distributions/INDEX.md` jour

### Étape 7 — Compatibilité des commandes principales

- `python tools/vbb-status-dashboard.py`
- `python tools/vbb-index.py search "release"`
- `python tools/vbb-architecture.py graph --write`
- `python tools/vbb-gate-check.py <run_dir>`
- `python tools/vbb-adversarial-gate.py <run_dir>`

### Étape 8 — Régression sur les contrats documentaires

- `tests/test_document_convention.py` (s'il existe)
- `tools/vbb-document-convention-lint.py` (s'il existe)
- Frontmatter validations : `tests/test_frontmatter*.py`

### Étape 9 — Cohérence des artefacts de release

- `package.json` : version `1.1.0-rc.2` (sur S) et `1.1.1` (sur main post-promotion)
- `CHANGELOG.md` : entry rc.2
- `RELEASE_CHECKLIST.md` : complet
- `docs/TEMPORAL_PROVENANCE.md` : à jour

### Étape 10 — Stabilité du tag et de son peel

- `git ls-remote origin refs/tags/v1.1.0-rc.2` (constante)
- `git ls-remote origin 'refs/tags/v1.1.0-rc.2^{}'` (constante)
- `git rev-parse v1.1.0-rc.2` (local)
- `git rev-parse v1.1.0-rc.2^{}` (local)

## Décisions prévues

| # | Décision | Justification |
|---|---|---|
| D1 | Opérer dans worktree `/tmp/vbb-rc2-observe` | Isolation de l'observation |
| D2 | Stash `codex/governance-kernel-architecture` dirty state | Préservation travail session antérieure |
| D3 | Pas de commit pendant ce run, sauf si évidence le justifie | Observation pure |
| D4 | Si un défaut sérieux est trouvé, émettre `RC_INVALIDATED` plutôt que corriger | Interdiction de correction silencieuse |

## Garde-fous

- **Identité RC** : V/S/T vérifiées à chaque étape
- **Tag immuable** : jamais de `git tag -d` ou `git push --delete` ici
- **Pas de rebase** : toute manipulation respecte l'historique
- **33 dossiers historiques** : non touchés

## Risques anticipés

| Risque | Mitigation |
|---|---|
| Installation peut échouer dans `/tmp` (sandbox) | Utiliser `--user` ou `venv` |
| CI GitHub Actions inaccessible localement | Reproduire les commandes localement |
| Tests qui dépendent de fichiers inaccessibles | Documenter comme limitation |
| Repos externes dans `tests/adversarial_corpus/` | Exécuter en isolation |

## Handoff

Vers `05_EXECUTION.md` pour l'exécution séquentielle des 10
vérifications. Les sorties brutes sont dans `evidence/raw/`.

## Critères d'acceptation

- `01_INTAKE.md`, `04_PLAN.md`, `05_EXECUTION.md`, `07_CLOSEOUT.md` produits
- 10 vérifications effectuées et documentées
- Chaque observation classifiée selon la taxonomie 5 statuts
- Verdict final parmi `READY_FOR_STABLE_PROMOTION` / `EXTEND_RC_OBSERVATION` / `RC_INVALIDATED`
- `07_CLOSEOUT.md` validé par `vbb-loop-closure-check.py --strict`

## Plan de rollback global

Si décision `RC_INVALIDATED` :

1. **Préservation de l'état** : ne pas toucher au tag, ni à main
2. **Documentation** : émettre le finding dans `07_CLOSEOUT.md`
3. **Handoff** : préparer un run de remédiation avec liste précise
4. **Communication** : informer Brice pour décision manuelle

Si décision `EXTEND_RC_OBSERVATION` :

1. **Identité RC** : reste intacte
2. **Extension** : nouvelle fenêtre d'observation planifiée
3. **Critères d'extension** : explicités dans `07_CLOSEOUT.md`

Si décision `READY_FOR_STABLE_PROMOTION` :

1. **Identité RC** : préservée
2. **Prep** : `07_CLOSEOUT.md` émet la consigne pour futur run de promotion
3. **Pas de création de tag stable** ici
4. **Pré-requis pour promotion stable** : nouveau freeze, nouveau tag, controles post-publication, rollback