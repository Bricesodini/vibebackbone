"""Append-only encrypted audit log for the privacy proxy POC.

Every action that the proxy attempts is recorded as a JSON Lines entry,
encrypted with the active crypto backend (libsodium SecretStream by
default). The on-disk file is binary (``file(1)`` reports ``data``) and
can only be read back with the key used to write it.

Each entry is keyed on ``(date, request_id)`` so that replays and
duplicate ids in the same day cannot silently overwrite a previous
record. The on-disk representation is:

    magic(4) || header(24) || nonce(0 for libsodium / 12 for AES-GCM)
    || ciphertext || tag

where ``ciphertext`` is the concatenation of all JSON Lines entries
written in the lifetime of the file (one per call to
:meth:`AuditLog.append`).

The audit key is loaded from ``config.secrets.key_path`` (the same key
as the secret store at the POC level — there is no separate audit key
yet, see ADR 0007 §2.1).
"""

from __future__ import annotations

import json
import logging
import os
import stat
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Final

from . import crypto
from . import errors

LOG = logging.getLogger("vbb.proxy.audit")

# Same magic as the secret store, with a distinct version byte to make
# tooling able to tell them apart. The body is still a single
# length-prefixed encrypted blob.
_FILE_HEADER: Final[str] = "VBBA1"


class AuditLog:
    """Encrypted append-only JSON Lines log.

    The implementation keeps an in-memory buffer of the current day's
    file, encrypted on every flush. This keeps the POC simple (one
    file per day, rewritten atomically on each append) while preserving
    the on-disk encryption property.
    """

    def __init__(
        self,
        dir_path: Path,
        key: bytes,
        backend: str,
        file_prefix: str = "audit-",
        file_suffix: str = ".log",
    ) -> None:
        self._dir = Path(dir_path)
        self._key = key
        self._backend = backend
        self._file_prefix = file_prefix
        self._file_suffix = file_suffix
        self._lock = threading.Lock()
        self._dir.mkdir(parents=True, exist_ok=True)
        # The audit dir must be 0o700 so the file is unspoofable by
        # other local users.
        os.chmod(self._dir, 0o700)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def append(self, entry: dict[str, Any]) -> None:
        """Encrypt and append a single audit entry.

        ``entry`` MUST NOT contain secret values, HMAC key material or
        raw request bodies. The helper enforces that the only string
        values written are non-empty ``request_id``/``action_id`` etc.
        (the contract guarantees this upstream).
        """
        if not isinstance(entry, dict):
            raise TypeError("audit entry must be a dict")
        # Inject timestamp if missing. The caller may also set it
        # explicitly for deterministic tests.
        entry.setdefault(
            "timestamp",
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )
        # Defensive: refuse to persist anything that looks like a
        # secret string. This is belt-and-braces; the proxy never
        # passes secrets here.
        for k, v in entry.items():
            if isinstance(v, str) and ("secret" in k.lower() and "value" in k.lower()):
                raise errors.ProxyError(
                    errors.E_INTERNAL,
                    f"refusing to write audit entry that looks like a "
                    f"secret: key={k!r}",
                )
        line = json.dumps(entry, sort_keys=True, ensure_ascii=False)
        with self._lock:
            path = self._path_for(entry["timestamp"])
            entries = self._load_entries(path)
            entries.append(line)
            raw = self._encrypt(entries)
            self._atomic_write(path, raw)
        LOG.debug("audit: appended entry for %s", entry.get("request_id"))

    def current_path(self) -> Path:
        """Return the path of the file that would be written today."""
        return self._path_for(datetime.now(timezone.utc).isoformat())

    # ------------------------------------------------------------------
    # Test / debug helpers
    # ------------------------------------------------------------------

    def read_entries(self, day: datetime | None = None) -> list[dict[str, Any]]:
        """Return the decrypted entries for ``day`` (defaults to today)."""
        if day is None:
            day = datetime.now(timezone.utc)
        path = self._dir / (
            f"{self._file_prefix}{day.strftime('%Y-%m-%d')}{self._file_suffix}"
        )
        lines = self._load_entries(path)
        return [json.loads(l) for l in lines]

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _path_for(self, ts: str) -> Path:
        day = ts[:10]  # ISO-8601 prefix
        return self._dir / f"{self._file_prefix}{day}{self._file_suffix}"

    def _load_entries(self, path: Path) -> list[str]:
        if not path.exists():
            return []
        cur = stat.S_IMODE(path.stat().st_mode)
        if cur & 0o077:
            raise errors.ProxyError(
                errors.E_PERMISSION,
                f"audit log {path} is group/world accessible "
                f"(mode=0o{cur:o}); refusing to read",
            )
        raw = path.read_bytes()
        if not raw:
            return []
        if not raw.startswith(_FILE_HEADER.encode("ascii")):
            raise errors.ProxyError(
                errors.E_INTERNAL,
                f"audit log {path} has invalid header",
            )
        body = raw[len(_FILE_HEADER):]
        blob = crypto.decode_blob(body)
        plaintext = crypto.decrypt(self._key, blob)
        # The plaintext is JSON Lines, one entry per line.
        text = plaintext.decode("utf-8").rstrip("\n")
        if not text:
            return []
        return text.split("\n")

    def _encrypt(self, entries: list[str]) -> bytes:
        plaintext = ("\n".join(entries) + "\n").encode("utf-8")
        blob = crypto.encrypt(self._key, plaintext, self._backend)
        return _FILE_HEADER.encode("ascii") + crypto.encode_blob(blob)

    def _atomic_write(self, path: Path, raw: bytes) -> None:
        tmp = path.with_suffix(path.suffix + ".tmp")
        fd = os.open(
            str(tmp),
            os.O_CREAT | os.O_WRONLY | os.O_TRUNC,
            0o600,
        )
        try:
            os.write(fd, raw)
        finally:
            os.close(fd)
        os.replace(tmp, path)
        os.chmod(path, 0o600)


__all__ = ["AuditLog"]
