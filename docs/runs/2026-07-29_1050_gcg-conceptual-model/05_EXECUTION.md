---
run_id: "2026-07-29_1050_gcg-conceptual-model"
phase: "05_EXECUTION"
voie: "STRUCTUREE"
status: "PARTIAL"
agent: "claude-opus-5 (Claude Code)"
started_at: "2026-07-29T08:50:00Z"
ended_at: "2026-07-29T09:25:00Z"
artifacts_produced:
  - "docs/REFERENCE/governance-compatibility-model.md"
---

# 05_EXECUTION — GCG-MODEL-01

## 1. `C1` — la frontière normative n'est plus dérivée

Avant : une constante unique, `ADVERSARIAL_ENFORCEMENT_BIRTH`, dont la valeur
provenait d'une archéologie git (quel commit a ajouté `vbb-adversarial-gate.py`
→ quel run l'a produit).

Après : deux bornes déclarées, et une preuve.

```
applies_from                : 2026-07-28_1400
enforcement_effective_from  : 2026-07-28_2000
enforcement_evidence        : commit 921a780c… (preuve d'implémentation)
```

Le gain n'est pas cosmétique. La dérivation reposait sur un mapping établi par
lecture d'artefacts — signalé comme incertitude résiduelle dans le closeout de
`1021` : *« si ce mapping est faux, quatre runs franchissent la frontière dans
le sens permissif »*. Une borne déclarée n'a pas cette propriété.

## 2. La distinction que la correction a fait apparaître

Formaliser la déclaration a révélé que **deux bornes distinctes** étaient
confondues en une seule :

- `applies_from` — l'obligation existe ;
- `enforcement_effective_from` — un mécanisme peut la vérifier.

Elles ne coïncident jamais : une règle est écrite, puis outillée. L'intervalle
entre les deux est la **fenêtre de dette** : la seule zone où une disposition de
dette est admissible.

C'est la formulation canonique de la règle anti-blanchiment, qui n'existait
jusqu'ici qu'en code. Elle est plus forte : la fenêtre est bornée et immuable
une fois la règle publiée, donc rien de produit aujourd'hui ne peut y entrer.

## 3. `C2` — `PENDING_LIFECYCLE` et son garde manquant

Le renommage a exposé un défaut réel. `OUT_OF_SCOPE` n'avait **aucune limite** :
la condition d'attribution était l'absence de closeout, mais rien n'empêchait
d'élargir la catégorie à « en attente d'une étape ultérieure ».

Or un run clos qui échoue faute de revue indépendante *est* en attente d'une
étape ultérieure. Sans limite, `2026-07-29_0840` et `2026-07-29_1021` — deux runs
`CURRENT_NONCOMPLIANCE` — auraient pu se déclarer en attente et cesser de
bloquer.

Limite retenue : la catégorie s'applique **uniquement quand l'artefact porteur
de la preuve n'existe pas encore**. Si la preuve existe et est insuffisante,
c'est un défaut. Test de discrimination inscrit dans le modèle §4.1 et porté par
`test_pending_lifecycle_never_covers_an_existing_failing_artifact`.

## 4. `C3` — séparation des responsabilités

Formalisée dans le modèle §2 : Scanner (observe) → Arbitration (décide, humaine)
→ Migration Engine (applique). La docstring du scanner déclare désormais son
rôle et l'invariant `I7`.

Le scanner respectait déjà la lecture seule ; ce qui manquait était la
déclaration explicite qu'aucun composant ne doit observer, juger et modifier
simultanément.

## 5. Vérification d'absence d'écart

| Élément du modèle | Porteur exécutable |
|---|---|
| Fenêtre de dette bornée des deux côtés | `test_debt_window_is_bounded_on_both_sides` |
| `I2` ledger non blanchissant | `test_ledger_cannot_launder_a_post_enforcement_run` |
| `I4` certification non dérivable | `test_certification_is_never_derived_from_the_gate` |
| `I5` OVERCLAIM prime sur l'historique | `test_overclaim_outranks_the_historical_reading` |
| `I6` limite stricte de `PENDING_LIFECYCLE` | `test_pending_lifecycle_never_covers_an_existing_failing_artifact` |
| `I1`, `I3`, `I7`, `I8` | **aucun** — déclarés dans le modèle §5, sans porteur |

Les quatre invariants sans porteur sont signalés comme tels dans le modèle. Un
invariant sans test est une intention ; le run ne prétend pas l'inverse.

## 6. Mesure inchangée

Le renommage et la redéclaration ne modifient aucun verdict :

```
current conformance : 2/13
verdict             : FAIL  (exit 2)
```

C'était l'objet du contrôle : une correction de modèle qui changerait la mesure
signalerait que le modèle n'était pas une reformulation mais une révision.

## 7. Écarts au plan

- **Migration Engine non implémenté** — délibéré. Un moteur sans ledger n'aurait
  d'autre source que le jugement de l'agent, ce que l'invariant `I1` interdit.
- **Contrôle de démarrage de session non implémenté** — spécifié (§6 du modèle),
  y compris la mise en cache et le refus d'ouvrir un run automatiquement.
- **`G7` non traité** — reporté sur décision explicite.
