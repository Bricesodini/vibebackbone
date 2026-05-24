---
context_role: review
phase: "06"
status: COMPLETE
run_id: "YYYY-MM-DD_HHmm_slug"
updated: YYYY-MM-DD
---

# 06_REVIEW_RUN — Run [#]

**Date** : YYYY-MM-DD HH:mm  
**Reviewer** : [Nom ou rôle]  
**Status** : Review complétée  
**Run** : #[numero du run, ex: 1]

---

## Scope de la review

Reviewing patch summary run #[N], exécuté par [executor name].

---

## Fichiers examinés

- ✅ `src/auth.ts` → [observations]
- ✅ `src/middleware/auth.js` → [observations]
- ✅ `tests/auth.test.js` → [observations]

---

## Respect du scope

**Plan vs réalisé** :
- Étape 1 : ✅ Complétée
- Étape 2 : ✅ Complétée
- Hors-scope ajouté ? : [ ] Non détecté

---

## Qualité du code

- **Readabilité** : [bon | peut mieux | problème détecté]
- **Conventions** : [adhère | minor divergence | major issue]
- **Tests** : [suffisant | manque couverture | excellent]

---

## Risques détectés

- [ ] Aucun risque
- [ ] Risque mineur : [description, mitigation suggérée]
- [ ] Risque majeur : [description, blocke la validation]

---

## Points non résolus

[Récapitulatif des points non résolus du patch, que reviewer note]

---

## Recommandation

**Verdict** : [ ] Approuvé | [ ] Modifications mineures | [ ] Rejeté

**Raison** : [justification courte]

---

## Handoff

Si approuvé : prêt pour merge / release.
Si modifications : créer nouveau run #[N+1] avec executor, puis re-review.
Si rejeté : retour au planner ou escalade.
