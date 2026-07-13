# ADR — 0025-supported-runtimes-pi-opencode-codex-claude

**Status**: ACCEPTED
**Date**: 2026-07-13
**Route**: STRUCTUREE
**Décideurs**: Brice
**Liée à**: ADR 0013
**Liée à POC**: `docs/runs/2026-07-13_1656_retire-hermes/POC.md`

## Contexte

Vibebackbone expose actuellement cinq distributions, dont Hermes/Cody. Le
retour d'usage de Brice ne justifie plus le coût de maintenance, la surface de
sécurité et la documentation spécifiques à Hermes. Les quatre outils de code
réellement retenus sont Pi, OpenCode, Codex et Claude Code.

## Décision

Vibebackbone devient un framework de gouvernance pour **Pi, OpenCode, Codex et
Claude Code uniquement**. La distribution Hermes/Cody, son proxy, son linter,
ses scripts et ses tests spécifiques sont retirés du dépôt et de l'installateur.

Le Core reste runtime-neutral afin d'éviter quatre forks méthodologiques, mais
la surface officiellement supportée et documentée est limitée à ces quatre
adaptateurs.

## Conséquences

### Positives

- Une promesse produit lisible : quatre runtimes supportés, tous installables.
- Moins de code de distribution, de sécurité et de documentation à maintenir.
- Aucun orchestrateur externe nécessaire pour appliquer la gouvernance Core.

### Négatives / coûts

- `bash setup.sh --provider hermes` devient invalide.
- Le proxy et le bypass-lint Hermes ne sont plus livrés dans l'état courant du dépôt.
- Les utilisateurs Hermes doivent rester sur une révision antérieure ou maintenir leur fork.

### Neutres

- Les runs, audits, ADR et changelogs historiques restent lisibles comme preuves datées.
- Aucun fichier sous `~/.hermes/` n'est modifié ou supprimé par cette migration.

## Alternatives rejetées

### Alternative A — Déprécier sans retirer

- **Description** : conserver tout le code Hermes avec un badge deprecated.
- **Pourquoi rejetée** : le coût de maintenance et la confusion documentaire resteraient présents.

### Alternative B — Promouvoir le proxy Hermes dans Core

- **Description** : généraliser le proxy et le bypass-lint avant de supprimer la distribution.
- **Pourquoi rejetée** : ces composants sont couplés aux profils, secrets et choix runtime Hermes ; aucune demande ni preuve ne justifie une nouvelle capacité Core.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Référence Hermes active oubliée | moyenne | moyen | scan ciblé hors historique + documentation tests |
| Régression installateur | faible | fort | smoke, dry-run des quatre providers et CI complète |
| Perte de preuve historique | faible | moyen | conserver runs/audits/changelog ; ADR 0025 supersède l'état actif uniquement |

## Hypothèses

- Pi, OpenCode, Codex et Claude Code restent les quatre runtimes voulus.
- Aucun consommateur actif ne dépend du contenu courant de `distributions/hermes/`.

## Références

- ADR amont : `docs/adr/0013-repo-organization-core-vs-distributions.md`
- Impact : `docs/audits/impact-analysis-20260713-1656.md`
- POC : `docs/runs/2026-07-13_1656_retire-hermes/POC.md`

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: ARCHITECTURE
reversible: true
depends_on:
  - ADR 0013
blocks: []
supersedes:
  - "Hermes-active portions of ADR 0013"
verified_at: "2026-07-13T16:56:00+02:00"
verified_by: "Brice"
verified_method: "explicit human request"
```
