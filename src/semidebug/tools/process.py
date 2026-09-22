"""No shell, no inherited credentials, bounded output, whole process-group timeout."""

import os
import signal
import subprocess
import threading
import time
from pathlib import Path

from semidebug.models import ValidationResult

ENV_KEYS = ("PATH", "SYSTEMROOT", "TMPDIR", "TMP", "TEMP")
MAX_OUTPUT = 262144


def run_process(command: list[str], cwd: Path, timeout: float, tool: str) -> ValidationResult:
    if not command or timeout <= 0:
        raise ValueError("Nonempty argv and positive timeout required")
    started = time.monotonic()
    env = {key: os.environ[key] for key in ENV_KEYS if key in os.environ}
    env.update({"LANG": "C", "LC_ALL": "C", "HOME": str(cwd)})
    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            env=env,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
    except OSError as exc:
        return ValidationResult(
            tool=tool,
            command=command,
            exit_code=-1,
            status="error",
            stderr=f"{type(exc).__name__}: executable unavailable",
        )
    buffers = [bytearray(), bytearray()]
    overflow = threading.Event()

    def drain(stream, buffer):
        while block := stream.read(8192):
            remaining = MAX_OUTPUT - len(buffer)
            buffer.extend(block[:remaining])
            if len(block) > remaining:
                overflow.set()
        stream.close()

    threads = [
        threading.Thread(target=drain, args=(s, b), daemon=True)
        for s, b in zip((process.stdout, process.stderr), buffers, strict=True)
    ]
    for thread in threads:
        thread.start()
    status = None
    while process.poll() is None:
        if overflow.is_set() or time.monotonic() - started >= timeout:
            status = "error" if overflow.is_set() else "timeout"
            break
        time.sleep(0.01)
    # Also kill background descendants which may keep the pipes open after parent exit.
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()
    for thread in threads:
        thread.join(timeout=2)
    stdout, stderr = [bytes(b).decode("utf-8", errors="replace") for b in buffers]
    if overflow.is_set():
        status = "error"
        stderr += "\nOutput limit exceeded."
    if status == "timeout":
        stderr += "\nProcess group killed after timeout."
    return ValidationResult(
        tool=tool,
        command=command,
        exit_code=process.returncode,
        status=status or ("pass" if process.returncode == 0 else "fail"),
        stdout=stdout,
        stderr=stderr,
        duration_ms=int((time.monotonic() - started) * 1000),
    )
