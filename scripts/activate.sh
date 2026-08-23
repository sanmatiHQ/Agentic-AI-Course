#!/usr/bin/env bash
# Activate the project venv in your shell:
#   source scripts/activate.sh
if [[ -n "${ZSH_VERSION:-}" ]]; then
  ROOT="$(cd "$(dirname "${(%):-%x}")/.." && pwd)"
else
  ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi
# shellcheck disable=SC1091
source "$ROOT/.venv/bin/activate"
echo "Activated: Agentic AI Course (.venv, Python $(python --version 2>&1 | cut -d' ' -f2))"
echo "Run app: bash scripts/run.sh  →  http://localhost:8501"
