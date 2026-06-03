#!/bin/bash
# distributions/opencode/setup.sh — OpenCode distribution installation.
#
# This file is sourced by the root setup.sh routeur. It is the
# FIFTH distribution in the VBB installer (OpenCode = one of the 4 providers).
#
# Behavior is identical to the pre-Phase-2E inlined §8+§9 "OpenCode"
# blocks in setup.sh. Extracted verbatim — mechanical relocation only.
#
# Globals expected from the caller (setup.sh):
#   REPO_ROOT, HOME
#   AGENTS_SRC, SYSTEM_SRC
#   OPENCODE_JSON, OPENCODE_COMMANDS
#   FORCE_GOVERNANCE, SYSTEM_AVAILABLE
#
# Side effects (consumed by setup.sh summary):
#   OPENCODE_PROMPTS_OK, OPENCODE_PROMPTS_SKIP
#
# Helpers expected (from setup-lib.sh, sourced earlier in setup.sh):
#   needs_python, generate_prompt_commands

# ── OpenCode entry point ────────────────────────────────────────────────────
opencode_install() {
  opencode_patch_opencode_json
  opencode_generate_prompt_commands
}

# 1. OpenCode — instructions — add AGENTS.md + SYSTEM.md to the
#    "instructions" field, creating the file with $schema if absent
opencode_patch_opencode_json() {
  mkdir -p "$HOME/.config/opencode"
  if needs_python; then
    python3 - "$OPENCODE_JSON" "$AGENTS_SRC" "$SYSTEM_SRC" "$SYSTEM_AVAILABLE" <<'PY'
import json, sys, os
path, agents_src, system_src, system_available = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
system_available_flag = system_available.lower() == "true"

if os.path.exists(path):
    with open(path) as f:
        cfg = json.load(f)
else:
    cfg = {"$schema": "https://opencode.ai/config.json"}

instructions = cfg.get("instructions", [])
changes = []

if agents_src not in instructions:
    instructions.append(agents_src)
    changes.append("AGENTS.md")

if system_available_flag and system_src not in instructions:
    instructions.append(system_src)
    changes.append("SYSTEM.md")

if changes:
    cfg["instructions"] = instructions
    with open(path, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"✓ OpenCode: {', '.join(changes)} instruction(s) added")
else:
    already = ["AGENTS.md"]
    if system_available_flag:
        already.append("SYSTEM.md")
    print(f"✓ OpenCode: {', '.join(already)} already referenced")
PY
  else
    echo "⚠ OpenCode: python3 not found — opencode.json patch skipped"
  fi
}

# 2. OpenCode — prompt commands — generate 26 vbb-*.md in commands/
opencode_generate_prompt_commands() {
  OPENCODE_PROMPTS_OK=0
  OPENCODE_PROMPTS_SKIP=0
  generate_prompt_commands "$OPENCODE_COMMANDS" "OpenCode prompts" "OPENCODE_PROMPTS_OK" "OPENCODE_PROMPTS_SKIP"
}
