"""Host orchestration, network-disabled EDA containers; no CLI credentials mounted."""

import os
import uuid
from pathlib import Path

from semidebug.models import Case, ValidationBundle, ValidationResult
from semidebug.tools.process import run_process


def docker_environment() -> dict[str, str]:
    # The Docker client needs its normal context, but no model/API credentials.
    keys = (
        "PATH",
        "HOME",
        "DOCKER_HOST",
        "DOCKER_CONTEXT",
        "DOCKER_CONFIG",
        "DOCKER_TLS_VERIFY",
        "DOCKER_CERT_PATH",
    )
    return {key: os.environ[key] for key in keys if key in os.environ}


def docker_validation(root: Path, mode: str, case: Case) -> ValidationBundle:
    if mode not in {"target", "regression"}:
        raise ValueError("Invalid EDA worker mode")
    name = "semidebug-eda-" + uuid.uuid4().hex[:12]
    command = [
        "docker",
        "run",
        "--rm",
        "--name",
        name,
        "--network",
        "none",
        "--cpus",
        "2",
        "--memory",
        "2g",
        "--pids-limit",
        "128",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        "--user",
        f"{os.getuid()}:{os.getgid()}",
        "--mount",
        f"type=bind,source={root.resolve()},target=/work",
        "-e",
        "PYTHONDONTWRITEBYTECODE=1",
        "-w",
        "/work",
        "semidebug:dev",
        "python",
        "-m",
        "semidebug.tools.worker",
        mode,
    ]
    stages = 4 if mode == "target" else 2 * len(case.regression)
    result = run_process(
        command, root, case.timeout_sec * stages + 30, "docker", environment=docker_environment()
    )
    if result.status != "pass":
        run_process(
            ["docker", "rm", "-f", name],
            root,
            10,
            "docker-cleanup",
            environment=docker_environment(),
        )
        return ValidationBundle(
            results={
                "infrastructure": ValidationResult(
                    tool="docker",
                    command=["docker", "run", "semidebug:dev", mode],
                    exit_code=result.exit_code,
                    status="error",
                    stderr=result.stderr[-4000:],
                    duration_ms=result.duration_ms,
                )
            }
        )
    try:
        return ValidationBundle.model_validate_json(result.stdout)
    except ValueError:
        return ValidationBundle(
            results={
                "infrastructure": ValidationResult(
                    tool="docker",
                    command=["docker", "run", "semidebug:dev", mode],
                    exit_code=-1,
                    status="error",
                    stderr="Invalid EDA worker output; rebuild semidebug:dev image",
                )
            }
        )
