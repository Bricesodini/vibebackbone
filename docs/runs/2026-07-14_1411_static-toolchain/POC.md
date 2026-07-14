# POC — Static toolchain reproducibility

**Liée à ADR**: `docs/adr/0035-supported-python-static-toolchain.md`

## Hypothèse

Ruff+mypy peuvent partager un périmètre explicite Python 3.11 sans conflit et
sans masquer la dette existante.

## Preuves avant configuration

- CI distante : Python 3.11 sur Ubuntu et macOS.
- Ruff 0.13.1 : 37 erreurs, 29 fichiers à formatter.
- Mypy 2.1.0 : 20 erreurs sur `tools/` après nettoyage executor.
- Pyright : absent, aucune configuration ou exigence distincte.
- Aucun `pyproject.toml`, `mypy.ini`, `.ruff.toml` concurrent.

## Critère

GO si les versions et périmètres sont bornés, si aucune exclusion ne cache la
baseline et si les gates existantes restent inchangées.

## Verdict

**Verdict**: GO

```yaml
FINAL_STATUS: GO
adr_link: docs/adr/0035-supported-python-static-toolchain.md
hypothesis_validated: true
metric_observed: "ruff 37; format 29; mypy 20; Python 3.11"
reproducible: true
```
