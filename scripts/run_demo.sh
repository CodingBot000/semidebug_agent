#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
case "${1:-api}" in
  --replay) uv run semidebug replay results/final/evidence/semantic_retry/result.json ;;
  --scripted) ./scripts/docker_run.sh semidebug fix examples/fifo_off_by_one_v2 --provider scripted --responses examples/scripted_fifo_v2_responses.json --verbose ;;
  api|--api) uv run semidebug fix examples/fifo_off_by_one_v2 --provider api --eda-runtime docker --verbose "${@:2}" ;;
  *) echo 'Usage: scripts/run_demo.sh [api|--scripted|--replay] [options]'; exit 2 ;;
esac
