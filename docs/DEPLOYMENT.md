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

## 2. Vérifier l'installation

```bash
ls ~/.agents/skills/vibebackbone/
# → liste des 57 skills : 0-vbb-scope-freeze, 1-vbb-conventions, 2-vbb-security, ...
```

---

## 3. Utilisation par agent

### Pi

Pi découvre automatiquement `~/.agents/skills/` au démarrage.

```bash
pi "Lance un audit de sécurité selon vibebackbone"
pi "Applique le skill conventions sur ce projet"
pi "Génère un risk-register pour ce repo"

# Ou via commande explicite
/skill:2-vbb-security
/skill:3-vbb-risk-register
```

### Claude Code

Ajouter dans `.claude/settings.json` de votre projet :

```json
{
  "skills": ["~/.agents/skills"]
}
```

Ou globalement dans `~/.claude/settings.json`.

### OpenCode / Codex

Référencer dans la config agent :

```json
{
  "skills": ["~/.agents/skills"]
}
```

---

## 4. Flux de travail standard

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

## 5. Mise à jour

```bash
cd ~/vibebackbone
git pull
# Le symlink ~/.agents/skills/vibebackbone suit automatiquement
```

Vérifier `CHANGELOG.md` pour les breaking changes entre versions majeures.

---

## 6. Désinstallation

```bash
bash ~/vibebackbone/setup.sh --uninstall
```

---

## 7. Escalade & Governance

**Escalader si** :
- Vulnérabilité de sécurité découverte
- Risque systémique identifié
- Incompatibilité avec un skill
- Besoin d'un nouveau skill

**Processus** :
1. Documenter le finding
2. Ouvrir une issue GitHub → [vibebackbone/issues](https://github.com/bricesodini/vibebackbone/issues)

---

## 8. Troubleshooting

**"Skill not found"**
→ Vérifier que `setup.sh` a été exécuté : `ls ~/.agents/skills/vibebackbone/`

**"Skill not applicable"**
→ Lire `INPUT CONTRACT` du skill — vérifier que les prérequis existent (README, ARCHITECTURE.md, etc.)

**"BLOCKING CONDITION triggered"**
→ Lire `BLOCKING CONDITIONS` — adresser le blocage (ex : lancer scope-freeze avant un audit)

**"Skill updates not visible"**
→ Vérifier que le symlink pointe bien vers le bon dossier : `ls -la ~/.agents/skills/vibebackbone`

---

## 9. Support

- **Issues** : https://github.com/bricesodini/vibebackbone/issues
- **Discussions** : https://github.com/bricesodini/vibebackbone/discussions

---

**Version** : vibebackbone v1.0.0
**Last updated** : 2026-05-16
