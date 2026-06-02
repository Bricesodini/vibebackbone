"""Pytest fixtures for the privacy proxy POC.

These fixtures produce a self-contained, hermetic test environment:
a temp directory with a complete ``config.yaml`` + ``actions.yaml``,
a freshly generated HMAC key, a freshly generated symmetric data key,
and a fixture for ``vault_read``.

No fixture ever writes to ``~/.hermes/proxy/`` directly. The daemon
must be pointed at the temp directory via the
``VBB_PROXY_CONFIG`` env var. The :func:`config_path` fixture does
exactly that and returns the path to the rendered config.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

# RUN 1 stabilization: the proxy code was migrated from
# tools/proxy/ to distributions/hermes/proxy/ (ADR 0013 Phase 3).
# The test files previously used the old import path. The cleanest
# fix is to expose the new location as a top-level ``proxy`` package
# on sys.path so test modules can do ``from proxy.X import Y``
# (avoids the ``distributions.hermes.proxy`` notation, which is
# awkward for paths with hyphens). See RUN 1 brief 2026-06-13.
_PROXY_PKG_PARENT = Path(__file__).resolve().parents[1]
if str(_PROXY_PKG_PARENT) not in sys.path:
    sys.path.insert(0, str(_PROXY_PKG_PARENT))

from proxy.crypto import generate_key, select_backend


@pytest.fixture
def proxy_workspace(tmp_path: Path) -> Path:
    """A hermetic, mode 0700 directory mimicking ``~/.hermes/proxy/``."""
    ws = tmp_path / "proxy"
    ws.mkdir(mode=0o700)
    (ws / "audit").mkdir(mode=0o700)
    return ws


@pytest.fixture
def hmac_key(proxy_workspace: Path) -> Path:
    """A 32-byte random HMAC key written with mode 0600."""
    p = proxy_workspace / "hmac.key"
    p.write_bytes(os.urandom(32))
    p.chmod(0o600)
    return p


@pytest.fixture
def secret_key(proxy_workspace: Path) -> Path:
    """A libsodium SecretStream key written with mode 0600."""
    p = proxy_workspace / "secrets.key"
    p.write_bytes(generate_key())
    p.chmod(0o600)
    return p


@pytest.fixture
def config_path(
    proxy_workspace: Path,
    hmac_key: Path,
    secret_key: Path,
    vault_read_fixture: Path,
) -> Path:
    """A complete, valid ``config.yaml`` pointing at the workspace.

    The proxy is configured to bind to ``127.0.0.1:0`` is not possible
    via YAML — the port is fixed to ``9911`` for E2E tests. Tests
    that need a free port should monkey-patch the loaded config
    *before* starting the server (see :func:`test_integration.py`).
    """
    cfg = proxy_workspace / "config.yaml"
    actions = proxy_workspace / "actions.yaml"
    actions.write_text(
        "actions:\n"
        "  - id: vault_read\n"
        "    description: stub\n"
        "    risk_level: low\n"
        "    mode: live\n"
        "    permissions: [read]\n"
        "    required_params: [secret_id]\n"
        "    stub: true\n",
        encoding="utf-8",
    )
    cfg.write_text(
        f"""host: 127.0.0.1
port: 9911
model: stub
log_level: WARNING
hmac:
  key_path: {hmac_key}
  timestamp_skew_seconds: 300
secrets:
  store_path: {proxy_workspace / "secrets.enc"}
  key_path: {secret_key}
audit:
  dir: {proxy_workspace / "audit"}
  file_prefix: audit-
  file_suffix: .log
actions_path: {actions}
fixtures:
  vault_read_response_path: {vault_read_fixture}
payload:
  max_bytes: 65536
  soft_bytes: 4096
crypto:
  backend: libsodium
""",
        encoding="utf-8",
    )
    cfg.chmod(0o600)
    return cfg


@pytest.fixture
def vault_read_fixture() -> Path:
    """Path to the canonical vault_read stub fixture (read-only)."""
    return Path(__file__).resolve().parents[1] / "fixtures" / "vault_read_response.json"


# ---------------------------------------------------------------------------
# Live HTTP server fixture
# ---------------------------------------------------------------------------
#
# Spin up a real HTTP server in a background thread, point it at a temp
# config, and yield ``{"port": int, "key": bytes}``. The chosen port is
# dynamically allocated to avoid conflicts in CI.
#
# The fixture is defined here (rather than in ``test_integration.py``)
# so any test module in the package can reuse it — the V2 client and
# CLI tests both need it.
#
# Implementation note: we re-import the server plumbing here to keep
# the fixture self-contained; the duplication with ``test_integration``
# is a one-time cost.

import socket as _socket
import threading as _threading
from http.server import HTTPServer as _HTTPServer

from proxy.actions import ActionDispatcher as _ActionDispatcher
from proxy.audit import AuditLog as _AuditLog
from proxy.config import load_actions as _load_actions
from proxy.config import load_config as _load_config
from proxy.crypto import select_backend as _select_backend
from proxy.hmac_auth import HmacVerifier as _HmacVerifier
from proxy.secret_store import SecretStore as _SecretStore
from proxy.secret_store import load_or_create_key as _load_or_create_key
from proxy.server import make_handler as _make_handler
from proxy import server as _server_mod


def _live_free_port() -> int:
    s = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _live_build_context(config_path: Path):
    cfg = _load_config(config_path)
    backend = _select_backend(cfg.crypto.backend)
    hmac_key = cfg.hmac.key_path.read_bytes()
    verifier = _HmacVerifier(
        key=hmac_key, timestamp_skew_seconds=cfg.hmac.timestamp_skew_seconds,
    )
    actions = _load_actions(cfg.actions_path)
    fx = cfg.fixtures.vault_read_response_path
    filtered = {k: v for k, v in actions.items() if k == "vault_read"}
    dispatcher = _ActionDispatcher(
        actions=filtered, fixtures_dir=fx.parent, vault_read_response_path=fx,
    )
    sk = _load_or_create_key(cfg.secrets.key_path)
    store = _SecretStore(cfg.secrets.store_path, sk, backend)
    audit = _AuditLog(cfg.audit.dir, sk, backend)
    return _server_mod.ServerContext(  # type: ignore[attr-defined]
        config=cfg,
        hmac=verifier,
        actions=dispatcher,
        secret_store=store,
        audit=audit,
        backend=backend,
    )


@pytest.fixture
def live_server(proxy_workspace, hmac_key, config_path):
    port = _live_free_port()
    txt = config_path.read_text()
    txt = txt.replace("port: 9911", f"port: {port}")
    config_path.write_text(txt)
    ctx = _live_build_context(config_path)
    handler = _make_handler(ctx)
    httpd = _HTTPServer(("127.0.0.1", port), handler)
    t = _threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    try:
        yield {"port": port, "key": hmac_key.read_bytes()}
    finally:
        httpd.shutdown()
        httpd.server_close()
        t.join(timeout=2)
