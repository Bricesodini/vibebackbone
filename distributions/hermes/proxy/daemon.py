"""Privacy proxy POC daemon entry point.

This module is the script the operator (Brice) launches to start the
proxy. It:

1. Locates the configuration file (``~/.hermes/proxy/config.yaml`` by
   default; ``VBB_PROXY_CONFIG`` env var overrides).
2. Validates the file permissions on the HMAC key, secrets key and
   audit directory.
3. Boots the runtime context and HTTP server.
4. Handles ``SIGTERM`` / ``SIGINT`` cleanly.

The daemon is a *single* Python process by design (ADR 0006 D1,
re-confirmed in ADR 0012).
"""

from __future__ import annotations

import argparse
import logging
import os
import signal
import sys
from pathlib import Path

from . import config as config_mod
from . import crypto, server
from .config import ProxyConfig

LOG = logging.getLogger("vbb.proxy.daemon")

DEFAULT_CONFIG_PATH = "~/.hermes/proxy/config.yaml"


def _setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )


def _check_filesystem(config: ProxyConfig) -> None:
    """Apply the security guardrails defined in the POC brief.

    The proxy MUST refuse to start if:

    * ``secrets.key`` is not 0o600 ;
    * ``~/.hermes/proxy/`` is not 0o700 ;
    * ``secrets.enc`` is not 0o600 (when it exists).
    """
    base = config.base_dir()
    config_mod.ensure_dir_secure(base, mode=0o700)
    if not config.secrets.key_path.exists():
        # create it now with 0o600 so the next start passes the check.
        from . import secret_store
        secret_store.load_or_create_key(config.secrets.key_path)
    config_mod.ensure_file_secure(config.secrets.key_path, mode=0o600)
    if config.secrets.store_path.exists():
        config_mod.ensure_file_secure(config.secrets.store_path, mode=0o600)
    if not config.hmac.key_path.exists():
        # Create a fresh HMAC key on first boot. 32 bytes hex-encoded
        # would be 64 chars; we store the raw bytes and strip on load.
        key = crypto.generate_key()
        config_mod.ensure_file_secure(config.hmac.key_path, mode=0o600)
        Path(config.hmac.key_path).write_bytes(key)
    config_mod.ensure_file_secure(config.hmac.key_path, mode=0o600)
    config_mod.ensure_dir_secure(config.audit.dir, mode=0o700)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="vbb.proxy.daemon",
        description="Vibebackbone privacy proxy POC daemon",
    )
    parser.add_argument(
        "--config",
        default=os.environ.get("VBB_PROXY_CONFIG", DEFAULT_CONFIG_PATH),
        help="Path to config.yaml (default: %(default)s)",
    )
    args = parser.parse_args(argv)

    from . import errors as _errors
    try:
        config = config_mod.load_config(args.config)
    except _errors.ProxyError as exc:
        # Logger is not yet configured; print to stderr and exit.
        sys.stderr.write(f"FATAL: {exc.code}: {exc.message}\n")
        return 2

    _setup_logging(config.log_level)
    LOG.info("vbb.proxy: booting with config=%s", args.config)

    try:
        _check_filesystem(config)
    except _errors.ProxyError as exc:
        LOG.error("filesystem check failed: %s :: %s", exc.code, exc.message)
        return 2

    try:
        ctx = server.build_context(config)
    except _errors.ProxyError as exc:
        LOG.error("context build failed: %s :: %s", exc.code, exc.message)
        return 2

    httpd = server.serve(config, ctx)
    LOG.info(
        "vbb.proxy: listening on http://%s:%d (exec=%s health=%s)",
        config.host, config.port, server.PATH_EXEC, server.PATH_HEALTH,
    )

    def _shutdown(signum: int, _frame: object) -> None:
        LOG.info("vbb.proxy: received signal %d, shutting down", signum)
        # ``shutdown`` must be called from a different thread in
        # Python; the signal handler runs in the main thread so we
        # schedule the actual shutdown via a timer.
        import threading
        threading.Timer(0.01, httpd.shutdown).start()

    signal.signal(signal.SIGTERM, _shutdown)
    signal.signal(signal.SIGINT, _shutdown)

    try:
        httpd.serve_forever()
    finally:
        httpd.server_close()
        LOG.info("vbb.proxy: stopped")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
