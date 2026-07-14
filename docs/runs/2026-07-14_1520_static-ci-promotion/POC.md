# POC — Static CI promotion

**Liée à ADR**: `docs/adr/0035-supported-python-static-toolchain.md`

## Hypothèse

Les trois commandes propres peuvent être ajoutées comme checks bloquants sans
nouveau service, permission ou configuration concurrente.

## Preuves avant code

- Main propre : Ruff check PASS, 33 fichiers formatés, mypy 0/16.
- GitHub Actions `a708165` : Ubuntu/macOS success avec Python 3.11.
- `requirements-dev.txt` inclut les dépendances runtime et fixe Ruff/mypy.
- Les historiques Wave 2 prouvent que chaque commande retourne non-zéro sur une
  baseline invalide ; une preuve contrôlée fraîche sera rejouée après wiring.

## Critère

GO si les deux CI peuvent invoquer les mêmes modules/configuration et si les
permissions/triggers restent inchangés.

## Verdict

**Verdict**: GO

```yaml
FINAL_STATUS: GO
adr_link: docs/adr/0035-supported-python-static-toolchain.md
hypothesis_validated: true
metric_observed: "3 clean commands; remote 2/2 OS success; read-only permissions"
reproducible: true
```
