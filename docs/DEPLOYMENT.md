# DEPLOYMENT — vibebackbone

Guide pour installer et utiliser vibebackbone.

---

## 1. Installation globale (recommandée)

vibebackbone s'installe **une seule fois** dans `~/.agents/skills/`, le répertoire universel
partagé par Pi, Claude Code, OpenCode et Codex.

```bash
# 1. Cloner vibebackbone
git clone https://github.com/bricesodini/vibebackbone ~/vibebackbone

# 2. Installer les 64 skills globalement
cd ~/vibebackbone
bash setup.sh
```

Après validation du plan d'installation, les 64 skills sont maintenant
disponibles pour tous vos agents.

**Ce que fait `setup.sh`** :
- Crée `~/.agents/skills/vibebackbone/` (symlink vers `skills/`)
- Crée `~/.agents/prompts/vibebackbone/` (symlink vers `prompts/`, 33 prompts disponibles)
- Génère 26 commandes prompt adaptateur pour Claude Code / OpenCode / Pi (les 7 prompts canoniques restent disponibles via le symlink et la prompt library)
- Les mises à jour se font via `git pull` (les symlinks suivent automatiquement)
- Affiche un plan d'installation avant toute écriture
- Propose les flags scriptables `--auto`, `--provider <name>`, `--dry-run`,
  `--force-governance`, `--no-interactive`

---

## 2. Ce que fait `setup.sh`

| Action | Fichier cible | Provider |
|--------|--------------|----------|
| Symlink `skills/` | `~/.agents/skills/vibebackbone/` | Pi, OpenCode, Codex, Claude Code |
| Symlink `prompts/` | `~/.agents/prompts/vibebackbone/` | Pi, OpenCode, Codex, Claude Code |
| Commandes prompt spécialisées | provider command dirs | Claude Code, OpenCode, Pi |
| Patch settings | `~/.claude/settings.json` | Claude Code |
| `@import` AGENTS.md | `~/.claude/CLAUDE.md` | Claude Code |
| **Compiled block** AGENTS+SYSTEM+Prompt Library | `~/.codex/AGENTS.md` (généré avec markers `<!-- VBB:START -->` / `<!-- VBB:END -->`) | Codex |
| Symlink AGENTS.md | `~/.pi/agent/AGENTS.md` | Pi |
| Symlink SYSTEM.md | `~/.pi/agent/SYSTEM.md` | Pi |
| Patch `instructions` | `~/.config/opencode/opencode.json` | OpenCode |

Modes d'installation :

| Mode | Flags | Effet |
|------|-------|-------|
| **Auto-detect** | `--auto` ou aucun drapeau | Installe le core et les providers disponibles sans sélection manuelle |
| **Selective install** | `--provider <name>` (répétable) | Installe uniquement les providers demandés en plus du core |
| **Advanced / governance** | `--force-governance` | Autorise les remplacements contrôlés des fichiers custom, avec backup |

> **Fichiers existants** : pour Claude/Pi, le script laisse les fichiers custom
> intacts et affiche la commande `ln -sf` à exécuter manuellement. Pour **Codex**,
> le bloc compilé est régénéré (avec backup automatique en `.bak` horodaté)
> et `--force-governance` permet d'écraser les blocs legacy imbriqués.

## 3. Vérifier l'installation

```bash
# Skills
ls ~/.agents/skills/vibebackbone/
# → liste des 64 skills : 0-vbb-scope-freeze, 1-vbb-conventions, 2-vbb-security, ...

# Prompts
find ~/.agents/prompts/vibebackbone -name '*.md' | wc -l
# → 33 prompts disponibles

# Governance Claude Code
grep "vibebackbone" ~/.claude/CLAUDE.md

# Governance Codex
ls -la ~/.codex/AGENTS.md

# Governance Pi
ls -la ~/.pi/agent/AGENTS.md

# Governance OpenCode
cat ~/.config/opencode/opencode.json
```

---

## 3bis. Architecture du script d'installation

`setup.sh` est un **routeur pur** (~675 LOC). Il ne contient aucune logique
provider inline : chaque couche est extraite dans un fichier dédié.

```
setup.sh (~675 LOC) — routeur
├── source setup-lib.sh          (helpers : relpath, symlink, backup, generate_prompt_commands)
├── source core/setup.sh         (pre-flight + symlinks universels)
├── source distributions/claude/setup.sh    (settings.json + CLAUDE.md block + 26 commands)
├── source distributions/codex/setup.sh     (compiled AGENTS.md block)
├── source distributions/pi/setup.sh        (symlinks AGENTS + SYSTEM + prompts)
├── source distributions/opencode/setup.sh (opencode.json patch + 26 commands)
```

| Fichier | Rôle | LOC |
|---------|------|-----|
| `setup.sh` | Routeur : `source + <couche>_install` pour chaque couche | ~675 |
| `setup-lib.sh` | Helpers transversaux (relpath, _realpath, _is_vbb_symlink, needs_python, backup_file, symlink_if_absent, generate_prompt_commands) | ~209 |
| `core/setup.sh` | Pre-flight + symlinks universels `~/.agents/skills/` et `~/.agents/prompts/` | ~116 |
| `distributions/<provider>/setup.sh` | Glue provider-spécifique | 74–118 |

**Pour ajouter une distribution** :
1. Créer `distributions/<name>/setup.sh` exposant `<name>_install`
2. Ajouter `source "$REPO_ROOT/distributions/<name>/setup.sh"` + `<name>_install`
   dans `setup.sh`
3. Documenter la décision dans `docs/DISTRIBUTIONS.md` §Decisions log
4. Si la distribution a des templates/docs : créer `distributions/<name>/README.md`

---

## 4. Utilisation par agent

### Pi

Pi découvre automatiquement `~/.agents/skills/` au démarrage — aucune configuration requise.

```bash
pi "Lance un audit de sécurité selon vibebackbone"
pi "Applique le skill conventions sur ce projet"
pi "Génère un risk-register pour ce repo"

# Ou via commande explicite
/skill:2-vbb-security
/skill:3-vbb-risk-register
```

### Claude Code

Claude Code ne lit pas `~/.agents/skills/` nativement (issue [#31005](https://github.com/anthropics/claude-code/issues/31005)).
`setup.sh` patche automatiquement `~/.claude/settings.json` pour y ajouter le chemin :

```json
{ "skills": ["~/.agents/skills"] }
```

Après `setup.sh`, les skills sont disponibles sans configuration supplémentaire.

### OpenCode

OpenCode découvre automatiquement `~/.agents/skills/` — aucune configuration requise.

### Codex

Codex découvre automatiquement `~/.agents/skills/` — aucune configuration requise.

---

## 5. Flux de travail standard

### Étape 1 — Classifier la tâche (triage)

Lire `AGENTS.md § 3` — 4 voies :

| Voie | Signaux | Action |
|------|---------|--------|
| **RAPIDE-ZERO** | Micro-tâche sûre, zéro risque, ≤ 3 fichiers | Activity Log only |
| **RAPIDE-MINIMAL** | Petite tâche non triviale | Activity Log + 05_PATCH_SUMMARY |
| **RAPIDE** | Risque faible, pas de contrats | Agir directement |
| **STRUCTURÉE** | Multi-fichiers, contrats de données | Plan → skill → PR |
| **AUDIT** | Sécurité, intégrité, production | Séquence [0→1→2→3] |
| **CLÔTURE** | Fin de session | Session handoff |

### Étape 2 — Sélectionner le skill

```bash
# Lister les skills disponibles
ls ~/.agents/skills/vibebackbone/

# Lire un skill
cat ~/.agents/skills/vibebackbone/2-vbb-security/SKILL.md
```

Ou via l'agent :

```bash
pi "Quel skill utiliser pour auditer une API REST ?"
# → recommande 2-vbb-api-auditor
```

### Étape 3 — Exécuter

```bash
pi "Exécute le skill 2-vbb-security sur ce projet"
# ou
/skill:2-vbb-security
```

Le skill génère ses livrables selon son OUTPUT CONTRACT (rapport, code, fichier, etc.).

### Étape 4 — Séquence d'audit [0→1→2→3]

Pour une session d'audit complète, respecter l'ordre :

```
[0] scope-freeze → audit-readiness
[1] dependency-mapper → conventions → tech-debt
[2] security, api-auditor, db-robustness, ops, ci
[3] risk-register  ← toujours dernier
```

Règle : ne jamais lancer [2] sans [0] + [1] `dependency-mapper`.

---

## 6. Mise à jour

```bash
cd ~/vibebackbone
git pull
# Le symlink ~/.agents/skills/vibebackbone suit automatiquement
```

Vérifier `CHANGELOG.md` pour les breaking changes entre versions majeures.

---

## 7. Désinstallation

```bash
bash ~/vibebackbone/setup.sh --uninstall
```

---

## 8. Escalade & Governance

**Escalader si** :
- Vulnérabilité de sécurité découverte
- Risque systémique identifié
- Incompatibilité avec un skill
- Besoin d'un nouveau skill

**Processus** :
1. Documenter le finding
2. Ouvrir une issue GitHub → [vibebackbone/issues](https://github.com/bricesodini/vibebackbone/issues)

---

## 9. Troubleshooting

**"Skill not found"**
→ Vérifier que `setup.sh` a été exécuté : `ls ~/.agents/skills/vibebackbone/`

**"Skill not applicable"**
→ Lire `INPUT CONTRACT` du skill — vérifier que les prérequis existent (README, ARCHITECTURE.md, etc.)

**"BLOCKING CONDITION triggered"**
→ Lire `BLOCKING CONDITIONS` — adresser le blocage (ex : lancer scope-freeze avant un audit)

**"Skill updates not visible"**
→ Vérifier que le symlink pointe bien vers le bon dossier : `ls -la ~/.agents/skills/vibebackbone`

---

## 10. Support

- **Issues** : https://github.com/bricesodini/vibebackbone/issues
- **Discussions** : https://github.com/bricesodini/vibebackbone/discussions

---

**Version** : vibebackbone v1.0.0-rc.1
**Last updated** : 2026-06-13
