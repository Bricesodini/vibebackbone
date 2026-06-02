"""Action whitelist and dispatch for the privacy proxy POC.

The action whitelist is loaded from ``actions.yaml`` at boot. The
proxy **only** runs actions whose id appears in the whitelist. There is
no fallback: a missing or unknown action id is refused with
:data:`E_UNDECLARED` (the canonical "action not declared" code called
out in ADR 0010).

The POC implements exactly one action: ``vault_read``. It is read-only
and stub-backed by a fixture file. The fixture is the *only* thing the
proxy ever returns for this action; we never read the real keychain or
make a network call. This is the only sensible posture for a POC and
is exactly the scope locked by the brief.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from . import errors

LOG = logging.getLogger("vbb.proxy.actions")

# The single action id allowed at the POC level. Hard-coded to
# guarantee a constant, well-known boundary.
ALLOWED_ACTIONS: Final[tuple[str, ...]] = ("vault_read",)


@dataclass(frozen=True)
class ActionResult:
    """The materialised result of an action execution.

    The :attr:`payload` is a JSON-serialisable dict that the server
    wraps into a :class:`~tools.proxy.contract.ProxyResponse`.
    """

    payload: dict[str, Any]
    secret_id_used: str | None = None


class ActionDispatcher:
    """Routes a validated :class:`ProxyRequest` to the matching action.

    The dispatcher is the only place where action-specific code lives;
    everything else in the proxy is action-agnostic. This is what makes
    it possible (in V2) to add new actions without touching the HTTP
    layer, the HMAC layer or the audit layer.
    """

    def __init__(
        self,
        actions: dict[str, Any],  # dict[str, ActionSpec] (avoiding import cycle)
        fixtures_dir: Path,
        vault_read_response_path: Path,
    ) -> None:
        self._actions = actions
        self._vault_read_response_path = Path(vault_read_response_path)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def is_allowed(self, action_id: str) -> bool:
        return action_id in self._actions

    def list_actions(self) -> list[str]:
        return list(self._actions.keys())

    def dispatch(
        self,
        action_id: str,
        params: dict[str, Any],
        dry_run: bool,
    ) -> ActionResult:
        if not self.is_allowed(action_id):
            raise errors.ProxyError(
                errors.E_UNDECLARED,
                f"action {action_id!r} is not declared in actions.yaml",
            )
        spec = self._actions[action_id]
        # Defensive: the spec must declare its required params.
        for required in spec.required_params:
            if required not in params:
                raise errors.ProxyError(
                    errors.E_PAYLOAD_INVALID,
                    f"action {action_id!r} requires param {required!r}",
                )

        if action_id == "vault_read":
            return self._vault_read(params, dry_run=dry_run)
        # Defence in depth: even if the whitelist were tampered with,
        # we still refuse to dispatch unknown implementations.
        raise errors.ProxyError(
            errors.E_UNDECLARED,
            f"no implementation registered for action {action_id!r}",
        )

    # ------------------------------------------------------------------
    # vault_read (stub)
    # ------------------------------------------------------------------

    def _vault_read(
        self,
        params: dict[str, Any],
        dry_run: bool,
    ) -> ActionResult:
        secret_id = params.get("secret_id")
        if not isinstance(secret_id, str) or not secret_id:
            raise errors.ProxyError(
                errors.E_PAYLOAD_INVALID,
                "vault_read requires a non-empty 'secret_id' string",
            )
        # Always load the fixture, even on dry-run, so the caller can
        # inspect what *would* have been returned. The fixture never
        # contains a real secret value; it is a controlled mock.
        payload = self._load_fixture()
        LOG.info(
            "vault_read: dispatch secret_id=%s dry_run=%s",
            secret_id, dry_run,
        )
        return ActionResult(
            payload={
                "secret_id": secret_id,
                "stub": True,
                "value_preview": payload.get("value_preview", ""),
                "value": payload.get("value", ""),  # fixture-controlled mock
                "dry_run": dry_run,
            },
            secret_id_used=secret_id,
        )

    def _load_fixture(self) -> dict[str, Any]:
        p = self._vault_read_response_path
        if not p.exists():
            raise errors.ProxyError(
                errors.E_BOOT_CONFIG,
                f"vault_read fixture missing: {p}",
            )
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise errors.ProxyError(
                errors.E_BOOT_CONFIG,
                f"vault_read fixture is not valid JSON: {p} ({exc})",
            ) from exc
        if not isinstance(data, dict):
            raise errors.ProxyError(
                errors.E_BOOT_CONFIG,
                f"vault_read fixture must be a JSON object: {p}",
            )
        return data


__all__ = [
    "ActionDispatcher",
    "ActionResult",
    "ALLOWED_ACTIONS",
]
