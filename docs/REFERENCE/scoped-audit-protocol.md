---
load_policy: reference
canonical: true
referenced_by:
  - skills/1-vbb-code-janitor/SKILL.md
  - skills/1-vbb-tech-debt/SKILL.md
  - skills/2-vbb-db-robustness/SKILL.md
context_role: scoped-audit-protocol-canon
phase: transverse
status: active
---

# Scoped Audit Protocol — Reference (canon unique, ADR-0028)

> **Source unique de vérité** pour l'itération d'audits par petits scopes.
> Les skills citent ce chemin, elles ne reproduisent pas le protocole.
> S'applique à : `1-vbb-code-janitor`, `1-vbb-tech-debt`, `2-vbb-db-robustness`
> (extensible à d'autres skills d'analyse après preuve d'usage).

## Pourquoi

Un rapport unique sur un repo à N blocs mélange des findings de natures
différentes et tue l'actionnabilité (AUDIT-A-001/002). Le protocole remplace
« un gros audit » par « N petites passes bornées + un registre consolidé » —
granularité au choix, contexte LLM maîtrisé par passe.

## Le paramètre `scope`

- **Absent** → analyse **globale** (comportement historique, inchangé).
- **Présent** → l'analyse est strictement restreinte au périmètre. Valeurs :
  1. **Id de bloc** `docs/ARCHITECTURE.md` (ex. `contract-tooling`) — le scope
     est l'ensemble `files:` du bloc ;
  2. **Chemin** (répertoire ou glob, ex. `frontend/src/features/ideas/`) ;
  3. **Label métier** explicite fourni par l'humain, accompagné de la liste
     des chemins qu'il couvre.
- Rapport nommé `{skill}-{scope-slug}-{YYYYMMDD-HHMM}.md` ; chaque finding
  porte `scope: <valeur>` ; ce qui est hors scope est ignoré (pas de finding
  opportuniste hors périmètre — le noter en une ligne « observé hors scope »
  maximum, pour l'inventaire).

**Gabarit de finding** (le tag `scope:` est obligatoire — TER-002) :

```markdown
### JAN-06 — AdminStatCard.tsx orpheline (24 L)
- scope: frontend/src/features/auth
- Sévérité : P3 · Confiance : high
- Evidence : 0 référence (grep), dernier usage retiré le 2026-05-17
- Action recommandée (texte) : suppression sûre
```

**Cas mono-scope** (TER-003) : une passe unique sur un scope imposé par l'humain
ne requiert **pas** de registre. Le registre devient obligatoire dès qu'un
inventaire multi-scopes est ouvert (≥2 scopes), même si un seul est traité.

## La boucle d'itération (inventaire → passes → registre)

```
1. INVENTAIRE  — lister les scopes : blocs ARCHITECTURE.md par défaut ;
                 sinon découpage par répertoires de premier niveau ;
                 l'humain peut imposer sa liste. Trier par risque décroissant.
2. PASSES      — 1 passe = 1 scope = 1 rapport. Jamais plus d'un scope par
                 passe. Entre deux passes : compacter le contexte si ≥ 40 %
                 de fenêtre (75 % = limite dure, cf. SESSION_RULES).
3. REGISTRE    — consolider dans {skill}-register-{YYYYMMDD}.md :
                 une ligne par scope (verdict, P0/P1/P2, rapport lié) +
                 agrégation des P0/P1 en tête. Le registre est le livrable
                 de synthèse ; les rapports par scope sont les preuves.
```

Règles :

- L'inventaire est un artefact (liste datée en tête du registre) — pas un état
  mental : une reprise de session doit pouvoir continuer la boucle.
- Un scope non traité reste listé `PENDING` dans le registre — la boucle est
  finie quand aucun scope n'est `PENDING`.
- Les passes sont indépendantes : ordre modifiable, interruption sans perte
  (le registre + les rapports déjà produits suffisent à reprendre).
- La remédiation n'appartient pas à la boucle d'audit : les P0/P1 du registre
  partent en runs séparés (cf. ADR-0026 : pas de nettoyage pendant le scan).

## Gabarit du registre consolidé

```markdown
# {skill} — Register {YYYY-MM-DD}
Inventaire : <source : ARCHITECTURE.md | répertoires | liste humaine>

| Scope | Verdict | P0 | P1 | P2 | Rapport |
|-------|---------|----|----|----|---------|
| contract-tooling | PARTIAL | 0 | 2 | 3 | {skill}-contract-tooling-....md |
| distributions    | PENDING | — | — | — | — |

## P0/P1 agrégés
- <scope> — <finding> (P1) → run de remédiation proposé
```
