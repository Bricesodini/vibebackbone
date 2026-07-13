---
audit_type: systemic_risk
date: 2026-06-13
auditor: codex
scope: public_publication_readiness
verdict: PARTIAL
---

# Systemic Risks — Public Publication Readiness

**Date**: 2026-06-13  
**Route**: AUDIT  
**Focus**: publication publique, lisibilité senior, onboarding non-dev, hygiène de repo

## 1. Périmètre audité

Audit de la surface publique du dépôt Vibebackbone, avec un angle volontairement
orienté vers une future mise à disposition externe:

- lisibilité du `README.md` pour des programmeurs seniors
- lisibilité du `GUIDE.md` pour des utilisateurs non développeurs de métier
- cohérence de la hiérarchie documentaire publique
- signaux de maturité / sécurité de publication

## 2. Méthode

Sources lues:

- `README.md`
- `GUIDE.md`
- `docs/DISTRIBUTIONS.md`
- `docs/INDEX.md`
- `docs/AUDIT_STATUS.md`
- `docs/audits/release-readiness-v1.0.0-rc.1-20260524.md`
- `docs/audits/global-evaluation-20260613.md`

Commandes utilisées:

- `python tools/vbb-status-dashboard.py`
- `python tools/vbb-index.py search "public"`
- `git status --short`
- `git ls-files | rg '\\.DS_Store$'`

## 3. Findings

| # | Dimension | Severity | Type | Evidence Level | Evidence Trace | Decision | Verdict |
|---|-----------|----------|------|----------------|----------------|----------|---------|
| 1 | Core vs distribution taxonomy in public README | `P1` | `VIOLATION` | `VERIFIED_FINDING` | Observation: `README.md` previously marked `distributions/{claude,codex,pi,opencode}/setup.sh` as "Stable core" (`README.md:36-41`). Signal: `docs/DISTRIBUTIONS.md` says distributions are operational declinations, not Core, and that Core is the generic method (`docs/DISTRIBUTIONS.md:2-4`, `docs/DISTRIBUTIONS.md:14-20`). Verification: the README also later separated distribution code as a distinct concern (`README.md:100-119`), so the top-level taxonomy was internally inconsistent. Finding: public readers could misclassify distribution setup scripts as Core canon. Remediation applied in-session: `README.md` and `docs/DISTRIBUTIONS.md` now separate Core from distribution code explicitly. | `MITIGATED` | `PARTIAL` |
| 2 | Non-dev onboarding path is not fully explicit yet | `P2` | `OBSERVATION` | `VERIFIED_FINDING` | Observation: `GUIDE.md` identifies the audience as "devs, leads, PM" (`GUIDE.md:1-4`) and frames the guide around agentic development (`GUIDE.md:38-44`, `GUIDE.md:69-73`). Signal: there is no fully dedicated operator-first path that starts from zero vocabulary and ends at a safe pause/resume cycle. Verification: the structure is rich for practitioners, and a short non-dev entry note has now been added in-session, but the guide still leans on internal terms early. Finding: the guide is usable, yet not fully optimised for the non-dev public audience requested. | `DEFER` | `PARTIAL` |
| 3 | Publication readiness remains partially open in live audit status | `P2` | `TREND` | `VERIFIED_FINDING` | Observation: `docs/AUDIT_STATUS.md` still records `PARTIAL` as the global verdict (`docs/AUDIT_STATUS.md:14-18`) and keeps open P2 items directly relevant to public release hygiene: stale pending artifact, optional quality tools not canonically gated, distribution code not fully covered by architecture/CI, and static status counter drift (`docs/AUDIT_STATUS.md:76-80`). Signal: the status dashboard also surfaces open risks and keeps the project in `PARTIAL`. Verification: these are not hypothetical; they are active, documented, and surfaced in the current project status. Finding: the repository is reference-ready, but not yet publication-clean enough to present as fully polished. | `NEEDS_DECISION` | `PARTIAL` |

## 4. Verdict global

- **Statut** : `PARTIAL`
- **Justification** : la base documentaire et gouvernance est solide, mais la surface publique n'est pas encore entièrement cohérente ni polie. Le principal défaut initial de mélange entre Core et distribution dans le README a été corrigé, mais l'absence d'un vrai chemin d'entrée non-dev et plusieurs risques P2 de publication restent ouverts. Le statut projet lui-même reste partiellement ouvert sur des risques de publication.

## 5. Manques d'évidence / UNKNOWN

- Je n'ai pas mené de revue exhaustive fichier-par-fichier du code applicatif non documentaire.
- Les conclusions portent surtout sur les surfaces publiques et les risques systémiques visibles, pas sur chaque implémentation interne.

## 6. Recommandations

1. Maintenir la taxonomie corrigée entre Core et distribution code dans `README.md`, et éviter toute régression lors des prochaines mises à jour du classement.
2. Compléter le chemin "non-dev / opérateur" dans `GUIDE.md`: vocabulaire minimal, parcours en 5 étapes, et consignes de sécurité de base.
3. Fermer ou reclasser les risques P2 encore ouverts dans `docs/AUDIT_STATUS.md` avant communication publique: artefact orphelin, gating des outils qualité, couverture des distributions, et counters statiques.
4. Garder `LICENSE`, `CODE_OF_CONDUCT.md` et `CONTRIBUTING.md` comme socle public, puis alléger le README pour en faire la porte d'entrée, pas le manuel complet.

## 7. Handoff

- **Décisions à arbitrer** : jusqu'où simplifier le README sans perdre la rigueur Core/distribution.
- **Points de vigilance** : ne pas créer un nouveau protocole; privilégier une restructuration documentaire légère et cohérente.
