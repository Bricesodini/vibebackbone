"""HMAC-SHA256 request authentication with anti-replay protection.

The proxy authenticates every request on the action endpoint with a
shared symmetric key (HMAC-SHA256, see ADR 0007 and 0010). The signature
is computed over the **raw HTTP body** (not the parsed JSON), and a
companion ``X-Proxy-Timestamp`` header provides an anti-replay window of
``config.hmac.timestamp_skew_seconds`` (default 300 s).

Why HMAC over the raw body?

* The body is exactly what the wire sees; the signature cannot be
  bypassed by re-ordering or re-serialising fields.
* The signature is verified **before** any parsing or dispatch, so
  malformed payloads from a misconfigured caller are still rejected
  with a 401 instead of a 400.

Headers:

* ``X-Proxy-Signature``: hex-encoded HMAC-SHA256 of the raw body using
  the shared key.
* ``X-Proxy-Timestamp``: integer Unix seconds (UTC) at which the
  caller signed the request.
* ``X-Proxy-Request-Id``: optional UUIDv4 echoed back in logs and the
  response (validated against the body, but not part of the signature
  to keep the contract simple).
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from . import errors

LOG = logging.getLogger("vbb.proxy.hmac_auth")

HEADER_SIGNATURE: Final[str] = "X-Proxy-Signature"
HEADER_TIMESTAMP: Final[str] = "X-Proxy-Timestamp"
HEADER_REQUEST_ID: Final[str] = "X-Proxy-Request-Id"


@dataclass(frozen=True)
class HmacVerifier:
    """Stateless HMAC verifier.

    Instances are cheap; the daemon creates one at boot and reuses it
    for every request.
    """

    key: bytes
    timestamp_skew_seconds: int = 300

    @classmethod
    def from_key_file(
        cls,
        key_path: Path,
        timestamp_skew_seconds: int = 300,
    ) -> "HmacVerifier":
        p = Path(key_path)
        if not p.exists():
            raise errors.ProxyError(
                errors.E_BOOT_CONFIG,
                f"HMAC key file not found: {p}",
            )
        if p.stat().st_mode & 0o077:
            raise errors.ProxyError(
                errors.E_PERMISSION,
                f"HMAC key file {p} is group/world accessible; "
                f"refusing to start",
            )
        key = p.read_bytes().strip()
        if not key:
            raise errors.ProxyError(
                errors.E_BOOT_CONFIG,
                f"HMAC key file {p} is empty",
            )
        return cls(key=key, timestamp_skew_seconds=timestamp_skew_seconds)

    def sign(self, body: bytes) -> str:
        """Compute the hex HMAC-SHA256 of ``body`` (used by clients)."""
        return hmac.new(self.key, body, hashlib.sha256).hexdigest()

    def verify(
        self,
        body: bytes,
        signature: str | None,
        timestamp: str | None,
    ) -> None:
        """Verify a request. Raises :class:`ProxyError` on failure.

        The function does **not** read the body; the HTTP layer is
        expected to pass the already-read raw bytes. This avoids
        double-reading and keeps the verifier framework-agnostic.
        """
        if not signature:
            raise errors.ProxyError(
                errors.E_HMAC_MISSING,
                f"missing {HEADER_SIGNATURE} header",
            )
        if not timestamp:
            raise errors.ProxyError(
                errors.E_TIMESTAMP_MISSING,
                f"missing {HEADER_TIMESTAMP} header",
            )
        try:
            ts_int = int(timestamp)
        except ValueError as exc:
            raise errors.ProxyError(
                errors.E_TIMESTAMP_INVALID,
                f"invalid {HEADER_TIMESTAMP}: not an integer",
            ) from exc

        now = int(time.time())
        if abs(now - ts_int) > self.timestamp_skew_seconds:
            raise errors.ProxyError(
                errors.E_REPLAY_DETECTED,
                f"timestamp skew exceeds {self.timestamp_skew_seconds}s "
                f"(now={now}, header={ts_int})",
            )

        # Compute the expected signature. The signature header is hex
        # encoded; we re-derive it locally to allow a constant-time
        # comparison. We use ``hmac.compare_digest`` on the hex
        # strings, which is the recommended pattern (avoids both timing
        # leaks and accepting non-hex garbage).
        expected = self.sign(body)
        if not hmac.compare_digest(expected, str(signature).strip()):
            raise errors.ProxyError(
                errors.E_HMAC_INVALID,
                "HMAC signature mismatch",
            )

    def key_fingerprint(self) -> str:
        """Stable short fingerprint of the HMAC key, safe to log.

        This is ``sha256(key)[:8]``. It is *not* the key itself and
        cannot be used to forge signatures.
        """
        return hashlib.sha256(self.key).hexdigest()[:8]


__all__ = [
    "HmacVerifier",
    "HEADER_SIGNATURE",
    "HEADER_TIMESTAMP",
    "HEADER_REQUEST_ID",
]
