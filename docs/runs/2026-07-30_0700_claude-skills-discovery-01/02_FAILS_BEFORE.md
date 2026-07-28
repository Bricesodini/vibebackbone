---
run_id: "2026-07-30_0700_claude-skills-discovery-01"
phase: "02_FAILS_BEFORE"
voie: "STRUCTUREE"
status: "READY"
kind: "DISTRIBUTION_CLAUDE_BUG_FIX"
adversarial_level: "A1"
scope_id: "CLAUDE-SKILLS-DISCOVERY-01"
agent: "minimax/MiniMax-M3 (publication operator)"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "02_FAILS_BEFORE.md (this file)"
---

# 02_FAILS_BEFORE — Reproduction du bug

## Résumé exécutif

**Bug confirmé** : la distribution Claude actuelle n'expose aucun
skill sous `~/.claude/skills/<skill-name>/SKILL.md`. Les skills
canoniques de Vibe Backbone ne sont donc **pas découvrables** par
Claude Code. La clé `settings.json.skills` que le setup injecte n'est
**pas consommée** par Claude Code comme mécanisme de découverte.

## 1. Reproduction

### 1.1. Scénario

```bash
TEST_HOME="$(mktemp -d)"
HOME="$TEST_HOME" \
REPO_ROOT="$(pwd)" \
AGENTS_SRC="$(pwd)/AGENTS.md" \
SYSTEM_SRC="$(pwd)/SYSTEM.md" \
PROMPTS_SRC="$(pwd)/prompts" \
CLAUDE_SETTINGS="$TEST_HOME/.claude/settings.json" \
CLAUDE_MD="$TEST_HOME/.claude/CLAUDE.md" \
CLAUDE_COMMANDS="$TEST_HOME/.claude/commands" \
FORCE_GOVERNANCE="false" \
SYSTEM_AVAILABLE="true" \
PROMPTS_AVAILABLE="true" \
bash -c '
  source "$(pwd)/setup-lib.sh"
  source "$(pwd)/distributions/claude/setup.sh"
  claude_install
'
```

### 1.2. Sortie observée

```
✓ Claude Code: settings.json patched with '~/.agents/skills'
Deploying governance (AGENTS.md + SYSTEM.md)...
✓ Claude Code: AGENTS.md + SYSTEM.md reference added
```

### 1.3. État du filesystem après install

```
$TEST_HOME/.claude/
├── CLAUDE.md            # présent (governance block)
└── settings.json        # présent (skills key, non fonctionnel)
```

**Aucun répertoire `~/.claude/skills/` n'est créé.**
**Aucun symlink `<skill-name>/SKILL.md` n'est créé.**

### 1.4. Contenu de `~/.claude/settings.json`

```json
{
  "skills": [
    "~/.agents/skills"
  ]
}
```

Cette clé `skills` est un vestige historique :
- Issue tracker : anthropics/claude-code#31005 (workaround non implémenté)
- Claude Code **ne consomme pas** cette clé pour découvrir les skills
- Mécanisme réel : `~/.claude/skills/<skill-name>/SKILL.md`

## 2. Preuves que le bug est réel

### 2.1. Documentation officielle Claude Code

Le mécanisme de découverte canonique est :

```
~/.claude/skills/<skill-name>/SKILL.md
```

où `<skill-name>/SKILL.md` est le fichier Markdown qui décrit le
skill. Claude Code scanne ce répertoire au démarrage de session.

### 2.2. Inspection du code source

```bash
$ grep -n "skill" distributions/claude/setup.sh
29:# 1. Claude Code — settings.json — patch with ~/.agents/skills path
39:skills = cfg.get("skills", [])
40:entry = "~/.agents/skills"
41:if entry not in skills:
42:    skills.append(entry)
43:    cfg["skills"] = skills
```

Le seul traitement des "skills" est l'écriture de la clé JSON
`settings.json.skills`. **Aucun appel à `mkdir ~/.claude/skills`**,
**aucune création de symlink vers `skills/<name>/SKILL.md`**.

### 2.3. État attendu vs état réel

| Attendu (Claude Code discovery) | Réel (actuel) |
|---|---|
| `~/.claude/skills/0-vbb-guide/SKILL.md` | ABSENT |
| `~/.claude/skills/2-vbb-security/SKILL.md` | ABSENT |
| `~/.claude/skills/vibebackbone/SKILL.md` | ABSENT |
| ... (66 skills au total) | TOUS ABSENTS |

**Conclusion** : aucun skill Vibe Backbone n'est découvrable.

## 3. Implications

1. **Aucun skill ne fonctionne** dans Claude Code avec ce setup.
2. La gouvernance v1.1 adversariale, les skills de phase 1-2, les
   skills transverses (t-vbb-*) sont **invisibles** à Claude Code.
3. L'utilisateur doit installer manuellement les skills en copiant
   les fichiers, contournant complètement le setup officiel.
4. La documentation `distributions/claude/README.md` ne mentionne
   pas la découverte de skills, ce qui crée une fausse impression
   que l'installation est complète.

## 4. Cible après correction

Pour chaque skill canonique du dépôt (66 skills) :

```
~/.claude/skills/0-vbb-guide/SKILL.md
  -> <repo>/skills/0-vbb-guide/SKILL.md

~/.claude/skills/2-vbb-security/SKILL.md
  -> <repo>/skills/2-vbb-security/SKILL.md

... (66 symlinks au total)
```

Avec :
- liens symboliques absolus (plus simples à diagnostiquer)
- idempotent (2 exécutions → même état)
- fail-closed sur collision mal gérée
- aucun impact sur les fichiers utilisateur existants
- retrait manuel documenté
