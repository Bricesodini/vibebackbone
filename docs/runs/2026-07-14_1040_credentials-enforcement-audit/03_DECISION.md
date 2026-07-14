---
run_id: "2026-07-14_1040_credentials-enforcement-audit"
phase: "03_DECISION"
voie: "AUDIT"
status: "READY"
agent: "codex"
started_at: "2026-07-14T10:50:00+02:00"
ended_at: "2026-07-14T10:52:00+02:00"
next_phase: "07_CLOSEOUT"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_AUDIT.md"
artifacts_produced:
  - "03_DECISION.md"
---

# 03_DECISION — Credentials enforcement

## Question à trancher

Quel modèle doit faire respecter l'interdiction canonique sans dépendre
exclusivement d'un hook local contournable ?

## Options envisagées

### Option A — Outil Core partagé, hook + CI

- **Description** : un scanner unique lit les blobs staged localement et les
  changements de la PR en CI, avec la même politique et le même corpus.
- **Coût / effort** : moyen ; outil, fixtures, tests, hook et workflow.
- **Risques** : faux positifs, allowlist abusive, divergence de mode d'entrée.
- **Réversibilité** : facile si l'activation stricte est séparée du moteur.

### Option B — Hook local uniquement

- **Description** : ajouter le scanner au hook existant sans étape CI.
- **Coût / effort** : faible.
- **Risques** : absence d'installation et `--no-verify` laissent le P1 ouvert.
- **Réversibilité** : facile.

### Option C — Revue manuelle maintenue

- **Description** : conserver le comportement log-only et la règle canonique.
- **Coût / effort** : nul.
- **Risques** : dépendance humaine, détection non reproductible.
- **Réversibilité** : facile.

## Critères d'arbitrage

- Couverture de la frontière de confiance et des bypass — poids fort.
- Politique unique, testable et portable — poids fort.
- Faux positifs maîtrisables — poids moyen.
- Coût de maintenance Core/distributions — poids moyen.

## Verdict

- **Décision recommandée** : Option A.
- **Statut** : `CONDITIONAL_GO`.
- **Conditions de validité** : validation humaine de l'architecture, ADR
  acceptée, POC `GO`, corpus synthétique et Integration Gate avant code.

## Justification

Seule l'option A compense l'absence ou le bypass d'un hook local tout en gardant
une politique unique. L'audit n'autorise cependant pas à choisir silencieusement
le moteur, l'allowlist ou le niveau de blocage : ces points relèvent du prochain
run STRUCTURÉ.

## Conséquences attendues

- **Court terme** : P0-5-D reste ouvert et visible.
- **Moyen terme** : un contrôle Core commun peut fermer SEC-CRED-001/002.
- **Hypothèses à valider** : portabilité Bash/Python, temps d'exécution,
  changements de PR vs index staged et taux de faux positifs.

## Handoff vers `07_CLOSEOUT`

- **À planifier** : SEC-02, ADR + POC du contrôle en couches.
- **À surveiller** : aucune fixture réelle, aucune activation stricte sans
  corpus positif/négatif.
