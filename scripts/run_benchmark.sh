#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
./scripts/docker_run.sh --live semidebug benchmark "${1:-benchmark/public}" "${@:2}"
