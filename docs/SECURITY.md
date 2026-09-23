# Execution and integrity boundaries

- The bundled fixtures are original, trusted HDL. Native mode is for trusted projects only.
- No shell commands or arbitrary manifest build commands. Validated identifier/path syntax prevents argument and Yosys script injection. Symlinks, traversal, extra dependencies and out-of-root paths are rejected.
- No source directory walk in context selection. Model requests contain only mutable RTL and explicitly visible target source or problem text. Internal gold/mutation definitions stay outside candidate workspaces. External reference/test files are present only in evaluator workspaces for official validation; their source and detailed mismatch output do not enter provider requests. This is an application data boundary, not protection from a malicious user who can modify the Python process.
- Unified diffs must apply exactly to existing mutable RTL, <=2 files and <=40 added/deleted lines. Tests, expected outputs, manifest, assertions, system-task manipulation, force/release, preprocessor/tool directives and hierarchical references cannot be changed. Lexical checks are defense in depth, not a proof against semantically malicious HDL.
- Immutable SHA256 maps are compared before/after validation. The original selected project files are also fingerprinted. Candidate failures do not modify source files. A missing completion marker, nonzero status, critical lint warning, timeout or failed regression cannot become success.
- The subprocess environment does not inherit LLM credentials. Captured output is bounded at 256 KiB per stream; each tool gets a bounded timeout, and the process group is killed on timeout/output overflow and on parent exit.
- `scripts/docker_run.sh` and every EDA worker use no network, 2 CPUs, 2 GiB memory, PID limit 128, dropped capabilities, no-new-privileges and a non-root user. The API call runs in the trusted host process; the API key is never mounted or forwarded to EDA containers.
- API keys come from `.env` or the host environment; `.env` is excluded from the Docker build context and submission ZIP. Prompts are not persisted; returned explanation/diff and relevant EDA logs are evidence and may contain source code.
- Package scanning detects common key formats/private keys; it is a heuristic, not a guarantee. Review what is shared. Repository visibility defaults to private.

## OpenAI API mode

The provider sends only manifest-selected context to Chat Completions Structured Outputs and requests one combined diagnosis and patch per attempt. The model receives no tools and cannot run EDA or inspect the filesystem. Successful HTTP completion is insufficient: the response must match the strict schema, the patch guard must accept the diff, and all independent validators must pass. Evaluator gold, hidden source and detailed official mismatch output remain outside API requests.
