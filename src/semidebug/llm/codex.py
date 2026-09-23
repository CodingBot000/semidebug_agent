"""Stateless structured inference using the user's normal ChatGPT CLI login.
No auth file is read/copied by this adapter. Codex owns authentication.
"""

import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path

from semidebug.agent.prompts import PATCHER
from semidebug.config import Settings
from semidebug.llm.base import ProviderError, T
from semidebug.models import Analysis, Model, PatchProposal
from semidebug.tools.process import run_process

DISABLED_FEATURES = [
    "shell_tool",
    "unified_exec",
    "plugins",
    "apps",
    "multi_agent",
    "browser_use",
    "browser_use_external",
    "computer_use",
    "image_generation",
    "view_image",
    "hooks",
    "skill_search",
    "workspace_dependencies",
    "code_mode_host",
]


class RepairSuggestion(Model):
    analysis: Analysis
    patch: PatchProposal


def cli_environment() -> dict[str, str]:
    # Preserve normal home/login lookup; explicitly omit API-key and access-token overrides.
    keys = ("PATH", "HOME", "TMPDIR", "LANG", "LC_ALL", "CODEX_HOME")
    return {key: os.environ[key] for key in keys if key in os.environ}


def context_key(context: dict) -> str:
    context = {k: v for k, v in context.items() if k != "hypothesis"}
    return hashlib.sha256(json.dumps(context, sort_keys=True).encode()).hexdigest()


def codex_auth_status() -> bool:
    binary = shutil.which("codex")
    if not binary:
        return False
    result = run_process(
        [binary, "login", "status"], Path.home(), 15, "codex-auth", environment=cli_environment()
    )
    return result.status == "pass" and "ChatGPT" in result.stdout + result.stderr


class CodexCLIProvider:
    name = "live-codex-cli"
    billing_mode = "chatgpt-subscription"

    def __init__(self, settings: Settings):
        self.binary = shutil.which("codex")
        if not self.binary or not codex_auth_status():
            raise ProviderError(
                "Run `codex login` with ChatGPT on the host before using --provider codex"
            )
        version = run_process(
            [self.binary, "--version"],
            Path.home(),
            10,
            "codex-version",
            environment=cli_environment(),
        )
        self.cli_version = version.stdout.strip()
        self.model = settings.codex_model
        self.reasoning_effort = settings.reasoning_effort
        self.timeout = settings.codex_timeout
        self.calls = self.input_tokens = self.output_tokens = self.cached_input_tokens = 0
        self.invocations = []
        self.pending = None

    def generate_structured(self, request: dict, schema: type[T]) -> T:
        key = context_key(request["context"])
        if schema is PatchProposal:
            if not self.pending or self.pending[0] != key:
                raise ProviderError("Codex combined response missing or context changed")
            proposal = self.pending[1]
            self.pending = None
            return schema.model_validate(proposal.model_dump())
        if schema is not Analysis:
            raise ProviderError("Codex provider expects Analysis followed by PatchProposal")
        self.pending = None
        result = self._invoke(request)
        self.pending = (key, result.patch)
        return schema.model_validate(result.analysis.model_dump())

    def _invoke(self, request: dict) -> RepairSuggestion:
        with tempfile.TemporaryDirectory(prefix="semidebug-inference-") as temporary:
            cwd = Path(temporary)
            schema_path, result_path = cwd / "schema.json", cwd / "answer.json"
            instructions_path = cwd / "instructions.md"
            instructions_path.write_text(
                "You are a stateless RTL diagnosis and minimal patch generator. "
                "Use only evidence and source provided in the user message. "
                "Do not use tools, inspect the filesystem or execute commands. "
                "Return the required JSON schema only. Never claim validation passed without evidence."
            )
            schema_path.write_text(json.dumps(RepairSuggestion.model_json_schema()))
            command = [
                self.binary,
                "exec",
                "--ignore-user-config",
                "--ephemeral",
                "--skip-git-repo-check",
                "--sandbox",
                "read-only",
                "--json",
                "--model",
                self.model,
                "--cd",
                str(cwd),
                "--color",
                "never",
                "--output-schema",
                str(schema_path),
                "--output-last-message",
                str(result_path),
            ]
            for feature in DISABLED_FEATURES:
                command += ["--disable", feature]
            for setting in [
                f'model_reasoning_effort="{self.reasoning_effort}"',
                'approval_policy="never"',
                'forced_login_method="chatgpt"',
                'web_search="disabled"',
                "project_doc_max_bytes=0",
                'personality="none"',
                "skills.max_context_tokens=1",
                "model_instructions_file=" + json.dumps(str(instructions_path)),
            ]:
                command += ["-c", setting]
            command += ["-"]
            context = json.loads(json.dumps(request["context"]))
            for evidence in context.get("evidence", []):
                if evidence.get("status") == "pass":
                    evidence["message"] = (
                        "Independent validator passed; verbose success log omitted."
                    )
            for attempt in context.get("previous_attempts", []):
                for stage in ("validation", "regression"):
                    for result in (attempt.get(stage) or {}).get("results", {}).values():
                        if result.get("status") == "pass":
                            result["stdout"] = result["stderr"] = ""
            prompt = (
                "You are a stateless RTL diagnosis and patch proposal engine. Do not use tools, "
                "read files or run commands. All permitted evidence is below. Return ONLY the "
                "required JSON: analysis (1-3 hypotheses), and patch for the most likely hypothesis.\n"
                + request["system"]
                + "\n"
                + PATCHER
                + "\nINPUT_JSON:\n"
                + json.dumps(context)
            )
            self.calls += 1
            process = run_process(
                command,
                cwd,
                self.timeout,
                "codex",
                environment=cli_environment(),
                input_text=prompt,
            )
            record = {
                "model": self.model,
                "cli_version": self.cli_version,
                "prompt_characters": len(prompt),
                "reasoning_effort": self.reasoning_effort,
                "billing_mode": self.billing_mode,
                "duration_ms": process.duration_ms,
                "process_status": process.status,
                "tool_events": 0,
                "item_types": [],
                "input_tokens": 0,
                "cached_input_tokens": 0,
                "output_tokens": 0,
            }
            completed = False
            for line in process.stdout.splitlines():
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                if event.get("type") == "turn.completed":
                    completed = True
                    usage = event.get("usage") or {}
                    for field in ["input_tokens", "cached_input_tokens", "output_tokens"]:
                        record[field] += int(usage.get(field, 0))
                if event.get("type") in {"item.started", "item.completed"}:
                    item_type = event.get("item", {}).get("type")
                    if item_type not in record["item_types"]:
                        record["item_types"].append(item_type)
                    if item_type not in {
                        "agent_message",
                        "reasoning",
                        "todo_list",
                        "structured_output",
                        "error",
                    }:
                        record["tool_events"] += 1
            for field in ["input_tokens", "cached_input_tokens", "output_tokens"]:
                setattr(self, field, getattr(self, field) + record[field])
            self.invocations.append(record)
            if process.status != "pass":
                # Never persist stderr, auth storage, session data or raw diagnostic content.
                raise ProviderError(
                    f"Codex CLI {process.status} (exit {process.exit_code}); check login, model and usage limits"
                )
            if record["tool_events"]:
                raise ProviderError(
                    "Codex attempted a tool call; reject inference to preserve benchmark isolation"
                )
            if not completed or not result_path.is_file():
                raise ProviderError("Codex did not produce a completed structured response")
            try:
                return RepairSuggestion.model_validate_json(result_path.read_text())
            except ValueError:
                raise ProviderError("Codex returned malformed structured output") from None
