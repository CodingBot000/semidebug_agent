# Submission document audit

Observed 2026-09-23 against commit `afc0582e08ba5463a0d4e35630dbebc7432028d4`. Numerical source priority: per-run records, aggregate JSON/CSV, generated summary, prose.

## Document inventory and ownership

| Path | Present purpose | V2 disposition |
|---|---|---|
| `README.md` | Project overview, result headline, quickstart | Keep short; link to measured V2 evidence after it exists. |
| `PORTFOLIO_EVIDENCE.md` | Problem, controls, results and limitations | Make the submission narrative and distinguish format from semantic retries. |
| `QUICKSTART.md` | Setup and commands | Keep as reproducibility guide; support ZIP extraction without requiring GitHub. |
| `docs/ARCHITECTURE.md` | Runtime modules and trust boundaries | Keep under `docs/`; clarify visible and hidden evaluator boundaries. |
| `docs/BENCHMARK.md` | Dataset, V1 methodology and measured results | Preserve V1; put changed V2 protocol/results in a new document. |
| `docs/CODEX_CLI.md` | Host CLI provider, authentication and usage | Keep provider-specific details here. |
| `docs/SECURITY.md` | Execution and integrity boundaries | Correct visibility description once hidden tests are isolated. |
| `docs/THIRD_PARTY.md` | Dependency attribution | Add pinned external benchmark provenance and redistribution choice. |
| `docs/DECISIONS.md`, `docs/RESEARCH.md` | Design decisions and upstream research | Preserve and append V2 decisions/research without rewriting history. |
| `docs/PROGRESS.md`, `docs/ISSUES.md`, `docs/issues/*.md`, `docs/FINAL_CHECKLIST.md` | Development history and V1 checks | Treat as internal history; omit from compact submission ZIP if links are adjusted. |
| `artifacts/README.md`, `results/README.md`, `results/**/summary.md` | Artifact/result interpretation | Preserve historical results; link only selected evidence in submission. |
| `docs/update/*.md` | V2 task and document instructions | Keep as project instructions; currently untracked. Exclude from reviewer ZIP. |

## Findings

1. **No verified numerical contradiction in headline V1 results.** `results/live_codex/summary.json` gives 30/30 final, 23/30 first attempt, 37 calls, 14,679.5 ms median. Public and holdout summaries give 24/24 and 6/6. README, portfolio and benchmark prose round consistently. The historical 95-test count is a recorded V1 check, not a fresh V2 test result.
2. **Feedback claims need precision.** Per-run records show seven retries, all after `Hunk truncated or invalid` guard rejection. V1 provides format-retry evidence, not a semantic-retry success. V2 documents must not infer semantic improvement from 23/30 to 30/30.
3. **Visibility language is incomplete.** `docs/BENCHMARK.md` and `docs/SECURITY.md` say testbench source is selected, but do not explain that current context selection includes regression sources and that the same testbench serves target and regression in existing cases. Correct after Phase A, and state V1's weaker protocol when discussing V1.
4. **Document duplication:** README, portfolio, benchmark, final checklist and progress repeat the same V1 counts. Keep a compact README table, methodology in benchmark, detailed evidence in portfolio/V2 evaluation, and history in internal notes.
5. **Plan path mismatch:** supplied plans refer to root `ARCHITECTURE.md` and `CODEX_SUBMISSION_DOC_REVIEW.md`; actual paths are `docs/ARCHITECTURE.md` and `docs/update/CODEX_SKHynix_Submission_Doc_Review_Instructions.md`. Use actual paths or add explicit reviewer copies in the ZIP.
6. **Private repository:** GitHub reports `CodingBot000/semidebug_agent` as private. A submission ZIP must be understandable and reproducible from its own contents; the clone URL is optional for reviewers without access.
7. **Relative links:** a filesystem check found no missing relative Markdown link targets in current files. It did not validate headings, external URLs or links after future file moves. Recheck on the packaged tree.
8. **Packaging:** current script recursively includes `evaluator/`, `results/`, `docs/` and tests. V2 ZIP needs a small explicit evidence set, no evaluator answers or internal journal, link and local-path checks, and attribution. The existing script already excludes `.env`, common caches and symlinks, scans common secret formats, enforces 50 MB and writes SHA256.

## Core submission message

The model proposes diagnoses and RTL patches; the application decides acceptance using an exact patch policy, independent EDA tools, evaluator-only regression and integrity checks. Show raw successful **and failed** attempts, distinguish internal from external cases and one-shot from full loop, and state that finite simulation is not formal proof.

## Editing order

Finish the evaluation boundary and freeze the external selection protocol before rewriting result headlines. Then write `docs/V2_EVALUATION.md`, update architecture/benchmark/security/attribution, shorten README/portfolio, add `SUBMISSION_GUIDE.md`, and validate the extracted ZIP. Preserve historical documents and V1 result files.

## Resolution (2026-09-23)

The V2 evaluation and external selected denominator now exist. README, portfolio, quickstart, architecture, benchmark, security and third-party attribution were updated against the raw results. `results/README.md` and the historical pre-CLI note in `docs/DECISIONS.md` were corrected after this audit identified stale wording. The V2 ZIP includes selected evidence and primary documents while excluding `docs/internal/`, `docs/update/` and external reference files. Its package link scan passed, and a clean extraction passed bootstrap, replay, scripted EDA demo, lint and 106 tests. The repository remains private; the ZIP is the independent reviewer entry point.
