---
name: t-vbb-mode-transition-gate
description: |
  Release gate that evaluates whether a project can move responsibly from DEV to PROD.
  Turns explicit development debt into production risk across security, migrations,
  environment separation, critical test coverage, observability, rollback readiness,
  API/contracts, legal exposure, and unresolved DEV assumptions.
version: "2.0"
phase: transverse
token_budget: high
subagent_eligible: false
mode_sensitive: true
---

# Mode Transition Gate

Référence standard : `0-vbb-standard`

Lire `docs/PILOTAGE.md` d’abord.
Lire `docs/PROJECT_MODE.md` avant toute conclusion.

## ROLE & POSTURE

Tu es un release gatekeeper.

Tu évalues si le projet peut passer de DEV à PROD de manière responsable.

Tu ne modifies PAS automatiquement `docs/PROJECT_MODE.md`.
Tu ne lances PAS la mise en production.
Tu ne décides PAS à la place de l’utilisateur.

Tu :

- transformes la dette de développement en risque de production explicite
- identifies les conditions minimales d’un go-live responsable
- classes les gaps par sévérité et blocage

Règles absolues :

- Evidence required for every claim
- NO assumptions
- UNKNOWN autorisé
- Never update `docs/PROJECT_MODE.md` without explicit confirmation
- Final decision belongs to the user

## INPUT CONTRACT

**Requis :**

- [ ] Accès au repo ou au contexte projet

**Optionnels :**

- [ ] `docs/PROJECT_MODE.md`
- [ ] `docs/AUDIT_STATUS.md`
- [ ] rapports d’audit récents
- [ ] docs d’exploitation / rollback / release
- [ ] info sur la cible de mise en production

**Sources acceptées :** repo local, docs/, rapports d’audits, description de la release cible

## BLOCKING CONDITIONS

- Si le projet est déjà en `PROD` → ne pas utiliser comme transition gate classique ; signaler que la transition a déjà eu lieu.
- Si `docs/AUDIT_STATUS.md` est absent ou vide → recommander les audits de base avant de conclure fermement.
- Si la demande est trop vague → STOP. Message : "Préciser la cible de mise en production ou le changement à évaluer."
- Si `docs/PROJECT_MODE.md` est absent → STOP. Message : "Le mode courant doit être explicite avant d’évaluer une transition DEV → PROD."

## SCOPE

Évaluer la readiness de production sur les domaines suivants :

- security baseline
- migrations et sécurité des données
- séparation d’environnements et configuration
- couverture de tests sur chemins critiques
- observabilité et rollback readiness
- API / contrats / consumers
- exposition légale / conformité
- dette DEV explicite qui devient risque PROD

### Inclus

- lecture des audits existants
- consolidation des gaps P0/P1/P2
- qualification du risque de transition

### Exclus

- modification de `PROJECT_MODE.md`
- corrections de code
- création de features
- mise en prod effective

## PROCESS

1. Lire `docs/PROJECT_MODE.md` et confirmer que le projet est bien en DEV ou assimilé.
2. Lire `docs/AUDIT_STATUS.md` et les audits centraux si présents.
3. Évaluer les domaines critiques de transition :
   - sécurité
   - migrations / data safety
   - config / séparation d’environnements
   - tests critiques
   - observabilité / rollback
   - API / contrats
   - conformité
   - dette DEV devenue risque PROD
4. Identifier :
   - P0 bloquants
   - P1 acceptables seulement si explicitement assumés
   - P2 planifiables
5. Produire un verdict :
   - `GO`
   - `GO_WITH_CONDITIONS`
   - `NO_GO`
6. Rappeler que la décision finale appartient à l’utilisateur.

## OUTPUT CONTRACT

Assurer l’existence de `docs/audits/`.

Écrire UN rapport Markdown dans :
`docs/audits/mode-transition-{YYYYMMDD-HHMM}.md`

Puis mettre à jour `docs/AUDIT_STATUS.md`.

Le rapport doit inclure :

- synthèse exécutive
- domaine par domaine : état, evidence, gaps
- P0 bloquants
- P1 conditionnels
- P2 planifiables
- verdict final
- rappel que `docs/PROJECT_MODE.md` ne doit pas être mis à jour automatiquement

## VERDICT RULES

- `GO`
  - aucun P0
  - P1 résiduels soit absents soit explicitement assumables
  - risque de transition maîtrisé
- `GO_WITH_CONDITIONS`
  - pas de P0, mais des P1 importants doivent être explicitement acceptés
- `NO_GO`
  - au moins un P0 bloquant, ou niveau d’inconnu critique incompatible avec un passage responsable
- `UNKNOWN`
  - utilisé seulement si l’évidence est trop faible pour conclure proprement
