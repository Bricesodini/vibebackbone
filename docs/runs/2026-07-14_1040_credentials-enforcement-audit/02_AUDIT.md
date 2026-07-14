---
run_id: "2026-07-14_1040_credentials-enforcement-audit"
phase: "02_AUDIT"
voie: "AUDIT"
status: "PARTIAL"
agent: "codex"
started_at: "2026-07-14T10:44:00+02:00"
ended_at: "2026-07-14T10:50:00+02:00"
next_phase: "03_DECISION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "POC.md"
  - "scripts/hooks/pre-commit-framework-gate"
  - "scripts/install-vbb-hooks.sh"
  - ".github/workflows/vbb-contracts.yml"
artifacts_produced:
  - "02_AUDIT.md"
  - "../../audits/audit-readiness-20260714-1040.md"
  - "../../audits/scope-freeze-20260714-1040.md"
  - "../../audits/security-credentials-20260714-1040.md"
---

# 02_AUDIT — Credentials enforcement

## Périmètre audité

Contrôle des contenus staged depuis le hook Core jusqu'à la CI, installation
locale et bypass compris. Aucun scanner ni credential réel n'est introduit.

## Méthode

- Readiness et scope freeze : `READY`.
- Lecture des hooks, installateurs, tests et workflow CI versionnés.
- Reproduction dans un dépôt Git temporaire avec blob synthétique staged.
- Chaîne de preuve OBSERVATION → SIGNAL → VÉRIFICATION → FINDING.

## Findings

| # | Dimension | Severity | Type | Evidence Level | Evidence Trace | Decision | Verdict |
|---|---|---|---|---|---|---|---|
| SEC-CRED-001 | staged content | `P1` | `VIOLATION` | `VERIFIED_FINDING` | message log-only → commentaire tool différé → blob synthétique exit 0 → aucun blocage | `NEEDS_DECISION` | invariant canonique non automatisé |
| SEC-CRED-002 | trust boundary | `P1` | `OBSERVATION` | `VERIFIED_FINDING` | hook local → install optionnelle/bypass → CI sans scan → aucun filet commun | `NEEDS_DECISION` | contrôle contournable sans backstop |
| SEC-CRED-003 | detection policy | `P2` | `TREND` | `VERIFIED_FINDING` | tests sans contenu → outil absent → cas limites non spécifiés → risque de scanner naïf | `NEEDS_DECISION` | politique et corpus manquants |
| SEC-CRED-004 | disclosure | `P3` | `OBSERVATION` | `VERIFIED_FINDING` | canon + hook déclarent le report → pas de claim trompeur | `MITIGATED` | transparence correcte |

## Verdict global

- **Statut** : `PARTIAL`
- **Justification** : la posture est observable et honnête, mais deux P1 restent
  ouverts. Le dépôt n'est pas bloqué pour sa maintenance ; il ne doit pas
  déclarer P0-5-D fermé avant un contrôle partagé local + CI.

## Manques d'évidence / UNKNOWN

- Installation effective dans les dépôts consommateurs.
- Choix du moteur et politique d'allowlist.
- Taux réel de faux positifs/négatifs avant corpus POC.

## Recommandations

- Créer une ADR dédiée au modèle d'enforcement en couches.
- Prouver un scanner de blobs staged avec fixtures synthétiques et cas limites.
- Réutiliser exactement le même outil dans le hook et la CI.

## Handoff vers `03_DECISION`

- **Décisions à arbitrer** : outil Core interne ou dépendance ; politique
  d'allowlist ; activation bloquante locale et CI.
- **Points de vigilance** : ne jamais créer de fixture ressemblant à un secret
  réel et ne pas confondre heuristique avec garantie absolue.
