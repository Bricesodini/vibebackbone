# POC — Ruff format diff

**Liée à ADR**: `docs/adr/0035-supported-python-static-toolchain.md`

## Hypothèse

Le formatter Ruff 0.13.1 produit un diff exclusivement syntaxique et son
absence de changement sémantique peut être renforcée par comparaison AST.

## Preuves avant code

- `ruff format --check tools tests` : 29 fichiers à reformater, 4 conformes.
- `ruff format --diff tools tests` : 4 382 lignes de diff sur ces 29 fichiers,
  sans mutation du worktree.
- La version exécutée est celle figée par ADR 0035.

## Critère

GO si le périmètre est exactement celui configuré et si un contrôle AST
avant/après accompagne tests et P.R2.

## Verdict

**Verdict**: GO

```yaml
FINAL_STATUS: GO
adr_link: docs/adr/0035-supported-python-static-toolchain.md
hypothesis_validated: true
metric_observed: "29 files; 4382 diff lines; 4 already formatted"
reproducible: true
```
