---
run_id: "2026-08-03_f03-provenance-alignment"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-08-03T00:00:00Z"
ended_at: null
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "04_PLAN.md"

implementation_authorization:
  status: "NOT_AUTHORIZED"
  required_gate_ids: ["f03-provenance-validation"]
  reasons:
    - "Le run est limité à l’observation et à la preuve; aucune écriture de candidat n’est autorisée."

adr_status:
  adr: "docs/adr/0053-a2-a3-assurance-alignment.md"
  verdict: "PASS"

poc_status:
  poc: "POC.md"
  verdict: "GO"
---

# 04_PLAN — F-03 Provenance Alignment

## Objectif

Démontrer que la provenance observée conserve 0051 comme fondation historique
et rattache explicitement la gouvernance v1.2 à 0053, sans réécriture rétroactive.

## Étapes bornées

| # | Action | Validation | Rollback |
|---|---|---|---|
| 1 | Capturer les identités, références et hashes des quatre représentations | `sha256sum`, `readlink`, recherches ciblées | Aucune écriture; supprimer uniquement les preuves du run si autorisé |
| 2 | Comparer ADR-0051, ADR-0053 et la gouvernance v1.2 | assertions textuelles et provenance | Aucune modification de source |
| 3 | Vérifier la projection `SYSTEM.md` | `readlink`, hash source/projection | Aucune modification de source |
| 4 | Rejouer les validateurs concernés | adversarial gate, architecture/contract/convention lint applicables | Conserver tout échec comme preuve |

## Critères d’acceptation

- [ ] 0051 est décrit comme fondation historique, sans réécriture.
- [ ] 0053 est la référence explicite de l’alignement v1.2.
- [ ] La gouvernance v1.2 porte `adr: "0053"`.
- [ ] `SYSTEM.md` et sa source Pi sont identiques par résolution symlink.
- [ ] Aucun candidat documentaire n’est modifié.
- [ ] F-03 est soit démontré cohérent, soit laissé ouvert avec cause exacte.

## Analyse d’impact

- **Effectuée ?** : NON (justifié : run de validation de provenance borné, sans
  modification architecturale ni changement de comportement).
- **Périmètre d’impact** : ADR-0051, ADR-0053, gouvernance adversariale v1.2,
  représentation Pi de `SYSTEM.md`.
- **Risques d’effet de bord** : confusion historique/fondation si 0051 est
  présenté comme l’autorité v1.2; rupture de projection si le symlink diverge.
