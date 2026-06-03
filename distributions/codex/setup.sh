#!/bin/bash
# distributions/codex/setup.sh — Codex distribution installation.
#
# This file is sourced by the root setup.sh routeur. It is the
# FOURTH distribution in the VBB installer (Codex = one of the 4 providers).
#
# Behavior is IDENTICAL to the pre-Phase-2D inlined §6 "Codex — compiled
# AGENTS.md" block in setup.sh. Extracted verbatim — no simplification,
# no refactoring, no content change. Mechanical relocation only.
#
# Globals expected from the caller (setup.sh):
#   REPO_ROOT, HOME
#   AGENTS_SRC, SYSTEM_SRC, PROMPTS_SRC
#   CODEX_AGENTS
#   FORCE_GOVERNANCE, SYSTEM_AVAILABLE, PROMPTS_AVAILABLE
#
# Helpers expected (from setup-lib.sh, sourced earlier in setup.sh):
#   needs_python

# ── Codex entry point ───────────────────────────────────────────────────────
codex_install() {
  codex_compile_agents_md
}

# 1. Codex — compiled AGENTS.md — generate the block with start/end markers
#    (manages existing custom files via --force-governance backup)
codex_compile_agents_md() {
  mkdir -p "$HOME/.codex"

  if needs_python; then
    python3 - "$CODEX_AGENTS" "$AGENTS_SRC" "$SYSTEM_SRC" "$SYSTEM_AVAILABLE" "$FORCE_GOVERNANCE" "$PROMPTS_SRC" "$PROMPTS_AVAILABLE" <<'PY'
import sys, os
path, agents_src, system_src, system_available, force_governance, prompts_src, prompts_available = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
force = force_governance.lower() == "true"
system_available_flag = system_available.lower() == "true"
prompts_available_flag = prompts_available.lower() == "true"
START = "<!-- vibebackbone:generated:start -->"
END = "<!-- vibebackbone:generated:end -->"

def replace_generated_block(content, new_block):
    first = content.find(START)
    if first == -1:
        return None
    last = content.rfind(END)
    if last == -1 or last < first:
        return content[:first] + new_block.rstrip() + "\n"
    last += len(END)
    while last < len(content) and content[last] in "\r\n":
        last += 1
    return content[:first] + new_block.rstrip() + "\n" + content[last:]

def build_block(agents_src, system_src, system_available_flag, prompts_src, prompts_available_flag):
    lines = [
        "\n<!-- vibebackbone:generated:start -->\n",
        f"<!-- Source: {agents_src} -->\n",
        open(agents_src).read(),
    ]
    if system_available_flag:
        lines.extend([
            "\n---\n",
            f"<!-- Source: {system_src} -->\n",
            open(system_src).read(),
        ])
    if prompts_available_flag:
        lines.extend([
            "\n---\n",
            "# Vibebackbone Prompt Library\n",
            "Prompt templates are available at:\n",
            f"`{os.path.expanduser('~/.agents/prompts/vibebackbone/')}`\n",
            "They are session entrypoints, not skills.\n",
            "Resolve prompt short names to Markdown files before reading them:\n",
            "- `quick-task` -> `1-p-vbb-quick-task.md`\n",
            "- `structured-task` -> `1-p-vbb-structured-task.md`\n",
            "- `audit-task` -> `2-p-vbb-audit-task.md`\n",
            "- `release-check` -> `2-p-vbb-release-check.md`\n",
            "- `session-handoff` -> `t-p-vbb-session-handoff.md`\n",
            "Read the resolved Markdown prompt from that directory and apply it before execution.\n",
            "Do not invent prompt behavior from the name alone. If the prompt file is missing, state that explicitly and proceed only as best-effort.\n",
        ])
    lines.append("\n<!-- vibebackbone:generated:end -->\n")
    return "".join(lines)

if os.path.exists(path):
    with open(path) as f:
        content = f.read()
    has_markers = START in content

    if has_markers:
        new_block = build_block(agents_src, system_src, system_available_flag, prompts_src, prompts_available_flag)
        content = replace_generated_block(content, new_block)
        with open(path, "w") as f:
            f.write(content)
        print("✓ Codex: generated block updated")
        sys.exit(0)
    else:
        if force:
            from datetime import datetime as _dt
            backup_path = f"{path}.backup.{_dt.now().strftime('%Y%m%d-%H%M%S')}"
            import shutil
            shutil.copy(path, backup_path)
            print(f"✓ Codex: backup created at {backup_path}")
            new_block = build_block(agents_src, system_src, system_available_flag, prompts_src, prompts_available_flag)
            with open(path, "w") as f:
                f.write(new_block)
            print("✓ Codex: generated AGENTS.md created (custom file backed up and replaced)")
        else:
            print("⚠ Codex: existing custom AGENTS.md skipped (use --force-governance)")
        sys.exit(0)

new_block = build_block(agents_src, system_src, system_available_flag, prompts_src, prompts_available_flag)
with open(path, "w") as f:
    f.write(new_block)
print("✓ Codex: generated AGENTS.md created")
PY
  else
    echo "⚠ Codex: python3 not found — compiled AGENTS.md generation skipped"
  fi
}
