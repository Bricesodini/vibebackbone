# TROUBLESHOOTING — vibebackbone

Common issues & resolutions.

## "Skills not discovered by my agent"
→ Vérifier que `setup.sh` a été exécuté : `ls ~/.agents/skills/vibebackbone/`
→ Vérifier le symlink : `ls -la ~/.agents/skills/vibebackbone`
→ Relancer : `bash ~/vibebackbone/setup.sh`

## "Skills outdated après un git pull"
→ Le symlink suit automatiquement — aucune action requise
→ Si doute : `ls -la ~/.agents/skills/vibebackbone` → pointe vers `~/vibebackbone/skills/`

## "Which skill should I use?"
→ Consulter [README.md](../README.md) tableau des 57 skills
→ Ou [AGENTS.md](../AGENTS.md) § 3 (triage opérationnel)

## "Skill says BLOCKING CONDITION"
→ Lire la section BLOCKING CONDITIONS du SKILL.md
→ Adresser le blocage (généralement : audit précédent manquant, ou scope non congelé)
→ Relancer le skill

## "Audit findings don't make sense"
→ Relire la section SCOPE du skill
→ Consulter [PILOTAGE.md](../skills/vibebackbone/docs/PILOTAGE.md) pour le contexte opérationnel
→ Ouvrir une issue GitHub avec la question

## "ModuleNotFoundError: No module named 'yaml'"
→ Les outils Python de contrat et de clôture utilisent PyYAML pour lire les frontmatters et contrats.
→ Installer les dépendances Python du dépôt : `python3 -m pip install -r requirements.txt`
→ Relancer la commande, par exemple : `python3 tools/vbb-loop-closure-check.py <run_id>`

Si l'installation locale est impossible, noter explicitement la validation comme non réalisée dans le `07_CLOSEOUT.md` concerné avec cette erreur.

## "How do I extend vibebackbone?"
→ Lire [CONTRIBUTING.md](../CONTRIBUTING.md)
→ Créer un nouveau skill : `skills/[phase]-vbb-[name]/SKILL.md`
→ Suivre la structure de [0-vbb-guide](../skills/0-vbb-guide/SKILL.md)
→ Ouvrir une PR avec les guidelines de CONTRIBUTING.md

## "Project has multiple teams, how do we coordinate?"
→ Chaque agent utilise les mêmes skills depuis `~/.agents/skills/vibebackbone/`
→ La coordination se fait via les livrables des skills (rapports, risk-register)
→ Pas de configuration partagée nécessaire — les skills sont stateless

## "Can we add phases beyond [0-4]?"
→ Non recommandé pour l'instant (vibebackbone est stable à [0-4] + [t])
→ Ouvrir une GitHub Discussion pour en débattre

## "How often should we audit?"
→ Recommandé : audit complet [0→3] annuellement
→ Ou : audits légers [1] trimestriellement
→ Ad-hoc : [2] security sur incident

---

**Last updated** : 2026-05-16
