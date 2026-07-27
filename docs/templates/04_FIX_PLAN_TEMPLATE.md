---
context_role: plan
phase: "04"
status: OPEN
run_id: "YYYY-MM-DD_HHmm_slug"
updated: YYYY-MM-DD
---

# 04_FIX_PLAN — [Objectif de la solution]

**Date** : YYYY-MM-DD HH:mm  
**Planner** : [Nom ou rôle]  
**Status** : Plan prêt pour exécution

> **Sections stables P0** : Objectif · Scope délimité · Étapes d'implémentation · Risques identifiés · Handoff — ne pas renommer sans mise à jour corrélative de CONTEXT.md.

---

## Objectif

[Une phrase résumant ce qu'on va accomplir]

---

## Scope délimité

- **Domaine** : [architectural area impactée]
- **Fichiers** : [liste estimée]
- **Hors scope** : [ce qu'on ne fera PAS, pour clarté]

---

## Étapes d'implémentation

### Étape 1
- **Quoi** : [description]
- **Fichiers** : [liste]

### Étape 2
- **Quoi** : [description]

[... repeat]

---

## Tests prévus

- **Unit tests** : [où, quoi]
- **Integration tests** : [où, quoi]
- **Manual testing** : [scénario]

---

## Risques identifiés

- **Risque 1** : [description, mitigation]
- **Risque 2** : [description]

---

## Dépendances

- [Artefact ou ressource requise]
- [Timing ou ordre d'exécution]

---

## Autorisation d'implémentation

```yaml
implementation_authorization:
  status: "AUTHORIZED|NOT_AUTHORIZED"
  required_gate_ids: ["gate-id"]
  reasons: ["raison explicite"]
```

L'autorisation est fail-closed et n'est jamais déduite de verdicts PASS.

---

## Handoff

Agent suivant (executor) : plan validé, commencer phase 05 selon ces étapes.
