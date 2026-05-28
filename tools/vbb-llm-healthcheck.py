#!/usr/bin/env python3
"""
vbb-llm-healthcheck.py — Vérifie la santé des LLMs déclarés dans docs/LLM_PROVIDERS.md

Usage:
    python3 tools/vbb-llm-healthcheck.py [--full]

Options:
    --full    Teste aussi la génération (plus lent)
"""

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

# --- Configuration ---
REGISTRY_PATH = Path(__file__).parent.parent / "docs" / "LLM_PROVIDERS.md"
OVERRIDES_PATH = Path(__file__).parent.parent / ".pi" / "subagent-overrides.json"

# Providers locaux standards
PROVIDERS = {
    "ollama": {
        "endpoint": "http://localhost:11434",
        "model": "qwen3.6-27b-agent-nvfp4-64k:latest",
        "tags_endpoint": "/api/tags",
        "generate_endpoint": "/api/generate",
    },
    "ollama-cloud": {
        "endpoint": "https://api.ollama.com",
        "model": "deepseek-v4-flash:cloud",
        "tags_endpoint": "/api/tags",
        "generate_endpoint": "/api/generate",
    },
}


def check_provider(name: str, config: dict, full: bool = False) -> dict:
    """Vérifie qu'un provider local est accessible."""
    result = {
        "name": name,
        "endpoint": config["endpoint"],
        "model": config["model"],
        "status": "UNKNOWN",
        "latency_ms": None,
        "error": None,
    }

    # Test basic connectivity
    try:
        start = time.time()
        cmd = [
            "curl", "-s", "--max-time", "5",
            f"{config['endpoint']}{config['tags_endpoint']}"
        ]
        output = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        result["latency_ms"] = round((time.time() - start) * 1000)

        if output.returncode == 0 and output.stdout.strip():
            result["status"] = "✅ UP"
        else:
            result["status"] = "❌ DOWN"
            result["error"] = f"Curl returned {output.returncode}"
    except subprocess.TimeoutExpired:
        result["status"] = "❌ TIMEOUT"
        result["error"] = "5s timeout"
    except Exception as e:
        result["status"] = "❌ ERROR"
        result["error"] = str(e)

    # Test generation if --full
    if full and result["status"] == "✅ UP":
        try:
            if name == "ollama":
                gen_cmd = [
                    "curl", "-s", "--max-time", "30",
                    f"{config['endpoint']}{config['generate_endpoint']}",
                    "-d", json.dumps({
                        "model": config["model"],
                        "prompt": "Hi",
                        "stream": False
                    })
                ]
            else:
                gen_cmd = [
                    "curl", "-s", "--max-time", "30",
                    f"{config['endpoint']}{config['generate_endpoint']}",
                    "-d", json.dumps({
                        "model": config["model"],
                        "messages": [{"role": "user", "content": "Hi"}],
                        "max_tokens": 10
                    })
                ]
            output = subprocess.run(gen_cmd, capture_output=True, text=True, timeout=35)
            if output.returncode != 0 or not output.stdout.strip():
                result["status"] = "⚠️ DEGRADED"
                result["error"] = "Generation failed"
        except Exception as e:
            result["status"] = "⚠️ DEGRADED"
            result["error"] = str(e)

    return result


def get_fallback_chain() -> list:
    """Lit la chaîne de fallback depuis overrides."""
    if OVERRIDES_PATH.exists():
        try:
            with open(OVERRIDES_PATH) as f:
                overrides = json.load(f)
            chain = []
            for agent, config in overrides.items():
                if agent.startswith("_"):
                    continue
                if "fallbackModels" in config:
                    chain = [config["model"]] + config["fallbackModels"]
                    break
            return chain
        except Exception:
            pass
    return ["ollama/qwen3.6-27b-agent-nvfp4-64k:latest", "ollama/deepseek-v4-flash:cloud"]


def main():
    full = "--full" in sys.argv

    print("## LLM Healthcheck — vibebackbone\n")

    # Check each provider
    results = []
    for name, config in PROVIDERS.items():
        r = check_provider(name, config, full=full)
        results.append(r)
        status_icon = "✅" if "UP" in r["status"] else "❌" if "DOWN" in r["status"] else "⚠️"
        print(f"{status_icon} {name.upper()}")
        print(f"   Endpoint: {r['endpoint']}")
        print(f"   Model:    {r['model']}")
        print(f"   Status:   {r['status']}")
        if r["latency_ms"]:
            print(f"   Latency:  {r['latency_ms']}ms")
        if r["error"]:
            print(f"   Error:    {r['error']}")
        print()

    # Fallback chain
    chain = get_fallback_chain()
    print(f"**Fallback chain**: {' → '.join(chain)}\n")

    # Verdict
    local_up = any(r["name"] == "ollama" and "UP" in r["status"] for r in results)
    fallback_up = any(r["name"] == "ollama-cloud" and "UP" in r["status"] for r in results)

    if local_up and fallback_up:
        verdict = "✅ READY — Local + fallback disponibles"
    elif local_up:
        verdict = "⚠️ DEGRADED — Local OK, fallback injoignable"
    elif fallback_up:
        verdict = "⚠️ DEGRADED — Local down, fallback actif"
    else:
        verdict = "❌ DOWN — Aucun provider accessible"

    print(f"**Verdict**: {verdict}")

    # Exit code
    if not local_up:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
