---
name: t-vbb-docker-audit
description: |
  Scans a Git repository for Docker readiness: detects Dockerfiles, identifies
  persistence zones (databases, SQLite, uploads), maps service dependencies,
  and produces a structured audit report. Read-only — never modifies the repo.
  Use before any Docker generation or deployment. Keywords: docker audit,
  dockerfile detection, persistence mapping, volume identification,
  containerization assessment, service dependency mapping.
version: "1.1"
phase: transverse
token_budget: low
subagent_eligible: true
mode_sensitive: false
---

# Docker Audit — Read-Only Repository Scan

Référence standard : `0-vbb-standard`

Lire `skills/vibebackbone/docs/PILOTAGE.md` d'abord.
Lire `docs/PROJECT_MODE.md` si disponible.

## ROLE & POSTURE

Tu es un **auditeur d'infrastructure Docker** en lecture seule.

Ton rôle est de scanner le dépôt, d'identifier les artefacts Docker existants,
de cartographier les zones de persistance et de produire un bilan structuré.

Tu ne MODIFIES PAS le dépôt.
Tu ne GÉNÈRES PAS de fichiers.
Tu OBSERVES et tu RAPPORTE.

Règles absolues :

- READ-ONLY — aucune écriture dans le repo
- NO assumptions — si un Dockerfile est absent, le dire explicitement
- Evidence required — chaque identification doit être sourcée
- UNKNOWN autorisé — si les preuves sont insuffisantes

## INPUT CONTRACT

**Requis :**

- [ ] Un dépôt Git local accessible

**Optionnels :**

- [ ] `docs/PROJECT_MODE.md`
- [ ] `docs/SESSION.md`
- [ ] Dockerfiles existants dans le repo
- [ ] docker-compose*.yml existants
- [ ] Fichiers de configuration de persistance (DB configs, etc.)

**Sources acceptées :** repo local, fichiers de config, lockfiles, CI config

## BLOCKING CONDITIONS

- Si le dépôt est inaccessible ou vide → STOP. Message : "Dépôt inaccessible ou vide. Audit Docker impossible."
- Si aucune application identifiable (aucun lockfile, aucun Dockerfile, aucun manifeste) → STOP. Message : "Aucun point d'entrée identifiable. Fournir au minimum un Dockerfile ou un manifeste de dépendances."
- Si l'audit est demandé sur un dépôt qui n'est pas le working directory → signaler le chemin et demander confirmation.

## SCOPE

### Inclus

- Détection de Dockerfiles existants (`Dockerfile`, `Dockerfile.*`, `*.dockerfile`)
- Détection de compose files existants (`docker-compose*.yml`, `compose*.yml`)
- Identification du langage/framework dominant (lockfiles, manifests)
- Cartographie des zones de persistance :
  - Bases de données (PostgreSQL, MySQL, SQLite, Redis, MongoDB)
  - Fichiers SQLite (`*.db`, `*.sqlite`, `*.sqlite3`)
  - Répertoires d'uploads/assets (`uploads/`, `public/`, `media/`, `data/`, `static/`)
  - Configuration runtime (`.env`, `config.yaml`, `settings.json`)
- Identification des dépendances de service (app → data → reverse-proxy)
- Vérification de la compatibilité Docker de l'application détectée
- Vérification de l'espace disque disponible

### Exclus

- Génération de Dockerfile ou compose files (→ `t-vbb-docker-generate`)
- Déploiement ou cycle de vie (→ `t-vbb-deploy-runtime`)
- Audit sécurité détaillé (→ `2-vbb-security`)
- Audit robustesse DB (→ `2-vbb-db-robustness`)
- Audit intégrité données métier (→ `2-vbb-data-integrity`)

## PROCESS

### Étape 1 — Scan des artefacts Docker

Outils : `bash` (find, grep)

```bash
# Dockerfiles existants
find . -maxdepth 4 -name "Dockerfile*" -o -name "*.dockerfile" 2>/dev/null

# Compose files existants
find . -maxdepth 3 -name "docker-compose*.yml" -o -name "compose*.yml" 2>/dev/null

# .dockerignore
find . -maxdepth 1 -name ".dockerignore" 2>/dev/null
```

### Étape 2 — Identification du langage/framework

Outils : `bash` (find)

```bash
find . -maxdepth 2 \( -name "package.json" -o -name "requirements.txt" \
  -o -name "go.mod" -o -name "Cargo.toml" -o -name "pom.xml" \
  -o -name "Gemfile" -o -name "pubspec.yaml" -o -name ".netlify.toml" \) 2>/dev/null
```

Déduire :
- Image de base suggérée
- Besoin de multi-stage build
- Commande de développement (hot-reload)
- Port d'écoute par défaut

### Étape 3 — Cartographie de la persistance

Outils : `read` (fichiers de config), `bash` (find, grep)

1. **Bases de données** : Chercher les configs de connexion dans les
   fichiers de configuration de l'application.
2. **SQLite** : Chercher les fichiers `*.db`, `*.sqlite`, `*.sqlite3`.
3. **Uploads/Assets** : Chercher les répertoires de fichiers statiques.
4. **Configuration runtime** : Chercher les `.env`, `config.yaml`, `settings.json`.

### Étape 4 — Carte des services

À partir des étapes 1-3, construire la carte des services :

- **Service principal** : L'application (type, port, commande start)
- **Services de données** : PostgreSQL / MySQL / SQLite / Redis selon dépendances
- **Service reverse-proxy** : Nginx (nécessaire en prod seulement)
- **Services complémentaires** : Sidecars, workers, etc.

### Étape 5 — Vérifications environnementales

```bash
# Docker daemon actif ?
docker info >/dev/null 2>&1

# Espace disque
df -P . | awk 'NR==2 {print $4}'

# Git disponible
git rev-parse --is-inside-work-tree 2>/dev/null
```

### Étape 6 — Bilan d'audit

Produire le bilan structuré ET écrire le rapport dans `docs/audits/docker-audit-{YYYYMMDD-HHMM}.md`
selon le template défini dans OUTPUT CONTRACT.

Ce fichier est le **contrat d'entrée obligatoire** pour `t-vbb-docker-generate`.
Sans ce fichier, le skill generate DOIT refuser de s'exécuter.

## OUTPUT CONTRACT

Assurer l'existence de `docs/audits/`.

Écrire UN rapport Markdown dans :
`docs/audits/docker-audit-{YYYYMMDD-HHMM}.md`

Puis mettre à jour `docs/AUDIT_STATUS.md` si le format du repo le prévoit.

Ce rapport est le **contrat d'entrée obligatoire** pour `t-vbb-docker-generate`.
Le skill generate DOIT lire ce fichier — il ne doit pas dépendre du contexte LLM seul.

Chaque finding doit inclure :

- ID `DOCK-XX`
- sévérité `P0/P1/P2`
- finding
- evidence
- impact
- action recommandée

Le rapport doit suivre le template :

```markdown
# Audit Docker — {YYYY-MM-DD}

## Bilan

| Critère | Valeur |
|---|---|
| Langage/Framework | |
| Dockerfile existant | oui/non, chemin |
| Compose files | liste ou aucun |
| .dockerignore | présent/absent |
| Docker daemon | actif/inactif |
| Espace disque | Mo disponibles |

## Persistance

| Zone | Type | Chemin config |
|---|---|---|
| Bases de données | | |
| SQLite | | |
| Uploads/Assets | | |
| Config runtime | | |

## Services requis

| Service | Type | Port |Dépendances |
|---|---|---|---|
| App | | | |
| Data | | | |
| Reverse-proxy | | | |

## Base image suggérée

| Champ | Valeur |
|---|---|
| Image builder | |
| Image runtime | |
| Multi-stage | oui/non |

## Findings

### DOCK-XX : {titre}
- **Sévérité** : P0/P1/P2
- **Finding** : ... 
- **Evidence** : ...
- **Impact** : ...
- **Action** : ...
```

## VERDICT RULES

- `READY`
  - application identifiable
  - persistance cartographiée
  - Docker daemon actif
  - espace disque suffisant
- `PARTIAL`
  - application identifiée mais persistance partiellement cartographiée
  - Docker daemon inactif (audit possible, déploiement bloqué)
- `BLOCKED`
  - aucune application identifiable
  - espace disque inférieur à 200 Mo
- `UNKNOWN`
  - preuves insuffisantes pour identifier les dépendances ou la persistance
## SUPPORT BOUNDARY

Supporté :
- Dépôts mono-application avec 1-3 services de données (PostgreSQL, MySQL, Redis, SQLite)
- Dépôts avec Dockerfile existant (audit des artefacts existants)
- Dépôts avec docker-compose*.yml existants
- Langages/frameworks courants : Node.js, Python, Go, Rust, Java, Ruby, Flutter/Dart

Non supporté (refuser explicitement) :
- Monorepo multi-app avec >3 applications Docker → message : "Architecture multi-app non supportée. Auditer chaque application séparément."
- Windows containers → message : "Windows containers non supportés."
- Orchesrateurs K8s/Swarm/Nomad → rediriger vers outils spécialisés
- Dépôts sans aucun manifeste de dépendances ni Dockerfile → BLOCKED
