# POC — Four-provider independence

**Statut**: CONCLUDED
**Date**: 2026-07-13
**Liée à ADR**: `docs/adr/0025-supported-runtimes-pi-opencode-codex-claude.md`
**Liée à RUN**: `docs/runs/2026-07-13_1656_retire-hermes/`

## Hypothèse

Les adaptateurs Pi, OpenCode, Codex et Claude Code sont installables sans
dépendance au code Hermes.

## Test

```bash
bash setup.sh --provider pi --provider opencode --provider codex --provider claude --dry-run --no-interactive
rg -i "hermes|cody" distributions/{pi,opencode,codex,claude}
```

## Critère de réussite

GO si le dry-run sort avec le code 0 et si aucun adaptateur conservé ne
référence Hermes/Cody.

## Résultat observé

- Dry-run : exit 0 ; quatre providers `install`, Hermes `skip`.
- Scan des quatre dossiers : aucune occurrence, exit 1 attendu par `rg`.
- Écriture externe : aucune (`--dry-run`).

## Décision

- **Verdict** : GO
- **Justification** : la dépendance à retirer est confinée au routeur, à la
  distribution Hermes et aux surfaces documentaires/tests identifiées.

## Bilan

Le retrait peut procéder avec une rupture CLI explicite et une régression
complète du routeur à quatre providers.
