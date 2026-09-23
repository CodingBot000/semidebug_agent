import json
from pathlib import Path

import pytest

from semidebug.config import Settings
from semidebug.llm.base import ProviderError
from semidebug.llm.codex import CodexCLIProvider, cli_environment
from semidebug.models import Analysis, PatchProposal, ValidationResult

SUGGESTION = {
    "analysis": {
        "hypotheses": [
            {
                "summary": "Boundary error",
                "likely_files": ["rtl/a.v"],
                "likely_lines": [1],
                "reasoning": "Simulation assertion",
                "confidence": 0.9,
                "evidence_ids": ["baseline:simulation"],
            }
        ]
    },
    "patch": {
        "explanation": "Fix boundary",
        "unified_diff": "diff\n",
        "expected_effect": "Correct full flag",
        "risks": [],
    },
}
REQUEST = {"system": "Analyze RTL", "context": {"sources": {"rtl/a.v": "x"}}}


def setup_provider(monkeypatch, *, status="pass", tool_call=False, valid=True):
    monkeypatch.setattr("semidebug.llm.codex.shutil.which", lambda _: "/usr/local/bin/codex")
    monkeypatch.setattr("semidebug.llm.codex.codex_auth_status", lambda: True)
    commands = []

    def run(command, cwd, timeout, tool, **kwargs):
        if tool == "codex-version":
            return ValidationResult(
                tool=tool, command=command, exit_code=0, status="pass", stdout="codex-cli 0.156.1"
            )
        commands.append((command, kwargs))
        Path(command[command.index("--output-last-message") + 1]).write_text(
            json.dumps(SUGGESTION) if valid else "invalid"
        )
        events = [
            {"type": "item.completed", "item": {"type": "error", "message": "metadata warning"}},
            {
                "type": "turn.completed",
                "usage": {"input_tokens": 100, "cached_input_tokens": 25, "output_tokens": 40},
            },
        ]
        if tool_call:
            events.insert(0, {"type": "item.completed", "item": {"type": "command_execution"}})
        return ValidationResult(
            tool="codex",
            command=command,
            exit_code=0,
            status=status,
            stdout="\n".join(json.dumps(e) for e in events),
        )

    monkeypatch.setattr("semidebug.llm.codex.run_process", run)
    return CodexCLIProvider(Settings()), commands


def test_combined_response_is_one_low_reasoning_call(monkeypatch):
    provider, commands = setup_provider(monkeypatch)
    analysis = provider.generate_structured(REQUEST, Analysis)
    context = {**REQUEST["context"], "hypothesis": analysis.hypotheses[0].model_dump()}
    proposal = provider.generate_structured({"system": "Patch", "context": context}, PatchProposal)
    assert proposal.explanation == "Fix boundary"
    assert provider.calls == 1 and len(commands) == 1
    assert (provider.input_tokens, provider.cached_input_tokens, provider.output_tokens) == (
        100,
        25,
        40,
    )
    command, kwargs = commands[0]
    assert command[command.index("--model") + 1] == "gpt-6-sol"
    assert 'model_reasoning_effort="low"' in command
    assert "--ignore-user-config" in command and "--ephemeral" in command
    assert "shell_tool" in command and "plugins" in command
    assert kwargs["input_text"] and "auth" not in kwargs["input_text"]


def test_cli_environment_does_not_inherit_api_credentials(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "private")
    monkeypatch.setenv("CODEX_API_KEY", "private")
    monkeypatch.setenv("CODEX_ACCESS_TOKEN", "private")
    env = cli_environment()
    assert not any(key in env for key in ["OPENAI_API_KEY", "CODEX_API_KEY", "CODEX_ACCESS_TOKEN"])
    assert env["HOME"]


@pytest.mark.parametrize("kwargs", [{"tool_call": True}, {"valid": False}, {"status": "timeout"}])
def test_codex_failures_are_rejected(monkeypatch, kwargs):
    provider, _ = setup_provider(monkeypatch, **kwargs)
    with pytest.raises(ProviderError):
        provider.generate_structured(REQUEST, Analysis)
    assert provider.calls == 1


def test_cached_patch_rejects_changed_context(monkeypatch):
    provider, _ = setup_provider(monkeypatch)
    provider.generate_structured(REQUEST, Analysis)
    with pytest.raises(ProviderError):
        provider.generate_structured({"context": {"different": True}}, PatchProposal)


def test_auth_required(monkeypatch):
    monkeypatch.setattr("semidebug.llm.codex.codex_auth_status", lambda: False)
    with pytest.raises(ProviderError, match="codex login"):
        CodexCLIProvider(Settings())
