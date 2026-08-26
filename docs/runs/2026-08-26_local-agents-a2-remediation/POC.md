---
run_id: "2026-08-26_local-agents-a2-remediation"
phase: "POC"
status: "CONCLUDED"
---

# POC — local-agents-a2-remediation

## Hypothèse

Tester la frontière résolue avant toute lecture et calculer l'état Git sur
l'entrée sélectionnée suffit à fermer les deux findings sans élargir la
discovery.

## Test

Fixtures temporaires : symlink externe non UTF-8 et symlink local non suivi
vers une cible tracked.

## Critère de réussite

GO si le premier retourne `EXTERNAL_SYMLINK` sans lecture et le second
retourne `UNTRACKED` pour l'entrée `AGENTS.md`.

## Décision

- **Verdict**: GO
- **Justification** : les deux comportements sont déterministes et testables.
