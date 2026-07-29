---
run_id: "2026-07-29_0840_audit-remediation"
phase: "04_PLAN"
voie: "STRUCTUREE"
status: "READY"
agent: "claude-opus-5 (Claude Code)"
started_at: "2026-07-29T06:40:00Z"
ended_at: "2026-07-29T09:30:00Z"
artifacts_consumed:
  - "01_INTAKE.md"
artifacts_produced:
  - "04_PLAN.md"
---

# 04_PLAN — AUDIT-REMEDIATION-01

## Objectif

Fermer les findings `F2`–`F7` d'un audit en lecture seule qui a établi que le
verdict `READY` publié n'était pas soutenu par la mesure.

Les six findings ne sont pas six défauts indépendants mais une seule chaîne
rompue. Les corriger séparément laisserait la chaîne cassée ailleurs.

```
déclaration d'un invariant
  → enregistrement dans les contrats et l'index      F2
  → gate capable de le vérifier                      F3/F5
  → test capable d'échouer                           F4
  → CI qui exécute le gate                           F3
  → surface canonique qui reflète le résultat        F6/F7
  → verdict READY autorisé ou interdit
```

L'objectif n'est pas de remettre les gates au vert : c'est de les rendre capables
de dire non.

## Pré-conditions

- CI locale et distante vertes avant tout travail de fond — sinon aucune
  vérification ultérieure n'est interprétable. Assuré hors run par `f8850ca`
  (F1) et `a2a1d0a` (F14).
- `python tools/vbb-gate-check.py docs/runs/2026-07-29_0840_audit-remediation` renvoie `CAN_CODE_START=true`
  (Critical Rule #11). Premier appel : `MISSING_POC` → POC exécuté, puis PASS.
- Aucun ADR nouveau. Le run **applique** ADR 0042, 0046 et 0051, déjà `accepted`.
  Si un arbitrage non couvert apparaît, le run s'arrête et produit un
  `CANON_CHANGE_PROPOSAL.md`.
- Niveau adversarial `A2` déclaré à l'intake ; proxy déclaré ou absence déclarée,
  jamais une indépendance simulée.

## Étapes ordonnées

| # | Objet | Findings |
|---|---|---|
| 2.0 | Verdict honnête `NOT_READY` avant tout code | — |
| 2.2 | Contractualiser les 2 skills adversariaux | F2 |
| 2.1 | Lint bidirectionnel + dashboard binaire | F2 |
| 2.3 | Gate 5b exécutable et exécuté | F3, F5 |
| 2.4 | Test corpus comportemental | F4 |
| 2.5 | Réaligner les surfaces + contrôle de cohérence | F6, F7 |
| 2.6 | Matrice de preuve négative + verdict final | — |

Ordre imposé : **2.2 précède 2.1**. Durcir le lint avant d'écrire les contrats
aurait rendu l'arbre rouge entre deux commits.

## Critères d'acceptation

Aucun critère n'est satisfait par une observation « au vert ».

| # | Critère | Preuve exigée |
|---|---|---|
| 1 | Lint bidirectionnel | Skill sans `CONTRACT.yaml` → exit non-zéro |
| 2 | Population canonique définie dans le code | Commentaire au-dessus de la fonction, pas seulement dans ce run |
| 3 | Couverture 66/66 | Lint 0 erreur, dashboard `PASS` |
| 4 | Dashboard binaire | Sous 100 % rendu `FAIL`, pas un pourcentage |
| 5 | Sept sections ADR 0042 | Les 2 skills passent `check_required_skill_sections` |
| 6 | Bloc pre-merge exécutable | Copié-collé tel quel → exit 0 |
| 7 | 5b câblé identiquement | Commandes identiques CI locale et distante |
| 8 | Corpus vide sort proprement | `pytest tests/adversarial_corpus/ -q` → 0, pas 5 |
| 9 | Test corpus comportemental | CONFIRMED sans corpus → échec ; avec → succès ; pré-cutoff → non exigé |
| 10 | Cohérence vérifiable | Contradiction ADR/AUDIT_STATUS détectée par une commande |
| 11 | Verdict honnête pendant le run | `NOT_READY` dès le premier commit |
| 12 | F8–F13 inscrits | Registre des risques actifs avec owner et trigger |

## Plan de rollback global

Chaque étape est un commit isolé et réversible par `git revert`, dans l'ordre
inverse. Aucune migration de données, aucun état persistant hors dépôt, aucune
modification de `distributions/**` : le rollback est purement Git.

Points de retour sûrs :

- **avant le run** — `f8850ca` (F1 corrigé, CI locale verte) ;
- **avant tout durcissement de gate** — `a2a1d0a` (CI distante verte).

Si un durcissement casse un consommateur non anticipé, la règle est de revenir au
commit précédent plutôt que d'assouplir le gate : un gate assoupli pour faire
passer la CI reproduit le défaut audité.

Le seul geste non réversible par `git revert` serait la réécriture d'un run
historique — explicitement hors scope (`TEMPORAL_PROVENANCE.md`).

## Risques identifiés

| Risque | Mitigation |
|---|---|
| Le durcissement du lint casse un skill non anticipé | Lancer le lint sur les 66 avant de rendre l'erreur bloquante |
| La normalisation des 7 sections altère le sens des 2 skills | Remapper le contenu, ne rien réécrire ; diff relu section par section |
| Le nouveau test corpus devient à son tour tautologique | Preuve négative obligatoire (critère 9) |
| Ajouter 5b à la CI distante casse les PR existantes | Vérifier le comportement sur corpus vide avant de rendre bloquant |
| Corriger `AUDIT_STATUS` sans corriger le mécanisme | Le contrôle de cohérence (critère 10) est le livrable, pas l'édition |
| Le run se déclare indépendant sans l'être | Proxy déclaré explicitement, ou absence déclarée |
| Un gate durci échoue pour une raison d'environnement | Exécuter le bloc canonique verbatim, pas seulement le lire |

## Méthode de vérification

`pytest` sur l'arbre de travail ne prouve rien sur l'état commité. Toute
vérification revendiquant un verdict passe par un `git clone --no-local` de HEAD.
Cette règle vient de `F14`, découvert pendant le POC de ce run.

Les artefacts du run sont commités au closeout, pas incrémentalement : le hook de
clôture exige les quatre phases dès qu'un run est stagé, et les fournir à
mi-parcours reviendrait à publier des résultats de gate non produits.
