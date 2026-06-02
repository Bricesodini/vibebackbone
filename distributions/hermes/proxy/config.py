"""Configuration loader for the privacy proxy.

The proxy reads two YAML files at boot:

* ``~/.hermes/proxy/config.yaml`` — runtime configuration
  (host, port, model, paths, crypto backend, log level).
* ``~/.hermes/proxy/actions.yaml`` — declarative action whitelist
  (see ADR 0009).

Both files are loaded with PyYAML and validated against a tiny schema
implemented in plain Python (Pydantic is not used here to keep the POC
boot path light). Invalid configurations cause the daemon to refuse to
start — there is no implicit fallback.
"""

from __future__ import annotations

import logging
import os
import stat
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final

import yaml

from . import errors

LOG = logging.getLogger("vbb.proxy.config")

# Default values match ``config.example.yaml`` shipped with the POC.
DEFAULT_CONFIG: Final[dict[str, Any]] = {
    "host": "127.0.0.1",
    "port": 9911,
    "model": "stub",  # the POC does not run an LLM (see ADR 0006 D1).
    "log_level": "INFO",
    "hmac": {
        "key_path": "~/.hermes/proxy/hmac.key",
        "timestamp_skew_seconds": 300,
    },
    "secrets": {
        "store_path": "~/.hermes/proxy/secrets.enc",
        "key_path": "~/.hermes/proxy/secrets.key",
    },
    "audit": {
        "dir": "~/.hermes/proxy/audit",
        "file_prefix": "audit-",
        "file_suffix": ".log",
    },
    "actions_path": "~/.hermes/proxy/actions.yaml",
    "fixtures": {
        "vault_read_response_path": "tools/proxy/fixtures/vault_read_response.json",
    },
    "payload": {
        "max_bytes": 65536,  # 64 KB hard cap (ADR 0012).
        "soft_bytes": 4096,  # 4 KB nominal cap.
    },
    "crypto": {
        "backend": "libsodium",  # "libsodium" or "cryptography"
    },
}

DEFAULT_ACTIONS: Final[dict[str, Any]] = {
    "actions": [
        {
            "id": "vault_read",
            "description": "Read a secret from the encrypted store (stub).",
            "risk_level": "low",
            "mode": "live",  # dry-run | live
            "permissions": ["read"],
            "required_params": ["secret_id"],
            "stub": True,
        }
    ]
}


def _expand(path: str | os.PathLike[str]) -> Path:
    return Path(os.path.expanduser(os.path.expandvars(str(path))))


@dataclass(frozen=True)
class HmacConfig:
    key_path: Path
    timestamp_skew_seconds: int


@dataclass(frozen=True)
class SecretsConfig:
    store_path: Path
    key_path: Path


@dataclass(frozen=True)
class AuditConfig:
    dir: Path
    file_prefix: str
    file_suffix: str


@dataclass(frozen=True)
class FixturesConfig:
    vault_read_response_path: Path


@dataclass(frozen=True)
class PayloadConfig:
    max_bytes: int
    soft_bytes: int


@dataclass(frozen=True)
class CryptoConfig:
    backend: str


@dataclass(frozen=True)
class ProxyConfig:
    host: str
    port: int
    model: str
    log_level: str
    hmac: HmacConfig
    secrets: SecretsConfig
    audit: AuditConfig
    actions_path: Path
    fixtures: FixturesConfig
    payload: PayloadConfig
    crypto: CryptoConfig
    raw: dict[str, Any] = field(repr=False)

    def base_dir(self) -> Path:
        """Return the canonical ``~/.hermes/proxy/`` directory."""
        return self.secrets.key_path.parent


def _require(mapping: dict[str, Any], key: str, ctx: str) -> Any:
    if key not in mapping:
        raise errors.ProxyError(
            errors.E_BOOT_CONFIG,
            f"missing key {key!r} in {ctx}",
        )
    return mapping[key]


def load_config(path: str | os.PathLike[str]) -> ProxyConfig:
    """Load and validate the proxy config from ``path``.

    Missing files cause a :class:`ProxyError` with ``E_BOOT_CONFIG``; the
    daemon must refuse to start in that case.
    """
    p = _expand(path)
    if not p.exists():
        raise errors.ProxyError(
            errors.E_BOOT_CONFIG,
            f"config file not found: {p}",
        )
    with p.open("rb") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise errors.ProxyError(
            errors.E_BOOT_CONFIG,
            f"config root must be a mapping, got {type(data).__name__}",
        )
    # Merge with defaults so the user can omit optional sections.
    merged: dict[str, Any] = {**DEFAULT_CONFIG, **data}
    # Re-merge nested dicts shallowly.
    for k in ("hmac", "secrets", "audit", "fixtures", "payload", "crypto"):
        if k in data and isinstance(data[k], dict):
            merged[k] = {**DEFAULT_CONFIG[k], **data[k]}

    try:
        hmac_cfg = HmacConfig(
            key_path=_expand(_require(merged["hmac"], "key_path", "hmac")),
            timestamp_skew_seconds=int(
                _require(merged["hmac"], "timestamp_skew_seconds", "hmac")
            ),
        )
        secrets_cfg = SecretsConfig(
            store_path=_expand(_require(merged["secrets"], "store_path", "secrets")),
            key_path=_expand(_require(merged["secrets"], "key_path", "secrets")),
        )
        audit_cfg = AuditConfig(
            dir=_expand(_require(merged["audit"], "dir", "audit")),
            file_prefix=str(_require(merged["audit"], "file_prefix", "audit")),
            file_suffix=str(_require(merged["audit"], "file_suffix", "audit")),
        )
        actions_path = _expand(
            _require(merged, "actions_path", "root"),
        )
        fixtures_cfg = FixturesConfig(
            vault_read_response_path=_expand(
                _require(merged["fixtures"], "vault_read_response_path", "fixtures")
            ),
        )
        payload_cfg = PayloadConfig(
            max_bytes=int(_require(merged["payload"], "max_bytes", "payload")),
            soft_bytes=int(_require(merged["payload"], "soft_bytes", "payload")),
        )
        crypto_cfg = CryptoConfig(
            backend=str(_require(merged["crypto"], "backend", "crypto")),
        )
        return ProxyConfig(
            host=str(merged["host"]),
            port=int(merged["port"]),
            model=str(merged["model"]),
            log_level=str(merged["log_level"]).upper(),
            hmac=hmac_cfg,
            secrets=secrets_cfg,
            audit=audit_cfg,
            actions_path=actions_path,
            fixtures=fixtures_cfg,
            payload=payload_cfg,
            crypto=crypto_cfg,
            raw=merged,
        )
    except errors.ProxyError:
        raise
    except (KeyError, ValueError, TypeError) as exc:
        raise errors.ProxyError(
            errors.E_BOOT_CONFIG,
            f"invalid config: {exc}",
        ) from exc


@dataclass(frozen=True)
class ActionSpec:
    id: str
    description: str
    risk_level: str
    mode: str  # dry-run | live
    permissions: tuple[str, ...]
    required_params: tuple[str, ...]
    stub: bool


def load_actions(path: str | os.PathLike[str]) -> dict[str, ActionSpec]:
    """Load the action whitelist from ``path``.

    Returns a dict keyed by action id. Refuses to start if the file is
    missing — there is no implicit fallback (per ADR 0010).
    """
    p = _expand(path)
    if not p.exists():
        raise errors.ProxyError(
            errors.E_BOOT_CONFIG,
            f"actions file not found: {p}",
        )
    with p.open("rb") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict) or "actions" not in data:
        raise errors.ProxyError(
            errors.E_BOOT_CONFIG,
            f"actions file must define an 'actions' list: {p}",
        )
    actions_raw = data["actions"]
    if not isinstance(actions_raw, list):
        raise errors.ProxyError(
            errors.E_BOOT_CONFIG,
            f"actions must be a list, got {type(actions_raw).__name__}",
        )
    out: dict[str, ActionSpec] = {}
    for entry in actions_raw:
        if not isinstance(entry, dict):
            raise errors.ProxyError(
                errors.E_BOOT_CONFIG,
                "each action entry must be a mapping",
            )
        try:
            spec = ActionSpec(
                id=str(entry["id"]),
                description=str(entry.get("description", "")),
                risk_level=str(entry.get("risk_level", "low")),
                mode=str(entry.get("mode", "live")),
                permissions=tuple(entry.get("permissions", ())),
                required_params=tuple(entry.get("required_params", ())),
                stub=bool(entry.get("stub", False)),
            )
        except KeyError as exc:
            raise errors.ProxyError(
                errors.E_BOOT_CONFIG,
                f"action missing required field: {exc}",
            ) from exc
        if spec.id in out:
            raise errors.ProxyError(
                errors.E_BOOT_CONFIG,
                f"duplicate action id: {spec.id}",
            )
        out[spec.id] = spec
    return out


# ---------------------------------------------------------------------------
# Filesystem permission helpers
# ---------------------------------------------------------------------------

def ensure_dir_secure(path: Path, mode: int = 0o700) -> None:
    """Create ``path`` (and parents) with the requested mode.

    Refuses to reuse a directory that already exists with looser
    permissions — this is a defence-in-depth check called out in the
    POC's security contract.
    """
    path = Path(path)
    if path.exists():
        if not path.is_dir():
            raise errors.ProxyError(
                errors.E_BOOT_CONFIG,
                f"path exists and is not a directory: {path}",
            )
        cur = stat.S_IMODE(path.stat().st_mode)
        if cur & 0o077:
            raise errors.ProxyError(
                errors.E_PERMISSION,
                f"directory {path} is group/world accessible "
                f"(mode=0o{cur:o}); refusing to start",
            )
        return
    path.mkdir(parents=True, mode=mode)
    # mkdir is affected by umask; force the requested mode.
    os.chmod(path, mode)


def ensure_file_secure(path: Path, mode: int = 0o600) -> None:
    """Tight permissions on a single file. Creates the file if missing."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        cur = stat.S_IMODE(path.stat().st_mode)
        if cur & 0o077:
            raise errors.ProxyError(
                errors.E_PERMISSION,
                f"file {path} is group/world accessible "
                f"(mode=0o{cur:o}); refusing to start",
            )
        return
    fd = os.open(str(path), os.O_CREAT | os.O_WRONLY | os.O_TRUNC, mode)
    os.close(fd)
    os.chmod(path, mode)
