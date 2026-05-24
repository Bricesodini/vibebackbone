# 04_RISK_CLASSIFICATION — RUN 04B · Lot 1C : Classification dette technique

**Date** : 2026-06-10  
**Voie** : AUDIT

---

## Roadmap de remédiation

### Immediate (P2 — bloquante avant gros chantier)

| ID | Action | Effort | Impact |
|----|--------|--------|--------|
| TD-003 | Contractualiser 16 skills Phase 1 | Moyen | Passe de 22→38 contrats (66 %) |
| TD-006 | Créer test pour contract lint | Faible | Sécurise le gardien de qualité |
| TD-001 | Extraire blocs Python de setup.sh | Moyen | Réduit complexité, testabilité |
| TD-002 | Dédupliquer install/uninstall | Moyen | Réduit risque de divergence |

### Next (P3 — avant v1.0)

| ID | Action | Effort | Impact |
|----|--------|--------|--------|
| TD-005 | Corriger phase t-vbb-status-report | 1 ligne | Cohérence |
| TD-007 | Supprimer .bak | 1 commande | Propreté |
| TD-009 | Bump status-report v0.1→1.0 | 1 ligne | Cohérence |
| TD-010 | Créer test pour phase router | Faible | Couverture |
| TD-004 | Archiver 5 artefacts racine | Faible | Propreté |

### Later (ACCEPTED_RISK / cosmétique)

| ID | Action | Effort | Impact |
|----|--------|--------|--------|
| TD-008 | Documenter sections du deploy.sh template | Faible | Transparence |

---

## Dette acceptable

| Dette | Raison |
|-------|--------|
| TD-008 | Template distribué, pas du code exécuté par VBB. Complexité inhérente à un deploy script complet. |
| 0-vbb-guide/standard/pilotage en `0-` avec `phase: transverse` | Intentionnel (pré-condition, pas phase 0 opérationnelle). Documenté dans RUN 01. |

---

## Verdict prévu

**PARTIAL** — dette existe, bornée, lisible, actionnable. Plusieurs zones P2 nécessitent remédiation avant gros chantier. Le système reste compréhensible.