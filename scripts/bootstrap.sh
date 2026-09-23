#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v uv >/dev/null || { echo 'Install uv from https://docs.astral.sh/uv/getting-started/installation/'; exit 2; }
uv sync --frozen
if command -v docker >/dev/null && docker info >/dev/null 2>&1; then
  docker build -t semidebug:dev .
  ./scripts/doctor.sh
else
  echo 'Docker is unavailable. Install iverilog, verilator and yosys for native operation.'
  uv run semidebug doctor
fi
