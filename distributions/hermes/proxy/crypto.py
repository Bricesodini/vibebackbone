"""Crypto primitives used by the privacy proxy.

Two backends are supported:

* **libsodium SecretStream** (XChaCha20-Poly1305) — preferred backend,
  selected by setting ``crypto.backend: "libsodium"`` in
  ``~/.hermes/proxy/config.yaml`` (this is the default).
* **AES-256-GCM** — fallback used when ``crypto.backend: "cryptography"``
  is set, or when libsodium is not importable. Used so the POC can still
  run on a host where PyNaCl is missing.

The fallback exists for portability (ADR 0007 D3) and is not a feature
toggle to be used lightly. The chosen backend is logged once at boot
without leaking the key.

Every secret written by the proxy is encrypted with a unique nonce
(either a fresh libsodium SecretStream header, or a fresh 12-byte IV
for AES-GCM). The plaintext is never written to disk.

Security properties:

* the symmetric key never leaves the local user filesystem ;
* the encrypted file is unreadable without the key (verified by
  ``file(1)`` reporting ``data``) ;
* tampering with a single byte of the ciphertext is detected on read.
"""

from __future__ import annotations

import hashlib
import logging
import os
import secrets
from dataclasses import dataclass
from typing import Final

LOG = logging.getLogger("vbb.proxy.crypto")

# Backends
BACKEND_LIBSODIUM = "libsodium"
BACKEND_CRYPTOGRAPHY = "cryptography"

# libsodium SecretStream constants. ABYTES = 16 (Poly1305) + 1 byte for
# the tag indicator (MESSAGE / FINAL / etc.). We keep the whole opaque
# ``ciphertext || tag_indicator`` block together: the ``tag`` field of
# :class:`EncryptedBlob` is the integer tag indicator (0 for MESSAGE, 3
# for FINAL) and is *not* stripped from the wire format.
LIBSODIUM_HEADER_SIZE: Final[int] = 24

# Default key size (32 bytes = 256 bits) for both backends.
KEY_SIZE: Final[int] = 32

# AES-GCM IV size.
AES_GCM_NONCE_SIZE: Final[int] = 12


@dataclass(frozen=True)
class EncryptedBlob:
    """A self-describing encrypted blob.

    Attributes:
        backend: the backend used to encrypt ("libsodium" or
            "cryptography").
        ciphertext: backend-specific ciphertext. For libsodium this is
            ``ciphertext || tag_indicator`` (opaque, length-prefixed on
            disk). For cryptography this is ``ciphertext || tag``.
        header: libsodium SecretStream header (24 bytes), empty for
            AES-GCM.
        nonce: AES-GCM IV (12 bytes), empty for libsodium.
        tag: integer tag indicator (libsodium) or raw tag bytes
            (cryptography). Kept for inspection only; the on-disk
            representation already includes it.
    """

    backend: str
    ciphertext: bytes
    header: bytes
    nonce: bytes
    tag: bytes | int


# ---------------------------------------------------------------------------
# Backend selection
# ---------------------------------------------------------------------------

def _libsodium_available() -> bool:
    try:
        from nacl import bindings  # noqa: F401
        return True
    except Exception:  # pragma: no cover - environment dependent
        return False


def select_backend(configured: str) -> str:
    """Resolve the crypto backend from the configured value.

    If ``configured`` is ``"libsodium"`` but libsodium is not importable,
    we fall back to ``"cryptography"`` and log a warning. If
    ``configured`` is ``"cryptography"``, that is honoured directly.
    """
    if configured == BACKEND_LIBSODIUM:
        if _libsodium_available():
            return BACKEND_LIBSODIUM
        LOG.warning(
            "crypto backend requested=libsodium but PyNaCl is not "
            "importable; falling back to cryptography (AES-256-GCM)"
        )
        return BACKEND_CRYPTOGRAPHY
    if configured == BACKEND_CRYPTOGRAPHY:
        return BACKEND_CRYPTOGRAPHY
    # Unknown configured value: hard fail at boot, never guess.
    raise ValueError(
        f"unknown crypto backend: {configured!r} "
        f"(expected {BACKEND_LIBSODIUM!r} or {BACKEND_CRYPTOGRAPHY!r})"
    )


# ---------------------------------------------------------------------------
# Key handling
# ---------------------------------------------------------------------------

def generate_key() -> bytes:
    """Generate a fresh symmetric key of :data:`KEY_SIZE` bytes.

    Uses ``secrets.token_bytes`` (CSPRNG) and never logs the result.
    """
    return secrets.token_bytes(KEY_SIZE)


# ---------------------------------------------------------------------------
# libsodium SecretStream backend
# ---------------------------------------------------------------------------

def _libsodium_encrypt(key: bytes, plaintext: bytes) -> EncryptedBlob:
    from nacl import bindings

    state = bindings.crypto_secretstream_xchacha20poly1305_state()
    header = bindings.crypto_secretstream_xchacha20poly1305_init_push(state, key)
    if len(header) != LIBSODIUM_HEADER_SIZE:
        raise RuntimeError(
            f"libsodium SecretStream header has unexpected length "
            f"{len(header)} (expected {LIBSODIUM_HEADER_SIZE})"
        )
    ciphertext = bindings.crypto_secretstream_xchacha20poly1305_push(
        state,
        plaintext,
        b"",
        bindings.crypto_secretstream_xchacha20poly1305_TAG_FINAL,
    )
    # ``ciphertext`` is ``encrypted_plaintext || tag_indicator``; we
    # store it as-is and the tag indicator is recovered on pull.
    return EncryptedBlob(
        backend=BACKEND_LIBSODIUM,
        ciphertext=bytes(ciphertext),
        header=bytes(header),
        nonce=b"",
        tag=int(bindings.crypto_secretstream_xchacha20poly1305_TAG_FINAL),
    )


def _libsodium_decrypt(key: bytes, blob: EncryptedBlob) -> bytes:
    from nacl import bindings

    if not blob.header or len(blob.header) != LIBSODIUM_HEADER_SIZE:
        raise ValueError("libsodium blob missing or malformed header")
    state = bindings.crypto_secretstream_xchacha20poly1305_state()
    bindings.crypto_secretstream_xchacha20poly1305_init_pull(
        state, blob.header, key
    )
    result = bindings.crypto_secretstream_xchacha20poly1305_pull(
        state, blob.ciphertext, b""
    )
    if result is None or result is False:  # bindings signal failure
        raise ValueError("libsodium SecretStream integrity check failed")
    plaintext, tag_indicator = result
    if int(tag_indicator) != int(
        bindings.crypto_secretstream_xchacha20poly1305_TAG_FINAL
    ):
        raise ValueError(
            f"libsodium SecretStream unexpected tag indicator "
            f"{int(tag_indicator)} (expected FINAL)"
        )
    return bytes(plaintext)


# ---------------------------------------------------------------------------
# AES-256-GCM (cryptography) backend
# ---------------------------------------------------------------------------

def _aesgcm_encrypt(key: bytes, plaintext: bytes) -> EncryptedBlob:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    nonce = os.urandom(AES_GCM_NONCE_SIZE)
    aesgcm = AESGCM(key)
    combined = aesgcm.encrypt(nonce, plaintext, associated_data=None)
    # cryptography's AESGCM returns ciphertext || tag (last 16 bytes).
    if len(combined) < 16:
        raise RuntimeError("cryptography returned a too-short ciphertext")
    ciphertext = combined[:-16]
    tag = combined[-16:]
    return EncryptedBlob(
        backend=BACKEND_CRYPTOGRAPHY,
        ciphertext=bytes(ciphertext),
        header=b"",
        nonce=bytes(nonce),
        tag=bytes(tag),
    )


def _aesgcm_decrypt(key: bytes, blob: EncryptedBlob) -> bytes:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    if not blob.nonce or len(blob.nonce) != AES_GCM_NONCE_SIZE:
        raise ValueError("AES-GCM blob missing or malformed nonce")
    aesgcm = AESGCM(key)
    combined = blob.ciphertext + bytes(blob.tag)
    return aesgcm.decrypt(blob.nonce, combined, associated_data=None)


# ---------------------------------------------------------------------------
# Public dispatch
# ---------------------------------------------------------------------------

def encrypt(key: bytes, plaintext: bytes, backend: str) -> EncryptedBlob:
    """Encrypt ``plaintext`` using the chosen backend.

    A fresh nonce / header is generated on every call. The plaintext is
    never logged.
    """
    if not isinstance(key, (bytes, bytearray)) or len(key) != KEY_SIZE:
        raise ValueError(
            f"key must be {KEY_SIZE} bytes, got {type(key).__name__} of "
            f"{len(key) if hasattr(key, '__len__') else '?'} bytes"
        )
    if not isinstance(plaintext, (bytes, bytearray)):
        raise TypeError("plaintext must be bytes")
    if backend == BACKEND_LIBSODIUM:
        return _libsodium_encrypt(bytes(key), bytes(plaintext))
    if backend == BACKEND_CRYPTOGRAPHY:
        return _aesgcm_encrypt(bytes(key), bytes(plaintext))
    raise ValueError(f"unknown backend: {backend!r}")


def decrypt(key: bytes, blob: EncryptedBlob) -> bytes:
    """Decrypt a blob produced by :func:`encrypt`.

    Raises ``ValueError`` if the integrity tag does not verify.
    """
    if blob.backend == BACKEND_LIBSODIUM:
        return _libsodium_decrypt(key, blob)
    if blob.backend == BACKEND_CRYPTOGRAPHY:
        return _aesgcm_decrypt(key, blob)
    raise ValueError(f"unknown backend: {blob.backend!r}")


def sha256_hex(data: bytes) -> str:
    """Return the hex SHA-256 of ``data`` (used for params_hash)."""
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------------------
# Serialisation helpers
# ---------------------------------------------------------------------------

def encode_blob(blob: EncryptedBlob) -> bytes:
    """Serialise an :class:`EncryptedBlob` to a single byte string.

    Layout (length-prefixed, big-endian unsigned 32-bit)::

        [backend_len:4][backend][header_len:4][header]
        [nonce_len:4][nonce][tag_len:4][tag][ct_len:8][ciphertext]

    The framing is self-describing and the resulting file is binary
    (i.e. ``file(1)`` reports ``data``), which is the property checked
    in the POC closeout.
    """

    def _lp32(n: int) -> bytes:
        return n.to_bytes(4, "big", signed=False)

    def _lp64(n: int) -> bytes:
        return n.to_bytes(8, "big", signed=False)

    backend_b = blob.backend.encode("utf-8")
    tag_b: bytes
    if isinstance(blob.tag, int):
        tag_b = int(blob.tag).to_bytes(4, "big", signed=False)
    else:
        tag_b = bytes(blob.tag)
    return (
        _lp32(len(backend_b)) + backend_b
        + _lp32(len(blob.header)) + blob.header
        + _lp32(len(blob.nonce)) + blob.nonce
        + _lp32(len(tag_b)) + tag_b
        + _lp64(len(blob.ciphertext)) + blob.ciphertext
    )


def decode_blob(raw: bytes) -> EncryptedBlob:
    """Inverse of :func:`encode_blob`. Raises ``ValueError`` on truncated
    input.
    """

    def _read(buf: bytes, off: int, n: int) -> tuple[bytes, int]:
        if off + n > len(buf):
            raise ValueError("truncated encrypted blob")
        return buf[off:off + n], off + n

    off = 0
    backend_b, off = _read(raw, off, 4)
    backend_len = int.from_bytes(backend_b, "big", signed=False)
    backend_b, off = _read(raw, off, backend_len)
    backend = backend_b.decode("utf-8")

    header_len_b, off = _read(raw, off, 4)
    header_len = int.from_bytes(header_len_b, "big", signed=False)
    header, off = _read(raw, off, header_len)

    nonce_len_b, off = _read(raw, off, 4)
    nonce_len = int.from_bytes(nonce_len_b, "big", signed=False)
    nonce, off = _read(raw, off, nonce_len)

    tag_len_b, off = _read(raw, off, 4)
    tag_len = int.from_bytes(tag_len_b, "big", signed=False)
    tag_raw, off = _read(raw, off, tag_len)
    # For libsodium we encode the indicator as a 4-byte int; for
    # cryptography we keep the raw 16-byte tag.
    if backend == BACKEND_LIBSODIUM and tag_len == 4:
        tag_val: int | bytes = int.from_bytes(tag_raw, "big", signed=False)
    else:
        tag_val = tag_raw

    ct_len_b, off = _read(raw, off, 8)
    ct_len = int.from_bytes(ct_len_b, "big", signed=False)
    ciphertext, off = _read(raw, off, ct_len)

    return EncryptedBlob(
        backend=backend,
        ciphertext=ciphertext,
        header=header,
        nonce=nonce,
        tag=tag_val,
    )
