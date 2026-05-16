# DEPLOYMENT — vibebackbone

Guide pour installer et utiliser vibebackbone.

---

## 1. Installation globale (recommandée)

vibebackbone s'installe **une seule fois** dans `~/.agents/skills/`, le répertoire universel
découvert automatiquement par Pi, Claude Code, OpenCode, Codex et tout agent compatible
[agentskills.io](https://agentskills.io).

```bash
# 1. Cloner vibebackbone
git clone https://github.com/bricesodini/vibebackbone ~/vibebackbone

# 2. Installer les 57 skills globalement
cd ~/vibebackbone
bash setup.sh
```

C'est tout. Les 57 skills sont maintenant disponibles pour tous vos agents.

**Ce que fait `setup.sh`** :
- Crée `~/.agents/skills/vibebackbone/` (symlink vers `skills/`)
- Les mises à jour se font via `git pull` (le symlink suit automatiquement)

---

## 2. Ce que fait `setup.sh`

| Action | Fichier cible | Provider |
|--------|--------------|----------|
| Symlink `skills/` | `~/.agents/skills/vibebackbone/` | Pi, OpenCode, Codex, Claude Code |
| Patch settings | `~/.claude/settings.json` | Claude Code |
| `@import` AGENTS.md | `~/.claude/CLAUDE.md` | Claude Code |
| Symlink AGENTS.md | `~/.codex/AGENTS.md` | Codex |
| Symlink AGENTS.md | `~/.pi/agent/AGENTS.md` | Pi |
| Patch `instructions` | `~/.config/opencode/opencode.json` | OpenCode |

> **Fichiers existants** : si `~/.codex/AGENTS.md` ou `~/.pi/agent/AGENTS.md` ont du contenu,
> le script les laisse intacts et affiche la commande `ln -sf` à exécuter manuellement.

## 3. Vérifier l'installation

```bash
# Skills
ls ~/.agents/skills/vibebackbone/
# → liste des 57 skills : 0-vbb-scope-freeze, 1-vbb-conventions, 2-vbb-security, ...

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

**Version** : vibebackbone v1.0.0
**Last updated** : 2026-05-16
