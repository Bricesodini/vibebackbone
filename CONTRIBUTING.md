# Contribution Guide

Merci d'envisager de contribuer à vibebackbone ! Ce document décrit les directives de contribution et les meilleures pratiques.

## Code of Conduct

En contribuant à vibebackbone, vous acceptez notre [Code de Conduite](CODE_OF_CONDUCT.md).

## Comment contribuer

### Signaler des bugs

Les bugs sont documentés via des **GitHub Issues**. Avant de signaler un bug, vérifiez que :

1. Le bug n'est pas déjà signalé dans les issues existantes
2. Vous pouvez reproduire le bug de manière cohérente
3. Vous avez testé avec la version la plus récente de vibebackbone

**Détails à inclure dans le rapport :**
- Version de vibebackbone
- Système d'exploitation et version
- Étapes précises pour reproduire le problème
- Comportement attendu vs. réel observé
- Logs ou transcripts si disponibles

### Proposer des fonctionnalités

Les demandes de fonctionnalités sont bienvenues ! Ouvrez une **GitHub Issue** avec :

1. Description claire de la fonctionnalité proposée
2. Cas d'usage / contexte
3. Implémentation suggérée (optionnel)
4. Références aux standards Pi, OpenCode, Codex ou Claude si applicable

### Soumettre des corrections / améliorations

1. Fork le repo
2. Créez une branche descriptive : `git checkout -b fix/issue-description` ou `feat/feature-name`
3. Commitez avec des messages clairs :
   ```
   Correction: [brève description]
   
   - Point 1
   - Point 2
   
   Résout #123
   ```
4. Poussez vers votre fork
5. Ouvrez une Pull Request (utiliser le template fourni)

### Structure des commits

Suivi du [Conventional Commits](https://www.conventionalcommits.org/) :

```
type(scope): description courte

Corps optionnel (1-2 paragraphes si contexte complexe)

Résout #123
```

Types reconnus :
- `feat` : nouvelle fonctionnalité (skill, prompt)
- `fix` : correction de bug
- `docs` : mise à jour de documentation
- `refactor` : restructuration (sans changement de comportement)
- `perf` : amélioration de performance
- `test` : ajout/amélioration de tests
- `chore` : maintenance, dépendances

## Standards de qualité

### Skills

Tous les nouveaux skills doivent :

1. **Suivre la structure canonique** (voir `0-vbb-standard/SKILL.md`)
2. **Avoir un SKILL.md** avec :
   - Frontmatter YAML complet (name, description, version, phase, etc.)
   - Sections : ROLE & POSTURE, INPUT CONTRACT, BLOCKING CONDITIONS, SCOPE, PROCESS, OUTPUT CONTRACT
   - Contrats d'entrée/sortie explicites
3. **Être placés dans le dossier phase appropriée** : `skills/[phase]-vbb-[nom]/`
4. **Respecter le nommage** : `[phase]-vbb-intention-descriptive`
5. **Être orthogonal** : pas de chevauchement avec d'autres skills
6. **Référencer PILOTAGE.md** : "Lire `docs/PILOTAGE.md` d'abord"

### Prompts

Tous les nouveaux prompts doivent :

1. **Avoir un frontmatter YAML** avec description
2. **Être nommés** : `{phase}-p-vbb-{nom}`
3. **Inclure les règles de routage** vers les skills appropriés
4. **Être documentés** dans `README.md`

### Documentation

- **Français primaire**, anglais secondaire pour spécifications techniques
- Lire `docs/PILOTAGE.md` pour cohérence opérationnelle
- Respecter la hiérarchie documentaire : PILOTAGE.md > PROJECT_MODE.md > SESSION.md

## Processus de review

1. **Automatique** : Les tests de linting et structure sont exécutés
2. **Manuel** : Un mainteneur examine la PR dans les 2-5 jours
3. **Feedback** : Les changements demandés sont discutés dans les commentaires de la PR
4. **Approbation** : Après approbation, fusion vers `main`

## Développement local

### Installation

```bash
git clone https://github.com/vibebackbone/vibebackbone.git
cd vibebackbone
```

### Validation locale

```bash
# Vérifier la structure (si scripts disponibles)
./scripts/validate-skills.sh
./scripts/validate-prompts.sh
```

### Documentation

```bash
# Générer la table des matières du README
# (si script fourni)
./scripts/generate-readme-toc.sh
```

## Contact & Discussions

- **Questions** : Ouvrez une GitHub Discussion
- **Sécurité** : Voir [SECURITY.md](SECURITY.md) (politique de divulgation responsable)
- **Autre** : Contactez les mainteneurs via [email support]

---

**Merci pour votre contribution !** 🙏
