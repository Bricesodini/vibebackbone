---
run_id: "2026-07-27_2145_design-certification-gates-core-integration"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "codex"
started_at: "2026-07-27T19:49:00Z"
ended_at: "2026-07-27T19:50:00Z"
next_phase: "05_EXECUTION"
artifacts_consumed:
  - "01_INTAKE.md"
  - "02_AUDIT.md"
  - "docs/adr/0050-design-certification-assurance-schema.md"
  - "POC.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — Design/Certification gate Core integration

## Objectif

Activer le schéma canonique d'assurance v1 sans casser les runs historiques ni
modifier de projet consommateur.

## Pré-conditions

- ADR 0050 `ACCEPTED`.
- POC `GO`.
- Décision humaine `APPROVED`.
- `vbb-gate-check.py` doit rendre `can_code_start=true`.

## Étapes ordonnées

1. Ajouter l'autorité canonique et mettre à jour pilotage, protocole,
   architecture et journal de propagation.
2. Enrichir les templates et prompts de run, review et closeout.
3. Ajouter l'enforcement cutoff-aware et les tests de compatibilité.
4. Régénérer les relations et exécuter les gates.
5. Obtenir une revue indépendante; remédier ou bloquer selon son verdict.
6. Closeout avec Knowledge Harvest, puis commit/push uniquement sur PASS.

## Critères d'acceptation

- [ ] `DESIGN` et `CERTIFICATION` sont canoniques; `PASS/FAIL` sont conservés.
- [ ] `FINAL_STATUS` et `ASSURANCE_STATUS` restent orthogonaux.
- [ ] L'autorisation est explicite et fail-closed.
- [ ] Les reviews ont deux profils distincts.
- [ ] Le closeout est déterministe et conserve Knowledge Harvest.
- [ ] Les runs historiques restent valides sans réécriture.
- [ ] Pi/OpenCode/Codex/Claude héritent d'une règle Core unique.
- [ ] Revue indépendante PASS et P.R2 PASS.

## Rollback

Revert atomiquement autorité, prompts/templates, enforcement, tests et graphe.
Ne jamais conserver l'enforcement sans son autorité canonique.

## Risques identifiés

- Mauvaise reclassification d'un finding substantif : règle de réouverture
  Design et revue dédiée.
- Autorisation inférée : record explicite et validator fail-closed.
- Régression historique : cutoff objectif et fixtures legacy.
- Divergence distributions : règle unique dans Core et smoke quatre runtimes.

## Analyse d'impact

- **Effectuée** : OUI via `t-vbb-impact-analyzer`.
- **Classification** : CONDITIONAL avant gate; NON_BREAKING si tous les
  invariants et tests sont satisfaits.
- **UNKNOWN** : consommateurs externes non publiés.

## Integration Gate

- **ADR référencé** :
  `docs/adr/0050-design-certification-assurance-schema.md`
- **POC référencé** :
  `docs/runs/2026-07-27_2145_design-certification-gates-core-integration/POC.md`
- **ADR_REQUIRED** : Y
- **POC_REQUIRED** : Y
- **CAN_CODE_START** : attente du calcul automatique.
