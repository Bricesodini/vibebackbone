# Hermes / Cody — Agent-Mediated Installation Guide

**Status**: AGENT-INSTALL ONLY — never auto-installed by `bash setup.sh`.
**Audience**: Vibebackbone operator (human) with full shell access to `~/.hermes/`.
**Read first**: this file, end-to-end, before touching anything.

---

## 1. Statut : installation agent-mediated, non automatique

`bash setup.sh` ne touche **jamais** `~/.hermes/`. Cette décision est
contractuelle (ADR 0006 + ADR 0011) et défendue par
`distributions/hermes/bypass-lint/`. L'installation Hermes/Cody est
délibérément **médiée par l'opérateur** pour :

- garder le contrôle sur les profils (`SOUL.md`)
- garder le contrôle sur les secrets (`secrets.enc`, HMAC keys)
- permettre un rollback déterministe
- auditer chaque mutation avant qu'elle ne touche le runtime

**Conséquence** : le seul fichier qui doit changer dans `~/.hermes/`
est celui que tu décides explicitement de changer, à la main.

---

## 2. Préconditions Hermes/Cody

Avant toute installation, vérifier :

- [ ] `~/.hermes/` existe (sinon : `mkdir -p ~/.hermes` n'est **pas**
      recommandé ; installer Hermes CLI d'abord via ta méthode habituelle)
- [ ] `~/.hermes/bin/cody-check` est présent et exécutable
      (sinon : `bash distributions/hermes/verify/verify.sh` doit FAIL)
- [ ] `~/.hermes/profiles/` existe (sinon : `mkdir -p ~/.hermes/profiles`)
- [ ] Python 3.10+ disponible (`python3 --version`)
- [ ] `bash distributions/hermes/verify/verify.sh` retourne `RESULT: PASS`
      (sinon : STOP — ne pas continuer, le diagnostic verify doit d'abord
      être vert)

**Sanity check rapide** (non-destructif) :

```bash
bash distributions/hermes/verify/verify.sh
```

Si exit code ≠ 0 : ne pas continuer. Lire le diagnostic.

---

## 3. Backups obligatoires de `~/.hermes/profiles/`

**Avant** toute copie de profil VBB vers `~/.hermes/profiles/`, faire :

```bash
# 1. Backup horodaté de tous les profils existants
TS=$(date +%Y%m%d-%H%M%S)
tar -czf ~/.hermes/profiles.backup.$TS.tar.gz -C ~/.hermes profiles/
echo "Backup: ~/.hermes/profiles.backup.$TS.tar.gz"

# 2. Snapshot des SOUL.md actuels (lisibles par humain)
for p in ~/.hermes/profiles/*/; do
    if [ -f "$p/SOUL.md" ]; then
        cp "$p/SOUL.md" "$p/SOUL.md.backup.$TS"
    fi
done
```

**Politique de rétention** : garder les 5 derniers backups, purger
les plus vieux via cron ou manuellement. Les backups ne doivent
**jamais** quitter la machine (pas de cloud, pas de NAS non chiffré).

---

## 4. Installation Cody / workers

Les profils VBB vivent dans `~/.hermes/profiles/`. Voici la procédure
standard (cf. ADR 0006 §"Profile distribution") :

```bash
# Pour chaque profil VBB
for prof in vbb-cody-orchestrator vbb-fast-worker vbb-struct-worker \
            vbb-audit-worker vbb-close-worker; do
    mkdir -p ~/.hermes/profiles/$prof
    # Copier le SOUL.md depuis ce repo
    cp ~/.hermes/profiles/cody/SOUL.md ~/.hermes/profiles/$prof/SOUL.md 2>/dev/null \
        || echo "⚠ pas de SOUL.md de base pour $prof — voir ADR 0006"
done
```

**Alternative** (recommandée pour un setup initial propre) : utiliser
le mécanisme de `vbb-profiles.yaml` (registre des profils) et laisser
Cody orchestrator copier depuis le repo, pas depuis un profil existant.

⚠ **Ne jamais écraser un SOUL.md existant sans backup.** Si le profil
cible a déjà un SOUL.md custom, comparer d'abord (diff), fusionner
manuellement si besoin.

---

## 5. Intégration proxy

Le LLM Proxy Security est un composant officiel de la distribution
Hermes. Il détient les credentials cloud, n'expose que des ordres
abstraits, et refuse les lectures directes (cf. ADR 0006, 0007, 0008,
0011).

### 5.1 Fichiers à créer dans `~/.hermes/proxy/`

```bash
mkdir -p ~/.hermes/proxy/audit
# Config runtime (depuis l'exemple du repo)
cp distributions/hermes/proxy/config.example.yaml ~/.hermes/proxy/config.yaml
# Actions whitelist (depuis l'exemple du repo)
cp distributions/hermes/proxy/actions.example.yaml ~/.hermes/proxy/actions.yaml
# Secrets : NE PAS créer à la main — utiliser le client proxy
# (voir 5.2)
```

### 5.2 Premier secrets.enc via le client

**À ne jamais faire** : créer `secrets.enc` ou une HMAC key à la main.
Le client proxy fournit une commande dédiée :

```bash
# POC : stub-backed, NE PAS utiliser en prod
python distributions/hermes/proxy/cli.py init-secrets
# Production (quand le daemon tourne) :
# python distributions/hermes/proxy/cli.py init-secrets --keyfile ~/.hermes/proxy/master.key
```

Le client :
- génère la HMAC key (libsodium SecretStream prioritaire, AES-256-GCM fallback)
- chiffre le payload
- écrit `secrets.enc` en 600
- crée `audit/` en 700

### 5.3 Audit directory

```bash
# Création à la première utilisation
mkdir -p ~/.hermes/proxy/audit
# Vérification après utilisation
ls -la ~/.hermes/proxy/audit/
```

---

## 6. Permissions recommandées

| Path | Mode | Owner | Justification |
|---|---|---|---|
| `~/.hermes/proxy/` | `700` | user | dir proxy sensible |
| `~/.hermes/proxy/secrets.enc` | `600` | user | chiffré mais défense en profondeur |
| `~/.hermes/proxy/config.yaml` | `600` | user | contient endpoints + mode config |
| `~/.hermes/proxy/actions.yaml` | `600` | user | whitelist d'actions, lecture seule runtime |
| `~/.hermes/proxy/audit/` | `700` | user | logs d'audit, jamais world-readable |
| `~/.hermes/profiles/*/SOUL.md` | `644` | user | documents, pas de secrets |
| `~/.hermes/profiles/*/SOUL.md.backup.*` | `600` | user | backups, defense in depth |

**Vérification** (à relancer après chaque install) :

```bash
chmod 700 ~/.hermes/proxy/
chmod 600 ~/.hermes/proxy/secrets.enc ~/.hermes/proxy/config.yaml ~/.hermes/proxy/actions.yaml
chmod 700 ~/.hermes/proxy/audit/
find ~/.hermes/proxy/ -type d -exec chmod 700 {} \;
find ~/.hermes/proxy/ -type f -exec chmod 600 {} \;
```

Si une de ces permissions est plus large (`755`, `644`) : le bypass-lint
peut le détecter, ou à défaut, le reverifier manuellement.

---

## 7. Usage client officiel

Tous les workers VBB doivent passer par le **client proxy** pour
accéder aux credentials cloud. Les clients officiels sont :

- **Lib Python** (programmatique) : `distributions/hermes/proxy/client.py`
- **CLI** (ligne de commande) : `distributions/hermes/proxy/cli.py`

### 7.1 Exemple CLI

```bash
# Lecture d'un secret (POC : stub-backed)
python distributions/hermes/proxy/cli.py vault_read <secret_id>

# Liste des actions autorisées
python distributions/hermes/proxy/cli.py list_actions

# Status du daemon (si actif)
python distributions/hermes/proxy/cli.py status
```

### 7.2 Exemple lib

```python
from distributions.hermes.proxy.client import ProxyClient

client = ProxyClient(config_path="~/.hermes/proxy/config.yaml")
secret = client.vault_read("openai_api_key")
```

### 7.3 Standalone vs in-tree

Le client peut s'utiliser :

- **In-tree** (depuis le repo VBB) : chemin absolu, OK pour dev/POC
- **Standalone** (production) : `pip install -e distributions/hermes/proxy/`
  puis import classique. Voir ADR 0009 §"Extensibility".

---

## 8. Règle anti-bypass

**Contract** (ADR 0011) : aucun worker, agent ou code VBB ne lit
**jamais** directement :

- variables d'env contenant des secrets (`OPENAI_API_KEY`, etc.)
- fichiers `secrets.enc`, `config.yaml`, `actions.yaml`
- sorties de commandes SSH/NAS/cloud qui retournent des credentials
- sorties d'autres agents (Cody, sub-delegates) qui contiennent des secrets

**Toute lecture doit passer par le client proxy.** Cette règle est
défendue par `distributions/hermes/bypass-lint/`.

### Pattern interdit

```python
# ❌ INTERDIT — bypass direct
import os
api_key = os.environ["OPENAI_API_KEY"]

# ❌ INTERDIT — lecture directe du secret store
with open(os.path.expanduser("~/.hermes/proxy/secrets.enc"), "rb") as f:
    raw = f.read()
```

### Pattern correct

```python
# ✅ CORRECT — via le client proxy
from distributions.hermes.proxy.client import ProxyClient

client = ProxyClient()
api_key = client.vault_read("openai_api_key")
```

### Détection

- Linter : `python tools/vbb-bypass-lint.py` (ou équivalent dans
  `distributions/hermes/bypass-lint/`)
- Audit READ-ONLY : tout chemin de code qui touche un secret sans
  passer par le client est un bypass, à signaler immédiatement

---

## 9. Smoke tests

Trois niveaux de vérification, à relancer après chaque install :

### 9.1 verify.sh (non-destructif)

```bash
bash distributions/hermes/verify/verify.sh
# Attendu : RESULT: PASS (28 checks)
```

### 9.2 Proxy tests (unit tests du runtime)

```bash
cd distributions/hermes/proxy/
python -m pytest tests/ -q
# Attendu : tous tests verts (61/61 en POC, plus en prod)
```

### 9.3 bypass-lint (anti-bypass)

```bash
python distributions/hermes/bypass-lint/lint.py --strict
# Attendu : 0 CRITICAL, 0 HIGH
# (mode report par défaut, --strict pour fail-on-CRITICAL)
```

Si l'un de ces trois FAIL : STOP, ne pas continuer l'install, lire
le diagnostic, fixer la racine.

---

## 10. Rollback

En cas d'install ratée, le rollback est **complet et déterministe** :

### 10.1 Restaurer les profils

```bash
# Trouver le backup le plus récent
ls -t ~/.hermes/profiles.backup.*.tar.gz | head -1
# Restaurer
tar -xzf ~/.hermes/profiles.backup.<TS>.tar.gz -C ~/.hermes/
```

### 10.2 Restaurer les SOUL.md custom

```bash
# Pour chaque profil qui avait un backup
for p in ~/.hermes/profiles/*/; do
    backup=$(ls -t "$p"/SOUL.md.backup.* 2>/dev/null | head -1)
    if [ -n "$backup" ]; then
        cp "$backup" "$p/SOUL.md"
    fi
done
```

### 10.3 Désactiver le proxy

```bash
# Si le daemon tourne
pkill -f "proxy/daemon.py" 2>/dev/null
# Supprimer les fichiers proxy
rm -rf ~/.hermes/proxy/
# Restaurer les permissions par défaut
chmod 755 ~/.hermes/
```

### 10.4 Vérifier que rien d'autre n'a changé

```bash
# Snapshot avant/après install (utiliser git, mtime, ou stat)
find ~/.hermes -newer /tmp/hermes-pre-install-marker -type f
# Tout fichier listé doit être attendu (proxies, profiles, audit logs)
```

---

## Références

- **ADR 0006** : Architecture LLM Proxy (VibeBackbone/transverse)
- **ADR 0007** : Credentials management
- **ADR 0008** : Failover multi-providers
- **ADR 0009** : Extensibility du client
- **ADR 0010** : Security model
- **ADR 0011** : Bypass prevention (rule A — repo governance)
- **ADR 0012** : Révision sécurité D1-D7
- **ADR 0013** : Distribution structure (Hermes verify/install deferred per F-015)
- **Skill** : `vbb-gouvernance-poc-gate` (mode advisory opt-in)
- **Linter** : `distributions/hermes/bypass-lint/`
- **Smoke** : `tests/test_setup_smoke.sh` (Couvre les 5 sections + Hermes ajouté en Phase 2F)

---

**Dernière mise à jour** : 2026-06-14 (Phase 2F)
**Statut** : LIVRÉ, AGENT-INSTALL ONLY
