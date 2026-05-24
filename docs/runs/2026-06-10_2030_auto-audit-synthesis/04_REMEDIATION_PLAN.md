# 04_REMEDIATION_PLAN — RUN 05 : Plan de remédiation priorisé

**Date** : 2026-06-10  
**Voie** : AUDIT → CLÔTURE

---

## TOP 5 risques à traiter

| # | ID | Sévérité | Constat | Pourquoi |
|---|------|----------|---------|----------|
| 1 | SYNERGY-008 | P2 | 36/58 skills sans contrat | Plus grand gap structurel — sans contrats, le runtime est aveugle sur 62 % des skills |
| 2 | SYNERGY-004 | P2 | setup.sh monolithe | Concentrateur de risques (sécurité + dette), difficile à tester, risqué à modifier |
| 3 | SYNERGY-003 | P2 | Pas de tests lint/router | Le linter est le gardien de qualité — sans tests négatifs, faux PASS possibles |
| 4 | SYNERGY-001 | P2 | Workflows sans permissions | Sécurité CI — un workflow compromis peut modifier le repo |
| 5 | SYNERGY-009 | P2 | Incohérence CI locale/remote | Faux sentiment de confiance — local ≠ GitHub |

---

## TOP 5 quick wins

| # | ID | Action | Effort |
|---|------|--------|--------|
| 1 | SYNERGY-001 | Ajouter `permissions: contents: read` aux 2 workflows | 2 lignes |
| 2 | SYNERGY-002 | Épingler `pyyaml>=6.0,<7.0` | 2 lignes |
| 3 | SYNERGY-006 | Remplacer os.popen par datetime | 1 ligne |
| 4 | SYNERGY-012 | Remplacer `rm && ln -s` par `ln -sf` | 2 lignes |
| 5 | SYNERGY-010 | smoke.yml matrice OS | 5 lignes |

---

## TOP 5 chantiers structurels

| # | ID | Constat | Effort | Horizon |
|---|------|---------|--------|---------|
| 1 | SYNERGY-008 | Contractualiser 36 skills | Élevé | RUN 06D + itérations |
| 2 | SYNERGY-004 | setup.sh refactor en modules | Moyen | RUN 06C |
| 3 | SYNERGY-005 | Dédupliquer install/uninstall | Moyen | RUN 06C |
| 4 | SYNERGY-007 | Symlinks relatifs + intégrité | Moyen | RUN 07+ |
| 5 | SYNERGY-009 | Fusionner workflows, aligner CI | Moyen | RUN 06A |

---

## Roadmap de remédiation proposée

### RUN 06A — Quick wins sécurité/CI (1-2h)

Corriger en une passe les 5 quick wins + quick wins cosmétiques :
- SYNERGY-001 : permissions workflows
- SYNERGY-002 : PyYAML pinning
- SYNERGY-006 : os.popen → datetime
- SYNERGY-012 : ln -sf
- SYNERGY-010 : smoke.yml matrice OS
- SYNERGY-014 : t-vbb-status-report phase
- SYNERGY-015 : supprimer .bak
- SYNERGY-016 : bump v0.1→1.0
- SYNERGY-017 : cache pip
- SYNERGY-018 : filtre branche
- SYNERGY-019 : matrice Python

**11 corrections, toutes ≤ 5 lignes chacune.**

### RUN 06B — Tests négatifs lint/router (2-3h)

Créer :
- `tests/test_contract_lint.py` — tests positifs + négatifs pour le linter
- `tests/test_phase_router.py` — tests positifs + négatifs pour le router

Résout SYNERGY-003.

### RUN 06C — setup.sh hardening (3-4h)

- SYNERGY-004 : Extraire 8 blocs Python en `tools/vbb-setup-*.py`
- SYNERGY-005 : Centraliser les cibles pour install/uninstall
- SYNERGY-011 : Supprimer eval(), remplacer par retours stdout
- SYNERGY-013 : Archiver 5 artefacts migration

### RUN 06D — Contractualisation progressive (itératif)

- Lot 1 : contractualiser 16 skills Phase 1
- Lot 2 : contractualiser 10 skills Phase 4
- Lot 3 : contractualiser 10 skills transverse restants
- Résout SYNERGY-008

### RUN 07+ — Structurels long terme

- SYNERGY-007 : Symlinks relatifs + vérification intégrité
- SYNERGY-009 : Fusionner workflows CI
- SYNERGY-021 : Intégrité des skills ( Accepté pour l'instant)

---

## Après RUN 06A : verdict attendu

Si RUN 06A est exécuté avec succès :
- 10 P3 corrigés → 0 P3 remaining (hors ACCEPTED_RISK)
- 2 P2 corrigés (SYNERGY-001, SYNERGY-002) → 7 P2 remaining
- 3 ACCEPTED_RISK unchanged

Couverture contrats : 22/58 → inchangé (RUN 06D nécessaire)