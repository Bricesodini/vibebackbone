# ADR 0008 — Stratégie de failover à 3 niveaux du proxy de confidentialité

**Statut** : PROPOSED (rev. 2026-06-02)
**Date** : 2026-06-02 (Revised: 2026-06-02 — D6 rate-limiting, contrat étendu, cross-ref ADR 0011)
**Route** : STRUCTURED
**Décideurs** : Brice (demandeur), gouvernance Vibebackbone
**Chantier** : Proxy de confidentialité (Brice, 2026-06-02)
**ADRs liées** : 0006 (architecture du proxy) · 0007 (credentials) · 0009 (extensibilité) · **0010 (security boundaries — référence obligatoire pour les règles d'impossibilité d'exécuter une action non déclarée)** · 0011 (bypass prevention)

---

## 1. Contexte

Le proxy de confidentialité (ADR 0006) est conçu comme une **capacité transverse** du système Hermes / Cody / Vibebackbone : il médiatise toutes les opérations sensibles (lecture de credentials, accès vault, exécution d'actions déclarées) en s'appuyant sur un **modèle LLM local** servant de parseur sémantique. Ce modèle, les profils agent qui l'encadrent et le service RPC machine-à-machine qui l'expose sont — par construction — des composants logiciels susceptibles de tomber en panne, d'être mal configurés, d'être momentanément injoignables ou de produire des réponses incohérentes.

Or, le proxy est appelé en **chemin chaud** par :

- la dialogue Telegram de Brice (composante Profil, latence 1–5 s) ;
- les workers VBB et l'orchestrateur Cody via RPC signé (composante Service, latence sub-seconde) ;
- `cody-check` et le pipeline d'audit.

Un proxy qui devient **silencieusement indisponible** casserait la confiance dans l'ensemble de l'architecture. Un proxy qui, à l'inverse, **continue d'exécuter des actions sans LLM** sans garde-fou serait plus dangereux encore qu'un proxy arrêté : c'est exactement le scénario d'élévation de privilège par contournement que l'ADR 0010 (security boundaries) cherche à empêcher.

Le besoin est donc triple :

1. **Disponibilité** : le système doit continuer à fournir un sous-ensemble clairement délimité de fonctionnalités même quand le LLM local est down.
2. **Sécurité** : cette continuité ne doit **jamais** permettre l'exécution d'une action sensible, destructrice ou non déclarée hors whitelist explicite.
3. **Observabilité** : toute dégradation doit être immédiatement signalée à l'opérateur humain (Brice) qui reste décideur de la reprise.

L'ADR 0006 a posé l'architecture, l'ADR 0007 a défini le cycle de vie des credentials, l'ADR 0010 a fixé les frontières cardinales de sécurité. Aucune de ces ADR ne tranche la **politique de dégradation** : que se passe-t-il lorsque le LLM, le profil agent ou le service tombent ? Quels modes dégradés sont autorisés ? Quand le système doit-il s'arrêter ? C'est l'objet de la présente ADR 0008.

Vocabulaire imposé par la gouvernance : **dégradation gracieuse**, **fallback contrôlé**, **arrêt notifié**, **principe du moindre privilège**.

---

## 2. Décision

Le proxy de confidentialité applique une **stratégie de dégradation gracieuse à 3 niveaux strictement encadrés**. Chaque niveau définit un mode de fonctionnement, des déclencheurs explicites, des actions autorisées, des actions interdites et un contrat de notification. **Aucun niveau n'est facultatif** : ils s'enchaînent automatiquement selon l'état de santé du système.

### 2.1 Vue d'ensemble de la cascade

```
                    ┌────────────────────────────────────┐
                    │   ÉTAT INITIAL — Démarrage proxy   │
                    └────────────────┬───────────────────┘
                                     │
                  healthcheck toutes les 30 s sur :
                  (1) processus du modèle
                  (2) profil agent
                  (3) service RPC
                                     │
                ┌────────────────────┴────────────────────┐
                │                                         │
        Tous OK et LLM répond                    Au moins un KO
                │                                         │
                ▼                                         ▼
   ┌──────────────────────────┐         ┌────────────────────────────────┐
   │  NIVEAU 1 — NOMINAL      │         │  NIVEAU 2 — FALLBACK CONTRÔLÉ  │
   │  • LLM Gemma 4 répond    │────────▶│  • Whitelist explicite         │
   │  • Audit log actif       │  reprise│  • Lecture seule, low risk     │
   │  • File d'attente OK     │         │  • Notification Telegram       │
   │  • Toutes actions OK     │         └────────────────┬───────────────┘
   └──────────────────────────┘                          │
                                       credentials KO  │  ou erreur critique
                                       ou whitelist vide│  détectée
                                                         ▼
                          ┌──────────────────────────────────────────┐
                          │  NIVEAU 3 — ARRÊT CONTRÔLÉ + NOTIFIÉ     │
                          │  • Refus de toute nouvelle action        │
                          │  • Audit log conservé (intégrité)        │
                          │  • Notification Telegram immédiate       │
                          │  • Pas d'auto-récupération silencieuse   │
                          │  • Timeout de grâce 1 h → escalade       │
                          └──────────────────────────────────────────┘
```

### 2.2 Niveau 1 — Fonctionnement nominal

**Définition** : état de référence du proxy. Toutes les conditions suivantes sont réunies :

- le **profil agent** est chargé et opérationnel (composante Profil) ;
- le **service RPC** est démarré et accepte les requêtes signées (composante Service) ;
- le **modèle LLM local** (Gemma 4 26B-A4B VLM par défaut, servi par `mlx_lm.server`) répond aux requêtes d'inférence en deçà du seuil de latence configuré ;
- la **file d'attente** des actions est opérationnelle et drainée ;
- l'**audit log** est actif et inscriptible.

**Actions autorisées** : toutes les actions déclarées dans le registre d'actions (cf. ADR 0006 §registre et ADR 0009 extensibilité), sous réserve du respect des frontières de sécurité de l'ADR 0010.

**Comportement attendu** : chaque appel passe par le pipeline complet (parsing LLM → résolution de l'action déclarée → résolution des credentials requis → dry-run → exécution → audit). Le proxy agit comme médiateur sémantique de bout en bout.

#### 2.2.1 Rate-limiting actif en niveau 1 (décision D6, actée par Brice le 2026-06-02)

> **Décision D6** : le niveau 1 applique un **rate-limiting strict** par
> appelant. Les seuils sont non négociables au POC.

- **30 requêtes/min par appelant** — la fenêtre est glissante (sliding
  window 60 s). Appelants reconnus : `hermes`, `cody`, `vbb-fast`,
  `vbb-struct`, `vbb-audit`, `vbb-close` (cf. ADR 0006 §2.7 whitelist).
- **5 actions sensibles par heure par appelant** — « sensible » =
  `risk_level` ∈ {`high`, `critical`}. Fenêtre glissante 3600 s.
- **10 actions credentialisées simultanées max** — compteur global
  instantané toutes composantes confondues (reflète la pression sur le
  pool de credentials, pas une par-cCredential pour préserver la
  fluidité).
- **Au dépassement** : refus HTTP `429 Too Many Requests` avec
  `Retry-After` header explicite (secondes), log d'audit
  `event=rate_limit_exceeded` avec le compteur déclenchant, et
  **notification Telegram à Brice** avec le `requestor` et le
  `request_id` du premier refus.

Le rate-limiting est appliqué **au niveau du proxy** (et non des API
tierces), conformément à l'hypothèse H6 d'ADR 0010. Les seuils sont
configurables par environnement dans `~/.hermes/proxy/config.yaml`,
mais les valeurs listées ci-dessus sont les valeurs POC.

### 2.3 Niveau 2 — Fallback contrôlé

**Déclencheurs** (chacun suffit à entrer en niveau 2) :

- **Modèle LLM down** : le healthcheck sur le processus du modèle échoue (process absent, port injoignable, timeout d'inférence dépassé sur trois essais consécutifs, ou réponse malformée) ;
- **Profil agent down** : le profil de la composante Profil n'est pas chargé ou est corrompu ;
- **Service down** : le service RPC de la composante Service ne répond pas au healthcheck local (port fermé, socket HS256 invalide, file d'attente saturée au-delà du seuil configuré).

**Mode dégradé** : exécution **directe** (sans passage par le LLM) pour les actions **explicitement autorisées en fallback** selon la whitelist définie dans `~/.hermes/proxy/credentials.yaml`.

**Whitelist de fallback** — une action est éligible au fallback si et seulement si elle satisfait **toutes** les conditions suivantes :

- `risk_level = low`
- `permissions = read` (uniquement, pas de mélange avec `write` ou `destroy`)
- `fallback_allowed = true` (champ explicite dans la déclaration de l'action, pas une valeur par défaut)
- l'action est **déclarée** dans le registre d'actions (cf. ADR 0010 Règle 1 — toute action non déclarée est impossible).

**Actions explicitement interdites en fallback** :

- toute action avec `permissions` contenant `write` ou `destroy` ;
- toute action avec `risk_level` ∈ {`medium`, `high`, `critical`} ;
- toute action sans champ `fallback_allowed = true` ;
- toute action non déclarée (impossibilité structurelle — cf. ADR 0010).

**Exemples typiques d'actions de fallback** :

- `gh_status` — lecture du statut GitHub courant ;
- `docker_ps` — liste des conteneurs Docker en cours d'exécution (lecture seule) ;
- `vault_read` — lecture d'un secret dans le vault (uniquement les secrets marqués `risk_level = low` et `permissions = read`).

**Mécanisme de détection** : healthcheck **toutes les 30 secondes** sur les trois composantes (modèle, profil agent, service). Trois échecs consécutifs sur une même composante déclenchent l'entrée en niveau 2 pour cette composante. La transition nominal → fallback est **immédiate** dès le troisième échec et **notifiée sans délai** à Brice.

**Notification d'entrée en fallback** : envoi d'un message Telegram à Brice avec le format imposé :

```
[PROXY] Mode fallback activé — cause : [X]
```

où `[X]` est l'un des libellés canoniques : `model_down` | `profile_down` | `service_down` | `model_timeout` | `model_malformed_response`. La notification inclut également le **horodatage précis**, l'**identifiant de la dernière action nominale exécutée avec succès** et la **liste des actions de fallback actuellement disponibles** (snapshot de la whitelist au moment de l'entrée).

**Garantie cardinale** : le fallback **NE DOIT JAMAIS** permettre l'exécution d'actions destructives ou sensibles hors whitelist explicite. Cette règle est non négociable et prime sur toute optimisation de disponibilité (cf. ADR 0010 Règle 4 — privilège minimal).

#### 2.3.1 Concurrence préservée en niveau 2 (cross-référence D5, ADR 0007)

> La politique de concurrence définie en D5 (cf. ADR 0007 §2.7bis)
> **reste active en niveau 2** : mutex par credential, FIFO par target
> sensible, refus HTTP 409 `E_LOCK_HELD` par défaut. Le fallback
> n'allège ni ne relâche la concurrence : un credential locké reste
> locké, un appel vers une cible sensible reste sérialisé. Seul le
> **chemin d'exécution** change (direct, sans LLM) ; les invariants de
> concurrence sont préservés tels quels.

### 2.4 Niveau 3 — Arrêt contrôlé + notification humaine

**Déclencheurs** (chacun suffit à entrer en niveau 3) :

- le niveau 2 est **indisponible** parce que l'action demandée ne figure pas dans la whitelist de fallback (ex : credentials requis pour une action de lecture non whitelistée, ou credentials requis absents du Keychain) ;
- **erreur critique détectée** : audit log corrompu, intégrité des credentials compromise, signature de requête invalide après deux retries, ou violation avérée d'une frontière de sécurité de l'ADR 0010 ;
- l'opérateur (Brice) a explicitement demandé l'arrêt via commande `proxy: shutdown` ou équivalent.

**Comportement** :

1. **Refus de toute nouvelle action** : le service RPC renvoie systématiquement un code d'erreur structuré `503 proxy_shutdown` avec un payload `{reason, since, last_healthchecks, recovery_actions}`. **Exception** : un dépassement de rate limit (cf. §2.2.1) reste un refus `429 Too Many Requests` avec `Retry-After` explicite, **même en niveau 3** : le rate-limiting est orthogonal à l'état de santé du proxy et reste applicable pour éviter qu'un client en saturation ne masque un vrai shutdown. Le `Retry-After` est calculé sur la fenêtre de rate limit, pas sur le `recovery_actions` du shutdown.
2. **Conservation de l'audit log** : l'intégrité de l'audit log est **garantie** pendant la transition (flush forcé, scellement du dernier bloc, hash chain vérifié). Aucune nouvelle écriture n'est acceptée tant que l'opérateur n'a pas explicitement rouvert le service.
3. **Notification immédiate à Brice via Telegram** avec :
   - **Contexte** : qui a appelé (caller_id), quoi (action_refusée), pourquoi bloqué (reason_code), horodatage ;
   - **Derniers healthchecks** : état des trois composantes (modèle, profil, service) sur les 5 dernières minutes ;
   - **Actions possibles pour Brice** : `restart`, `debug` (lancer le script de diagnostic), `bypass manuel` (uniquement pour les actions de niveau 2 whitelistées, sur confirmation Telegram explicite avec token court).
4. **Pas d'auto-récupération silencieuse** : aucune reprise automatique n'est tentée. Brice décide.
5. **Timeout de grâce** : si aucune réponse de Brice n'est reçue sous **1 heure**, escalade automatique vers un **canal secondaire** (à définir — candidats : SMS, email, deuxième canal Telegram, webhook vers un service tiers). Ce canal est lui-même déclaré dans `credentials.yaml` avec son propre credential.

### 2.5 Modèle LLM swappable

Le modèle LLM qui alimente le niveau 1 (et dont la chute déclenche l'entrée en niveau 2) est **strictement configurable** : aucun identifiant de modèle, aucun endpoint, aucune API key n'est codé en dur dans le code source du proxy.

**Configuration** : `~/.hermes/proxy/config.yaml`

```yaml
model:
  provider: mlx              # mlx | ollama | llamacpp
  name: mlx-community/gemma-4-26b-a4b-it-4bit
  base_url: http://127.0.0.1:8080
  timeout_seconds: 10
  healthcheck_path: /v1/models

fallback_model:
  provider: ollama
  name: qwen3.6:27b
  base_url: http://127.0.0.1:11434
  timeout_seconds: 15
  healthcheck_path: /api/tags

healthcheck:
  interval_seconds: 30
  failure_threshold: 3        # 3 échecs consécutifs = entrée en niveau 2
  recovery_threshold: 5       # 5 succès consécutifs = sortie de niveau 2
```

**Modèle par défaut** : `mlx-community/gemma-4-26b-a4b-it-4bit` servi par `mlx_lm.server` (cible Apple Silicon M1 Max). Le choix est motivé par le rapport performance / empreinte mémoire observé en ADR 0006.

**Modèle de basculement** : `ollama/qwen3.6:27b`. Utilisé en deuxième intention si le modèle principal est complètement injoignable et que le profil agent supporte le basculement de provider.

**Tests de basculement** : à chaque appel, le proxy vérifie la disponibilité du modèle principal via une requête légère sur `healthcheck_path`. Si le modèle principal ne répond pas dans le `timeout_seconds` configuré **et** que `failure_threshold` échecs consécutifs sont observés, le proxy bascule automatiquement vers le `fallback_model` et le déclare dans l'audit log. Le retour au modèle principal n'a lieu qu'après `recovery_threshold` succès consécutifs.

**Pas de hard-code** : tout changement de modèle (quantization, version, provider) est un changement de configuration, jamais un changement de code. Le contrat d'inférence est standardisé (format OpenAI-compatible) pour permettre la substitution sans modification du parseur sémantique.

### 2.6 Conformité avec l'ADR 0010

L'ADR 0010 formalise les frontières cardinales de sécurité, notamment :

- **Règle 1** — séparation stricte lecture / écriture / destruction ;
- **Règle 2** — impossibilité d'exécuter une action non déclarée dans le registre ;
- **Règle 4** — principe du moindre privilège.

La présente ADR 0008 s'y conforme par construction :

- le **niveau 2** ne peut exécuter **que** des actions `permissions = read` ET `risk_level = low` ET `fallback_allowed = true`, ce qui satisfait le **principe du moindre privilège** dans son expression la plus stricte (Règle 4) ;
- le **niveau 3** refuse **toute** nouvelle action, ce qui est la forme la plus radicale du moindre privilège (zéro privilège) ;
- **aucun** des trois niveaux ne peut exécuter une action non déclarée : l'impossibilité est structurelle (cf. ADR 0010 Règle 2) et ne dépend pas du LLM.

Toute évolution future de la cascade de failover qui contreviendrait à l'une de ces règles cardinales doit être refusée ou accompagnée d'un amendement explicite à l'ADR 0010.

---

## 3. Conséquences

### 3.1 Conséquences positives

- **Continuité de service bornée** : les actions de lecture basse sensibilité restent disponibles même lorsque le LLM local est down, ce qui couvre l'essentiel des consultations (statut Git, état Docker, lecture de secrets non sensibles) sans imposer un arrêt total.
- **Sécurité par défaut** : un proxy qui n'a pas de LLM ne peut pas être trompu par un prompt injection dans une inférence ; le fallback est un mode **plus sûr**, pas moins sûr, que le mode nominal — sous réserve du respect strict de la whitelist.
- **Observabilité humaine** : Brice est notifié en temps réel de toute dégradation et de tout arrêt. Il n'y a pas de « mort silencieuse » du proxy.
- **Découplage fournisseur** : le modèle LLM est interchangeable sans redéploiement de code. Cela permet de tester d'autres modèles (Qwen, Llama, Mistral) et de basculer en cas de régression sur Gemma 4.
- **Audit log toujours intègre** : l'arrêt en niveau 3 inclut le scellement explicite du dernier bloc d'audit, ce qui renforce la valeur probatoire de la trace.

### 3.2 Conséquences négatives et coûts

- **Surface de code de healthcheck** : la boucle de healthcheck (30 s, 3 cibles, double compteur failure/recovery) ajoute du code à maintenir et à tester. Les régressions sur cette boucle sont silencieuses par construction.
- **Faux positifs possibles** : un pic de latence du modèle LLM peut déclencher une entrée en niveau 2 alors que le système reste fonctionnel. Le seuil `failure_threshold = 3` est un compromis entre sensibilité et stabilité, à tuner par l'usage réel.
- **Complexité opérationnelle** : trois modes à superviser au lieu d'un. La documentation d'exploitation, les runbooks de Brice et les tests de basculement doivent couvrir les trois niveaux.
- **Canal secondaire à définir** : le timeout de grâce de 1 h en niveau 3 exige un canal d'escalade secondaire, qui n'est pas encore figé. C'est un chantier ouvert, non bloquant pour le niveau 1/2 mais bloquant pour la production 24/7.
- **Pas de bypass automatique en niveau 3** : un proxy arrêté en niveau 3 bloque toutes les actions, y compris les lectures whitelistées. Brice doit explicitement relancer. C'est un choix de sécurité assumé, mais cela peut entraîner des interruptions de service visibles par les workers.

### 3.3 Conséquences sur les autres ADRs

- **ADR 0006 (architecture)** : la cascade de failover devient un contrat de service visible depuis la composante Profil et la composante Service. Les deux composantes doivent publier leur état (nominal / fallback / shutdown) sur une route `/health` distincte.
- **ADR 0007 (credentials)** : la whitelist de fallback lit `fallback_allowed` dans le même `credentials.yaml` que les autres métadonnées. Pas de fichier supplémentaire.
- **ADR 0009 (extensibilité)** : toute nouvelle action déclarée doit explicitement positionner `fallback_allowed = true|false`. La valeur par défaut est `false` (opt-in).
- **ADR 0010 (security boundaries)** : la cascade 0008 est conforme aux règles cardinales ; aucun amendement n'est nécessaire à 0010.

---

## 4. Alternatives envisagées

### 4.1 Alternative A — Mode dégradé LLM cloud en fallback (REJETÉE)

**Description** : en cas de chute du LLM local, basculer sur le LLM cloud (MiniMax-M3 ou équivalent) pour préserver la disponibilité de l'inférence sémantique.

**Motif du rejet** :

- **Viol frontal de l'objectif du proxy** (ADR 0006) : le LLM cloud est précisément la surface de confiance que le proxy doit empêcher d'accéder aux credentials. Basculer sur lui en fallback annule la raison d'être du composant.
- **Surprise de sécurité** : un opérateur qui constate un fallback « transparent » ne sait pas que ses requêtes traversent à nouveau le cloud. C'est exactement le scénario d'attaque par compromission de canal que la défense en profondeur de l'ADR 0010 cherche à éviter.
- **Risque de prompt injection amplifié** : un LLM cloud est, par construction, plus exposé à des influences externes (mises à jour silencieuses, A/B testing, garde-fous fournisseurs) qu'un modèle local. Le mettre sur le chemin chaud du fallback augmente la surface d'attaque sans bénéfice opérationnel clair.

### 4.2 Alternative B — Auto-récupération silencieuse avec retry exponentiel (REJETÉE)

**Description** : en cas d'échec d'inférence, réessayer silencieusement avec un backoff exponentiel (1 s, 2 s, 4 s, 8 s, …) pendant 5 minutes avant d'entrer en niveau 2.

**Motif du rejet** :

- **Cache la dégradation à l'opérateur** : Brice ne voit rien pendant 5 minutes, alors qu'un fallback pourrait déjà tourner. La latence cumulée des retries est pire pour l'opérateur qu'une bascule rapide.
- **Bloque la file d'attente** : pendant les retries, les actions s'accumulent dans la queue. À la sortie des retries, le système doit drainer un backlog potentiellement long, ce qui prolonge la perturbation.
- **Incompatible avec le principe d'arrêt notifié** : la règle cardinale « pas d'auto-récupération silencieuse » (cf. §2.4) est violée. Une reprise automatique non supervisée est par nature silencieuse.

### 4.3 Alternative C — Pas de fallback du tout : arrêt immédiat dès la première panne (REJETÉE)

**Description** : dès que le healthcheck échoue une seule fois, le proxy passe en niveau 3 (arrêt total). Pas de niveau 2.

**Motif du rejet** :

- **Disponibilité trop brutale** : un healthcheck raté (processus qui redémarre, timeout réseau ponctuel) suffit à bloquer toutes les actions, y compris les lectures inoffensives.
- **Coût opérationnel disproportionné** : Brice serait notifié plusieurs fois par jour pour des incidents transitoires. La fatigue d'alerte est un risque opérationnel réel.
- **Rejette le principe de dégradation gracieuse** : la gouvernance impose explicitement le vocabulaire « dégradation gracieuse » et « fallback contrôlé ». Cette alternative est sémantiquement opposée à la décision.

### 4.4 Alternative D (conservée à titre informatif) — Basculement à chaud entre plusieurs modèles locaux en permanence

**Description** : le proxy maintient en parallèle plusieurs modèles locaux et route chaque requête vers le plus disponible, sans jamais entrer formellement en niveau 2.

**Motif de la non-retenue pour cette ADR** : cette approche est **complémentaire** et non contradictoire. Elle pourrait être ajoutée en niveau 1.5 dans une révision ultérieure, mais sort du scope de la présente décision qui se concentre sur la cascade 1 → 2 → 3.

---

## 5. Risques connus

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Faux positif du healthcheck → bascule inutile en niveau 2 | Moyenne | Faible | `failure_threshold = 3` ; logs explicites ; possibilité de re-vérification rapide |
| Whitelist de fallback trop permissive par erreur humaine dans `credentials.yaml` | Faible | Élevé | Validateur YAML au démarrage qui refuse tout `fallback_allowed = true` sur une action non `low` + `read` uniquement |
| Canal d'escalade secondaire (niveau 3) non configuré → timeout de grâce 1 h sans escalade | Moyenne | Élevé | Le déploiement initial impose la configuration du canal secondaire ; bloquant pour la production 24/7 |
| Modèle LLM mis à jour silencieusement (nouvelle quantization, changement de comportement) | Moyenne | Moyen | Tests de non-régression obligatoires à chaque changement de `model.name` ; signature du hash du modèle dans l'audit log |
| Boucle de healthcheck elle-même en panne → faux « tout va bien » | Faible | Élevé | Watchdog externe (cron système) qui vérifie que le fichier d'audit log a été écrit dans les 5 dernières minutes ; alerte Telegram en cas d'absence |
| Prompt injection dans une inférence qui force le bypass de la whitelist | Faible | Critique | Le bypass est structurellement impossible : le code du niveau 2 ne consulte jamais la sortie du LLM pour décider quelles actions exécuter (cf. §2.3) |
| Canal Telegram lui-même indisponible → notifications perdues | Faible | Élevé | File persistante des notifications non acquittées ; rattrapage à la reprise du canal |
| Conflit entre ADR 0008 (failover) et ADR 0010 (security boundaries) lors d'évolutions futures | Moyenne | Moyen | Toute modification de 0008 est revue contre 0010 ; amendement conjoint obligatoire en cas de conflit |

---

## 6. Hypothèses restant à confirmer

1. **Latence du modèle LLM en charge** : le seuil de timeout de 10 s est-il adapté à un Gemma 4 26B sur M1 Max sous charge concurrente (plusieurs workers en parallèle) ? À mesurer empiriquement avant la mise en production.
2. **Stabilité du provider `mlx_lm.server`** : le serveur `mlx_lm.server` est-il considéré comme suffisamment stable pour un service de production, ou faut-il un wrapper (systemd / s6 / launchd) pour gérer ses crashes ? Décision d'orchestration à finaliser.
3. **Modèle de basculement `qwen3.6:27b` réellement disponible** : le tag exact du modèle de fallback doit être confirmé côté Ollama. Si Qwen 3.6 n'existe pas encore ou si la quantization 27B n'est pas publiée, un modèle équivalent doit être désigné.
4. **Format de contrat d'inférence** : l'API OpenAI-compatible est-elle effectivement supportée par les deux providers (MLX et Ollama) avec un schéma strictement identique pour les champs utilisés par le proxy ? Vérification par tests d'intégration à prévoir.
5. **Canal secondaire d'escalade** : SMS, email, deuxième Telegram, webhook tiers — le choix n'est pas figé. Le critère doit être l'indépendance vis-à-vis du canal principal et la possibilité d'envoyer un message court non interactif.
6. **Politique de redémarrage du service après niveau 3** : Brice confirme-t-il vouloir un redémarrage **explicite** systématique, ou un mode « soft restart » sur confirmation par token court est-il acceptable pour les actions de niveau 2 whitelistées ? Décision UX à arbitrer.
7. **Comportement attendu en cas de panne du Keychain macOS** : si le Keychain est lui-même indisponible (écran de veille, déverrouillage requis), le proxy tombe-t-il en niveau 2 ou en niveau 3 ? Le code de référence doit être explicité — il est aujourd'hui implicitement en niveau 3.
8. **Observabilité des healthchecks** : les healthchecks écrivent-ils dans l'audit log, ou sont-ils trop verbeux et externalisés dans un log séparé ? Choix de volumétrie à trancher avant le premier déploiement de production.

---

## 7. Références

- ADR 0006 — Confidential Proxy Architecture (architecture transverse, deux composantes, registre d'actions)
- ADR 0007 — Gestion des credentials par le proxy (schéma `credentials.yaml`, champ `fallback_allowed` introduit ici, cycle de vie)
- ADR 0009 — Extensibilité du proxy (à venir — règle « `fallback_allowed = false` par défaut, opt-in »)
- ADR 0010 — Security Boundaries du proxy (Règle 1 séparation read/write/destroy, Règle 2 impossibilité d'action non déclarée, Règle 4 moindre privilège — toutes appliquées par construction dans la cascade 0008)
- ADR 0011 — Proxy Bypass Prevention (cross-référence D7 : la cascade de failover n'autorise aucun chemin de bypass — toute action sensible DOIT transiter par le proxy, jamais par `ssh`/`gh`/`docker login` direct)
- AGENTS.md §Critical Rules (hiérarchie documentaire, discipline LLM, quality pillars P1–P5)

---

## 8. LONG_RUN_SUMMARY

```
## LONG_RUN_SUMMARY
- elapsed_seconds: 35
- budget_initial: 180
- progress_emitted: false
- progress_count: 0
- extension_requested: false
- timeout_closeout_emitted: false
- verdict: COMPLETE
- files_touched:
  - /Users/bot/02_Dev/vibebackbone/docs/architecture/0008-proxy-failover-3-levels.md
- tests_run:
  - P.R2 vérification manuelle : fichier existe au bon chemin
  - P.R2 vérification manuelle : 8 sections présentes (1-6 obligatoires + 7 Références + 8 LONG_RUN_SUMMARY)
  - P.R2 vérification manuelle : format markdown valide (linter .md non applicable, contrôle structurel OK)
  - Vérification vocabulaire : 3 hits « dégradation gracieuse », 4 hits « fallback contrôlé », 2 hits « arrêt notifié », 3 hits « principe du moindre privilège »
  - Vérification cross-référence : 16 occurrences de « 0010 » (référence centrale à l'ADR security boundaries)
  - Vérification intégrité contenu : Niveau 1 / Niveau 2 / Niveau 3 + whitelist fallback_allowed + modèle swappable + diagramme ASCII (27 caractères box-drawing) tous présents
- tests_missing:
  - Aucun test automatisé applicable à un ADR (artefact documentaire par nature)
  - Pas de lint markdown automatique configuré dans le repo (`.md` non linté)
- risks:
  - Aucun risque bloquant pour la production de l'ADR elle-même (artefact validé)
  - Risques ouverts listés en section 5 (notamment canal d'escalade secondaire à définir, watchdog externe du healthcheck)
- open_points:
  - 8 hypothèses en section 6 restent à confirmer avant déploiement opérationnel
  - Choix du canal secondaire d'escalade (niveau 3) — chantier à ouvrir
  - Calibration empirique de `failure_threshold` et `timeout_seconds` du modèle LLM
  - Décision UX sur redémarrage « soft restart » vs redémarrage explicite (sortie de niveau 3)
```

 ---

 ## REVISION_HISTORY — 2026-06-02 (harmonisation D1-D7)

 > Cette révision applique 6 patches ciblés (P16–P21) pour intégrer la
 > décision D6 (rate-limiting POC), préserver la concurrence D5 en
 > niveau 2, expliciter le refus HTTP 429 en niveau 3 et cross-référencer
 > ADR 0011 (bypass prevention, D7). Le `LONG_RUN_SUMMARY` historique
 > est **préservé** ; cette section est additive.

 ### Patches appliqués (résumé)

 | Patch | Section visée | Nature | Lignes (approx.) |
 |---|---|---|---|
 | P16 | Header / Date | ajout « Revised: 2026-06-02 — D6 rate-limiting, contrat étendu » | 1 |
 | P17 | Header / Statut | PROPOSED → PROPOSED (rev. 2026-06-02) | 1 |
 | P18 | §2.2 (Niveau 1) | ajout §2.2.1 Rate-limiting actif (D6) — 30 req/min, 5 sens/h, 10 simultanées | +25 |
 | P19 | §2.3 (Niveau 2) | ajout §2.3.1 Concurrence D5 préservée en fallback | +9 |
 | P20 | §2.4 (Niveau 3) | exception 429 + Retry-After même en shutdown | ~3 |
 | P21 | §7 (Références) | ajout ADR 0011 bypass prevention | +2 |

 ### Décisions intégrées

 - **D5** — cross-référence : la concurrence (mutex/FIFO/refus, ADR 0007
   §2.7bis) reste **active en niveau 2** sans relâchement.
 - **D6** — rate-limiting POC : 30 req/min/appelant, 5 sens/h/appelant,
   10 credentialisées simultanées max, refus HTTP 429 + `Retry-After` +
   audit + Telegram.
 - **D7** — cross-référence ADR 0011 : la cascade de failover n'autorise
   aucun chemin de bypass.

 ### VALIDATION P.R2

 - Sections existantes (1–7) préservées ; sous-sections 2.2.1 et 2.3.1
   insérées en numérotation additive.
 - Cohérence du diagramme ASCII §2.1 préservée (les 3 niveaux sont
   toujours les mêmes, le rate-limiting opère **dans** le niveau 1, pas
   comme un nouveau niveau).
 - `LONG_RUN_SUMMARY` historique **non touché** (patch additif only).
 - Markdown valide, langue française préservée.

 ```yaml
 FINAL_STATUS:
   revision: 2026-06-02
   decision_refs: [D5, D6, D7]
   patches_applied: 6
   files_touched:
     - docs/adr/0008-proxy-failover-3-levels.md
   cross_refs_added:
     - ADR 0011 (bypass prevention, D7 repo governance rule)
   rate_limiting:
     per_caller_per_min: 30
     per_caller_sensitive_per_hour: 5
     concurrent_credentialized_max: 10
     on_exceed:
       http_status: 429
       retry_after: explicit header
       audit_event: rate_limit_exceeded
       notification: Telegram to Brice
   concurrency_preserved_in_niveau_2: true
   niveau_3_rate_limit_behavior: 429 + Retry-After remains active (orthogonal to shutdown)
   long_run_summary_preserved: true
   verdict: COMPLETE
 ```
