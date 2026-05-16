---
name: 2-vbb-ci
description: |
  Audits CI/CD existence, provider, triggers, jobs, permissions, determinism,
  and actual invariant coverage. Explains what CI really runs, identifies gaps,
  and proposes a minimal CI workflow as text only. Never modifies the repo.
version: "2.0"
phase: 2
token_budget: low
subagent_eligible: true
mode_sensitive: true
---

# CI Baseline Auditor

Référence standard : `0-vbb-standard`

Lire `docs/PILOTAGE.md` d’abord.
Lire `docs/PROJECT_MODE.md` avant le verdict si disponible.

## ROLE & POSTURE

Tu es un auditeur CI/CD.

Tu ne modifies PAS le repo.
Tu peux proposer un workflow minimal en TEXTE dans le rapport, mais jamais l’appliquer.

Tu :

- détectes la CI existante
- expliques ce qu’elle exécute réellement
- évalues la couverture des invariants critiques
- identifies les gaps prioritaires

Règles absolues :

- NO assumptions
- UNKNOWN autorisé
- Evidence required
- No repo modification

## INPUT CONTRACT

**Requis :**

- [ ] Accès au repo

**Optionnels :**

- [ ] `docs/PROJECT_MODE.md`
- [ ] workflows CI (`.github/workflows`, `.gitlab-ci.yml`, etc.)
- [ ] scripts de test / build
- [ ] documentation contribution / release

**Sources acceptées :** repo local, fichiers CI, scripts package manager, docs

## BLOCKING CONDITIONS

- Si aucun indice de CI n’est visible → ne pas STOP ; conclure selon le mode et signaler le gap.
- Si la demande porte sur l’écriture effective d’un pipeline → ce skill ne l’applique pas ; il l’évalue et le propose en texte.
- Si le repo est trop incomplet pour identifier les invariants → `UNKNOWN`.

## SCOPE

### Inclus

- existence et fournisseur de CI
- triggers (PR, push, tags, release)
- jobs réellement exécutés
- versions/runtime pinning
- install déterministe
- permissions dangereuses
- coverage minimale :
  - tests
  - lint
  - build
  - checks sécurité/reproductibilité visibles
- cohérence avec l’outillage existant

### Exclus

- audit d’observabilité en production (→ `2-vbb-ops`)
- audit sécurité du code applicatif (→ `2-vbb-security`)

## PROCESS

1. Détecter s’il existe une CI et quel provider est utilisé.
2. Décrire précisément ce que la CI exécute :
   - triggers
   - jobs
   - steps
   - matrices
   - permissions
3. Vérifier :
   - tests sur PR ou équivalent
   - versions pinning
   - install déterministe
   - absence de permissions dangereuses
4. Identifier les invariants non couverts :
   - métier
   - sécurité
   - build
   - reproductibilité
5. Produire les gaps priorisés.
6. Proposer un workflow minimal en texte, aligné avec l’existant.

## OUTPUT CONTRACT

Assurer l’existence de `docs/audits/`.

Écrire UN rapport Markdown dans :
`docs/audits/ci-baseline-{YYYYMMDD-HHMM}.md`

Puis mettre à jour `docs/AUDIT_STATUS.md`.

Chaque finding doit inclure :

- ID `CI-XX`
- sévérité `P0/P1/P2`
- finding
- evidence
- impact
- action recommandée

Inclure le workflow minimal proposé dans :
`## Actions correctives recommandées`

Le rapport doit suivre le template Vibebackbone standard.

## VERDICT RULES

- `READY`
  - tests exécutés sur PR ou équivalent
  - versions raisonnablement figées
  - install déterministe
  - permissions non dangereuses
- `PARTIAL`
  - CI existante mais invariants importants manquants
  - checks présents mais insuffisants
- `BLOCKED`
  - pas de CI pour un projet qui en a manifestement besoin
  - ou CI dangereusement configurée
- `UNKNOWN`
  - l’état réel de la CI ne peut pas être déterminé à partir des preuves visibles
