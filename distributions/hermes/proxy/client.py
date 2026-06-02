"""Official Python client for the Vibebackbone privacy proxy.

This module is the canonical way to call the proxy from inside the
Vibebackbone system (Hermes, Cody, VBB workers, third-party tools).
It wraps the raw HTTP + HMAC dance in a tiny, dependency-free helper
that produces a single structured exception type
(:class:`~tools.proxy.errors.ProxyClientError`) on any failure.

Design rules (mirrors the contract in :mod:`tools.proxy.contract`):

* snake_case JSON body with the canonical v1.0.0 keys;
* raw bytes are signed (HMAC-SHA256) over the *body*, not the dict;
* the request id is auto-generated as a UUIDv4 when the caller does
  not provide one;
* transport is the stdlib ``urllib.request`` — no ``requests``, no
  ``httpx``, no third-party dependency.

Security posture (this is the *only* public-facing client, treat it
as a security boundary — see ADR 0010 §3 and ADR 0011):

* the client NEVER logs the body, the HMAC key, the raw secret value
  or the full request URL with sensitive query parameters;
* in ``verbose=False`` mode (default) the client is silent;
* in ``verbose=True`` mode it logs ``request_id``, ``action_id``,
  ``status_code`` and ``duration_ms`` — never the body, never the
  value, never the HMAC key;
* on every transport / protocol failure it raises
  :class:`ProxyClientError` with a stable ``code``;
* the last response status / error are exposed as attributes
  (``last_status_code``, ``last_error``) so callers can inspect
  outcomes without parsing log lines.

Usage::

    from tools.proxy.client import ProxyClient

    client = ProxyClient(
        base_url="http://127.0.0.1:9911",
        hmac_key=open(os.path.expanduser("~/.hermes/proxy/hmac.key"), "rb").read(),
        requestor="my-worker",
    )
    result = client.exec("vault_read", {"secret_id": "fixture"})
    # result is a dict with the action payload (never log this
    # blindly if it may contain secret values; ``vault_read`` is
    # read-only and the stub fixture includes a ``value_preview``
    # field for display).

Errors are signalled as :class:`ProxyClientError`::

    from tools.proxy.errors import ProxyClientError
    try:
        client.exec(...)
    except ProxyClientError as exc:
        # exc.code: E_DAEMON_UNAVAILABLE | E_TIMEOUT | E_PROTOCOL |
        #           E_HMAC_INVALID | E_UNDECLARED | ...
        # exc.message: human-readable, safe to log
        ...
"""

from __future__ import annotations

import hashlib
import hmac as hmac_mod
import json
import logging
import time
import urllib.error
import urllib.request
import uuid
from typing import Any, Final

from . import contract, errors

LOG = logging.getLogger("vbb.proxy.client")

# Re-export the HTTP path constant from server for consistency. We
# avoid a hard import of :mod:`tools.proxy.server` to keep the client
# importable in contexts where the server module is not available
# (e.g. lightweight worker scripts).
EXEC_PATH: Final[str] = "/proxy/v1/exec"

# Default request timeout. Short by design: the proxy is on the
# loopback, anything slower is a sign of trouble.
DEFAULT_TIMEOUT: Final[float] = 5.0


class ProxyClient:
    """Minimal, dependency-free client for the privacy proxy.

    Parameters
    ----------
    base_url:
        Origin of the proxy daemon, e.g. ``"http://127.0.0.1:9911"``.
        Trailing slashes are tolerated.
    hmac_key:
        The shared HMAC key as raw bytes. The key is held in memory
        for the lifetime of the instance; it is never logged and
        should be loaded from ``~/.hermes/proxy/hmac.key`` (or the
        path the local config points at).
    requestor:
        Free-form human-readable identifier of the caller, written
        into the contract ``requestor`` field. Used by the audit log.
    timeout:
        Per-request timeout in seconds (default 5.0). Loops over
        many requests should set this explicitly to avoid surprises.
    verbose:
        When ``True`` the client logs ``request_id``, ``action_id``,
        ``status_code`` and ``duration_ms`` at INFO level. The
        default ``False`` keeps the client silent; this is the
        recommended posture for production workers that already have
        their own logging.
    """

    def __init__(
        self,
        base_url: str,
        hmac_key: bytes,
        requestor: str = "client",
        timeout: float = DEFAULT_TIMEOUT,
        verbose: bool = False,
    ) -> None:
        if not isinstance(base_url, str) or not base_url:
            raise ValueError("base_url must be a non-empty string")
        if not isinstance(hmac_key, (bytes, bytearray)) or not hmac_key:
            raise ValueError("hmac_key must be a non-empty bytes object")
        if not isinstance(requestor, str) or not requestor:
            raise ValueError("requestor must be a non-empty string")
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            raise ValueError("timeout must be a positive number")
        # Strip a single trailing slash so the URL builder is clean.
        self._base_url = base_url.rstrip("/")
        # Keep a defensive copy of the key bytes; never expose them.
        self._hmac_key = bytes(hmac_key)
        self._requestor = requestor
        self._timeout = float(timeout)
        self._verbose = bool(verbose)
        # Observable state for the caller — never logged automatically.
        self.last_status_code: int | None = None
        self.last_error: errors.ProxyClientError | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def exec(
        self,
        action_id: str,
        params: dict[str, Any] | None = None,
        *,
        request_id: str | None = None,
    ) -> dict[str, Any]:
        """Execute ``action_id`` with ``params`` and return the result.

        Returns the ``result`` dict from the proxy response on success.

        Raises
        ------
        ProxyClientError
            On any transport, protocol, or daemon-reported failure.
            The ``code`` attribute is the canonical error code (see
            :mod:`tools.proxy.errors`).
        """
        if not isinstance(action_id, str) or not action_id:
            raise errors.ProxyClientError(
                errors.E_PAYLOAD_INVALID,
                "action_id must be a non-empty string",
            )
        if params is None:
            params = {}
        if not isinstance(params, dict):
            raise errors.ProxyClientError(
                errors.E_PAYLOAD_INVALID,
                "params must be a dict",
            )

        rid = request_id or str(uuid.uuid4())
        # Defensive: refuse to send a non-UUID request_id so the proxy
        # cannot blame the client for E_PAYLOAD_INVALID.
        if not _is_uuid4(rid):
            raise errors.ProxyClientError(
                errors.E_PAYLOAD_INVALID,
                "request_id must be a UUIDv4 string",
            )

        body_obj = {
            "contract_version": contract.CONTRACT_VERSION,
            "request_id": rid,
            "action_id": action_id,
            "params": params,
            "requestor": self._requestor,
        }
        # Compact serialisation: matches the contract lint and the
        # other test helpers (separators=(",", ":")).
        body = json.dumps(body_obj, separators=(",", ":")).encode("utf-8")
        ts = str(int(time.time()))
        sig = hmac_mod.new(self._hmac_key, body, hashlib.sha256).hexdigest()

        url = f"{self._base_url}{EXEC_PATH}"
        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "X-Proxy-Signature": sig,
                "X-Proxy-Timestamp": ts,
                "X-Proxy-Request-Id": rid,
            },
            method="POST",
        )

        if self._verbose:
            LOG.info(
                "client: request_id=%s action_id=%s -> %s",
                rid, action_id, url,
            )

        start = time.monotonic()
        try:
            response = urllib.request.urlopen(req, timeout=self._timeout)
            raw = response.read()
            status = int(response.status)
        except urllib.error.HTTPError as exc:
            # HTTP error is the *expected* failure mode for protocol
            # errors (401, 403, 400 ...). Try to read the structured
            # error body.
            status = int(exc.code)
            try:
                raw = exc.read()
            except Exception:  # pragma: no cover - defensive
                raw = b""
            self.last_status_code = status
            self.last_error = self._build_error_from_http(
                status=status, raw=raw, url=url,
            )
            if self._verbose:
                LOG.info(
                    "client: response request_id=%s status=%d duration_ms=%d",
                    rid, status, _ms(start),
                )
            assert self.last_error is not None  # for type-checkers
            raise self.last_error
        except urllib.error.URLError as exc:
            # Connection refused, DNS, etc.
            self.last_status_code = None
            reason = getattr(exc, "reason", None)
            self.last_error = errors.ProxyClientError(
                errors.E_DAEMON_UNAVAILABLE,
                f"daemon not reachable at {url} ({reason or exc!r})",
            )
            if self._verbose:
                LOG.info(
                    "client: response request_id=%s status=<unreachable> duration_ms=%d",
                    rid, _ms(start),
                )
            raise self.last_error
        except (TimeoutError, socket_timeout()) as exc:
            self.last_status_code = None
            self.last_error = errors.ProxyClientError(
                errors.E_TIMEOUT,
                f"request to {url} timed out after {self._timeout}s ({exc!r})",
            )
            if self._verbose:
                LOG.info(
                    "client: response request_id=%s status=<timeout> duration_ms=%d",
                    rid, _ms(start),
                )
            raise self.last_error
        except (ConnectionRefusedError, ConnectionError, OSError) as exc:
            # Belt-and-braces: some Python builds surface connection
            # errors as plain OSError rather than URLError.
            self.last_status_code = None
            self.last_error = errors.ProxyClientError(
                errors.E_DAEMON_UNAVAILABLE,
                f"daemon not reachable at {url} ({exc!r})",
            )
            if self._verbose:
                LOG.info(
                    "client: response request_id=%s status=<unreachable> duration_ms=%d",
                    rid, _ms(start),
                )
            raise self.last_error

        self.last_status_code = status
        # 2xx is the only branch that does not raise.
        if status < 200 or status >= 300:  # pragma: no cover - defensive
            self.last_error = errors.ProxyClientError(
                errors.E_PROTOCOL,
                f"unexpected HTTP status {status} from {url}",
            )
            raise self.last_error

        try:
            payload = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            self.last_error = errors.ProxyClientError(
                errors.E_PROTOCOL,
                f"response from {url} is not valid JSON: {exc!r}",
            )
            raise self.last_error

        if not isinstance(payload, dict):
            self.last_error = errors.ProxyClientError(
                errors.E_PROTOCOL,
                f"response from {url} is not a JSON object",
            )
            raise self.last_error

        if self._verbose:
            LOG.info(
                "client: response request_id=%s status=%d duration_ms=%d",
                rid, status, _ms(start),
            )

        if payload.get("status") == "error":
            err_obj = payload.get("error") or {}
            code = str(err_obj.get("code") or errors.E_PROTOCOL)
            message = str(err_obj.get("message") or "")
            self.last_error = errors.ProxyClientError(code, message)
            raise self.last_error

        result = payload.get("result")
        if not isinstance(result, dict):
            # Treat a missing or malformed result as a protocol
            # violation; the proxy is supposed to return a dict.
            self.last_error = errors.ProxyClientError(
                errors.E_PROTOCOL,
                f"response from {url} has no 'result' object",
            )
            raise self.last_error
        self.last_error = None
        return result

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _build_error_from_http(
        self,
        *,
        status: int,
        raw: bytes,
        url: str,
    ) -> errors.ProxyClientError:
        """Convert an HTTP error into a structured :class:`ProxyClientError`.

        The proxy always responds with a JSON ``error.code`` /
        ``error.message`` pair; we try to surface those. If the
        body is not parseable we fall back to a generic
        :data:`E_PROTOCOL` so the caller can still tell *something*
        went wrong.
        """
        if raw:
            try:
                payload = json.loads(raw.decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                payload = None
            if isinstance(payload, dict):
                err_obj = payload.get("error") or {}
                if isinstance(err_obj, dict):
                    code = str(err_obj.get("code") or _status_to_default(status))
                    message = str(err_obj.get("message") or f"HTTP {status}")
                    return errors.ProxyClientError(code, message)
        return errors.ProxyClientError(
            _status_to_default(status),
            f"HTTP {status} from {url}",
        )


def _status_to_default(status: int) -> str:
    """Map an HTTP status to a client-side default error code."""
    if status in (401, 403):
        return errors.E_HMAC_INVALID
    if status in (400, 404, 409, 422):
        return errors.E_PAYLOAD_INVALID
    if status in (408,):
        return errors.E_TIMEOUT
    if status in (502, 503, 504):
        return errors.E_DAEMON_UNAVAILABLE
    if status >= 500:
        return errors.E_INTERNAL
    return errors.E_PROTOCOL


_UUID4_RE: Final = (
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)


def _is_uuid4(s: str) -> bool:
    import re
    return bool(re.match(_UUID4_RE, s, re.IGNORECASE))


def _ms(start: float) -> int:
    return int((time.monotonic() - start) * 1000)


def socket_timeout():
    """Return the platform socket.timeout class for isinstance checks."""
    import socket
    return socket.timeout


__all__ = ["ProxyClient", "EXEC_PATH", "DEFAULT_TIMEOUT"]
