# 03_AUDIT_FINDINGS — RUN 04A · Lot 1C : Audit sécurité vibebackbone

**Date** : 2026-06-10  
**Voie** : AUDIT  
**Skill** : `2-vbb-security`

---

## SEC-001 — os.popen() pour horodatage de backup

| Champ | Valeur |
|-------|--------|
| **ID** | SEC-001 |
| **Sévérité** | P2 |
| **Zone** | setup.sh (Codex backup block) |
| **Fichier** | `setup.sh` ligne 484 |
| **Constat** | `os.popen('date +%Y%m%d-%H%M%S').read().strip()` utilisé pour générer le nom de fichier de backup. `os.popen` exécute une commande shell héritée de l'environnement PATH de l'utilisateur. Si un attaquant contrôle le PATH ou l'exécutable `date`, il peut exécuter du code arbitraire. |
| **Impact** | Exécution de code arbitbre lors de `setup.sh --force-governance` |
| **Preuve** | `backup_path = f"{path}.backup.{os.popen('date +%Y%m%d-%H%M%S').read().strip()}"` |
| **Recommandation** | Remplacer par `datetime.datetime.now().strftime('%Y%m%d-%H%M%S')` — pas de subprocess, pas de shell |
| **Statut** | OPEN |

---

## SEC-002 — eval() pour variable dynamique dans generate_prompt_commands

| Champ | Valeur |
|-------|--------|
| **ID** | SEC-002 |
| **Sévérité** | P3 |
| **Zone** | setup.sh (generate_prompt_commands) |
| **Fichier** | `setup.sh` lignes 157-158 |
| **Constat** | `eval "$ok_var=\$ok"` et `eval "$skip_var=\$skip"` utilisé pour retourner des valeurs depuis la fonction. Si `ok_var` ou `skip_var` contient des caractères spéciaux, cela permet l'injection de commandes. Les valeurs sont fixées par l'appelant (noms de variables codés en dur), donc le risque est faible mais la pattern est dangereuse. |
| **Impact** | Injection de commandes théorique si les noms de variables sont contrôlés par un attaquant |
| **Preuve** | `eval "$ok_var=\$ok"` — lignes 157-158 |
| **Recommandation** | Remplacer par des retours via stdout ou des tableaux associatifs bash |
| **Statut** | OPEN |

---

## SEC-003 — Symlinks absolus — dangling après déplacement du repo

| Champ | Valeur |
|-------|--------|
| **ID** | SEC-003 |
| **Sévérité** | P2 |
| **Zone** | setup.sh (skills + prompts symlinks) |
| **Fichier** | `setup.sh` ligne 332 |
| **Constat** | `ln -s "$SKILLS_SRC" "$LINK_NAME"` crée un symlink absolu vers `$REPO_ROOT/skills`. Si le repo est déplacé (git clone ailleurs, mv), le symlink devient dangling. Un attaquant pourrait placer un repo malveillant à l'ancien chemin pour que les agents LLM chargent des skills compromis. |
| **Impact** | Skills compromis si le chemin d'origine est recréé par un attaquant |
| **Preuve** | `REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"` → path absolu → `ln -s "$SKILLS_SRC" "$LINK_NAME"` |
| **Recommandation** | Utiliser des symlinks relatifs ou ajouter une vérification d'intégrité (checksum ou vérification du contenu de SKILL.md) au démarrage |
| **Statut** | OPEN |

---

## SEC-004 — TOCTOU race condition sur création de symlinks

| Champ | Valeur |
|-------|--------|
| **ID** | SEC-004 |
| **Sévérité** | P3 |
| **Zone** | setup.sh (skills symlink) |
| **Fichier** | `setup.sh` lignes 330-332 |
| **Constat** | `[ -L "$LINK_NAME" ] && rm "$LINK_NAME"` suivi de `ln -s "$SKILLS_SRC" "$LINK_NAME"`. Entre le rm et le ln -s, une autre processus pourrait créer un fichier ou symlink malveillant à l'emplacement. |
| **Impact** | Symlink malveillant créé dans ~/.agents/skills/vibebackbone pendant la fenêtre |
| **Preuve** | Pattern check-then-act classique |
| **Recommandation** | Utiliser `ln -sf` (force) au lieu du pattern rm + ln séparé |
| **Statut** | OPEN |

---

## SEC-005 — PyYAML non épinglé — risque supply chain

| Champ | Valeur |
|-------|--------|
| **ID** | SEC-005 |
| **Sévérité** | P2 |
| **Zone** | requirements.txt + tools Python |
| **Fichier** | `requirements.txt` |
| **Constat** | `pyyaml` sans version épinglée. Une mise à jour malveillante ou cassée de PyYAML sur PyPI pourrait introduire du code malveillant. PyYAML a déjà eu des vulnérabilités (CVE-2020-14343, arbitrary code execution via yaml.load). Les outils utilisent `yaml.safe_load` mais un update malveillant pourrait remplacer safe_load. |
| **Impact** | Exécution de code arbitraire via une dépendance compromise |
| **Preuve** | `requirements.txt` contient uniquement `pyyaml` (sans version) |
| **Recommandation** | Épingler la version : `pyyaml>=6.0,<7.0` ou `pyyaml==6.0.2` |
| **Statut** | OPEN |

---

## SEC-006 — exec_module pour chargement dynamique du phase-router

| Champ | Valeur |
|-------|--------|
| **ID** | SEC-006 |
| **Sévérité** | P3 |
| **Zone** | tools/vbb-contract-runtime.py |
| **Fichier** | `tools/vbb-contract-runtime.py` ligne 405 |
| **Constat** | `router_spec.loader.exec_module(router_module)` charge dynamiquement `vbb-phase-router.py`. Si le fichier est compromis (par un attaquant avec accès en écriture au repo), cela permet l'exécution de code arbitraire. |
| **Impact** | Exécution de code arbitraire si tools/ est compromis |
| **Preuve** | `import importlib.util` + `spec_from_file_location` + `exec_module` |
| **Recommandation** | Acceptable en mode DISTRIBUTION (pas de surface réseau). Ajouter un commentaire dans le code documentant le risque. Évaluer l'intégrité si le repo est cloné depuis une source non fiable. |
| **Statut** | ACCEPTED_RISK |

---

## SEC-007 — setup.sh modifie des fichiers hors du repo dans $HOME

| Champ | Valeur |
|-------|--------|
| **ID** | SEC-007 |
| **Sévérité** | P2 |
| **Zone** | setup.sh |
| **Fichier** | `setup.sh` (multiple) |
| **Constat** | Le script écrit dans `~/.claude/`, `~/.codex/`, `~/.pi/`, `~/.config/opencode/`, `~/.agents/`. Ces chemins sont dans `$HOME` de l'utilisateur et ne sont pas sandboxés. Le script devrait être exécuté dans un environnement de confiance. Cependant, le script ne télécharge rien depuis internet et ne fait pas de network I/O. |
| **Impact** | Modification non sandboxée de la configuration des agents LLM de l'utilisateur |
| **Preuve** | `mkdir -p "$HOME/.claude"`, `touch "$CLAUDE_MD"`, `echo '{}' > "$CLAUDE_SETTINGS"` |
| **Recommandation** | Documenter clairement que setup.sh nécessite une confiance élevée. Ajouter un avertissement en début de script. |
| **Statut** | OPEN |

---

## SEC-008 — Pas de vérification d'intégrité des skills chargés par les agents

| Champ | Valeur |
|-------|--------|
| **ID** | SEC-008 |
| **Sévérité** | P2 |
| **Zone** | Architecture globale (agents LLM + skills/) |
| **Fichier** | N/A (conception) |
| **Constat** | Les agents LLM chargent les SKILL.md fichiers depuis le filesystem sans vérification d'intégrité (hash, signature). Si un attaquant modifie un SKILL.md (par commit malveillant, PR non vérifiée, ou accès filesystem), l'agent LLM exécutera les instructions compromises. |
| **Impact** | Instructions compromisées injectées dans le contexte LLM — risque de prompt injection, manipulation du comportement de l'agent |
| **Preuve** | Aucun hash, signature ou vérification d'intégrité n'existe dans le pipeline de chargement des skills |
| **Recommandation** | 1. Ajouter des checksums pour les skills critiques. 2. Valider les PR avec revue humaine avant merge. 3. Documenter que les skills sont du code exécutable par LLM. |
| **Statut** | ACCEPTED_RISK |

---

## SEC-009 — GitHub Actions : pas de permissions minimales

| Champ | Valeur |
|-------|--------|
| **ID** | SEC-009 |
| **Sévérité** | P2 |
| **Zone** | .github/workflows/ |
| **Fichier** | `.github/workflows/vbb-contracts.yml`, `.github/workflows/smoke.yml` |
| **Constat** | Les workflows GitHub Actions n'ont pas de `permissions` block explicite. Par défaut, GitHub accorde `write` sur les contents, packages, etc. Si un workflow est compromis, il peut pousser du code au repo. |
| **Impact** | Un workflow compromis peut modifier le repo ou exfiltrer des secrets |
| **Preuve** | Aucun `permissions:` dans les workflows |
| **Recommandation** | Ajouter `permissions: contents: read` au niveau du workflow |
| **Statut** | OPEN |

---

## SEC-010 — Pas de secret exposé — verification

| Champ | Valeur |
|-------|--------|
| **ID** | SEC-010 |
| **Sévérité** | N/A |
| **Zone** | Global |
| **Fichier** | N/A |
| **Constat** | Aucun secret, clé API, token ou credential n'a été trouvé dans le repo. Les fichiers .env, .key, .pem sont absents. .gitignore exclut correctement SESSION.md et les fichiers locaux. |
| **Impact** | Aucun |
| **Preuve** | `find . -name ".env*" -o -name "*.secret" -o -name "*.key" -o -name "*.pem"` → 0 résultats |
| **Recommandation** | Maintenir la vigilance — aucun changement nécessaire |
| **Statut** | FALSE_POSITIVE (pas de finding, confirmation positive) |

---

## Résumé des findings

| ID | Sévérité | Statut | Résumé court |
|----|----------|--------|-------------|
| SEC-001 | P2 | OPEN | `os.popen()` pour horodatage backup |
| SEC-002 | P3 | OPEN | `eval()` pour variable dynamique |
| SEC-003 | P2 | OPEN | Symlinks absolus → dangling si repo déplacé |
| SEC-004 | P3 | OPEN | TOCTOU race condition sur symlinks |
| SEC-005 | P2 | OPEN | PyYAML non épinglé (supply chain) |
| SEC-006 | P3 | ACCEPTED_RISK | exec_module pour phase-router |
| SEC-007 | P2 | OPEN | setup.sh écrit dans $HOME sans sandbox |
| SEC-008 | P2 | ACCEPTED_RISK | Pas de vérification d'intégrité des skills |
| SEC-009 | P2 | OPEN | GitHub Actions sans permissions minimales |
| SEC-010 | N/A | FALSE_POSITIVE | Pas de secret exposé (confirmation) |

**Distribution par sévérité** :
- P0 : 0
- P1 : 0
- P2 : 5 (SEC-001, SEC-003, SEC-005, SEC-007, SEC-009)
- P3 : 3 (SEC-002, SEC-004, SEC-006)
- FALSE_POSITIVE : 1 (SEC-010)

**Aucun P0 ou P1 identifié.** La posture sécurité est acceptable pour un mode DISTRIBUTION mais nécessite des remédiations ciblées.