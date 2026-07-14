# POC — Differential credentials scanner

**Statut**: CONCLUDED
**Date**: 2026-07-14
**Liée à ADR**: `docs/adr/0033-layered-core-credentials-enforcement.md`
**Liée à RUN**: `docs/runs/2026-07-14_1150_credentials-enforcement/`

## Hypothèse

Un moteur Python stdlib peut détecter des credentials synthétiques uniquement
sur les lignes ajoutées par Git, ignorer suppressions/binaires/placeholders et
exiger une justification locale pour les exemples autorisés.

## Méthode sûre

- Dépôt Git temporaire supprimé automatiquement.
- Blobs injectés directement dans l'index Git ; aucun fichier de worktree.
- Valeurs de forme sensible assemblées en mémoire à partir de fragments ; aucune
  valeur complète ressemblant à un credential n'est suivie dans le dépôt.
- Prototype inline non sauvegardé sous `tools/`.

## Corpus et résultat

| Cas | Attendu | Résultat |
|---|---:|---:|
| Format AWS synthétique assemblé | finding | PASS |
| Format GitHub synthétique assemblé | finding | PASS |
| Délimiteur de clé privée assemblé | finding | PASS |
| Affectation générique `api_key` synthétique | finding | PASS |
| Placeholder explicitement synthétique | aucun | PASS |
| Référence `${API_KEY}` | aucun | PASS |
| Exception avec `reason=` | warning/aucun finding | PASS |
| Exception sans justification | finding | PASS |
| Ligne ajoutée dans l'index staged | finding | PASS |
| Suppression staged | aucun | PASS |
| Blob binaire staged | aucun | PASS |

**Score final** : `11/11`.

## Itérations du harness

1. Premier essai : erreur de type `str`/`bytes` dans la capture subprocess ;
   aucune conclusion métier.
2. Deuxième essai : 8/11, échappement excessif dans deux regex du prototype.
3. Troisième essai : 11/11 après correction de la seule mécanique regex.

Ces itérations sont conservées pour distinguer la preuve finale des erreurs du
harness et éviter de transformer un faux négatif de test en validation.

## Verdict

- **Verdict** : GO
- **Justification**: extraction différentielle et politique minimale faisables
  sans dépendance externe ni fixture sensible suivie.
- **Limite**: le POC valide la faisabilité, pas la couverture exhaustive de tous
  les formats de credentials.

```yaml
FINAL_STATUS: GO
adr_link: docs/adr/0033-layered-core-credentials-enforcement.md
hypothesis_validated: true
metric_observed: "11/11 synthetic cases"
metric_threshold: "all positive and negative cases match expectations"
reproducible: true
verified_at: "2026-07-14T11:58:00+02:00"
verified_by: codex
```
