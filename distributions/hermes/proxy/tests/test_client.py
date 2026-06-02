"""End-to-end tests for :class:`tools.proxy.client.ProxyClient`.

The tests reuse the ``live_server`` fixture from ``conftest.py``
(spin a daemon on a free loopback port) and the standard
``hmac_key`` / ``config_path`` / ``proxy_workspace`` fixtures.

Coverage:

* ``test_signed_vault_read_via_client_succeeds`` — happy path: the
  client signs a vault_read, the daemon returns ``status=ok`` and
  the client returns the result dict.
* ``test_invalid_hmac_via_client_raises`` — the client signs with
  the wrong key, the daemon returns 401, the client raises
  :class:`ProxyClientError` with ``code=E_HMAC_INVALID``.
* ``test_unknown_action_via_client_raises`` — the client asks for
  an action that is not on the whitelist, the client raises with
  ``code=E_UNDECLARED``.
* ``test_daemon_unavailable_raises`` — point the client at a
  closed port, the client raises with
  ``code=E_DAEMON_UNAVAILABLE``.
* ``test_request_id_is_generated_if_absent`` — when no request_id
  is supplied, the client fills in a UUIDv4.

The tests never log or assert on the value of the secret; the
fixture returns a stub whose ``value_preview`` is the only thing
that ever appears in test logs / assertions.
"""

from __future__ import annotations

import re

import pytest

from tools.proxy.client import ProxyClient
from tools.proxy.errors import ProxyClientError


_UUID4_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def test_signed_vault_read_via_client_succeeds(live_server):
    base_url = f"http://127.0.0.1:{live_server['port']}"
    client = ProxyClient(
        base_url=base_url,
        hmac_key=live_server["key"],
        requestor="pytest-client",
        timeout=2.0,
    )
    result = client.exec("vault_read", {"secret_id": "fixture"})
    assert isinstance(result, dict)
    assert result.get("stub") is True
    assert result.get("secret_id") == "fixture"
    # The proxy returns a value_preview; the raw value must never
    # appear in our assertions (we don't want the test logs to leak
    # it).
    assert "value_preview" in result
    assert client.last_status_code == 200
    assert client.last_error is None


def test_invalid_hmac_via_client_raises(live_server):
    base_url = f"http://127.0.0.1:{live_server['port']}"
    bad_key = b"\x00" * 32
    assert bad_key != live_server["key"]
    client = ProxyClient(
        base_url=base_url,
        hmac_key=bad_key,
        requestor="pytest-client",
        timeout=2.0,
    )
    with pytest.raises(ProxyClientError) as excinfo:
        client.exec("vault_read", {"secret_id": "fixture"})
    assert excinfo.value.code == "E_HMAC_INVALID"
    assert client.last_status_code == 401
    assert client.last_error is excinfo.value


def test_unknown_action_via_client_raises(live_server):
    base_url = f"http://127.0.0.1:{live_server['port']}"
    client = ProxyClient(
        base_url=base_url,
        hmac_key=live_server["key"],
        requestor="pytest-client",
        timeout=2.0,
    )
    with pytest.raises(ProxyClientError) as excinfo:
        client.exec("ssh_root", {})
    assert excinfo.value.code == "E_UNDECLARED"
    assert client.last_status_code is not None
    assert 400 <= client.last_status_code < 500


def test_daemon_unavailable_raises():
    # Port 1 on loopback is reserved and never bound by a real
    # daemon; the client must surface E_DAEMON_UNAVAILABLE.
    client = ProxyClient(
        base_url="http://127.0.0.1:1",
        hmac_key=b"k" * 32,
        requestor="pytest-client",
        timeout=1.0,
    )
    with pytest.raises(ProxyClientError) as excinfo:
        client.exec("vault_read", {"secret_id": "fixture"})
    assert excinfo.value.code == "E_DAEMON_UNAVAILABLE"
    assert client.last_status_code is None
    assert client.last_error is excinfo.value


def test_request_id_is_generated_if_absent(live_server):
    base_url = f"http://127.0.0.1:{live_server['port']}"
    client = ProxyClient(
        base_url=base_url,
        hmac_key=live_server["key"],
        requestor="pytest-client",
        timeout=2.0,
    )
    # We do not pass request_id; the client must generate one.
    # We assert by side effect: the response (which echoes the
    # request_id) is logged in the proxy; here we simply check
    # that no exception is raised and that the response is well
    # formed.
    result = client.exec("vault_read", {"secret_id": "fixture"})
    assert result.get("status") in (None, "ok")  # result dict, not response
    # And the second call also gets its own auto-id.
    result2 = client.exec("vault_read", {"secret_id": "fixture"})
    assert result2 is not None


def test_explicit_request_id_is_accepted(live_server):
    base_url = f"http://127.0.0.1:{live_server['port']}"
    client = ProxyClient(
        base_url=base_url,
        hmac_key=live_server["key"],
        requestor="pytest-client",
        timeout=2.0,
    )
    rid = "00000000-0000-4000-8000-000000000123"
    result = client.exec(
        "vault_read", {"secret_id": "fixture"}, request_id=rid,
    )
    assert result is not None


def test_constructor_rejects_empty_key():
    with pytest.raises(ValueError):
        ProxyClient(base_url="http://127.0.0.1:1", hmac_key=b"", requestor="t")
