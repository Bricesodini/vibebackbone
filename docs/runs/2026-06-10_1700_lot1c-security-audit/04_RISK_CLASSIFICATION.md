# 04_RISK_CLASSIFICATION — RUN 04A · Lot 1C : Classification des risques sécurité

**Date** : 2026-06-10  
**Voie** : AUDIT

---

## Carte des risques

| ID | Sévérité | Exploitabilité | Impact | Priorité remédiation |
|----|----------|---------------|--------|---------------------|
| SEC-005 | P2 | Moyenne (supply chain) | Critique (RCE via PyYAML compromis) | Haute |
| SEC-009 | P2 | Faible (nécessite compromission workflow) | Élevée (push malveillant au repo) | Haute |
| SEC-001 | P2 | Faible (nécessite contrôle PATH) | Moyenne (RCE lors de setup) | Moyenne |
| SEC-003 | P2 | Faible (nécessite accès physique au chemin) | Élevée (skills compromis) | Moyenne |
| SEC-007 | P2 | N/A (by design) | Moyenne (modification config agents) | Basse (documentaire) |
| SEC-002 | P3 | Très faible (variables codées en dur) | Faible (injection théorique) | Basse |
| SEC-004 | P3 | Très faible (nécessite concurrence) | Faible (symlink dangling) | Basse |
| SEC-006 | P3 | Faible (accès écriture tools/) | Élevée (RCE) | ACCEPTED_RISK |

---

## Risques acceptés

| ID | Raison d'acceptation |
|----|---------------------|
| SEC-006 | Mode DISTRIBUTION — pas de surface réseau. exec_module charge un fichier local du repo. Risque identique à l'exécution de n'importe quel script Python du repo. |
| SEC-008 | Par conception, les skills sont du texte injecté dans le contexte LLM. L'intégrité repose sur le contrôle d'accès git et la revue de PR. Ajouter des checksums serait utile mais pas critique en mode DISTRIBUTION. |

---

## Quick wins (remédiation facile)

| ID | Action | Effort |
|----|--------|--------|
| SEC-005 | Épingler `pyyaml>=6.0,<7.0` dans requirements.txt | 1 ligne |
| SEC-009 | Ajouter `permissions: contents: read` aux workflows | 2 lignes |
| SEC-001 | Remplacer `os.popen` par `datetime.now().strftime()` | 1 ligne |
| SEC-004 | Remplacer `rm && ln -s` par `ln -sf` | 2 lignes |

---

## Actions structurelles (remédiation plus longue)

| ID | Action | Effort |
|----|--------|--------|
| SEC-003 | Utiliser des symlinks relatifs ou ajouter vérification d'intégrité | Moyen |
| SEC-007 | Ajouter avertissement de confiance en début de setup.sh | Faible |
| SEC-002 | Refactoriser generate_prompt_commands sans eval | Moyen |