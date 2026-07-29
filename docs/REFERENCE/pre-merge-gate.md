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
| 4 | `python tools/vbb-loop-closure-check.py <run_id> --strict` | Closure invariant satisfied |
| 5 | `pytest tests/ -q && bash scripts/vbb-ci-local.sh` | Test suite + local CI pass |
| **5b** *(adversarial — ADR 0051)* | **`python tools/vbb-adversarial-gate.py <run_id> --strict && python -m pytest tests/adversarial_corpus/ -q`** | Adversarial validator + adversarial corpus execution as a **separately reported** check. **Distinct from command 5.** |

`<run_id>` désigne partout l'identifiant nu du run (`2026-07-29_0840_audit-remediation`),
jamais un chemin. Les deux outils résolvent le chemin eux-mêmes.

### Liaison exacte pour une preuve de release

Le bloc P.R2 emploie déjà un run explicite. Lorsqu'il sert de preuve pour une
release ou une certification, le SHA attendu est également obligatoire et doit
correspondre au `certification.bound_to.commit` du closeout :

```bash
RUN_ID=<run_id>
EXPECTED_COMMIT=<full-40-character-git-sha>

python tools/vbb-loop-closure-check.py "$RUN_ID" \
  --expected-commit "$EXPECTED_COMMIT" --strict && \
python tools/vbb-adversarial-gate.py "$RUN_ID" \
  --expected-commit "$EXPECTED_COMMIT" --strict
```

`--expected-commit` refuse l'auto-sélection et un SHA différent. Sans ces deux
arguments explicites, une exécution reste un diagnostic ou un contrôle de run ;
elle ne constitue pas une preuve de release liée à un état Git.

En mode certification, les deux gates imposent la même égalité stricte :
`certification.bound_to.commit == --expected-commit == HEAD` évalué. La
résolution d'un commit historique reste consultable par le helper Core mais ne
peut produire aucun verdict de certification.

## Bloc shell canonique

```bash
RUN_ID=<run_id>

python tools/vbb-architecture.py lint && \
python tools/vbb-architecture.py graph --write && \
python tools/vbb-contract-lint.py && \
python tools/vbb-loop-closure-check.py "$RUN_ID" --strict && \
python tools/vbb-adversarial-gate.py "$RUN_ID" --strict && \
python -m pytest tests/adversarial_corpus/ -q && \
python -m pytest tests/ -q && \
bash scripts/vbb-ci-local.sh
```

Ce bloc est **exécutable tel quel** : il se copie-colle après avoir renseigné
`RUN_ID`. Toute ligne qui ne s'exécute pas n'appartient pas à ce bloc.

Toutes les lignes passent par le **même interpréteur** (`python -m pytest`,
jamais `pytest` nu). Le raccourci `pytest` résout vers le premier shim du `PATH`,
qui n'est pas nécessairement l'interpréteur exécutant les autres lignes : sur un
poste où `python` est 3.11 et `pytest` un shim 3.13, le bloc échouait sur un
`ModuleNotFoundError: No module named 'yaml'` sans aucun rapport avec l'état du
dépôt (audit 2026-07-29, finding F20).

> **Historique.** Jusqu'au 2026-07-29, les deux lignes `5b` étaient encadrées par
> `[ "$(adversarial_governance_cutoff_state)" = "pre-cutoff" ]`. Cette fonction
> n'a jamais existé dans le dépôt : la substitution échouait, la comparaison était
> fausse, et la chaîne `&&` s'interrompait quel que soit l'état. Le bloc dit
> « canonique » n'a donc jamais pu être exécuté (audit 2026-07-29, finding F5).
> Le cutoff `2026-07-28_1400` étant dépassé, `5b` est désormais inconditionnel et
> la conditionnalité ascendante (cf. ADR 0050 §Compatibility) ne concerne plus que
> les runs historiques, qui ne sont pas rejoués.

### Corpus vide

`pytest tests/adversarial_corpus/ -q` retourne 0 quand le corpus est vide : c'est
un état légitime tant qu'aucun finding `CONFIRMED` n'est en attente
(`tests/adversarial_corpus/conftest.py`). L'obligation « tout finding CONFIRMED
possède une entrée de corpus » est portée par `tests/test_corpus_mandatory.py`,
exécuté par la commande 5, et non par le code de sortie de cette commande.

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
