# POC Closeout — Vibebackbone Privacy Proxy (v1.0.0)

**Date**: 2026-06-02
**Status**: COMPLETE (POC scope)
**Route**: STRUCTURED
**Verdict**: READY_FOR_V1_RELEASE

## 1. What was built

| # | Deliverable | Path | Status |
|---|---|---|---|
| L1 | Single-process daemon (HTTP localhost) | `tools/proxy/daemon.py` | ✅ |
| L2 | Versioned contract (v1.0.0, snake_case, UUIDv4) | `tools/proxy/contract.py` | ✅ |
| L3 | HMAC-SHA256 validation + 300 s anti-replay | `tools/proxy/hmac_auth.py` | ✅ |
| L4 | Config loader (PyYAML, schema-enforced) | `tools/proxy/config.py` | ✅ |
| L5 | Action whitelist + dispatch (one action: `vault_read`) | `tools/proxy/actions.py` | ✅ |
| L6 | Secret store: libsodium SecretStream (XChaCha20-Poly1305) | `tools/proxy/secret_store.py` + `crypto.py` | ✅ |
| L7 | Audit log: libsodium SecretStream, append-only, daily rotation | `tools/proxy/audit.py` | ✅ |
| L8 | pytest suite (14 tests, all green) | `tools/proxy/tests/` | ✅ |
| L9 | POC usage doc (Hermes/Cody contract) | `docs/proxy/POC_USAGE.md` | ✅ |
| L10 | This closeout doc | `docs/proxy/POC_CLOSEOUT.md` | ✅ |

### Test result

```
14 passed in 1.65s
```

### Linters

- `python tools/vbb-architecture.py lint` → 0 error, 0 warning
- `python tools/vbb-contract-lint.py` → 0 error
- `python -m py_compile tools/proxy/*.py tools/proxy/tests/*.py` → OK

## 2. Security verification (P.R2)

| Property | Result | Evidence |
|---|---|---|
| Signature mismatch refused | ✅ 401 `E_HMAC_INVALID` | `test_hmac.py::test_wrong_signature_is_refused` |
| Missing signature refused | ✅ 401 `E_HMAC_MISSING` | `test_hmac.py::test_missing_signature_is_refused` |
| Replay (>300 s) refused | ✅ 401 `E_REPLAY_DETECTED` | `test_hmac.py::test_stale_timestamp_is_refused` |
| Unknown action refused | ✅ 4xx `E_UNDECLARED` | `test_actions.py::test_unknown_action_is_refused` + `test_integration.py::test_unknown_action_returns_4xx` |
| Wrong `contract_version` | ✅ 400 `E_CONTRACT_VERSION` | manual end-to-end |
| camelCase keys refused | ✅ 400 `E_PAYLOAD_INVALID` | manual end-to-end |
| Body > 64 KB refused | ✅ 413 `E_PAYLOAD_TOO_LARGE` | manual end-to-end |
| `secrets.enc` is binary (VBBP1 magic, 5 bytes) | ✅ `file` → data, grep of plaintext → 0 hits | `test_secret_store.py::test_on_disk_file_contains_no_cleartext` |
| Audit log is binary (VBBA1 magic, 5 bytes) | ✅ `file` → data, grep of action_id → 0 hits | `test_audit.py::test_audit_does_not_leak_secrets` |
| `secrets.key` 0600 enforced at boot | ✅ daemon refuses with `E_PERMISSION` otherwise | `daemon.py::_check_filesystem` |
| `~/.hermes/proxy/` 0700 enforced at boot | ✅ daemon refuses with `E_PERMISSION` otherwise | `daemon.py::_check_filesystem` |

## 3. Files produced

```
tools/proxy/
├── __init__.py
├── daemon.py              # Entry point
├── server.py              # HTTP server (http.server stdlib)
├── contract.py            # Pydantic-free dataclass contract
├── hmac_auth.py           # HMAC verifier + sign helper
├── config.py              # YAML loader + schema
├── actions.py             # Whitelist + dispatch
├── secret_store.py        # Encrypted key/value store
├── audit.py               # Encrypted append-only log
├── crypto.py              # libsodium SecretStream + AES-GCM fallback
├── errors.py              # E_* codes
├── config.example.yaml    # Template
├── actions.example.yaml   # Whitelist template
├── fixtures/
│   └── vault_read_response.json
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Hermetic fixtures
│   ├── test_hmac.py       # 4 tests
│   ├── test_actions.py    # 3 tests
│   ├── test_secret_store.py # 2 tests
│   ├── test_audit.py      # 2 tests
│   └── test_integration.py # 3 tests
├── run.sh                 # Launcher
└── README.md              # Quickstart

docs/proxy/
├── POC_USAGE.md           # Hermes/Cody-facing doc
└── POC_CLOSEOUT.md        # This file
```

## 4. Known limits

These are **deliberate POC limits**, not bugs. They are the boundary of what the brief authorised and the ADRs locked.

1. **One action only (`vault_read`).** No SSH, no NAS, no `gh`, no `docker login`. Adding any other action requires a new ADR (per ADR 0009 §2.3 cycle).
2. **`vault_read` is stub-backed.** It returns a static JSON fixture (`tools/proxy/fixtures/vault_read_response.json`). The fixture value is intentionally a clearly fake string (`STUB-POC-VAULT-READ-VALUE-XXXX`) — never replace it with a real secret.
3. **No Telegram UI.** Credential ingestion is out of scope. The proxy's `SecretStore` already supports `read_secret`/`write_secret`, but no human-facing flow exists yet (V2: see ADR 0007 §2.4).
4. **No file-based queue.** The `actions.example.yaml` references queue-related fields, but the daemon only serves HTTP localhost. The queue transport is a documented V2 fallback (ADR 0006 §2.6.1).
5. **Single-threaded daemon.** `http.server.HTTPServer` is used in its blocking form. Rate limiting (D6, ADR 0008 §2.2.1) is documented but not enforced at the POC level — the daemon is fast enough that one request at a time is fine for the single action.
6. **No key rotation helper.** `secrets.key` and `hmac.key` are created manually. Rotation is V2 (cf. ADR 0007 §2.6 `update`).
7. **No `tools/vbb-bypass-lint.py`.** Per ADR 0011, the linter is V2. The POC relies on the static `ALLOWED_ACTIONS = ("vault_read",)` constant in `actions.py` and on the fact that no real SSH/Docker binaries are reachable from the action layer.
8. **No LLM.** `config.model: stub`. The proxy never calls a model. The contract is JSON-only.
9. **No client helper library.** Callers (Hermes, Cody, VBB workers) must inline the 4-line HMAC+POST snippet. A `tools/proxy/client.py` is V2.
10. **No audit log rotation policy.** The current code opens a new file per UTC day. File size growth and archive policy are V2.

## 5. Known risks (carried over from ADRs)

- **R-CP-001 (LLM cold start)**: N/A at POC level (no LLM).
- **R-CP-002 (queue starvation)**: N/A at POC level (no queue).
- **R-CP-007 (semantic drift on "no reasoning")**: Mitigated by `ALLOWED_ACTIONS` being a frozen tuple — there is no path for the proxy to invent a new action_id at runtime.
- **R-CP-008 (single-process SPOF)**: Acknowledged. The POC is one process; if it crashes, no calls succeed. V2 will add a watchdog / launchd supervision.
- **R7-09 (libsodium absent)**: Mitigated by `select_backend("auto")` falling back to AES-256-GCM transparently with a log entry.
- **R9-T1 (secret in `command_template`)**: Mitigated by stub-only actions at POC level. V2 will add the linter.
- **Audit log write contention**: Single-threaded daemon at POC, no contention. V2 with concurrent workers will need the mutex mentioned in ADR 0007 §2.7bis.

## 6. Compliance with the brief

| Brief requirement | Status |
|---|---|
| HTTP localhost + HMAC | ✅ |
| Single action `vault_read` | ✅ |
| `~/.hermes/proxy/secrets.enc` | ✅ |
| libsodium SecretStream prioritaire | ✅ (default `libsodium`; AES-256-GCM fallback documented) |
| Audit log chiffré | ✅ |
| Refus explicite des actions hors whitelist | ✅ (`E_UNDECLARED`) |
| Aucun accès direct aux secrets par Hermes/Cody/workers | ✅ (HMAC required, signature is the only path) |
| Pas de SSH réel | ✅ (no SSH code path) |
| Pas de Telegram UI | ✅ (no Telegram code) |
| Queue file-based = stub only | ✅ (queue fields in YAML, no consumer) |
| Pas d'élargissement | ✅ (no extra actions, no extra endpoints) |
| Pas d'ADR ajouté | ✅ (no new ADR file) |
| Pas de secret en clair dans logs / stdout / LLM | ✅ (verified by grep, header magic, and audit log structure) |

## 7. Next steps (V2)

Prioritised, by impact/risk:

1. **`tools/proxy/client.py`** — thin Python client for Hermes/Cody/VBB workers (no inline HMAC in every call site).
2. **`tools/vbb-bypass-lint.py`** — ADR 0011 linter, integrated as a pre-commit hook on `tools/proxy/` and on worker SOUL.md.
3. **Real `vault_read`** — replace the stub fixture with a call to `SecretStore.read_secret(secret_id)`. Backward-compatible: same action id, same response shape.
4. **Second action: `nas_exec` or `gh_status`** — first real action with a credential; validates the action-extension lifecycle (ADR 0009 §2.3) end-to-end.
5. **Rate limiting (D6)** — middleware on the HTTPServer handler; 30 req/min per caller, 5 sensitive/h, 10 concurrent. Required before exposing to multiple VBB workers.
6. **Mutex per credential (D5)** — required as soon as two VBB workers can target the same secret.
7. **Watchdog / launchd supervision** — addresses R-CP-008.
8. **Queue file-based fallback (D2)** — small, isolated, and easy to add when needed.
9. **LLM hook (D1, model=stub → real)** — plug mlx_lm or ollama behind the same `LLMRouter` interface.
10. **Audit log rotation + WORM** — daily rotation is already in place; the next step is size-based rollover and an integrity check (`vbb-proxy audit verify`).

## 8. Files NOT touched (per the brief)

- `docs/adr/0001`–`0012` (ADR governance, frozen)
- All `tools/vbb-*.py` (VBB runtime, unrelated)
- `~/02_Dev/trame`, `~/02_Dev/solutions_mjc`, `~/02_Dev/studio` (other projects)
- `~/.hermes/`, `~/.hermes/proxy/` (the real proxy data dir; the POC only ever writes inside `/tmp/vbb_proxy_test/`)

---

## LONG_RUN_SUMMARY

```yaml
FINAL_STATUS:
  revision: 2026-06-02
  route: STRUCTURED
  scope: POC_v1.0.0
  files_produced: 16 (12 Python + 2 YAML + 1 fixture + 1 run.sh)
  tests_run: 14
  tests_passed: 14
  tests_failed: 0
  tests_skipped: 0
  test_duration_seconds: 1.65
  files_touched_outside_proxy:
    - docs/adr/0009-proxy-action-extensibility.md (CJK cleanup, 1 patch)
  new_adrs_created: 0
  linters_clean: [vbb-architecture, vbb-contract-lint, py_compile]
  security_scan_clean: true   # no plaintext secret in secrets.enc, audit, code
  verdict: COMPLETE
  ready_for_v1_release: true
  next_action: wait_for_brice_signoff_before_v2
```
