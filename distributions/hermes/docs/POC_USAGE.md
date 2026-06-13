# POC Usage — Vibebackbone Privacy Proxy (v1.0.0)

> **Scope** : single-process local daemon, one action (`vault_read`), HMAC over HTTP localhost. See [POC_CLOSEOUT.md](./POC_CLOSEOUT.md) for limits, risks, and V2 roadmap.

## 1. Overview

The proxy is a single Python process that binds to `127.0.0.1` and accepts a single HTTP endpoint:

```
POST /proxy/v1/exec
```

Every request must carry an HMAC-SHA256 signature over the raw body and a timestamp within ±300 seconds. The proxy validates the signature, parses the request against a strict versioned contract, dispatches the declared action if it is on the whitelist, logs an entry to an encrypted audit log, and returns a JSON response.

The POC only ships **one action**: `vault_read`. It is read-only, stub-backed, and never reads real secrets, never makes network calls, and never touches a remote system. It exists to validate the security boundaries (HMAC, contract, whitelist, encryption) before V2 adds real actions.

## 2. Install (one-time)

```bash
# From the vibebackbone repo root
python3 -m pip install --user pynacl pytest
```

`pynacl` provides the libsodium bindings used by the secret store and the audit log. The proxy has a fallback to `cryptography` (AES-256-GCM) — see [§7](#7-crypto-backends) — but the default is libsodium.

## 3. Configure

```bash
mkdir -p ~/.hermes/proxy/audit
chmod 700 ~/.hermes/proxy

cp distributions/hermes/proxy/config.example.yaml  ~/.hermes/proxy/config.yaml
cp distributions/hermes/proxy/actions.example.yaml ~/.hermes/proxy/actions.yaml

# Generate keys (the daemon refuses to start without them and with wrong perms)
python3 -c "
import os
os.urandom(32).tofile('/tmp/__hmac') if hasattr(os.urandom(32), 'tofile') else None
open('~/.hermes/proxy/hmac.key', 'wb').write(os.urandom(32))
from distributions.hermes.proxy.crypto import generate_key
open('~/.hermes/proxy/secrets.key', 'wb').write(generate_key())
" 2>/dev/null
python3 -c "
import os
open(os.path.expanduser('~/.hermes/proxy/hmac.key'), 'wb').write(os.urandom(32))
from distributions.hermes.proxy.crypto import generate_key
open(os.path.expanduser('~/.hermes/proxy/secrets.key'), 'wb').write(generate_key())
"
chmod 600 ~/.hermes/proxy/hmac.key ~/.hermes/proxy/secrets.key
```

`config.example.yaml` and `actions.example.yaml` are the canonical templates. The default `config.yaml` binds to `127.0.0.1:9911`, the default `actions.yaml` whitelists exactly one action: `vault_read`.

## 4. Run the daemon

```bash
./distributions/hermes/proxy/run.sh
# or, equivalently:
PYTHONPATH=. VBB_PROXY_CONFIG=$HOME/.hermes/proxy/config.yaml \
    python3 -m distributions.hermes.proxy.daemon
```

The daemon validates the filesystem permissions at boot and refuses to start if:

- `~/.hermes/proxy/` is not `0700`
- `~/.hermes/proxy/hmac.key` or `secrets.key` is not `0600`
- `secrets.enc` is not `0600` (once it exists)

## 5. Make a signed request

Below is a self-contained Python client. It mirrors what an internal caller (Hermes, Cody, or a VBB worker) is expected to do: build a JSON body, sign the raw bytes with HMAC-SHA256, send the headers, parse the response.

```python
import hashlib
import hmac
import json
import os
import time
import urllib.request

KEY = open(os.path.expanduser("~/.hermes/proxy/hmac.key"), "rb").read()

body_obj = {
    "contract_version": "1.0.0",
    "request_id": "00000000-0000-4000-8000-000000000001",
    "action_id": "vault_read",
    "params": {"secret_id": "fixture"},
    "requestor": "my-client",
}
body = json.dumps(body_obj, separators=(",", ":")).encode()
ts = str(int(time.time()))
sig = hmac.new(KEY, body, hashlib.sha256).hexdigest()

req = urllib.request.Request(
    "http://127.0.0.1:9911/proxy/v1/exec",
    data=body,
    headers={
        "Content-Type": "application/json",
        "X-Proxy-Signature": sig,
        "X-Proxy-Timestamp": ts,
        "X-Proxy-Request-Id": body_obj["request_id"],
    },
)
with urllib.request.urlopen(req, timeout=5) as r:
    print(r.status, r.read().decode())
```

### Headers

| Header | Required | Meaning |
|---|---|---|
| `Content-Type` | yes | `application/json` |
| `X-Proxy-Signature` | yes | hex HMAC-SHA256 of the raw body |
| `X-Proxy-Timestamp` | yes | Unix seconds (UTC) at signing time |
| `X-Proxy-Request-Id` | recommended | UUID echoed back in logs and response |

### Body contract (v1.0.0)

```json
{
  "contract_version": "1.0.0",
  "request_id": "00000000-0000-4000-8000-000000000001",
  "action_id": "vault_read",
  "params": { "secret_id": "fixture" },
  "requestor": "my-client"
}
```

| Field | Type | Notes |
|---|---|---|
| `contract_version` | string | Must be exactly `"1.0.0"`. Mismatch → `E_CONTRACT_VERSION`. |
| `request_id` | UUIDv4 string | Echoed back in the response. Mismatch/garbage → `E_PAYLOAD_INVALID`. |
| `action_id` | string | Must appear in the whitelist. Unknown → `E_UNDECLARED`. |
| `params` | object | Action-specific. Currently only `vault_read` is defined, with a required `secret_id` field. |
| `requestor` | string | Free-form human-readable identifier of the caller (logged). |

All top-level keys must be `snake_case`; `camelCase` or `kebab-case` → `E_PAYLOAD_INVALID`. Body size is capped at 64 KB (`E_PAYLOAD_TOO_LARGE`).

## 6. Response

### 200 OK — happy path

```json
{
  "contract_version": "1.0.0",
  "request_id": "00000000-0000-4000-8000-000000000001",
  "action_id": "vault_read",
  "status": "ok",
  "result": {
    "secret_id": "fixture",
    "stub": true,
    "value": "STUB-POC-VAULT-READ-VALUE-XXXX",
    "value_preview": "STUB***"
  }
}
```

### 4xx / 5xx — error

```json
{
  "contract_version": "1.0.0",
  "request_id": "00000000-0000-4000-8000-000000000001",
  "action_id": "<unknown>",
  "status": "error",
  "error": {
    "code": "E_HMAC_INVALID",
    "message": "HMAC signature mismatch"
  }
}
```

| Code | HTTP | Meaning |
|---|---|---|
| `E_HMAC_MISSING` | 401 | No `X-Proxy-Signature` header. |
| `E_HMAC_INVALID` | 401 | Signature does not match the body. |
| `E_REPLAY_DETECTED` | 401 | Timestamp outside the ±300 s window. |
| `E_TIMESTAMP_MISSING` / `E_TIMESTAMP_INVALID` | 401 | Header missing or unparseable. |
| `E_PAYLOAD_TOO_LARGE` | 413 | Body > 64 KB. |
| `E_CONTRACT_VERSION` | 400 | `contract_version` not `"1.0.0"`. |
| `E_PAYLOAD_INVALID` | 400 | snake_case violation, missing field, bad UUID, etc. |
| `E_UNDECLARED` | 400 | `action_id` is not on the whitelist. |
| `E_PERMISSION` | 500 | Boot-time filesystem permission check failed. |
| `E_BOOT_CONFIG` | 500 | Config file missing or malformed. |

## 7. Crypto backends

The proxy supports two backends, selected at boot via `crypto.backend` in `config.yaml`:

| Value | Meaning |
|---|---|
| `libsodium` (default) | XChaCha20-Poly1305 SecretStream via `pynacl`. AEAD, deterministic nonce derivation, re-keying support. |
| `cryptography` | AES-256-GCM via the `cryptography` package. Documented fallback (cf. ADR 0007 D3). |
| `auto` | Pick `libsodium` if available, otherwise `cryptography`. |

The actual backend used is logged at boot (`vbb.proxy.crypto :: backend=libsodium`).

## 8. Run the tests

```bash
python3 -m pytest distributions/hermes/proxy/tests/ -v
```

The test suite is hermetic — it builds its own config in a `tmp_path`, generates fresh keys, and spins up the HTTP server in a background thread on a random free port. There is no dependency on `~/.hermes/proxy/`.

## 9. For Hermes / Cody / VBB workers

The contract from a caller's perspective is:

1. Read the HMAC key from `~/.hermes/proxy/hmac.key` (or whatever path is set in the caller's config).
2. Build the JSON body per the v1.0.0 schema.
3. Sign the **raw bytes** of the body (not the parsed dict) with HMAC-SHA256.
4. POST to `http://127.0.0.1:9911/proxy/v1/exec` with the three headers.
5. Treat the response as JSON. If `status == "error"`, surface `error.code` to the user (do **not** log the message if it contains a hint about a credential).

The VBB workers (fast, struct, audit, close) should call this endpoint via a thin client helper (e.g. `distributions/hermes/proxy/client.py`, **V2**). At POC time there is no such helper yet — call sites are expected to inline the four lines above until V2.

## 10. V2 client & CLI (added 2026-06-02)

V2 ships an official Python client and a thin CLI wrapper so workers no longer have to inline the HMAC dance.

### 10.1 Using the official client

```python
import os
from distributions.hermes.proxy.client import ProxyClient

client = ProxyClient(
    base_url="http://127.0.0.1:9911",
    hmac_key=open(os.path.expanduser("~/.hermes/proxy/hmac.key"), "rb").read(),
    requestor="my-worker",
)
result = client.exec("vault_read", {"secret_id": "fixture"})
print(result["value_preview"])  # safe display field, never the raw value
```

The client is dependency-free (stdlib `urllib.request` only), never logs the body or the HMAC key, and raises a single `ProxyClientError` (with `code` + `message`) on every failure mode (`E_DAEMON_UNAVAILABLE`, `E_TIMEOUT`, `E_PROTOCOL`, or any server-side code echoed back).

### 10.2 Using the CLI

```bash
python -m tools.proxy.cli vault_read fixture
# or with explicit key path:
python -m tools.proxy.cli --hmac-key ~/.hermes/proxy/hmac.key vault_read fixture
```

The CLI prints `secret_id` and `value_preview` on stdout and exits non-zero on any error (the error code is written to stderr). It **never** prints the raw value.

### 10.3 Hermes / Cody integration example

```python
from distributions.hermes.proxy.client import ProxyClient
from distributions.hermes.proxy.errors import ProxyClientError

def vault_lookup(secret_id: str) -> str:
    client = ProxyClient("http://127.0.0.1:9911", hmac_key, requestor="hermes-worker")
    try:
        result = client.exec("vault_read", {"secret_id": secret_id})
        return result["value_preview"]  # safe to display / log
    except ProxyClientError as exc:
        # Surface only the code; the message may contain sensitive hints.
        return f"<unavailable: {exc.code}>"
```

> **WARNING — Never log or print the value of a secret.** The client and CLI return `secret_id` and `value_preview` for display, but the raw `value` should never appear in logs, stdout, or LLM prompts. This is a hard rule, not a convention: any code path that touches a secret value is a security boundary (see ADR 0010 and ADR 0011).

## 11. Out of scope (V2+)

The following are explicitly tracked for future versions:
- `tools/vbb-bypass-lint.py` (the linter is V2, see ADR 0011)
- Real SSH / NAS / GitHub / Docker actions
- Telegram UI for adding credentials interactively
- Queue file-based transport (file-based is a documented V2 fallback, not implemented in v1.0.0)
- LLM-backed intent parsing (the proxy never reads a body semantically)
- Multi-user concurrent access (mutex/fifo is in the contract but the daemon is single-threaded at the POC level)

## 12. Anti-bypass linter (V3, added 2026-06-02)

The Vibebackbone repo ships a dedicated linter that detects direct invocations
of sensitive binaries (per [ADR 0011 §3 Règle 1](../adr/0011-proxy-bypass-prevention.md)).
It is the **executable counterpart** of the textual rules in ADR 0011.

### Usage

```bash
# Default scan (report mode — exit 0 unless CRITICAL findings)
python tools/vbb-bypass-lint.py

# Strict mode for CI (exit non-zero on HIGH+CRITICAL)
python tools/vbb-bypass-lint.py --strict

# JSON output for tooling
python tools/vbb-bypass-lint.py --json
```

By default the linter scans `SOUL.md`, `tools/` (excluding the historical
`tools/proxy/` path retained in legacy docs), `prompts/`, `skills/`,
`scripts/`. `tools/proxy/` and `docs/adr/` are **always exempt** because they
contain the reference material the linter targets. The canonical runtime path
for the proxy cluster is `distributions/hermes/proxy/`; older reports may still
mention `tools/proxy/` for forensics. Use `--all` to scan the entire repo (will
surface doc-anchored "negative examples" as informational findings).

### Patterns detected

| Pattern | Severity | Example |
|---|---|---|
| `ssh user@host` (non-localhost) | CRITICAL | `ssh root@nas` |
| `gh auth` / `gh repo` / `gh secret` | CRITICAL | `gh auth login` |
| `docker login` / `docker push` | CRITICAL | `docker login -u admin` |
| `cat .env` / `printenv SECRET` | CRITICAL | `cat .env` |
| `aws configure` / `gcloud auth` / `az login` | CRITICAL | — |
| `vault read/write`, `pass show` | CRITICAL | — |
| `mysql/psql/redis-cli -p<pwd>` | HIGH | — |
| `kubectl config`, `helm secrets` | HIGH | — |
| `curl -H "Authorization: …"` | HIGH | — |
| `python -c "import os; os.environ[…]"` | HIGH | — |

### Integration with Hermes / Cody / VBB

The linter is meant to be wired into the VBB workers' pre-commit / CI loop
in V4. At V3 it ships as a **report-only** tool — the default exit code
is `0` even with `LOW` and `MEDIUM` findings, and only `CRITICAL`
findings force a non-zero exit. Use `--strict` in CI.

For full reference, see [`tools/vbb-bypass-lint/README.md`](../../tools/vbb-bypass-lint/README.md).

---

*See also: [ADR 0006](../adr/0006-confidential-proxy-architecture.md) — proxy architecture · [ADR 0011](../adr/0011-proxy-bypass-prevention.md) — bypass prevention · [POC_CLOSEOUT.md](./POC_CLOSEOUT.md) — limits, risks, next steps.*
