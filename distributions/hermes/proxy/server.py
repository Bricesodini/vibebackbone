"""HTTP server for the privacy proxy POC.

The server uses :mod:`http.server` from the stdlib — no Flask, no
external HTTP framework. The request flow is:

1. Read up to ``config.payload.max_bytes`` of the body.
2. Verify HMAC + anti-replay (raw body).
3. Parse the JSON contract.
4. Look the action up in the whitelist.
5. Dispatch, write an audit entry, return the result.

Every error path returns a structured :class:`ProxyResponse` with
``status="error"`` and a stable ``code`` (see :mod:`tools.proxy.errors`).
The response body is always JSON.

The server also exposes a tiny ``/proxy/v1/health`` endpoint which is
unauthenticated (it returns server liveness, not data).
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable, Final

from . import actions as actions_mod
from . import audit as audit_mod
from . import config as config_mod
from . import contract, crypto, errors, hmac_auth, secret_store

LOG = logging.getLogger("vbb.proxy.server")

PATH_EXEC: Final[str] = "/proxy/v1/exec"
PATH_HEALTH: Final[str] = "/proxy/v1/health"


@dataclass
class ServerContext:
    """Bundle of services the HTTP handler needs per request.

    Kept as a class attribute on the handler factory so we don't pass
    a bag of globals through the handler.
    """

    config: config_mod.ProxyConfig
    hmac: hmac_auth.HmacVerifier
    actions: actions_mod.ActionDispatcher
    secret_store: secret_store.SecretStore
    audit: audit_mod.AuditLog
    backend: str


def make_handler(ctx: ServerContext) -> type[BaseHTTPRequestHandler]:
    """Factory that returns a :class:`BaseHTTPRequestHandler` subclass
    bound to ``ctx``.
    """

    class ProxyHTTPHandler(BaseHTTPRequestHandler):
        server_version = "VBBProxy/0.1"

        # Silence the default per-request stderr access log; the proxy
        # has its own structured logging.
        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
            return

        # ------------------------------------------------------------------
        # Routing
        # ------------------------------------------------------------------

        def do_GET(self) -> None:  # noqa: N802
            if self.path == PATH_HEALTH:
                self._handle_health()
                return
            self._send_error(errors.ProxyError(
                errors.E_NOT_FOUND, f"no such resource: {self.path}"
            ), action_id="<unknown>")

        def do_POST(self) -> None:  # noqa: N802
            if self.path == PATH_EXEC:
                self._handle_exec()
                return
            self._send_error(errors.ProxyError(
                errors.E_NOT_FOUND, f"no such resource: {self.path}"
            ), action_id="<unknown>")

        # ------------------------------------------------------------------
        # /proxy/v1/health
        # ------------------------------------------------------------------

        def _handle_health(self) -> None:
            try:
                body = json.dumps({
                    "status": "ok",
                    "contract_version": contract.CONTRACT_VERSION,
                    "actions": ctx.actions.list_actions(),
                    "crypto_backend": ctx.backend,
                }).encode("utf-8")
            except Exception as exc:  # pragma: no cover - defensive
                self._send_error(errors.ProxyError(
                    errors.E_HEALTH,
                    f"health response build failed: {exc}",
                ), action_id="<health>")
                return
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        # ------------------------------------------------------------------
        # /proxy/v1/exec
        # ------------------------------------------------------------------

        def _handle_exec(self) -> None:
            start = time.monotonic()
            request_id = self.headers.get(hmac_auth.HEADER_REQUEST_ID, "")
            # We log the *hash* of the body, not the body itself, to
            # never leak sensitive parameters in stdout/stderr.
            body = self._read_body()
            if isinstance(body, errors.ProxyError):
                self._send_error(body, action_id="<unknown>", request_id=request_id)
                return
            params_hash = crypto.sha256_hex(body)

            sig = self.headers.get(hmac_auth.HEADER_SIGNATURE)
            ts = self.headers.get(hmac_auth.HEADER_TIMESTAMP)
            try:
                ctx.hmac.verify(body, sig, ts)
            except errors.ProxyError as exc:
                self._audit(
                    request_id=request_id or "<missing>",
                    action_id="<unknown>",
                    status="hmac_failed",
                    params_hash=params_hash,
                    duration_ms=_ms(start),
                    error_code=exc.code,
                )
                self._send_error(exc, action_id="<unknown>", request_id=request_id)
                return

            try:
                payload = json.loads(body.decode("utf-8")) if body else {}
            except json.JSONDecodeError as exc:
                err = errors.ProxyError(
                    errors.E_PAYLOAD_INVALID, f"invalid JSON body: {exc}"
                )
                self._send_error(err, action_id="<unknown>", request_id=request_id)
                return

            try:
                req = contract.parse_request(payload)
            except errors.ProxyError as exc:
                self._audit(
                    request_id=request_id or "<missing>",
                    action_id=str(payload.get("action_id", "<unknown>")) if isinstance(payload, dict) else "<unknown>",
                    status="contract_invalid",
                    params_hash=params_hash,
                    duration_ms=_ms(start),
                    error_code=exc.code,
                )
                self._send_error(exc, action_id="<unknown>", request_id=request_id)
                return

            # Whitelist check (defence in depth — the dispatcher also
            # enforces this, but we audit before dispatching).
            if not ctx.actions.is_allowed(req.action_id):
                err = errors.ProxyError(
                    errors.E_UNDECLARED,
                    f"action {req.action_id!r} is not declared in actions.yaml",
                )
                self._audit(
                    request_id=req.request_id,
                    requestor=req.requestor,
                    action_id=req.action_id,
                    status="undeclared",
                    params_hash=params_hash,
                    duration_ms=_ms(start),
                    error_code=err.code,
                )
                self._send_error(err, action_id=req.action_id, request_id=req.request_id)
                return

            try:
                result = ctx.actions.dispatch(
                    req.action_id, req.params, dry_run=req.dry_run
                )
            except errors.ProxyError as exc:
                self._audit(
                    request_id=req.request_id,
                    requestor=req.requestor,
                    action_id=req.action_id,
                    status="dispatch_error",
                    params_hash=params_hash,
                    duration_ms=_ms(start),
                    error_code=exc.code,
                )
                self._send_error(exc, action_id=req.action_id, request_id=req.request_id)
                return

            response = contract.make_ok_response(
                request_id=req.request_id,
                action_id=req.action_id,
                result=result.payload,
            )
            self._audit(
                request_id=req.request_id,
                requestor=req.requestor,
                action_id=req.action_id,
                status="ok",
                params_hash=params_hash,
                duration_ms=_ms(start),
                error_code=None,
            )
            self._write_json(HTTPStatus.OK, response.to_dict())

        # ------------------------------------------------------------------
        # I/O helpers
        # ------------------------------------------------------------------

        def _read_body(self) -> bytes | errors.ProxyError:
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                return errors.ProxyError(
                    errors.E_PAYLOAD_INVALID,
                    "Content-Length is not an integer",
                )
            if length < 0:
                return errors.ProxyError(
                    errors.E_PAYLOAD_INVALID,
                    "Content-Length is negative",
                )
            if length > ctx.config.payload.max_bytes:
                return errors.ProxyError(
                    errors.E_PAYLOAD_TOO_LARGE,
                    f"body length {length} exceeds max {ctx.config.payload.max_bytes}",
                )
            if length == 0:
                return b""
            try:
                return self.rfile.read(length)
            except OSError as exc:
                return errors.ProxyError(
                    errors.E_PAYLOAD_INVALID,
                    f"failed to read body: {exc}",
                )

        def _write_json(self, status: HTTPStatus, body: dict[str, Any]) -> None:
            raw = json.dumps(body, sort_keys=True).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def _send_error(
            self,
            err: errors.ProxyError,
            action_id: str,
            request_id: str = "",
        ) -> None:
            response = contract.make_error_response(
                request_id=request_id or "",
                action_id=action_id,
                err=err,
            )
            self._write_json(HTTPStatus(err.http_status), response.to_dict())

        def _audit(
            self,
            request_id: str,
            action_id: str,
            status: str,
            params_hash: str,
            duration_ms: int,
            requestor: str = "",
            error_code: str | None = None,
        ) -> None:
            entry: dict[str, Any] = {
                "request_id": request_id or "<missing>",
                "requestor": requestor or "<unknown>",
                "action_id": action_id,
                "status": status,
                "params_hash": params_hash,
                "duration_ms": duration_ms,
            }
            if error_code:
                entry["error_code"] = error_code
            try:
                ctx.audit.append(entry)
            except Exception:  # pragma: no cover - never let audit kill the response
                LOG.exception("audit append failed")

    return ProxyHTTPHandler


def _ms(start: float) -> int:
    return int((time.monotonic() - start) * 1000)


# ---------------------------------------------------------------------------
# Boot helper
# ---------------------------------------------------------------------------

def build_context(config: config_mod.ProxyConfig) -> ServerContext:
    """Wire the runtime services together.

    This is the single place that knows how to compose the proxy; the
    HTTP handler is intentionally unaware of these dependencies.
    """
    hmac_verifier = hmac_auth.HmacVerifier.from_key_file(
        key_path=config.hmac.key_path,
        timestamp_skew_seconds=config.hmac.timestamp_skew_seconds,
    )
    actions_specs = config_mod.load_actions(config.actions_path)
    dispatcher = actions_mod.ActionDispatcher(
        actions=actions_specs,
        fixtures_dir=config.fixtures.vault_read_response_path.parent,
        vault_read_response_path=config.fixtures.vault_read_response_path,
    )
    # Restrict the whitelist to the canonical allow-list at the POC
    # level. The whitelist is the union of (a) what's declared in
    # actions.yaml and (b) the hard-coded ALLOWED_ACTIONS tuple. We
    # filter so that the dispatcher can never execute something
    # outside the canonical set.
    filtered = {k: v for k, v in actions_specs.items() if k in actions_mod.ALLOWED_ACTIONS}
    if not filtered:
        raise errors.ProxyError(
            errors.E_BOOT_CONFIG,
            f"no actions from {config.actions_path} match the canonical "
            f"ALLOWED_ACTIONS={actions_mod.ALLOWED_ACTIONS}",
        )
    dispatcher = actions_mod.ActionDispatcher(
        actions=filtered,
        fixtures_dir=config.fixtures.vault_read_response_path.parent,
        vault_read_response_path=config.fixtures.vault_read_response_path,
    )

    secret_key = secret_store.load_or_create_key(config.secrets.key_path)
    secrets = secret_store.SecretStore(
        store_path=config.secrets.store_path,
        key=secret_key,
        backend=crypto.select_backend(config.crypto.backend),
    )
    audit = audit_mod.AuditLog(
        dir_path=config.audit.dir,
        key=secret_key,
        backend=crypto.select_backend(config.crypto.backend),
        file_prefix=config.audit.file_prefix,
        file_suffix=config.audit.file_suffix,
    )
    backend = crypto.select_backend(config.crypto.backend)
    LOG.info(
        "proxy: build_context ok actions=%s backend=%s hmac_fp=%s",
        sorted(filtered.keys()), backend, hmac_verifier.key_fingerprint(),
    )
    return ServerContext(
        config=config,
        hmac=hmac_verifier,
        actions=dispatcher,
        secret_store=secrets,
        audit=audit,
        backend=backend,
    )


def serve(
    config: config_mod.ProxyConfig,
    context: ServerContext,
) -> ThreadingHTTPServer:
    """Construct (but do not start) the HTTP server.

    Use :meth:`ThreadingHTTPServer.serve_forever` to actually start
    serving. The function returns the server so tests can call
    ``server.shutdown()`` deterministically.
    """
    handler = make_handler(context)
    server = ThreadingHTTPServer((config.host, config.port), handler)
    return server


__all__ = [
    "ServerContext",
    "make_handler",
    "build_context",
    "serve",
    "PATH_EXEC",
    "PATH_HEALTH",
]
