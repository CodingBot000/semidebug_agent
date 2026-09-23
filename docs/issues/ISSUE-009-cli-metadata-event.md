# ISSUE-009 — CLI informational event mistaken for tool use

- Discovered: 2026-09-23 during the first successful model response.
- Status: Resolved.
- Symptom: a completed CLI turn with valid structured output was rejected by the adapter as an attempted tool call.
- Cause: CLI emits an `item.completed` event of type `error` for a model-catalog metadata warning even when inference succeeds. The initial fail-closed event allowlist treated that as a tool event.
- Resolution: recognize diagnostic `error` and `structured_output` as non-tool events, record item types, and continue requiring successful process exit, turn.completed, validated output and zero actual tool events. Command/MCP/file-change/other tool events remain rejected.
- Verification: mocked diagnostic event test and successful real GPT-6 Sol FIFO demo (tool_events=0, actual item types error/agent_message). The rejected pilot is preserved in artifacts/ and is excluded from performance measurements.
