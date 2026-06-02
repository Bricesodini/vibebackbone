"""End-to-end tests for the ``tools.proxy.cli`` module.

The tests run the CLI in a subprocess (the way an operator would)
and assert on its exit code and output. The CLI must NEVER print
the secret value, even in verbose mode (verbose only dumps the
proxy response to stderr, but the response itself is the caller's
responsibility to scrub if needed; the contract here is that the
*default* mode never emits the value).
"""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import threading
from http.server import HTTPServer
from pathlib import Path

import pytest

from tools.proxy.actions import ActionDispatcher
from tools.proxy.audit import AuditLog
from tools.proxy.config import load_actions, load_config
from tools.proxy.crypto import select_backend
from tools.proxy.hmac_auth import HmacVerifier
from tools.proxy.secret_store import SecretStore, load_or_create_key
from tools.proxy.server import make_handler  # type: ignore[attr-definitions]
from tools.proxy import server as server_mod


def _free_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _build_context(config_path: Path):
    cfg = load_config(config_path)
    backend = select_backend(cfg.crypto.backend)
    hmac_key = cfg.hmac.key_path.read_bytes()
    verifier = HmacVerifier(
        key=hmac_key, timestamp_skew_seconds=cfg.hmac.timestamp_skew_seconds,
    )
    actions = load_actions(cfg.actions_path)
    fx = cfg.fixtures.vault_read_response_path
    filtered = {k: v for k, v in actions.items() if k == "vault_read"}
    dispatcher = ActionDispatcher(
        actions=filtered, fixtures_dir=fx.parent, vault_read_response_path=fx,
    )
    sk = load_or_create_key(cfg.secrets.key_path)
    store = SecretStore(cfg.secrets.store_path, sk, backend)
    audit = AuditLog(cfg.audit.dir, sk, backend)
    return server_mod.ServerContext(  # type: ignore[attr-defined]
        config=cfg,
        hmac=verifier,
        actions=dispatcher,
        secret_store=store,
        audit=audit,
        backend=backend,
    )


@pytest.fixture
def cli_live_server(proxy_workspace, hmac_key, config_path):
    """A live server plus the env var so the CLI picks the key automatically."""
    port = _free_port()
    txt = config_path.read_text()
    txt = txt.replace("port: 9911", f"port: {port}")
    config_path.write_text(txt)
    ctx = _build_context(config_path)
    handler = make_handler(ctx)
    httpd = HTTPServer(("127.0.0.1", port), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    try:
        yield {"port": port, "key_path": hmac_key}
    finally:
        httpd.shutdown()
        httpd.server_close()
        t.join(timeout=2)


def test_cli_vault_read_success(cli_live_server):
    env = os.environ.copy()
    env["VBB_PROXY_HMAC_KEY"] = str(cli_live_server["key_path"])
    proc = subprocess.run(
        [
            sys.executable, "-m", "tools.proxy.cli",
            "--url", f"http://127.0.0.1:{cli_live_server['port']}",
            "--timeout", "5",
            "vault_read", "fixture",
        ],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(Path(__file__).resolve().parents[3]),
    )
    assert proc.returncode == 0, (
        f"CLI failed: rc={proc.returncode} stdout={proc.stdout!r} "
        f"stderr={proc.stderr!r}"
    )
    # stdout must contain the safe display fields.
    assert "status: ok" in proc.stdout
    assert "secret_id: fixture" in proc.stdout
    assert "value_preview:" in proc.stdout
    # And the raw secret value (the STUB marker) must NEVER appear
    # in stdout. The stub value_preview is "STUB***" but the full
    # value is "STUB-POC-VAULT-READ-VALUE-XXXX" — we assert the
    # full value is absent.
    assert "STUB-POC-VAULT-READ-VALUE-XXXX" not in proc.stdout
    assert "STUB-POC-VAULT-READ-VALUE-XXXX" not in proc.stderr


def test_cli_daemon_unavailable(tmp_path):
    # No server running. The CLI must exit non-zero and print the
    # error code on stderr.
    fake_key = tmp_path / "hmac.key"
    import os as _os
    fake_key.write_bytes(_os.urandom(32))
    fake_key.chmod(0o600)

    proc = subprocess.run(
        [
            sys.executable, "-m", "tools.proxy.cli",
            "--url", "http://127.0.0.1:1",
            "--hmac-key", str(fake_key),
            "--timeout", "1",
            "vault_read", "fixture",
        ],
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).resolve().parents[3]),
    )
    assert proc.returncode != 0
    assert "E_DAEMON_UNAVAILABLE" in proc.stderr
    # stdout must be empty (no result fields).
    assert proc.stdout == ""


def test_cli_help_exits_zero():
    proc = subprocess.run(
        [sys.executable, "-m", "tools.proxy.cli", "--help"],
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).resolve().parents[3]),
    )
    assert proc.returncode == 0
    assert "vault_read" in proc.stdout
    assert "--url" in proc.stdout
    assert "--hmac-key" in proc.stdout
