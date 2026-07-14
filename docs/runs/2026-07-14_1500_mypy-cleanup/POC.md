# POC — Mypy remediation shapes

**Liée à ADR**: `docs/adr/0035-supported-python-static-toolchain.md`

## Hypothèse

Les 20 erreurs proviennent de cinq formes bornées et peuvent être retirées avec
des annotations/guards cohérents avec les valeurs déjà produites.

## Preuves avant code

- 10 conteneurs vides reçoivent ensuite uniquement strings, dicts ou chemins
  observables dans leur fonction.
- `count_contracts` retourne déjà un float non vide ; seule l'annotation ment.
- Les deux boucles credentials itèrent deux dataclasses distinctes sous le même
  nom local ; les outputs sont testés.
- `spec_from_file_location` est optionnel par contrat Python ; executor et loop
  closure protègent déjà la même frontière.
- Contract runtime produit volontairement un dictionnaire hétérogène enrichi
  après création.

## Critère

GO si aucune valeur, branche, chaîne ou sortie n'a besoin de changer, hors guard
explicite sur une erreur de chargement déjà terminale.

## Verdict

**Verdict**: GO

```yaml
FINAL_STATUS: GO
adr_link: docs/adr/0035-supported-python-static-toolchain.md
hypothesis_validated: true
metric_observed: "20 errors; 5 bounded type-shape classes; 9 tools"
reproducible: true
```
