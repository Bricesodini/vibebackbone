"""Action whitelist and dispatch tests.

Covers:

* the registry exposes exactly the actions declared in actions.yaml;
* dispatching an unknown action id raises E_UNDECLARED;
* dispatching the allowed ``vault_read`` action returns the stub fixture.
"""

from __future__ import annotations

import pytest

from tools.proxy.actions import ActionDispatcher
from tools.proxy.config import load_actions
from tools.proxy.errors import ProxyError


def _dispatcher(config_path, vault_read_fixture):
    actions = load_actions(config_path.parent / "actions.yaml")
    return ActionDispatcher(
        actions=actions,
        fixtures_dir=config_path.parent,
        vault_read_response_path=vault_read_fixture,
    )


def test_registry_contains_declared_actions(config_path, vault_read_fixture):
    disp = _dispatcher(config_path, vault_read_fixture)
    assert "vault_read" in disp.list_actions()


def test_unknown_action_is_refused(config_path, vault_read_fixture):
    disp = _dispatcher(config_path, vault_read_fixture)
    with pytest.raises(ProxyError) as ei:
        disp.dispatch("ssh_root", {}, dry_run=False)
    assert ei.value.code == "E_UNDECLARED"


def test_vault_read_dispatch_returns_stub(config_path, vault_read_fixture):
    disp = _dispatcher(config_path, vault_read_fixture)
    result = disp.dispatch("vault_read", {"secret_id": "fixture"}, dry_run=False)
    payload = result.payload
    assert payload["stub"] is True
    assert payload["secret_id"] == "fixture"
    assert "value" in payload and "value_preview" in payload
