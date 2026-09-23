#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
case "${1:-codex}" in
  --replay) uv run semidebug replay results/v2/evidence/semantic_retry/result.json ;;
  --replay-v1) uv run semidebug replay results/sample_run/result.json ;;
  --scripted) ./scripts/docker_run.sh semidebug fix examples/fifo_off_by_one_v2 --provider scripted --responses examples/scripted_fifo_v2_responses.json --verbose ;;
  codex|--codex) uv run semidebug fix examples/fifo_off_by_one_v2 --provider codex --eda-runtime docker --verbose "${@:2}" ;;
  live|--api) ./scripts/docker_run.sh --live semidebug fix examples/fifo_off_by_one_v2 --provider live --verbose "${@:2}" ;;
  *) echo 'Usage: scripts/run_demo.sh [codex|--scripted|--replay|--replay-v1|--api] [options]'; exit 2 ;;
esac
