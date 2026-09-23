from semidebug.benchmark.loader import load_case
from semidebug.models import ValidationBundle, ValidationResult
from semidebug.tools.docker import docker_validation


def test_docker_worker_no_auth_mount(counter, monkeypatch):
    commands = []
    bundle = ValidationBundle(
        results={
            "compile": ValidationResult(
                tool="iverilog", command=["iverilog"], exit_code=0, status="pass"
            )
        }
    )

    def run(command, *args, **kwargs):
        commands.append((command, kwargs))
        return ValidationResult(
            tool="docker",
            command=command,
            exit_code=0,
            status="pass",
            stdout=bundle.model_dump_json(),
        )

    monkeypatch.setattr("semidebug.tools.docker.run_process", run)
    assert docker_validation(counter, "target", load_case(counter)).passed
    command, kwargs = commands[0]
    assert command[command.index("--network") + 1] == "none"
    mounts = [command[i + 1] for i, v in enumerate(command) if v == "--mount"]
    assert len(mounts) == 1 and "target=/work" in mounts[0] and ".codex" not in mounts[0]
    assert "OPENAI_API_KEY" not in kwargs["environment"]


def test_container_cleaned_after_timeout(counter, monkeypatch):
    commands = []

    def run(command, *args, **kwargs):
        commands.append(command)
        return ValidationResult(tool="docker", command=command, exit_code=-9, status="timeout")

    monkeypatch.setattr("semidebug.tools.docker.run_process", run)
    bundle = docker_validation(counter, "target", load_case(counter))
    assert bundle.infrastructure_error
    assert commands[1][:3] == ["docker", "rm", "-f"]
    assert commands[1][-1] == commands[0][commands[0].index("--name") + 1]
