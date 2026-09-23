import hashlib
import json
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from semidebug.agent.prompts import ANALYZER, PATCHER
from semidebug.benchmark.loader import load_case
from semidebug.config import Settings
from semidebug.context.selector import evidence_from, select_context
from semidebug.llm.base import LLMProvider, ProviderError
from semidebug.models import Analysis, EvidenceItem, PatchAttempt, PatchProposal, RunState
from semidebug.patch.apply import apply_patches
from semidebug.patch.guard import guard_patch
from semidebug.patch.parser import PatchError, parse_diff
from semidebug.report.renderer import save_report
from semidebug.tools.validation import regress, validate
from semidebug.tools.workspace import copy_project, hashes


def dump(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value.model_dump() if hasattr(value, "model_dump") else value, indent=2) + "\n"
    )


def save_bundle(directory, bundle):
    dump(directory / "validation.json", bundle)
    for name, result in bundle.results.items():
        (directory / f"{name}.log").write_text(
            f"argv: {json.dumps(result.command)}\nstatus: {result.status}\nexit: {result.exit_code}\n"
            + result.stdout
            + "\n"
            + result.stderr
        )


def provider_history(attempts: list[PatchAttempt]) -> list[dict]:
    """Return retry context without evaluator-only commands or expected values."""
    entries = []
    for attempt in attempts:
        entry = attempt.model_dump()
        if entry["validation"]:
            for result in entry["validation"]["results"].values():
                result["stdout"] = result["stdout"][-4000:]
                result["stderr"] = result["stderr"][-4000:]
        if entry["regression"]:
            entry["regression"] = {
                "results": {
                    f"check_{index}": {"tool": result["tool"], "status": result["status"]}
                    for index, result in enumerate(entry["regression"]["results"].values(), 1)
                }
            }
        entries.append(entry)
    return entries


def validation_retry_reason(bundle) -> str | None:
    for check in ("compile", "simulation", "lint", "synthesis"):
        result = bundle.results.get(check)
        if result and result.status != "pass":
            return f"{check.upper()}_RETRY"
    return None


def repair(
    project: Path, provider: LLMProvider, output: Path, settings: Settings | None = None
) -> RunState:
    settings = settings or Settings()
    if not 1 <= settings.max_iterations <= 10:
        raise ValueError("max_iterations must be 1..10")
    project = project.resolve()
    case = load_case(project)
    started = time.monotonic()
    initial_usage = (provider.calls, provider.input_tokens, provider.output_tokens)
    initial_cached = getattr(provider, "cached_input_tokens", 0)
    initial_records = len(getattr(provider, "invocations", []))
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:8]
    directory = output / run_id
    directory.mkdir(parents=True, exist_ok=False)
    immutable = sorted(set(case.immutable + ["case.json"]))
    files = sorted(set(case.mutable + immutable))
    original_all = hashes(project, files)
    state = RunState(
        run_id=run_id,
        case_id=case.id,
        category=case.category,
        provider=provider.name,
        model=provider.model,
        reasoning_effort=getattr(provider, "reasoning_effort", None),
        billing_mode=getattr(provider, "billing_mode", None),
        max_iterations=settings.max_iterations,
        project_root=project.name,
        mutable_files=case.mutable,
        immutable_files=immutable,
        immutable_before=hashes(project, immutable),
    )

    def event(name, summary="", status=None):
        with (directory / "events.jsonl").open("a") as stream:
            stream.write(
                json.dumps(
                    {
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "run_id": run_id,
                        "case_id": case.id,
                        "iteration": state.iteration,
                        "event_type": name,
                        "status": status,
                        "summary": summary,
                    }
                )
                + "\n"
            )
        dump(directory / "run.json", state)

    def integrity(workspace):
        if (
            hashes(workspace, immutable) != state.immutable_before
            or hashes(project, files) != original_all
        ):
            raise PatchError("Project or immutable files changed outside permitted patch")

    def validation(workspace, regression=False):
        function = regress if regression else validate
        if settings.eda_runtime == "native":
            return function(workspace, case)
        from semidebug.tools.docker import docker_validation

        return docker_validation(workspace, "regression" if regression else "target", case)

    work_parent = None
    if settings.eda_runtime == "docker":
        work_parent = Path.home() / ".cache" / "semidebug" / "workspaces"
        work_parent.mkdir(parents=True, exist_ok=True)
    try:
        event("LOAD_PROJECT")
        with tempfile.TemporaryDirectory(prefix="semidebug-", dir=work_parent) as temporary:
            root = Path(temporary)
            baseline_root = root / "baseline"
            copy_project(project, baseline_root, files)
            event("BASELINE")
            state.baseline = validation(baseline_root)
            state.current_validation = state.baseline
            save_bundle(directory / "baseline", state.baseline)
            integrity(baseline_root)
            state.evidence = evidence_from(state.baseline, "baseline")
            if state.baseline.infrastructure_error:
                state.final_status = "INFRA_ERROR"
                state.failure_reason = (
                    "Required EDA executable unavailable or output limit exceeded"
                )
            elif state.baseline.passed:
                baseline_regression = validation(baseline_root, regression=True)
                save_bundle(directory / "baseline" / "regression", baseline_regression)
                integrity(baseline_root)
                if baseline_regression.infrastructure_error:
                    state.final_status = "INFRA_ERROR"
                    state.failure_reason = "Baseline regression infrastructure failure"
                elif baseline_regression.passed:
                    state.final_status = "ALREADY_PASS"
                    state.regression_pass = True
                else:
                    state.evidence += evidence_from(
                        baseline_regression, "baseline-regression", evaluator_only=True
                    )
            seen = set()
            rejected = 0
            fingerprints = set()
            for iteration in range(1, settings.max_iterations + 1):
                if state.final_status != "RUNNING":
                    break
                state.iteration = iteration
                event("COLLECT_EVIDENCE")
                context = select_context(baseline_root, case, state.evidence)
                context["previous_attempts"] = provider_history(state.patch_attempts)
                event("ANALYZE")
                analysis = provider.generate_structured(
                    {"system": ANALYZER, "context": context}, Analysis
                )
                hypothesis = analysis.hypotheses[0]
                state.hypotheses.extend(analysis.hypotheses)
                context["hypothesis"] = hypothesis.model_dump()
                attempt = PatchAttempt(iteration=iteration, hypothesis=hypothesis)
                state.patch_attempts.append(attempt)
                attempt_dir = directory / "attempts" / f"{iteration:02d}"
                dump(attempt_dir / "hypothesis.json", hypothesis)
                event("GENERATE_PATCH")
                proposal = provider.generate_structured(
                    {"system": PATCHER, "context": context}, PatchProposal
                )
                attempt.proposal = proposal
                (attempt_dir / "patch.diff").write_text(proposal.unified_diff)
                digest = hashlib.sha256(proposal.unified_diff.encode()).hexdigest()
                if digest in seen:
                    attempt.retry_reason = "REPEATED_PATCH_STOP"
                    state.final_status = "REPEATED_PATCH"
                    state.failure_reason = "Provider repeated a previous diff"
                    event("FAILED", state.failure_reason)
                    break
                seen.add(digest)
                candidate = root / f"attempt-{iteration}"
                copy_project(project, candidate, files)
                event("GUARD_PATCH")
                try:
                    parse_diff(proposal.unified_diff)
                    patches = guard_patch(proposal.unified_diff, candidate, case)
                    event("APPLY_PATCH")
                    apply_patches(candidate, patches)
                except (PatchError, ValueError) as exc:
                    attempt.guard_error = str(exc)
                    try:
                        parse_diff(proposal.unified_diff)
                    except PatchError:
                        attempt.retry_reason = "PATCH_PARSE_RETRY"
                    else:
                        attempt.retry_reason = "PATCH_GUARD_RETRY"
                    rejected += 1
                    state.evidence = evidence_from(state.baseline, "baseline") + [
                        EvidenceItem(
                            id=f"guard:{iteration}",
                            tool="patch_guard",
                            status="fail",
                            message=str(exc),
                        )
                    ]
                    event("PATCH_REJECTED", str(exc))
                    if rejected >= 2:
                        state.final_status = "PATCH_REJECTED"
                        state.failure_reason = "Two consecutive invalid patches"
                    else:
                        event("SHOULD_RETRY", "Patch rejected; baseline remains unchanged")
                    continue
                rejected = 0
                integrity(candidate)
                event("VALIDATE_TARGET")
                attempt.validation = validation(candidate)
                state.current_validation = attempt.validation
                save_bundle(attempt_dir, attempt.validation)
                integrity(candidate)
                state.evidence = evidence_from(attempt.validation, f"attempt-{iteration}")
                if attempt.validation.infrastructure_error:
                    attempt.retry_reason = "INFRA_ERROR"
                    state.final_status = "INFRA_ERROR"
                    state.failure_reason = "Validation infrastructure failure"
                    break
                if attempt.validation.passed:
                    event("VALIDATE_REGRESSION")
                    attempt.regression = validation(candidate, regression=True)
                    save_bundle(attempt_dir / "regression", attempt.regression)
                    integrity(candidate)
                    if attempt.regression.passed:
                        state.final_status = "FIXED"
                        state.success = state.regression_pass = True
                        dump(directory / "final" / "regression.json", attempt.regression)
                        (directory / "final" / "patch.diff").write_text(proposal.unified_diff)
                        for name in case.mutable:
                            destination = directory / "final" / name
                            destination.parent.mkdir(parents=True, exist_ok=True)
                            destination.write_bytes((candidate / name).read_bytes())
                        event("SUCCESS", "All independent validators and regression passed")
                        break
                    attempt.retry_reason = "REGRESSION_RETRY"
                    state.evidence += evidence_from(
                        attempt.regression, f"regression-{iteration}", evaluator_only=True
                    )
                    if attempt.regression.infrastructure_error:
                        attempt.retry_reason = "INFRA_ERROR"
                        state.final_status = "INFRA_ERROR"
                        state.failure_reason = "Regression infrastructure failure"
                        break
                else:
                    attempt.retry_reason = validation_retry_reason(attempt.validation)
                fingerprint = (
                    hypothesis.summary,
                    tuple(
                        (e.tool, e.status, e.message) for e in state.evidence if e.status != "pass"
                    ),
                )
                if fingerprint in fingerprints:
                    attempt.retry_reason = "REPEATED_FAILURE_STOP"
                    state.final_status = "REPEATED_FAILURE"
                    state.failure_reason = "Repeated hypothesis and failure evidence"
                    break
                fingerprints.add(fingerprint)
                event("SHOULD_RETRY", "Validation failed; next patch starts from baseline")
            if state.final_status == "RUNNING":
                state.final_status = "MAX_RETRY"
                state.failure_reason = "Iteration budget exhausted"
            integrity(baseline_root)
            state.immutable_after = hashes(baseline_root, immutable)
            state.integrity_pass = True
    except ProviderError as exc:
        if state.patch_attempts and state.patch_attempts[-1].proposal is None:
            state.patch_attempts[-1].retry_reason = "LLM_ERROR"
        state.final_status = "LLM_ERROR"
        state.failure_reason = str(exc)
    except PatchError as exc:
        state.final_status = "INTEGRITY_ERROR"
        state.failure_reason = str(exc)
        state.success = state.regression_pass = False
    except (OSError, ValueError) as exc:
        state.final_status = "INFRA_ERROR"
        state.failure_reason = f"{type(exc).__name__}: invalid workspace or data"
        state.success = state.regression_pass = False
    finally:
        try:
            original_unchanged = hashes(project, files) == original_all
            if state.final_status == "LLM_ERROR":
                state.immutable_after = hashes(project, immutable)
                state.integrity_pass = original_unchanged
            if not original_unchanged:
                state.final_status = "INTEGRITY_ERROR"
                state.failure_reason = "Original project changed during execution"
                state.integrity_pass = state.success = state.regression_pass = False
        except (OSError, ValueError):
            state.final_status = "INTEGRITY_ERROR"
            state.failure_reason = "Original project unavailable during final integrity check"
            state.integrity_pass = state.success = state.regression_pass = False
        state.duration_ms = int((time.monotonic() - started) * 1000)
        state.llm_calls = provider.calls - initial_usage[0]
        state.input_tokens = provider.input_tokens - initial_usage[1]
        state.output_tokens = provider.output_tokens - initial_usage[2]
        state.cached_input_tokens = getattr(provider, "cached_input_tokens", 0) - initial_cached
        state.provider_metadata = (
            {"invocations": getattr(provider, "invocations", [])[initial_records:]}
            if hasattr(provider, "invocations")
            else {}
        )
        if (
            state.billing_mode == "openai-api"
            and settings.input_price is not None
            and settings.cached_input_price is not None
            and settings.output_price is not None
            and settings.price_source
        ):
            uncached_input_tokens = max(0, state.input_tokens - state.cached_input_tokens)
            state.estimated_cost = (
                uncached_input_tokens * settings.input_price
                + state.cached_input_tokens * settings.cached_input_price
                + state.output_tokens * settings.output_price
            ) / 1_000_000
            state.price_source = settings.price_source
        if not state.success:
            event(
                "FAILED" if state.final_status != "ALREADY_PASS" else "ALREADY_PASS",
                state.failure_reason or "",
                state.final_status,
            )
        dump(directory / "run.json", state)
        dump(directory / "result.json", state)
        dump(directory / "final" / "metrics.json", state)
        save_report(state, directory)
    return state
