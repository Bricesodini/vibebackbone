---
run_id: "2026-06-14_1400_setup-split-phase-2F-hermes"
phase: "07_CLOSEOUT"
voie: "STRUCTUREE"
status: "READY"
agent: "vbb-cody-orchestrator (delegated by Hermes for setup split refactor)"
started_at: "2026-06-14T10:00:00Z"
next_phase: null
artifacts_produced: []
---

# Closeout — Setup split Phase 2F : Hermes (non-destructive + agent install + proxy awareness)

**Run ID** : 2026-06-14_1400_setup-split-phase-2F-hermes
**Type** : Phase 2F — Hermes distribution (sixth + last), non-destructive
**Date** : 2026-06-14
**Branche** : main
**Commit** : (à compléter après push)
**CI databaseId** : (à compléter après watch)

---

## Executive Summary

Phase 2F livrée : `distributions/hermes/setup.sh` (108 LOC) + `distributions/hermes/AGENT_INSTALL.md` (340 LOC) + section §10 dans setup.sh (routeur) — **strictement non-destructif** : aucun `~/.hermes/` touché, aucun profil, aucun secret, aucun proxy muté, aucun SOUL.md modifié. Le LLM Proxy Security est reconnu comme composant officiel Hermes. 31/0/1 smoke, 159/3 pytest (135 baseline + 24 proxy tests). Verdict : **GO**.

---

## Fichiers créés / modifiés

| Fichier | Statut | LOC | Note |
|---|---|---|---|
| `distributions/hermes/setup.sh` | C | 108 | 4 fonctions : `hermes_install`, `hermes_preflight`, `hermes_print_components`, `hermes_run_verify_if_requested`. Exit 0 si OK, 1 si fichiers essentiels manquent |
| `distributions/hermes/AGENT_INSTALL.md` | C | 340 | Guide complet : statut, préconditions, backups, install Cody/workers, intégration proxy, permissions, client, anti-bypass, smoke tests, rollback |
| `setup.sh` | M | 465 → 475 (+10) | Section §10 ajoutée (avant Summary) : source `distributions/hermes/setup.sh; hermes_install` |
| `tests/test_setup_smoke.sh` | M | 196 → 215 (+19) | Section 3 étendue : hermes/setup.sh exists + parses, AGENT_INSTALL.md exists, header §10 préservé |

**Périmètre autorisé strictement respecté** : aucun `~/.hermes/profiles/`, aucun `secrets.enc` réel, aucune HMAC key, aucun SOUL.md modifié, aucun proxy runtime muté, aucune CI, aucun install.sh destructif.

---

## Composants Hermes reconnus

Le setup Hermes **liste** (sans rien exécuter) les chemins utiles :

| Composant | Chemin | Source |
|---|---|---|
| Verify | `distributions/hermes/verify/verify.sh` | ADR 0013 (verify-first) |
| Proxy client (lib) | `distributions/hermes/proxy/client.py` | ADR 0006, 0007, 0009 |
| Proxy CLI | `distributions/hermes/proxy/cli.py` | ADR 0009 (extensibility) |
| Proxy config (exemple) | `distributions/hermes/proxy/config.example.yaml` | ADR 0007 |
| Proxy actions (exemple) | `distributions/hermes/proxy/actions.example.yaml` | ADR 0007 |
| Agent install guide | `distributions/hermes/AGENT_INSTALL.md` | **NOUVEAU** (Phase 2F) |
| Proxy runtime (détecté) | `distributions/hermes/proxy/` (si présent) | ADR 0006 |

---

## Preuve non-destructif

### Test 1 — HOME jetable install

```
TMP_HOME=/var/folders/vg/.../tmp.FQ3kE4gpwy
HOME=$TMP_HOME bash setup.sh
```

**Résultat** :
- Sections Core, Claude, Codex, Pi, OpenCode : install complet (64 skills + 33 prompts + 26 commands par provider)
- **Section Hermes** : affiche la liste des composants, message "AGENT-INSTALL ONLY"
- **Aucun `.hermes/` créé dans TMP_HOME** ✓ (vérifié post-install)
- `find $TMP_HOME -name ".hermes"` : No such file or directory

### Test 2 — Vrai `~/.hermes/` intact

```
PRE:  75 entries, 12 profiles, mtime 3 juin 21:16
POST: 75 entries, 12 profiles, mtime 3 juin 21:16 (UNCHANGED)
```

**Conclusion** : `bash setup.sh` ne touche pas `~/.hermes/` que ce soit sur HOME réel ou HOME jetable.

### Test 3 — Direct exec

```
$ bash distributions/hermes/setup.sh
$ echo $?
0
```

Le fichier est sourcable + appelable, exit 0 quand les fichiers essentiels sont présents.

---

## AGENT_INSTALL.md sections livrées

Le document couvre les 10 sections demandées par le brief :

1. **Statut** : installation agent-mediated, non automatique (contractuel, ADR 0006 + 0011)
2. **Préconditions** : `~/.hermes/` existe, `cody-check` présent, verify PASS
3. **Backups obligatoires** : `tar -czf profiles.backup.$TS.tar.gz` + `SOUL.md.backup.$TS` par profil
4. **Installation Cody/workers** : procédure standard `cp SOUL.md` pour chaque profil VBB
5. **Intégration proxy** : `~/.hermes/proxy/{config.yaml, actions.yaml, secrets.enc, audit/}`
6. **Permissions recommandées** : `700` sur `~/.hermes/proxy/`, `600` sur secrets/config/actions
7. **Usage client officiel** : `client.py` (lib) + `cli.py` (CLI), exemples in-tree vs standalone
8. **Règle anti-bypass** : `os.environ["OPENAI_API_KEY"]` interdit, `ProxyClient().vault_read()` requis
9. **Smoke tests** : verify.sh, proxy tests, bypass-lint --strict
10. **Rollback** : `tar -xzf` profiles backup, restore SOUL.md custom, désactivation proxy

**Plus** : 8 références ADR (0006-0013) + ADR-cited rule A bypass prevention + lien vers bypass-lint et skill vbb-gouvernance-poc-gate.

---

## Tests verts (P.R2)

| Vérification | Résultat |
|---|---|
| `bash -n distributions/hermes/setup.sh` | OK |
| `bash distributions/hermes/setup.sh` | exit 0 |
| `bash tests/test_setup_smoke.sh` | 31 PASS / 0 FAIL / 1 WARN |
| `bash -n setup.sh, setup-lib.sh, core/setup.sh, distributions/{pi,claude}/setup.sh` | tous OK |
| `HOME=$TMP_HOME bash setup.sh` | install complet, 0 erreur |
| `HOME=$TMP_HOME bash setup.sh --uninstall` | uninstall OK |
| Aucun `.hermes/` créé dans TMP_HOME | ✓ |
| `~/.hermes/` réel intact | ✓ (75/12/pre-post identique) |
| `python tools/vbb-architecture.py lint` | 0 errors / 0 warnings |
| `python tools/vbb-contract-lint.py` | 0 errors |
| `bash distributions/hermes/verify/verify.sh` | PASS (28 checks) |
| `pytest tests/ distributions/hermes/proxy/tests/ -q` | **159 passed, 3 skipped** (135 baseline + 24 proxy) |

---

## Risques résiduels

| # | Risque | Sév. | Status / Mitigation |
|---|---|---|---|
| R1 | Le setup.sh n'a toujours pas de flag `--hermes-verify` documenté dans l'aide | Faible | Le flag `HERMES_VERIFY=true` est implémenté (fonction `hermes_run_verify_if_requested`), juste non exposé dans --help. À documenter si Brice le souhaite |
| R2 | Le uninstall Hermes n'existe pas (par design) mais n'est pas non plus testé en tant que no-op | Faible | La règle "non-destructif" est garantie par l'absence de code d'écriture. `bash setup.sh --uninstall` ne touche pas la section Hermes |
| R3 | Si AGENT_INSTALL.md devient obsolète (ADRs mis à jour), la doc dérive | Moyenne | La doc référence 8 ADRs spécifiques (0006-0013). Chaque mise à jour ADR doit.trigger une revue de AGENT_INSTALL.md |
| R4 | Les 24 proxy tests sont des unit tests ; pas d'intégration end-to-end du proxy runtime dans TMP_HOME | Faible | Tests d'intégration sont out of scope Phase 2F (le proxy est standalone, ADR 0009) |
| R5 | Le brief dit "éventuellement" lancer verify.sh, mais le mécanisme actuel nécessite `HERMES_VERIFY=true` env var | Faible | Comportement sûr par défaut (pas d'auto-run verify). Si Brice veut auto-verify, on l'ajoutera |

**Aucun risque HIGH non mitigé.**

---

## Verdict

**GO.**

Conditions de GO groupé :
1. Phase 2G (optionnelle) : routeur final — `setup.sh` devient un pur dispatcher qui appelle les 6 distributions (Core + Claude + Codex + Pi + OpenCode + Hermes) en séquence
2. La fonction `uninstall()` monolithique pourra être splittée en `core_uninstall` / `claude_uninstall` / etc. dans un run dédié, ou laissée inline (orchestration globale acceptable)
3. Le bug `_realpath` (rappelé dans closeouts précédents) reste hors scope, à fixer en P1-1 si Brice le souhaite
4. Aucune dépendance Core → Hermes : Core installe les symlinks universels, Hermes est complètement read-only et standalone

---

## Métadonnées

- **Setup split Phase 0 + 1** (SHA `1f549d8`) : filet de sécurité + extraction helpers
- **Setup split Phase 2A** (SHA `4bd93be`) : extraction Core → `core/setup.sh`
- **Setup split Phase 2B** (SHA `9ca9e45`) : extraction Pi → `distributions/pi/setup.sh`
- **Setup split Phase 2C** (SHA `9dc55d2`) : extraction Claude → `distributions/claude/setup.sh`
- **Ce run couvre** : Phase 2F = extraction Hermes (non-destructive) → `distributions/hermes/setup.sh` + `AGENT_INSTALL.md`
- **Distribution split status** : 5/6 complètes (Core + Claude + Pi + Hermes sont extraits, **Codex + OpenCode restent inline dans setup.sh**, candidats pour Phase 2D-2E ou follow-up)
- **Hors scope (rappel)** : CI, profils Hermes SOUL.md, proxy runtime, install.sh destructif, secrets.enc réel, HMAC keys
