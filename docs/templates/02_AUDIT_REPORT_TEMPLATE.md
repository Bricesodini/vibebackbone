---
context_role: audit
phase: "02"
status: COMPLETE
run_id: "YYYY-MM-DD_HHmm_slug"
updated: YYYY-MM-DD
---

# 02_AUDIT_REPORT — [Type d'audit]

**Date** : YYYY-MM-DD HH:mm
**Type d'audit** : [sécurité | intégrité | ops | architecture | ci | légal | systémique | autre]
**Skill utilisé** : [nom du skill ou "grille générique"]
**Scope** : [description du périmètre audité]
**Auditor** : [Nom ou rôle]
**Status** : Complété

> **Sections stables P0** : Scope audité · Constats clés · Verdicts · Risques remontés · Recommandations · Handoff — ne pas renommer sans mise à jour corrélative de CONTEXT.md.

---

## Scope audité

- **Domaine** : [fichiers, dossiers, ou système audité]
- **Objectif** : [qu'on cherchait à vérifier]
- **Environnement** : [dev | staging | prod]

---

## Verdict global

**Verdict** : READY | PARTIAL | BLOCKED | UNKNOWN

**Justification** : [Résumé des raisons du verdict]

---

## Constats

### [ID — ex: SEC-001, SYS-002, DATA-003]

| Champ | Valeur |
|-------|--------|
| **Severity** | P0 (critical/blocking) · P1 (major) · P2 (minor) · P3 (info/trend) |
| **Type** | VIOLATION · OBSERVATION · TREND · FALSE_POSITIVE |
| **Location** | [fichier:ligne ou module ou domaine] |
| **Evidence Level** | OBSERVATION · SIGNAL · HYPOTHESIS · VERIFIED_FINDING |
| **Evidence Trace** | OBSERVATION → SIGNAL → VÉRIFICATION → FINDING (obligatoire si VERIFIED_FINDING) |
| **Evidence** | [sources — pas d'hypothèse non fondée] |
| **Decision** | ACCEPTED · MITIGATED · DEFER · NEEDS_DECISION |
| **Recommendation** | [action corrective suggérée] |

[Répéter pour chaque constat]

---

## Risques consolidés

| Risque | Severity | Probabilité | Impact | Action recommandée |
|--------|----------|-------------|--------|--------------------|
| ...    | P0/P1/P2/P3 | High/Medium/Low | High/Medium/Low | ... |

---

## Ce qui est hors scope

[Ce qui n'a PAS été audité, et pourquoi]

---

## Handoff

**Phase suivante** : 03_DECISION
**Nouvelle session recommandée** : Oui (rôle décideur ≠ rôle auditeur)
**À transmettre** : ce rapport + liste des constats prioritaires
**Points de vigilance** : [risques à traiter en priorité]