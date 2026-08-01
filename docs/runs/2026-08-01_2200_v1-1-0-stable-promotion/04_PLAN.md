---
run_id: "2026-08-01_2200_v1-1-0-stable-promotion"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
started_at: "2026-08-01T22:00:00Z"
ended_at: "2026-08-01T22:05:00Z"
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

# 04_PLAN — Plan de promotion v1.1.0-rc.2 → v1.1.0 stable

## Objectif

Promouvoir Vibe Backbone v1.1.0-rc.2 vers v1.1.0 stable en
respectant strictement l'identité RC et en évitant toute
modification fonctionnelle.

## Pré-conditions

- Identité RC `v1.1.0-rc.2` immuable (V/S/T)
- `origin/main` contient S_rc = `3486300`
- Tag `v1.1.0-rc.2` toujours présent et pointant sur S_rc
- Tag `v1.1.0` absent localement et à distance
- Worktree propre sur `b4bedbb`
- Décision Brice `PROMOTE_TO_STABLE` reçue
- Run d'observation RC avec verdict `READY_FOR_STABLE_PROMOTION`

## Étapes ordonnées

Les 10 étapes du protocole de promotion stable sont exécutées séquentiellement. Chaque étape produit une évidence brute dans `evidence/raw/`. La phase 7 marque un STOP obligatoire pour décision Brice avant création du tag.

### Étape 2 — Vérifier l'état de départ

Sur worktree `/tmp/vbb-stable-promote` (sur `b4bedbb`) :

- `origin/main` contient S_rc
- `v1.1.0-rc.2` pointe toujours sur S_rc
- `v1.1.0` absent localement et à distance
- Worktree propre
- Aucun `REQUIRES_FIX_BEFORE_STABLE` ni `INVALIDATES_RC` dans observation

### Étape 3 — Produire le commit stable minimal S_stable

Sur branche `chore/v1.1.0-stable-promotion` :

- Modifier `package.json` version → `1.1.0`
- Modifier `CHANGELOG.md` ajouter entrée stable 1.1.0
- Modifier `RELEASE_CHECKLIST.md` marquer stable
- Ajouter artefacts du présent run
- **Aucune** modification de : validateurs, schémas, workflows,
  distributions, contrats fonctionnels, gouvernance suspendue
- Commit `chore(release): promote v1.1.0-rc.2 to v1.1.0`
- Enregistrer SHA comme S_stable

### Étape 4 — Vérifier l'équivalence fonctionnelle

Classifier le diff `S_rc..S_stable` :

- VERSION_IDENTITY (package.json, version files)
- RELEASE_DOCUMENTATION (CHANGELOG, RELEASE_CHECKLIST)
- RUN_EVIDENCE (artefacts du run)
- FUNCTIONAL_CHANGE (à 0)

### Étape 5 — Rejouer validations sur S_stable

Worktree détaché et propre sur S_stable. Exécuter :

- `vbb-architecture.py lint`
- `vbb-contract-lint`
- `vbb-loop-closure-check.py`
- `vbb-adversarial-gate.py`
- `pytest tests/adversarial_corpus/`
- `pytest tests/`
- `bash scripts/vbb-ci-local.sh`
- `python -c "import json; print(json.load(open('package.json'))['version'])"`
- `python tools/vbb-project-init.py --target-dir /tmp/smoke-stable --dry-run`
- `python -c "import vibebackbone; ..."` (smoke test)
- `bash -n distributions/{pi,opencode,codex,claude}/setup.sh`
- `git rev-parse --verify refs/tags/v1.1.0` (doit fail)

### Étape 6 — Définir R_stable_pre

Produire le contrat stable avec hash. Forme canonique :

```yaml
R_stable_pre:
  V: "1.1.0"
  S_rc: "3486300f359ff3b51effb007ed950dd48592556f"
  S_stable: "<nouveau SHA>"
  T_rc: "v1.1.0-rc.2 -> S_rc"
  T_stable: "v1.1.0 absent, réservé"
  P: "absent ou NOT_REQUIRED"
```

### Étape 7 — Décision finale avant tag

Produire un record avec 3 choix :

- `APPROVE_STABLE_PUBLICATION`
- `DEFER_STABLE_PUBLICATION`
- `REJECT_STABLE_PUBLICATION`

**STOP** — attendre la décision Brice avant de continuer.

### Étape 8 — Publication stable transactionnelle (après APPROVE)

- `git tag -a v1.1.0 <S_stable> -m "Release v1.1.0"`
- Vérifier `git rev-parse 'v1.1.0^{commit}'` correspond à S_stable
- `git push origin main` (si commit pas déjà présent)
- `git push origin v1.1.0`

### Étape 9 — Contrôles post-publication (7)

- tag distant v1.1.0 présent
- peel exact vers S_stable
- tag RC toujours présent et inchangé
- `origin/main` contient S_stable
- version publiée = 1.1.0
- installation depuis l'état stable
- loop closure + status dashboard
- absence de divergence du contrat

### Étape 10 — Verdict

- `STABLE_RELEASE_PUBLISHED` (si tout passe)
- `READY_FOR_STABLE_PUBLICATION` (en attente d'APPROVE)
- `REVISE_BEFORE_STABLE_RELEASE` (si fail)
- `IMPLEMENTATION_FAILED_ROLLBACK_REQUIRED` (si anomalie grave)

## Décisions prévues

| # | Décision | Justification |
|---|---|---|
| D1 | Worktree `/tmp/vbb-stable-promote` | Isolation de la promotion |
| D2 | Branche `chore/v1.1.0-stable-promotion` | Convention de nommage release |
| D3 | STOP à l'étape 7 pour Brice | 2-step decision: PROMOTE intent, APPROVE publication |
| D4 | Option A: stable pointe même S = 3486300 | Recommandation du run d'observation |

## Garde-fous

- **Identité RC** : V/S/T vérifiées à chaque étape
- **Tag immuable** : `v1.1.0-rc.2` jamais déplacé
- **Pas de force-push** : push contrôlé
- **Pas de rebase** : historique respecté
- **33 plans historiques** : non touchés
- **Voie Gouvernance** : non rouverte

## Risques anticipés

| Risque | Mitigation |
|---|---|
| Écart dans la classification du diff | Re-vérifier étape 4 |
| Validations échouent sur S_stable | Abandonner, REVISE_BEFORE_STABLE_RELEASE |
| Brice choisit DEFER/REJECT | STOP, ne pas créer le tag |
| Push échoue | Re-tentative contrôlée |
| Tag distant incorrect | `git push --delete` + re-tag (uniquement si exécuté correctement) |

## Handoff

- Étape 1-2 : setup, vérification
- Étape 3-6 : commit stable, validation, contrat
- Étape 7 : STOP pour Brice
- Étape 8-9 : tag + push (après APPROVE)
- Étape 10 : verdict final

## Critères d'acceptation

- 4 phases obligatoire (01_INTAKE, 04_PLAN, 05_EXECUTION, 07_CLOSEOUT)
- Loop closure PASS
- Adversarial gate PASS
- 0 FUNCTIONAL_CHANGE dans le diff S_rc..S_stable
- Validations complètes passantes
- R_stable_pre défini + hash
- Décision Brice documentée
- Tag stable créé et poussé (après APPROVE)
- RC immuable pendant tout le run

## Plan de rollback global

Si verdict `REVISE_BEFORE_STABLE_RELEASE` :

1. **Arrêt immédiat** : pas de tag créé
2. **Documentation** : émettre le finding dans `07_CLOSEOUT.md`
3. **Handoff** : préparer un run de remédiation
4. **Communication** : informer Brice

Si verdict `IMPLEMENTATION_FAILED_ROLLBACK_REQUIRED` :

1. **Arrêt immédiat** : pas de tag
2. **Rollback** : `git reset --hard` sur `chore/v1.1.0-stable-promotion`
   pour revenir à `b4bedbb`
3. **Documentation** : émettre le finding
4. **Communication** : informer Brice

Si Brice choisit `REJECT_STABLE_PUBLICATION` :

1. **Arrêt** : pas de tag
2. **Documentation** : émettre verdict `REVISE_BEFORE_STABLE_RELEASE`
3. **Handoff** : nouveau run selon décision Brice

Si Brice choisit `DEFER_STABLE_PUBLICATION` :

1. **Arrêt** : pas de tag
2. **Préservation** : S_stable existant, branche préservée
3. **Documentation** : émettre verdict `READY_FOR_STABLE_PUBLICATION` (deferred)
4. **Handoff** : run futur pour reprendre