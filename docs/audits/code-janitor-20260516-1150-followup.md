# Code Janitor Follow-up

**Date :** 2026-05-16 12:20  
**Agent :** Brice × Claude  
**Parent :** `code-janitor-20260516-1150.md`

---

## Resolved

- **JAN-01** — Factorisation des blocs Claude Code / OpenCode prompt commands en fonction shell `generate_prompt_commands()`. `setup.sh` réduit de ~84 lignes dupliquées à une fonction de 35 lignes appelée 2 fois.
- **JAN-02** — Commentaire debug `# Use rough backup` supprimé (n'existait déjà plus dans le fichier après réécriture précédente ; confirmé absent).
- **JAN-03** — Summary final modifié pour afficher les compteurs skipped : `24 generated / 0 skipped`. Section `Warnings:` ajoutée quand des fichiers custom sont skipped.
- **JAN-04** — `tests/smoke-install.sh` renforcé : `find | grep` fragiles remplacés par `find ... | wc -l` avec test numérique explicite. Fonction `assert_dir_has_files()` corrigée pour passer les arguments `find` correctement.

## Tests

- `bash tests/smoke-install.sh` → ✅ pass
- Install avec `$HOME` temporaire → ✅ 24 prompts déployés sur 4 providers
- Idempotence (2e install) → ✅ pas de doublon
- Custom file skip behavior → ✅ skipped count affiché, warning explicite
- `--force-governance` backup + replace → ✅ backups créés, remplacement effectif
- `--uninstall` cleanup → ✅ tous les artefacts prompts et governance retirés

## Not changed

- `AGENTS.md`
- `SYSTEM.md`
- Prompt source files
- Skill source files
