"""Request / response contract for the privacy proxy POC.

The contract is a strict, versioned JSON schema defined in ADR 0012.
This module encodes the rules in pure Python dataclasses + manual
validation. Pydantic is intentionally NOT used at runtime to keep the
boot path small and the validation logic obvious.

Validation rules:

* ``contract_version`` must equal the constant :data:`CONTRACT_VERSION`
  (semver ``"1.0.0"``). Any other value (including missing) is refused
  with :data:`E_CONTRACT_VERSION`.
* ``request_id`` must be a UUIDv4 string. Any other value (including
  missing) is refused with :data:`E_PAYLOAD_INVALID`.
* All top-level keys must be ``snake_case`` (``[a-z0-9_]+``). camelCase
  or kebab-case is refused with :data:`E_PAYLOAD_INVALID`. This applies
  to the top-level keys only (deeper validation is the responsibility
  of each action, which is itself read-only at the POC level).
* ``action_id`` must be present and a non-empty string.
* ``params`` is an optional dict. The body size is checked separately
  by the HTTP layer using :data:`tools.proxy.config.PayloadConfig`.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Final

from . import errors

CONTRACT_VERSION: Final[str] = "1.0.0"

_SNAKE_CASE_RE: Final = re.compile(r"^[a-z0-9_]+$")
_UUID4_RE: Final = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ProxyRequest:
    contract_version: str
    request_id: str
    requestor: str
    action_id: str
    params: dict[str, Any] = field(default_factory=dict)
    dry_run: bool = False

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        # Keep dict[str,Any] so JSON serialisation is stable.
        return d


@dataclass(frozen=True)
class ProxyResponse:
    contract_version: str
    request_id: str
    status: str  # "ok" | "error"
    action_id: str
    result: dict[str, Any] = field(default_factory=dict)
    error: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        # Drop None error to keep wire format compact.
        if d.get("error") is None:
            d.pop("error", None)
        return d


def _ensure_snake_case_keys(d: dict[str, Any], ctx: str) -> None:
    for k in d.keys():
        if not _SNAKE_CASE_RE.match(str(k)):
            raise errors.ProxyError(
                errors.E_PAYLOAD_INVALID,
                f"non-snake_case key in {ctx}: {k!r}",
            )


def parse_request(payload: Any) -> ProxyRequest:
    """Parse and validate a raw JSON payload into a :class:`ProxyRequest`.

    Raises :class:`ProxyError` on any validation failure. The error code
    reflects the most specific failure detected (contract version,
    request id, etc.).
    """
    if not isinstance(payload, dict):
        raise errors.ProxyError(
            errors.E_PAYLOAD_INVALID,
            "request body must be a JSON object",
        )

    # Top-level keys must be snake_case.
    _ensure_snake_case_keys(payload, "request root")

    # contract_version: required, exact match.
    cv = payload.get("contract_version")
    if not isinstance(cv, str):
        raise errors.ProxyError(
            errors.E_CONTRACT_VERSION,
            "contract_version is required and must be a string",
        )
    if cv != CONTRACT_VERSION:
        raise errors.ProxyError(
            errors.E_CONTRACT_VERSION,
            f"unsupported contract_version {cv!r}; expected {CONTRACT_VERSION!r}",
        )

    # request_id: required, UUIDv4.
    rid = payload.get("request_id")
    if not isinstance(rid, str) or not _UUID4_RE.match(rid):
        raise errors.ProxyError(
            errors.E_PAYLOAD_INVALID,
            "request_id is required and must be a UUIDv4",
        )

    # requestor: required, non-empty string.
    requestor = payload.get("requestor")
    if not isinstance(requestor, str) or not requestor:
        raise errors.ProxyError(
            errors.E_PAYLOAD_INVALID,
            "requestor is required and must be a non-empty string",
        )

    # action_id: required, non-empty string.
    action_id = payload.get("action_id")
    if not isinstance(action_id, str) or not action_id:
        raise errors.ProxyError(
            errors.E_PAYLOAD_INVALID,
            "action_id is required and must be a non-empty string",
        )

    # params: optional dict with snake_case keys.
    params = payload.get("params", {})
    if params is None:
        params = {}
    if not isinstance(params, dict):
        raise errors.ProxyError(
            errors.E_PAYLOAD_INVALID,
            "params must be an object",
        )
    _ensure_snake_case_keys(params, "params")

    # dry_run: optional bool.
    dry_run = payload.get("dry_run", False)
    if not isinstance(dry_run, bool):
        raise errors.ProxyError(
            errors.E_PAYLOAD_INVALID,
            "dry_run must be a boolean",
        )

    return ProxyRequest(
        contract_version=cv,
        request_id=rid,
        requestor=requestor,
        action_id=action_id,
        params=params,
        dry_run=dry_run,
    )


def make_ok_response(
    request_id: str,
    action_id: str,
    result: dict[str, Any],
) -> ProxyResponse:
    return ProxyResponse(
        contract_version=CONTRACT_VERSION,
        request_id=request_id,
        status="ok",
        action_id=action_id,
        result=result,
    )


def make_error_response(
    request_id: str,
    action_id: str,
    err: errors.ProxyError,
) -> ProxyResponse:
    return ProxyResponse(
        contract_version=CONTRACT_VERSION,
        request_id=request_id,
        status="error",
        action_id=action_id,
        result={},
        error=err.to_dict(),
    )


__all__ = [
    "CONTRACT_VERSION",
    "ProxyRequest",
    "ProxyResponse",
    "parse_request",
    "make_ok_response",
    "make_error_response",
]
