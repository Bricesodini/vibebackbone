---
template_id: "POC"
version: "1.0"
lane_eligible:
  - "STRUCTUREE"
  - "AUDIT"
related:
  - "docs/templates/ADR.md.template"
  - "docs/CONVENTIONS.md#pr3--gate-before-action"
---

# POC — vbb-doc-v1 external adoption on Backbone Know

**Statut**: CONCLUDED
**Date**: 2026-07-31
**Liée à ADR**: aucune (non requis)
**Liée à RUN**: `docs/runs/2026-07-31_vbb-doc-v1-external-pilot/`

## Hypothèse

Nous supposons que la convention `vbb-doc-v1` v1.0, telle que publiée dans
`docs/DOCUMENT_CONVENTION.md`, suffit à un dépôt tiers (Backbone Know)
pour comprendre, adopter et appliquer la convention sans accompagnement
oral, sous réserve que le linter canonique soit exécuté et qu'un périmètre
représentatif de 5 documents soit migré.

## Test (concret, exécutable)

Le test est le pilote lui-même, exécuté dans un worktree isolé de
Backbone Know :

```bash
# 1. Création du worktree
git -C /Users/bricesodini/02_dev/Backbone-know worktree add \
  ../backbone-know-pilot -b pilot/vbb-doc-v1-external main

# 2. Phase 1 : inventaire de la doc Backbone Know (lecture seule)
#    → evidence/phase1_inventory.md

# 3. Phase 2 : adoption minimale
#    a) Déclaration d'adoption
echo "document_convention: vbb-doc-v1
version: \"1.0\"
adoption: adopted
scope:
  roots:
    - docs/DOCUMENT_CONVENTION.md
    - docs
  excludes:
    - docs/archive
  historical_before: \"2026-07-31\"" > .vbb/document-convention.yaml
#    b) Copie de la convention et du linter depuis Vibe Backbone
cp /Users/bricesodini/01_ai-stack/vibebackbone/docs/DOCUMENT_CONVENTION.md \
   docs/DOCUMENT_CONVENTION.md
cp /Users/bricesodini/01_ai-stack/vibebackbone/tools/vbb-document-convention-lint.py \
   tools/vbb-document-convention-lint.py
#    c) Migration des 5 documents représentatifs
#    d) Exécution du linter
python3 tools/vbb-document-convention-lint.py .

# 4. Sortie capturée et classifiée
#    → evidence/phase2_linter_output.txt
#    → evidence/phase2_frictions.md (par catégorie)
```

## Critère de réussite (mesurable)

- **GO** si verdict final ∈ {`PILOT_PASS`, `PILOT_PASS_WITH_REVISIONS`},
  c'est-à-dire si l'adoption est possible sans accompagnement oral au-delà
  des corrections documentées comme findings.
- **NO-GO** si verdict final = `PILOT_FAIL`, c'est-à-dire si une friction
  `V1_BLOCKER` empêche l'adoption fiable.
- **PIVOT** non applicable ici (pas d'alternative au contrat v1.0 publiée).

## Résultat observé

- **Date d'exécution** : 2026-07-31
- **Sortie littérale** : à compléter au closeout dans `evidence/`
- **Métrique mesurée** : verdict final (PILOT_PASS /
  PILOT_PASS_WITH_REVISIONS / PILOT_FAIL) + nombre de frictions par
  catégorie.

## Décision

Verdict: GO

Le verdict pilote est `PILOT_PASS_WITH_REVISIONS`, ce qui satisfait le
critère GO de la POC : l'adoption est possible sans accompagnement oral
au-delà des corrections documentées comme findings (F-PH1-10, F-PH1-02,
F-PH1-07).

Décision complémentaire :

- **Verdict** : `GO` (formaté pour lisibilité humaine ; voir `Verdict: GO` ci-dessus pour la gate).
- **Justification** : la POC est tranchée après exécution complète du
  pilote sur Backbone Know.

## Bilan

- **Hypothèse validée partiellement** : la convention v1.0 peut être
  adoptée sans accompagnement oral **sur un périmètre représentatif
  minimal** (6 fichiers dans Backbone Know, linter PASS après une
  seule correction triviale). Trois révisions sont **bloquantes pour
  une Release Candidate** (F-PH1-10, F-PH1-02, F-PH1-07) et quatre
  améliorations peuvent attendre une version ultérieure (cf.
  [`03_DECISION.md`](03_DECISION.md)).
- **Verdict pilote** : `PILOT_PASS_WITH_REVISIONS`.
- **Verdict POC** : `GO` (au sens du critère de cette POC : adoption
  possible sans accompagnement oral au-delà des corrections
  documentées).
- **Suite** : un **run de remédiation canonique séparé** doit traiter
  les trois findings bloquants RC (F-PH1-10 adoption progressive,
  F-PH1-02 extension de domaine `status`, F-PH1-07 linter
  `--suggest-scope`) avant qu'une RC v1.1 ne soit publiée.

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: GO
adr_link: null
hypothesis_validated: partial
metric_observed: "PILOT_PASS_WITH_REVISIONS"
metric_threshold: "verdict ∈ {PILOT_PASS, PILOT_PASS_WITH_REVISIONS}"
reproducible: true
verified_at: "2026-07-31T11:30:00Z"
verified_by: "pi"
```