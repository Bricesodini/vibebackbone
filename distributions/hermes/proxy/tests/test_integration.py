"""End-to-end HTTP tests.

These tests spin up a real HTTP server in a background thread, point
it at a temp config, and exercise the action endpoint over the loopback
interface. The server is shut down at the end of each test.

The chosen port is dynamically allocated to avoid conflicts. (A fixed
port would be fragile in CI.)
"""

from __future__ import annotations

import hashlib
import hmac as hmac_mod
import json
import socket
import threading
import time
import urllib.error
import urllib.request
import uuid
from http.server import HTTPServer
from pathlib import Path

import pytest

from tools.proxy.config import load_config
from tools.proxy.server import make_handler  # type: ignore[attr-definitions]


def _free_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _signed_call(url: str, key: bytes, payload: dict, *, bad_sig: bool = False, ts: int | None = None) -> tuple[int, dict]:
    body = json.dumps(payload, separators=(",", ":")).encode()
    sig = hmac_mod.new(key, body, hashlib.sha256).hexdigest()
    if bad_sig:
        sig = "0" * 64
    headers = {
        "Content-Type": "application/json",
        "X-Proxy-Signature": sig,
        "X-Proxy-Timestamp": str(ts or int(time.time())),
    }
    req = urllib.request.Request(url, data=body, headers=headers)
    try:
        r = urllib.request.urlopen(req, timeout=5)
        return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())


def _build_server_context(config_path: Path):
    """Build a ServerContext from a config file path.

    We do not import ServerContext to avoid an import cycle; the
    server module exposes ``make_handler(ctx)`` so we instantiate the
    bound handler and use ``cls``'s globals to reach the context.
    """
    from tools.proxy.config import load_actions as _load_actions
    from tools.proxy.crypto import select_backend
    from tools.proxy.hmac_auth import HmacVerifier
    from tools.proxy.actions import ActionDispatcher
    from tools.proxy.secret_store import SecretStore, load_or_create_key
    from tools.proxy.audit import AuditLog
    from tools.proxy import server as server_mod
    cfg = load_config(config_path)
    backend = select_backend(cfg.crypto.backend)
    hmac_key = cfg.hmac.key_path.read_bytes()
    verifier = HmacVerifier(key=hmac_key, timestamp_skew_seconds=cfg.hmac.timestamp_skew_seconds)
    actions = _load_actions(cfg.actions_path)
    fixtures_dir = cfg.fixtures.vault_read_response_path.parent
    dispatcher = ActionDispatcher(
        actions=actions,
        fixtures_dir=fixtures_dir,
        vault_read_response_path=cfg.fixtures.vault_read_response_path,
    )
    store = SecretStore(cfg.secrets.store_path, load_or_create_key(cfg.secrets.key_path), backend)
    audit = AuditLog(cfg.audit.dir, load_or_create_key(cfg.secrets.key_path), backend)
    return server_mod.ServerContext(  # type: ignore[attr-defined]
        config=cfg,
        hmac=verifier,
        actions=dispatcher,
        secret_store=store,
        audit=audit,
        backend=backend,
    )


@pytest.fixture
def live_server(proxy_workspace, hmac_key, config_path):
    port = _free_port()
    # Re-render the config with the free port.
    txt = config_path.read_text()
    txt = txt.replace("port: 9911", f"port: {port}")
    config_path.write_text(txt)

    ctx = _build_server_context(config_path)
    handler = make_handler(ctx)
    httpd = HTTPServer(("127.0.0.1", port), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    try:
        yield {"port": port, "key": hmac_key.read_bytes()}
    finally:
        httpd.shutdown()
        httpd.server_close()
        t.join(timeout=2)


def test_signed_vault_read_succeeds(live_server):
    payload = {
        "contract_version": "1.0.0",
        "request_id": str(uuid.uuid4()),
        "action_id": "vault_read",
        "params": {"secret_id": "fixture"},
        "requestor": "pytest",
    }
    code, body = _signed_call(
        f"http://127.0.0.1:{live_server['port']}/proxy/v1/exec",
        live_server["key"],
        payload,
    )
    assert code == 200, body
    assert body["status"] == "ok"
    assert body["action_id"] == "vault_read"
    assert body["result"]["stub"] is True


def test_invalid_hmac_returns_401(live_server):
    payload = {
        "contract_version": "1.0.0",
        "request_id": str(uuid.uuid4()),
        "action_id": "vault_read",
        "params": {"secret_id": "fixture"},
        "requestor": "pytest",
    }
    code, body = _signed_call(
        f"http://127.0.0.1:{live_server['port']}/proxy/v1/exec",
        live_server["key"],
        payload,
        bad_sig=True,
    )
    assert code == 401
    assert body["error"]["code"] == "E_HMAC_INVALID"


def test_unknown_action_returns_4xx(live_server):
    payload = {
        "contract_version": "1.0.0",
        "request_id": str(uuid.uuid4()),
        "action_id": "ssh_root",
        "params": {},
        "requestor": "pytest",
    }
    code, body = _signed_call(
        f"http://127.0.0.1:{live_server['port']}/proxy/v1/exec",
        live_server["key"],
        payload,
    )
    assert 400 <= code < 500
    assert "error" in body
