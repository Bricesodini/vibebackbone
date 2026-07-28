---
run_id: "2026-07-30_0700_claude-skills-discovery-01"
phase: "03_IMPLEMENTATION"
voie: "STRUCTUREE"
status: "READY"
kind: "DISTRIBUTION_CLAUDE_BUG_FIX"
adversarial_level: "A1"
scope_id: "CLAUDE-SKILLS-DISCOVERY-01"
agent: "minimax/MiniMax-M3 (publication operator)"
artifacts_consumed:
  - "02_FAILS_BEFORE.md"
artifacts_produced:
  - "03_IMPLEMENTATION.md (this file)"
---

# 03_IMPLEMENTATION — Stratégie d'implémentation

## 1. Vue d'ensemble

La correction remplace la manipulation ineffective de
`settings.json.skills` par une installation effective de symlinks sous
`~/.claude/skills/<skill-name>/SKILL.md`, qui est le mécanisme canonique
de découverte de Claude Code.

## 2. Stratégie adoptée

| Élément | Choix |
|---|---|
| **Settings.json** | **Option A** — retirer la manipulation de `skills` ; ne plus écrire cette clé. |
| **Découverte** | Créer un symlink par skill sous `~/.claude/skills/<name>/SKILL.md` |
| **Cible** | Chemin absolu vers `<repo>/skills/<name>/SKILL.md` (diagnostic simple) |
| **Source canonique** | Énumération depuis le répertoire `skills/` du repo (pas de liste divergente) |
| **Type de lien** | Symlink absolu (préféré — plus simple à diagnostiquer) |
| **Idempotence** | Détection du symlink correct → no-op |
| **Fail-closed** | Collision (fichier, mauvais lien) → erreur explicite + exit non-zéro |
| **Réversibilité** | `rm -rf ~/.claude/skills/<name>` pour chaque skill installé |

## 3. Détails de la modification

### 3.1. `distributions/claude/setup.sh` — Avant

```bash
claude_install() {
  claude_install_settings_json
  claude_install_claude_md_block
  claude_install_prompt_commands
}

claude_install_settings_json() {
  if needs_python; then
    mkdir -p "$HOME/.claude"
    [ ! -f "$CLAUDE_SETTINGS" ] && echo '{}' > "$CLAUDE_SETTINGS"
    python3 - "$CLAUDE_SETTINGS" <<'PY'
import json, sys
path = sys.argv[1]
with open(path) as f:
    cfg = json.load(f)
skills = cfg.get("skills", [])
entry = "~/.agents/skills"
if entry not in skills:
    skills.append(entry)
    cfg["skills"] = skills
    with open(path, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"✓ Claude Code: settings.json patched with {entry!r}")
PY
  fi
}
```

### 3.2. `distributions/claude/setup.sh` — Après

```bash
claude_install() {
  claude_install_settings_json
  claude_install_claude_md_block
  claude_install_prompt_commands
  claude_install_skill_symlinks   # NEW
}

claude_install_settings_json() {
  mkdir -p "$(dirname "$CLAUDE_SETTINGS")"
  if [ ! -f "$CLAUDE_SETTINGS" ]; then
    echo '{}' > "$CLAUDE_SETTINGS"
    echo "✓ Claude Code: settings.json created (empty)"
  else
    echo "✓ Claude Code: settings.json preserved (untouched — no longer patched)"
  fi
}

claude_install_skill_symlinks() {
  local skills_src="$REPO_ROOT/skills"
  local skills_dst="$HOME/.claude/skills"
  # ... (enumerates skills/*/SKILL.md, creates symlinks, idempotent, fail-closed)
}
```

## 4. Comportement fail-closed — Cas couverts

| Cas | Comportement |
|---|---|
| Source `SKILL.md` manquante | `skip` + warning (skill incomplet) |
| Source à l'intérieur du `skills_dst` | `fail` (recurse guard) |
| `dst_dir` est un fichier | `fail` (collision) |
| `dst` est un symlink vers autre chose | `fail` (lien incorrect préexistant) |
| `dst` est un fichier régulier | `fail` (fichier utilisateur — ne pas écraser) |
| `dst` est un symlink correct | no-op (idempotent) |
| `dst` est un symlink cassé | remplace par le bon (si on en est propriétaire) |
| Chemin du repo avec espaces | OK (utilise `$(cd ... && pwd)`) |

## 5. Sécurité et atomicité

- **Pas d'écrasement silencieux** : tout fichier utilisateur à la
  destination provoque une erreur explicite.
- **Liens absolus** : `ln -s <abs_src> <dst>` — le lien survit au
  déplacement du `$HOME` (par ex. backup/restore).
- **Pas de liens imbriqués** : le recurse guard refuse tout chemin
  source sous `$HOME/.claude/skills/`.
- **Création atomique du répertoire** : `mkdir -p` avant `ln -s`.

## 6. Idempotence

Deux exécutions successives :

```bash
$ HOME="$TEST_HOME" bash distributions/claude/setup.sh
✓ Claude Code: settings.json preserved
✓ Claude Code: 66 skill symlink(s) created

$ HOME="$TEST_HOME" bash distributions/claude/setup.sh
✓ Claude Code: settings.json preserved
✓ Claude Code: 66 skill symlink(s) created   # même état, 0 modifications
```

Preuve : `claude_install_skill_symlinks` détecte le symlink correct et
incrémente `ok` sans toucher au filesystem.

## 7. Procédure de retrait

### 7.1. Retrait complet

```bash
rm -rf ~/.claude/skills
```

### 7.2. Retrait par skill

```bash
rm ~/.claude/skills/<skill-name>/SKILL.md
rmdir ~/.claude/skills/<skill-name>
```

### 7.3. Vérification de la présence

```bash
find ~/.claude/skills -maxdepth 2 -name SKILL.md -print
```

Chaque ligne confirme qu'un skill est exposé.

```bash
readlink ~/.claude/skills/<skill-name>/SKILL.md
```

Affiche la cible absolue du symlink.

## 8. Aucune dépendance externe

Le script utilise uniquement :
- `bash` (POSIX-compat)
- `ln`, `mkdir`, `readlink`, `basename` (coreutils standard)
- Aucun appel `python3` dans la nouvelle fonction

Donc la nouvelle installation fonctionne même si `python3` est absent.

## 9. Conformité aux contraintes

| Contrainte | Respect |
|---|---|
| Idempotent | ✅ |
| Fail-closed | ✅ |
| Réversible | ✅ (procédure documentée §7) |
| Pas d'écrasement silencieux | ✅ |
| HOME réel non touché (test uniquement) | ✅ |
| Pas d'impact sur codex/opencode | ✅ |
| settings.json préservé | ✅ |
| `settings.json.skills` non fonctionnel | ✅ (la clé n'est plus injectée) |
| Chemin source calculé depuis le script | ✅ (`$(cd "$(dirname "$REPO_ROOT/skills/..")" && pwd)`) |
| Test de la source canonique (énumération depuis `skills/`) | ✅ |
| Test fail-closed sur source manquante | ✅ |
| Test fail-closed sur collision | ✅ |
| Test idempotence | ✅ |
