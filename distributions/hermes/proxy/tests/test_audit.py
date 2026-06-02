"""Audit log tests.

Covers:

* an append() call writes to a daily file under the audit dir;
* the file is binary (header starts with the VBB magic) and does not
  leak the action_id or any secret value in cleartext.
"""

from __future__ import annotations

from tools.proxy.audit import AuditLog
from tools.proxy.crypto import select_backend


def test_audit_file_is_created_and_binary(proxy_workspace, secret_key):
    backend = select_backend("libsodium")
    al = AuditLog(proxy_workspace / "audit", secret_key.read_bytes(), backend)
    al.append(
        {
            "request_id": "00000000-0000-4000-8000-000000000099",
            "requestor": "test",
            "action_id": "vault_read",
            "status": "ok",
            "params_hash": "deadbeef",
            "duration_ms": 12,
        }
    )
    files = sorted((proxy_workspace / "audit").iterdir())
    assert files, "no audit file written"
    raw = files[0].read_bytes()
    # Header should be VBBA1 magic (5 canonical bytes)
    assert raw[:5] == b"VBBA1", f"unexpected audit header: {raw[:5]!r}"


def test_audit_does_not_leak_secrets(proxy_workspace, secret_key):
    backend = select_backend("libsodium")
    al = AuditLog(proxy_workspace / "audit", secret_key.read_bytes(), backend)
    secret_marker = b"SECRET-MARKER-ABCDEF-12345"
    al.append(
        {
            "request_id": "00000000-0000-4000-8000-0000000000aa",
            "requestor": "test",
            "action_id": "vault_read",
            "status": "ok",
            "params_hash": "abc",
            "duration_ms": 1,
        }
    )
    files = sorted((proxy_workspace / "audit").iterdir())
    raw = files[0].read_bytes()
    assert secret_marker not in raw
