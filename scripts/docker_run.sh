#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# Keep the option array nonempty for macOS Bash 3.2 + nounset compatibility.
options=(--rm --cpus 2 --memory 2g --pids-limit 128 --cap-drop ALL --security-opt no-new-privileges)
if [[ "${1:-}" == '--live' ]]; then
  shift
  if [[ -f .env ]]; then options+=(--env-file .env); fi
  for name in OPENAI_API_KEY OPENAI_MODEL OPENAI_BASE_URL SEMIDEBUG_JSON_MODE SEMIDEBUG_API_TIMEOUT SEMIDEBUG_MAX_ITERATIONS SEMIDEBUG_INPUT_PRICE SEMIDEBUG_OUTPUT_PRICE SEMIDEBUG_PRICE_SOURCE; do
    if printenv "$name" >/dev/null 2>&1; then options+=(-e "$name"); fi
  done
else
  options+=(--network none)
fi
docker run "${options[@]}" --user "$(id -u):$(id -g)" \
  -e PYTHONDONTWRITEBYTECODE=1 -e HOME=/tmp \
  -v "$PWD:/app:ro" -v "$PWD/artifacts:/app/artifacts" \
  -w /app semidebug:dev sh -c '
    if [ ! -f /app/pyproject.toml ] || [ ! -d /app/src/semidebug ]; then
      echo "Docker cannot read the project bind mount. Use a Docker-shared directory (Colima: under your home), or configure filesystem sharing." >&2
      exit 2
    fi
    exec "$@"
  ' semidebug-command "$@"
