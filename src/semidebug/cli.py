import argparse
import json
import shutil
import sys
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

from semidebug.agent.orchestrator import repair
from semidebug.benchmark.loader import load_case
from semidebug.benchmark.runner import run_benchmark
from semidebug.config import Settings
from semidebug.llm.base import ProviderError
from semidebug.llm.codex import CodexCLIProvider, codex_auth_status
from semidebug.llm.fake import ScriptedProvider
from semidebug.llm.provider import OpenAICompatibleProvider
from semidebug.models import RunState
from semidebug.report.renderer import render_run
from semidebug.tools.process import run_process
from semidebug.tools.validation import validate
from semidebug.tools.workspace import copy_project


def doctor(runtime="native"):
    settings = Settings.from_env()
    checks = {}
    for tool, flags in {
        "iverilog": ["-V"],
        "vvp": ["-V"],
        "verilator": ["--version"],
        "yosys": ["-V"],
    }.items():
        if not shutil.which(tool):
            checks[tool] = {"available": False, "version": None}
            continue
        result = run_process([tool, *flags], Path.cwd(), 10, tool)
        checks[tool] = {
            "available": result.status == "pass",
            "version": (result.stdout + result.stderr).splitlines()[0],
        }
    if runtime == "docker":
        from semidebug.tools.docker import docker_environment

        result = run_process(
            ["docker", "run", "--rm", "--network", "none", "semidebug:dev", "semidebug", "doctor"],
            Path.cwd(),
            30,
            "docker",
            environment=docker_environment(),
        )
        try:
            checks = json.loads(result.stdout)
        except ValueError:
            checks["docker_error"] = "Build semidebug:dev and start Docker"
    checks["python"] = sys.version.split()[0]
    checks["eda_runtime"] = runtime
    checks["codex"] = {
        "installed": bool(shutil.which("codex")),
        "chatgpt_authenticated": codex_auth_status(),
        "model": settings.codex_model,
        "reasoning_effort": settings.reasoning_effort,
    }
    checks["llm"] = {
        "configured": bool(settings.api_key and settings.model),
        "model": settings.model or None,
    }
    checks["docker"] = {"installed": bool(shutil.which("docker")), "optional": True}
    print(json.dumps(checks, indent=2))
    return (
        0 if all(checks[t]["available"] for t in ["iverilog", "vvp", "verilator", "yosys"]) else 2
    )


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="semidebug", description="RTL repair accepted only after independent EDA validation"
    )
    sub = parser.add_subparsers(dest="command", required=True)
    doctor_parser = sub.add_parser("doctor")
    doctor_parser.add_argument("--eda-runtime", choices=["native", "docker"], default="native")
    for command in ["fix", "benchmark"]:
        p = sub.add_parser(command)
        p.add_argument("path", type=Path)
        p.add_argument("--provider", choices=["codex", "live", "scripted"], default="codex")
        p.add_argument(
            "--responses", type=Path, help="Explicit scripted test responses, never gold lookup"
        )
        p.add_argument("--model")
        p.add_argument("--reasoning-effort", choices=["low", "medium", "high", "xhigh", "max"])
        p.add_argument("--eda-runtime", choices=["native", "docker"])

        p.add_argument("--max-iterations", type=int)
        p.add_argument("--output", type=Path)
        p.add_argument("--verbose", action="store_true")
    p = sub.add_parser("validate")
    p.add_argument("path", type=Path)
    for command in ["report", "replay"]:
        p = sub.add_parser(command)
        p.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    provider = None
    try:
        if args.command == "doctor":
            return doctor(args.eda_runtime)
        if args.command in {"replay", "report"}:
            state = RunState.model_validate_json(args.path.read_text())
            if args.command == "replay":
                print("RECORDED RUN — no LLM or EDA tool is being executed\n")
            print(render_run(state))
            return 0
        if args.command == "validate":
            import tempfile

            case = load_case(args.path)
            with tempfile.TemporaryDirectory(prefix="semidebug-validate-") as temporary:
                root = Path(temporary) / "project"
                copy_project(
                    args.path, root, sorted(set(case.mutable + case.immutable + ["case.json"]))
                )
                bundle = validate(root, case)
                print(bundle.model_dump_json(indent=2))
                return 0 if bundle.passed else 1
        settings = Settings.from_env()
        if args.model:
            settings = replace(
                settings, **{"codex_model" if args.provider == "codex" else "model": args.model}
            )
        if args.reasoning_effort:
            settings = replace(settings, reasoning_effort=args.reasoning_effort)
        if args.eda_runtime:
            settings = replace(settings, eda_runtime=args.eda_runtime)
        elif args.provider == "codex" and not all(
            shutil.which(t) for t in ["iverilog", "vvp", "verilator", "yosys"]
        ):
            settings = replace(settings, eda_runtime="docker")
        if args.max_iterations is not None:
            settings = replace(settings, max_iterations=args.max_iterations)
        if not 1 <= settings.max_iterations <= 10:
            raise ValueError("max_iterations must be 1..10")
        if args.provider == "scripted":
            if not args.responses:
                raise ValueError("Scripted mode requires --responses and is not an AI benchmark")
            provider = ScriptedProvider(json.loads(args.responses.read_text()))
            print("SCRIPTED TEST MODE — not live AI")
        elif args.provider == "codex":
            provider = CodexCLIProvider(settings)
            print(
                f"LIVE CODEX CLI — {provider.model}, reasoning={provider.reasoning_effort}, ChatGPT subscription",
                flush=True,
            )
        else:
            provider = OpenAICompatibleProvider(settings)
        if args.command == "fix":
            state = repair(args.path, provider, args.output or Path("artifacts/runs"), settings)
            print(
                f"{state.case_id}: {state.final_status}; iterations={state.iteration}; integrity={state.integrity_pass}"
            )
            print(
                f"Evidence: {(args.output or Path('artifacts/runs')) / state.run_id / 'report.md'}"
            )
            if args.verbose:
                print(render_run(state))
            return 0 if state.success or state.final_status == "ALREADY_PASS" else 1
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
        summary = run_benchmark(
            args.path, provider, args.output or Path("artifacts/benchmark") / stamp, settings
        )
        print(json.dumps(summary, indent=2))
        return (
            0
            if not any(
                k in summary["failure_breakdown"]
                for k in ["INFRA_ERROR", "LLM_ERROR", "INTEGRITY_ERROR"]
            )
            else 2
        )
    except (ProviderError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    finally:
        if isinstance(provider, OpenAICompatibleProvider):
            provider.close()


if __name__ == "__main__":
    raise SystemExit(main())
