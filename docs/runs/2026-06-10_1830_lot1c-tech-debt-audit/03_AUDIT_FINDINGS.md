# 03_AUDIT_FINDINGS — RUN 04B · Lot 1C : Audit dette technique

**Date** : 2026-06-10  
**Voie** : AUDIT  
**Skill** : `1-vbb-tech-debt`

---

## TD-001 — setup.sh : monolithe de 652 lignes avec 8 blocs Python embarqués

| Champ | Valeur |
|-------|--------|
| **ID** | TD-001 |
| **Sévérité** | P2 |
| **Confiance** | high |
| **Zone** | setup.sh |
| **Fichier** | `setup.sh` |
| **Constat** | setup.sh est un monolithe de 652 lignes mêlant bash et 8 scripts Python embarqués (heredoc `<<'PY'`). Chaque bloc Python est responsable d'une opération différente (settings.json patch, CLAUDE.md patch, Codex compile, OpenCode config, etc.). Le script est difficile à tester, à maintenir et à déboguer. |
| **Impact** | Toute modification d'un provider nécessite de modifier setup.sh directement. Les blocs Python embarqués ne sont pas testables unitairement. Risque de régression élevé à chaque extension. |
| **Preuve** | 8 occurrences de `<<'PY'` / `PY`. Aucun test unitaire pour le script. 652 lignes, 9 `mkdir -p`, 7 `ln -s`. |
| **Recommandation** | Extraire les blocs Python en scripts séparés dans `tools/` (ex: `vbb-setup-claude.py`, `vbb-setup-codex.py`, etc.). Garder setup.sh comme orchestrateur qui appelle ces scripts. |
| **Statut** | OPEN |

---

## TD-002 — setup.sh : duplication install/uninstall

| Champ | Valeur |
|-------|--------|
| **ID** | TD-002 |
| **Sévérité** | P2 |
| **Confiance** | high |
| **Zone** | setup.sh |
| **Fichier** | `setup.sh` |
| **Constat** | La section install (lignes ~300-640) et la section uninstall (lignes ~162-295) connaissent les mêmes chemins de fichiers et la même logique de patch/revert. Si un provider est ajouté dans install mais oublié dans uninstall, l'utilisateur ne peut pas nettoyer complètement. |
| **Impact** | Divergence install/uninstall à chaque modification. Risque de résidus après uninstall. |
| **Preuve** | `CLAUDE_SETTINGS`, `CLAUDE_MD`, `CODEX_AGENTS`, `PI_AGENTS`, `OPENCODE_JSON` — déclarés deux fois chacun. |
| **Recommandation** | Centraliser les cibles de déploiement dans un tableau associatif ou un fichier de config. Installer et désinstaller par itération sur la même source de vérité. |
| **Statut** | OPEN |

---

## TD-003 — 36 skills sans CONTRACT.yaml (62 %)

| Champ | Valeur |
|-------|--------|
| **ID** | TD-003 |
| **Sévérité** | P2 |
| **Confiance** | high |
| **Zone** | skills/ |
| **Fichier** | N/A (36 dossiers) |
| **Constat** | 36 skills sur 58 n'ont pas de CONTRACT.yaml. Le runtime ne peut pas les vérifier mécaniquement. Les phases 1 (16 skills) et 4 (10 skills) sont entièrement sans contrats. |
| **Impact** | Aucune vérification mécanique possible pour 62 % des skills. Impossible de valider unitairement que les inputs/outputs sont respectés. |
| **Preuve** | `find skills -name CONTRACT.yaml | wc -l` = 22. `find skills -name SKILL.md | wc -l` = 58. 58 - 22 = 36. |
| **Recommandation** | Contractualiser les skills Phase 1 en priorité (16 skills). Puis Phase 4 (10 skills). Puis transverse restants. |
| **Statut** | OPEN |

---

## TD-004 — 5 artefacts de migration en racine du repo

| Champ | Valeur |
|-------|--------|
| **ID** | TD-004 |
| **Sévérité** | P3 |
| **Confiance** | high |
| **Zone** | Racine du repo |
| **Fichier** | `AGENTIC_PROTOCOL_REFORMAT_SUMMARY.md`, `CONTROL_AUDIT_PROMPTS_AGENTIC_MIGRATION.md`, `PROMPTS_AGENTIC_ALIGNMENT_AUDIT.md`, `PROMPTS_ALIGNMENT_DECISION.md`, `VIBEBACKBONE_AGENTIC_AUDIT.md` |
| **Constat** | 5 fichiers .md en racine sont des artefacts de cycles de migration complétés en mai 2026. Ils polluent la racine et ne servent plus de référence active. |
| **Impact** | Bruit dans la racine. Risque de confusion sur la source de vérité active. |
| **Preuve** | Ces fichiers contiennent "Statut: ✅ Complété" ou "Date: 2026-05-18". Leurs contenus sont archivés dans `docs/runs/`. |
| **Recommandation** | Déplacer dans `docs/archive/` ou `docs/runs/` correspondant. Garder la racine limitée à README, AGENTS, SYSTEM, GUIDE, CLAUDE, CONTRIBUTING, CHANGELOG, CODE_OF_CONDUCT, PROMPTS_ARCHITECTURE. |
| **Statut** | OPEN |

---

## TD-005 — 4 skills avec phase frontmatter ≠ préfixe de nom

| Champ | Valeur |
|-------|--------|
| **ID** | TD-005 |
| **Sévérité** | P3 |
| **Confiance** | high |
| **Zone** | skills/ |
| **Fichier** | `0-vbb-guide`, `0-vbb-pilotage`, `0-vbb-standard`, `t-vbb-status-report` |
| **Constat** | 3 skills en `0-vbb-*` ont `phase: transverse` (pas 0). 1 skill en `t-vbb-*` a `phase: 4` (pas transverse). Le préfixe et le frontmatter ne sont pas alignés. |
| **Impact** | Routage incorrect si le runtime utilise le préfixe pour déterminer la phase. Confusion pour les contributeurs. |
| **Preuve** | `0-vbb-guide/SKILL.md: phase: transverse`, `t-vbb-status-report/SKILL.md: phase: 4` |
| **Recommandation** | Corriger `t-vbb-status-report` phase → transverse (c'est un skill transverse par nom). Pour les 3 skills `0-vbb-*` méta, documenter que le préfixe 0- est intentionnel (pré-condition, pas phase 0 opérationnelle). |
| **Statut** | OPEN |

---

## TD-006 — Aucun test pour vbb-contract-lint.py

| Champ | Valeur |
|-------|--------|
| **ID** | TD-006 |
| **Sévérité** | P2 |
| **Confiance** | high |
| **Zone** | tests/ |
| **Fichier** | N/A (fichier manquant) |
| **Constat** | Le linter de contrats (`vbb-contract-lint.py`, 288 lignes) n'a aucun test unitaire. Le smoke test `smoke-contract-runtime.sh` le lance indirectement mais ne teste pas les cas négatifs (contrat invalide, référence cassée, dépendance circulaire). |
| **Impact** | Une régression dans le linter peut passer inaperçue jusqu'à merge. Surtout critique car le linter est le gardien de la qualité des 22 contrats. |
| **Preuve** | `find tests -name "*lint*"` → 0 résultats |
| **Recommandation** | Créer `tests/test_contract_lint.py` avec tests positifs et négatifs |
| **Statut** | OPEN |

---

## TD-007 — Fichier .bak non nettoyé

| Champ | Valeur |
|-------|--------|
| **ID** | TD-007 |
| **Sévérité** | P3 |
| **Confiance** | high |
| **Zone** | skills/vibebackbone/docs/ |
| **Fichier** | `skills/vibebackbone/docs/PILOTAGE.md.bak` (323 lignes) |
| **Constat** | Un fichier backup `.bak` est présent dans le repo versionné. C'est un résidu d'une édition précédente qui n'a pas été nettoyé. |
| **Impact** | Pollution du repo. Confusion potentielle sur la source de vérité (PILOTAGE.md vs PILOTAGE.md.bak). |
| **Preuve** | `find . -name "*.bak"` → 1 résultat |
| **Recommandation** | Supprimer le fichier .bak (git rm) |
| **Statut** | OPEN |

---

## TD-008 — deploy.sh template : 1303 lignes, complexité élevée

| Champ | Valeur |
|-------|--------|
| **ID** | TD-008 |
| **Sévérité** | P3 |
| **Confiance** | medium |
| **Zone** | skills/t-vbb-deploy-runtime/templates/ |
| **Fichier** | `skills/t-vbb-deploy-runtime/templates/deploy.sh` |
| **Constat** | Le template deploy.sh est un script de 1303 lignes. C'est le plus gros fichier du repo. Sa complexité rend l'audit et la maintenance difficiles. Cependant, c'est un template distribué, pas du code exécuté par vibebackbone lui-même. |
| **Impact** | Template difficile à auditer par les utilisateurs. Risque de bugs non testés dans les projets clients. |
| **Preuve** | `wc -l skills/t-vbb-deploy-runtime/templates/deploy.sh` = 1303 |
| **Recommandation** | Découper en modules (backup.sh, deploy.sh, healthcheck.sh) ou documenter les sections critiques. ACCEPTED_RISK si traité comme template à usage client. |
| **Statut** | ACCEPTED_RISK |

---

## TD-009 — t-vbb-status-report en version 0.1 (seul skill non aligné)

| Champ | Valeur |
|-------|--------|
| **ID** | TD-009 |
| **Sévérité** | P3 |
| **Confiance** | high |
| **Zone** | skills/t-vbb-status-report/ |
| **Fichier** | `skills/t-vbb-status-report/SKILL.md` |
| **Constat** | Seul skill à la version 0.1. Tous les autres sont en 1.0, 1.1, ou 2.0. La version 0.1 suggère un prototype non stabilisé. |
| **Impact** | Signal de maturité incohérent dans le catalogue. |
| **Preuve** | `grep "^version:" skills/*/SKILL.md | grep "0.1"` → 1 résultat |
| **Recommandation** | Évaluer si le skill est stable. Si oui, bump à 1.0. Si non, documenter les lacunes. |
| **Statut** | OPEN |

---

## TD-010 — Pas de test pour vbb-phase-router.py

| Champ | Valeur |
|-------|--------|
| **ID** | TD-010 |
| **Sévérité** | P3 |
| **Confiance** | high |
| **Zone** | tests/ |
| **Fichier** | N/A (fichier manquant) |
| **Constat** | Le phase router (`vbb-phase-router.py`) est testé indirectement via `smoke-contract-runtime.sh` mais n'a pas de test unitaire dédié. |
| **Impact** | Régression possible dans le routing des skills non détectée par CI. |
| **Preuve** | `find tests -name "*router*"` → 0 résultats |
| **Recommandation** | Créer `tests/test_phase_router.py` |
| **Statut** | OPEN |

---

## Résumé des findings

| ID | Sévérité | Confiance | Statut | Résumé |
|----|----------|-----------|--------|--------|
| TD-001 | P2 | high | OPEN | setup.sh monolithe (652 lignes, 8 blocs Python) |
| TD-002 | P2 | high | OPEN | setup.sh duplication install/uninstall |
| TD-003 | P2 | high | OPEN | 36/58 skills sans contrat (62 %) |
| TD-004 | P3 | high | OPEN | 5 artefacts migration en racine |
| TD-005 | P3 | high | OPEN | 4 skills phase/préfixe incohérents |
| TD-006 | P2 | high | OPEN | Pas de test pour contract lint |
| TD-007 | P3 | high | OPEN | 1 fichier .bak non nettoyé |
| TD-008 | P3 | medium | ACCEPTED_RISK | deploy.sh template 1303 lignes |
| TD-009 | P3 | high | OPEN | 1 skill en v0.1 |
| TD-010 | P3 | high | OPEN | Pas de test pour phase router |

**Distribution par sévérité** :
- P0 : 0
- P1 : 0
- P2 : 4 (TD-001, TD-002, TD-003, TD-006)
- P3 : 6 (TD-004, TD-005, TD-007, TD-009, TD-010 + TD-008 ACCEPTED_RISK)

**Aucun P0 ou P1.** La dette technique est réelle mais bornée — le système reste compréhensible et faisable à évoluer.