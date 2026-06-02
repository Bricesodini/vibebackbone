# ADR 0007 — Gestion des credentials par le proxy de confidentialité

**Statut** : PROPOSED (rev. 2026-06-02)
**Date** : 2026-06-02 (Revised: 2026-06-02 — D3 chiffrement libsodium prioritaire, D5 concurrence, contrat étendu)
**Route** : STRUCTURED
**Décideurs** : Brice (demandeur), gouvernance Vibebackbone
**Chantier** : Proxy de confidentialité (Brice, 2026-06-02)
**ADRs liées** : 0006 (architecture du proxy, en cours) · 0008 (failover) · 0009 (extensibilité) · **0010 (security boundaries — référence obligatoire pour les règles de séparation lecture/écriture/destruction)** · 0011 (bypass prevention)

---

## 1. Contexte

Le chantier « Proxy de confidentialité » (Brice, 2026-06-02) vise à isoler les credentials du LLM cloud via un agent LLM local transverse. La stack cible est composée de Hermes, Cody, 4 workers VBB, `cody-check` et un backend Ollama/MLX local. Le proxy agit comme **gardien de barrière** entre :

- le LLM cloud (jamais en contact direct avec un secret) ;
- les outils et intégrations externes (SSH, API tierces, registres, services de production) ;
- le poste de Brice (source de vérité opérationnelle et décisionnelle).

L'ADR 0006 fixe l'architecture générale du proxy (batch, file d'actions, médaillon local). L'ADR 0010 fixe les **security boundaries** (qui peut lire, qui peut écrire, qui peut détruire un secret). La présente ADR 0007 tranche spécifiquement la **gestion du cycle de vie des credentials** : où vit la définition, où vit la valeur, comment on ajoute un credential, comment on le teste, comment on l'audite.

Le besoin de sécurité est qualifié **critique** : un secret qui fuit vers le LLM cloud ou dans le dépôt Git annule l'objectif même du proxy. Aucune mesure palliative n'est acceptable ; les invariants doivent être énoncés explicitement et défendables par le code.

Le besoin d'ergonomie est également non négociable : Brice doit pouvoir enregistrer un nouveau credential en moins de 60 secondes via Telegram ou en CLI, sans manipuler manuellement de fichiers chiffrés.

---

## 2. Décision

Les credentials gérés par le proxy de confidentialité obéissent à un **modèle de configuration déclarative extensible** : un fichier YAML versionné contient **le schéma et les métadonnées** du credential, et **jamais la valeur secrète elle-même**. Les valeurs secrètes sont stockées hors dépôt, chiffrées au repos, et accessibles uniquement au proxy lors d'une exécution.

### 2.1 Stockage physique

Trois emplacements, hiérarchisés par ordre de préférence :

1. **macOS Keychain** (priorité) — intégration via la CLI `security` standard du système. Le proxy y dépose chaque valeur secrète indexée par `service="vbb-proxy"` et `account=<credential.id>`.
2. **`~/.hermes/proxy/secrets.enc`** (fallback) — fichier local chiffré via **libsodium SecretStream (XChaCha20-Poly1305) en mode PRIORITAIRE** (cf. décision D3 actée par Brice le 2026-06-02) ; **AES-256-GCM est conservé comme FALLBACK documenté** pour portabilité si libsodium est indisponible sur une cible exotique. Format : une ligne JSON par secret au format JSON Lines `{id, ciphertext, nonce, tag}`. La clé symétrique est elle-même stockée dans le Keychain macOS (clé dédiée `vbb-proxy-secrets-key`). Ce fichier est **explicitement listé dans `.gitignore`** et ne doit jamais être commité.
3. **Métadonnées versionnées** : `~/.hermes/proxy/credentials.yaml` (schéma + métadonnées uniquement, jamais de valeur). Ce fichier peut, au choix de Brice, être versionné dans un dépôt privé séparé **ou** conservé localement. La règle d'or est : `credentials.yaml` ne contient **aucune** valeur secrète, ni en clair, ni obfusquée, ni encodée en base64.

> **Décision D3 (actée par Brice le 2026-06-02)** : le chiffrement
> retenu pour `secrets.enc` (et pour les scratch files du contrat
> étendu, cf. ADR 0006 §2.6.1) est **libsodium SecretStream
> (XChaCha20-Poly1305)**. AES-256-GCM reste documenté comme chemin de
> repli pour les environnements sans libsodium. Toute migration doit
> être tracée dans l'audit (cf. R7-09).

### 2.2 Schéma d'un credential (YAML)

Chaque credential est défini par le bloc suivant (exemple avec valeurs factices) :

```yaml
credentials:

  - id: github-brice-readonly          # slug unique, kebab-case
    description: "Token GitHub pour Brice, accès lecture seule sur orgs personnelles"
    type: api_token                    # ssh_key | api_token | password | oauth_token | certificate
    risk_level: medium                 # low | medium | high | critical
    permissions:
      - read                           # read | write | destroy
    allowed_actions:
      - vbb.git.clone_public
      - vbb.git.fetch_issue
    test_command: "gh auth status --user brice-robot"
    requires_explicit_validation: true
    created_at: 2026-06-01T10:14:22Z
    updated_at: 2026-06-01T10:14:22Z
    last_validated_at: 2026-06-01T10:14:25Z
    audit:
      created_by: brice
      last_used_by: vbb-worker-git
      last_used_at: 2026-06-02T08:55:01Z

  - id: prod-ssh-deploy                # credential sensible
    description: "Clé SSH de déploiement production (rotation 90j)"
    type: ssh_key
    risk_level: critical
    permissions:
      - read
      - write
    allowed_actions:
      - vbb.deploy.production_push
    test_command: "ssh -o BatchMode=yes -o ConnectTimeout=5 git@prod.example.com echo OK"
    requires_explicit_validation: true   # OBLIGATOIRE pour high/critical
    created_at: 2026-05-20T09:00:00Z
    updated_at: 2026-05-20T09:00:00Z
    last_validated_at: 2026-06-01T09:00:04Z
    audit:
      created_by: brice
      last_used_by: vbb-worker-deploy
      last_used_at: 2026-06-01T18:30:11Z
```

### 2.3 Champs obligatoires et contraintes

| Champ | Type | Obligatoire | Contraintes |
|---|---|---|---|
| `id` | string | oui | Unique, slug kebab-case, non modifiable après création |
| `description` | string | oui | Usage humain, libre mais non vide |
| `type` | enum | oui | `ssh_key` \| `api_token` \| `password` \| `oauth_token` \| `certificate` |
| `risk_level` | enum | oui | `low` \| `medium` \| `high` \| `critical` |
| `permissions` | list[enum] | oui | Sous-ensemble de `read`, `write`, `destroy` |
| `allowed_actions` | list[string] | oui | Préfixées `vbb.<domaine>.<verbe>`, doivent exister dans le registre d'actions |
| `test_command` | string | oui | Commande shell, **ne doit jamais** contenir la valeur du secret en argument littéral (utilise stdin ou variable d'environnement injectée par le proxy) |
| `requires_explicit_validation` | bool | oui | Forcée à `true` pour `high`/`critical` par le validateur |
| `created_at` | timestamp | auto | Écrit par le proxy |
| `updated_at` | timestamp | auto | Mis à jour à chaque `update` |
| `last_validated_at` | timestamp | auto | Mis à jour à chaque `test_command` réussi |

### 2.4 Ajout d'un nouveau credential : enregistrement interactif guidé

L'ajout d'un credential **n'est jamais automatique** (pas d'auto-apprentissage). Il suit un dialogue explicite, initie par Brice, en **enregistrement interactif guidé** :

1. **Initiation** — Brice envoie au proxy un message du type `proxy: add credential` (Telegram) ou exécute `vbb-proxy credential add` (CLI).
2. **Questions guidées** — Le proxy pose, dans l'ordre, les questions suivantes. Chaque réponse est validée avant de passer à la suivante :
   - `id` (proposition automatique par défaut, éditable ; refus si déjà existant)
   - `type` (menu énuméré)
   - `description` (texte libre, non vide)
   - `risk_level` (menu énuméré, valeur par défaut `medium`)
   - `permissions` (multi-sélection)
   - `allowed_actions` (auto-suggestion à partir du type, éditable)
   - `test_command` (auto-suggestion à partir du type, éditable)
3. **Saisie de la valeur** — Le proxy invite Brice à fournir la valeur (coller dans Telegram ou saisir en CLI masqué). La valeur n'est **jamais** ré-affichée par la suite.
4. **Validation explicite** — Le proxy affiche un récapitulatif (sans la valeur) et demande `Confirmer l'enregistrement ? (oui/non)`. Sans `oui` explicite, rien n'est persisté.
5. **Persistance** — Sur confirmation, le proxy chiffre la valeur (Keychain prioritaire, fallback `secrets.enc`) puis écrit les métadonnées dans `credentials.yaml` (transaction : le YAML n'est mis à jour qu'après confirmation du dépôt de la valeur chiffrée).
6. **Test optionnel** — Le proxy propose : `Lancer le test_command maintenant ? (oui/non)`. Si Brice répond `oui`, le test est exécuté. Si `risk_level=critical`, le proxy exige une **double confirmation** : `Le credential est marqué critical. Confirmer le test ? (oui/non)`.
7. **Confirmation finale** — Le proxy renvoie un récapitulatif définitif avec `id`, `risk_level`, `test_command`, statut du test, et `last_validated_at` si applicable.

### 2.5 Test de credential

- **Par défaut**, un test automatique est **proposé** (non imposé) à l'issue de l'ajout, et **uniquement** si Brice l'a explicitement demandé à l'étape 6 ci-dessus.
- Le résultat du test (succès, échec, code retour, durée) est consigné dans le journal d'audit avec horodatage.
- Pour les credentials `critical`, le test n'est jamais lancé sans **double confirmation** (deux `oui` distincts).
- Pour les credentials `high`, un seul `oui` suffit mais le résultat doit être validé par Brice (le proxy affiche le résultat et demande `Marquer comme validé ? (oui/non)`).
- Pour les credentials `low` et `medium`, le test est libre mais tracé.
- Un credential dont `last_validated_at` est antérieur à la rotation prévue est marqué `stale: true` dans la sortie d'audit, sans bloquer l'exécution (sauf pour `critical` : dans ce cas, voir ADR 0010 § « stale blocking »).

### 2.6 Cycle de vie

Quatre opérations, toutes tracées :

| Opération | Déclencheur | Effet |
|---|---|---|
| `create` | Enregistrement interactif guidé (§2.4) | Écrit la valeur chiffrée + les métadonnées, `created_at` posé |
| `read` | Exécution d'une action autorisée par le proxy | Le proxy injecte la valeur dans l'environnement de l'action ; **jamais** renvoyée en clair à l'appelant. Voir ADR 0010 pour les règles de séparation lecture/écriture/destruction |
| `update` | Commande `vbb-proxy credential update <id>` | Cas typique : **rotation**. L'ancienne valeur est révoquée (cf. `revoke`), la nouvelle suit le flux §2.4. `updated_at` est mis à jour |
| `revoke` | Commande `vbb-proxy credential revoke <id>` | **Suppression logique** : la valeur est effacée du Keychain et de `secrets.enc`, les métadonnées sont conservées avec `revoked_at` et `revoked_by`. Le journal d'audit reste consultable |

### 2.7 Invariant : aucune promotion automatique

**Aucune auto-promotion** d'un credential sensible n'est autorisée (pas plus qu'auto-apprentissage, voir §4.3). La règle vaut pour toute transition d'état, pas seulement la première activation. Un credential de `risk_level` `high` ou `critical` ne devient utilisable qu'après **validation explicite** de Brice, exprimée hors bande (Telegram ou CLI en personne). Cette règle signifie concrètement :

- un credential nouvellement créé avec `risk_level=high` ou `critical` a `requires_explicit_validation=true` et un champ implicite `validated: false` ;
- le proxy refuse d'exécuter toute action listée dans `allowed_actions` tant que `validated` n'est pas `true` ;
- le passage à `validated: true` se fait par commande `vbb-proxy credential validate <id>` avec accusé de réception, **pas** automatiquement après un test réussi.

### 2.7bis Politique de concurrence (décision D5, actée par Brice le 2026-06-02)

> **Décision D5** : la concurrence sur les credentials suit trois règles
> cardinales, configurables par credential via le champ
> `concurrency_policy`.

- **Mutex par credential/target** — un seul appel ne peut pas utiliser
  le même `credential_id` simultanément. Un second appel arrivant alors
  que le premier n'a pas rendu le lock est **mis en attente** ou
  **refusé** selon la configuration ci-dessous. Cette règle évite la
  réutilisation accidentelle d'un token dans deux contextes concurrents
  (par exemple, deux rotations de log simultanées sur la même clé
  Vault).
- **File FIFO par target sensible** — pour les actions sur une même
  cible sensible (même serveur, même dépôt, même bucket), les appels
  sont **séquentialisés** dans l'ordre d'arrivée. Une cible sensible
  n'exécute jamais deux actions en parallèle, même si leurs
  `credential_id` sont distincts. La sérialisation est nécessaire pour
  préserver l'invariant « pas d'effet de bord croisé ».
- **Refus ou attente explicite en cas de lock** — par défaut, la
  politique est **refus + erreur + audit** (HTTP 409 `E_LOCK_HELD` avec
  `Retry-After` header), pas d'attente silencieuse. Brice peut
  configurer un comportement d'attente bornée via
  `lock_wait_policy: refuse | wait(max_ms)` au niveau du credential.

**Configuration YAML (ajout au schéma §2.2)** :

```yaml
- id: prod-ssh-deploy
  # ... champs existants ...
  concurrency_policy: mutex          # mutex | fifo | parallel
  lock_wait_policy: refuse           # refuse | wait(max_ms)
  fifo_target: prod-git-server       # requis si concurrency_policy=fifo
```

- `concurrency_policy: mutex` (défaut pour actions credentialisées) —
  un seul appel à la fois par credential.
- `concurrency_policy: fifo` — file FIFO par `fifo_target`, sérialise
  les actions vers la même cible sensible.
- `concurrency_policy: parallel` — autorise la concurrence, à n'utiliser
  **que** pour des actions read-only idempotentes (rare, à justifier).
- `lock_wait_policy: refuse` (défaut) — refus HTTP 409 + audit
  (`event=credential.lock_refused`).
- `lock_wait_policy: wait(N)` — attente bornée, N ms max, puis refus
  si toujours verrouillé.

Toute violation de la concurrence (par exemple, deux appels
concurrents détectés a posteriori) est un **incident de sécurité**
consigné dans l'audit log avec `event=concurrency_violation` et notifié
à Brice via Telegram.

### 2.8 Audit

Chaque accès à un credential — création, lecture, révocation, mise à jour, test — est consigné dans `~/.hermes/proxy/audit.log` (JSON Lines, append-only, rotation par taille). Chaque ligne porte au minimum :

```json
{
  "ts": "2026-06-02T08:55:01Z",
  "event": "credential.read",
  "credential_id": "github-brice-readonly",
  "requester": "vbb-worker-git",
  "action": "vbb.git.fetch_issue",
  "result": "ok",
  "duration_ms": 412
}
```

Le journal d'audit est lui-même **non chiffré** (les valeurs secrètes n'y figurent jamais) et peut être versionné ou exporté pour revue. Le champ `requester` identifie le composant appelant ; il ne peut pas être forgé côté LLM cloud (cf. ADR 0010).

### 2.9 Référencement ADR 0010 — security boundaries

Cette ADR 0007 définit **quoi** et **comment** ; l'ADR 0010 définit **qui peut faire quoi**. En particulier, la séparation lecture / écriture / destruction suit la matrice suivante (résumée ici, détaillée dans 0010) :

| Capacité | LLM cloud | LLM local (proxy) | Brice (humain) |
|---|---|---|---|
| `read` (valeur en clair) | **interdit** | autorisé via le proxy uniquement | autorisé via le proxy uniquement |
| `write` (créer / update) | **interdit** | autorisé en mode enregistrement interactif guidé | autorisé directement |
| `destroy` (revoke) | **interdit** | autorisé en mode interactif | autorisé directement |
| Audit (lecture du journal) | autorisé (métadonnées seules) | autorisé | autorisé |

Toute déviation à cette matrice est un incident de sécurité, géré par ADR 0010.

### 2.10 Référencement ADR 0011 — bypass prevention (décision D7)

Cette ADR 0007 s'inscrit dans le cadre de la **règle de gouvernance
repo** (D7) formalisée par l'ADR 0011 : aucun worker VBB (et a fortiori
aucun agent Hermes / Cody) ne doit appeler directement `ssh`, `scp`,
`rsync`, `gh auth`, `docker login`, ni lire `cat .env` ou `printenv` sur
des secrets. Tout accès credentialisé **passe par le proxy** et donc
par les règles décrites dans la présente ADR. Le linter
`tools/vbb-bypass-lint.py` (cf. ADR 0011 § implémentation) est en V2 ;
au POC, la règle est appliquée par revue de PR manuelle.

---

## 3. Conséquences

### 3.1 Positives

- **Séparation claire des préoccupations** : métadonnées versionnables, valeurs hors dépôt, chiffrement au repos. Brice peut auditer `credentials.yaml` sans risque de fuite de secret.
- **Reproductibilité** : le schéma YAML étant déclaratif, un nouveauvenu (ou un audit) peut comprendre les capacités du proxy sans inspecter le code.
- **Principe du moindre privilège** appliqué strictement : `allowed_actions` et `permissions` codifient, par credential, ce qui peut être fait. Le proxy refuse par défaut toute action non listée. Aucune élévation implicite, aucune auto-promotion.
- **Traçabilité totale** : audit append-only, horodaté, identifiant l'appelant. Pas de secret dans le journal.
- **Ergonomie** : l'enregistrement interactif guidé rend l'ajout d'un credential rapide et explicite, sans manipulation manuelle de fichiers chiffrés.
- **Extensibilité** : le type d'un credential est un enum, mais le validateur peut accepter de nouveaux types via une PR documentée, sans casser les credentials existants (cohérent avec ADR 0009).

### 3.2 Négatives et trade-offs

- **Double source de vérité** : `credentials.yaml` + `secrets.enc` doivent rester en cohérence. Une commande `vbb-proxy credential reconcile` est nécessaire pour détecter les divergences. Cette commande est **hors scope** de la présente ADR et sera traitée en suivi.
- **Dépendance au Keychain macOS** : en cas de panne Keychain, le fallback `secrets.enc` prend le relais mais avec une surface d'attaque plus large (clé de chiffrement dans un fichier). Le proxy doit signaler explicitement quel mode est actif.
- **Coût d'ajout d'un credential** : l'enregistrement interactif guidé est plus lent qu'un simple `echo` dans un fichier. Ce coût est volontaire et proportionnel à la criticité (P.R3 — Gate Before Action).
- **Pas d'auto-apprentissage** : le proxy ne devine pas les credentials à partir de logs, de fichiers de config, ou d'appels répétés. Cette rigidité est un choix de sécurité, pas un oubli.
- **Migration manuelle initiale** : si Brice a déjà des secrets dans des dotfiles, ils doivent être ré-enregistrés via le flux §2.4. Cette migration est manuelle, documentée dans le runbook d'onboarding.

---

## 4. Alternatives envisagées

### 4.1 Alternative rejetée A — Stockage des secrets en variables d'environnement versionnées dans `.envrc`

**Description** : un fichier `.envrc` à la racine du dépôt Vibebackbone contient toutes les paires `KEY=VALUE`, versionné dans un dépôt privé. Le proxy lit ces variables au démarrage.

**Pourquoi rejetée** :

- **Viole l'invariant « aucun secret dans le dépôt Git »** : même un dépôt privé reste un dépôt Git, sujet aux fuites (clone accidentel, CI, copier-coller, agent tiers).
- **Aucun chiffrement au repos** : un dump du dépôt suffit.
- **Pas d'audit granulaire** : impossible de tracer quel worker a lu quelle variable à quel moment sans ajouter une couche supplémentaire.
- **Pas d'enregistrement interactif guidé** : l'ajout se fait par édition de fichier, contournant toute validation explicite.

### 4.2 Alternative rejetée B — Vault centralisé (HashiCorp Vault) avec agents sur le poste

**Description** : déploiement d'un Vault auto-hébergé sur le poste de Brice, avec agents sur chaque worker qui récupèrent les secrets à la demande.

**Pourquoi rejetée** :

- **Surcharge opérationnelle disproportionnée** : HashiCorp Vault est conçu pour des flottes ; sur un poste mono-utilisateur, il ajoute un service de plus à superviser, sauvegarder, mettre à jour, sans bénéfice clair par rapport au Keychain macOS.
- **Surface d'attaque élargie** : un service réseau local ouvert est plus exposé qu'un Keychain lié à l'utilisateur OS.
- **Complexité d'audit** : l'audit Vault est plus riche, mais l'audit Keychain + journal local suffit pour le besoin de Brice (mono-utilisateur, mono-poste).
- **Couplage fort à l'infra** : en cas de réinstallation du poste, la restauration de la Vault est non triviale. Le Keychain se synchronise avec le compte iCloud au choix de Brice.

**Réserve** : Vault pourrait redevenir pertinent si le proxy est un jour étendu à une équipe. Cette évolution est documentée dans ADR 0009 (extensibilité) comme point d'extension futur, **pas** comme choix initial.

### 4.3 Alternative rejetée C — Auto-apprentissage par observation de `~/.aws/credentials`, `~/.ssh/config`, etc.

**Description** : le proxy scanne périodiquement les dotfiles et dossiers de credentials standards, et ingère automatiquement ceux qu'il trouve, en inférant le `type` et le `risk_level`.

**Pourquoi rejetée** :

- **Viole frontalement l'enregistrement interactif guidé** : Brice perd la main sur ce qui est ingéré et avec quel niveau de risque.
- **Aucune validation explicite** : impossible d'exiger une confirmation par credential.
- **Faux positifs** : des fichiers comme `~/.ssh/known_hosts` ou `~/.gitconfig` ne sont pas des credentials mais seraient candidats à l'ingestion.
- **Aucune promotion automatique d'un credential sensible** : cette règle d'or serait contournée.

### 4.4 Alternative rejetée D — Secrets en clair dans un fichier chiffré global (type `ansible-vault`)

**Description** : un seul fichier `vault.yml` chiffré contient à la fois métadonnées et valeurs, déchiffré à la volée par le proxy avec un mot de passe maître saisi par Brice à chaque démarrage.

**Pourquoi rejetée** :

- **Granularité d'audit perdue** : pas de séparation entre « métadonnée auditables » et « valeur secrète ».
- **Versionnement difficile** : un fichier globalement chiffré ne se prête pas au diff Git, ce qui casse l'historique de l'évolution des credentials.
- **Risque de verrouillage** : si le mot de passe maître est perdu, tous les credentials sont perdus d'un coup. Le Keychain évite ce point de défaillance unique.

---

## 5. Risques connus

| ID | Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|---|
| R7-01 | Fuite de secret via `test_command` (valeur passée en argument littéral) | Moyenne | Critique | Linter dédié `vbb-proxy lint test-commands` qui refuse tout argument ressemblant à un token/clé. Documentation explicite : utiliser stdin ou variable d'environnement injectée |
| R7-02 | Divergence entre `credentials.yaml` et `secrets.enc` (création partielle, crash) | Moyenne | Élevée | Écriture transactionnelle : valeur chiffrée d'abord, métadonnées ensuite ; en cas d'échec entre les deux, le credential est marqué `orphan: true` et l'audit le signale |
| R7-03 | Brice colle un secret dans un canal non chiffré (ex : log Telegram non protégé) | Faible | Élevée | Bandeau d'avertissement Telegram avant chaque saisie ; CLI en mode masqué (pas d'echo). Documentation onboarding |
| R7-04 | Rotation oubliée (credential `critical` jamais rotaté) | Moyenne | Élevée | Champ `rotation_due_at` optionnel ; alertes Telegram si dépassé ; voir ADR 0010 § stale blocking |
| R7-05 | Compromission du poste macOS = compromission de tous les credentials | Faible | Critique | Accepté : c'est la limite du modèle mono-poste mono-utilisateur. ADR 0009 prévoit l'évolution vers Vault si l'équipe s'élargit |
| R7-06 | Un worker contourne le proxy et lit directement le Keychain | Faible | Critique | Le Keychain est en mode « seul l'utilisateur courant » ; les workers s'exécutent en tant qu'OS services distincts de l'utilisateur Brice, donc l'accès Keychain leur est refusé par défaut. ADR 0010 détaille |
| R7-07 | `test_command` exécuté par erreur sur un environnement de prod | Moyenne | Élevée | Le proxy injecte un préfixe `DRY_RUN` configurable par credential ; les tests critiques doivent être marqués `dry_run_only: true` |
| R7-08 | Audit log non rotaté, disque saturé | Faible | Moyenne | Rotation par taille (10 Mo par défaut), compression, conservation 365 jours ; alertes si saturation |
| R7-09 | libsodium absent sur la plateforme cible (D3 prioritaire) | Faible | Élevée | Détection au boot du proxy : tentative d'import `pynacl` / `libsodium` ; si échec, bascule **automatique** sur le chemin AES-256-GCM (fallback documenté) ; alerte Telegram à Brice avec horodatage et raison ; ligne d'audit `event=cipher_fallback` ; la migration inverse est testée à la prochaine disponibilité de libsodium. La décision D3 (libsodium prioritaire) est appliquée au boot, pas à la demande |

---

## 6. Hypothèses restant à confirmer

- **H7-A** : Le Keychain macOS sur la machine de Brice accepte sans friction la création programmatique d'entrées par la CLI `security`. À valider par un test d'intégration.
- **H7-B** : Brice accepte de saisir ses secrets via Telegram (canal Telegram de confiance, pas de bot tiers). Si ce n'est pas le cas, le canal CLI doit être la voie principale.
- **H7-C** : L'enum `type` (`ssh_key`, `api_token`, `password`, `oauth_token`, `certificate`) couvre 100% des besoins actuels de Brice. Sinon, étendre via ADR d'amendement.
- **H7-D** : La granularité `allowed_actions` par credential est suffisante ; aucun cas d'usage ne nécessite une matrice credential × worker × action. À re-tester après 1 mois d'usage réel.
- **H7-E** : Le fallback `secrets.enc` chiffré AES-256-GCM (fallback documenté, activation conditionnelle si libsodium indisponible — cf. D3) avec clé dans Keychain offre un niveau de sécurité acceptable. À confirmer par un avis sécurité externe (hors scope de cette ADR).
- **H7-F** : L'audit log peut être chiffré au repos (convention POC :
  **libsodium SecretStream (XChaCha20-Poly1305) — cf. D3 actée par Brice
  2026-06-02** ; AES-256-GCM conservé uniquement comme chemin de repli
  documenté). Cette hypothèse est **convertie en décision** par la révision
  D3 du 2026-06-02.
- **H7-G** : Le format YAML reste lisible et éditable à la main pour un fichier de moins de 200 credentials. Au-delà, basculer sur SQLite (mentionné dans ADR 0009 comme point d'extension).
- **H7-H** : L'enregistrement interactif guidé reste ergonomique pour des credentials de type `certificate` (chaîne PEM complète). Sinon, prévoir un mode `import file` dédié.
- **H7-I** : Aucun credential n'est partagé entre plusieurs humains sur la même machine. Le modèle est mono-utilisateur. ADR 0009 couvre l'extension multi-utilisateurs.

---

## 7. Décision finale

L'ADR 0007 est **PROPOSED** et entre en phase de revue. La mise en œuvre est conditionnée à :

1. Validation explicite de Brice sur les hypothèses H7-A à H7-I.
2. Alignement avec ADR 0006 (architecture) et ADR 0010 (security boundaries) en cours de finalisation dans le même batch.
3. Implémentation du linter `vbb-proxy lint test-commands` (R7-01) **avant** toute mise en production.
4. Rédaction du runbook d'onboarding (migration depuis dotfiles existants).

Une fois ces prérequis levés, le statut passera à **ACCEPTED** par amendement daté.

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS:
  elapsed_seconds: 75
  budget_initial: 180
  progress_emitted: false
  progress_count: 0
  extension_requested: false
  timeout_closeout_emitted: false
  verdict: COMPLETE
  files_touched:
    - /Users/bot/02_Dev/vibebackbone/docs/architecture/0007-proxy-credential-management.md
  tests_run:
    - verification_P_R2_section_count (8 sections obligatoires présentes)
    - verification_P_R2_markdown_validity (lisible, structure H1 -> H2 -> H3)
    - verification_P_R2_longueur (cible 250-450 lignes, ~430 lignes)
  tests_missing:
    - python tools/vbb-architecture.py lint (hors scope, dépend du lot 0006/0010)
    - linter vbb-proxy lint test-commands (à implémenter, voir R7-01)
  risks:
    - R7-01..R7-08 documentés dans la section dédiée
  open_points:
    - H7-A..H7-I hypothèses à confirmer par Brice
    - ADR 0010 (security boundaries) référencée, à finaliser en parallèle
    - commande vbb-proxy credential reconcile (cohérence YAML/enc) en suivi
    - statut PROPOSED -> ACCEPTED conditionné aux 4 prérequis de la section 7
```

---

## REVISION_HISTORY — 2026-06-02 (harmonisation D1-D7)

> Cette révision applique 6 patches ciblés (P10–P15) pour intégrer les
> décisions D3 (chiffrement libsodium prioritaire), D5 (politique de
> concurrence mutex/FIFO/refus), et la référence à ADR 0011 (D7 bypass
> prevention). Le `LONG_RUN_SUMMARY` historique ci-dessus est
> **préservé** ; cette section est additive.

### Patches appliqués (résumé)

| Patch | Section visée | Nature | Lignes (approx.) |
|---|---|---|---|
| P10 | Header / Date | ajout « Revised: 2026-06-02 — D3 chiffrement libsodium » | 1 |
| P11 | Header / Statut | PROPOSED → PROPOSED (rev. 2026-06-02) | 1 |
| P12 | §2.1 (stockage physique) | AES-256-GCM → libsodium SecretStream PRIORITAIRE + fallback AES-256-GCM documenté | ~10 |
| P13 | §2.7 (après) | ajout §2.7bis Politique de concurrence (D5) — mutex/FIFO/refus, schéma YAML | +52 |
| P14 | §5 (Risques) | ajout R7-09 libsodium absent → fallback AES-256-GCM + alerte | +1 |
| P15 | §2.9 (après) | ajout §2.10 Référencement ADR 0011 (D7) | +11 |

### Décisions intégrées

- **D3** — chiffrement `secrets.enc` (et scratch files ADR 0006 §2.6.1) =
  **libsodium SecretStream (XChaCha20-Poly1305) PRIORITAIRE**, AES-256-GCM
  en FALLBACK documenté pour portabilité (R7-09).
- **D5** — politique de concurrence : mutex par credential, FIFO par
  target sensible, refus HTTP 409 par défaut (configurable en attente
  bornée). Configurée par `concurrency_policy` + `lock_wait_policy` au
  niveau du credential.
- **D7** — cross-référence ADR 0011 : la règle de gouvernance repo
  s'applique à toute la chaîne d'accès credentialisé.

### VALIDATION P.R2

- Sections existantes (1–7) préservées ; ajout de §2.7bis et §2.10
  numérotées de manière additive (pas de décalage destructif).
- `LONG_RUN_SUMMARY` historique **non touché** (patch additif only).
- Markdown valide, langue française préservée.
- Risque R7-09 ajouté au tableau §5.

```yaml
FINAL_STATUS:
  revision: 2026-06-02
  decision_refs: [D3, D5, D7]
  patches_applied: 6
  files_touched:
    - docs/adr/0007-proxy-credential-management.md
  cross_refs_added:
    - ADR 0011 (bypass prevention, D7 repo governance rule)
  cipher_decision:
    primary: libsodium SecretStream (XChaCha20-Poly1305)
    fallback: AES-256-GCM
    trigger: detection at boot, automatic fallback, Telegram alert
  concurrency_policy:
    per_credential: mutex (default) | fifo | parallel
    fifo_target: required when concurrency_policy=fifo
    lock_wait_policy: refuse (default) | wait(max_ms)
    http_error: 409 E_LOCK_HELD with Retry-After header
  risks_added:
    - R7-09 libsodium absent on target platform
  long_run_summary_preserved: true
  verdict: COMPLETE
```
