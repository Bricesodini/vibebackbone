"""Secret store tests.

Covers:

* roundtrip write/read with libsodium SecretStream;
* the on-disk file is *not* plain text (no grep-able secret).
"""

from __future__ import annotations

from pathlib import Path

from proxy.crypto import select_backend
from proxy.secret_store import SecretStore, load_or_create_key


def test_roundtrip_is_correct(proxy_workspace, secret_key):
    backend = select_backend("libsodium")
    key = load_or_create_key(secret_key)
    store_path = proxy_workspace / "secrets.enc"
    ss = SecretStore(store_path, key, backend)

    ss.write_secret("github_token", b"ghp_AAAABBBBCCCCDDDD")
    assert ss.read_secret("github_token") == b"ghp_AAAABBBBCCCCDDDD"


def test_on_disk_file_contains_no_cleartext(proxy_workspace, secret_key):
    backend = select_backend("libsodium")
    key = load_or_create_key(secret_key)
    store_path = proxy_workspace / "secrets.enc"
    ss = SecretStore(store_path, key, backend)

    plain = b"PLAINTEXT-MARKER-987654321"
    ss.write_secret("marker", plain)

    raw = store_path.read_bytes()
    assert plain not in raw, "Secret leaked in cleartext into secrets.enc"
    # And the VBBP1 magic header is present (5 canonical bytes)
    assert raw[:5] == b"VBBP1"
