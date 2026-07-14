---
name: t-vbb-llm-healthcheck
description: |
  Checks the health of LLMs declared in docs/LLM_PROVIDERS.md.
  Tests connectivity, local-model availability, and fallback behavior.
  Use when: checking LLM availability, before launching subagents, or troubleshooting
  subagent failures. Keywords: healthcheck, LLM, Ollama, provider, connectivity,
  subagent fallback, model availability.
version: "1.0"
phase: transverse
token_budget: low
subagent_eligible: false
mode_sensitive: false
---

# T-VBB-LLM-Healthcheck

## ROLE & POSTURE

Check whether providers declared in `docs/LLM_PROVIDERS.md` are reachable.
Read-only: do not modify provider configuration or start/stop services.

## INPUT CONTRACT

Required: none. Optional: `docs/LLM_PROVIDERS.md` and full generation-test mode.

## BLOCKING CONDITIONS

Return `DOWN` when no declared provider can be reached. Return `BLOCKED` only
when the provider registry is required but missing or unreadable.

## SCOPE

Provider connectivity, declared model availability, minimal optional generation,
and fallback-chain reporting. Exclude model benchmarking and configuration edits.

## PROCESS

### 1. Read the registry

```
docs/LLM_PROVIDERS.md
```

Extract local models (`provider: Ollama` / `provider: LM Studio`), each local
endpoint, and the fallback model.

### 2. Test each local provider

```bash
# Check Ollama
curl -s --max-time 5 http://localhost:11434/api/tags

# Verify that the model is available
ollama list | grep qwen3.6-27b-agent-nvfp4-64k
```

### 3. Minimal generation test (optional with `--full`)

```bash
# Verify that Ollama actually generates a response
curl -s --max-time 30 http://localhost:11434/api/generate \
  -d '{"model":"qwen3.6-27b-agent-nvfp4-64k:latest","prompt":"Hi","stream":false}' \
  | jq -r '.response' | head -c 100
```

### 4. Report

Output:

```markdown
## LLM Healthcheck

| Provider | Endpoint | Model | Status |
|----------|----------|-------|--------|
| Ollama | localhost:11434 | qwen3:6b-agent-np4-64k | ✅ / ❌ |
| LM Studio | http://169.254.37.109:1234 | MiniMax-M2.7 | ✅ / ❌ |

**Fallback chain**: qwen3:6b-agent-np4-64k → MiniMax-M2.7

**Verdict**: READY | DEGRADED | DOWN
```

## OUTPUT CONTRACT

| Field | Description |
|---|---|
| `providers` | Provider list with status |
| `fallback_chain` | Ordered model list |
| `verdict` | `READY` (local OK) / `DEGRADED` (fallback only) / `DOWN` (none reachable) |
| `recommendation` | Action when verdict is not READY |

## VERDICT RULES

- `READY`: the declared local provider and model are available.
- `DEGRADED`: local provider unavailable but a fallback is reachable.
- `DOWN`: no declared provider is reachable.
- `BLOCKED`: registry evidence is unavailable.

## USAGE

```bash
# Quick healthcheck
python3 tools/vbb-llm-healthcheck.py

# Full healthcheck with generation test
python3 tools/vbb-llm-healthcheck.py --full
```

## NOTES

- Fallback is automatic when the local provider fails.
- This skill is read-only.
- When local status is DOWN, subagents use the declared fallback automatically.
