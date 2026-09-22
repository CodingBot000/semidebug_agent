# ISSUE-007 — Clean checkout outside Colima shared mounts

- Discovered: 2026-09-22 UTC, fresh-clone reproduction.
- Status: Resolved.
- Symptom: a host clone under /tmp installed and Docker-built successfully, but bind-mounted runtime saw an empty project; pytest found no tests and the CLI could not import semidebug.
- Reproduction: active Docker context `colima`; mounting macOS /tmp or /private/tmp returned an empty directory inside the VM.
- Cause: Colima's default shared filesystem covers the user home, not this host temporary directory. Docker build transfers its context and therefore succeeded; runtime bind mounts reference the VM filesystem.
- Impact: initial clean-checkout EDA reproduction failed. Earlier runs from the shared project directory were valid.
- Resolution: repeat fresh clone under the shared user home cache; wrapper now checks the project mount and gives an actionable error before launching any command. No EDA tests or expected results changed.
- Verification: explicit unshared-path check plus fresh-clone full suite, demo, lint and package results in PROGRESS.md.
