---
template_id: "INTEGRATION_GATE"
version: "1.0"
lane_eligible: ["STRUCTUREE", "AUDIT"]
verifier: "tools/vbb-gate-check.py"
---

# INTEGRATION_GATE — 2026-07-27_1612_engineering-knowledge-governance

**Run**: `docs/runs/2026-07-27_1612_engineering-knowledge-governance/`
**Date**: 2026-07-27
**Voie**: AUDIT → STRUCTUREE
**Statut gate**: BLOCKED

## ADR Status

- **ADR référencé** : `docs/adr/0049-engineering-knowledge-governance.md`
- **Statut attendu** : `ACCEPTED`
- **Statut observé** : `PROPOSED`
- **Verdict** : `BLOCKED`

## Résultat automatique observé

Commande :

```bash
python tools/vbb-gate-check.py \
  docs/runs/2026-07-27_1612_engineering-knowledge-governance --json
```

Résultat utile :

```yaml
ADR_REQUIRED: true
ADR_PRESENT_AND_ACCEPTED: false
POC_REQUIRED: false
POC_PRESENT_AND_GO: true
CAN_CODE_START: false
BLOCKERS:
  - ADR_NOT_ACCEPTED
```

Le détecteur lexical ne rend pas le POC obligatoire pour cet intake, mais il
observe correctement son verdict `GO`. Le document ne lui attribue pas
l'obligation manuelle du plan.

## POC Status — précondition manuelle du plan

- **POC référencé** : `docs/runs/2026-07-27_1612_engineering-knowledge-governance/POC.md`
- **Verdict attendu** : `GO`
- **Verdict observé** : `GO`
- **Verdict manuel** : `PASS`
- **Contrôle explicite avant code** :

  ```bash
  rg -n "^\\- \\*\\*Verdict\\*\\*: GO$" \
    docs/runs/2026-07-27_1612_engineering-knowledge-governance/POC.md
  ```

  Exit `0` requis indépendamment du résultat lexical de
  `vbb-gate-check.py`.

## Human gate

- **Ouverture du run** : `APPROVED`
- **Validation du Core** : `PENDING`
- **Revue indépendante de connaissance** : `PENDING`

## Gates

- [x] **ADR_REQUIRED? → Y** — détecté automatiquement.
- [ ] **POC_REQUIRED? → N** — non détecté automatiquement.
- [x] **POC_REQUIRED_BY_PLAN? → Y** — précondition manuelle explicite.
- [ ] **CAN_CODE_START? → NO**

## Décision

STOP avant toute modification du Core. Reprendre uniquement après :

1. revue indépendante approuvée ;
2. décision humaine finale ;
3. passage de l'ADR 0049 à `ACCEPTED` ;
4. `vbb-gate-check.py` avec `can_code_start=true` ;
5. contrôle manuel du verdict POC avec exit `0`.
