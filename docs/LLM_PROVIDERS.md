---
title: LLM Provider Registry
status: active
updated: 2026-05-28
version: "1.0"
---

# LLM Provider Registry

Registre des LLMs utilisables par les subagents vibebackbone.

**Stratégie**: LOCAL d'abord → FALLBACK automatique vers Ollama Cloud.

---

## LLMs Locaux

| Nom | Provider | Endpoint | Modèle | Port | Status |
|-----|----------|----------|--------|------|--------|
| Ollama | Ollama | http://localhost:11434 | qwen3.6-27b-agent-nvfp4-64k:latest | 11434 | ✅ |

### Vérification

```bash
# Vérifier qu'Ollama tourne
ollama list

# Tester le modèle
curl -s http://localhost:11434/api/tags | jq
```

---

## LLMs Cloud (Fallback)

| Nom | Provider | Modèle | Status |
|-----|----------|---------|--------|
| Ollama Cloud | Ollama.com | deepseek-v4-flash:cloud | ✅ |

**Fallback chain**: `qwen3.6-27b-agent-nvfp4-64k:latest` → `deepseek-v4-flash:cloud`

---

## Configuration des Agents Vibebackbone

| Agent | Modèle local | Fallback | Thinking |
|-------|-------------|----------|----------|
| vbb-scouter | ollama/qwen3.6-27b-agent-nvfp4-64k:latest | ollama/deepseek-v4-flash:cloud | medium |
| vbb-reviewer | ollama/qwen3.6-27b-agent-nvfp4-64k:latest | ollama/deepseek-v4-flash:cloud | medium |
| vbb-worker | ollama/qwen3.6-27b-agent-nvfp4-64k:latest | ollama/deepseek-v4-flash:cloud | high |
| vbb-researcher | ollama/qwen3.6-27b-agent-nvfp4-64k:latest | ollama/deepseek-v4-flash:cloud | medium |
| vbb-planner | ollama/qwen3.6-27b-agent-nvfp4-64k:latest | ollama/deepseek-v4-flash:cloud | high |
| vbb-oracle | ollama/qwen3.6-27b-agent-nvfp4-64k:latest | ollama/deepseek-v4-flash:cloud | high |

---

## Changement de Configuration

### Pour changer le modèle local

1. Modifier ce fichier (`model` dans le tableau "LLMs Locaux")
2. Mettre à jour `distributions/pi/overrides.template.json` (path canonique depuis ADR 0013 Phase 4 ; le symlink `.pi/subagent-overrides.json` historique n'est plus utilisé)
3. Relancer les subagents

### Pour ajouter un fallback supplémentaire

```json
// Editer distributions/pi/overrides.template.json
{
  "vbb-worker": {
    "model": "ollama/qwen3.6-27b-agent-nvfp4-64k:latest",
    "fallbackModels": ["ollama/deepseek-v4-flash:cloud", "openai/gpt-4o-mini"]
  }
}
```

---

## Healthcheck

Voir `skills/t-vbb-llm-healthcheck/SKILL.md`

---

*Ce fichier est la source unique de vérité pour les providers LLM des subagents.*
