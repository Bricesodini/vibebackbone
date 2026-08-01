---
run_id: "2026-08-01_2100_release-rc-observation"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
started_at: "2026-08-01T21:00:00Z"
ended_at: "2026-08-01T21:00:00Z"
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/runs/2026-08-01_0815_release-freeze-integration/07_CLOSEOUT.md"
  - "docs/runs/2026-08-01_1200_rc2-candidate/07_CLOSEOUT.md"
  - "docs/runs/2026-08-01_0752_release-freeze-publish/07_CLOSEOUT.md"
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

# 01_INTAKE — Observation v1.1.0-rc.2 et décision de promotion

## Référence immuable (V/S/T)

```yaml
V: "1.1.0-rc.2"
S: "3486300f359ff3b51effb007ed950dd48592556f"
T:
  tag: "v1.1.0-rc.2"
  tag_object_sha: "54561520eedb1632d6257879dbea973f08cb6f99"
  peeled_commit_sha: "3486300f359ff3b51effb007ed950dd48592556f"
  remote_pushed: true
  peel_correct: true
R_pre_sha256: "32a94f80e356582ebd21996e4f8872832f899d9436fdc301f1672ef34fb362bb"
main_merge_sha: "b4bedbbd4528e55b6d81d537bc1e6a465f62e157"
integration_run: "docs/runs/2026-08-01_0815_release-freeze-integration/"
```

**Interdiction fondamentale** : aucune modification de l'identité de
cette RC n'est autorisée pendant ce run.

## Cadre de la fenêtre d'observation

### Critères de clôture obligatoires

La fenêtre est bornée par :

1. **Un cycle complet de CI sur main** — vérification `vbb-ci.yml`
   sur le commit intégré `b4bedbb`
2. **Un test d'installation depuis l'état publié** — installation
   de la RC via `pip install` / `npm install` / clone-and-run depuis
   les sources publiées
3. **Un smoke test réel sur un projet vierge** — `vbb-init.sh` /
   `python tools/vbb-project-context-init.py` sur path vide
4. **Un smoke test sur un projet existant** — reprise d'un projet
   Vibe Backbone antérieur, exécution des validateurs
5. **Au moins un run Vibe Backbone complet exécuté avec la RC** —
   voie STRUCTUREE depuis l'init jusqu'au closeout
6. **Collecte des retours ou incidents éventuels**

### Critères de durée

La durée calendaire n'est pas souveraine. La clôture dépend des
preuves obtenues. Les sorties brutes sont conservées dans
`evidence/raw/`.

### Vérifications obligatoires (10)

| # | Vérification | Surface |
|---|---|---|
| V1 | Installation propre | `tools/`, `distributions/`, `requirements.txt` |
| V2 | Initialisation d'un nouveau projet | `vbb-project-context-init.py` |
| V3 | Reprise d'un projet existant | minimal + maximal |
| V4 | Exécution des validateurs | `vbb-architecture.py`, `vbb-contract-lint`, `vbb-loop-closure-check.py` |
| V5 | Création et fermeture d'un run | structure 01_INTAKE → 07_CLOSEOUT |
| V6 | Comportement des quatre distributions | `pi`, `opencode`, `codex`, `claude` |
| V7 | Compatibilité des commandes principales | `python tools/vbb-status-dashboard.py`, `vbb-index.py`, etc. |
| V8 | Absence de régression sur les contrats documentaires | templates, frontmatter, validateurs |
| V9 | Cohérence des artefacts de release | `package.json`, `CHANGELOG.md`, `RELEASE_CHECKLIST.md` |
| V10 | Stabilité du tag et de son peel | `git ls-remote refs/tags/v1.1.0-rc.2` |

### Classification des observations

| Statut | Critère |
|---|---|
| `NO_ISSUE` | Comportement attendu conforme |
| `COSMETIC` | Différence visible sans impact fonctionnel |
| `ACCEPTABLE_STABLE_RISK` | Risque acceptable pour promotion stable |
| `REQUIRES_FIX_BEFORE_STABLE` | Correction requise avant promotion |
| `INVALIDATES_RC` | Invalide la RC — rollback requis |

Pour chaque problème : reproduction, impact, périmètre, workaround,
lien avec la RC, recommandation.

## Dette documentaire historique — exclusion

Les **33 dossiers `04_PLAN.md` non conformes** dans `origin/main` :

- **Hors périmètre** de la validation fonctionnelle de la RC
- **Non bloquants** tant qu'ils ne cassent ni installation, ni CI, ni usage courant
- **À ouvrir dans un run dédié** de remédiation historique

**Aucun de ces 33 dossiers** ne sera corrigé dans ce run.

## Verdicts autorisés

| Verdict | Pré-requis |
|---|---|
| `READY_FOR_STABLE_PROMOTION` | 0 `REQUIRES_FIX_BEFORE_STABLE`, 0 `INVALIDATES_RC`, install+smoke PASS, CI main stable, décision humaine augmentée favorable, identité RC inchangée |
| `EXTEND_RC_OBSERVATION` | Évidence insuffisante ou incident en cours d'analyse |
| `RC_INVALIDATED` | Au moins 1 finding `INVALIDATES_RC` non remédiable |

## Interdictions strictes

- Aucune réécriture ou suppression du tag RC
- Aucune correction silencieuse pendant l'observation
- Aucune promotion stable automatique
- Aucune réouverture de la transition de gouvernance
- Aucune remédiation globale des 33 plans historiques dans ce run

## Sources consommées

- [`docs/runs/2026-08-01_0815_release-freeze-integration/07_CLOSEOUT.md`](docs/runs/2026-08-01_0815_release-freeze-integration/07_CLOSEOUT.md) — verdict integration réalisée
- [`docs/runs/2026-08-01_1200_rc2-candidate/07_CLOSEOUT.md`](docs/runs/2026-08-01_1200_rc2-candidate/07_CLOSEOUT.md) — verdict `READY_FOR_RELEASE_FREEZE`
- [`docs/runs/2026-08-01_0752_release-freeze-publish/07_CLOSEOUT.md`](docs/runs/2026-08-01_0752_release-freeze-publish/07_CLOSEOUT.md) — verdict `REVISE_BEFORE_RELEASE`

## Niveau d'assurance

**A2 (Distinct Agent Proxy)** — Publication/release promotion
nécessite A2 minimum (ADR 0051). Brice est sollicité en tant que
`reviewer_role: human_release_owner` pour la décision finale ; les
critères de décisions restent techniques et l'agent demeure l'auteur
des mesures techniques.