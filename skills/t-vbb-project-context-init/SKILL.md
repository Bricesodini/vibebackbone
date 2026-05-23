---
name: t-vbb-project-context-init
description: |
  Bootstraps vibebackbone governance in a target project that has none.
  Creates docs/{PROJECT_MODE,CONTEXT,AUDIT_STATUS,INDEX}.md, docs/runs/,
  docs/audits/, docs/adr/, docs/templates/ (7 phase templates) and updates
  .gitignore. Idempotent — skips files that already exist unless --overwrite.
version: "1.0"
phase: transverse
token_budget: low
subagent_eligible: true
mode_sensitive: false
---

# Project Context Init

Référence standard : `0-vbb-standard`

## ROLE & POSTURE

Tu es un bootstrapper de gouvernance vibebackbone.

Ton rôle est de préparer un projet existant pour fonctionner sous VBB :
créer les fichiers de gouvernance manquants, configurer `.gitignore`,
copier les templates de phase.

Tu ne modifies PAS le code du projet.
Tu ne supprimes PAS de fichiers existants.
Tu ne forces PAS la réécriture sans confirmation explicite.

Règles absolues :

- Idempotent : skip si le fichier existe déjà (sauf `--overwrite` explicite).
- Non destructeur : si `.git/hooks/pre-commit` existe, ne pas écraser sans `--overwrite`.
- Evidence required : signaler clairement les fichiers créés, skippés, en erreur.

## INPUT CONTRACT

**Requis :**

- [ ] Accès au repo cible (répertoire courant ou chemin explicite)

**Optionnels :**

- [ ] Nom du projet (pour renseigner `docs/CONTEXT.md`)
- [ ] Mode initial (`DEV` ou `PROD`, défaut : `DEV`)
- [ ] Flag `--overwrite` pour forcer la réécriture des fichiers existants
- [ ] Flag `--dry-run` pour prévisualiser sans écriture

## BLOCKING CONDITIONS

- Si `tools/vbb-project-init.py` est introuvable → STOP.
  Message : « L'outil tools/vbb-project-init.py est absent. Vérifier l'installation VBB. »
- Si le répertoire cible n'existe pas → STOP. Demander la confirmation du chemin.
- Si le projet est déjà complètement sur VBB rails (tous les fichiers présents) →
  signaler que c'est déjà initialisé, proposer `--overwrite` pour mise à jour.

## SCOPE

### Inclus

- création de `docs/PROJECT_MODE.md`
- création de `docs/CONTEXT.md` (avec nom du projet)
- création de `docs/AUDIT_STATUS.md` (squelette)
- création de `docs/INDEX.md`
- création de `docs/runs/README.md` (copié depuis VBB)
- création de `docs/audits/README.md`
- création de `docs/adr/README.md`
- copie de `docs/templates/*.md.template` (7 templates de phase)
- mise à jour de `.gitignore` (entrées SESSION.md)
- copie optionnelle de `scripts/install-vbb-pre-commit.sh`

### Exclus

- modification du code du projet
- modification de la configuration CI/CD existante
- création d'un run d'initialisation dans le projet cible
- suppression ou remplacement de fichiers de gouvernance existants sans flag explicite

## PROCESS

1. Vérifier que `tools/vbb-project-init.py` est accessible.
2. Vérifier si le projet est déjà sur VBB rails :
   - `ls docs/PROJECT_MODE.md docs/CONTEXT.md docs/AUDIT_STATUS.md` → si tout existe → PARTIAL (mise à jour partielle possible).
3. Lancer le dry-run pour prévisualiser :
   ```bash
   python3 tools/vbb-project-init.py --target-dir <chemin> --dry-run
   ```
4. Présenter le résumé à l'utilisateur (fichiers qui seraient créés / skippés).
5. Si l'utilisateur confirme, lancer l'initialisation réelle :
   ```bash
   python3 tools/vbb-project-init.py \
     --target-dir <chemin> \
     --project-name "<Nom du projet>" \
     --mode DEV
   ```
6. Vérifier les fichiers créés et signaler les skips.
7. Guider l'utilisateur pour compléter `docs/CONTEXT.md` :
   - Description du projet
   - Stack principale
   - Mode opératoire attendu
8. Signaler que le pre-commit hook est disponible :
   ```bash
   bash scripts/install-vbb-pre-commit.sh
   ```
   (ou utiliser `--install-hook` pour le faire automatiquement)
9. Produire le `07_CLOSEOUT.md` du run d'initialisation.

## OUTPUT CONTRACT

### Artefact principal (phase artifact)

- **Chemin** : `docs/runs/{run_id}/07_CLOSEOUT.md`
- **Template** : [`docs/templates/07_CLOSEOUT.md.template`](../../docs/templates/07_CLOSEOUT.md.template)
- **Kind** : `phase_artifact`
- **Frontmatter requis** : `run_id`, `phase=07_CLOSEOUT`, `voie`, `status`, `agent`, `started_at`, `ended_at`, `artifacts_consumed`, `artifacts_produced`

### Artefacts secondaires

- **`docs/PROJECT_MODE.md`** (`kind: persistent_state_update`) — créé si absent.
- **`docs/CONTEXT.md`** (`kind: persistent_state_update`) — créé si absent.
- **`docs/AUDIT_STATUS.md`** (`kind: persistent_state_update`) — créé si absent.

### Contenu attendu de la sortie

- liste des fichiers créés
- liste des fichiers skippés (déjà existants)
- éventuelles erreurs
- prochaine étape : compléter `docs/CONTEXT.md`

## VERDICT RULES

- `PASS`
  - au moins les fichiers core créés (`PROJECT_MODE.md`, `CONTEXT.md`, `AUDIT_STATUS.md`)
  - `.gitignore` mis à jour
- `PARTIAL`
  - certains fichiers skippés (existants) mais core OK
  - templates manquants (source VBB non trouvée) mais gouvernance de base créée
- `BLOCKED`
  - outil `vbb-project-init.py` introuvable
  - répertoire cible inaccessible
  - erreurs d'écriture système
- `UNKNOWN`
  - état du projet indéterminable avant exécution
