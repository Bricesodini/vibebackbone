"""HMAC verification tests.

Covers the four core security paths:

* a correctly signed body is accepted;
* a missing ``X-Proxy-Signature`` is refused with E_HMAC_MISSING;
* a body that does not match the signature is refused with E_HMAC_INVALID;
* a timestamp outside the skew window is refused with E_REPLAY_DETECTED.
"""

from __future__ import annotations

import hmac
import hashlib
import json
import time
from pathlib import Path

import pytest

from tools.proxy.errors import ProxyError
from tools.proxy.hmac_auth import HmacVerifier


def _signed_body(hmac_key: Path, **overrides) -> tuple[bytes, str]:
    payload = {
        "contract_version": "1.0.0",
        "request_id": "00000000-0000-4000-8000-000000000001",
        "action_id": "vault_read",
        "params": {"secret_id": "fixture"},
        "requestor": "test",
    }
    payload.update(overrides)
    body = json.dumps(payload, separators=(",", ":")).encode()
    key = hmac_key.read_bytes()
    sig = hmac.new(key, body, hashlib.sha256).hexdigest()
    return body, sig


def _verifier(hmac_key: Path, skew: int = 300) -> HmacVerifier:
    return HmacVerifier(key=hmac_key.read_bytes(), timestamp_skew_seconds=skew)


def test_valid_signature_is_accepted(hmac_key):
    verifier = _verifier(hmac_key)
    body, sig = _signed_body(hmac_key)
    verifier.verify(body=body, signature=sig, timestamp=str(int(time.time())))


def test_missing_signature_is_refused(hmac_key):
    verifier = _verifier(hmac_key)
    with pytest.raises(ProxyError) as ei:
        verifier.verify(body=b'{}', signature="", timestamp=str(int(time.time())))
    assert ei.value.code == "E_HMAC_MISSING"


def test_wrong_signature_is_refused(hmac_key):
    verifier = _verifier(hmac_key)
    body, _ = _signed_body(hmac_key)
    with pytest.raises(ProxyError) as ei:
        verifier.verify(body=body, signature="a" * 64, timestamp=str(int(time.time())))
    assert ei.value.code == "E_HMAC_INVALID"


def test_stale_timestamp_is_refused(hmac_key):
    verifier = _verifier(hmac_key, skew=300)
    body, sig = _signed_body(hmac_key)
    stale = str(int(time.time()) - 1000)
    with pytest.raises(ProxyError) as ei:
        verifier.verify(body=body, signature=sig, timestamp=stale)
    assert ei.value.code == "E_REPLAY_DETECTED"
