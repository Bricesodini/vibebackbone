# 02_DISCOVERY — RUN 04A · Lot 1C : Zone d'analyse sécurité

**Date** : 2026-06-10  
**Voie** : AUDIT  
**Skill** : `2-vbb-security`

---

## Fichiers analysés

| Fichier | Lignes | Risque potentiel |
|---------|--------|-----------------|
| `setup.sh` | 652 | Écriture dans $HOME, symlinks, embedded Python, eval, os.popen |
| `scripts/install-vbb-pre-commit.sh` | 49 | Écriture dans .git/hooks/, exécution Python via hook |
| `scripts/vbb-ci-local.sh` | 75 | Exécution tools, faible risque |
| `.github/workflows/vbb-contracts.yml` | 23 | CI, injection de dépendances |
| `.github/workflows/smoke.yml` | 10 | CI, install test |
| `tools/vbb-contract-lint.py` | 288 | Lecture fichiers, YAML parsing |
| `tools/vbb-contract-runtime.py` | ~410 | exec_module, subprocess, écriture traces |
| `tools/vbb-loop-closure-check.py` | ~200 | Lecture artefacts de run |
| `tools/vbb-phase-router.py` | ~150 | Routing, import dynamique |
| `tools/vbb-project-init.py` | ~200 | Écriture fichiers dans projets cibles |
| `requirements.txt` | 1 | PyYAML non épinglé |
| `AGENTS.md` | ~250 | Instructions agent LLM |
| `SYSTEM.md` | ~120 | Instructions agent LLM |

---

## Entry points identifiés

1. **`setup.sh`** — Script exécuté par l'utilisateur, écrit dans `$HOME`, crée des symlinks, modifie des configs
2. **Pre-commit hook** — Exécuté automatiquement par git, lance Python
3. **GitHub Actions** — Exécuté sur push/PR
4. **LLM agent instructions** — AGENTS.md + SYSTEM.md injectés dans le contexte des agents
5. **Contract runtime** — `vbb-contract-runtime.py` utilise `exec_module` pour charger dynamiquement

---

## Trust boundaries

```
User → setup.sh → $HOME (fs write)
User → git commit → pre-commit hook → Python execution
External contributor → PR → GitHub Actions → repo
LLM agent → AGENTS.md/SYSTEM.md read → agent behavior
Tools → YAML parsing (PyYAML) → potential unsafe load
```

---

## Zones NON analysées (UNKNOWN)

- `tests/smoke-contract-runtime.sh` — Écrit des traces en `docs/audits/vbb-runtime/` (non critique mais side effect)
- `providers/` — Contenu inconnu, non analysé en détail
- Templates nginx dans `t-vbb-deploy-runtime/templates/` — Hors scope (modèle, pas du code exécuté ici)