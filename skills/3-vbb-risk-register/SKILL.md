---
name: 3-vbb-risk-register
description: |
  Consolidates findings from existing Vibebackbone reports into a single risk register.
  Performs no new audit and no new analysis beyond normalization, deduplication,
  priority ordering, and explicit identification of unknown or uncovered areas.
  Use after phase 2 audits, or when compiling "risques identifiés et assumés".
version: "2.0"
phase: 3
token_budget: low
subagent_eligible: true
mode_sensitive: false
---

# Risk Register Compiler

Référence standard : `0-vbb-standard`

Lire `docs/PILOTAGE.md` d’abord.

## ROLE & POSTURE

Tu es un consolidateur.
Tu ne ré-audites PAS.
Tu ne crées PAS de nouveaux findings.
Tu compiles, normalises et ordonnes les risques déjà présents dans les rapports existants.

Règles absolues :

- NO assumptions
- Si un rapport manque, marquer la zone `UNKNOWN`
- No new analysis beyond consolidation
- No code patches
- No feature work

## INPUT CONTRACT

**Requis :**

- [ ] Accès à `docs/audits/`

**Optionnels :**

- [ ] `docs/AUDIT_STATUS.md`
- [ ] rapports récents de phase 0, 1 et 2
- [ ] décisions explicites déjà documentées (accept / mitigate / defer)

**Sources acceptées :** rapports Markdown Vibebackbone, `docs/AUDIT_STATUS.md`, documentation projet

## BLOCKING CONDITIONS

- Si `docs/audits/` n’est pas accessible → STOP. Message : "Impossible de compiler le registre des risques sans accès aux rapports."
- Si aucun rapport n’est présent → STOP. Message : "Aucun rapport disponible à consolider."
- Si les rapports sont trop hétérogènes ou incomplets pour être rapprochés proprement → conclure avec forte part d’`UNKNOWN`.

## SCOPE

### Inclus

- consolidation des findings existants
- déduplication des risques
- regroupement par familles de risque
- identification des zones non couvertes
- reprise des décisions explicites si déjà présentes dans les rapports

### Exclus

- ré-audit
- création de nouveaux findings
- réinterprétation spéculative des rapports
- décision produit ou opérationnelle à la place de l’utilisateur

## PROCESS

1. Lister les rapports récents dans `docs/audits/`.
2. Identifier les rapports pertinents disponibles :
   - scope freeze
   - audit readiness
   - security
   - systemic risk
   - data integrity
   - db robustness
   - ops
   - ci
   - legal
   - api auditor
3. Extraire les findings et risques explicites.
4. Dédupliquer les items manifestement redondants sans perdre les références d’origine.
5. Regrouper les risques consolidés.
6. Lister les zones non couvertes ou les rapports manquants comme `UNKNOWN`.
7. Reprendre les décisions explicites (`Accept`, `Mitigate`, `Defer`) seulement si elles sont déjà documentées.

## OUTPUT CONTRACT

Assurer l’existence de `docs/audits/`.

Écrire UN fichier Markdown dans :
`docs/audits/risk-register-{YYYYMMDD-HHMM}.md`

Puis mettre à jour `docs/AUDIT_STATUS.md`.

Le rapport doit suivre ce format :

# Registre des risques identifiés et assumés — v1.0 — YYYY-MM-DD

## Risques identifiés et assumés

1. [SEC-02] ...
2. [SYS-05] ...
3. [DATA-03] ...

## UNKNOWN / Zones non couvertes

- Missing report: ...

## Décision

- Accept / Mitigate / Defer / UNKNOWN

Chaque risque consolidé doit contenir :

- référence(s) d’origine
- résumé du risque
- niveau de priorité si visible
- état de décision s’il est explicitement documenté

## VERDICT RULES

- `READY`
  - les risques existants sont consolidés proprement
  - les zones non couvertes sont explicitement listées
- `PARTIAL`
  - consolidation possible mais plusieurs zones restent dispersées ou faiblement reliées
- `BLOCKED`
  - les rapports disponibles sont trop absents ou trop incohérents pour produire un registre utile
- `UNKNOWN`
  - utilisé seulement si les preuves documentaires sont trop faibles pour conclure proprement
