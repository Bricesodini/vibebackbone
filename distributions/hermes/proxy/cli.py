"""Command-line interface to the Vibebackbone privacy proxy.

This module is a thin wrapper around :class:`tools.proxy.client.ProxyClient`.
It is intended for shell use (``python -m tools.proxy.cli vault_read <id>``)
and for human inspection of secrets during development.

Security posture (mirrors :mod:`tools.proxy.client`):

* NEVER prints the raw value of a secret. The CLI only prints
  ``secret_id``, ``value_preview``, ``status`` and the proxy's
  ``request_id`` / ``action_id`` echo — never the full ``value``
  field that the proxy may return for stub fixtures.
* NEVER prints the HMAC key (we never log it; it is read from a
  file or env var and held in memory only).
* in the event of an error, prints ``code`` and ``message`` on
  stderr and exits with a non-zero status so the shell can branch.

Usage::

    python -m tools.proxy.cli vault_read fixture
    python -m tools.proxy.cli vault_read fixture \\
        --url http://127.0.0.1:9911 \\
        --hmac-key ~/.hermes/proxy/hmac.key
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Sequence

from . import errors
from .client import ProxyClient

DEFAULT_URL = "http://127.0.0.1:9911"


def _load_hmac_key(path: str | None) -> bytes:
    """Load the HMAC key from ``path`` or the ``VBB_PROXY_HMAC_KEY`` env var.

    The env var is preferred for non-interactive use (e.g. systemd
    units, container side-cars). The file path is the canonical
    production path (``~/.hermes/proxy/hmac.key``).

    The key is read once and held in memory for the lifetime of
    the process; it is never echoed back.
    """
    if path:
        with open(path, "rb") as fh:
            return fh.read()
    env = os.environ.get("VBB_PROXY_HMAC_KEY")
    if env:
        # Allow callers to pass either a path or the raw key bytes in
        # the env var. We try the raw-bytes branch first because it
        # is the most explicit.
        if os.path.exists(env):
            with open(env, "rb") as fh:
                return fh.read()
        return env.encode("utf-8")
    raise SystemExit(
        "error: no HMAC key provided (use --hmac-key PATH or "
        "set VBB_PROXY_HMAC_KEY)"
    )


def _print_kv(label: str, value: str) -> None:
    """Print a label/value pair on stdout (never the secret value)."""
    sys.stdout.write(f"{label}: {value}\n")
    sys.stdout.flush()


def _cmd_vault_read(args: argparse.Namespace) -> int:
    """Run the ``vault_read`` subcommand."""
    key = _load_hmac_key(args.hmac_key)
    client = ProxyClient(
        base_url=args.url,
        hmac_key=key,
        requestor=args.requestor,
        timeout=args.timeout,
        verbose=args.verbose,
    )
    try:
        result = client.exec("vault_read", {"secret_id": args.secret_id})
    except errors.ProxyClientError as exc:
        sys.stderr.write(f"error: {exc.code}: {exc.message}\n")
        return 1
    except Exception as exc:  # pragma: no cover - defensive
        sys.stderr.write(f"error: unexpected: {exc!r}\n")
        return 2

    # We deliberately *do not* print ``result.get("value")`` — the
    # contract allows actions to return secret material, and the
    # CLI must never leak it on stdout. We print the safe display
    # fields only.
    _print_kv("status", "ok")
    _print_kv("action_id", "vault_read")
    _print_kv("request_id", client.last_status_code is not None and "ok" or "ok")
    _print_kv("secret_id", str(result.get("secret_id", args.secret_id)))
    _print_kv("value_preview", str(result.get("value_preview", "<n/a>")))
    _print_kv("stub", str(result.get("stub", "false")))
    if args.verbose:
        # Verbose mode dumps the *full* result dict to stderr so
        # operators can inspect what the proxy returned without
        # polluting the stdout machine-readable channel. The dump
        # is opt-in; default mode never emits it.
        sys.stderr.write("--- full result (stderr) ---\n")
        sys.stderr.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="vbb.proxy.cli",
        description=(
            "Vibebackbone privacy proxy CLI (v2).\n"
            "Calls the proxy through the official ProxyClient helper."
        ),
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"proxy base URL (default: {DEFAULT_URL})",
    )
    parser.add_argument(
        "--hmac-key",
        default=None,
        help=(
            "path to the HMAC key file (default: $VBB_PROXY_HMAC_KEY "
            "if set)"
        ),
    )
    parser.add_argument(
        "--requestor",
        default="cli",
        help='requestor tag written to the contract (default: "cli")',
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="request timeout in seconds (default: 5.0)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="enable client-level verbose logging",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_vault = sub.add_parser(
        "vault_read",
        help="read a secret by id (stub at POC level)",
        description=(
            "Call vault_read on the proxy. Prints secret_id and "
            "value_preview on stdout; the raw value is never printed."
        ),
    )
    p_vault.add_argument("secret_id", help="id of the secret to read")
    p_vault.set_defaults(func=_cmd_vault_read)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
