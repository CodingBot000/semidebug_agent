#!/usr/bin/env python3
"""Run and preserve final lint, full suite and scripted demo evidence."""

import hashlib
import json
import platform
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from semidebug.config import Settings

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results/final/verification"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def probe(command: list[str]) -> dict:
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"available": False, "detail": type(exc).__name__}
    return {
        "available": result.returncode == 0,
        "detail": (result.stdout + result.stderr).strip()[:300],
    }


def capture(command: list[str], label: str) -> tuple[dict, str]:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            timeout=1200,
        )
        exit_code = completed.returncode
        output = completed.stdout
    except subprocess.TimeoutExpired as exc:
        exit_code = 124
        output = (
            (exc.stdout or b"").decode(errors="replace")
            if isinstance(exc.stdout, bytes)
            else (exc.stdout or "")
        )
        output += "\nVerification command timed out.\n"
    except OSError as exc:
        exit_code = 127
        output = f"Verification command could not start: {type(exc).__name__}\n"
    log = OUTPUT / f"{label}.log"
    log.write_text(f"Command: {' '.join(command)}\nExit code: {exit_code}\n\n{output}")
    return (
        {
            "command": command,
            "exit_code": exit_code,
            "duration_ms": round((time.monotonic() - started) * 1000),
            "log": log.relative_to(ROOT).as_posix(),
            "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
        },
        output,
    )


def demo_gates(output: str) -> dict:
    match = re.search(r"Evidence: (artifacts/runs/[^\s]+/report\.md)", output)
    if not match:
        return {"status": "FAIL", "reason": "Demo did not report an evidence path"}
    report = ROOT / match.group(1)
    result_path = report.parent / "result.json"
    if not result_path.is_file():
        return {"status": "FAIL", "reason": "Demo result.json was not saved"}
    result = json.loads(result_path.read_text())
    curated_result = OUTPUT / "scripted_demo_result.json"
    curated_report = OUTPUT / "scripted_demo_report.md"
    curated_result.write_bytes(result_path.read_bytes())
    curated_report.write_bytes(report.read_bytes())
    attempts = result.get("patch_attempts", [])
    first = attempts[0] if len(attempts) == 1 else {}
    baseline = result.get("baseline") or {}
    baseline_results = baseline.get("results", {})
    validation = (first.get("validation") or {}).get("results", {})
    regression = (first.get("regression") or {}).get("results", {})
    regression_checks = (
        "regression_17.compile",
        "regression_17.simulation",
        "regression_103.compile",
        "regression_103.simulation",
    )
    gates = {
        "case_is_final_demo": result.get("case_id") == "demo_fifo_off_by_one_v2",
        "scripted_provider": result.get("provider") == "scripted-test-double",
        "baseline_failed": bool(baseline_results)
        and any(check["status"] == "fail" for check in baseline_results.values()),
        "patch_accepted": bool(first) and first.get("guard_error") is None,
        "compile_pass": validation.get("compile", {}).get("status") == "pass",
        "simulation_pass": validation.get("simulation", {}).get("status") == "pass",
        "lint_pass": validation.get("lint", {}).get("status") == "pass",
        "synthesis_pass": validation.get("synthesis", {}).get("status") == "pass",
        "hidden_regression_pass": set(regression) == set(regression_checks)
        and all(regression[key]["status"] == "pass" for key in regression_checks),
        "integrity_pass": result.get("integrity_pass") is True,
        "final_fixed": result.get("final_status") == "FIXED" and result.get("success") is True,
    }
    return {
        "status": "PASS" if all(gates.values()) else "FAIL",
        "result": curated_result.relative_to(ROOT).as_posix(),
        "report": curated_report.relative_to(ROOT).as_posix(),
        "gates": gates,
    }


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    settings = Settings.from_env()
    environment = {
        "observed_at_utc": utc_now(),
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "host_python": platform.python_version(),
        "project_python": probe(["uv", "run", "python", "--version"]),
        "uv": probe(["uv", "--version"]),
        "docker_cli": probe(["docker", "--version"]),
        "docker_daemon": probe(["docker", "info", "--format", "{{.ServerVersion}}"]),
        "openai_api": {
            "configured": bool(settings.api_key and settings.model),
            "model": settings.model or None,
            "reasoning_effort": settings.reasoning_effort,
            "endpoint": settings.base_url,
        },
    }
    (OUTPUT / "environment.json").write_text(json.dumps(environment, indent=2) + "\n")

    lint, _ = capture(["make", "lint"], "lint")
    lint["status"] = "PASS" if lint["exit_code"] == 0 else "FAIL"
    if environment["docker_daemon"]["available"]:
        tests, test_output = capture(["make", "test-all"], "test_all")
        counts = re.findall(r"\b(\d+) passed\b", test_output)
        tests["passed_count"] = int(counts[-1]) if counts else None
        tests["status"] = "PASS" if tests["exit_code"] == 0 and counts else "FAIL"
        demo, demo_output = capture(["./scripts/run_demo.sh", "--scripted"], "scripted_demo")
        demo.update(demo_gates(demo_output))
        if demo["exit_code"] != 0:
            demo["status"] = "FAIL"
    else:
        tests = {
            "command": ["make", "test-all"],
            "status": "NOT_RUN",
            "reason": "Docker unavailable",
        }
        demo = {
            "command": ["./scripts/run_demo.sh", "--scripted"],
            "status": "NOT_RUN",
            "reason": "Docker unavailable",
        }
    checks = {"lint": lint, "tests": tests, "scripted_pipeline_demo": demo}
    summary = {
        "observed_at_utc": utc_now(),
        "status": "PASS" if all(item["status"] == "PASS" for item in checks.values()) else "FAIL",
        "checks": checks,
    }
    (OUTPUT / "verification_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": summary["status"],
                "tests": tests.get("passed_count"),
                "demo": demo["status"],
            }
        )
    )
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
