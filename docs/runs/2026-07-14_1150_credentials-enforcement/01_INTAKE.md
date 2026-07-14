---
run_id: "2026-07-14_1150_credentials-enforcement"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-14T11:50:00+02:00"
ended_at: "2026-07-14T11:52:00+02:00"
next_phase: "02_AUDIT"
artifacts_consumed:
  - "docs/runs/2026-07-14_1040_credentials-enforcement-audit/07_CLOSEOUT.md"
  - "docs/audits/security-credentials-20260714-1040.md"
artifacts_produced:
  - "01_INTAKE.md"
  - "../../adr/0033-layered-core-credentials-enforcement.md"
---

# 01_INTAKE — Layered Core credentials enforcement

## Demande reçue

> Go

## Décision humaine interprétée

Validation explicite de l'Option A proposée par SEC-01 : un scanner Core unique
partagé par le hook local et la CI. Cette validation autorise la formalisation
ADR/POC, pas le code avant passage de l'Integration Gate.

## Objectif

Fermer SEC-CRED-001 et SEC-CRED-002 par un contrôle différentiel, reproductible
et sans dépendance externe, identique aux frontières locale et CI.

## Scope

### Dans le périmètre

- `tools/vbb-credentials-gate.py`
- `scripts/hooks/pre-commit-framework-gate`
- `.github/workflows/vbb-contracts.yml`
- `scripts/vbb-ci-local.sh`
- tests unitaires et intégration hook
- architecture, ADR, décision Core→distributions et vérité d'audit

### Hors périmètre

- rotation ou recherche de credentials historiques
- secrets réels ou fixtures suivies ressemblant à des credentials
- dépendance tierce, coffre de secrets ou runtime consommateur
- changement spécifique à Pi, OpenCode, Codex ou Claude Code

## Invariants

- Aucun secret, token, clé API ou clé privée réel n'est créé ou commité.
- Le hook et la CI exécutent le même moteur de détection.
- Les suppressions, binaires et lignes inchangées ne bloquent pas.
- Une exception est locale, explicite, justifiée et visible dans la sortie.

## Linkage

- **Liée à ADR**: `docs/adr/0033-layered-core-credentials-enforcement.md`
- **Liée à POC**: `docs/runs/2026-07-14_1150_credentials-enforcement/POC.md`

## Risque et route

- **Risque** : sécurité P1.
- **Route** : STRUCTURÉE pour la remédiation, après un AUDIT SEC-01 terminé.
- **Escalade** : STOP immédiat si le POC ou le gate n'est pas `GO/PASS`.
