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

# POC — memory-authority-seam

**Statut**: CONCLUDED
**Date**: 2026-08-26
**Liée à ADR**: docs/adr/0055-memory-authority-seam.md
**Liée à RUN**: docs/runs/2026-08-26_2105_memory-authority-seam/

## Hypothèse

Nous supposons que la frontière d'autorité de l'ADR 0055 est **falsifiable de
façon déterministe et model-free**, c'est-à-dire qu'un vérificateur sans LLM peut
accepter un vault conforme et rejeter chacun des six cas adversariaux T1–T6 avec
un code d'erreur stable — sans disposer de l'implémentation Backbone Memory.

## Test (concret, exécutable)

```bash
cd docs/runs/2026-08-26_2105_memory-authority-seam/poc

# 1. Banc complet : vault conforme + les six cas adversariaux
python3 seam_check.py --selftest

# 2. T5 en deux temps : destruction, reconstruction depuis le canon seul
python3 seam_check.py --canon fixtures/canon --vault fixtures/vaults/t5_vault_destroyed.json
python3 seam_check.py --canon fixtures/canon --rebuild > /tmp/rebuilt.json
python3 seam_check.py --canon fixtures/canon --vault /tmp/rebuilt.json --answers

# 3. C7 : les trois questions, pour chaque entrée
python3 seam_check.py --canon fixtures/canon --vault fixtures/vaults/conformant.json --answers
```

Dépendances : Python 3, bibliothèque standard uniquement. Aucun LLM, aucun
réseau, aucun accès à Backbone Memory. Le canon de test est un arbre de cinq
artefacts à frontmatter plat ; le vault de test est un tableau JSON.

## Critère de réussite (mesurable)

GO si : le vault conforme sort en `exit=0` **et** les six cas adversariaux
sortent en `exit=1` en levant chacun son code attendu (6/6), **et** le
round-trip T5 (destruction → reconstruction depuis le canon → re-vérification)
repasse en `exit=0`, **et** les trois questions de C7 sont émises pour 100 % des
entrées.

## Résultat observé

- **Date d'exécution** : 2026-08-26 21:35

- **Sortie littérale** — banc complet :

```
VBB Memory Seam Check — selftest (ADR 0055 T1..T6)

  OK   conformant                         exit=0 codes=[]
  OK   t1_candidate_contradicts_canon     exit=1 codes=['CANDIDATE_CONTRADICTION_UNFLAGGED']
  OK   t2_projection_source_superseded    exit=1 codes=['PROJECTION_STALE_SUPERSEDED', 'REBUILD_DIVERGENCE']
  OK   t3_fact_without_source             exit=1 codes=['PROJECTION_WITHOUT_SOURCE']
  OK   t4_incompatible_candidates         exit=1 codes=['CONFLICT_AUTO_RESOLVED']
  OK   t5_vault_destroyed                 exit=1 codes=['REBUILD_DIVERGENCE']
  OK   t6_direct_production_marking       exit=1 codes=['CANONICAL_CLAIM_IN_MEMORY']

SELFTEST PASS — the conformant vault passes and each of the six
adversarial cases fails with its expected code.
[exit 0]
```

- **Sortie littérale** — T5 en deux temps :

```
=== T5a : vault détruit
  REBUILD_DIVERGENCE   art_db_choice        canon artifact has no projection
  REBUILD_DIVERGENCE   art_export_v2        canon artifact has no projection
  REBUILD_DIVERGENCE   art_shopping_list    canon artifact has no projection
  REBUILD_DIVERGENCE   art_ui_stack         canon artifact has no projection
VERDICT: FAIL   [exit 1]

=== T5c : re-vérification du vault reconstruit
canon: 5 artifact(s) | vault: 4 entry(ies)
VERDICT: PASS   [exit 0]
```

Le canon compte cinq artefacts et la reconstruction en produit **quatre** :
`art_export_v1`, supersédé, ne projette rien. La supersession est donc portée par
le canon et suivie par la projection, jamais décidée par la mémoire.

- **Sortie littérale** — C7, réponses mécaniques :

```
  p_art_db_choice      projection  repo   canon:art_db_choice       none (rebuildable)
  p_art_export_v2      projection  repo   canon:art_export_v2       none (rebuildable)
  p_art_shopping_list  projection  repo   canon:art_shopping_list   none (rebuildable)
  p_art_ui_stack       projection  repo   canon:art_ui_stack        none (rebuildable)
```

- **Métrique mesurée** : conforme `exit=0` ; **6/6** cas adversariaux rejetés
  avec le code attendu ; round-trip T5 `FAIL → rebuild → PASS` ; C7 émis pour
  **100 %** des entrées (seuil attendu : 6/6, round-trip vert, 100 %).

### Démonstration d'échec (fail-before)

Le banc a effectivement échoué avant de réussir, deux fois, et les deux échecs
sont instructifs :

1. Les fixtures canoniques initiales n'avaient pas de `---` de fermeture : le
   parseur a rejeté chaque artefact (`fixture error: … has no id`) et le banc
   s'est arrêté. Un vérificateur qui aurait *toléré* un frontmatter malformé
   aurait silencieusement considéré le canon comme vide — donc accepté n'importe
   quel vault. Le comportement fail-closed du parseur est une propriété, pas un
   accident.
2. Chaque cas Tn a été exécuté et **doit** échouer : le `--selftest` compare le
   code de sortie *et* le code d'erreur attendu. Un contrôle incapable
   d'échouer serait signalé `BAD` par le banc lui-même.

## Décision

- **Verdict** : GO
- **Justification** : la couture est vérifiable sans LLM, sans réseau et sans
  l'implémentation candidate ; les six cas adversariaux sont discriminés avec des
  codes stables et le round-trip de reconstruction est vert.

## Bilan

Hypothèse validée → l'ADR 0055 peut passer `ACCEPTED`, **amendé** par les cinq
points ci-dessous, que la construction du banc a révélés. Chacun est un endroit
où le contrat était sous-spécifié : l'implémenteur aurait dû trancher seul, ce
qui est précisément la porte d'entrée d'une vérité parallèle.

| # | Amendement | Découvert en construisant | Code du vérificateur |
|---|---|---|---|
| **A1** | Tout `candidate` déclare un `subject_key` | sans clé de sujet, la contradiction avec le canon n'est pas détectable model-free — il faudrait de la sémantique | `CANDIDATE_WITHOUT_SUBJECT_KEY` |
| **A2** | Un artefact canonique supersédé **ne projette rien** | T2 : le contrat disait « suit la source ou est invalidée », deux comportements incompatibles | `PROJECTION_STALE_SUPERSEDED` |
| **A3** | `working` n'est ni promouvable ni porteur de source | implicite dans C2/C3, non énoncé comme règle vérifiable | `WORKING_PROMOTED`, `WORKING_WITH_SOURCE` |
| **A4** | Les réponses attendues de C7 sont fixées par classe | C7 posait les trois questions sans fixer les réponses admissibles | table C7 + `C7_UNANSWERABLE` |
| **A5** | Une promotion exige une autorisation **humaine** explicite et traçable | « provenance exploitable » n'était pas vérifiable en l'état | `PROMOTION_WITHOUT_AUTHORIZATION` |

Réserves connues, à porter dans l'audit architectural (I2) :

- La détection de contradiction est **par clé de sujet déclarée**. Deux
  formulations différentes du même fait sous deux clés distinctes ne seront pas
  détectées : c'est le prix du model-free, et c'est une limite à documenter, pas
  un défaut à masquer.
- Le banc éprouve la **couture**, pas une implémentation. Il ne dit rien de la
  conformité de Backbone Memory : c'est l'objet de l'audit architectural, qui
  consistera à faire produire par le kernel un export au format vault et à le
  passer dans ce même vérificateur.
- Le prototype vit dans le dossier de run. Sa promotion en `tools/` avec tests
  associés est un pas d'implémentation, soumis à la gate.

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS: GO
adr_link: docs/adr/0055-memory-authority-seam.md
hypothesis_validated: true
metric_observed: "conformant exit=0 ; 6/6 adversarial rejected with expected code ; T5 round-trip FAIL→rebuild→PASS ; C7 emitted for 100% of entries"
metric_threshold: "6/6 adversarial rejected ; round-trip green ; C7 100%"
reproducible: true
verified_at: "2026-08-26T21:35:00Z"
verified_by: "agent"
```
