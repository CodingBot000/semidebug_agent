#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
uv run semidebug benchmark "${1:-benchmark_v2/public}" --provider api --eda-runtime docker "${@:2}"
