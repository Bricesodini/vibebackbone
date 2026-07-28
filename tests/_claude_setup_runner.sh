#!/bin/bash
set -e
source "$REPO_ROOT/setup-lib.sh"
source "$REPO_ROOT/distributions/claude/setup.sh"
generate_prompt_commands() {
  mkdir -p "$3"
  eval "$4=0"
}
claude_install
