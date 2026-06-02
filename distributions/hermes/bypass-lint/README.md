# vbb-bypass-lint

**v0.1** — Anti-bypass linter for the Vibebackbone confidentiality proxy.
Reference: [ADR 0011 §3 Règle 1](../../../docs/adr/0011-proxy-bypass-prevention.md).

The linter scans the Vibebackbone codebase for direct invocations of sensitive
binaries (`ssh`, `gh auth`, `docker login`, `vault read`, `curl -H
"Authorization: ..."`, etc.) and reports them as `CRITICAL` or `HIGH` findings.

## Quickstart

```bash
# Default scan (report mode — exit 0 unless CRITICAL findings)
python tools/vbb-bypass-lint.py

# Explicit paths
python tools/vbb-bypass-lint.py tools/ prompts/ skills/

# Strict mode (CI) — exit 1 on HIGH+CRITICAL
python tools/vbb-bypass-lint.py --strict

# Machine-readable output
python tools/vbb-bypass-lint.py --json

# Include docs/ in the scan (default skips docs/)
python tools/vbb-bypass-lint.py --docs

# Scan the entire repo (no path filtering)
python tools/vbb-bypass-lint.py --all
```

## CLI options

| Flag | Description |
| --- | --- |
| `PATHS...` | Files or directories to scan. If omitted, defaults to `SOUL.md`, `tools/`, `prompts/`, `skills/`, `scripts/`. |
| `--severity-threshold {LOW,MEDIUM,HIGH,CRITICAL}` | Minimum severity to surface. Default: `LOW`. |
| `--json` | Emit machine-readable JSON output. |
| `--quiet` | Suppress human-readable output; rely on exit code. |
| `--exclude GLOB` | Additional exclude glob (repeatable). |
| `--strict` | Strict mode: exit non-zero on HIGH+CRITICAL. |
| `--all` | Scan the entire repository (no path filtering). |
| `--docs` | Include `docs/` in the scan (default skips `docs/`). |
| `--root PATH` | Repository root for path resolution (default: CWD). |

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Clean (or report mode with no CRITICAL findings). |
| `1` | At least one CRITICAL finding (report mode) or HIGH+CRITICAL (strict mode). |

> **Le mode par défaut est `report` — exit 0 même avec findings. Utilisez `--strict` en CI pour bloquer.**

## Patterns detected

Each pattern is anchored with context (`ssh `, `gh auth`, `docker login`, etc.)
to avoid false positives in prose. The full list lives at the top of
`tools/vbb-bypass-lint.py` (`DEFAULT_FORBIDDEN_PATTERNS`) and is the source of
truth for what is forbidden, derived from ADR 0011 §3 Règle 1.

| Category | Severity |
| --- | --- |
| `ssh` / `scp` / `rsync` to non-localhost | CRITICAL |
| `gh auth` / `gh repo` / `gh secret` | CRITICAL |
| `docker login` / `podman login` / `docker push` (private registry) | CRITICAL |
| `cat .env`, `printenv`, `env | grep` on secrets | CRITICAL |
| `aws configure`, `gcloud auth`, `az login` | CRITICAL |
| `mysql` / `psql` / `redis-cli` with credentials in CLI | HIGH |
| `kubectl config`, `helm secrets` | HIGH |
| `vault read` / `vault write`, `pass show` | CRITICAL |
| `curl -H "Authorization: ..."` with a secret | HIGH |
| `python -c "import os; os.environ[...]"` | HIGH |

## Mode strict vs report

- **Report (default)** — print all findings; `exit 1` only if at least one
  CRITICAL is present. This is the right mode for day-to-day developer runs:
  see the linter output but don't block a commit on HIGH-only noise.
- **Strict (`--strict`)** — print all findings; `exit 1` on any HIGH or
  CRITICAL finding. This is the right mode for CI: the linter becomes a hard
  gate.

## Allowlist (always exempt)

The following paths are never scanned (exempt from the forbidden patterns):

- `tools/proxy/` — proxy code itself, contains the reference list of
  forbidden patterns in comments, docstrings and tests.
- `docs/adr/` — ADR reference documents.
- `tools/vbb-bypass-lint.py` — this linter.
- `tools/vbb-bypass-lint/tests/` — this linter's tests.

## Documentation markers

Lines containing any of these tokens (case-insensitive) are skipped, even
if they would otherwise match a forbidden pattern:

- `interdit`, `bypass`, `do not`, `don't`, `ne pas`, `forbidden`
- `exemple négatif`, `anti-pattern`, `test négatif`
- `noqa: bypass-doc`, `DOC_CONTEXT`, `WHITELIST`

## Security notes

- The linter never logs file contents in full. Excerpts are capped to 200
  characters per finding.
- Files larger than 1 MB are skipped (no slurp).
- Binary files are detected heuristically and skipped silently.

## Tests

```bash
python -m pytest tools/vbb-bypass-lint/tests/ -v
```

37 unit tests, all passing, covering pattern detection, allowlist
exemption, documentation markers, test-context awareness, and the full
CLI surface.
