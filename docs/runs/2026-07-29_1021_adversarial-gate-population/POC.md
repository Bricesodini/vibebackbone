---
template_id: "POC"
version: "1.0"
lane_eligible:
  - "STRUCTUREE"
run_id: "2026-07-29_1021_adversarial-gate-population"
---

# POC — GATE-POPULATION-01

**Statut**: CONCLUDED
**Date**: 2026-07-29
**Liée à ADR**: `docs/adr/0051-adversarial-assurance-dimension.md`
**Liée à RUN**: `docs/runs/2026-07-29_1021_adversarial-gate-population/`

## Hypothèse

Nous supposons que la population des runs post-cutoff est énumérable de façon
déterministe depuis la donnée committée seule, et que l'agrégation du gate
**existant** sur cette population sort `FAIL` à `6b0daf4` — c'est-à-dire que
l'instrument est capable d'échouer avant qu'on lui fasse confiance.

## Test (concret, exécutable)

Aucun outil du dépôt n'est modifié. Le POC ne fait que réutiliser
`tools/vbb_run_resolution.py` et invoquer le gate existant run par run.

```bash
python3 - <<'PY'
import subprocess, sys
from datetime import datetime
from pathlib import Path
sys.path.insert(0, "tools")
from vbb_run_resolution import list_runs_chronological, run_identity_datetime, find_closeout

CUTOFF = datetime(2026, 7, 28, 14, 0)
runs = list_runs_chronological(Path("docs/runs"))
post = [r for r in runs if (d := run_identity_datetime(r)) is not None and d >= CUTOFF]
failing, closeoutless = [], []
for r in sorted(post, key=lambda p: p.name):
    if find_closeout(r) is None:
        closeoutless.append(r.name); continue
    rc = subprocess.run(["python3", "tools/vbb-adversarial-gate.py", str(r), "--strict"],
                        capture_output=True, text=True).returncode
    if rc != 0:
        failing.append(r.name)
print("failing:", len(failing), "closeoutless:", len(closeoutless))
sys.exit(2 if (failing or closeoutless) else 0)
PY
```

## Critère de réussite (mesurable)

GO si, à `6b0daf4`, l'agrégation sort un code de sortie **non nul** et énumère au
moins un run non conforme. Un exit `0` invaliderait l'hypothèse : l'instrument
serait incapable de détecter l'état que l'audit a mesuré à la main, et R1 devrait
être reconçu avant tout code.

## Résultat observé

- **Date d'exécution** : 2026-07-29 10:26 CEST, working tree à `6b0daf4` + `01_INTAKE.md` non committé
- **Métrique mesurée** : exit `2`, 10 runs non conformes (seuil attendu : exit ≠ 0, ≥ 1 run)

### Sortie littérale

```
total run dirs        : 161
undatable identities  : 0 -> []
post-cutoff population: 13

  gate=2      2026-07-28_1400_m2-adversarial-loop-implementation
  gate=2      2026-07-28_1600_r0-adversarial-audit-of-m2-implementation
  gate=2      2026-07-28_1800_r1-r0-findings-normative-arbitration
  gate=2      2026-07-28_2000_m2-bis-adversarial-loop-bootstrap-deployment
  gate=2      2026-07-28_2200_a2-certification-of-m2-bis-bootstrap
  gate=2      2026-07-28_2300_r2-a2-arbitration-of-a2-findings
  gate=2      2026-07-29_0100_m3-remediation-of-a2-findings
  gate=2      2026-07-29_0300_a2-retry-certification-of-m3-remediation
  gate=2      2026-07-29_0840_audit-remediation
  NO_CLOSEOUT  2026-07-29_1021_adversarial-gate-population
  gate=0      2026-07-30_0100_a2-auth-certification-of-m3-remediation
  gate=2      2026-07-30_0500_final-publication-of-v1.1-certification
  gate=0      2026-07-30_0700_claude-skills-discovery-01

conformant : 2
failing    : 10
closeoutless: 1
AGGREGATE_VERDICT: FAIL
POC_EXIT=2
```

## Verdict

**Verdict: GO**

## Ce que le POC a appris au-delà de son critère

Trois observations de conception, non anticipées à l'intake :

1. **Le run courant entre dans sa propre population.**
   `2026-07-29_1021` est post-cutoff et n'a pas de closeout : compté comme échec,
   il rendrait le gate impossible à satisfaire pendant l'exécution de tout run.
   La population gatée doit donc être *« runs post-cutoff clôturés »* ; un run
   ouvert est `OUT_OF_SCOPE`, pas `NON_CONFORMANT`. C'est le même piège que
   `--latest` en miroir : une sémantique de sélecteur importée dans un gate.

2. **`undatable identities: 0`** — les 161 répertoires ont tous une identité
   parsable. La borne cutoff est donc totalement ordonnante sur la population
   réelle, sans cas de repli sur `mtime`. Le risque F8 (dérive temporelle) affecte
   *quels* runs sont post-cutoff, pas la capacité à trancher.

3. **La population post-cutoff est de 13, pas 12.** L'audit initial en comptait 12
   parce qu'il énumérait à la main. L'écart est ce run lui-même. Une énumération
   dérivée de la donnée est déjà plus fiable que l'énumération qui a servi à
   fonder le finding.
