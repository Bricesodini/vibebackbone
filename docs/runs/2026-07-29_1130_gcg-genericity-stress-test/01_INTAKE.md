---
run_id: "2026-07-29_1130_gcg-genericity-stress-test"
phase: "01_INTAKE"
voie: "STRUCTUREE"
status: "PARTIAL"
kind: "GOVERNANCE_MODEL_VALIDATION"
adversarial_level: "A2"
scope_id: "GCG-STRESS-01"
agent: "claude-opus-5 (Claude Code)"
knowledge_governance_version: "1.0"
assurance_governance_version: "1.0"
adversarial_governance_version: "1.1"
adr_link: "docs/adr/0051-adversarial-assurance-dimension.md"
started_at: "2026-07-29T09:30:00Z"
ended_at: null
next_phase: "04_PLAN"
artifacts_consumed:
  - "docs/REFERENCE/governance-compatibility-model.md (PROPOSED)"
  - "docs/runs/2026-07-29_1021_adversarial-gate-population/"
  - "docs/runs/2026-07-29_1050_gcg-conceptual-model/"
artifacts_produced:
  - "01_INTAKE.md (this file)"
  - "04_PLAN.md"
  - "02_STRESS_TEST.md"
  - "05_EXECUTION.md"
  - "07_CLOSEOUT.md"
  - "docs/REFERENCE/governance-compatibility-model.md (révision v2)"
---

# 01_INTAKE — GCG-STRESS-01

## 1. Demande reçue

Valider la généricité du *Governance Compatibility Gate* avant toute poursuite
de l'implémentation. Réaliser un stress test conceptuel en appliquant le modèle
à **au moins une deuxième règle de gouvernance, indépendante de la campagne
adversariale**.

Objet du test : déterminer si les concepts introduits — Scanner, Arbitration,
Migration Engine, Governance Compatibility Act, `OVERCLAIM`,
`applies_from` / `enforcement_effective_from` — constituent un modèle générique
ou restent spécialisés sur la dimension adverse.

Attendu : un verdict argumenté sur la robustesse, et si nécessaire une version
révisée avant de considérer le modèle comme canonique.

## 2. Contraintes normatives déclarées

| # | Contrainte | Portée |
|---|---|---|
| C1 | **Ne pas écrire de code.** Le but est conceptuel. | tout le run |
| C2 | **Ne pas rédiger l'ADR 0052.** | tout le run |
| C3 | **Ne pas poursuivre l'implémentation** (Migration Engine, ledger, câblage CI) tant que la validation n'est pas concluante. | tout le run |
| C4 | Si le modèle révèle des limites → le faire évoluer. S'il tient → **justifier pourquoi**, pas seulement l'affirmer. | livrable |

C1 est structurante : un défaut découvert dans `tools/vbb-governance-compat.py`
sera **enregistré et opposable**, pas corrigé. Corriger ici invaliderait le test
— on ne mesure pas un instrument en le réglant pendant la mesure.

## 3. Méthode

Le risque d'un stress test conceptuel est de choisir une deuxième règle
suffisamment proche de la première pour que le modèle tienne par construction.
La méthode l'écarte explicitement : les règles candidates sont choisies pour
**maximiser la distance structurelle**, et l'application est **mesurée** sur le
dépôt réel, jamais raisonnée sur des exemples fabriqués.

Quatre règles indépendantes de la dimension adverse, ordonnées par distance
croissante à la règle d'origine :

| Règle | Source | Population | Distance |
|---|---|---|---|
| **A** adversarial-assurance 1.1 | ADR 0051 | runs | *référence* |
| **B** engineering-knowledge 1.0 | ADR 0049 | runs | même population, obligation différente |
| **C** exact seven-section skill layout | ADR 0042 | skills | population non datée, **mutable** |
| **D** credentials enforcement | ADR 0033 | lignes ajoutées d'un diff | **pas une population** — un flux |

Critère de réussite : le modèle est générique s'il classe correctement B, et
s'il **déclare son inapplicabilité** sur C et D au lieu de produire une
classification fausse. Un modèle qui répond à tout ne discrimine rien.

## 4. Baseline mesurée avant le test

Acte de compatibilité courant, règle A (`vbb-governance-compat.py --json`) :

```
population_total       : 162
population_applicable  : 14
current_conformance    : 2/14
counts                 : HISTORICAL_VALID 148 · CURRENT_NONCOMPLIANCE 7
                         UNKNOWN 4 · CURRENT 2 · OVERCLAIM 1
verdict                : FAIL
```

`vbb-contract-lint.py` : 0 error, 1 warning (F12). Suite de tests verte au
commit `f7e21a3`.

## 5. Niveau adverse

`A2` — le sujet est le canon de gouvernance lui-même. `A2_DISTINCT_AGENT_PROXY`
n'est pas satisfait : l'agent qui éprouve le modèle est celui qui l'a écrit.
C'est la limite principale de ce run et elle est déclarée au closeout, pas
compensée.
