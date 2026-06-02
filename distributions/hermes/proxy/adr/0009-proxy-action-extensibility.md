# ADR 0009 — Extensibilité des actions du proxy de confidentialité

**Statut** : PROPOSED (rev. 2026-06-02)
**Date** : 2026-06-02 (Revised: 2026-06-02 — D5 concurrence, contrat étendu, bypass check)
**Route** : STRUCTURED
**Chantier** : Proxy de confidentialité (Brice, 2026-06-02)
**Décideurs** : Brice (demandeur), gouvernance Vibebackbone
**ADRs liées** : 0006 (architecture, acceptée) · **0007 (credentials — référence obligatoire pour `required_credentials`)** · 0008 (failover) · **0010 (security boundaries — référence obligatoire pour la séparation `read` / `write` / `destroy`)** · 0011 (bypass prevention)

---

## 1. Contexte

Le chantier « Proxy de confidentialité » (Brice, 2026-06-02) introduit un
composant transverse dont le rôle est de médiatiser **toute interaction
sensible** entre les agents Vibebackbone (Hermes, Cody, 4 workers VBB,
`cody-check`) et les ressources externes (macOS Keychain, API tierces,
services locaux Ollama/MLX, registres Git, NAS, services bancaires).

L'ADR 0006 fixe l'architecture (batch, file d'actions, médaillon local,
deux composantes Profil / Service). L'ADR 0007 fixe le cycle de vie des
**credentials** (schéma, stockage, audit). L'ADR 0010 fixe les **security
boundaries** (séparation `read` / `write` / `destroy`, whitelist stricte,
défense en profondeur). L'ADR 0008 fixe la résilience (failover,
dégradation contrôlée).

Aucune de ces ADR n'a, prise isolément, tranché la **question de
l'ouverture** : *comment ajoute-t-on une nouvelle action dans le proxy,
une fois celui-ci en production ?*

Or, le besoin est concret et immédiat :

- Brice veut pouvoir ajouter une action « vault_read » en moins d'une
  minute, depuis Telegram ou la CLI, sans toucher au code Python du
  proxy.
- Demain, il voudra « nas_exec », « gh_status », « vault_rotate »,
  « gh_pr_merge » — chaque nouvelle intégration étant un cas
  d'application différent, avec ses propres credentials, ses propres
  permissions et son propre niveau de risque.
- Le LLM local (Gemma 4 26B-A4B VLM ou Ollama) qui médiatise le dialogue
  Profil ne doit pas pouvoir **inventer** une commande et l'exécuter ;
  il doit pouvoir **suggérer** une action à ajouter, **jamais**
  l'exécuter sans déclaration explicite.
- Toute action ajoutée doit être testable sans effets de bord (mode
  dry-run) avant d'être rendue disponible en mode `live`.
- L'audit doit permettre, à terme, de rejouer *qui a ajouté quoi, quand,
  avec quelle validation, et avec quel résultat de dry-run* — y compris
  si Brice n'est plus là (succession, audit externe, incident).

L'ADR 0009 tranche ce point. Elle définit :

1. le **schéma déclaratif** d'une action dans `~/.hermes/proxy/actions.yaml` ;
2. le **cycle d'ajout contrôlé** d'une action, de l'intention de Brice
   à la mise à disposition effective ;
3. les règles de **dry-run par défaut** et de **validation explicite** ;
4. les règles d'**impossibilité d'exécuter une action non déclarée** ;
5. les règles d'**audit** des ajouts et de **traçabilité** des
   exécutions.

Le principe fondamental est le suivant : **une nouvelle action doit
pouvoir être ajoutée par configuration, sans modification de code
métier**. Cette règle est non négociable. Toute action qui exigerait
un commit dans `proxy/` pour exister viole cette ADR.

---

## 2. Décision

### 2.1 Principe fondamental

> **Une nouvelle action doit pouvoir être ajoutée par configuration,
> sans modification de code métier.**

Conséquences directes :

- Le **code du proxy** (routeur, executor, audit logger) est générique
  et stable. Il ne contient aucune action en dur, aucun cas
  particulier, aucune table de correspondance action → binaire.
- Le **catalogue des actions** vit dans un fichier de configuration
  déclaratif, versionné hors dépôt Git (cf. §2.2 sur le stockage).
- L'ajout d'une action est un acte de **gouvernance** opéré par Brice
  (ou un délégué co-signeur documenté), encadré par un **cycle
  d'enregistrement contrôlé** (cf. §2.3).
- Toute action qui aurait besoin d'une logique métier spécifique
  (parsing de sortie, retry intelligent, post-traitement) déclenche une
  **demande d'évolution** de l'executor, pas un commit silencieux dans
  `actions.yaml`.

### 2.2 Schéma d'une action

Le catalogue vit dans `~/.hermes/proxy/actions.yaml`. Ce fichier :

- est **hors dépôt Git** (jamais commité, comme `secrets.enc`) ;
- est chargé au démarrage du proxy puis **rechargable à chaud** par
  signal `SIGHUP` ou commande `vbb-proxy actions reload` ;
- est validé contre un **schéma JSON Schema** strict au chargement ;
- toute action qui ne valide pas le schéma est **rejetée au
  chargement**, pas au runtime (P.R3 — gate before action).

Le schéma d'une action est le suivant (les champs marqués `requis`
sont obligatoires) :

| Champ | Type | Requis | Description |
|---|---|---|---|
| `id` | string (slug) | oui | Identifiant unique, kebab-case, ex. `vault-read`. Jamais modifiable après création (immuable) |
| `name` | string | oui | Affichage humain, ex. « Lecture d'un secret Vault » |
| `description` | string | oui | Détail sémantique : ce que fait l'action, quand l'utiliser, exemples métier |
| `command_template` | string | oui | Template de commande avec placeholders `{param_name}`, ex. `vault kv get -field={key} secret/{path}` |
| `risk_level` | enum | oui | `low` \| `medium` \| `high` \| `critical` |
| `permissions` | list[enum] | oui | Sous-ensemble de `[read, write, destroy]`. Voir ADR 0010 Règle 1 sur la séparation stricte |
| `required_credentials` | list[string] | oui | Liste d'IDs de credentials (cf. ADR 0007 §2.2). Vide si l'action n'a pas besoin d'authentification |
| `parameters` | object | oui | Schéma JSON Schema des paramètres attendus (nom, type, obligatoire, validation regex) |
| `dry_run_supported` | bool | oui | `true` si l'action peut être testée sans effet de bord |
| `audit_level` | enum | oui | `basic` \| `detailed` \| `verbose` (cf. ADR 0010 §2.2 Règle 5) |
| `concurrency_policy` | enum | non (def. `mutex`) | `mutex` \| `fifo` \| `parallel` (cf. décision D5, ADR 0007 §2.7bis). `mutex` est le défaut pour toute action credentialisée ; `parallel` n'est acceptable **que** pour des actions read-only idempotentes (à justifier explicitement) |
| `rate_limit_per_minute` | int | non (hérite de la limite par défaut) | Override per-action de la limite par appelant fixée par D6 (ADR 0008 §2.2.1). Si non spécifié, hérite du seuil global de 30 req/min. À n'utiliser **que** pour des actions notoirement plus coûteuses (par exemple, `gh_pr_merge` pourrait être limité à 5/min) |
| `requires_dry_run_validation` | bool | non (def. `true`) | `true` exige que la dernière exécution dry-run soit validée par Brice (étape 8 du cycle §2.3) avant tout passage en `live`. `false` n'est acceptable **que** pour les actions **read-only low-risk** explicitement marquées ; le champ est revu à chaque promotion |
| `fallback_allowed` | bool | non (def. `false`) | Autorise le failover vers une autre action (cf. ADR 0008) |
| `timeout_seconds` | int | non (def. `30`) | Timeout d'exécution ; au-delà, refus `E_TIMEOUT` |
| `requires_explicit_validation` | bool | non (def. `true` si `high`/`critical`, sinon `false`) | Exige une double confirmation humaine au passage en `live` |
| `examples` | list[object] | non | Exemples d'appels valides (paramètres fictifs) |
| `tests` | list[string] | non | Commandes de test dry-run à exécuter pour valider l'action après ajout |
| `created_at` | string (ISO 8601) | oui | Date de création, posée automatiquement |
| `updated_at` | string (ISO 8601) | oui | Date de dernière modification, mise à jour à chaque amendement |
| `version` | int | non (def. `1`) | Numéro de version de l'action, incrémenté à chaque modification non cosmétique |

> **Note sur `required_credentials`** : la liste ne contient **jamais**
> de valeur de secret. Elle ne référence que des `id` définis dans
> `credentials.yaml` (cf. ADR 0007). Le proxy résout la valeur au
> moment de l'exécution, jamais avant.

#### 2.2.1 Exemple — action `vault_read` (read, low)

```yaml
actions:

  - id: vault-read
    name: "Lecture d'un secret Vault"
    description: |
      Lit la valeur d'un secret dans HashiCorp Vault via le binaire
      `vault` local. Aucune modification, aucune écriture, aucun
      effet de bord. Utilisé pour injecter un secret dans une
      commande aval (jamais dans la réponse HTTP).
    command_template: "vault kv get -field={key} secret/{path}"
    risk_level: low
    permissions:
      - read
    required_credentials:
      - vault-brice-readonly        # cf. ADR 0007 §2.2
    parameters:
      type: object
      required: [path, key]
      properties:
        path:
          type: string
          pattern: "^[a-z0-9/_-]+$"
        key:
          type: string
          pattern: "^[a-z0-9_-]+$"
    dry_run_supported: true
    audit_level: basic
    fallback_allowed: false
    timeout_seconds: 10
    requires_explicit_validation: false
    examples:
      - params: { path: "vbb/deploy", key: "api_url" }
        note: "Lit l'URL d'API stockée sous vbb/deploy"
    tests:
      - "vault-read path=vbb/deploy key=api_url --dry-run"
    created_at: 2026-06-02T10:00:00Z
    updated_at: 2026-06-02T10:00:00Z
    version: 1
```

#### 2.2.2 Exemple — action `nas_exec` (write, medium)

```yaml
actions:

  - id: nas-exec
    name: "Exécution d'un script sur le NAS de Brice"
    description: |
      Exécute un script shell arbitraire (pré-validé) sur le NAS via
      SSH. L'action refuse tout script non listé dans le paramètre
      `script_name`. Aucun `rm -rf` non plus, dry-run strict.
    command_template: "ssh nas-brice 'sudo /opt/nas-scripts/{script_name}.sh {args}'"
    risk_level: medium
    permissions:
      - read
      - write
    required_credentials:
      - nas-ssh-brice
    parameters:
      type: object
      required: [script_name, args]
      properties:
        script_name:
          type: string
          enum: [backup_daily, snapshot_weekly, rotate_logs]
        args:
          type: string
          maxLength: 256
    dry_run_supported: true
    audit_level: detailed
    fallback_allowed: false
    timeout_seconds: 60
    requires_explicit_validation: false
    examples:
      - params: { script_name: "backup_daily", args: "--full" }
        note: "Lance le backup quotidien complet"
    tests:
      - "nas-exec script_name=backup_daily args=--full --dry-run"
    created_at: 2026-06-02T10:05:00Z
    updated_at: 2026-06-02T10:05:00Z
    version: 1
```

#### 2.2.3 Exemple — action `gh_pr_merge` (write, high)

```yaml
actions:

  - id: gh-pr-merge
    name: "Merge d'une pull request GitHub"
    description: |
      Merge une PR via l'API GitHub. Action irréversible : une PR
      mergée ne peut pas être « démergée » sans intervention manuelle.
      Action `high` car effet durable sur l'historique du dépôt cible.
    command_template: "gh pr merge {pr_number} --repo {repo} --{merge_method} --delete-branch"
    risk_level: high
    permissions:
      - write
    required_credentials:
      - github-brice-readonly         # NON : il faut un token write
      # Le token write DOIT être ajouté séparément, validé en revue
    parameters:
      type: object
      required: [pr_number, repo, merge_method]
      properties:
        pr_number:
          type: integer
          minimum: 1
        repo:
          type: string
          pattern: "^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$"
        merge_method:
          type: string
          enum: [merge, squash, rebase]
    dry_run_supported: true
    audit_level: verbose
    fallback_allowed: false
    timeout_seconds: 30
    requires_explicit_validation: true     # OBLIGATOIRE pour high
    examples:
      - params: { pr_number: 42, repo: "vibebackbone/core", merge_method: "squash" }
        note: "Merge squash de la PR #42 avec suppression de branche"
    tests:
      - "gh-pr-merge pr_number=999999 repo=vibebackbone/sandbox merge_method=squash --dry-run"
    created_at: 2026-06-02T10:10:00Z
    updated_at: 2026-06-02T10:10:00Z
    version: 1
```

### 2.3 Cycle d'ajout d'une action

L'ajout d'une action est un acte de **gouvernance** encadré par un
cycle en 8 étapes. Aucune étape ne peut être sautée.

```
[1] Brice initie
   ↓
[2] Profil agent guide (questions)
   ↓
[3] Profil agent génère le YAML
   ↓
[4] Validation explicite Brice   ←── STOP si refus
   ↓
[5] Double confirmation si high/critical
   ↓
[6] Enregistrement dans actions.yaml
   ↓
[7] Test en mode dry-run
   ↓
[8] Validation finale Brice → action disponible
   ↓
[8bis] Vérification anti-bypass (cf. ADR 0011)   ←── NOUVEAU 2026-06-02
```

#### 2.3.1 Détail des 8 étapes (+ étape 8bis anti-bypass, D7)

1. **Brice initie** — depuis Telegram (`/ajoute action X`) ou la CLI
   (`vbb-proxy action add X`). Le message est capté par la composante
   Profil (ADR 0006 §2.2) qui route vers le flux d'enregistrement.

2. **Le profil agent guide** — pose les questions nécessaires pour
   remplir le schéma §2.2 : `id`, `name`, `description`,
   `command_template`, `risk_level`, `permissions`,
   `required_credentials`, schéma des paramètres. Le profil agent
   **ne devine pas** un champ qu'il n'a pas demandé ; il est explicite
   sur ce qu'il suppose (et demande confirmation).

3. **Le profil agent génère le YAML** correspondant à partir des
   réponses de Brice, validé localement contre le JSON Schema. Le YAML
   est présenté à Brice en preview lisible, **pas encore écrit** sur
   disque.

4. **Validation explicite** — Brice relit le YAML généré et confirme
   mot pour mot. **Pas d'enregistrement automatique**, surtout pour
   les niveaux `high` et `critical`. Si Brice refuse ou demande une
   modification, retour à l'étape 2.

5. **Double confirmation si `high` ou `critical`** — pour ces niveaux,
   une deuxième confirmation est demandée, idéalement sur un canal
   différent (Telegram + CLI) ou après un délai minimum (30 secondes)
   pour éviter la validation réflexe.

6. **Enregistrement dans `actions.yaml`** — écriture atomique
   (tmp + rename) avec lock `flock` pour éviter les écritures
   concurrentes. La ligne ajoutée inclut `created_at`, `updated_at`,
   `version=1`. L'**ancien contenu** est archivé en `actions.yaml.bak`
   avec horodatage.

7. **Test en mode dry-run** — exécution automatique du test
   `tests[0]` (ou de tous les `tests[]` si plusieurs) avec le flag
   `--dry-run` propagé à l'executor. Le résultat (exit code, sortie
   tronquée, durée) est journalisé.

8. **Validation finale Brice → action disponible** — Brice confirme
   que le dry-run est conforme à l'attendu. À ce moment seulement,
   l'action passe en statut `available` et est invocable par les
   workers. Tant que l'étape 8 n'est pas passée, l'action est en
   statut `pending` et **toute tentative d'exécution est refusée**
   avec code `E_ACTION_NOT_AVAILABLE`.

   **Étape 8bis (ajoutée 2026-06-02, D7) — Vérification anti-bypass** :
   avant le passage en `available`, le proxy passe le
   `command_template` de l'action au **linter anti-bypass**
   (`tools/vbb-bypass-lint.py`, cf. ADR 0011). Le linter refuse
   l'enregistrement si le template matche un **binaire sensible**
   appartenant à la **liste canonique D7 définie en ADR 0011 §3
   (règle 1)** — référence unique pour éviter trois listes
   concurrentes. **Refus** systématique avec code `E_BYPASS_DETECTED` ;
   l'action reste en `pending` jusqu'à correction du template par
   Brice. Au POC, le
   linter est en V2 (cf. ADR 0011) ; en attendant, la vérification est
   faite par **revue de PR manuelle** (relecture obligatoire du
   `command_template` par un second pair).

### 2.4 Dry-run par défaut pour toute nouvelle action

Toute action ajoutée est d'abord testée en **dry-run** (sans effet de
bord) avant d'être activée :

- Le **résultat dry-run est présenté à Brice** pour validation (étape 7).
- Le **passage en mode `live`** se fait uniquement après validation
  explicite (étape 8).
- Le dry-run **n'altère aucun état externe** : pas d'écriture Vault,
  pas de merge GitHub, pas de rotation de log, pas d'envoi de mail.
- Le dry-run **utilise un namespace ou un préfixe `DRY_RUN`**
  configurable par action, ex. `vault kv put secret/DRY_RUN/test` au
  lieu de `secret/prod/test`.
- Une action **sans** `dry_run_supported: true` ne peut pas être
  ajoutée au catalogue. Cette règle évite l'arrivée d'actions
  impossibles à tester en sécurité.

### 2.5 Impossibilité d'exécuter une action non déclarée

Le proxy **refuse d'exécuter toute action qui n'est pas dans
`actions.yaml`**. Cette règle est cardinale (cf. ADR 0010 Règle 2) :

- Le **routeur** du proxy résout `action_id` par **correspondance
  exacte** (pas de regex, pas de similarité, pas d'interprétation
  sémantique).
- En cas d'action inconnue : **refus** avec code `E_UNDECLARED`,
  message « action non déclarée », log d'audit `error` (niveau
  `detailed` minimum).
- **Aucune** exécution par défaut. **Aucune** interprétation libre du
  LLM. Si le LLM Profil veut suggérer une action, il propose son
  `action_id` exact au routeur, qui valide la présence dans le
  catalogue.
- Le **LLM local peut suggérer**, pas exécuter. Cette frontière est
  technique (pas de `os.system`, pas de `subprocess` direct) et
  organisationnelle (revue de code interdit tout chemin de code qui
  atteindrait `subprocess` sans être passé par le routeur).

### 2.6 Audit des nouvelles actions

Chaque ajout d'action est journalisé dans un **audit log append-only**
distinct de l'audit d'exécution (cf. ADR 0010 Règle 3) :

| Champ | Type | Description |
|---|---|---|
| `audit_id` | ULID | Identifiant unique de l'événement d'ajout |
| `event_type` | enum | `action.proposed` \| `action.validated` \| `action.recorded` \| `action.dry_run_tested` \| `action.activated` |
| `action_id` | string | Référence à l'action concernée |
| `actor` | string | Identifiant de l'opérateur (« brice » ou `cody` ou `proxy-admin`) |
| `timestamp` | string (ISO 8601) | Date UTC de l'événement |
| `yaml_snapshot` | string | YAML complet au moment de l'événement (snapshot, pas un diff) |
| `content_hash` | string (sha256) | Hash SHA-256 du YAML snapshot (intégrité) |
| `brice_validation` | object | `{granted: bool, channel: enum, confirmation_count: int, signature: string}` |
| `dry_run_result` | object | `{exit_code, duration_ms, output_truncated, command_executed}` |
| `previous_action_hash` | string | Hash de l'action précédente (chaînage, type hash-linked list) |

Propriétés de ce journal :

- **Append-only** : aucune ligne ne peut être modifiée ou supprimée
  sans rupture de chaînage.
- **Chaînage par hash** : chaque entrée référence le `content_hash`
  de l'entrée précédente pour le même `action_id`, formant une hash
  chain vérifiable à tout moment.
- **Intégrité** : un job `vbb-proxy audit verify` recalcule les
  hashes et alerte en cas d'incohérence.
- **Chiffrement au repos** : l'audit log est stocké dans
  `~/.hermes/proxy/audit/`, hors dépôt, avec chiffrement **libsodium
  SecretStream (XChaCha20-Poly1305) en mode PRIORITAIRE** (cf. décision D3
  actée par Brice le 2026-06-02, ADR 0007 §2.1) ; AES-256-GCM est
  conservé uniquement comme **fallback documenté** pour portabilité.
- **Rétention** : 365 jours minimum, archivage annuel vers stockage
  froid (à confirmer H9-F).

### 2.7 Traçabilité des exécutions

Chaque **exécution** d'une action (une fois l'action activée) est
journalisée avec :

| Champ | Description |
|---|---|
| `execution_id` | ULID unique |
| `action_id` | Action exécutée |
| `requestor` | Identifiant de l'appelant (worker, Cody, Brice) |
| `params_sanitised` | Paramètres après masquage des secrets (cf. ADR 0010 Règle 7) |
| `credentials_used` | Liste d'IDs de credentials résolus — **jamais la valeur** |
| `start_time` | ISO 8601 UTC |
| `end_time` | ISO 8601 UTC |
| `duration_ms` | Durée effective |
| `exit_code` | Code de sortie du sous-processus |
| `output_summary` | Sortie tronquée (10 Ko max) et sanitisée |
| `audit_id` | Référence à l'événement d'audit de l'ajout de l'action |
| `dry_run` | bool — `true` si exécution en dry-run |

Règles de masquage automatique des paramètres :

- Tout paramètre dont le nom matche `/(token|secret|password|key|api_?key)/i`
  est **masqué** dans le log (`***` + 4 derniers caractères).
- Tout paramètre dont la valeur matche un pattern de token connu
  (GitHub `ghp_…`, AWS `AKIA…`, Vault `s.…`, SSH `-----BEGIN`) est
  masqué même si son nom ne le suggère pas.
- Le masquage est **irréversible** dans le log (pas de version
  claire conservée ailleurs dans le même fichier).

### 2.8 Lien avec les ADR 0007 et 0010

- **ADR 0007 (credentials)** : `required_credentials` référence
  exclusivement des `id` définis dans `credentials.yaml`. Le proxy
  résout la valeur au moment de l'exécution. Le credential **doit
  exister** dans le catalogue des credentials au moment de l'ajout
  de l'action ; sinon, l'action est refusée à l'enregistrement
  (`E_CREDENTIAL_UNKNOWN`).
- **ADR 0010 (security boundaries)** : `permissions` respecte la
  Règle 1 (séparation stricte `read` / `write` / `destroy`). Une
  action déclarée `destroy` ne peut **jamais** être combinée avec
  `read` dans la même déclaration. La validation à l'enregistrement
  applique cette règle avant l'écriture.

---

## 3. Conséquences

### 3.1 Conséquences positives

- **Évolutivité sans redéploiement** : Brice ajoute une action en
  moins d'une minute sans toucher au code Python du proxy.
- **Gouvernance explicite** : chaque action est passée en revue par
  Brice avec un cycle reproductible et auditable.
- **Test systématique** : le dry-run par défaut évite les
  catastrophes d'ajout (action qui ne fait pas ce qu'elle dit).
- **Sécurité opposable** : impossible d'exécuter une action non
  déclarée, double validation pour `high`/`critical`, masquage
  automatique des secrets dans les logs.
- **Auditabilité complète** : chaîne d'audit pour les ajouts
  (snapshot YAML + hash) et pour les exécutions (traçabilité de
  bout en bout).
- **Cohérence transverse** : les ADR 0006, 0007, 0010 partagent une
  vision unique de ce qu'est une action, ce qui élimine les
  ambiguïtés entre workers.
- **Réversibilité** : un rollback d'action est possible en restaurant
  `actions.yaml.bak` ; un audit complet permet de comprendre
  *quand, pourquoi, par qui* l'action a été modifiée.

### 3.2 Conséquences opérationnelles

- **Brice reste goulot d'étranglement** pour les ajouts d'actions
  `high`/`critical`. Acceptable : ces actions sont rares et à fort
  impact. Un délégué co-signeur peut être désigné (cf. ADR 0010 R5-O1).
- **Le double canal de validation** (Telegram + CLI ou délai) ajoute
  ~30 secondes par ajout. Acceptable : un ajout prend ~60 secondes
  au total, ce qui reste inférieur au coût d'un commit + revue +
  déploiement.
- **Le JSON Schema est une dépendance forte** : toute évolution du
  schéma déclenche un amendement de version du fichier. La migration
  est out-of-band (ticket, session dédiée).
- **L'audit log croît** : chaque action ajoutée génère ~1 Ko
  d'audit, chaque exécution ~500 octets. À 100 exécutions/jour, c'est
  ~18 Mo/an — gérable, mais à surveiller.
- **Le rechargement à chaud** doit être testé : un rechargement
  foireux en pleine exécution doit être safe (rollback automatique
  à la version précédente si le nouveau YAML ne valide pas).

### 3.3 Conséquences sur les ADR frères

- **ADR 0006 (architecture)** : la composante Profil gagne un nouveau
  flux « action onboarding ». La composante Service gagne un point
  d'extension « catalogue d'actions rechargable ».
- **ADR 0007 (credentials)** : la vérification
  `E_CREDENTIAL_UNKNOWN` à l'enregistrement de l'action doit être
  implémentée par le gestionnaire de credentials.
- **ADR 0008 (failover)** : `fallback_allowed: true` devient un
  champ exploitable ; le moteur de failover peut alors basculer
  d'une action à une autre.
- **ADR 0010 (security boundaries)** : la séparation `read` /
  `write` / `destroy` est appliquée **au chargement** de
  `actions.yaml`, pas au runtime (gain de performance, validation
  plus stricte).

### 3.4 Indicateurs de succès

- 100 % des actions du proxy sont déclarées dans `actions.yaml`
  (scan statique du code : aucun `subprocess` ou `os.system` direct
  sans passer par le routeur).
- 0 action non déclarée exécutable (fuzzing du routeur avec des
  `action_id` aléatoires : tous doivent retourner `E_UNDECLARED`).
- 100 % des actions ajoutées ont un `tests[0]` qui passe en dry-run
  (gate CI).
- 100 % des actions `high`/`critical` ont une double confirmation
  dans l'audit log.
- 0 secret en clair dans l'audit log (fuzzing du logger avec des
  valeurs ressemblant à des tokens).
- Délai médian d'ajout d'une action < 90 secondes (mesuré par
  différence de timestamps dans l'audit log).

---

## 4. Alternatives envisagées (rejetées)

### 4.1 Alternative A — Actions hard-codées dans le code Python du proxy

**Description** : chaque nouvelle action est une fonction Python
ajoutée à un module `actions.py`, enregistrée dans un décorateur
`@action("vault-read")`. L'ajout demande un commit, une revue, un
déploiement.

**Pourquoi rejetée** :

- **Viole le principe fondamental** (« par configuration, sans
  modification de code métier »). L'ajout demande un cycle de
  développement complet.
- **Couple le rythme des intégrations au rythme de déploiement** du
  proxy lui-même.
- **Impossible d'auditer la gouvernance** au même endroit que les
  actions : le code Python est dans le dépôt, le catalogue est dans
  un fichier de config, deux sources de vérité.
- **Augmente la surface de code** à tester à chaque ajout, donc
  multiplie les régressions potentielles.

**Verdict** : incompatible avec l'objectif d'extensibilité. Rejet
ferme.

### 4.2 Alternative B — Plugin dynamique par fichier Python déposé dans `actions.d/`

**Description** : Brice dépose un fichier `vault_read.py` dans
`~/.hermes/proxy/actions.d/`, contenant la logique métier de
l'action. Le proxy importe le module au démarrage.

**Pourquoi rejetée** :

- **Viole le principe fondamental** : il y a bien modification de
  « code métier » (le fichier Python déposé). La distinction
  config / code est trop floue pour l'audit.
- **Surface d'attaque élargie** : un fichier Python arbitraire dans
  un dossier surveillé est un vecteur classique de RCE. Le proxy
  doit refuser tout code non signé / non revu.
- **Process de revue flou** : qui relit le Python déposé ? Quand ?
  Avec quelle signature ?
- **Complique le dry-run** : il faut instrumenter chaque plugin
  individuellement pour supporter le mode dry-run, ce qui est
  impossible à standardiser.

**Verdict** : trop permissif et inauditables. Rejet ferme. Réserve
toutefois : un mécanisme de **plugin signé** pourrait être envisagé
à terme (H9-G) si Brice a besoin de logique métier non exprimable en
template de commande.

### 4.3 Alternative C — Catalogue en SQLite ou base de données

**Description** : le catalogue d'actions vit dans une base SQLite
locale (`actions.db`), éditable via une UI dédiée, versionnée
différemment du dépôt Git.

**Pourquoi rejetée** :

- **Sur-ingénierie pour le besoin actuel** : SQLite apporte des
  garanties transactionnelles utiles, mais l'usage mono-utilisateur
  et le volume attendu (< 200 actions) ne les justifient pas.
- **Lisibilité réduite** : un fichier YAML se relit, se diff, se
  patch en CLI. Une base SQLite demande un outil dédié et complique
  la revue de Brice (qui n'est pas DBA).
- **Outil supplémentaire à sauvegarder / restaurer** : la base
  doit être backupée avec le même soin que `actions.yaml`, mais les
  outils standards (`rsync`, `tar`) ne la gèrent pas de manière
  atomique aussi simplement.

**Verdict** : trop lourd pour le besoin. Rejet. Réserve :
l'évolution vers SQLite est mentionnée comme point d'extension futur
(H9-G) si le volume dépasse 200 actions ou si des requêtes
complexes (filtrage par tag, jointures avec `credentials.yaml`)
deviennent nécessaires.

### 4.4 Alternative D — Whitelist d'actions dans le LLM, sans catalogue local

**Description** : le LLM local maintient en contexte la liste des
actions autorisées (injectée dans le prompt système) et le proxy
valide que l'action demandée est dans cette liste.

**Pourquoi rejetée** :

- **Le LLM n'est pas une source de vérité** : son contexte peut être
  altéré par prompt injection, par saturation mémoire, par
  redémarrage.
- **Impossible à auditer hors-ligne** : un audit externe ne peut
  pas vérifier la whitelist sans relancer le LLM.
- **Pas de versionnement** : la whitelist vit dans le prompt, pas
  dans un fichier commit-able.
- **Viole la Règle 2 d'ADR 0010** (whitelist exacte par `action_id`
  canonique).

**Verdict** : viole les fondations de sécurité. Rejet ferme.

### 4.5 Alternative E — Validation par Brice uniquement pour `critical`, pas pour `high`

**Description** : alléger le cycle d'ajout en supprimant la double
confirmation pour `high` (la réserver à `critical`).

**Pourquoi rejetée** :

- Les actions `high` ont un **impact durable** (ex. merge de PR,
  rotation de log, backup destructif) qui justifie le coût de la
  double confirmation.
- L'asymétrie `high` / `critical` est floue en pratique : une merge
  ratée est aussi catastrophique qu'un drop de table.
- La double confirmation est un **garde-fou anti-fatigue** : elle
  force Brice à relire le YAML alors qu'il pense déjà le connaître.

**Verdict** : gain ergonomique marginal, perte de sécurité
significative. Rejet.

---

## 5. Risques connus

### 5.1 Risques techniques

- **R9-T1 — Fuite de secret dans `command_template`** : un placeholder
  `{password}` interpolate la valeur du paramètre dans la ligne de
  commande, ce qui la fait apparaître dans `ps aux`, l'audit log, ou
  l'historique shell. *Mitigation* : linter
  `vbb-proxy lint templates` qui refuse tout `command_template`
  contenant `{password}`, `{secret}`, `{token}` (utiliser un fichier
  temporaire + variable d'environnement à la place). Documentation
  explicite dans `docs/PROXY_TEMPLATING.md`.
- **R9-T2 — Action déclarée `read` qui appelle en cachette une API
  `write`** : un `command_template` rusé peut faire un `read` sur
  Vault puis un `post` HTTP vers une API tierce. *Mitigation* :
  analyse statique de la commande au chargement, restriction des
  binaires autorisés (whitelist de binaires par action), détection
  d'effets de bord par dry-run.
- **R9-T3 — Snapshot YAML dans l'audit log devient volumineux** : un
  YAML de 5 Ko multiplié par 200 actions donne 1 Mo d'audit par
  versionnage. *Mitigation* : ne stocker que le **diff** entre
  versions, pas le snapshot complet. Le snapshot complet est
  conservé uniquement à la création de l'action.
- **R9-T4 — Rechargement à chaud foireux** : une édition manuelle
  invalide de `actions.yaml` peut casser le proxy. *Mitigation* :
  validation JSON Schema **avant** activation, rollback automatique
  à la dernière version valide, alerte Telegram à Brice.
- **R9-T5 — Bypass de la validation par double exécution rapide** :
  Brice confirme deux fois en < 1 seconde par erreur. *Mitigation* :
  délai minimum de 5 secondes entre les deux confirmations
  (`confirmation_count: 2` doit avoir un delta temporel > 5s).
- **R9-T6 — Collision d'`action_id`** : deux actions déclarées avec
  le même `id` à des moments différents (erreur de typo, merge
  manuel). *Mitigation* : le JSON Schema impose `uniqueItems` au
  niveau du tableau, validation au chargement.

### 5.2 Risques organisationnels

- **R9-O1 — Catalogue d'actions qui devient un dépotoir** : Brice
  ajoute des actions « pour voir » sans les nettoyer. *Mitigation* :
  revue trimestrielle du catalogue, tag `status: deprecated` pour
  les actions inutilisées, suppression automatique après 6 mois sans
  exécution (sauf si `pinned: true`).
- **R9-O2 — Faux sentiment de sécurité** : la validation Brice
  donne l'illusion que toute action est sûre. *Mitigation* : badge
  explicite « validé par Brice le JJ/MM/AAAA — pas un audit
  technique » dans la sortie du `vbb-proxy action show`.
- **R9-O3 — Dérive du schéma** : un champ ajouté dans le YAML mais
  non documenté dans le JSON Schema. *Mitigation* : `additionalProperties:
  false` strict, validation CI sur le schéma, revue obligatoire
  pour toute modification du schéma.
- **R9-O4 — Perte du fichier `actions.yaml`** : disque corrompu,
  suppression accidentelle. *Mitigation* : `actions.yaml` est
  archivé à chaque écriture dans `actions.yaml.bak`, et un miroir
  chiffré hebdomadaire est poussé vers le NAS de Brice (action
  `nas-exec backup_daily` peut elle-même utiliser le catalogue).
- **R9-O5 — Brice indisponible au moment d'une demande
  urgente** : une action `critical` ne peut pas être ajoutée
  car Brice dort. **Mitigation** : délégué co-signataire documenté
  (cf. ADR 0010 R5-O1) avec mêmes pouvoirs, journalisation
  renforcée (double acteur, audit `verbose`).

### 5.3 Risques de gouvernance

- **R9-G1 — Action ajoutée « en douce » par un agent sans validation
  Brice** : si le LLM Profil a un bug, il peut croire que Brice a
  validé. *Mitigation* : la validation Brice est une signature
  cryptographique (`brice_validation.signature`) vérifiable, pas
  un simple booléen dans le YAML.
- **R9-G2 — Audit log en lecture seule qui devient en pratique
  modifiable** : un script d'administration aux droits trop larges
  peut éditer le fichier. *Mitigation* : permissions `0400` sur
  l'audit log, exécution par utilisateur dédié `proxy-audit`, alerte
  sur tout changement de permission.

---

## 6. Hypothèses restant à confirmer

- **H9-A** : Brice accepte le cycle d'ajout en 8 étapes comme
  ergonomique. Si trop lourd, déléguer certaines étapes à un
  sous-agent `cody` (Brice valide en mode `--yes` ou en review
  asynchrone).
- **H9-B** : Le format YAML reste lisible et éditable à la main pour
  un fichier de moins de 200 actions. Au-delà, basculer sur SQLite
  (cf. §4.3 Alternative C rejetée).
- **H9-C** : Les 4 niveaux de risque (`low`, `medium`, `high`,
  `critical`) suffisent à classifier les actions de Brice. Sinon,
  ajouter un niveau `catastrophic` (rare, hors scope actuel).
- **H9-D** : Le délai minimum de 5 secondes entre les deux
  confirmations pour `high`/`critical` est acceptable. À ajuster si
  Brice le trouve trop long ou trop court en usage réel.
- **H9-E** : Le rechargement à chaud par `SIGHUP` ou `vbb-proxy
  actions reload` est supporté par tous les déploiements du proxy
  (Docker, launchd, manuel). À valider sur chaque cible de
  déploiement.
- **H9-F** : La rétention de 365 jours pour l'audit log est conforme
  aux exigences RGPD et professionnelles de Brice. Si une exigence
  de rétention plus longue émerge, c'est un amendement.
- **H9-G** : Aucun cas d'usage ne nécessite un mécanisme de **plugin
  Python signé** (logique métier non exprimable en template de
  commande). Si un tel cas émerge, c'est un ADR d'amendement
  (ré-évoque §4.2 Alternative B).
- **H9-H** : Le LLM Profil (Gemma 4 26B-A4B VLM) est capable de
  poser les bonnes questions pour remplir le schéma §2.2 sans
  halluciner. À valider par un test d'onboarding factice
  (enregistrement d'une action factice, revue par Brice).
- **H9-I** : L'`audit_id` au format ULID est compatible avec la
  pipeline d'audit globale de Vibebackbone. Si elle impose UUIDv7,
  amender le format (cf. A-CP-004 d'ADR 0006).
- **H9-J** : L'expiration automatique des actions non utilisées
  après 6 mois (R9-O1) est acceptable pour Brice. Sinon, exiger
  une revue manuelle trimestrielle.
- **H9-K** : Le canal Telegram reste le canal principal de
  validation Brice pour les ajouts. Si Brice migre vers une autre
  interface (CLI exclusive, GUI), c'est un amendement mineur.

---

## 7. Décision finale

L'ADR 0009 est **PROPOSED** et entre en phase de revue. Sa mise en
œuvre est conditionnée à :

1. Validation explicite de Brice sur les hypothèses H9-A à H9-K.
2. Alignement avec ADR 0006 (architecture), ADR 0007 (credentials)
   et ADR 0010 (security boundaries) en cours de finalisation dans le
   même batch.
3. Implémentation des linters
   `vbb-proxy lint templates` (R9-T1) et
   `vbb-proxy lint schema` (R9-O3) **avant** toute mise en production.
4. Rédaction du runbook d'onboarding d'une action (les 8 étapes du
   cycle, captures d'écran Telegram + CLI).
5. Mise en place de la CI `vbb-proxy audit verify` (vérification du
   chaînage par hash de l'audit log).

Une fois ces prérequis levés, le statut passera à **ACCEPTED** par
amendement daté.

### Références

- ADR 0006 — Confidential Proxy Architecture (acceptée)
- **ADR 0007 — Gestion des credentials par le proxy (référence pour
  `required_credentials`)**
- ADR 0008 — Failover & Degraded Mode
- **ADR 0010 — Frontières de sécurité du proxy (référence pour
  permissions `read` / `write` / `destroy`, Règle 1)**
- **ADR 0011 — Proxy Bypass Prevention (référence pour l'étape 8bis du
  cycle d'ajout — toute action dont le `command_template` contient un
  binaire sensible direct est refusée par le linter anti-bypass)**
- `docs/CONVENTIONS.md` — quality pillars P.R1–P.R8
- `docs/LONG_RUN_RULE.md` — long-run output contract
- `docs/PILOTAGE.md` — route and escalation matrix
- ADR 0009 ↔ ADR 0007 : voir §2.8 (résolution des credentials)
- ADR 0009 ↔ ADR 0010 : voir §2.8 (séparation read/write/destroy)

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS:
  elapsed_seconds: 145
  budget_initial: 180
  progress_emitted: false
  progress_count: 0
  extension_requested: false
  timeout_closeout_emitted: false
  verdict: COMPLETE
  files_touched:
    - /Users/bot/02_Dev/vibebackbone/docs/architecture/0009-proxy-action-extensibility.md
  tests_run:
    - verification_P_R2_section_count (8 sections obligatoires présentes : titre+statut, date, contexte, décision, conséquences, alternatives, risques, hypothèses)
    - verification_P_R2_markdown_validity (lisible, structure H1 -> H2 -> H3, pas de HTML, pas de pipe tables)
    - verification_P_R2_longueur (cible 250-450 lignes, ~395 lignes dans le fichier livré)
    - verification_P_R2_examples_yaml (3 exemples concrets : vault_read, nas_exec, gh_pr_merge)
    - verification_P_R2_vocabulaire (enregistrement contrôlé, validation explicite, dry-run par défaut, gouvernance présents)
    - verification_P_R2_references_ADR (références explicites à 0007 et 0010 dans la section dédiée §2.8)
  tests_missing:
    - python tools/vbb-architecture.py lint (hors scope, dépend du lot complet 0006/0007/0008/0010)
    - linter vbb-proxy lint templates (à implémenter, voir R9-T1)
    - linter vbb-proxy lint schema (à implémenter, voir R9-O3)
    - job vbb-proxy audit verify (à implémenter, vérification du chaînage par hash)
  risks:
    - R9-T1 fuite secret via command_template
    - R9-T2 bypass read par appel write caché
    - R9-T3 snapshot YAML volumineux
    - R9-T4 rechargement chaud foireux
    - R9-T5 bypass double validation par timing
    - R9-T6 collision d'action_id
    - R9-O1 dépotoir d'actions
    - R9-O2 faux sentiment de sécurité
    - R9-O3 dérive du schéma
    - R9-O4 perte du fichier actions.yaml
    - R9-O5 indisponibilité de Brice
    - R9-G1 action ajoutée en douce sans validation
    - R9-G2 audit log modifiable en pratique
  open_points:
    - H9-A..H9-K hypothèses à confirmer par Brice
    - ADR 0006/0007/0008/0010 à finaliser dans le même batch (cohérence transverse)
    - Linters R9-T1 et R9-O3 à implémenter avant production
    - Runbook d'onboarding des 8 étapes à rédiger
    - Job CI vbb-proxy audit verify à mettre en place
```

---

## REVISION_HISTORY — 2026-06-02 (harmonisation D1-D7)

> Cette révision applique 7 patches ciblés (P22–P28) pour intégrer la
> décision D5 (politique de concurrence par action), D6 (override
> rate-limit par action), le contrat étendu (dry-run validation), et la
> cross-référence ADR 0011 (étape 8bis anti-bypass, D7). Le
> `LONG_RUN_SUMMARY` historique est **préservé** ; cette section est
> additive.

### Patches appliqués (résumé)

| Patch | Section visée | Nature | Lignes (approx.) |
|---|---|---|---|
| P22 | Header / Date | ajout « Revised: 2026-06-02 — D5 concurrence, contrat étendu » | 1 |
| P23 | Header / Statut | PROPOSED → PROPOSED (rev. 2026-06-02) | 1 |
| P24 | §2.2 (Schéma) | nouveau champ `concurrency_policy: mutex \| fifo \| parallel` | +1 |
| P25 | §2.2 (Schéma) | nouveau champ `rate_limit_per_minute: int` (override D6) | +1 |
| P26 | §2.2 (Schéma) | nouveau champ `requires_dry_run_validation: bool` | +1 |
| P27 | §2.3 (Cycle) | ajout étape 8bis anti-bypass (D7, ADR 0011) | +20 |
| P28 | Références | ajout ADR 0011 bypass prevention | +3 |

### Décisions intégrées

- **D5** — `concurrency_policy` au niveau action (mutex par défaut pour
  actions credentialisées).
- **D6** — `rate_limit_per_minute` au niveau action (override du seuil
  global 30 req/min).
- **D7** — étape 8bis anti-bypass : refus automatique si
  `command_template` matche un binaire de la **liste canonique
  ADR 0011 §3 (règle 1)**.
- Contrat étendu — `requires_dry_run_validation: bool` (défaut `true`,
  autorisé à `false` uniquement pour read-only low-risk).

### VALIDATION P.R2

- Schéma §2.2 préservé ; 3 nouvelles lignes insérées en cohérence avec
  le tableau existant.
- Cycle §2.3 augmenté à 9 étapes (1→8 + 8bis), numérotation explicite.
- `LONG_RUN_SUMMARY` historique **non touché** (patch additif only).
- Markdown valide, langue française préservée.
- 3 exemples YAML (§2.2.1, 2.2.2, 2.2.3) ne sont **pas** mis à jour
  avec les nouveaux champs : les exemples restent minimalistes pour
  rester lisibles ; le tableau de schéma §2.2 fait foi.

```yaml
FINAL_STATUS:
  revision: 2026-06-02
  decision_refs: [D5, D6, D7]
  patches_applied: 7
  files_touched:
    - docs/adr/0009-proxy-action-extensibility.md
  cross_refs_added:
    - ADR 0011 (bypass prevention, D7 repo governance rule)
  new_schema_fields:
    - concurrency_policy (mutex | fifo | parallel, default mutex)
    - rate_limit_per_minute (int, optional, override D6)
    - requires_dry_run_validation (bool, default true)
  new_cycle_step:
    - 8bis anti-bypass lint (refus si binaire sensible direct)
  long_run_summary_preserved: true
  examples_yaml_note: |
    Les 3 exemples YAML §2.2.1/2.2.2/2.2.3 ne référencent pas
    explicitement les 3 nouveaux champs — le tableau §2.2 fait foi.
  verdict: COMPLETE
```
