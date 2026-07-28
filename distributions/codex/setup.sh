#!/bin/bash
# distributions/codex/setup.sh — Codex distribution installation.
#
# This file is sourced by the root setup.sh routeur. It is the
# FOURTH distribution in the VBB installer (Codex = one of the 4 providers).
#
# Runtime files are compiled without ever writing through a destination
# symlink. Legacy VBB links to the Core source are migrated to regular files.
#
# Adversarial governance (M3-11): this script inherits v1.1 adversarial
# governance from Core (`docs/ADVERSARIAL_ASSURANCE_GOVERNANCE.md`,
# `tools/vbb-adversarial-gate.py`) via the AGENTS.md reference. Provider
# binaries are unaware of the v1.1 schema version on their own; the
# gateway check is performed through the Core resolver.
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

codex_uninstall() {
  if needs_python; then
    python3 - "$CODEX_AGENTS" "$AGENTS_SRC" <<'PY'
import os
import sys
import tempfile

path, agents_src = sys.argv[1], sys.argv[2]
START = "<!-- vibebackbone:generated:start -->"
END = "<!-- vibebackbone:generated:end -->"


def write_atomic(target, content):
    directory = os.path.dirname(target) or "."
    fd, temporary = tempfile.mkstemp(prefix=".vbb-codex-", dir=directory, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary, target)
    except Exception:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


if os.path.islink(path):
    if os.path.realpath(path) == os.path.realpath(agents_src):
        os.unlink(path)
        print("✓ Removed legacy Codex AGENTS.md symlink without touching Core")
    else:
        print("⚠ Codex: unrelated AGENTS.md symlink preserved during uninstall")
    sys.exit(0)

if not os.path.isfile(path):
    sys.exit(0)

with open(path, encoding="utf-8") as handle:
    content = handle.read()
first = content.find(START)
last = content.rfind(END)
if first != -1 and last != -1 and last >= first:
    last += len(END)
    while last < len(content) and content[last] in "\r\n":
        last += 1
    cleaned = content[:first] + content[last:]
elif first != -1:
    cleaned = content[:first]
else:
    cleaned = content

if not cleaned.strip():
    os.remove(path)
    print("✓ Removed ~/.codex/AGENTS.md (empty after block removal)")
elif cleaned != content:
    write_atomic(path, cleaned)
    print("✓ Removed vibebackbone generated block from ~/.codex/AGENTS.md")
else:
    print("✓ Codex AGENTS.md contained no vibebackbone generated block")
PY
  else
    echo "⚠ Codex: python3 not found — AGENTS.md uninstall skipped"
  fi
}

# 1. Codex — compiled AGENTS.md — generate the block with start/end markers
#    (manages existing custom files via --force-governance backup)
codex_compile_agents_md() {
  mkdir -p "$HOME/.codex"

  if needs_python; then
    python3 - "$CODEX_AGENTS" "$AGENTS_SRC" "$SYSTEM_SRC" "$SYSTEM_AVAILABLE" "$FORCE_GOVERNANCE" "$PROMPTS_SRC" "$PROMPTS_AVAILABLE" <<'PY'
import os
import shutil
import sys
import tempfile
from datetime import datetime as _dt

path, agents_src, system_src, system_available, force_governance, prompts_src, prompts_available = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
force = force_governance.lower() == "true"
system_available_flag = system_available.lower() == "true"
prompts_available_flag = prompts_available.lower() == "true"
START = "<!-- vibebackbone:generated:start -->"
END = "<!-- vibebackbone:generated:end -->"

with open(agents_src, encoding="utf-8") as handle:
    agents_content = handle.read()
if START in agents_content or END in agents_content:
    print("✗ Codex: canonical AGENTS.md contains generated runtime markers", file=sys.stderr)
    print("  Restore the Core source before compiling runtime governance.", file=sys.stderr)
    sys.exit(1)


def write_atomic(target, content):
    directory = os.path.dirname(target) or "."
    fd, temporary = tempfile.mkstemp(prefix=".vbb-codex-", dir=directory, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary, target)
    except Exception:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def backup_content(source):
    backup_path = f"{path}.backup.{_dt.now().strftime('%Y%m%d-%H%M%S')}"
    shutil.copyfile(source, backup_path, follow_symlinks=True)
    print(f"✓ Codex: backup created at {backup_path}")
    return backup_path

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

def build_block(agents_src, agents_content, system_src, system_available_flag, prompts_src, prompts_available_flag):
    lines = [
        "\n<!-- vibebackbone:generated:start -->\n",
        f"<!-- Source: {agents_src} -->\n",
        agents_content,
    ]
    if system_available_flag:
        lines.extend([
            "\n---\n",
            f"<!-- Source: {system_src} -->\n",
            open(system_src, encoding="utf-8").read(),
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

if os.path.islink(path):
    linked_to_core = os.path.realpath(path) == os.path.realpath(agents_src)
    if linked_to_core:
        os.unlink(path)
        print("✓ Codex: migrated legacy AGENTS.md symlink to a regular file")
    elif not force:
        print("⚠ Codex: existing AGENTS.md symlink skipped (use --force-governance)")
        sys.exit(0)
    else:
        if os.path.exists(path):
            backup_content(path)
        os.unlink(path)
        print("✓ Codex: unrelated AGENTS.md symlink replaced without modifying its target")

if os.path.isfile(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    has_markers = START in content

    if has_markers:
        new_block = build_block(agents_src, agents_content, system_src, system_available_flag, prompts_src, prompts_available_flag)
        content = replace_generated_block(content, new_block)
        write_atomic(path, content)
        print("✓ Codex: generated block updated")
        sys.exit(0)
    else:
        if force:
            backup_content(path)
            new_block = build_block(agents_src, agents_content, system_src, system_available_flag, prompts_src, prompts_available_flag)
            write_atomic(path, new_block)
            print("✓ Codex: generated AGENTS.md created (custom file backed up and replaced)")
        else:
            print("⚠ Codex: existing custom AGENTS.md skipped (use --force-governance)")
        sys.exit(0)

new_block = build_block(agents_src, agents_content, system_src, system_available_flag, prompts_src, prompts_available_flag)
write_atomic(path, new_block)
print("✓ Codex: generated AGENTS.md created")
PY
  else
    echo "⚠ Codex: python3 not found — compiled AGENTS.md generation skipped"
  fi
}
