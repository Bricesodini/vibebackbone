---
template_id: "POC"
version: "1.0"
lane_eligible:
  - "STRUCTUREE"
---

# POC — audit-remediation

**Statut**: CONCLUDED
**Date**: 2026-07-29
**Liée à ADR**: docs/adr/0051-adversarial-assurance-dimension.md
**Liée à RUN**: docs/runs/2026-07-29_0840_audit-remediation/

## Hypothèse

Nous supposons que les gates audités sont **fail-open par construction** — ils
rendent un verdict positif sur un défaut qu'ils prétendent couvrir — et qu'une
règle bidirectionnelle sur une population canonique explicite suffit à les rendre
capables d'échouer, sans modifier les contrats existants.

## Test (concret, exécutable)

Trois expériences reproductibles. La troisième a été découverte pendant
l'exécution et a produit un finding nouveau (F14), documenté §Résultat.

```bash
# EXP-1 — le lint est-il fail-open sur un skill canonique sans contrat ?
mkdir -p skills/zz-poc-fixture
cat > skills/zz-poc-fixture/SKILL.md <<'EOF'
---
name: zz-poc-fixture
description: POC fixture — canonical skill deliberately shipped without CONTRACT.yaml.
context_role: poc-fixture
phase: "transverse"
status: "active"
---
# zz-poc-fixture
## ROLE & POSTURE
## INPUT CONTRACT
## BLOCKING CONDITIONS
## SCOPE
## PROCESS
## OUTPUT CONTRACT
## VERDICT RULES
EOF
python tools/vbb-contract-lint.py; echo "exit=$?"
python tools/vbb-status-dashboard.py | grep -i "Skills\|Contracts"

# EXP-2 — la règle bidirectionnelle proposée détecte-t-elle le cas ?
# (prototype hors production : le gate interdit encore de modifier l'outil)
python3 - <<'PY'
from pathlib import Path
import yaml
SKILLS = Path("skills")
canon = {d.name for d in SKILLS.iterdir() if d.is_dir() and (d / "SKILL.md").exists()}
contracted = {d.name for d in SKILLS.iterdir() if d.is_dir() and (d / "CONTRACT.yaml").exists()}
indexed = {e["id"] for e in yaml.safe_load((SKILLS / "INDEX.yaml").read_text())["skills"]}
print("would_exit_nonzero =", bool((canon - contracted) or (canon - indexed)))
PY

rm -rf skills/zz-poc-fixture   # restauration obligatoire

# EXP-3 — l'état local masque-t-il des défauts que la CI voit ?
git clone --no-local . /tmp/vbbclone && cd /tmp/vbbclone && python -m pytest tests/ -q
```

## Critère de réussite (mesurable)

GO si les trois énoncés sont simultanément vrais :

1. EXP-1 : le lint actuel sort **exit 0** sur une population contenant un skill
   canonique sans contrat (fail-open démontré, pas supposé) ;
2. EXP-2 : le prototype sort `would_exit_nonzero = True` sur la même population ;
3. EXP-3 : la suite exécutée sur un clone frais diverge de la suite exécutée sur
   l'arbre de travail (preuve que la méthode de détection est nécessaire).

NO-GO si le lint échouait déjà sur EXP-1 : l'hypothèse de fail-open serait fausse
et le plan de remédiation devrait être rebâti.

## Résultat observé

- **Date d'exécution** : 2026-07-29 06:45–07:05

### EXP-1 — fail-open confirmé

```
lint exit=0
VBB Contract Linter — 0 error(s), 1 warning(s) found
  ✓ All contracts valid
║  Skills          : 67                           ║
║  Contracts       : 64/67 (96%)                  ║
```

Le lint déclare « All contracts valid » alors qu'un skill canonique vient d'être
ajouté sans contrat. Le dashboard enregistre la dégradation 97 % → 96 % et
**n'émet aucun signal d'échec** : la couverture est rendue comme une statistique,
pas comme un verdict.

### EXP-2 — la règle proposée détecte

```
canonical=67 contracted=64 indexed=64
  ERROR [2-vbb-adversarial-campaign] canonical skill has no CONTRACT.yaml
  ERROR [t-vbb-adversarial-corpus]   canonical skill has no CONTRACT.yaml
  ERROR [zz-poc-fixture]             canonical skill has no CONTRACT.yaml
  ERROR [2-vbb-adversarial-campaign] canonical skill is missing from INDEX.yaml
  ERROR [t-vbb-adversarial-corpus]   canonical skill is missing from INDEX.yaml
  ERROR [zz-poc-fixture]             canonical skill is missing from INDEX.yaml
would_exit_nonzero = True
```

La règle capture la fixture **et** les deux skills adversariaux réels du finding
F2. La définition de population (`répertoire de premier niveau de skills/
contenant un SKILL.md`) rend 66 skills réels et n'attrape aucun sous-répertoire
de templates.

Fixture supprimée après mesure ; `contract-lint` et dashboard revenus à
`64/66 (97%)`, arbre de travail propre.

### EXP-3 — divergence clone / arbre de travail, et finding nouveau

```
arbre de travail : 386 passed, 1 skipped
clone frais      : 1 failed, 385 passed, 1 skipped
  FAILED tests/test_corpus_mandatory.py::test_corpus_directory_exists
```

L'expérience destinée à valider une méthode a produit un défaut réel :
`tests/adversarial_corpus/` était un répertoire **vide et non suivi par git**,
donc absent de tout clone. Le test échouait sur **chaque run CI depuis
`3d2eeee`** — huit commits — tout en passant sur chaque poste de développement.

Vérification croisée sur l'API GitHub Actions : `vbb-contracts` en `failure` sur
`3d2eeee`, `b9084e2`, `479bef7`, `0b35ad0`, `d3f5c25`, `3f4d831`, `218a6fd`,
`f8850ca`. Dernier vert : `75953fc` (2026-07-28T08:39). Deux causes
indépendantes : `Ruff check` sur certains commits, `Pytest suite` sur les autres.

Ce finding est enregistré comme **F14** et corrigé hors de ce run par le commit
`a2a1d0a` (route FAST-MINIMAL), parce qu'il bloquait la vérification de tout le
reste.

- **Métrique mesurée** : 3 critères / 3 satisfaits (seuil attendu : 3/3)

## Décision

- **Verdict** : GO
- **Justification** : le fail-open est démontré par mesure et non par lecture, la
  règle proposée le capture sans faux positif sur les 66 skills réels, et la
  méthode de vérification par clone frais s'est révélée capable de trouver un
  défaut que huit closeouts consécutifs avaient manqué.

## Bilan

Trois enseignements pour le run aval :

1. **La preuve négative est la seule preuve utile ici.** EXP-1 aurait été invisible
   en lisant le code : le lint « passait ». Chaque durcissement du run devra être
   accompagné de sa fixture d'échec.
2. **La population soumise à contrat doit être déclarée dans le code**, pas
   seulement dans un run. EXP-2 ne fonctionne que parce que la définition est
   explicite et vérifiable.
3. **`pytest` sur l'arbre de travail n'est pas une preuve de CI.** La vérification
   par `git clone --no-local` doit devenir le geste par défaut avant tout closeout
   revendiquant un verdict. C'est la seule chose qui a séparé l'état local de
   l'état commité.

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: GO
adr_link: docs/adr/0051-adversarial-assurance-dimension.md
hypothesis_validated: true
metric_observed: "3/3 criteria satisfied"
metric_threshold: "3/3"
reproducible: true
verified_at: "2026-07-29T07:05:00Z"
verified_by: "agent"
side_finding: "F14 — tests/adversarial_corpus/ untracked; remote CI red for 8 commits; fixed out of run by a2a1d0a"
```
