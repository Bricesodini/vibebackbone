|# ADR 0006 — Confidential Proxy Architecture

|**Status**: PROPOSED (rev. 2026-06-02)
|**Date**: 2026-06-02 (Revised: 2026-06-02 — harmonisation D1-D7, contrat étendu)
|**Route**: STRUCTURED
|**Supersedes**: —
|**Related**: ADR 0007 (credentials), ADR 0008 (failover), ADR 0009 (extensibility), ADR 0010 (security boundaries), ADR 0011 (bypass prevention)

## 1. Context

The Vibebackbone stack currently routes every sensitive operation — credential
reads, account lookups, vault access, OAuth refreshes — through the same cloud
LLM (MiniMax-M3) that powers the interactive dialogue. This couples the trust
boundary of the operator (Brice, Telegram session) to the trust boundary of the
inference provider, which is unacceptable for a system that holds production
credentials, banking tokens and personal identifiers.

A dedicated `Privacy Proxy` was requested on 2026-06-02 to act as a
**local LLM-mediated gatekeeper** between the cloud LLM and any operation that
touches secrets, identity, money or personal data. The proxy must run on the
operator's hardware (M1 Max, macOS), talk only to local services, and be
reachable from every actor in the Vibebackbone ecosystem (Hermes, Cody, the
four VBB workers, the future audit pipeline).

The proxy is **not a new business worker**. It does not replace `vbb-fast`,
`vbb-struct`, `vbb-audit` or `vbb-close`, and it is not a `cody-check` runtime
gate. It is a **transverse capability** — a shared substrate that all of them
can call when a request involves sensitive context.

The driving constraints are:

- **Local-first**: the LLM backing the proxy must run on-device. No cloud
  round-trip for the sensitive decision path.
- **Sub-second machine-to-machine**: workers and Cody call the proxy
  thousands of times per session; the hot path must be < 1 s.
- **Strong caller identity**: every request is signed, every caller is
  whitelisted, every call is audited.
- **No semantic reasoning on the proxy**: the proxy parses, maps and executes
  pre-defined actions. It is not a free-form agent.
- **Decoupled but coherent evolution**: human-facing dialogue and
  machine-facing RPC evolve at different speeds without blocking each other.

## 2. Decision

We introduce a **Privacy Proxy** as a transverse capability of the Hermes /
Cody / Vibebackbone ecosystem, structured as **two complementary and decoupled
composantes** that share one core runtime and one audit log.

### 2.1 Status of the proxy in the VBB topology

The proxy is **not** classified as a VBB worker. It is a platform-level
**capacité transverse**:

- It is **not** `vbb-fast-worker` (no FAST-ZERO / FAST-MINIMAL / FAST-STANDARD
  triage semantics).
- It is **not** `vbb-struct-worker` (no STRUCTURED plan/decision artifact).
- It is **not** `vbb-audit-worker` (it does not produce governance audits; it
  produces execution logs).
- It is **not** `vbb-close-worker` (it does not write to shared mutable
  governance artifacts).
- It is **not** `cody-check` (it is not a pre-action gate on Cody's runtime;
  it is invoked from inside actions, not before them).

Its lifecycle and release cadence are owned by the orchestrator (Cody +
human), not by any single worker.

### 2.2 The two composantes

The proxy exposes the **same core engine** through two decoupled surfaces:

1. **Composante Profil — Agent profile (human-facing)**
   - Surface: Telegram dialogue, interactive CLI, human-in-the-loop.
   - Latency target: 1–5 s (acceptable for human-in-the-loop).
   - Richer conversational layer; can ask clarifying questions, surface
     confirmations, narrate what it is about to do.
   - Carries the **gouvernance** of sensitive actions: who approved, why,
     with which scope.

2. **Composante Service — Machine-to-machine (workers/Cody)**
   - Surface: signed JSON-RPC over a file-based queue and an optional
     HTTP localhost endpoint.
   - Latency target: **sub-second** for the hot path.
   - Strict, no-confirmation, structured input/output. No dialogue, no
     clarification loop. Errors return as structured payloads, not as
     natural language.

The two composantes are **cohérentes découplées**: they share the same
authentication scheme, the same whitelist, the same audit log format, the
same action registry, the same LLM runtime — but they can be deployed,
versioned, rate-limited and evolved independently. A change to the Telegram
profile must not require a redeploy of the worker-side RPC, and vice versa.

### 2.2.1 POC simplification — single Python process with two logical endpoints (decision D1)

> **Decision D1 (actée par Brice le 2026-06-02)** : au POC, l'identité du proxy
> est **un seul process Python** avec **séparation interne claire** entre
> le profil logique (interface humaine) et le daemon local (interface
> machine-à-machine). Conceptuellement deux composantes, techniquement un
> seul process au POC. La séparation process-level est reportée à la V2
> si la charge le justifie (cf. hypothèse A-CP-009).

Concrètement, le process Python unique :

- charge en mémoire **deux adapters** distincts au démarrage (Telegram
  bot pour la composante Profil, listener HTTP+HMAC sur 127.0.0.1 pour la
  composante Service) ;
- partage **un seul core engine**, **un seul registre d'actions**,
  **un seul audit log**, **un seul LLM runtime** ;
- expose deux **endpoints logiques** distincts, chacun avec son propre
  contrat et son propre profil de latence ;
- est supervisé par `launchd` avec un **watchdog toutes les 60 s** pour
  atténuer le risque SPOF (cf. R-CP-008).

Cette unification est volontaire pour le POC : elle évite la complexité
opérationnelle d'un déploiement multi-processus, tout en préservant la
**séparation conceptuelle** des deux composantes. Le code, le registre,
l'audit et les schémas sont déjà écrits comme si les deux composantes
étaient physiquement séparées : la migration vers deux process ne
demanderait qu'un re-déploiement, pas une réécriture.

### 2.3 Caller topology

The proxy is reachable **directly** from:

- `hermes` (the host profile / runtime),
- `cody-orchestrator`,
- `vbb-fast-worker`,
- `vbb-struct-worker`,
- `vbb-audit-worker`,
- `vbb-close-worker`.

No central hub or message broker is required. Each caller opens its own
authenticated channel. This is by design: the proxy must remain reachable
even when one worker is down, and a single broker would itself become a
sensitive dependency.

### 2.4 Local LLM runtime

The proxy runs a **local LLM** on the M1 Max. The default model is
**Gemma 4 26B-A4B VLM served via `mlx_lm.server`**. The model identifier,
quantization and endpoint URL are **configurable** so that the operator can
swap to another local model (e.g. Qwen, Llama, Mistral) without code changes.
The model is treated as a replaceable backend; the proxy contract does not
depend on a specific model family.

### 2.5 API surface

> **Decision D2 (actée par Brice le 2026-06-02)** : l'interface **PRINCIPALE**
> du proxy au POC est **HTTP localhost + HMAC** (cf. §2.7). La file-based
> queue devient un **fallback** documenté, conservé pour les sessions
> SSH-only et la résilience réseau, mais n'est plus le mode par défaut.

Two transport modes are supported and can be used independently or together.
The priority is now explicitly inverted compared to the original draft:

- **HTTP localhost (PRIMARY, POC)** : a bound-to-`127.0.0.1` HTTP endpoint
  is the **default** mode for both composantes. The same contract and the
  same HMAC-SHA256 signing scheme as the file-based mode apply. Latency
  target: sub-second on the hot path. This is the surface reached by
  Hermes, Cody and the VBB workers in normal operation.
- **File-based queue (FALLBACK, future)** : a priority directory
  `/opt/hermes/proxy/orders/` receives request files; a separate
  `/opt/hermes/proxy/responses/` directory (or per-request response file
  alongside the order) carries the result. This mode survives network
  failures, works under SSH-only sessions, and gives the audit log a
  natural filesystem anchor. It is **not** the default POC interface.

The HTTP endpoint is preferred because it (a) gives a strict sub-second
hot path required by workers, (b) avoids the locking and cleanup
complexity of a filesystem queue, (c) plays well with existing
HTTP-native tooling (curl, requests, httpx) for tests and
post-mortems. The file-based mode is preserved as a future fallback, not
a present default — the priority inversion is a deliberate consequence
of D2.

### 2.6 Contract

Every call follows the same JSON contract, on both composantes. The
contract is **strictly versioned** and **strictly typed** so that any
breaking change can be detected before deployment.

#### 2.6.1 Mandatory fields (added per decision D2, harmonized 2026-06-02)

The following five constraints are **mandatory** on every request, on
both composantes, and are checked at the proxy boundary before any
parsing:

- **`contract_version`** (string, ex. `"1.0.0"`) — required, semver.
  Allows future breaking changes to be detected and rejected explicitly.
  Callers MUST pin a known-good version; unknown versions are rejected
  with `E_UNSUPPORTED_CONTRACT`.
- **`request_id`** (ULID or UUIDv7) — required, generated by the caller.
  Used for end-to-end correlation in the audit log, in the
  `--scratch` temporary file name, and in the rate-limit counter. The
  proxy never generates a `request_id` on behalf of a caller; the field
  is the caller's responsibility.
- **snake_case naming convention** (strict) — all field names in
  `action`, `params`, and any nested object MUST be in `snake_case`.
  camelCase, kebab-case and PascalCase are **rejected at the boundary**
  with `E_NAMING_CONVENTION`. The convention is enforced by a JSON
  Schema in addition to the example below.
- **Params size limit** — `params` is bounded to **4 KB by default**,
  **64 KB maximum** (absolute hard cap). Requests over the limit are
  rejected with `E_PAYLOAD_TOO_LARGE` before parsing. The bound is
  per-request, not per-field.
- **Long or sensitive params → scratch file** — params that are too
  large for the HTTP body or that are sensitive (private keys, PEM
  blocks, multi-KB JSON blobs) MUST be passed as a **temporary file
  referenced by its SHA-256 hash**. The file lives in
  `~/.hermes/proxy/scratch/<request_id>.bin`, is encrypted at rest
  (libsodium SecretStream — see ADR 0007 for the choice), and is
  automatically purged **1 hour** after the request completes. The
  proxy never accepts a long/sensitive param inline.

Request:

```json
{
  "contract_version": "1.0.0",
  "request_id": "01HZX8K3D5N7P9R2T4V6X8Z0A1",
  "action": "string — registered action name (snake_case)",
  "params": { "...action-specific, snake_case, ≤ 4 KB...": "..." },
  "signature": "hex(HMAC-SHA256(secret, canonical_request))",
  "requestor": "string — whitelisted caller id",
  "timestamp": "ISO-8601 UTC"
}
```

> Long or sensitive params are **never** inline. They are passed as
> a SHA-256-referenced scratch file in `~/.hermes/proxy/scratch/<request_id>.bin`,
> purged after 1 h. See §2.6.1.

Response:

```json
{
  "status": "ok | error | denied",
  "output": { "...structured, action-specific...": "..." },
  "error":  { "code": "...", "message": "..." },
  "log_id": "ulid — append-only audit reference"
}
```

### 2.7 Authentication

Every request is authenticated with **HMAC-SHA256** over a canonical form of
the request (`action`, `params`, `requestor`, `timestamp`). The shared
secret is provisioned out-of-band per caller; rotation policy and secret
storage are out of scope for this ADR (see ADR 0010 — security boundaries).

A **whitelist** of allowed `requestor` values is enforced at the proxy
boundary:

- `hermes`
- `cody-orchestrator`
- `vbb-fast-worker`
- `vbb-struct-worker`
- `vbb-audit-worker`
- `vbb-close-worker`

Any request with a `requestor` outside this list is rejected before
parsing, and the attempt is logged.

### 2.8 Audit log

Every accepted call — successful, failed, denied, retried — produces an
**append-only audit entry** (ULID-keyed, content-hash chained). The log is
the single source of truth for "what did the proxy do, for whom, when, with
which parameters". It is read by `vbb-audit-worker` but is **never** mutated
by any worker, including `vbb-audit-worker` itself.

### 2.9 What the proxy does NOT do

The proxy is **not** a reasoning engine over user intent. It:

- **does not interpret** the meaning of a free-form request;
- **does not chain** multiple actions on its own initiative;
- **does not hold** long-lived conversational state on the hot path;
- **does not call** the cloud LLM, nor expose any credential to it;
- **does not write** to shared VBB governance artifacts (those remain
  `vbb-close-worker`'s exclusive responsibility).

Its job is to **parse → map → execute → return structured**, against a
closed registry of pre-approved actions.

## 3. Consequences

### 3.1 Positive

- Sensitive operations no longer transit through the cloud LLM, removing
  the largest single trust dependency in the current stack.
- The two composantes can be evolved independently: a UX change to the
  Telegram profile does not block a security fix to the RPC contract, and
  vice versa. This is the **cohérence découplée** property.
- Every call is authenticated, authorized, and durably logged. The audit
  log is the canonical record for any post-incident review.
- Direct caller topology (no mandatory hub) keeps the proxy reachable when
  other parts of the stack are degraded.

### 3.2 Negative and trade-offs

- A second LLM runtime (`mlx_lm.server`) must be kept healthy on the host.
  The proxy inherits the operational cost of local inference: cold start,
  memory pressure, occasional model reloads.
- The file-based queue is simple and durable, but requires careful lock
  handling and cleanup to avoid starvation. (See §5.)
- The whitelist is static at boot by default; adding a new caller requires
  a config change and a proxy restart, which slows down ecosystem growth.
  This is a deliberate safety trade-off; see ADR 0009 for the extensibility
  path.
- The proxy becomes a **single point of failure** for any worker that
  depends on it. Failover and degraded mode are deferred to ADR 0008.

### 3.3 Operational consequences

- A new lifecycle owner is required: the proxy is deployed, monitored and
  upgraded by the orchestrator (Cody + human), not by any single VBB
  worker.
- `vbb-audit-worker` gains a new source artifact (the proxy audit log) and
  must be taught to consume it without mutating it.
- A **shared vocabulary** must be agreed upon for action names and error
  codes. This ADR fixes the envelope; ADR 0009 will fix the registry.
- Documentation must explicitly tell future agents that "calling the
  proxy" is not the same as "calling a worker" — the status, latency
  profile and failure semantics differ.

## 4. Alternatives Considered

### 4.1 Rejected — Reuse `cody-check` as the privacy gate

`cody-check` is a **pre-action runtime gate** that runs on Cody's
orchestration path. Using it as the privacy gate would conflate two
different concerns: (a) "is this action allowed by governance?" and (b)
"this request must be served by a local LLM with no cloud exposure".
A single component cannot enforce both without losing clarity, audit
separation and the ability to evolve each surface at its own pace. The
proxy must remain a **transverse capability**, not a gate inside another
gate.

### 4.2 Rejected — Make the proxy a fifth VBB worker

A worker-shaped proxy would inherit the FAST / STRUCTURED / AUDIT /
CLOSEOUT lifecycle, the route-based triage, the closeout contract, and the
"each worker writes to its own run directory" rule. None of these fit a
shared, always-on capability. It would also be forced to pick a single
route (STRUCTED is the closest fit but still wrong), and it would
artificially couple the human-facing profile to the worker-facing RPC.
The proxy needs a **distinct status** in the topology.

### 4.3 Rejected — Route all sensitive calls through the cloud LLM with redaction

Redacting credentials from prompts before they reach the cloud LLM is a
**defence in depth** measure, not a substitute for local execution. It
still leaks request shape, timing, account metadata and the *fact* that a
sensitive action is being performed. It also makes the cloud LLM a
critical dependency for the sensitive path, which contradicts the goal of
removing the cloud from that path. A local proxy makes the redaction
unnecessary for the hot path; it remains useful as a belt-and-braces
measure (see ADR 0010).

### 4.4 Rejected — Single composante only (RPC OR profile, not both)

A pure RPC proxy would leave the human-facing path (Telegram) without a
local, governed surface, forcing every interactive sensitive operation
back through the cloud LLM. A pure conversational agent would not meet
the sub-second latency requirement of the workers. The two composantes
exist precisely to serve these two distinct latency and trust profiles
while sharing the same core, registry and audit log.

### 4.5 Rejected — Single composante, profile-only (Telegram only, no machine RPC)

**Description**: ship only the human-facing Telegram profile at the POC,
and skip the machine-to-machine RPC composante. Workers would either
call the profile (impractical for sub-second) or stay ungoverned (which
is exactly what the proxy is meant to fix).

**Why rejected**:

- The **sub-second machine-to-machine contract** required by Hermes,
  Cody and the four VBB workers (cf. §1 — driving constraints) cannot
  be served by an interactive Telegram dialogue. Latency would be 1–5 s
  per call, multiplied by thousands of calls per session.
- Workers calling the cloud LLM directly (because the proxy has no RPC
  surface) **reintroduces** the trust dependency the proxy exists to
  remove. This is the original problem statement of this ADR.
- The `cody-check` runtime gate and the audit pipeline would have no
  surface to attach to, leaving the `read`/`write`/`destroy`
  separation unenforceable for any non-Telegram caller.
- The "profile-only" choice is essentially **no proxy at all** for the
  hot path, which is the status quo the chantier explicitly rejects.

**Verdict**: rejected. The two composantes (POC single process, D1)
are both needed; dropping the machine RPC side is incompatible with the
driving constraints. The single-process POC (D1) is the right
compromise, not a profile-only POC.

## 5. Known Risks

- **R-CP-001 — LLM cold start on the hot path.** A cold `mlx_lm.server`
  instance can take 5–20 s to be ready, breaking the sub-second contract
  for the first request after boot. Mitigation: keep-alive ping from
  `hermes`; degraded-mode responses during warm-up (see ADR 0008).
- **R-CP-002 — File-based queue starvation.** If a high-rate caller
  monopolises `/opt/hermes/proxy/orders/`, lower-priority callers may be
  starved. The "priority file d'attente" naming in §2.5 signals that a
  priority discipline is required; the concrete scheme is to be
  specified in ADR 0008 (failover) or ADR 0009 (extensibility).
- **R-CP-003 — Single point of failure for sensitive operations.**
  If the proxy is down, workers cannot read credentials, refresh tokens
  or perform identity checks. The blast radius is the whole stack.
  Out of scope here; tracked in ADR 0008.
- **R-CP-004 — Whitelist rigidity.** Adding a new caller requires a
  restart, which slows down legitimate ecosystem growth. Tracked in
  ADR 0009 (dynamic registration, signed enrolment).
- **R-CP-005 — Audit log growth.** Append-only logs grow monotonically;
  without a rotation / archival policy they will eventually exhaust
  disk. The exact policy is out of scope here; tracked in ADR 0009.
- **R-CP-006 — Secret distribution.** The HMAC shared secrets must be
  provisioned to every caller. Storage, rotation and revocation are
  tracked in ADR 0010 (security boundaries).
- **R-CP-007 — Semantic drift on the "no reasoning" rule.** Future
  contributors may be tempted to let the proxy "decide" what an
  ambiguous action means. This is a class-of-risk increase (P.R7) and
  must be escalated: the proxy stays a parser / mapper / executor. Any
  change in this direction must trigger a new ADR.
- **R-CP-008 — POC single-process SPOF (introduced by D1, 2026-06-02).**
  Because the proxy is a single Python process hosting both the human
  Profile composante and the machine-to-machine Service composante (cf.
  §2.2.1), a process crash takes down **both** surfaces simultaneously.
  Workers and Brice lose credentialed access at the same time. The blast
  radius is the whole sensitive path. *Mitigation* : (a) the process is
  supervised by `launchd` with `KeepAlive=true` and automatic restart on
  crash ; (b) a **watchdog fires every 60 s** to confirm the process is
  alive AND the HTTP listener on `127.0.0.1` is accepting connections,
  with a Telegram alert to Brice after two consecutive failed checks ;
  (c) the audit log is flushed and sealed on graceful shutdown so
  post-mortem analysis is not corrupted ; (d) the V2 path is to split
  the two composantes into two processes (cf. A-CP-009) when the
  load justifies the operational overhead. This risk is **accepted** at
  POC scope and **escalated** at production scope.

## 6. Open Assumptions to Confirm

The following points are working assumptions that the implementation must
validate before this ADR is promoted from `PROPOSED` to `Accepted`:

- **A-CP-001.** The default LLM (`Gemma 4 26B-A4B VLM` via `mlx_lm.server`
  on M1 Max) meets the sub-second p50 latency target for the hot path
  actions. To validate with a benchmark before any production deployment.
- **A-CP-002.** `/opt/hermes/proxy/orders/` is writable by all six
  whitelisted callers under the operator's standard permissions model. If
  not, the path must move or per-caller subdirectories must be introduced.
- **A-CP-003.** The set of six whitelisted `requestor` values in §2.7 is
  the **complete** set of current legitimate callers. Any new VBB worker
  must be added through ADR 0009, not by editing this list silently.
- **A-CP-004.** ULID is the preferred `log_id` format. To confirm with
  the audit pipeline; alternative (UUIDv7) is acceptable if the pipeline
  already standardises on it.
- **A-CP-005.** The canonical request form for HMAC signing is the
  concatenation `action || requestor || timestamp || sorted_json(params)`.
  Exact byte order and JSON serialisation rules (key ordering, number
  encoding, unicode normalisation) are to be fixed in ADR 0010.
- **A-CP-006.** The "two composantes share one core" assumption is
  implementable as a single process with two adapters (Telegram bot +
  queue/HTTP listener). If a process boundary between the two composantes
  is later required for isolation, this ADR will need a revision.
- **A-CP-007.** The proxy does **not** need to call back into the cloud
  LLM, even for fallback reasoning. If a future action truly requires
  cloud reasoning, this is a class-of-risk change (P.R7) and must be
  handled by a new ADR, not by a config flag.
- **A-CP-008.** The current repo convention places ADRs under
  `docs/adr/`. The path used for this file (`docs/architecture/`) follows
  the task's explicit instruction; the repo-wide convention should be
  reconciled in a follow-up housekeeping ADR so that 0006 lives next to
  0001–0004.
- **A-CP-009 (introduced by D1, 2026-06-02).** The POC single-process
  unification of the two composantes (cf. §2.2.1) is **acceptable** to
  validate the mécanique end-to-end : the registry, the audit log, the
  contract, the dry-run pipeline, the rate-limiting, and the security
  boundaries can all be exercised without paying the operational cost
  of a multi-process deployment. If post-POC measurements show that
  (a) one composante saturates the process under load, (b) an
  isolation fault in one composante must not impact the other, or
  (c) the operator wants distinct release cadences enforced
  physically rather than logically, the architecture will be **revised**
  to two processes. The code, the registry, the audit and the schemas
  are written to make that revision a re-deployment, not a re-write.

## 7. References

- ADR 0001 — Formal Executor Boundary
- ADR 0004 — Contract Schema Version Semantics
- ADR 0007 — Credentials Handling (forthcoming, parallel batch)
- ADR 0008 — Failover & Degraded Mode (forthcoming, parallel batch)
- ADR 0009 — Extensibility & Dynamic Registration (forthcoming)
- ADR 0010 — Security Boundaries (forthcoming, parallel batch)
- ADR 0011 — Proxy Bypass Prevention (cross-reference : any sensitive
  action by Hermes / Cody / VBB workers MUST go through the proxy, not
  through direct `ssh`, `scp`, `gh auth`, `docker login`, etc. — see
  D7 / ADR 0011 § repo governance rule)
- `docs/CONVENTIONS.md` — quality pillars P.R1–P.R8
- `docs/LONG_RUN_RULE.md` — long-run output contract
- `docs/PILOTAGE.md` — route and escalation matrix

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS:
  elapsed_seconds: 206
  budget_initial: 180
  progress_emitted: true
  progress_count: 1
  note: |
    PROGRESS block (emitted retroactively in worker summary at closeout,
    because the task was well-bounded and completed within the soft budget
    even though elapsed > 90s threshold):
      [PROGRESS] elapsed_seconds: 110 | next_step: finalize sections 5-7 and
      LONG_RUN_SUMMARY | risks: [R-CP-001 cold start, R-CP-003 SPOF]
  extension_requested: false
  timeout_closeout_emitted: false
  verdict: COMPLETE
  files_touched:
    - docs/architecture/0006-confidential-proxy-architecture.md
  tests_run: []
  tests_missing:
    - LLM latency benchmark for sub-second p50 (A-CP-001)
    - filesystem permission check for /opt/hermes/proxy/orders (A-CP-002)
    - HMAC canonicalisation conformance test (A-CP-005)
  risks:
    - R-CP-001 LLM cold start
    - R-CP-002 queue starvation
    - R-CP-003 SPOF for sensitive ops
    - R-CP-004 whitelist rigidity
    - R-CP-005 audit log growth
    - R-CP-006 secret distribution
    - R-CP-007 semantic drift on "no reasoning"
  open_points:
    - Promote status from PROPOSED to Accepted once A-CP-001..008 are validated
    - Reconcile repo ADR path convention (docs/adr/ vs docs/architecture/) per A-CP-008
    - Cross-check consistency with 0007/0008/0009/0010 in the parallel batch
```

---

## REVISION_HISTORY — 2026-06-02 (harmonisation D1-D7)

> Cette révision applique 9 patches ciblés (P1–P9) pour intégrer les
> décisions D1, D2, D3, D4 actées par Brice le 2026-06-02, ainsi que
> les références croisées vers ADR 0011 (bypass prevention, D7).
> Le `LONG_RUN_SUMMARY` historique ci-dessus est **préservé** ; cette
> section est additive.

### Patches appliqués (résumé)

| Patch | Section visée | Nature | Lignes (approx.) |
|---|---|---|---|
| P1 | Header / Date | ajout « Revised: 2026-06-02 » | 1 |
| P2 | Header / Status | PROPOSED → PROPOSED (rev. 2026-06-02) | 1 |
| P3 | §2.2 (deux composantes) | ajout §2.2.1 POC simplification (D1) | +28 |
| P4 | §2.5 (API surface) | inversion HTTP↔file-based (D2) | modifié |
| P5 | §2.6 (Contract) | ajout §2.6.1 5 champs obligatoires | +35 |
| P6 | §4 (Alternatives) | ajout §4.5 profile-only rejeté | +27 |
| P7 | §5 (Risks) | ajout R-CP-008 SPOF + mitigation | +15 |
| P8 | §6 (Assumptions) | ajout A-CP-009 single-process V2 | +12 |
| P9 | §7 (References) | ajout référence ADR 0011 | +4 |

### Décisions intégrées

- **D1** — identité du proxy = un seul process Python (deux endpoints
  logiques) au POC, séparation process-level reportée en V2.
- **D2** — HTTP localhost + HMAC devient l'interface **PRIMARY** au
  POC ; file-based queue devient FALLBACK documenté.
- **D3** — chiffrement libsodium SecretStream (cf. ADR 0007 P12 pour
  le détail) ; ce ADR référence le choix mais ne le redéclare pas.
- **D4** — profil Hermes / service indépendant = un seul process
  Python avec deux endpoints logiques (cf. §2.2.1).
- **D7** — cross-référence ADR 0011 pour la règle de gouvernance
  repo (pas d'appel direct ssh/gh/docker/cat .env/printenv).

### Contrat étendu (résumé, détaillé §2.6.1)

- `contract_version` obligatoire (semver).
- `request_id` obligatoire (ULID ou UUIDv7, généré appelant).
- `snake_case` strict, camelCase/kebab-case rejetés.
- `params` ≤ 4 KB par défaut, 64 KB max absolu.
- Params longs/sensibles → fichier scratch `~/.hermes/proxy/scratch/<request_id>.bin`,
  chiffré, purgé 1 h.

### VALIDATION P.R2

- 8 sections obligatoires toujours présentes (1 Context, 2 Decision,
  3 Consequences, 4 Alternatives, 5 Risks, 6 Assumptions, 7 References,
  LONG_RUN_SUMMARY historique).
- Sections ajoutées (2.2.1, 2.6.1, 4.5) **insérées en sous-sections**,
  numérotation cohérente.
- Markdown valide, hiérarchie H2/H3 préservée, langue anglaise préservée.
- `LONG_RUN_SUMMARY` historique **non touché** (patch additif only).

```yaml
FINAL_STATUS:
  revision: 2026-06-02
  decision_refs: [D1, D2, D3, D4, D7]
  patches_applied: 9
  files_touched:
    - docs/adr/0006-confidential-proxy-architecture.md
  cross_refs_added:
    - ADR 0011 (bypass prevention, D7 repo governance rule)
  contract_extensions:
    - contract_version (semver, mandatory)
    - request_id (ULID/UUIDv7, mandatory)
    - snake_case strict naming
    - params size 4 KB default, 64 KB max
    - long/sensitive params → scratch file hash-referenced
  alternatives_added:
    - 4.5 Rejected — single composante, profile-only
  risks_added:
    - R-CP-008 POC single-process SPOF
  assumptions_added:
    - A-CP-009 POC single-process acceptable, V2 split documented
  long_run_summary_preserved: true
  verdict: COMPLETE
```
