"""Structured error codes for the Vibebackbone privacy proxy POC.

All errors raised by the proxy MUST map to one of the codes defined here.
Codes are stable strings (NOT numeric) and follow the pattern ``E_<UPPER_SNAKE>``.

The set of codes is intentionally small and is the union of:

- codes called out in the task brief (``E_BYPASS_DETECTED``,
  ``E_UNDECLARED``, ``E_HMAC_INVALID``) ;
- additional codes required to surface every failure mode in a
  structured, machine-readable way (anti-replay, contract version
  mismatch, unknown action, transport errors, internal).

Codes are referenced by ADR 0010 (security boundaries) and ADR 0011
(bypass prevention). They are the only contract surface that clients
should switch on.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


# Canonical error codes. Adding a new code is a controlled change; the
# set is closed at the POC level.
E_BYPASS_DETECTED = "E_BYPASS_DETECTED"
E_UNDECLARED = "E_UNDECLARED"
E_HMAC_INVALID = "E_HMAC_INVALID"
E_HMAC_MISSING = "E_HMAC_MISSING"
E_TIMESTAMP_MISSING = "E_TIMESTAMP_MISSING"
E_TIMESTAMP_INVALID = "E_TIMESTAMP_INVALID"
E_REPLAY_DETECTED = "E_REPLAY_DETECTED"
E_CONTRACT_VERSION = "E_CONTRACT_VERSION"
E_PAYLOAD_TOO_LARGE = "E_PAYLOAD_TOO_LARGE"
E_PAYLOAD_INVALID = "E_PAYLOAD_INVALID"
E_ACTION_UNKNOWN = "E_ACTION_UNKNOWN"
E_INTERNAL = "E_INTERNAL"
E_BOOT_CONFIG = "E_BOOT_CONFIG"
E_PERMISSION = "E_PERMISSION"
E_NOT_FOUND = "E_NOT_FOUND"
E_HEALTH = "E_HEALTH"
E_RATE_LIMITED = "E_RATE_LIMITED"
# Client-side error codes (V2): these never come from the server. They
# are raised by ``tools.proxy.client.ProxyClient`` when transport /
# decoding / connection problems occur. They are intentionally distinct
# from the server-side codes so the caller can tell "I never reached
# the daemon" apart from "the daemon rejected my request".
E_DAEMON_UNAVAILABLE = "E_DAEMON_UNAVAILABLE"
E_TIMEOUT = "E_TIMEOUT"
E_PROTOCOL = "E_PROTOCOL"


# HTTP status code associated with each error. Centralised here so the
# HTTP layer is a thin renderer.
_STATUS_BY_CODE: dict[str, int] = {
    E_BYPASS_DETECTED: 403,
    E_UNDECLARED: 403,
    E_HMAC_INVALID: 401,
    E_HMAC_MISSING: 401,
    E_TIMESTAMP_MISSING: 401,
    E_TIMESTAMP_INVALID: 401,
    E_REPLAY_DETECTED: 401,
    E_CONTRACT_VERSION: 400,
    E_PAYLOAD_TOO_LARGE: 413,
    E_PAYLOAD_INVALID: 400,
    E_ACTION_UNKNOWN: 403,
    E_INTERNAL: 500,
    E_BOOT_CONFIG: 500,
    E_PERMISSION: 500,
    E_NOT_FOUND: 404,
    E_HEALTH: 503,
    E_RATE_LIMITED: 429,
}


@dataclass(frozen=True)
class ProxyError(Exception):
    """Structured proxy error.

    Attributes:
        code: machine-readable error code (see module-level constants).
        message: short human-readable description, safe to log.
        details: optional structured details (no secrets).
        http_status: HTTP status the server should return.
    """

    code: str
    message: str
    details: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        # Register the exception args so ``str(exc)`` is informative in
        # logs (never includes payload / secret values).
        Exception.__init__(self, f"{self.code}: {self.message}")

    @property
    def http_status(self) -> int:
        return _STATUS_BY_CODE.get(self.code, 500)

    def to_dict(self) -> dict[str, Any]:
        body: dict[str, Any] = {
            "code": self.code,
            "message": self.message,
        }
        if self.details:
            body["details"] = self.details
        return body


@dataclass(frozen=True)
class ProxyClientError(Exception):
    """Client-side error raised by :class:`tools.proxy.client.ProxyClient`.

    Distinct from :class:`ProxyError` (which is the server-side error
    contract). :class:`ProxyClientError` reports transport / protocol
    problems on the *caller* side (daemon unreachable, timeout, bad
    response shape, etc.) and uses the dedicated client-side codes
    :data:`E_DAEMON_UNAVAILABLE`, :data:`E_TIMEOUT`, :data:`E_PROTOCOL`,
    or echoes a server-side code when the daemon returned an error
    response that the client can parse.

    The exception is intentionally minimal: ``code`` and ``message``
    are the public surface. Callers should never need to inspect
    ``args`` or a stack trace.
    """

    code: str
    message: str

    def __post_init__(self) -> None:
        Exception.__init__(self, f"{self.code}: {self.message}")

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


__all__ = [
    "ProxyError",
    "ProxyClientError",
    "E_BYPASS_DETECTED",
    "E_UNDECLARED",
    "E_HMAC_INVALID",
    "E_HMAC_MISSING",
    "E_TIMESTAMP_MISSING",
    "E_TIMESTAMP_INVALID",
    "E_REPLAY_DETECTED",
    "E_CONTRACT_VERSION",
    "E_PAYLOAD_TOO_LARGE",
    "E_PAYLOAD_INVALID",
    "E_ACTION_UNKNOWN",
    "E_INTERNAL",
    "E_BOOT_CONFIG",
    "E_PERMISSION",
    "E_NOT_FOUND",
    "E_HEALTH",
    "E_RATE_LIMITED",
    "E_DAEMON_UNAVAILABLE",
    "E_TIMEOUT",
    "E_PROTOCOL",
]
