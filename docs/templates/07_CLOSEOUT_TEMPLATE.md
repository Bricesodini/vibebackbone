---
context_role: closeout
phase: "07"
status: COMPLETE
run_id: "YYYY-MM-DD_HHmm_slug"
updated: YYYY-MM-DD
---

# 07_CLOSEOUT — [Objet de clôture]

**Date** : YYYY-MM-DD HH:mm  
**Closeout lead** : [Nom ou rôle]  
**Status** : Session clôturée

> **Sections stables P0** : Statut final · Travail effectué · Décisions prises · Points ouverts · Prochaine session recommandée · Mise à jour de la gouvernance — ne pas renommer sans mise à jour corrélative de CONTEXT.md.

---

## Statut final

**Verdict** : [ ] Succès | [ ] Partiellement complété | [ ] Escalade requise

---

## Travail effectué

[Résumé court de ce qu'on a fait dans cette session]

- Audit : [si applicable]
- Décision : [si applicable]
- Plan : [si applicable]
- Exécution : [nombre de runs, ce qu'on a livré]
- Review : [verdict final]

---

## Décisions prises

1. [Décision 1 + contexte court]
2. [Décision 2 + contexte court]

---

## Assurance

Insérer le bloc frère `ASSURANCE_STATUS` v1 de
`docs/GATE_ASSURANCE_GOVERNANCE.md`, avec résultats qualifiés, preuves et
autorisation explicite. Ne pas le fusionner avec `FINAL_STATUS`.

---

## Knowledge Harvest

Disposition obligatoire : `NONE`, `OBSERVATION_RECORDED` ou
`EVIDENCE_LINKED`. Le Harvest reste un contrôle de closeout et ne devient pas
un gate Design ou Certification.

---

## Risques identifiés et documentés

- **Risque 1** : [description, niveau P0/P1/P2/P3, mitigation]
- **Risque 2** : [si applicable]

[Tous les risques importants doivent être remontés dans AUDIT_STATUS.md]

---

## Points ouverts

- [ ] Point 1 : [description, priorité]
- [ ] Point 2 : [description]

[Liste ce qui n'a pas pu être résolu dans cette session]

---

## Prochaine session recommandée

**Objectif** : [ce qu'il faudra faire]

**Type** : [ ] Audit | [ ] Décision | [ ] Plan | [ ] Exécution | [ ] Review | [ ] Nouvelle tâche

**Rôle** : [auditeur | planner | executeur | reviewer]

**Dépendances** : [ressources requises]

---

## Artefacts produits

- [Lister tous les fichiers créés : 01_INTAKE.md, 02_AUDIT_REPORT.md, etc.]

---

## Mise à jour de la gouvernance

**SESSION.md** : Mise à jour avec contexte final  
**AUDIT_STATUS.md** : Mise à jour si risques nouveaux  

[Vérifier que ces fichiers reflètent l'état final de la session]

---

## Mise à jour de CONTEXT.md

**Obligation** : à chaque closeout formel (voie STRUCTURÉE), mettre à jour `docs/CONTEXT.md`.

Ajouter uniquement :
- **Statut** : verdict du run (succès, partiel, escalade)
- **Lien vers run** : `[YYYY-MM-DD_HHmm_slug](runs/YYYY-MM-DD_HHmm_slug/07_CLOSEOUT.md)`
- **Décisions actives** : si une décision a été prise, ajouter le lien vers `03_DECISION_RECORD.md`
- **Points ouverts** : si des points ouverts subsistent, les ajouter à la section correspondante
- **Prochaine action** : type et objectif de la prochaine session recommandée

**Interdictions** :
- ❌ Ne PAS recopier le contenu du closeout dans CONTEXT.md — CONTEXT.md pointe vers, il ne duplique pas
- ❌ Ne PAS transformer CONTEXT.md en narration longue

**Vérification de liens** : avant d'enregistrer, vérifier que chaque lien ajouté dans CONTEXT.md pointe vers un fichier existant et, si possible, vers une section stable (ancre P0).

**Comportement pour les tâches RAPIDES** :
- Si un `07_CLOSEOUT.md` formel est produit → `docs/CONTEXT.md` doit être mis à jour (même règle que STRUCTURÉE)
- Si la tâche RAPIDE ne produit pas de closeout formel → ne pas créer d'entrée lourde dans CONTEXT.md ; une mise à jour légère (statut, point ouvert) reste possible à la discrétion de l'agent si un événement significatif s'est produit

---

_Session clôturée le [DATE]. Prochaine étape : [NEXT]_
