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

- **Date d'exécution** : 2026-07-13 18:2x (GO Brice reçu)
- **Sortie littérale** :
  - (a) loop-closure : `[info] No run_id given — using most recent: 20260615-usage-audit`
    → `RESULT: FAIL — 1 issue(s)` avec en outre `unknown voie 'STRUCTURED'
    (expected ... 'STRUCTUREE')` — l'évidence exacte de l'audit TD-101 ;
  - (b) `ls -td docs/runs/*/ | head -1` → `2026-07-13_1811_v2r1-gates-fiables/` ;
  - (c) dashboard `latest_runs[0].id` → `2026-07-13_1717_global-debt-janitor-doc`.
- **Métrique mesurée** : (a) + (b) + (c) tous conformes au seuil.

## Décision

- **Verdict** : GO
- **Justification** : divergence TD-101 reproduite ; chaque sélecteur est correct
  dans sa population ; les populations divergent comme attendu (run actif non clôturé).

## Bilan

Hypothèse validée → ADR 0027 passe ACCEPTED, gate PASS, 04_PLAN peut s'ouvrir.
Constat supplémentaire pour le plan : loop-closure doit aussi normaliser le
vocabulaire de voie (`STRUCTURED`/`STRUCTUREE`) — couvert par l'évidence TD-101.

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: GO
adr_link: docs/adr/0027-shared-run-resolution-and-canonical-hook-installer.md
hypothesis_validated: true
metric_observed: "(a) loop-closure → 20260615-usage-audit + voie STRUCTURED rejetée ; (b) mtime → 2026-07-13_1811_v2r1-gates-fiables ; (c) dashboard → 2026-07-13_1717_global-debt-janitor-doc"
metric_threshold: "(a) divergence TD-101 reproduite ; (b) dernier run existant = 2026-07-13_1811_v2r1-gates-fiables ; (c) dernier run clôturé = 2026-07-13_1717_global-debt-janitor-doc — populations distinctes, identité non requise"
reproducible: true
verified_at: "2026-07-13T16:25:00Z"
verified_by: "claude-code (GO Brice)"
```
