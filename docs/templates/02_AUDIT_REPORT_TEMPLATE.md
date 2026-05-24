---
context_role: audit
phase: "02"
status: COMPLETE
run_id: "YYYY-MM-DD_HHmm_slug"
updated: YYYY-MM-DD
---

# 02_AUDIT_REPORT — [Type d'audit]

**Date** : YYYY-MM-DD HH:mm  
**Type** : [sécurité | intégrité | ops | architecture | autre]  
**Auditor** : [Nom ou rôle]  
**Status** : Complété

> **Sections stables P0** : Scope audité · Constats clés · Verdicts · Risques remontés · Recommandations · Handoff — ne pas renommer sans mise à jour corrélative de CONTEXT.md.

---

## Scope audité

- **Domaine** : [fichiers, dossiers, ou système audité]
- **Objectif** : [qu'on cherchait à vérifier]
- **Environnement** : [dev | staging | prod]

---

## Constats clés

### Finding 1
- **Description** : [quoi]
- **Sévérité** : [CRITICAL | MAJOR | MINOR | INFO]
- **Exemple** : [où, dans quel fichier]

### Finding 2
- **Description** : [quoi]
- **Sévérité** : [CRITICAL | MAJOR | MINOR | INFO]

[... repeat as needed]

---

## Verdicts

| Verdict | Signification |
|---|---|
| **READY** | Prêt pour production / release |
| **PARTIAL** | Quelques findings, continue avec attention |
| **BLOCKED** | Arret immédiat, corrections requises |

**Verdict final** : [READY | PARTIAL | BLOCKED]

---

## Risques remontés

- **Risque 1** : [description, impact estimé, mitigation]
- **Risque 2** : [description, impact estimé]

---

## Recommandations

1. [Action prioritaire]
2. [Action secondaire]

---

## Handoff

Agent suivant : pour continuer, lire ce rapport. Si audit déclenche une correction :
- Créer une nouvelle session phase 03 (DECISION) si decision non évidente
- Ou créer une nouvelle session phase 04 (PLAN) si décision est clear
