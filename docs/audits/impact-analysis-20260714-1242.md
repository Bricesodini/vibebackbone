# Impact analysis — consumer managed hook bundle

**Date**: 2026-07-14 12:42 Europe/Paris
**Mode**: DEV
**Verdict**: `READY`
**Classification**: `CONDITIONAL`

## Changement analysé

Remplacer la copie du redirecteur obsolète par un bundle runtime VBB géré avec
manifeste de hashes, détection de personnalisation, installation canonique et
propagation fidèle des erreurs.

## Impact direct

- `tools/vbb-project-init.py` : nouvelle sémantique pour `--install-hook`, flag
  dédié au remplacement d'un hook/asset et manifeste consommateur.
- `tests/test_project_init.py` : cycle de vie complet à couvrir.
- Sources copiées : installateur canonique, deux scripts hooks, credentials gate,
  loop-closure gate, résolveur de run et déclaration de dépendances VBB.
- `.git/hooks/pre-commit` et `commit-msg` du consommateur : créés seulement après
  preflight ; un hook préexistant reste intact sans autorisation dédiée.

## Impact indirect

- Le bloc `contract-tooling` acquiert un contrat d'ownership consommateur.
- Le manifeste devient une donnée de provenance versionnable ; aucun secret ni
  état métier n'y figure, seulement chemins et SHA-256.
- `t-vbb-project-context-init` et le prompt init doivent refléter le flag dédié.

## Impact externe

- Pi, OpenCode, Codex et Claude Code héritent du même outil Core ; aucun fichier
  dans `distributions/<provider>/` ne doit changer.
- Nouveau consommateur : non-breaking.
- Consommateur avec assets copiés historiquement sans manifeste : adoption
  explicite nécessaire, donc compatibilité conditionnelle.
- Aucun endpoint, schéma DB, API réseau ou runtime de production touché.

## Contrats et formats

- CLI : ajout non-breaking de `--overwrite-hook` et `--overwrite-managed`; `--overwrite` cesse
  d'autoriser implicitement le remplacement d'un hook Git lorsque
  `--install-hook` est combiné. Cette restriction est volontaire et sécurise un
  comportement dangereux.
- Format : manifeste JSON schema 1, chemins relatifs et hashes SHA-256.
- Dépendance : le loop-closure gate conserve PyYAML déclaré dans
  `requirements.txt`; aucune installation de package implicite.

## UNKNOWN

- Nombre et état des anciens dépôts consommateurs externes.
- Présence locale de PyYAML dans chacun ; le défaut doit produire un échec
  visible lors de l'exécution concernée, pas une installation silencieuse.
