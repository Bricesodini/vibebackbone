# POC — Managed consumer hook bundle

**Statut**: CONCLUDED
**Date**: 2026-07-14
**Liée à ADR**: `docs/adr/0034-consumer-managed-runtime-assets.md`
**Liée à RUN**: `docs/runs/2026-07-14_1242_consumer-managed-hook-bundle/`

## Hypothèse

Un bundle VBB listé explicitement peut être copié et rafraîchi sans écraser une
personnalisation : un manifeste SHA-256 fournit la provenance, un preflight sur
toutes les cibles empêche l'état partiel, et l'installateur canonique fonctionne
depuis un dépôt consommateur autonome.

## Méthode sûre

- Harness jetable versionné dans le run, sans modification de code produit.
- Dépôt Git consommateur créé dans un répertoire temporaire puis supprimé.
- Sources réelles du bundle Core : installateur, hooks, credentials gate,
  loop-closure gate, résolveur de run et requirements VBB séparés.
- Document projet avec sentinelle, asset géré personnalisé, comparaison binaire
  d'un second asset pour prouver l'absence de copie partielle.

## Résultat

Commande :

```bash
python3 docs/runs/2026-07-14_1242_consumer-managed-hook-bundle/poc_managed_bundle.py
```

| Cas | Résultat |
|---|---:|
| Bundle frais + manifeste | PASS |
| Hooks canoniques réellement installés | PASS |
| Refresh inchangé idempotent | PASS |
| Personnalisation détectée et préservée | PASS |
| Aucun autre asset copié après conflit | PASS |
| Vérité projet préservée | PASS |

**Score final** : `6/6`.

## Verdict

- **Verdict** : GO
- **Justification** : le mécanisme de provenance et de preflight borne le
  refresh au bundle runtime et résout le faux succès observé sans toucher aux
  documents projet.
- **Limite** : le POC n'inventorie pas les consommateurs externes historiques ;
  une cible sans manifeste doit être refusée ou adoptée par override explicite.

```yaml
FINAL_STATUS: GO
adr_link: docs/adr/0034-consumer-managed-runtime-assets.md
hypothesis_validated: true
metric_observed: "6/6 managed bundle scenarios"
metric_threshold: "all scenarios pass"
reproducible: true
verified_at: "2026-07-14T12:58:00+02:00"
verified_by: codex
```
