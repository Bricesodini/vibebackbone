# ADR — 0026-global-maintainability-audit-before-remediation

**Status**: ACCEPTED
**Date**: 2026-07-13
**Route**: AUDIT
**Décideurs**: Brice (demande), Codex (formalisation)
**Liée à**: ADR 0025
**Liée à POC**: vide — audit read-only, aucune hypothèse d'intégration à prototyper

## Contexte

Après le retrait d'Hermes et le recentrage sur quatre adaptateurs, Brice demande
une passe globale de dette technique, Janitor, conventions et cohérence
documentaire. Les quatre skills sélectionnés imposent une séparation entre le
diagnostic et les corrections afin d'éviter qu'un nettoyage global ne produise
du churn ou un changement de comportement non maîtrisé.

## Décision

La passe globale est exécutée comme un audit read-only unique : elle inventorie,
qualifie et priorise la dette, mais ne modifie ni code, ni structure, ni canon.
Les remédiations seront découpées ensuite en micro-boucles séparées et sourcées.

## Conséquences

### Positives

- Une baseline factuelle commune couvre dette, bruit, conventions et docs.
- Les corrections futures disposent de preuves, priorités et validations définies.
- Les changements utilisateur préexistants restent isolés.

### Négatives / coûts

- La passe ne rembourse pas immédiatement la dette détectée.
- L'inventaire global peut produire plusieurs findings de faible sévérité.

### Neutres

- Les archives et runs historiques restent visibles mais ne sont pas traités
  comme documentation active.

## Alternatives rejetées (≥ 2)

### Alternative A — Nettoyer pendant le scan

- **Description** : corriger chaque problème dès sa découverte.
- **Pourquoi rejetée** : mélange audit et exécution, augmente le risque de churn
  et contredit les contrats read-only des skills demandés.

### Alternative B — Auditer uniquement le dernier changement

- **Description** : limiter la passe aux fichiers touchés par ADR 0025.
- **Pourquoi rejetée** : la demande porte explicitement sur une passe globale et
  la dette ouverte dépasse la seule distribution retirée.

## Risques

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Faux positifs dans les archives | forte | moyen | séparer actif, historique et état local non suivi |
| Rapport trop large pour agir | moyenne | moyen | limiter la roadmap à 7 étapes et prioriser P0/P1/P2 |
| Conclusion sans preuve | faible | fort | exiger chemins et commandes reproductibles |

## Hypothèses

- Le dépôt courant est représentatif du framework distribué.
- Les fichiers non suivis préexistants ne sont pas une vérité canonique tant
  qu'ils ne sont pas intégrés explicitement.

## Références

- Run : `docs/runs/2026-07-13_1717_global-debt-janitor-doc/`
- Conventions : `docs/CONVENTIONS.md`
- Dette : `docs/TECH_DEBT.md`

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: ACCEPTED
decision_class: PROCESS
reversible: true
depends_on:
  - ADR 0025
blocks:
  - docs/runs/2026-07-13_1717_global-debt-janitor-doc/02_AUDIT.md
supersedes: []
verified_at: "2026-07-13T17:20:00+02:00"
verified_by: "codex"
verified_method: "gate linkage check"
```
