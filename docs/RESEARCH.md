# Phase 0 research — 2026-09-22 UTC

## Environment
macOS x86_64, Darwin 23.6, Python 3.13.1, pip points at 3.12 (use uv to avoid mismatch), uv 0.12.5. Docker daemon 29.5.2 is reachable. Native Icarus/Verilator/Yosys are absent. Homebrew 6.0.18 metadata lists Icarus 13.0, Verilator 5.052, Yosys 0.69. These are latest discovered releases, not claims about the versions installed in our image. The final doctor output records actual tool versions.

## Verified primary references and decisions
- [Icarus flags](https://steveicarus.github.io/iverilog/usage/command_line_flags.html): use `-g2012`, explicit top and output file. Compiler nonzero exit means failure.
- [VVP flags](https://steveicarus.github.io/iverilog/usage/vvp_flags.html): `-N` treats `$stop` as failure. Testbenches use `$fatal(1, ...)` and an explicit completion marker; exit zero alone is insufficient.
- [Icarus releases](https://github.com/steveicarus/iverilog/releases): v13_0 discovered. Native alternative: `brew install icarus-verilog`.
- [Verilator installation](https://verilator.org/guide/latest/install.html): distribution packages are supported but can lag upstream. Native alternative: `brew install verilator`.
- [Verilator flags](https://verilator.org/guide/latest/exe_verilator.html) and [warning categories](https://verilator.org/guide/latest/warnings.html): lint RTL separately from behavioral testbenches; retain all warning output. Fatal policy includes width, latch, missing/undriven pins and multiple drivers; stylistic warnings remain visible but nonfatal.
- [Yosys read_verilog](https://yosyshq.readthedocs.io/projects/yosys/en/latest/cmd/read_verilog.html): built-in `-sv` covers a subset of SystemVerilog. Restrict fixtures to synthesizable Verilog with basic SV testbenches. Native alternative: `brew install yosys`.
- [Yosys check](https://yosyshq.readthedocs.io/projects/yosys/en/latest/cmd/check.html): use `hierarchy -check -top`, `proc`, `opt`, `check -assert`. This is structural sanity, not physical implementation or formal equivalence.

## Orchestration and provider
An explicit Python state machine makes attempts, rollback, refusal, validation and termination auditable with minimal dependencies. LangGraph would add dependency/version complexity without a current need for distributed graphs or checkpoint orchestration. The provider returns Pydantic validated hypotheses and unified diffs. OpenAI compatible Chat Completions supports strict JSON schema where available; JSON mode is an explicit compatibility setting. No tool calling is necessary: the application owns every tool invocation. Bounded HTTP retry, timeout, usage counters and externally configured cost rates are required.

## Sandbox
Docker is the canonical reproducible toolchain. Offline runs use no network, dropped capabilities, no-new-privileges, memory/CPU/PID limits, and only the project/artifact mounts. Native process execution enforces an environment allowlist, process-group timeout and bounded captured logs, but is not a hostile-code security sandbox. Live API calls require network; do not execute untrusted RTL in that mode. Gold/evaluator files never enter the agent workspace or provider prompt.

Additional checked primary references:
- [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs): schema responses, refusals, incomplete outputs; application validation remains mandatory.
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/): strict model contracts and JSON schema generation.
- [HTTPX timeouts](https://www.python-httpx.org/advanced/timeouts/): explicit network timeouts.
- [uv Docker integration](https://docs.astral.sh/uv/guides/integration/docker/): locked environments and project installation.
