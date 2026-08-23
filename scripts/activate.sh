#!/usr/bin/env bash
# Source this file to activate the project venv in your shell:
#   source scripts/activate.sh
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck disable=SC1091
source "$ROOT/.venv/bin/activate"
echo "Activated: Agentic AI Course (.venv, Python $(python --version 2>&1 | cut -d' ' -f2))"
echo "Run app: bash scripts/run.sh  →  http://localhost:8501"
