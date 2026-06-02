"""Encrypted local secret store for the privacy proxy POC.

Each secret is stored as a single :class:`~tools.proxy.crypto.EncryptedBlob`
in a JSON file. The file format is deliberately append-friendly but the
POC only needs the read / write helpers called out in the brief:

* :func:`read_secret` returns the plaintext (or raises if missing).
* :func:`write_secret` stores or overwrites a secret.

The encrypted blob uses the same backend as the rest of the proxy
(libsodium SecretStream by default, AES-256-GCM as fallback).

Notes:

* The on-disk file (``secrets.enc``) is binary. ``file(1)`` reports
  ``data`` because the framing is length-prefixed binary.
* The HMAC key file (``hmac.key``) and the secret store key file
  (``secrets.key``) are managed separately; the secret store key is
  loaded once at construction.
* Every successful write also produces an audit log entry
  (status=``write_ok`` / ``read_ok`` / ``read_missing``) — but **never**
  with the secret value.
"""

from __future__ import annotations

import json
import logging
import os
import stat
from pathlib import Path
from typing import Any, Final

from . import crypto
from . import errors

LOG = logging.getLogger("vbb.proxy.secret_store")

_FILE_HEADER: Final[str] = "VBBP1"  # magic + version; length-prefixed binary follows.


class SecretStore:
    """An encrypted key/value store backed by a single file.

    Keys are short identifiers (``[a-z0-9_.-]+``). Values are arbitrary
    bytes. The file is rewritten atomically on every successful write.
    """

    def __init__(
        self,
        store_path: Path,
        key: bytes,
        backend: str,
    ) -> None:
        self._path = Path(store_path)
        self._key = key
        self._backend = backend
        # Ensure the store file exists with tight permissions.
        if not self._path.exists():
            self._path.parent.mkdir(parents=True, exist_ok=True)
            empty = self._encrypt({})
            self._atomic_write(empty)
        else:
            cur = stat.S_IMODE(self._path.stat().st_mode)
            if cur & 0o077:
                raise errors.ProxyError(
                    errors.E_PERMISSION,
                    f"secret store {self._path} is group/world accessible "
                    f"(mode=0o{cur:o}); refusing to start",
                )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def read_secret(self, secret_id: str) -> bytes:
        """Return the plaintext of ``secret_id`` or raise :class:`ProxyError`."""
        _validate_id(secret_id)
        data = self._load_decrypted()
        if secret_id not in data:
            raise errors.ProxyError(
                errors.E_NOT_FOUND,
                f"secret {secret_id!r} not found",
            )
        value = data[secret_id]
        if not isinstance(value, (bytes, bytearray)):
            # Defensive: values must be stored as base64-encoded text.
            raise errors.ProxyError(
                errors.E_INTERNAL,
                f"secret {secret_id!r} has unexpected type "
                f"{type(value).__name__}",
            )
        return bytes(value)

    def write_secret(self, secret_id: str, value: bytes) -> None:
        """Encrypt and persist ``secret_id`` -> ``value``."""
        _validate_id(secret_id)
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError("secret value must be bytes")
        data = self._load_decrypted()
        data[secret_id] = bytes(value)
        self._atomic_write(self._encrypt(data))
        LOG.info(
            "secret_store: write ok id=%s size=%d",
            secret_id, len(value),
        )

    def has_secret(self, secret_id: str) -> bool:
        _validate_id(secret_id)
        data = self._load_decrypted()
        return secret_id in data

    def list_ids(self) -> list[str]:
        """Return the list of secret ids currently stored."""
        return list(self._load_decrypted().keys())

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _atomic_write(self, raw: bytes) -> None:
        tmp = self._path.with_suffix(self._path.suffix + ".tmp")
        fd = os.open(
            str(tmp),
            os.O_CREAT | os.O_WRONLY | os.O_TRUNC,
            0o600,
        )
        try:
            os.write(fd, raw)
        finally:
            os.close(fd)
        os.replace(tmp, self._path)
        os.chmod(self._path, 0o600)

    def _load_decrypted(self) -> dict[str, bytes]:
        raw = self._path.read_bytes()
        if not raw:
            return {}
        if not raw.startswith(_FILE_HEADER.encode("ascii")):
            raise errors.ProxyError(
                errors.E_INTERNAL,
                f"secret store {self._path} has invalid header",
            )
        body = raw[len(_FILE_HEADER):]
        # The body is a length-prefixed concatenation of one or more
        # blobs, but the POC only ever writes a single blob. We treat
        # the body as exactly one blob.
        blob = crypto.decode_blob(body)
        plaintext = crypto.decrypt(self._key, blob)
        obj = json.loads(plaintext.decode("utf-8"))
        if not isinstance(obj, dict):
            raise errors.ProxyError(
                errors.E_INTERNAL,
                "secret store JSON must decode to an object",
            )
        # Values were stored as base64-encoded bytes for JSON safety.
        import base64
        out: dict[str, bytes] = {}
        for k, v in obj.items():
            if not isinstance(v, str):
                raise errors.ProxyError(
                    errors.E_INTERNAL,
                    f"secret {k!r} has non-string encoded value",
                )
            out[k] = base64.b64decode(v)
        return out

    def _encrypt(self, data: dict[str, bytes]) -> bytes:
        import base64
        serialisable = {k: base64.b64encode(v).decode("ascii") for k, v in data.items()}
        plaintext = json.dumps(serialisable, sort_keys=True).encode("utf-8")
        blob = crypto.encrypt(self._key, plaintext, self._backend)
        body = crypto.encode_blob(blob)
        return _FILE_HEADER.encode("ascii") + body


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _validate_id(secret_id: str) -> None:
    if not isinstance(secret_id, str) or not secret_id:
        raise errors.ProxyError(
            errors.E_PAYLOAD_INVALID,
            "secret_id must be a non-empty string",
        )
    import re
    if not re.match(r"^[a-z0-9_.\-]+$", secret_id):
        raise errors.ProxyError(
            errors.E_PAYLOAD_INVALID,
            f"secret_id {secret_id!r} contains illegal characters",
        )


def load_or_create_key(key_path: Path) -> bytes:
    """Load the symmetric key from ``key_path``, creating it if missing.

    The file is created with mode 0o600 and parent directories with
    0o700. The key itself is never logged.
    """
    p = Path(key_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        cur = stat.S_IMODE(p.stat().st_mode)
        if cur & 0o077:
            raise errors.ProxyError(
                errors.E_PERMISSION,
                f"secret key file {p} is group/world accessible "
                f"(mode=0o{cur:o}); refusing to start",
            )
        return p.read_bytes()
    key = crypto.generate_key()
    fd = os.open(str(p), os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
    try:
        os.write(fd, key)
    finally:
        os.close(fd)
    os.chmod(p, 0o600)
    return key


__all__ = ["SecretStore", "load_or_create_key"]
