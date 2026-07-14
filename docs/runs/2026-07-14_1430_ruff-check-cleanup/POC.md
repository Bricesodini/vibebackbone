# POC — Ruff safe-fix review

**Liée à ADR**: `docs/adr/0035-supported-python-static-toolchain.md`

## Hypothèse

Les corrections automatiques sûres retirent uniquement imports inutilisés et
préfixes `f` sans interpolation ; les 12 autres écarts restent sous revue
manuelle.

## Preuves avant code

`ruff check --fix --diff tools tests` propose 25 corrections : 6 imports
inutilisés et 19 préfixes de chaînes. Le contenu littéral des chaînes est
inchangé. Ruff annonce 8 corrections supplémentaires uniquement avec
`--unsafe-fixes`, option interdite dans ce run.

## Critère

GO si le diff automatique ne retire aucun appel, contrôle, argument ou contenu
de sortie et si les corrections restantes sont localement caractérisables.

## Verdict

**Verdict**: GO

```yaml
FINAL_STATUS: GO
adr_link: docs/adr/0035-supported-python-static-toolchain.md
hypothesis_validated: true
metric_observed: "25 safe fixes reviewed; 8 unsafe fixes excluded; 12 manual"
reproducible: true
```
