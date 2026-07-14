---
run_id: "2026-07-14_1242_consumer-managed-hook-bundle"
phase: "02_AUDIT"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T12:46:00+02:00"
ended_at: "2026-07-14T12:51:00+02:00"
next_phase: "04_PLAN"
artifacts_consumed:
  - "01_INTAKE.md"
  - "docs/ARCHITECTURE.md"
  - "docs/RELATIONS.md"
  - "docs/PROJECT_MODE.md"
artifacts_produced:
  - "02_AUDIT.md"
  - "docs/audits/impact-analysis-20260714-1242.md"
---

# 02_AUDIT — Impact du bundle hook consommateur géré

## Périmètre audité

Propagation de l'ADR 0034 sur l'initialiseur, l'installateur canonique, les
outils appelés par les hooks, la CLI publique et les quatre distributions.

## Méthode

Lecture du bloc `contract-tooling`, de sa projection RELATIONS, du source de
`vbb-project-init.py`, des deux hooks, de l'installateur et des imports
transitifs. Comparaison avec le POC NO-GO TER-001 et SEC-CRED-005.

## Findings

| # | Dimension | Severity | Type | Evidence Level | Evidence Trace | Decision | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | Direct | P1 | VIOLATION | VERIFIED_FINDING | initializer copie le redirecteur, qui appelle un installateur absent | ACCEPTED | bundle complet requis |
| 2 | Erreur | P1 | VIOLATION | VERIFIED_FINDING | `_install_hook` retourne ERROR mais `init_project` le classe dans skipped | ACCEPTED | erreur terminale requise |
| 3 | Ownership | P1 | VIOLATION | VERIFIED_FINDING | POC refresh : 0/3 sentinelles après deux overwrites | ACCEPTED | documents exclus du refresh |
| 4 | Dépendances | P2 | OBSERVATION | OBSERVATION | loop closure charge `vbb_run_resolution.py` et PyYAML | MITIGATED | bundle transitif + dépendance déclarée |
| 5 | Distributions | P3 | OBSERVATION | VERIFIED_FINDING | les quatre adapters héritent du même Core | ACCEPTED | aucune glue provider |

## Verdict global

- **Statut** : `READY`
- **Justification** : l'impact est borné au bloc Contract Tooling et à un format
  de manifeste consommateur. Le changement est conditionnellement compatible :
  les nouveaux consommateurs sont transparents, les assets historiques sans
  provenance exigent une adoption explicite.

## Manques d'évidence / UNKNOWN

- Aucun inventaire des dépôts consommateurs externes n'est disponible ; aucune
  affirmation n'est faite sur leurs personnalisations existantes.

## Recommandations

- Preflight complet avant copie.
- Inclure les dépendances transitives versionnées ; exposer PyYAML comme
  prérequis existant plutôt que l'installer implicitement.
- Séparer `--overwrite-hook` de `--overwrite`.

## Handoff vers `04_PLAN`

- **Décisions à arbitrer** : aucune, ADR 0034 acceptée.
- **Points de vigilance** : ne pas fermer TER-001 comme promesse de merge docs.
