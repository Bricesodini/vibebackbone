---
load_policy: reference
canonical: true
referenced_by:
  - AGENTS.md §Closeout Checklist
  - AGENTS.md §Pre-merge Gate Checklist
  - SYSTEM.md §Quality conventions
  - docs/CONVENTIONS.md Pillar 3 §Verification loop
  - docs/CONVENTIONS.md Pillar 5 §P.R2
  - docs/PILOTAGE.md §Quality standards
  - docs/AGENTIC_RUN_PROTOCOL.md
context_role: pre-merge-gate-canon
phase: transverse
status: active
---

# Pre-Merge Gate — Reference (canon unique du bloc P.R2)

> **Source unique de vérité** pour la séquence des 5 vérifications obligatoires
> avant tout `FINAL_STATUS=COMPLETE`. Ce fichier est `reference-only` :
> les autres docs citent ce chemin, elles ne reproduisent pas le bloc.

## Les 5 vérifications (5 P.R2 obligatoires)

À exécuter **dans cet ordre exact** avant tout `FINAL_STATUS=COMPLETE` :

| # | Commande | Ce qu'elle vérifie |
|---|----------|--------------------|
| 1 | `python tools/vbb-architecture.py lint` | `docs/ARCHITECTURE.md` blocks valid |
| 2 | `python tools/vbb-architecture.py graph --write` | `docs/RELATIONS.md` regenerated |
| 3 | `python tools/vbb-contract-lint.py` | Published contracts lint clean |
| 4 | `python tools/vbb-loop-closure-check.py <run> --strict` | Closure invariant satisfied |
| 5 | `pytest tests/ -q && bash scripts/vbb-ci-local.sh` | Test suite + local CI pass |
| **5b** *(adversarial — ADR 0051)* | **`python tools/vbb-adversarial-gate.py <run> --strict && python -m pytest tests/adversarial_corpus/ -q`** | Adversarial validator + adversarial corpus execution as a **separately reported** check. **Distinct from command 5.** |

## Bloc shell canonique

```bash
python tools/vbb-architecture.py lint && \
python tools/vbb-architecture.py graph --write && \
python tools/vbb-contract-lint.py && \
python tools/vbb-loop-closure-check.py <run_id> --strict && \
( python tools/vbb-adversarial-gate.py <run_id> --strict || [ "$(adversarial_governance_cutoff_state)" = "pre-cutoff" ] ) && \
( python -m pytest tests/adversarial_corpus/ -q || [ "$(adversarial_governance_cutoff_state)" = "pre-cutoff" ] ) && \
pytest tests/ -q && \
bash scripts/vbb-ci-local.sh
```

Les deux lignes intermédiaires (`5b` — adversarial) sont conditionnelles
au cutoff `2026-07-28_1400`. Avant le cutoff, le bloc retourne code 0
même si les deux lignes sont sautées ; après le cutoff, elles sont
obligatoires. Cette conditionnalité préserve la compatibilité
ascendante (cf. ADR 0050 §Compatibility).

## Règles d'application

- **Échec d'une commande** → STOP, ne pas marquer `FINAL_STATUS=COMPLETE`.
- Documenter l'échec dans `07_CLOSEOUT.md` §Points ouverts, fixer en scope, puis
  re-run la boucle.
- Le flag `--strict` sur `vbb-loop-closure-check.py` retourne exit code 2
  (`GATE_BLOCKED`) sur FAIL — c'est le signal explicite que `COMPLETE` est interdit.
- Pour les routes **FAST-MINIMAL / FAST-ZERO** : SKIP de la boucle. La closeout
  doit déclarer la voie explicitement.
- Pour les routes **FAST-STANDARD / STRUCTURED / AUDIT / CLOSEOUT** : exécution obligatoire.

## Couverture par gate-check

Le `vbb-gate-check.py` (ADR+POC+Integration Gate, voir
`AGENTS.md` Critical Rule #11 et `tools/vbb-gate-check.py`) **précède** la
boucle P.R2 : il valide qu'un chantier peut démarrer (ADR + POC + Integration)
avant que la boucle P.R2 ne valide qu'un chantier peut se clore.

## Renvois

- `AGENTS.md` §Closeout Checklist
- `AGENTS.md` §Pre-merge Gate Checklist (CANON)
- `SYSTEM.md` §Quality conventions
- `docs/CONVENTIONS.md` Pillar 3 §Verification loop
- `docs/CONVENTIONS.md` Pillar 5 §P.R2
- `docs/PILOTAGE.md` §Quality standards
