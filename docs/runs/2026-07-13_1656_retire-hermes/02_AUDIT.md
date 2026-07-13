---
run_id: "2026-07-13_1656_retire-hermes"
phase: "02_AUDIT"
route: "STRUCTUREE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex / t-vbb-impact-analyzer"
started_at: "2026-07-13T16:58:00+02:00"
ended_at: "2026-07-13T17:03:00+02:00"
next_phase: "03_DECISION"
artifacts_consumed:
  - "docs/ARCHITECTURE.md"
  - "docs/RELATIONS.md"
  - "docs/PROJECT_MODE.md"
  - "docs/DISTRIBUTIONS.md"
artifacts_produced:
  - "02_AUDIT.md"
  - "docs/audits/impact-analysis-20260713-1656.md"
---

# 02_AUDIT — Impact of retiring Hermes

## Change analyzed

Supprimer Hermes/Cody de la surface supportée et limiter le framework à Pi,
OpenCode, Codex et Claude Code.

## Direct impact

- `distributions/hermes/` supprimé.
- `setup.sh --provider hermes` devient invalide.
- Architecture, catalogues, docs d'installation et smoke tests mis à jour.

## Indirect impact

- Les hooks et règles Core doivent perdre leurs références Cody/Hermes tout en
  conservant leur comportement générique.
- Les fixtures de review-tier doivent devenir provider-neutral.
- RELATIONS doit être régénéré depuis ARCHITECTURE.

## External impact

- Rupture pour tout utilisateur du provider Hermes ou du proxy livré dans ce dépôt.
- Aucun effet sur les quatre adaptateurs conservés : aucun import Hermes trouvé.
- `~/.hermes/` reste intact ; la migration ne désinstalle aucun runtime externe.

## Final classification

**BREAKING** — rupture explicite, acceptée par Brice, bornée à la distribution
retirée et documentée dans ADR 0025/changelog.

## UNKNOWN

- Consommateurs externes non visibles qui importent directement le proxy Hermes.
