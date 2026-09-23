#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
uv run semidebug benchmark "${1:-benchmark/public}" --provider codex --eda-runtime docker "${@:2}"
