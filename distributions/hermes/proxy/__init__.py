"""Vibebackbone privacy proxy POC.

This package implements the local-first privacy proxy described in ADRs
0006-0012. The POC exposes a single HTTP endpoint
(``POST /proxy/v1/exec``) on ``127.0.0.1`` and accepts exactly one
action id: ``vault_read``.

The package is intentionally small. Adding a new action in V2 is a
matter of:

1. adding a new entry to ``actions.yaml`` (whitelist) ;
2. implementing a dispatch branch in :mod:`tools.proxy.actions` ;
3. updating the canonical :data:`tools.proxy.actions.ALLOWED_ACTIONS`
   tuple.

No other module of the proxy needs to change.
"""

from __future__ import annotations

__all__ = ["__version__"]

__version__ = "0.1.0"
