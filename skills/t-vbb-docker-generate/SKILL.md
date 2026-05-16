---
name: t-vbb-docker-generate
description: |
  Generates Docker infrastructure artifacts for a repository: Dockerfile
  (multi-stage), docker-compose files (dev, staging, prod), .env templates,
  .dockerignore, and Nginx reverse-proxy configuration. Requires prior audit
  from t-vbb-docker-audit. Modifies the repo by creating files.
  Keywords: docker generate, dockerfile creation, compose file generation,
  multi-environment docker, dev staging prod, nginx config, dockerignore,
  containerization.
version: "1.1"
phase: transverse
token_budget: medium
subagent_eligible: true
mode_sensitive: true
---

# Docker Generate — Artifact Creation

Référence standard : `0-vbb-standard`

Lire `skills/vibebackbone/docs/PILOTAGE.md` d'abord.
Lire `docs/PROJECT_MODE.md` si disponible.

Prérequis Vibebackbone : rapport d'audit Docker dans `docs/audits/docker-audit-*.md`.
Ce skill DOIT lire ce fichier. Il ne doit pas dépendre du contexte LLM seul.

## ROLE & POSTURE

Tu es un **générateur d'artefacts Docker** dans l'écosystème Vibebackbone.

Ton rôle est de transformer le bilan d'audit en fichiers d'infrastructure
Docker concrets, pour 3 environnements (Dev, Staging, Prod).

Tu ÉCRIS dans le repo — c'est un skill d'exécution.
Tu ne déploies PAS les conteneurs (→ `t-vbb-deploy-runtime`).
Tu valides la syntaxe de ce que tu génères.

Règles absolues :

1. **JAMAIS** de mot de passe réel dans les fichiers `.env` générés.
2. **JAMAIS** de Dockerfile sans utilisateur non-root.
3. **TOUJOURS** un `.dockerignore` cohérent.
4. **TOUJOURS** des compose files validables par `docker compose config`.
5. Rester **proportionné** : dev = simple, prod = sécurisé.

## INPUT CONTRACT

**Requis :**

- [ ] Rapport d'audit Docker dans `docs/audits/docker-audit-*.md` (généré par `t-vbb-docker-audit`)

**Optionnels :**

- [ ] `docs/PROJECT_MODE.md`
- [ ] Dockerfile existant (sera complété, pas écrasé sans confirmation)
- [ ] docker-compose*.yml existants (seront complétés)
- [ ] .gitignore existant (sera mis à jour via `edit`)

**Sources acceptées :** bilan d'audit, repo local, templates du skill

## BLOCKING CONDITIONS

- Si aucun rapport d'audit n'est trouvé dans `docs/audits/` → STOP. Message : "Exécuter `t-vbb-docker-audit` d'abord. Aucun rapport trouvé dans docs/audits/docker-audit-*.md."
- Si `.env.prod` contient des placeholders et que le mode cible est prod → STOP. Message : "Secrets non configurés en production."
- Si `docs/PROJECT_MODE.md` indique `frozen` → STOP. Message : "Projet en mode gelé."

## SCOPE

### Inclus

- Génération de `Dockerfile` multi-stage (si absent)
- Génération de `.dockerignore`
- Génération de `docker-compose.dev.yml`
- Génération de `docker-compose.staging.yml`
- Génération de `docker-compose.prod.yml`
- Génération de `.env.dev`, `.env.staging`, `.env.prod`, `.env.example`
- Mise à jour de `.gitignore` (via `edit`)
- Génération de `nginx/nginx.conf` + `nginx/security-headers.conf`
- Validation syntaxique des compose files générés

### Exclus

- Audit du repo (→ `t-vbb-docker-audit`)
- Cycle de déploiement, healthcheck, rollback (→ `t-vbb-deploy-runtime`)
- Audit sécurité détaillé (→ `2-vbb-security`)

## MATRICE DE DÉCISION D'ENVIRONNEMENT

| Critère | Dev | Staging | Prod |
|---|---|---|---|
| Build | Pas d'optimisation | Multi-stage | Multi-stage + squash |
| Volumes | Bind-mount (sync) | Named volumes | Named volumes + backup mount |
| Secrets | .env.dev en clair | .env.staging (warn) | Docker secrets / vault placeholders |
| Healthcheck | Désactivé | 30s interval | 15s interval |
| Restart | "no" | on-failure:3 | unless-stopped |
| Ressources | Unlimited | Limit mild | Limit strict + reservation |
| Réseau | Host/default | Bridge isolé | prod-frontend + prod-backend |
| Logging | Stdout | json-file 10m | json-file 50m + rotation |
| Sécurité | Standard | Standard | read_only + tmpfs + no-new-privileges |

## PROCESS

### Étape 1 — Lecture du rapport d'audit

Lire le rapport le plus récent dans `docs/audits/docker-audit-*.md`.

Si aucun fichier n'est trouvé, escalader vers `t-vbb-docker-audit` et STOP.

Extraire du rapport :
- Langage/framework
- Base image suggérée
- Zones de persistance
- Services requis
- Findings (P0 bloquants, P1 à prendre en compte)

Si le rapport contient des P0 non résolus → WARN et demander confirmation
avant de continuer (les P0 audit peuvent nécessiter une action corrective d'abord).

### Étape 2 — Dockerfile (si absent)

Si aucun Dockerfile n'a été détecté par l'audit, générer via `write` :

```dockerfile
# ─── Stage: builder ───
FROM <base_image> AS builder
# copie du lockfile AVANT les sources (cache layers)
# installation des dépendances + compilation

# ─── Stage: runtime ───
FROM <slim_image> AS runtime
# copie sélective des artefacts de builder
# USER non-root OBLIGATOIRE
# HEALTHCHECK (surcharge par compose)
```

Règles Dockerfile :
- Toujours `USER app` (ou équivalent non-root)
- Layers cachées : COPY lockfile avant sources
- HEALTHCHECK directive présente
- `.dockerignore` généré systématiquement

### Étape 3 — .dockerignore

Générer via `write` :

```gitignore
.git
.gitignore
node_modules
__pycache__
*.pyc
.env
.env.*
!.env.example
docker-compose*.yml
deploy.sh
backups/
*.md
.vscode
.idea
```

### Étape 4 — Compose files

Générer via `write` les 3 fichiers en respectant la matrice de décision.

**docker-compose.dev.yml** :
- Build context `.`, target adapté au hot-reload
- Bind-mount des sources (`./src:/app/src:cached`)
- Variables de `.env.dev`
- Ports exposés directement
- Command de dev avec hot-reload
- Pas de healthcheck
- `restart: "no"`
- Réseau default

**docker-compose.staging.yml** :
- Build multi-stage, target `runtime`
- Named volumes pour toutes les zones de persistance
- Variables de `.env.staging`
- Healthcheck : interval 30s, timeout 10s, retries 3, start_period 40s
- `restart: on-failure:3`
- Réseau `staging-net` (bridge isolé)
- Logging json-file max-size 10m, max-file 3
- `depends_on` avec `condition: service_healthy`

**docker-compose.prod.yml** :
- Build multi-stage, target `runtime`, image taggée
- Named volumes + `./backups:/backups`
- Variables de `.env.prod` — AUCUN secret en dur
- Healthcheck : interval 15s, timeout 5s, retries 3, start_period 30s
- `restart: unless-stopped`
- Réseau `prod-frontend` (nginx→app) + `prod-backend` (app→data)
- `deploy.resources.limits` + `reservations` stricts
- Logging json-file max-size 50m, max-file 5
- `read_only: true` + `tmpfs` + `security_opt: no-new-privileges:true`
- Service Nginx avec TLS termination

### Étape 5 — Environment files

Générer via `write` :

- `.env.dev` — variables en clair
- `.env.staging` — variables en clair, avertissement
- `.env.prod` — **tous les mots de passe en placeholders** `<CHANGE_ME_VAULT_OR_SECRETS>`
- `.env.example` — template commitable sans valeurs sensibles

### Étape 6 — Nginx configuration (prod)

Générer via `write` (ou copier depuis `skills/t-vbb-docker-generate/templates/`) :

- `nginx/nginx.conf` — reverse-proxy avec TLS, proxy_pass, WebSocket
- `nginx/security-headers.conf` — HSTS, X-Frame-Options, CSP, Permissions-Policy

### Étape 7 — .gitignore (mise à jour)

Utiliser `edit` pour ajouter au `.gitignore` existant :

```gitignore
# ─── t-vbb-docker-generate ───
.env.dev
.env.staging
.env.prod
backups/
```

Ne JAMAIS écraser le .gitignore existant — toujours `edit`.

### Étape 9 — Service map (pour deploy-runtime)

Générer via `write` le fichier `docker-services.map` à la racine du repo.
Ce fichier déclare explicitement les noms de services et leurs propriétés.
Il est lu par `deploy.sh` (généré par `t-vbb-deploy-runtime`) pour
éliminer toute heuristique de détection.

Format :

```yaml
# docker-services.map — généré par t-vbb-docker-generate
# Lu par deploy.sh — NE PAS MODIFIER MANUELLEMENT
app:
  name: <service_name>
  port: <port>
data:
  type: <postgres|mysql|sqlite|redis|none>
  name: <service_name>
  port: <port>
cache:
  type: <redis|memcached|none>
  name: <service_name>
  port: <port>
proxy:
  type: <nginx|caddy|traefik|none>
  name: <service_name>
  ports: [<http_port>, <https_port>]
volumes:
  named:
    - <volume_name>:<mount_point>
  bind:
    - <host_path>:<mount_point>
```

Règle : chaque champ `name` DOIT correspondre exactement au nom du
service dans le `docker-compose.prod.yml`.

### Étape 10 — Rapport de génération

Écrire un rapport dans `docs/audits/docker-generate-{YYYYMMDD-HHMM}.md`.

Ce rapport trace les décision architecturales prises par le skill :
- choix de la base image (builder + runtime)
- choix des ports
- choix des volumes (named vs bind, chemins)
- choix du réseau (bridge, isolé, etc.)
- pourquoi chaque service a été ajouté
- pourquoi chaque gate de sécurité a été configurée (ou omise en dev)

Format du rapport :

```markdown
# Génération Docker — {YYYY-MM-DD}

## Source
- Rapport d'audit lu : docs/audits/docker-audit-*.md
- Date de l'audit : {date}

## Décisions architecturales

| Décision | Choix | Justification |
|---|---|---|
| Base image builder | | |
| Base image runtime | | |
| Port app | | |
| Type DB | | |
| Port DB | | |
| Volumes persistants | | |
| Réseau prod | | |
| Nginx reverse-proxy | | |

## Fichiers générés

| Fichier | Statut | Validation compose |
|---|---|---|
| Dockerfile | créé/existant | N/A |
| docker-compose.dev.yml | créé | OK/FAIL |
| docker-compose.staging.yml | créé | OK/FAIL |
| docker-compose.prod.yml | créé | OK/FAIL |
| .env.dev | créé | N/A |
| .env.staging | créé | N/A |
| .env.prod | créé (placeholders) | N/A |
| docker-services.map | créé | N/A |

## Avertissements
- ...
```

### Étape 11 — Validation syntaxique

```bash
docker compose -f docker-compose.dev.yml config 2>&1
docker compose -f docker-compose.staging.yml config 2>&1
docker compose -f docker-compose.prod.yml config 2>&1
```

Si un compose file est invalide, corriger et re-valider.

## OUTPUT CONTRACT

Écrire UN rapport Markdown dans :
`docs/audits/docker-generate-{YYYYMMDD-HHMM}.md`

Puis mettre à jour `docs/AUDIT_STATUS.md` si le format du repo le prévoit.

Ce rapport est le **contrat d'entrée** pour `t-vbb-deploy-runtime`.

### Artefacts générés

```
<repo-root>/
├── Dockerfile                      # Multi-stage (généré si absent)
├── .dockerignore                   # Exclusions Docker
├── docker-compose.dev.yml          # Environnement Dev
├── docker-compose.staging.yml      # Environnement Staging
├── docker-compose.prod.yml         # Environnement Prod
├── docker-services.map             # Service map (lu par deploy.sh)
├── .env.dev                        # Variables Dev (non commité)
├── .env.staging                    # Variables Staging (non commité)
├── .env.prod                       # Variables Prod (secrets = placeholders)
├── .env.example                    # Template commitable
├── .gitignore                       # Mis à jour (append, pas overwrite)
├── nginx/
│   ├── nginx.conf                  # Reverse-proxy
│   └── security-headers.conf       # Headers sécurité
└── backups/
    └── .gitkeep
```

## VERDICT RULES

- `READY`
  - tous les artefacts générés
  - compose config valide pour les 3 environnements
  - .env.prod contient uniquement des placeholders
- `PARTIAL`
  - artefacts générés mais validation compose échoue sur 1+ env
  - Dockerfile existant non modifié (conflit potentiel)
- `BLOCKED`
  - rapport d'audit absent dans `docs/audits/`
  - projet en mode frozen
  - secrets prod déjà configurés avec de vrais mots de passe (risque de fuite)
- `UNKNOWN`
  - impossible de valider les compose files (Docker daemon inactif)
## SUPPORT BOUNDARY

Supporté :
- Mono-application avec 1-3 services de données (PostgreSQL, MySQL, Redis, SQLite)
- Nginx reverse-proxy pour production
- Multi-stage builds (builder + runtime)
- Hot-reload en dev pour les frameworks courants

Non supporté (refuser explicitement) :
- Monorepo multi-app avec >3 applications → message : "Un seul Dockerfile par exécution. Relancer pour chaque application."
- Orchestration K8s/Swarm/Nomad manifests → message : "Ce skill génère docker-compose, pas de manifests K8s."
- Windows containers → message : "Windows containers non supportés."
- Services avec dépendances stateful complexes (Kafka, Elasticsearch clusters, RabbitMQ clusters) → message : "Services stateful complexes non supportés. Configurer manuellement."
- Multi-architecture builds (arm64 + amd64) → message : "Multi-arch non supporté. Configurer buildx manuellement."
