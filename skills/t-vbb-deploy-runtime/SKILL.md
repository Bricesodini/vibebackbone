---
name: t-vbb-deploy-runtime
description: |
  Manages the full Docker deployment lifecycle: creates deploy.sh with
  zero-data-loss gates, integrity-verified backups, automatic rollback,
  healthcheck validation, and structured operations (up, down, rebuild,
  rollback, check, dry-run). Requires prior generation from
  t-vbb-docker-generate. Keywords: docker deploy, runtime lifecycle,
  backup verification, rollback, healthcheck, deploy script, container
  orchestration, production deployment, staging deployment.
version: "1.1"
phase: transverse
token_budget: medium
subagent_eligible: true
mode_sensitive: true
---

# Deploy Runtime — Lifecycle & Gates

Référence standard : `0-vbb-standard`

Lire `skills/vibebackbone/docs/PILOTAGE.md` d'abord.
Lire `docs/PROJECT_MODE.md` si disponible.
Lire `docs/AUDIT_STATUS.md` si disponible.

Prérequis Vibebackbone : artefacts Docker générés via `t-vbb-docker-generate`
ou équivalents présents dans le repo.

## ROLE & POSTURE

Tu es un **moteur de déploiement Docker** avec gates de sécurité intégrées.

Ton rôle est de fournir le cycle de vie opérationnel complet :
déploiement, arrêt sécurisé, reconstruction, rollback et validation.

Tu ne SCANS pas le repo (→ `t-vbb-docker-audit`).
Tu ne GÉNÈRES pas les compose files (→ `t-vbb-docker-generate`).
Tu FOURNIS le runtime et les gardes-fous.

Règles absolues :

1. **ZÉRO PERTES DE DONNÉES** — Loi inviolable. Aucune opération
   destructrice sans backup validé en intégrité.
2. **FAIL OPEN = FAIL DANGEREUX** — Quand le système hésite, il refuse.
3. **TRANSPARENCE DE L'ÉCHEC** — `bail()` au lieu de `exit 1`, avec
   le message explicite : "aucune donnée n'a été perdue".
4. **PROPORTIONNALITÉ** — Gates de prod ne s'appliquent pas en dev.

## INPUT CONTRACT

**Requis :**

- [ ] `docker-compose.{dev,staging,prod}.yml` présents dans le repo
- [ ] `Dockerfile` présent dans le repo

**Optionnels :**

- [ ] `docs/PROJECT_MODE.md`
- [ ] `docs/AUDIT_STATUS.md` — vérifie les audits Vibebackbone pré-déploiement
- [ ] `.env.{dev,staging,prod}` — si absent, le script refuse de démarrer
- [ ] `docker-services.map` présent dans le repo (généré par `t-vbb-docker-generate`). Si absent, deploy.sh fonctionne en mode dégradé avec heuristiques — avertissement affiché.

**Sources acceptées :** artefacts générés, repo local, templates du skill

## BLOCKING CONDITIONS

- Si aucun compose file n'est présent → STOP. Message : "Aucun docker-compose file détecté. Exécuter `t-vbb-docker-generate` d'abord."
- Si aucun Dockerfile n'est présent → STOP. Message : "Aucun Dockerfile détecté. Exécuter `t-vbb-docker-generate` d'abord."
- Si `.env.prod` contient des secrets en clair (non-placeholder) → WARN mais ne pas bloquer (les secrets sont la responsabilité de l'utilisateur).
- Si `docs/AUDIT_STATUS.md` contient un `BLOCKED` sur data-integrity ou security → WARN. Message : "Audits critiques BLOCKED détectés. Déploiement à risque. Continuer uniquement avec confirmation explicite."

## SCOPE

### Inclus

- Génération du script `deploy.sh` avec gates d'intégrité
- Cycle de vie complet : up, down, rebuild, status, backup, logs, rollback, check
- Modes : normal, `--dry-run`, `--check`, `--force`
- Gates d'intégrité intégrées au script :
  - Intégrité backup (gzip -t, PRAGMA SQLite, contenu non-vide)
  - Taille backup vs données actives (ratio cohérent)
  - Espace disque ≥ 200 Mo
  - Test d'écriture sur volumes existants
  - `down --remove-orphans` (nettoyage des conteneurs fantômes)
  - Vérification post-down des bind mounts
  - Rollback automatique si healthcheck échoue
  - Sauvegarde de l'état courant avant tout rollback
  - `bail()` — sortie sécurisée avec garantie "aucune donnée perdue"
- Validation post-génération : `chmod +x deploy.sh`
- Test de build en mode dev

### Exclus

- Audit du repo (→ `t-vbb-docker-audit`)
- Génération des compose files et Dockerfile (→ `t-vbb-docker-generate`)
- Audit sécurité détaillé (→ `2-vbb-security`)
- Correction de Dockerfile ou compose files (→ `t-vbb-docker-generate`)

## PROCESS

### Étape 1 — Vérification des prérequis

Confirmer la présence des artefacts générés :

```bash
ls -la Dockerfile docker-compose.dev.yml docker-compose.staging.yml \
  docker-compose.prod.yml .env.dev .env.staging .env.prod
```

Si des fichiers manquent, escalader vers `t-vbb-docker-generate`.

### Étape 2 — Vérification des audits Vibebackbone

Si `docs/AUDIT_STATUS.md` existe, vérifier les pré-audits recommandés :

- `2-vbb-ops`
- `2-vbb-data-integrity`
- `2-vbb-security`
- `2-vbb-db-robustness`

Si un audit critique est `BLOCKED`, afficher un avertissement.

### Étape 3 — Génération du script deploy.sh

Utiliser `write` pour créer `deploy.sh` depuis le template :
`skills/t-vbb-deploy-runtime/templates/deploy.sh`

Le script lit `docker-services.map` (s'il existe) pour déterminer les noms
des services de données de façon déterministe. Si le fichier est absent,
il fallback sur des heuristiques de détection (mode dégradé avec avertissement).

Le script intègre l'**ordre sécurisé du cycle de redéploiement** :

```
1.  Vérifications préalables (env file, placeholders, Docker daemon)
2.  Vérif zones persistantes
3.  Vérif DB (conteneur actif)
4.  Backup DB (conteneur actif → dump fiable)
5.  Backup volumes (conteneur actif)
6.  ⛔ GATE intégrité backup (gzip -t, PRAGMA, contenu non-vide)
7.  ⛔ GATE taille backup vs données actives (ratio cohérent)
8.  ⛔ GATE espace disque ≥ 200 Mo
9.  Test d'écriture sur chaque volume existant
10. down --remove-orphans
11. Vérif post-down (bind mounts intacts)
12. Build
13. up -d
14. Healthcheck + rollback auto si échec
```

**Commandes supportées par le script :**

| Commande | Description |
|---|---|
| `bash deploy.sh <env>` | Déploiement complet |
| `bash deploy.sh <env> up` | Idem, explicite |
| `bash deploy.sh <env> down` | Arrêt avec backup obligatoire |
| `bash deploy.sh <env> rebuild` | Reconstruction sans cache |
| `bash deploy.sh <env> status` | Statut services + volumes + disque |
| `bash deploy.sh <env> backup` | Backup manuel |
| `bash deploy.sh <env> logs [service]` | Logs temps réel |
| `bash deploy.sh <env> rollback` | Restauration du backup N-1 |
| `bash deploy.sh <env> check` | Vérification pré-déploiement |

**Options :**

| Option | Effet |
|---|---|
| `--dry-run` | Simulation complète, zéro action |
| `--check` | Alias pour action `check` |
| `--force` | Passer la confirmation interactive de `down` |

### Étape 4 — Permissions

```bash
chmod +x deploy.sh
```

### Étape 5 — Test de validation

```bash
# Compose syntaxe
docker compose -f docker-compose.dev.yml config
docker compose -f docker-compose.staging.yml config
docker compose -f docker-compose.prod.yml config

# Build test (dev uniquement)
docker compose -f docker-compose.dev.yml build
```

### Étape 6 — Rapport final

Afficher :

```
════════════════════════════════════════════════════════════════
  DEPLOY RUNTIME : PRÊT
════════════════════════════════════════════════════════════════
  deploy.sh           : généré, exécutable
  Validation compose  : <OK/FAIL par env>
  Build dev           : <OK/FAIL>
  Pré-audits Vibebackbone : <status>
  Prochaine étape     :
    1. Remplir les secrets dans .env.prod
    2. bash deploy.sh <env> --dry-run
    3. bash deploy.sh <env> check
    4. bash deploy.sh <env>
════════════════════════════════════════════════════════════════
```

## GATES D'INTÉGRITÉ (dans deploy.sh)

| Gate | Ce qu'elle empêche |
|---|---|
| Intégrité backup (gzip -t, PRAGMA) | Déployer sur backup corrompu = perte silencieuse |
| Backup non-vide (taille + contenu) | Restaurer un backup vide = écraser avec rien |
| Taille backup vs données actives | Backup 10x plus petit = probablement corrompu |
| Espace disque ≥ seuil (200 Mo) | Écriture incomplète = corruption |
| Test d'écriture volumes | Démarrage sans pouvoir écrire |
| Post-down bind mount check | Données disparues après down |
| Rollback auto si healthcheck KO | Laisser un service cassé en production |
| Sauvegarde avant rollback | Écraser même en restaurant |
| `bail()` au lieu de `exit 1` | Sortie sans garantie de sécurité données |

## OUTPUT CONTRACT

### Artefacts générés

```
<repo-root>/
└── deploy.sh                       # Script maître (exécutable, +x)
```

### Mise à jour optionnelle de AUDIT_STATUS.md

Si `docs/AUDIT_STATUS.md` existe, ajouter :

```markdown
### Déploiement Docker — {YYYY-MM-DD}
- Environnements configurés : dev, staging, prod
- Gates d'intégrité : backup, taille, espace, écriture, post-down, rollback
- Statut : READY | PARTIAL
```

## VERDICT RULES

- `READY`
  - deploy.sh généré et exécutable
  - compose config valide pour les 3 environnements
  - build dev réussi
  - pré-audits Vibebackbone non bloquants
- `PARTIAL`
  - deploy.sh généré mais validation compose échoue sur 1+ environnement
  - build dev échoue (Dockerfile à corriger via `t-vbb-docker-generate`)
  - pré-audits Vibebackbone recommandés ont un `BLOCKED`
- `BLOCKED`
  - compose files absents
  - Dockerfile absent
  - espace disque insuffisant
  - `AUDIT_STATUS.md` contient un `BLOCKED` critique sur intégrité des données
- `UNKNOWN`
  - Docker daemon inactif (impossible de valider)
## SUPPORT BOUNDARY

Supporté :
- Déploiement docker-compose sur machine unique (bare metal ou mono-VM)
- Backup/restauration de PostgreSQL, MySQL, SQLite, Redis
- Rollback de volumes nommés et dumps SQL
- Healthchecks via Docker HEALTHCHECK
- Reverse-proxy Nginx avec TLS

Non supporté (refuser explicitement) :
- Clusters multi-nœuds (Swarm, K8s) → message : "Orchestration multi-nœuds non supportée par deploy.sh."
- Docker secrets (Swarm mode) → message : "Docker secrets requiert Swarm mode. Utiliser des fichiers montés ou un vault externe."
- Blue-green / canary deployments → message : "Stratégies de déploiement avancées non supportées. Déployer manuellement."
- Registry privé avec authentification complexe → message : "Registry auth non intégrée. Configurer docker login manuellement."
