"""Validated contracts shared by the evaluator, tools, and repair loop."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ValidationResult(Model):
    tool: str
    command: list[str]
    exit_code: int
    status: Literal["pass", "fail", "timeout", "error"]
    stdout: str = ""
    stderr: str = ""
    duration_ms: int = 0


class ValidationBundle(Model):
    results: dict[str, ValidationResult] = Field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return bool(self.results) and all(r.status == "pass" for r in self.results.values())

    @property
    def infrastructure_error(self) -> bool:
        return any(r.status == "error" for r in self.results.values())


class TestSpec(Model):
    name: str = Field(pattern=r"^[A-Za-z][A-Za-z0-9_]*$")
    top: str = Field(pattern=r"^[A-Za-z_][A-Za-z0-9_]*$")
    sources: list[str] = Field(min_length=1)
    plusargs: list[str] = Field(default_factory=list)
    success_mode: Literal["semidebug_pass", "chipbench_mismatches"] = "semidebug_pass"


class Case(Model):
    id: str = Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
    category: str
    design_top: str = Field(pattern=r"^[A-Za-z_][A-Za-z0-9_]*$")
    mutable: list[str] = Field(min_length=1, max_length=20)
    immutable: list[str] = Field(min_length=1)
    prompt_visible: list[str] | None = None
    target: TestSpec
    regression: list[TestSpec] = Field(min_length=1)
    timeout_sec: float = Field(default=10, gt=0, le=120)


class EvidenceItem(Model):
    id: str
    tool: str
    status: str
    message: str


class Hypothesis(Model):
    summary: str
    likely_files: list[str]
    likely_lines: list[int]
    reasoning: str
    confidence: float = Field(ge=0, le=1)
    evidence_ids: list[str]


class Analysis(Model):
    hypotheses: list[Hypothesis] = Field(min_length=1, max_length=3)


class PatchProposal(Model):
    explanation: str
    unified_diff: str = Field(min_length=1, max_length=50000)
    expected_effect: str
    risks: list[str]


class PatchAttempt(Model):
    iteration: int
    hypothesis: Hypothesis | None = None
    proposal: PatchProposal | None = None
    guard_error: str | None = None
    validation: ValidationBundle | None = None
    regression: ValidationBundle | None = None
    retry_reason: (
        Literal[
            "PATCH_PARSE_RETRY",
            "PATCH_GUARD_RETRY",
            "COMPILE_RETRY",
            "SIMULATION_RETRY",
            "LINT_RETRY",
            "SYNTHESIS_RETRY",
            "REGRESSION_RETRY",
            "REPEATED_PATCH_STOP",
            "REPEATED_FAILURE_STOP",
            "LLM_ERROR",
            "INFRA_ERROR",
        ]
        | None
    ) = None


class RunState(Model):
    run_id: str
    case_id: str
    category: str
    provider: str
    model: str
    reasoning_effort: str | None = None
    billing_mode: str | None = None
    cached_input_tokens: int = 0
    provider_metadata: dict = Field(default_factory=dict)
    iteration: int = 0
    max_iterations: int
    project_root: str
    mutable_files: list[str]
    immutable_files: list[str]
    baseline: ValidationBundle | None = None
    current_validation: ValidationBundle | None = None
    evidence: list[EvidenceItem] = Field(default_factory=list)
    hypotheses: list[Hypothesis] = Field(default_factory=list)
    patch_attempts: list[PatchAttempt] = Field(default_factory=list)
    final_status: str = "RUNNING"
    failure_reason: str | None = None
    immutable_before: dict[str, str] = Field(default_factory=dict)
    immutable_after: dict[str, str] = Field(default_factory=dict)
    integrity_pass: bool = False
    success: bool = False
    regression_pass: bool = False
    duration_ms: int = 0
    llm_calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost: float | None = None
    price_source: str | None = None
