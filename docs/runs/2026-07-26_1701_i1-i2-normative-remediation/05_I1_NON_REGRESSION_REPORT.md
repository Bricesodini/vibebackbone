# 05_I1_NON_REGRESSION_REPORT — I1/I2 normative remediation

## Constats Git

- `git status --short --branch` a été exécuté avant la création du run.
- Le tag `i1-final-baseline` n'existe pas dans le dépôt courant.
- Sans tag de référence, un diff exact contre le baseline I1 est impossible.
- Aucun fichier de code, migration, test métier, runtime, format canonique, digest ou reçu I1 n'a été touché par ce run avant ce rapport.

## Verdict de preuve

`PARTIAL`: l'absence de mutation locale est observable, mais la comparaison normative exacte avec I1 ne peut pas être prouvée sans le tag demandé.

## Blocage restant

Fournir ou restaurer `i1-final-baseline` dans ce dépôt, puis relancer la comparaison exacte avant toute décision de gel.
