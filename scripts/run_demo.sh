#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
case "${1:-codex}" in
  --replay) uv run semidebug replay results/sample_run/result.json ;;
  --scripted) ./scripts/docker_run.sh semidebug fix examples/fifo_off_by_one --provider scripted --responses examples/scripted_fifo_responses.json --verbose ;;
  codex|--codex) uv run semidebug fix examples/fifo_off_by_one --provider codex --eda-runtime docker --verbose "${@:2}" ;;
  live|--api) ./scripts/docker_run.sh --live semidebug fix examples/fifo_off_by_one --provider live --verbose "${@:2}" ;;
  *) echo 'Usage: scripts/run_demo.sh [codex|--scripted|--replay|--api] [options]'; exit 2 ;;
esac
