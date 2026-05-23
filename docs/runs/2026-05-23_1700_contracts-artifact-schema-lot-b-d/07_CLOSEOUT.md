---
run_id: "2026-05-23_1700_contracts-artifact-schema-lot-b-d"
phase: "07_CLOSEOUT"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-code"
started_at: "2026-05-23T17:00:00Z"
ended_at: "2026-05-23T17:40:00Z"
next_phase: null
artifacts_consumed:
  - "docs/runs/2026-05-23_1600_artifact-infra-lot-a/07_CLOSEOUT.md"
  - "docs/templates/02_AUDIT.md.template"
  - "docs/templates/07_CLOSEOUT.md.template"
artifacts_produced:
  - "07_CLOSEOUT.md"
  - "skills/0-vbb-scope-freeze/CONTRACT.yaml"
  - "skills/0-vbb-audit-readiness/CONTRACT.yaml"
  - "skills/1-vbb-adr/CONTRACT.yaml"
  - "skills/t-vbb-commit-ready/CONTRACT.yaml"
  - "skills/t-vbb-impact-analyzer/CONTRACT.yaml"
  - "skills/t-vbb-mode-transition-gate/CONTRACT.yaml"
  - "skills/t-vbb-session-handoff/CONTRACT.yaml"
  - "skills/t-vbb-status-report/CONTRACT.yaml"
  - "skills/0-vbb-scope-freeze/SKILL.md"
  - "skills/0-vbb-audit-readiness/SKILL.md"
  - "skills/1-vbb-adr/SKILL.md"
  - "skills/t-vbb-commit-ready/SKILL.md"
  - "skills/t-vbb-impact-analyzer/SKILL.md"
  - "skills/t-vbb-mode-transition-gate/SKILL.md"
  - "skills/t-vbb-session-handoff/SKILL.md"
  - "skills/t-vbb-status-report/SKILL.md"
  - "tools/vbb-contract-lint.py"
---

# 07_CLOSEOUT — contracts-artifact-schema-lot-b-d

## Résultat

Le schéma `CONTRACT.yaml` v0.3 est en place. Les 8 contrats existants
déclarent maintenant l'artefact qu'ils produisent (path, template,
frontmatter, kind), avec leurs artefacts secondaires explicites. Les 8
SKILL.md correspondants ont une section `OUTPUT CONTRACT` réécrite qui
cite le même mapping. Le linter valide tout cela mécaniquement.

Pas encore de vérification d'existence à l'exécution (Lot C, PR #3) — les
contrats déclarent l'intention, le runtime ne vérifie pas encore.

## Décisions prises

### Schéma `outputs.artifact` (v0.3)

Champ obligatoire à partir de v0.3, structure suivante :

```yaml
outputs:
  artifact:
    path_pattern: "docs/runs/{run_id}/02_AUDIT.md"
    template: "docs/templates/02_AUDIT.md.template"
    must_exist_after_run: true
    kind: phase_artifact
    frontmatter_required:
      - run_id
      - phase
      - voie
      - status
      - agent
      - started_at
      - ended_at
      - next_phase
      - artifacts_consumed
      - artifacts_produced
  secondary_artifacts:
    - path_pattern: "docs/audits/<skill>-{YYYYMMDD-HHMM}.md"
      kind: audit_report
      must_exist_after_run: true
    - path_pattern: "docs/AUDIT_STATUS.md"
      kind: persistent_state_update
      must_exist_after_run: true
```

- **`artifact` peut valoir `null`** (cas explicite) pour les skills qui
  n'ont pas d'artefact propre (ex. `t-vbb-status-report` qui produit un
  rapport inline).
- **`kind`** est un ensemble fermé :
  `{phase_artifact, audit_report, ADR, persistent_state_update}`.
- **`template`**, s'il est spécifié, doit pointer vers un fichier existant
  (vérifié par le linter).
- **`frontmatter_required`** est attendu pour `kind: phase_artifact`
  (warning du linter sinon).

### Compatibilité ascendante

Versions acceptées par le linter : `0.1`, `0.2`, `0.3`. Les contrats v0.1
ou v0.2 ne sont pas tenus de déclarer `outputs.artifact` — seuls les v0.3
le sont. Migration progressive possible si jamais d'autres contrats étaient
ajoutés au catalogue avant Lot 5b (PR #5).

### Mapping primary artifact par skill

| Skill | Primary | Kind |
|-------|---------|------|
| `0-vbb-scope-freeze` | `docs/runs/{run_id}/02_AUDIT.md` | `phase_artifact` |
| `0-vbb-audit-readiness` | `docs/runs/{run_id}/02_AUDIT.md` | `phase_artifact` |
| `1-vbb-adr` | `docs/adr/{nnnn}-{slug}.md` | `ADR` |
| `t-vbb-commit-ready` | `docs/runs/{run_id}/07_CLOSEOUT.md` | `phase_artifact` |
| `t-vbb-impact-analyzer` | `docs/runs/{run_id}/02_AUDIT.md` | `phase_artifact` |
| `t-vbb-mode-transition-gate` | `docs/runs/{run_id}/02_AUDIT.md` | `phase_artifact` |
| `t-vbb-session-handoff` | `docs/runs/{run_id}/07_CLOSEOUT.md` | `phase_artifact` |
| `t-vbb-status-report` | `null` | — |

Les skills audit (`0-*`, `2-*`, `3-*` et les `t-*` audit) émettent
systématiquement un secondaire `audit_report` horodaté dans `docs/audits/`
+ un secondaire `persistent_state_update` sur `docs/AUDIT_STATUS.md`.

### Convention de chemins ADR

L'ADR conserve son chemin existant `docs/adr/{nnnn}-{slug}.md` (lowercase)
plutôt que la variante `docs/ADRs/` mentionnée dans le closeout PR #1.
Justification : aligner avec le SKILL.md et la gate existante
`output_must_contain: docs/adr/` — éviter le breaking change.

À reporter dans le closeout PR #1 si nécessaire ; ne change rien au plan
global.

## Artefacts livrés

### Contrats (8 fichiers, v0.1 → v0.3)

| # | Contrat | Primary | Secondaires |
|---|---------|---------|-------------|
| 1 | `skills/0-vbb-scope-freeze/CONTRACT.yaml` | `02_AUDIT.md` | audit_report + AUDIT_STATUS |
| 2 | `skills/0-vbb-audit-readiness/CONTRACT.yaml` | `02_AUDIT.md` | audit_report + AUDIT_STATUS |
| 3 | `skills/1-vbb-adr/CONTRACT.yaml` | ADR | DECISIONS.md |
| 4 | `skills/t-vbb-commit-ready/CONTRACT.yaml` | `07_CLOSEOUT.md` | — |
| 5 | `skills/t-vbb-impact-analyzer/CONTRACT.yaml` | `02_AUDIT.md` | audit_report + AUDIT_STATUS |
| 6 | `skills/t-vbb-mode-transition-gate/CONTRACT.yaml` | `02_AUDIT.md` | audit_report + AUDIT_STATUS |
| 7 | `skills/t-vbb-session-handoff/CONTRACT.yaml` | `07_CLOSEOUT.md` | SESSION.md (local) |
| 8 | `skills/t-vbb-status-report/CONTRACT.yaml` | `null` | — |

### SKILL.md (8 fichiers, section `OUTPUT CONTRACT` réécrite)

Pour chaque skill ci-dessus, la section `OUTPUT CONTRACT` cite désormais
explicitement : chemin, template, kind, frontmatter requis, secondaires.
Le contenu sémantique existant (sections obligatoires du rapport, cas
spéciaux) a été préservé.

### Linter (1 fichier)

`tools/vbb-contract-lint.py` étendu avec :

- `SUPPORTED_VERSIONS = {"0.1", "0.2", "0.3"}`
- `ARTIFACT_KINDS = {"phase_artifact","audit_report","ADR","persistent_state_update"}`
- `_check_artifact_mapping()` — validation structurelle d'un artefact
  (primary ou secondaire) : champs requis, types, template existant,
  frontmatter pour `phase_artifact`.
- `check_artifact()` — gating sur `version >= 0.3`, autorise `artifact: null`.
- Câblé dans `lint_all()` après `check_agents`.

## Validation

### Linter sur les 8 contrats v0.3

```
$ python3 tools/vbb-contract-lint.py
VBB Contract Linter — 0 error(s) found
  ✓ All contracts valid
```

### Tests négatifs (10 scénarios)

Vérifié manuellement que le linter détecte :

- Champ `outputs.artifact` absent en v0.3 → 1 erreur ✓
- `kind` hors ensemble fermé → 1 erreur ✓
- `template` pointant vers un fichier inexistant → 1 erreur ✓
- `phase_artifact` sans `frontmatter_required` → 1 erreur ✓
- `must_exist_after_run` non-booléen → 1 erreur ✓
- v0.1 sans `outputs.artifact` → 0 erreur (rétro-compatibilité ✓)
- `artifact: null` explicite → 0 erreur (cas autorisé ✓)
- `secondary_artifacts` non-liste → 1 erreur ✓
- Item secondaire sans `kind` ni `must_exist_after_run` → 2 erreurs ✓

### Runtime existant non régressé

```
$ python3 tools/vbb-contract-runtime.py run --all --dry-run
PASS: 1 | PARTIAL: 5 | BLOCKED/FAIL: 2
```

Identique au baseline pré-PR #2. Le runtime ignore les nouveaux champs
(comportement attendu — Lot C les exploitera en PR #3).

## Conventions retenues

- **Une seule version de schéma** active : `0.3`. Les anciennes
  (`0.1`, `0.2`) restent acceptées pour migration progressive.
- **`artifact: null` est explicite**, pas une omission. Le linter refuse
  l'absence du champ en v0.3 mais accepte `null`.
- **`kind` est un ensemble fermé** validé. Ajouter un kind futur =
  changement explicite du linter et du runtime.
- **Les `phase_artifact` ont toujours un `template`** et déclarent leur
  `frontmatter_required`. Les autres kinds (`ADR`, `audit_report`,
  `persistent_state_update`) n'en ont pas besoin (formats différents).
- **`AUDIT_STATUS.md` reçoit toujours un secondaire `persistent_state_update`**
  pour les skills audit — c'est le tableau de bord vivant.

## Points ouverts pour PR #3 (Lot C — runtime + hook)

### À livrer

- Étendre `tools/vbb-contract-runtime.py` :
  - Après chaque exécution, vérifier `outputs.artifact.must_exist_after_run`.
  - Vérifier frontmatter conforme à `frontmatter_required` (parse YAML).
  - Downgrade automatique en `PARTIAL` avec warning si artefact manquant.
- Nouveau `tools/vbb-loop-closure-check.py {run_id}` :
  - Lit `01_INTAKE.md` pour déterminer la voie.
  - Applique la matrice voie → phases minimales
    (cf. `docs/runs/README.md`).
  - Vérifie présence + frontmatter conforme de chaque artefact attendu.
  - Sortie exit 0 / 1, rapport human-readable.
- Hook commit-ready :
  - Le skill `t-vbb-commit-ready` appelle `vbb-loop-closure-check.py` sur
    le run en cours (détecté via env `VBB_RUN_ID` ou le dossier
    `docs/runs/` le plus récent).
  - Si exit ≠ 0 → status `BLOCKED`, refuser le commit.
- Script optionnel `scripts/install-vbb-pre-commit.sh` pour poser un
  `.git/hooks/pre-commit` léger qui appelle `vbb-loop-closure-check.py`
  quand un `docs/runs/{slug}/` est touché par le diff staged.

### Points de vigilance

- Le runtime actuel produit des statuts `PARTIAL`/`BLOCKED` parce que
  l'état du repo lui-même n'a pas de scope-freeze figé. Avec
  vérification d'artefact en plus, le statut va probablement basculer
  vers `INCOMPLETE` pour la plupart des contrats — comportement attendu.
- `t-vbb-status-report` a `artifact: null`. Le runtime ne doit pas
  exiger d'artefact pour ce skill — gating explicite à prévoir.
- L'`ADR` kind n'a pas de `frontmatter_required` (header Markdown). Le
  loop-closure-check doit le détecter et appliquer une vérification
  différente (présence du header `**Date**`, `**Statut**`, `**Décideur(s)**`).

### Hors scope PR #3

- Extension aux skills phase 2 (security, db-robustness, etc.) → PR #5
  / Lot 5b.
- Bootstrap projet client (`t-vbb-project-context-init`) → PR #4 / Lot E.
- Corrections de gouvernance (PILOTAGE, compteurs, etc.) → PR #6 / Lot F.

## Risques résiduels

- **R-005 nouveau (P3)** : la convention `docs/adr/` lowercase est en
  désaccord avec `docs/ADRs/` mentionné dans certains fichiers de
  gouvernance créés en PR #1. À harmoniser en PR #6.
- **R-002 (P2)** : couverture contrats inchangée — 8/58 skills. Mitigation
  toujours planifiée en PR #5.
- **Templates `<placeholder>`** : risque déjà tracé en PR #1, mitigation
  prévue en PR #3 (loop-closure-check détectera les frontmatters
  partiellement remplis).

## État pour la prochaine session

- **Branche** : `feat/artifact-loop-closure`
- **Dernier commit du run** : (à créer après ce closeout)
- **Première action concrète à reprendre** :
  1. Diff `git diff --stat` sur les 18 fichiers de PR #2.
  2. Créer le commit
     `feat(contracts): declare outputs.artifact schema v0.3 (Lot B+D)`.
  3. Démarrer PR #3 (Lot C) : étendre runtime + créer
     `vbb-loop-closure-check.py` + activer le hook commit-ready.
- **Fichiers à charger en priorité pour PR #3** :
  - `tools/vbb-contract-runtime.py` (extension de l'exécution)
  - `docs/runs/README.md` (matrice voie → phases minimales)
  - `docs/AGENTIC_RUN_PROTOCOL.md` (référence des phases)
  - Les 8 contrats v0.3 (pour valider la lecture du nouveau schéma)

## Mise à jour des artefacts agrégés

- [ ] `docs/CONTEXT.md` § Runs récents — à mettre à jour avec ce run après
      le commit (date stable).
- [ ] `docs/AUDIT_STATUS.md` — pas d'audit dans ce run ; mettre à jour
      R-005 (nouveau risque P3) lors du prochain refresh global.
- [ ] `docs/SESSION.md` — non versionné ; mise à jour locale au choix de
      l'utilisateur.
