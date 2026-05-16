---
name: t-vbb-git-sync
description: |
  Executes the full git sync lifecycle as a subagent: state check, targeted
  staging, conventional commit, push to remote, merge back to main, and
  branch cleanup. Designed for local Qwen execution — procedural, bash-first,
  zero creative judgment. Requires commit message from commit-ready.
  Keywords: git sync, git commit, git push, git merge, main merge,
  commit execution, branch cleanup, subagent, procedural, bash.
version: "1.1"
phase: transverse
token_budget: low
subagent_eligible: true
mode_sensitive: false
---

# Git Sync — Procédure d'Exécution Bash

Référence standard : `0-vbb-standard`

## ROLE & POSTURE

Tu exécutes une procédure git séquentielle. Tu neraisonnes pas créativement.
Tu suis les étapes. Tu vérifies chaque output. Tu refuses si les conditions
ne sont pas réunies.

Règles absolues :

1. **JAMAIS** `git push --force`
2. **JAMAIS** `git add -A` ou `git add .`
3. **JAMAIS** merger si `git merge --ff-only` échoue (sauf confirmation)
4. **TOUJOURS** vérifier l'output de chaque commande avant de continuer
5. **DRY-RUN par défaut** — utiliser `--execute` pour exécuter réellement

## INPUT CONTRACT

**Requis :**

- [ ] Un message de commit conventionnel (fourni par l'agent cloud via commit-ready)
- [ ] La liste des fichiers à committer (ou "all-tracked-changes")

**Optionnels :**

- [ ] Branche de merge cible (défaut : main)
- [ ] Remote name (défaut : origin)
- [ ] Flag `--execute` (sinon = dry-run)

## PROCESS — Procédure exacte

Exécuter les étapes dans l'ordre. Après chaque étape, vérifier le résultat
avant de continuer. Si une vérification échoue, STOP et rapporter.

### Étape 1 — Contexte initial

```bash
git rev-parse --abbrev-ref HEAD          # branche courante
git status --porcelain                   # fichiers modifiés
git remote -v                            # remote configuré
git log -1 --oneline                     # dernier commit
```

Stocke le nom de la branche courante dans `CURRENT_BRANCH`.

Si `CURRENT_BRANCH` == "main" :
- Afficher WARN : "Commit direct sur main détecté."
- Proposer de créer une branche : `git checkout -b work/{descriptive-name}`
- Attendre confirmation.

### Étape 2 — Staging

SI fichiers spécifiés dans l'input :
```bash
git add fichier1 fichier2 fichier3 ...
```

SINON (all-tracked-changes) :
```bash
git add -u    # stage seulement les fichiers déjà trackés modifiés
```

Vérification :
```bash
git diff --cached --name-only   # liste des fichiers stagés
```

Comparer avec les fichiers attendus. Si différence → WARN.

### Étape 3 — Commit

```bash
git commit -m "{MESSAGE FOURNI}"
```

Vérification :
```bash
git log -1 --oneline    # doit montrer le nouveau commit
```

Si le commit échoue → STOP. Rapporter l'erreur git.

### Étape 4 — Push

SI remote configuré (étape 1) :
```bash
git push -u origin {CURRENT_BRANCH}
```

Vérification :
- Si "rejected" dans l'output → STOP. "Remote en avance. git pull --rebase requis."
- Si "error" dans l'output → STOP. Rapporter l'erreur.

SINON :
- WARN : "Pas de remote. Commit local uniquement."

### Étape 5 — Merge vers main

SI `CURRENT_BRANCH` != "main" :

```bash
# checkout main
git checkout main
git pull --ff-only origin main    # synchroniser main
git merge --ff-only {CURRENT_BRANCH}
```

Vérifications après merge :
- Si "Already up to date" → déjà mergé, OK.
- Si "Fast-forward" → merge réussi, OK.
- SI "CONFLICT" → EXECUTER IMMÉDIATEMENT :
  ```bash
  git merge --abort
  ```
  puis STOP. "Conflits détectés. Merge annulé. Résolution manuelle requise."
- Si "fatal: Not possible to fast-forward" → demander confirmation pour :
  ```bash
  git merge --no-ff {CURRENT_BRANCH}
  ```
  Si confirmation refusée → STOP.

### Étape 6 — Push main

SI remote configuré :
```bash
git push origin main
```

Vérification : même logique qu'étape 4.

### Étape 7 — Nettoyage (optionnel)

Demander confirmation :
```bash
git branch -d {CURRENT_BRANCH}              # supprimer branche locale
git push origin --delete {CURRENT_BRANCH}   # supprimer branche remote
```

### Étape 8 — Rapport final

Afficher :

```
════════════════════════════════════════════════════════════════
  GIT SYNC : RÉSULTAT
════════════════════════════════════════════════════════════════
  Branche initiale : {CURRENT_BRANCH}
  Commit SHA        : {SHA}
  Push vers remote  : {OK/FAIL/SKIP}
  Merge vers main   : {OK/FAIL/CONFLICT/SKIP}
  Push main         : {OK/FAIL/SKIP}
  Branche nettoyée  : {oui/non}
  Branche courante  : main
════════════════════════════════════════════════════════════════
```

Écrire dans `docs/audits/git-sync-{YYYYMMDD-HHMM}.md` si le répertoire existe.

## BLOCKING CONDITIONS

- Aucun changement local → STOP.
- HEAD détaché → STOP.
- Conflits de merge → ABORT merge + STOP.
- `docs/PROJECT_MODE.md` = frozen → STOP.

## OUTPUT CONTRACT

Résultat des opérations git (exécutées ou dry-run).

Rapport dans `docs/audits/git-sync-{YYYYMMDD-HHMM}.md` si le répertoire existe.

## VERDICT RULES

- `READY` — cycle complet exécuté avec succès
- `PARTIAL` — commit OK mais push/merge échoué ou skip
- `BLOCKED` — préconditions non réunies ou conflits
- `UNKNOWN` — état du repo impossible à déterminer

## SUPPORT BOUNDARY

Supporté :
- Repos Git avec un seul remote (origin)
- Merge fast-forward vers main
- Conventional commits
- DRY-RUN + --execute

Non supporté (refuser) :
- Force push → interdit
- Rebase interactif → manuel
- Résolution auto de conflits → manuel
- Multi-remote → manuel
- Submodules modifiés → manuel