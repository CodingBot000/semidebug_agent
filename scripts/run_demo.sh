#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
case "${1:-live}" in
  --replay) uv run semidebug replay results/sample_run/result.json ;;
  --scripted) ./scripts/docker_run.sh semidebug fix examples/fifo_off_by_one --provider scripted --responses examples/scripted_fifo_responses.json --verbose ;;
  live) ./scripts/docker_run.sh --live semidebug fix examples/fifo_off_by_one --verbose ;;
  *) echo 'Usage: scripts/run_demo.sh [live|--scripted|--replay]'; exit 2 ;;
esac
