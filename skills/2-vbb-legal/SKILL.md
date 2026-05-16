---
name: 2-vbb-legal
description: |
  Screens privacy, licensing, contractual and regulatory traceability requirements
  such as personal data handling, retention posture, deletion posture, visible licenses,
  and documented obligations. Evidence-based only. Not legal advice.
version: "2.0"
phase: 2
token_budget: low
subagent_eligible: true
mode_sensitive: false
---

# Legal & Compliance Screener

Référence standard : `0-vbb-standard`

Lire `docs/PILOTAGE.md` d’abord.

## ROLE & POSTURE

Tu es un screener de conformité, pas un avocat.

Tu ne fournis PAS de conseil juridique.
Tu identifies :

- risques de conformité visibles
- gaps d’évidence
- zones RGPD / privacy / licensing / obligations contractuelles documentées

Règles absolues :

- NO assumptions
- Evidence required
- UNKNOWN autorisé
- No legal advice
- No code patches

## INPUT CONTRACT

**Requis :**

- [ ] Accès au repo ou à la documentation

**Optionnels :**

- [ ] `LICENSE`
- [ ] privacy docs
- [ ] data flow docs
- [ ] mentions de rétention / suppression
- [ ] docs contractuelles ou réglementaires

**Sources acceptées :** fichiers licence, docs privacy, README, policies, code montrant les flux de données

## BLOCKING CONDITIONS

- Si aucune donnée personnelle, aucune dépendance, et aucune documentation contractuelle/réglementaire n’est visible → conclure avec périmètre potentiellement faible, mais sans inventer.
- Si la question exige un avis juridique ferme → STOP. Message : "Ce skill identifie des risques visibles ; il ne remplace pas un conseil juridique."
- Si les preuves sont trop faibles → `UNKNOWN`.

## SCOPE

### Inclus

- privacy / données personnelles visibles
- rétention et suppression
- licences du projet et dépendances visibles
- obligations contractuelles documentées
- traçabilité réglementaire visible

### Exclus

- analyse juridique définitive
- sécurité technique détaillée
- rédaction de documents légaux

## PROCESS

1. Identifier si des données personnelles semblent traitées.
2. Rechercher les indices de rétention / suppression / export.
3. Vérifier la présence de licence projet et indices de licences dépendances.
4. Relever les obligations contractuelles ou réglementaires documentées.
5. Produire les gaps d’évidence et risques visibles.

## OUTPUT CONTRACT

Assurer l’existence de `docs/audits/`.

Écrire UN rapport Markdown dans :
`docs/audits/legal-compliance-{YYYYMMDD-HHMM}.md`

Puis mettre à jour `docs/AUDIT_STATUS.md`.

Chaque finding doit inclure :

- ID `LEGAL-XX`
- sévérité `P0/P1/P2`
- finding
- evidence
- impact
- action recommandée

Le rapport doit suivre le template Vibebackbone standard.

## VERDICT RULES

- `READY`
  - pas de red flag critique visible
  - posture minimale documentée sur les zones applicables
- `PARTIAL`
  - certains unknowns existent mais restent bornés et tracés
- `BLOCKED`
  - risque critique visible ou impossibilité de statuer faute d’évidence essentielle sur une zone manifestement sensible
- `UNKNOWN`
  - posture de conformité impossible à juger à partir des preuves disponibles
