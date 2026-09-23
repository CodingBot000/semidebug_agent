#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

verification_dir="artifacts/submission-verification"
mkdir -p "$verification_dir"

run_step() {
  local name="$1"
  shift
  local log="$verification_dir/$name.log"
  if "$@" >"$log" 2>&1; then
    printf '%s: PASS (%s)\n' "$name" "$log"
  else
    local status=$?
    cat "$log"
    printf '%s: FAIL, exit=%s (%s)\n' "$name" "$status" "$log" >&2
    return "$status"
  fi
}

run_step bootstrap ./scripts/bootstrap.sh
run_step replay ./scripts/run_demo.sh --replay
run_step scripted_v2_demo ./scripts/run_demo.sh --scripted
run_step lint make lint
run_step test_all make test-all
printf 'All submission checks passed. Logs: %s\n' "$verification_dir"
