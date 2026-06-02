"""pytest fixtures shared by the privacy proxy tests.

These fixtures are local to the proxy package — they do not depend on
any other vibebackbone tooling. They build an in-memory copy of the
proxy state (config, HMAC key, secrets store, audit log) in a tmp dir
and expose a :class:`ServerContext` ready to be bound to a
:class:`ThreadingHTTPServer`.

The intent is that each test starts from a clean filesystem and never
touches ``~/.hermes/proxy/`` directly.
"""
