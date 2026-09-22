import sys

from semidebug.tools.process import run_process


def test_timeout_kills_group(tmp_path):
    result = run_process(
        [
            sys.executable,
            "-c",
            'import subprocess,time; subprocess.Popen(["sleep","30"]); time.sleep(30)',
        ],
        tmp_path,
        0.15,
        "test",
    )
    assert result.status == "timeout"
    assert result.duration_ms < 3000


def test_no_secrets_and_no_shell(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "should-not-propagate")
    result = run_process(
        [
            sys.executable,
            "-c",
            'import os,sys; print(os.getenv("OPENAI_API_KEY")); print(sys.argv[1])',
            "$(touch injected)",
        ],
        tmp_path,
        2,
        "test",
    )
    assert result.status == "pass"
    assert "None" in result.stdout
    assert "$(touch injected)" in result.stdout
    assert not (tmp_path / "injected").exists()


def test_output_is_bounded(tmp_path):
    result = run_process(
        [sys.executable, "-c", 'import sys; sys.stdout.write("x"*1000000)'], tmp_path, 2, "test"
    )
    assert result.status == "error"
    assert len(result.stdout) <= 262144


def test_missing_tool(tmp_path):
    result = run_process(["nonexistent-semidebug-tool"], tmp_path, 1, "test")
    assert result.status == "error"
