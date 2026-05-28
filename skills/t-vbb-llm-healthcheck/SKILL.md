---
name: t-vbb-llm-healthcheck
description: |
  Vérifie la santé des LLMs déclarés dans docs/LLM_PROVIDERS.md.
  Teste la connectivité, la disponibilité du modèle local, et le fallback.
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

Vérifie que les LLMs déclarés dans `docs/LLM_PROVIDERS.md` sont accessibles.

## ROUTINE

### 1. Lire le registry

```
docs/LLM_PROVIDERS.md
```

Extraire:
- Modèles locaux (`provider: Ollama` / `provider: LM Studio`)
- Endpoint de chaque provider local
- Modèle fallback

### 2. Tester chaque provider local

```bash
# Test Ollama
curl -s --max-time 5 http://localhost:11434/api/tags

# Vérifier que le modèle est disponible
ollama list | grep qwen3.6-27b-agent-nvfp4-64k
```

### 3. Test de génération minimal (optionnel, si --full)

```bash
# Teste que Ollama répond vraiment
curl -s --max-time 30 http://localhost:11434/api/generate \
  -d '{"model":"qwen3.6-27b-agent-nvfp4-64k:latest","prompt":"Hi","stream":false}' \
  | jq -r '.response' | head -c 100
```

### 4.Rapport

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

| Champ | Description |
|-------|-------------|
| `providers` | Liste des providers avec status |
| `fallback_chain` | Liste ordonnée des modèles |
| `verdict` | `READY` (local OK) / `DEGRADED` (fallback only) / `DOWN` (aucun accessible) |
| `recommendation` | Action si verdict != READY |

## USAGE

```bash
# Healthcheck rapide
python3 tools/vbb-llm-healthcheck.py

# Healthcheck complet avec test de génération
python3 tools/vbb-llm-healthcheck.py --full
```

## NOTES

- Le fallback est automatique si le provider local échoue
- Ce skill ne modifie rien — lecture seule
- Si local est DOWN, les subagents utilisent automatiquement le fallback
