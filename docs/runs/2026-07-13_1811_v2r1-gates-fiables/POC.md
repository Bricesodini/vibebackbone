# POC — v2r1-run-resolution

**Statut**: DRAFT — définie, **non exécutée** (aucune exécution avant GO Brice)
**Date**: 2026-07-13 (révisée après revue Brice — distinction des populations de runs)
**Liée à ADR**: docs/adr/0027-shared-run-resolution-and-canonical-hook-installer.md
**Liée à RUN**: docs/runs/2026-07-13_1811_v2r1-gates-fiables/

## Hypothèse

Nous supposons qu'une résolution par mtime exposant **deux sélecteurs distincts** —
**dernier run existant** (population : tous les répertoires de `docs/runs/`) et
**dernier run clôturé** (population : runs avec closeout, celle du dashboard) —
identifie correctement chacun des deux sur les données réelles du dépôt, là où la
détection lexicale de loop-closure sélectionne un run périmé (`20260615-usage-audit`).
Les deux sélecteurs portent sur des **populations différentes par construction** et
ne doivent **pas** être supposés identiques.

## Test (concret, exécutable)

```bash
# 1. Reproduction TD-101 : sélection actuelle de loop-closure (lecture seule)
python tools/vbb-loop-closure-check.py ; echo "exit=$?"

# 2. Sélecteur « dernier run clôturé » (population dashboard = runs avec closeout)
python tools/vbb-status-dashboard.py --json | python -c "import json,sys; d=json.load(sys.stdin); print(d.get('latest_run') or d)"

# 3. Sélecteur « dernier run existant » (population complète, mtime)
ls -td docs/runs/*/ | head -3
```

## Critère de réussite (mesurable)

GO si les trois observations tiennent **simultanément** :

- (a) **Divergence TD-101 reproduite** : loop-closure sélectionne un run périmé,
  différent des deux sélecteurs ci-dessous ;
- (b) **Dernier run existant** (mtime, population complète) =
  `2026-07-13_1811_v2r1-gates-fiables` (le présent run, actif, sans closeout) ;
- (c) **Dernier run clôturé** (population dashboard) =
  `2026-07-13_1717_global-debt-janitor-doc`.

Aucune exigence d'identité entre (b) et (c) : leur divergence est normale tant que
le run actif n'est pas clôturé. La validation porte sur la justesse de **chaque
sélecteur dans sa population**. Décision d'implémentation à acter au `04_PLAN` :
le résolveur partagé expose les deux sélecteurs et chaque consommateur (dashboard,
CI, loop-closure) déclare explicitement lequel il utilise.

## Résultat observé

- **Date d'exécution** : — (en attente GO Brice)
- **Sortie littérale** : —
- **Métrique mesurée** : — (seuil attendu : (a) + (b) + (c) ci-dessus)

## Décision

- **Verdict** : PENDING — à exécuter immédiatement après GO (test 100 % lecture seule, < 5 min)
- **Justification** : le GO conditionnel du 2026-07-13 autorise la préparation, pas l'exécution.

## Bilan

À compléter après exécution. Attendu : « Hypothèse validée → ADR 0027 passe
ACCEPTED, gate PASS, 04_PLAN peut s'ouvrir (avec choix de sélecteur par
consommateur). » En cas de NO-GO ou PIVOT (ex. mtime non fiable sur runs
restaurés), revenir à l'ADR § Alternatives.

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: PENDING
adr_link: docs/adr/0027-shared-run-resolution-and-canonical-hook-installer.md
hypothesis_validated: null
metric_observed: null
metric_threshold: "(a) divergence TD-101 reproduite ; (b) dernier run existant = 2026-07-13_1811_v2r1-gates-fiables ; (c) dernier run clôturé = 2026-07-13_1717_global-debt-janitor-doc — populations distinctes, identité non requise"
reproducible: true
verified_at: null
verified_by: null
```
