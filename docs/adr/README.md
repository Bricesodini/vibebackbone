# docs/adr/

Architecture Decision Records.

Format : `{nnnn}-{slug}.md` (lowercase, zéro-paddé sur 4 chiffres)

Exemple : `0001-choix-framework-api.md`

---

## Index

| # | Titre | Statut | Date | Source |
|---|-------|--------|------|--------|
| [0001](0001-formal-executor-boundary.md) | Formal executor boundary | — | — | — |
| [0002](0002-surface-first-routing-ui-ux.md) | Surface-first routing (UI/UX) | — | — | — |
| [0003](0003-graphic-propagation-map.md) | Graphic propagation map | — | — | — |
| [0004](0004-contract-schema-version-semantics.md) | Contract schema version semantics | — | — | — |
| [0005](0005-db-orientation-context-extension.md) | DB Orientation (Gap-01) | ACCEPTED | 2026-07-12 | [multi-service Gap-01](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-01) |
| [0006](0006-project-archetype-context-extension.md) | Project Archetype (Gap-02) | ACCEPTED | 2026-07-12 | [multi-service Gap-02](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-02) |
| [0007](0007-contracts-consumed-canonical-file.md) | CONTRACTS_CONSUMED canonique (Gap-05, P0) | ACCEPTED | 2026-07-12 | [multi-service Gap-05](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-05) |
| [0008](0008-context-project-mode-enrichment.md) | CONTEXT.md / PROJECT_MODE.md enrichi (Gap-14) | ACCEPTED | 2026-07-12 | [multi-service Gap-14](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-14) |
| [0009](0009-multiservice-lint-discipline.md) | Linter discipline multi-service (Gap-04, P0) | ACCEPTED | 2026-07-13 | [multi-service Gap-04](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-04) |
| [0010](0010-impact-log-cumulative.md) | IMPACT_LOG cumulatif (Gap-06, P0) | ACCEPTED | 2026-07-13 | [multi-service Gap-06](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-06) |
| [0011](0011-cross-service-contract-taxonomy.md) | Taxonomie contrats cross-service (Gap-10, P0) | ACCEPTED | 2026-07-13 | [multi-service Gap-10](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-10) |
| [0012](0012-codegen-agents-claudemd.md) | Codegen AGENTS.md / CLAUDE.md (Gap-03, P1) | ACCEPTED | 2026-07-13 | [multi-service Gap-03](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-03) |
| [0014](0014-canon-vs-extension.md) | Mécanisme canon vs extension (Gap-09, P1) | ACCEPTED | 2026-07-13 | [multi-service Gap-09](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-09) |
| [0015](0015-contract-lint-archetype-aware.md) | vbb-contract-lint archetype-aware (Gap-11, P1) | ACCEPTED | 2026-07-13 | [multi-service Gap-11](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-11) |
| [0017](0017-co-evolution-discipline.md) | Discipline outillée de co-évolution (Gap-07, P1) | ACCEPTED | 2026-07-13 | [multi-service Gap-07](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-07) |
| [0018](0018-multirepo-support.md) | Multi-repo support (Gap-08, P0) | ACCEPTED | 2026-07-13 | [multi-service Gap-08](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-08) |
| [0019](0019-first-extension-database-per-service.md) | Première extension concrète (Gap-12, P1) | ACCEPTED | 2026-07-13 | [multi-service Gap-12](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-12) |
| [0020](0020-multiservice-graph.md) | Graphe inter-services (Gap-13, P0) | ACCEPTED | 2026-07-13 | [multi-service Gap-13](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-13) |
| [0021](0021-ci-gate-enforcement.md) | Gate CI enforcement (Gap-15, P0) | ACCEPTED | 2026-07-13 | [multi-service Gap-15](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-15) |
| [0022](0022-include-formalization.md) | Formalisation `@include` (Gap-16, P2) | ACCEPTED | 2026-07-13 | [multi-service Gap-16](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-16) |
| [0023](0023-generated-sentinel-detection.md) | Sentinel `@generated` + détection (Gap-17, P2) | ACCEPTED | 2026-07-13 | [multi-service Gap-17](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-17) |
| [0024](0024-snapshot-to-log.md) | Snapshot→log cumulatif (Gap-18, P2) | ACCEPTED | 2026-07-13 | [multi-service Gap-18](../../strategy/vbb-evolution-multi-service-support/01_GAP_ANALYSIS.md#gap-18) |
| [0025](0025-supported-runtimes-pi-opencode-codex-claude.md) | Supported runtimes: Pi, OpenCode, Codex, Claude Code | ACCEPTED | 2026-07-13 | [Run](../runs/2026-07-13_1656_retire-hermes/) |
| [0026](0026-global-maintainability-audit-before-remediation.md) | Global maintainability audit before remediation | ACCEPTED | 2026-07-13 | [Run](../runs/2026-07-13_1717_global-debt-janitor-doc/) |
| [0027](0027-shared-run-resolution-and-canonical-hook-installer.md) | Shared run resolution and canonical hook installer | ACCEPTED | 2026-07-13 | [Run](../runs/2026-07-13_1811_v2r1-gates-fiables/) |
| [0028](0028-scoped-audit-protocol.md) | Scoped audit protocol | ACCEPTED | 2026-07-13 | — |
| [0029](0029-risk-triggered-closeout-quality-pass.md) | Risk-triggered closeout quality pass | ACCEPTED | 2026-07-13 | — |
| [0030](0030-boot-set-diet-and-portability.md) | Boot-set diet and portability | ACCEPTED | 2026-07-13 | — |
| [0031](0031-autonomous-multirun-protocol.md) | Autonomous multirun protocol | ACCEPTED | 2026-07-13 | — |
| [0032](0032-responsibility-first-routing-consolidation.md) | Responsibility-first routing consolidation | ACCEPTED | 2026-07-14 | [Run](../runs/2026-07-14_0830_weakpoint-responsibility-routing/) |
| [0033](0033-layered-core-credentials-enforcement.md) | Layered Core credentials enforcement | ACCEPTED | 2026-07-14 | [Run](../runs/2026-07-14_1150_credentials-enforcement/) |
| [0013-arch](0013-repo-organization-core-vs-distributions.md) | Repo organization Core vs Distributions | — | — | — |

## Conventions

- Chaque ADR doit suivre le template [`docs/templates/ADR.md.template`](../templates/ADR.md.template).
- Status possibles : `PROPOSED` / `ACCEPTED` / `REJECTED` / `SUPERSEDED by NNNN`.
- Le `LONG_RUN_SUMMARY` YAML en bas de chaque ADR est lu par `t-vbb-impact-analyzer` pour calculer la propagation.
- Les ADR `ACCEPTED` sont immuables : tout changement ouvre une nouvelle ADR qui **supersede** l'ancienne.
- ADR 0025 supersède uniquement la surface Hermes active décrite par ADR 0013 ;
  l'organisation Core/distributions d'ADR 0013 reste valide.

## Run d'origine

Les ADR 0005-0008 proviennent du **Run 08** (2026-07-12) — Phase 2 de la caractérisation `vbb-evolution-multi-service-support`. Chaque ADR documente la décision de design ; l'implémentation runtime est différée à des Runs ultérieurs.
