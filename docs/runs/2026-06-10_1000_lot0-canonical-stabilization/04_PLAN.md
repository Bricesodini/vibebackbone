# 04_PLAN — RUN 01 · Lot 0 : Plan de corrections documentaires

**Date** : 2026-06-10  
**Voie** : STRUCTURÉE  
**Prérequis** : 02_DISCOVERY.md validé

---

## Chiffres canoniques retenus

| Métrique | Valeur canonique | Justification |
|----------|-------------------|---------------|
| Skills | **58** | `find skills -name SKILL.md \| wc -l` = 58 |
| Prompts total | **32** | 7 canoniques + 24 spécialisés + 1 router = 32 |
| Prompts canoniques | **7** | `find prompts/canonical -type f \| wc -l` = 7 |
| Prompts spécialisés | **25** | 3 (P0) + 7 (P1) + 5 (P2) + 1 (P3) + 3 (P4) + 6 (t) = 25 |
| Prompts spécialisés (hors router) | **24** | 25 - 1 router = 24 |
| Contrats mécaniques | **22** | `find skills -name CONTRACT.yaml \| wc -l` = 22 |

**Convention d'affichage** : « 58 skills · 32 prompts (7 canoniques + 24 spécialisés + 1 router) · 22 contrats »

---

## Liste exacte des corrections documentaires

### PATCH-01 : README.md — Chiffres et table

| Localisation | Avant | Après |
|--------------|-------|-------|
| Ligne 4 (banner) | "57 skills · 31 prompts · 4 voies d'exécution · 7 phases agentiques" | "58 skills · 32 prompts (7 canoniques + 24 spécialisés + 1 router) · 4 voies d'exécution · 7 phases agentiques" |
| Ligne 35 (arbre) | "57 skills prêts à injecter" | "58 skills prêts à injecter" |
| Ligne 43 (arbre prompts) | "31 prompts (7 canoniques + 24 spécialisés + 1 router)" | "32 prompts (7 canoniques + 24 spécialisés + 1 router)" |
| Ligne 62 (titre section) | "Les 57 skills en un coup d'œil" | "Les 58 skills en un coup d'œil" |
| Table t-* | 12 noms (manque status-report) | Ajouter "Status-report" |
| Ligne 79 (titre section) | "Les 31 prompts — architecture en 3 couches" | "Les 32 prompts — architecture en 3 couches" |
| Ligne 88 | "← 24 prompts spécialisés (domaine ou contexte précis)" | "← 24 prompts spécialisés + 1 router" |
| Ligne 99 (table spécialisés) | Liste de 24 | Ajouter note que le router est le 25e fichier root-level |
| Ligne 190 | "Les 57 skills sont disponibles" | "Les 58 skills sont disponibles" |

### PATCH-02 : AGENTS.md — Ligne de tag

| Localisation | Avant | Après |
|--------------|-------|-------|
| Ligne 350 | "57 skills · 24 prompts · 4 voies" | "58 skills · 32 prompts (7 canoniques + 24 spécialisés + 1 router) · 4 voies" |

### PATCH-03 : SYSTEM.md — Ligne de tag

| Localisation | Avant | Après |
|--------------|-------|-------|
| Ligne 5 | "57 skills · 24 prompts · 4 voies" | "58 skills · 32 prompts (7 canoniques + 24 spécialisés + 1 router) · 4 voies" |

### PATCH-04 : GUIDE.md — Chiffres multiples

| Localisation | Avant | Après |
|--------------|-------|-------|
| Ligne 82 | "31 PROMPTS" | "32 PROMPTS" |
| Ligne 88 | "57 SKILLS" | "58 SKILLS" |
| Ligne 168 | "← 24 prompts spécialisés" | "← 24 prompts spécialisés + 1 router" |
| Ligne 184 | "3.4 Les 57 skills" | "3.4 Les 58 skills" |
| Ligne 220 | "Les 57 skills" | "Les 58 skills" |
| Ligne 221 | "Les 24 prompts" | "Les 24 prompts spécialisés + 1 router" |
| Ligne 786 | "31 c'est beaucoup" | "32 c'est beaucoup" |
| Ligne 793 | "Les 31" | "Les 32" |
| Ligne 926 | "catalogue des 57 skills" | "catalogue des 58 skills" |

### PATCH-05 : docs/CONTEXT.md — Verdict et chiffres

| Localisation | Avant | Après |
|--------------|-------|-------|
| Ligne 48 | "🟢 PRODUCTION-READY + OPENCODE-READY" | "🟡 PARTIAL — not yet mechanically audited" |
| Ligne 57 | "58 skills · 22 CONTRACT.yaml indexés" | "58 skills · 22 contrats mécaniques (38 %)" |
| Ligne 58 | "24 prompts de session" | "32 prompts (7 canoniques + 24 spécialisés + 1 router)" |

### PATCH-06 : docs/INDEX.md — Prompts

| Localisation | Avant | Après |
|--------------|-------|-------|
| Ligne 47 | "Prompts spécialisés (25)" | "Prompts spécialisés (24) + 1 router" |

Note : INDEX.md disait « 25 » ce qui est correct si le router est inclus. La correction clarifie que « 24 spécialisés + 1 router = 25 au total root-level ».

### PATCH-07 : docs/AUDIT_STATUS.md — Chiffre obsolète

| Localisation | Avant | Après |
|--------------|-------|-------|
| Ligne 20 | "8 skills sur 58 (14 %)" | "22 skills sur 58 (38 %)" |
| Ligne 34 | "8/58 skills (14 %)" | "22/58 skills (38 %)" |

### PATCH-08 : Skills méta/orphelins — Documentation dans les SKILL.md

Aucune modification de SKILL.md (hors scope).  
Les 4 skills méta seront documentés dans cette section du plan pour référence future :

| Skill | Classification | Note |
|-------|---------------|------|
| `0-vbb-guide` | **Documentation** | Carte de référence système — phase `transverse` |
| `0-vbb-pilotage` | **Documentation** | Référentiel des voies — phase `transverse` |
| `0-vbb-standard` | **Méta-skill** | Standard canonique des skills — phase `transverse` |
| `vibebackbone` | **Orchestrateur** | Triage et routage global — phase `transverse` |

Ces 4 skills ne sont pas « orphelins » au sens de non-fonctionnels. Ils sont des **skills de gouvernance et méta**. Leurs préfixes `0-` reflètent leur rôle de « pré-condition à l'action », ce qui est cohérent, même si `phase: transverse` dans leur frontmatter est technique. Pas de renommage, pas de suppression (interdit).

### PATCH-09 : README.md — Ajout de status-report dans la table t-*

Ajouter `Status-report` à la liste des skills transverses dans la table du README.

### PATCH-10 : docs/SESSION.md — Ajout entrée Lot 0

Ajouter une entrée courte indiquant le run Lot 0.

---

## Traitement des labels non prouvés

| Label | Fichier | Action |
|-------|---------|--------|
| "🟢 PRODUCTION-READY + OPENCODE-READY" | CONTEXT.md ligne 48 | Remplacer par "🟡 PARTIAL — not yet mechanically audited" |
| "production-ready" (nginx) | README.md ligne 77 | ✅ Légitime — ne pas modifier |

---

## Fichiers à modifier (résumé)

1. `README.md` — PATCH-01, PATCH-09
2. `AGENTS.md` — PATCH-02
3. `SYSTEM.md` — PATCH-03
4. `GUIDE.md` — PATCH-04
5. `docs/CONTEXT.md` — PATCH-05
6. `docs/INDEX.md` — PATCH-06
7. `docs/AUDIT_STATUS.md` — PATCH-07
8. `docs/SESSION.md` — PATCH-10

---

## Critères de validation du plan

- [ ] Aucun fichier hors scope modifié
- [ ] Aucun nouveau CONTRACT.yaml ajouté
- [ ] Aucun SKILL.md modifié
- [ ] Aucun renommage ou suppression de skill
- [ ] Tous les chiffres cohérents après patch
- [ ] Label « PRODUCTION-READY » retiré de CONTEXT.md
- [ ] 4 skills méta documentés dans le plan (pas modifiés)