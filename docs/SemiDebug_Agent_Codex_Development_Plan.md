# SemiDebug Agent — Codex End-to-End Development Plan

> **목적:** SK하이닉스 AI 해커톤 2026 지원 포트폴리오용으로, AI가 RTL/Verilog 오류를 분석하고 최소 패치를 생성한 뒤 실제 EDA 도구로 검증하고, 실패 시 원인을 다시 분석하여 재시도하는 **검증 중심 AI Debugging Agent**를 완성한다.
>
> **문서 사용자:** Codex
>
> **중요:** 이 문서는 단순 기획서가 아니라 **Codex가 조사부터 구현·테스트·벤치마크·결과 정리·제출 ZIP 생성까지 스스로 수행하기 위한 실행계획서**다.

---

## 0. Codex 실행 지시 — 반드시 먼저 읽을 것

Codex는 이 문서를 읽은 뒤 **별도의 구현 계획만 작성하고 멈추지 말고**, 아래 순서대로 실제 작업을 끝까지 수행한다.

1. 현재 저장소와 개발 환경을 먼저 조사한다.
2. 이 문서의 `Phase 0 — 사전 조사`를 수행하고 `docs/RESEARCH.md`를 생성한다.
3. 조사 결과에 따라 기술 선택이 달라질 필요가 있다면 `docs/DECISIONS.md`에 근거를 기록하고 계획을 보정한다.
4. 이후 Phase 1부터 마지막 Phase까지 **순차적으로 실제 코드와 테스트를 구현한다.**
5. 각 Phase 종료 시 완료 조건을 실제 명령으로 검증한다.
6. 실패한 테스트를 숨기거나 삭제하지 않는다. 원인을 분석하고 수정한다.
7. LLM이 “완료됐다”고 주장하는 것을 신뢰하지 말고, **실제 subprocess 실행 결과·pytest·EDA 도구 결과를 source of truth로 사용한다.**
8. 외부 정보가 필요하고 인터넷 검색이 가능하면 **공식 문서 → 공식 GitHub → 신뢰 가능한 기술 자료** 순서로 조사한다.
9. 버전, 설치 방식, CLI 옵션, 라이선스 등 변경 가능성이 있는 정보는 기억에 의존하지 말고 실제 최신 문서를 확인한다.
10. API 키, 토큰, 비밀정보는 저장소에 커밋하지 않는다.
11. 개발 진행 상황과 발생한 이슈를 본 문서에만 누적하지 말고, 아래 별도 파일에 계속 기록한다.
    - 전체 작업 일지: `docs/PROGRESS.md`
    - 이슈 목록 및 현재 상태: `docs/ISSUES.md`
    - 이슈별 상세 기록: `docs/issues/ISSUE-NNN-short-title.md` (이슈마다 파일 하나)
12. 사용자의 명시적 개입이 필요한 경우는 다음뿐이다.
    - API credential이 전혀 없어 live LLM 호출이 불가능한 경우
    - OS 권한 승인이 필요한 설치 작업
    - 비용이 발생하는 외부 서비스 선택이 필요한 경우
    - 기존 사용자 파일을 파괴적으로 변경해야 하는 경우
13. 그 외 기술적 선택은 합리적인 기본값을 정해 진행하고 근거를 기록한다.
14. 마지막에는 GitHub 저장소 `semidebug_agent`에 프로젝트를 커밋하고 푸시한다. 원격 저장소가 없으면 만들고, 로컬 Git 저장소도 없으면 초기화한다. 구체적인 절차는 §40을 따른다.

### 진행 기록 및 이슈 기록 규칙

- 작업을 시작할 때 `docs/PROGRESS.md`, `docs/ISSUES.md`를 준비한다. 이미 있으면 내용을 보존하고 이어서 갱신한다.
- 각 Phase 시작 시 작업 항목과 상태를 `docs/PROGRESS.md`에 기록하고, Phase가 끝날 때 결과·실행한 검증 명령·검증 결과·다음 작업을 갱신한다. 장시간 작업은 의미 있는 마일스톤마다 기록한다.
- 작업 중 문제가 발견되면 해결 가능 여부와 무관하게 `docs/issues/`에 이슈별 Markdown 파일을 즉시 만든다. 파일명은 순차 번호와 짧은 kebab-case 제목을 사용한다(예: `ISSUE-001-iverilog-install.md`).
- 각 이슈 파일에는 발견 일시, 증상, 재현 절차 또는 관련 명령, 영향 범위, 원인(미확인 시 미확인으로 표시), 시도한 해결책, 최종 조치, 검증 결과, 상태(Open/Resolved/Blocked)를 기록한다.
- 새 이슈 파일을 만들거나 상태를 바꿀 때마다 `docs/ISSUES.md`의 요약 목록도 함께 갱신한다. 이슈를 해결하지 못했으면 근거와 막힌 이유를 남기고 `Blocked`로 표시한다.
- 기록은 실제 관찰한 사실에 근거해 작성한다. 실행하지 않은 명령이나 검증을 실행한 것처럼 쓰지 않으며, 기존 기록을 지우거나 실패 기록을 성공으로 고쳐 쓰지 않는다.
- 구현, 검증, 문서화, 패키징 및 GitHub 게시 단계까지 이 기록 규칙을 적용한다.

### Codex가 절대 하면 안 되는 것

- 테스트를 통과시키기 위해 testbench 자체를 수정하기
- expected output을 변경하기
- assertion을 삭제/비활성화하기
- 실패하는 test case를 skip 처리하기
- benchmark 정답(ground truth)을 Agent prompt에 노출하기
- 하드코딩으로 특정 benchmark case만 통과시키기
- 실제 실행하지 않은 결과를 PASS라고 기록하기
- 벤치마크 결과 숫자를 임의로 생성하기
- proprietary EDA tool이나 유료 라이선스가 있어야만 실행 가능한 구조로 만들기
- 실제 반도체 생산환경에서 검증한 것처럼 과장하기

---

# 1. 프로젝트 정의

## 1.1 프로젝트명

**SemiDebug Agent**

부제:

> Evidence-Driven RTL Debugging Agent with Compile, Simulation, Lint and Synthesis Verification

## 1.2 한 문장 설명

Verilog/SystemVerilog 코드와 실패 로그를 입력받아 AI가 원인을 추론하고 최소 패치를 생성한 뒤, 실제 시뮬레이터·Lint·Synthesis 도구로 검증하며 실패 시 동일 검증 루프를 반복하는 AI Debugging Agent.

## 1.3 해결하려는 문제

LLM은 RTL 오류에 대해 그럴듯한 수정안을 생성할 수 있지만 다음 문제가 있다.

- 문법적으로 맞아 보여도 compile이 되지 않을 수 있다.
- compile은 되지만 실제 동작이 틀릴 수 있다.
- 한 테스트를 고치면서 기존 정상 기능을 깨뜨릴 수 있다.
- AI가 testbench나 assertion을 변경해 “통과한 것처럼” 만들 수 있다.
- 원인 설명이 실제 patch와 일치하지 않을 수 있다.
- 반복 수정 과정이 기록되지 않아 신뢰하기 어렵다.

SemiDebug Agent의 핵심은 **LLM의 답변이 아니라 외부 Tool 기반 검증 결과를 최종 판정으로 사용하는 것**이다.

## 1.4 핵심 가치

```text
Failure
  ↓
Evidence Collection
  ↓
Hypothesis
  ↓
Minimal Patch
  ↓
Independent Validation
  ├─ FAIL → Evidence 갱신 → Retry
  └─ PASS → Full Regression → Report
```

---

# 2. MVP 범위

## 2.1 반드시 구현할 기능

1. Verilog/SystemVerilog 프로젝트 입력
2. baseline compile/simulation 실행
3. compiler/simulator 실패 로그 수집
4. 실패와 관련된 소스 context 추출
5. LLM 기반 root-cause hypothesis 생성
6. LLM 기반 **최소 patch** 생성
7. patch 정책 검증
8. 임시 workspace에 patch 적용
9. compile 재실행
10. simulation 재실행
11. lint 재실행
12. synthesis sanity check
13. 실패 시 로그를 이용한 retry
14. 성공 시 전체 regression suite 실행
15. 모든 과정에 대한 machine-readable trace 저장
16. 사람이 읽을 수 있는 Evidence Report 생성
17. 여러 benchmark case를 일괄 실행하고 metric 계산
18. 제출용 ZIP 생성 스크립트

## 2.2 MVP에서 제외할 것

아래는 우선 구현하지 않는다.

- 실제 상용 반도체 설계 프로젝트 지원
- Synopsys/Cadence/Siemens 등 proprietary EDA integration
- waveform을 Vision 모델로 분석
- gate-level timing simulation
- FPGA bitstream 생성
- 대규모 multi-million-line RTL repository
- 웹 기반 IDE
- 사용자 계정/권한/결제
- Multi-Agent를 위한 복잡한 분산 시스템

필요하면 이후 확장 항목으로 README에 기록한다.

---

# 3. Phase 0 — 사전 조사

**이 단계는 건너뛰지 않는다.**

Codex는 실제 개발 시작 전에 아래 내용을 조사하고 `docs/RESEARCH.md`에 결과를 작성한다.

## 3.1 로컬 환경 조사

다음을 실제로 확인한다.

```bash
uname -a
python3 --version
pip --version || true
uv --version || true
docker --version || true
git --version
iverilog -V || true
vvp -V || true
verilator --version || true
yosys -V || true
```

확인할 내용:

- macOS / Linux 여부
- Apple Silicon 여부
- Docker 사용 가능 여부
- Python 버전
- 설치된 EDA tool 여부
- package manager(Homebrew/apt 등)

## 3.2 EDA 도구 최신 정보 조사

반드시 공식 문서를 우선 확인한다.

### Icarus Verilog

조사 항목:

- 최신 stable release
- macOS/Apple Silicon 설치 방법
- Verilog/SystemVerilog language flag
- compile command
- vvp simulation command
- exit code의 의미
- warning/error 출력 특성

### Verilator

조사 항목:

- 최신 stable release
- `--lint-only` 권장 옵션
- warning severity 설정
- SystemVerilog 지원 범위
- Docker 사용 여부
- macOS에서의 설치 방법

### Yosys

조사 항목:

- 최신 stable 또는 공식 권장 release
- `read_verilog` / SystemVerilog frontend 제약
- generic RTL synthesis sanity check용 최소 script
- 실패 exit code 처리
- macOS/ARM 환경 지원

### 조사 결과에서 결정할 것

`docs/DECISIONS.md`에 다음을 확정한다.

```text
Primary Simulator = ?
Secondary Lint Tool = ?
Synthesis Sanity Tool = ?
Canonical Runtime = native | Docker
Canonical Python Version = ?
Package Manager = uv | pip
```

기본 권장 방향은 다음이지만 조사 결과가 우선한다.

```text
Primary Simulation: Icarus Verilog
Lint / independent parser: Verilator
Synthesis sanity: Yosys
Language: Python
Canonical benchmark environment: Docker where practical
```

## 3.3 Agent orchestration 방식 조사

다음 두 방식을 비교한다.

### A. Explicit Python State Machine

장점:

- dependency가 적다.
- Agent의 모든 전이를 직접 통제할 수 있다.
- portfolio에서 orchestration을 설명하기 쉽다.
- trace 구조를 자유롭게 설계할 수 있다.

### B. LangGraph

장점:

- retry/conditional routing이 명확하다.
- state graph 시각화가 쉽다.
- 프로젝트의 Agent 성격을 쉽게 보여줄 수 있다.

선택 원칙:

- MVP를 빠르고 투명하게 만들 수 있다면 **Explicit State Machine을 기본값으로 우선 고려한다.**
- LangGraph를 사용할 경우 단순히 유행해서 쓰지 말고 실제 장점이 있는지 `DECISIONS.md`에 기록한다.

## 3.4 LLM Provider 조사

Agent core가 특정 vendor에 종속되지 않게 한다.

최소 interface:

```python
class LLMProvider(Protocol):
    def generate_structured(self, request: LLMRequest, schema: type[T]) -> T:
        ...
```

지원 우선순위:

1. 현재 환경에서 사용 가능한 provider
2. OpenAI-compatible provider
3. Mock/Fake provider for tests

확인할 항목:

- structured output 지원
- tool calling을 실제로 사용할지 여부
- timeout
- max output
- token usage metadata
- retry 정책

**중요:** API가 없어도 unit test와 benchmark framework 자체는 실행 가능해야 한다.

## 3.5 보안 / sandbox 조사

RTL/testbench는 외부 입력이 될 수 있으므로 subprocess 실행 위험을 고려한다.

조사할 것:

- Docker sandbox 사용 가능 여부
- process timeout
- memory/cpu limit
- network disable
- volume mount 최소화

MVP의 bundled benchmark는 우리가 만든 안전한 fixture지만, architecture는 arbitrary command injection을 허용하면 안 된다.

## 3.6 라이선스 조사

다음을 `docs/THIRD_PARTY.md`에 기록한다.

- Icarus Verilog license
- Verilator license
- Yosys license
- Python dependency license

Benchmark RTL은 직접 작성하거나 라이선스가 명확한 자료만 사용한다.

---

# 4. 기술 아키텍처

## 4.1 전체 흐름

```text
┌────────────────────────────┐
│ Project / Benchmark Loader │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│ Baseline Validation        │
│ - compile                  │
│ - simulation               │
│ - lint                     │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│ Failure Evidence Extractor │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│ Context Selector           │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│ LLM Root Cause Analyzer    │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│ Minimal Patch Generator    │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│ Patch Policy Guard         │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│ Apply in Temp Workspace    │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│ Multi Validator            │
│ 1. compile                 │
│ 2. target test             │
│ 3. lint                    │
│ 4. synthesis sanity        │
└───────┬────────────────────┘
        │
        ├─ FAIL → Evidence → Retry Controller → Analyzer
        │
        └─ PASS
             ↓
┌────────────────────────────┐
│ Full Regression            │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│ Evidence / Metrics Report  │
└────────────────────────────┘
```

## 4.2 핵심 원칙

### Principle 1 — LLM은 Judge가 아니다

LLM은 hypothesis와 patch를 생성하지만 PASS/FAIL은 외부 도구가 결정한다.

### Principle 2 — 최소 변경

가급적 가장 작은 diff로 수정한다.

### Principle 3 — Evidence First

모든 재시도는 이전 실패 결과를 증거로 사용한다.

### Principle 4 — Regression Required

target test 하나만 통과했다고 성공으로 판정하지 않는다.

### Principle 5 — Immutable Tests

testbench/expected output/verification script는 Agent가 수정하지 못한다.

---

# 5. 권장 Repository 구조

조사 결과에 따라 약간 조정 가능하지만, 아래 구조를 기본으로 한다.

```text
semidebug-agent/
├── README.md
├── LICENSE
├── pyproject.toml
├── uv.lock                      # uv 사용 시
├── .python-version
├── .env.example
├── .gitignore
├── Makefile
├── Dockerfile
├── docker-compose.yml           # 필요 시
│
├── docs/
│   ├── RESEARCH.md
│   ├── DECISIONS.md
│   ├── ARCHITECTURE.md
│   ├── BENCHMARK.md
│   ├── SECURITY.md
│   └── THIRD_PARTY.md
│
├── src/
│   └── semidebug/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── models.py
│       │
│       ├── agent/
│       │   ├── orchestrator.py
│       │   ├── state.py
│       │   ├── analyzer.py
│       │   ├── patcher.py
│       │   ├── retry.py
│       │   └── prompts.py
│       │
│       ├── llm/
│       │   ├── base.py
│       │   ├── provider.py
│       │   └── fake.py
│       │
│       ├── tools/
│       │   ├── process.py
│       │   ├── iverilog.py
│       │   ├── verilator.py
│       │   ├── yosys.py
│       │   └── workspace.py
│       │
│       ├── patch/
│       │   ├── parser.py
│       │   ├── guard.py
│       │   └── apply.py
│       │
│       ├── context/
│       │   ├── source_index.py
│       │   └── selector.py
│       │
│       ├── benchmark/
│       │   ├── loader.py
│       │   ├── runner.py
│       │   ├── metrics.py
│       │   └── integrity.py
│       │
│       └── report/
│           ├── renderer.py
│           └── templates/
│
├── benchmark/
│   ├── manifest.json
│   ├── public/
│   │   ├── case_001_*/
│   │   └── ...
│   └── hidden/
│       └── ...
│
├── examples/
│   └── fifo_off_by_one/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── scripts/
│   ├── bootstrap.sh
│   ├── doctor.sh
│   ├── run_demo.sh
│   ├── run_benchmark.sh
│   └── package_submission.py
│
└── artifacts/
    ├── .gitkeep
    └── README.md
```

---

# 6. Domain 모델

Pydantic 또는 dataclass를 이용해 명확한 typed model을 사용한다.

## 6.1 RunState

필수 필드 예시:

```python
class RunState(BaseModel):
    run_id: str
    case_id: str
    iteration: int
    max_iterations: int

    project_root: str
    mutable_files: list[str]
    immutable_files: list[str]

    baseline: ValidationBundle | None
    current_validation: ValidationBundle | None

    evidence: list[EvidenceItem]
    hypotheses: list[Hypothesis]
    patch_attempts: list[PatchAttempt]

    final_status: str
    failure_reason: str | None
```

## 6.2 Hypothesis

```python
class Hypothesis(BaseModel):
    summary: str
    likely_files: list[str]
    likely_lines: list[int]
    reasoning: str
    confidence: float
    evidence_ids: list[str]
```

## 6.3 PatchProposal

```python
class PatchProposal(BaseModel):
    explanation: str
    unified_diff: str
    expected_effect: str
    risks: list[str]
```

## 6.4 ValidationResult

```python
class ValidationResult(BaseModel):
    tool: str
    command: list[str]
    exit_code: int
    status: Literal["pass", "fail", "timeout", "error"]
    stdout: str
    stderr: str
    duration_ms: int
```

## 6.5 BenchmarkResult

최소 다음을 저장한다.

```text
case_id
bug_category
success
iterations
llm_calls
compile_pass
simulation_pass
lint_pass
synthesis_pass
regression_pass
invalid_patch_attempts
duration_ms
input_tokens
output_tokens
estimated_cost
```

---

# 7. Tool Adapter 구현

## 7.1 공통 subprocess runner

`tools/process.py`를 먼저 만든다.

요구사항:

- shell=True 금지
- command는 list[str]
- timeout 필수
- stdout/stderr capture
- working directory 명시
- environment whitelist
- exit code 기록
- duration 기록
- timeout 시 child process 정리
- command injection 방지

반환은 `ValidationResult` 또는 `ProcessResult`로 통일한다.

## 7.2 IcarusAdapter

책임:

1. source 파일 목록 구성
2. compile
3. simulation 실행
4. 결과 normalization

예시 흐름:

```text
iverilog ... → compiled output
vvp compiled_output
```

실제 옵션은 Phase 0 조사 결과를 기준으로 설정한다.

## 7.3 VerilatorAdapter

주 역할은 독립 lint다.

- syntax/parser 문제
- width warning
- latch 등 의미 있는 warning

warning 정책은 문서화한다.

모든 warning을 실패로 처리하면 false negative가 과도할 수 있으므로 중요 warning category를 조사한 뒤 정책을 정한다.

## 7.4 YosysAdapter

목적은 완전한 physical synthesis가 아니라 **RTL이 최소한 일반적인 synthesis flow를 통과할 수 있는지 sanity check**하는 것이다.

예:

```text
read_verilog
hierarchy/check
proc
opt
check
```

정확한 script는 공식 문서를 확인한 뒤 결정한다.

---

# 8. Patch Integrity Guard — 매우 중요

SemiDebug의 차별화 포인트다.

## 8.1 수정 허용 경로

Case manifest에 명시한다.

예:

```json
{
  "mutable": ["rtl/fifo.v"],
  "immutable": [
    "tb/fifo_tb.v",
    "tests/**",
    "expected/**"
  ]
}
```

## 8.2 Patch 적용 전에 검사할 것

- 허용되지 않은 파일 변경 여부
- testbench 변경 여부
- expected result 변경 여부
- assertion 삭제 여부
- `$finish` / `$fatal` 조작 여부
- test bypass 코드 삽입 여부
- 새 외부 dependency 삽입 여부
- 너무 큰 patch 여부

## 8.3 변경량 제한

초기 정책 예시:

```text
Max files changed: 2
Max changed lines: 40
```

이 값은 benchmark를 돌려보고 조정 가능하지만 변경 이유를 `DECISIONS.md`에 기록한다.

## 8.4 Diff 기반 적용

LLM에게 전체 파일을 새로 작성하게 하기보다 unified diff를 반환하도록 한다.

장점:

- 변경 범위 측정 가능
- audit 가능
- rollback 쉬움
- portfolio에서 patch evidence 제시 가능

---

# 9. Context Selection

전체 repository를 무조건 prompt에 넣지 않는다.

## 9.1 우선순위

1. compiler/simulator가 지목한 파일/line
2. 해당 module 전체
3. 직접 연결된 module
4. 관련 testbench의 실패 assertion 주변 — **읽기만 허용**
5. 이전 retry의 patch와 failure evidence

## 9.2 Prompt에 포함할 것

```text
Goal
Constraints
Immutable files
Failure log
Relevant source
Previous attempts
Validation history
Required output schema
```

## 9.3 포함하지 않을 것

- benchmark ground truth
- 정답 patch
- 다른 case의 정답

---

# 10. Prompt 설계

Prompt는 source code에 문자열로 난립시키지 말고 `agent/prompts.py` 또는 template 파일에 분리한다.

## 10.1 Analyzer prompt

목표:

> 실패 로그와 소스 코드만을 근거로 root cause hypothesis를 만든다.

강제 조건:

- evidence 없는 원인을 사실처럼 단정하지 않는다.
- testbench 수정 제안 금지
- 최대 3개 hypothesis
- 가장 가능성 높은 hypothesis를 우선
- file/line 근거 제시

## 10.2 Patcher prompt

목표:

> 선택된 hypothesis를 해결하는 최소 patch를 생성한다.

강제 조건:

- mutable file만 변경
- testbench/expected result 수정 금지
- unrelated refactoring 금지
- formatting-only 변경 금지
- unified diff 출력
- 변경 이유 명시

## 10.3 Retry prompt

다음을 반드시 전달한다.

```text
Previous hypothesis
Previous diff
Validation command
Exit code
New stdout/stderr
Which checks passed
Which checks failed
```

Agent가 같은 patch를 반복하는 경우 중단한다.

---

# 11. Agent State Machine

최소 상태:

```text
LOAD_PROJECT
  ↓
BASELINE
  ↓
COLLECT_EVIDENCE
  ↓
ANALYZE
  ↓
GENERATE_PATCH
  ↓
GUARD_PATCH
  ↓
APPLY_PATCH
  ↓
VALIDATE_TARGET
  ├─ fail → SHOULD_RETRY
  │            ├─ yes → COLLECT_EVIDENCE
  │            └─ no  → FAILED
  │
  └─ pass → VALIDATE_REGRESSION
                 ├─ fail → SHOULD_RETRY
                 └─ pass → SUCCESS
```

## 11.1 종료 조건

다음 중 하나면 종료한다.

- 모든 validation PASS
- max retry 도달
- 동일 patch 반복
- 동일 root cause + 동일 failure가 반복
- patch guard가 연속으로 일정 횟수 거부
- infrastructure error
- LLM provider unrecoverable error

## 11.2 기본 retry

초기 기본값은 작게 설정한다.

예:

```text
max_iterations = 3
```

벤치마크 결과로 조정하되 무한 retry 금지.

---

# 12. Benchmark 설계

벤치마크는 프로젝트의 핵심 산출물이다.

## 12.1 목표

“AI가 고쳤다”가 아니라 다음을 숫자로 보여준다.

```text
얼마나 자주 고치는가?
한 번에 얼마나 자주 고치는가?
몇 번 retry하는가?
수정 후 다른 기능은 깨지지 않는가?
부적절한 patch를 얼마나 자주 생성하는가?
얼마나 오래/비싸게 동작하는가?
```

## 12.2 Case 수

최소 목표:

```text
Public benchmark: 24 cases
Hidden/holdout:     6 cases
Total:             30 cases
```

시간/환경 제약이 있더라도 **최소 20 case 이상**을 목표로 한다.

## 12.3 Base design 후보

복잡도가 지나치게 높지 않은 작은 RTL을 직접 작성한다.

추천:

1. counter / timer
2. synchronous FIFO
3. round-robin arbiter
4. simple FSM controller
5. ALU + register/control logic
6. UART TX 또는 pulse/edge controller

모든 정상 버전에는 regression test가 먼저 있어야 한다.

## 12.4 Bug category

최소 다음 범주를 포함한다.

### Syntax / compile
- typo
- undeclared identifier
- port mismatch

### Width / signedness
- width truncation
- signed/unsigned mismatch

### Reset
- reset polarity
- missing reset
- incorrect reset state

### Sequential logic
- blocking/non-blocking misuse
- wrong update order
- incorrect enable condition

### Boundary
- off-by-one
- counter overflow
- FIFO full/empty boundary

### FSM
- missing transition
- wrong transition condition
- wrong default state

### Combinational
- missing assignment / latch
- incorrect mux condition

### Connectivity
- swapped signal
- wrong module port connection

## 12.5 Case 구조

```text
benchmark/public/case_001_fifo_full/
├── case.json
├── rtl/
│   └── fifo.v
├── tb/
│   └── fifo_tb.v
└── expected/
    └── metadata.json
```

`case.json` 예시:

```json
{
  "id": "case_001_fifo_full",
  "category": "boundary_off_by_one",
  "top": "fifo_tb",
  "mutable": ["rtl/fifo.v"],
  "immutable": ["tb/fifo_tb.v", "expected/metadata.json"],
  "compile": {},
  "simulation": {},
  "timeout_sec": 10
}
```

정답 patch와 상세 ground truth는 Agent runtime에서 읽을 수 없는 별도 evaluator 영역에 둔다.

---

# 13. Benchmark Integrity

## 13.1 정상 버전부터 검증

각 benchmark는 bug를 삽입하기 전에 gold version이 모든 validation을 통과해야 한다.

```text
gold compile PASS
gold simulation PASS
gold lint acceptable
gold synthesis PASS
```

## 13.2 Bug version 검증

각 bug는 실제로 목표 validation을 실패해야 한다.

정상처럼 동작하는 mutation은 benchmark에서 제외한다.

## 13.3 Hidden cases

Agent prompt에는 hidden 여부를 전달하지 않는다.

public case를 튜닝한 뒤 hidden set으로 최종 generalization을 확인한다.

## 13.4 Benchmark fingerprint

testbench가 변경되지 않았음을 실행 전후 hash로 확인한다.

예:

```text
SHA256(before immutable files)
==
SHA256(after immutable files)
```

불일치하면 해당 run은 무조건 invalid 처리한다.

---

# 14. Metrics

최소 다음 metric을 계산한다.

## 14.1 핵심

### Repair Success Rate

```text
성공적으로 전체 regression까지 통과한 case / 전체 case
```

### First Attempt Fix Rate

```text
첫 patch에서 성공한 case / 전체 case
```

### Regression Integrity Rate

```text
수정 성공 case 중 전체 regression까지 통과한 비율
```

### Invalid Patch Rate

```text
Patch Guard에 걸린 patch / 전체 patch attempts
```

### Average Retry Count

### Median Repair Time

### Average LLM Calls

## 14.2 비용

provider가 token usage를 제공하면:

```text
input_tokens
output_tokens
estimated_cost
```

를 저장한다.

비용 계산식은 provider price가 변경될 수 있으므로 코드에 영구 하드코딩하지 말고 config/source date를 기록한다.

## 14.3 결과 해석

성능이 기대보다 낮아도 숫자를 숨기지 않는다.

예:

```text
Public  : 19 / 24 fixed
Hidden  :  3 / 6 fixed
Overall : 22 / 30 = 73.3%
```

**실제 결과로만 작성한다.**

---

# 15. CLI 설계

CLI framework는 Typer 또는 argparse를 사용한다. dependency 단순성을 고려해 조사 후 결정한다.

최종 UX 목표:

## 15.1 환경 검사

```bash
semidebug doctor
```

출력 예:

```text
Python      OK
Icarus      OK
Verilator   OK
Yosys       OK
LLM API     OK
Docker      optional
```

## 15.2 단일 case 실행

```bash
semidebug fix examples/fifo_off_by_one
```

옵션:

```text
--provider
--model
--max-iterations
--output
--verbose
```

## 15.3 benchmark

```bash
semidebug benchmark benchmark/public
```

## 15.4 report

```bash
semidebug report artifacts/runs/<run_id>/result.json
```

## 15.5 replay

Live API 없이 포트폴리오를 확인하기 위한 **명확히 표시된 replay mode**를 둘 수 있다.

```bash
semidebug replay artifacts/sample_run.json
```

주의:

- replay를 live AI 실행처럼 표현하면 안 된다.
- UI/README에서 `RECORDED RUN`임을 명시한다.

---

# 16. Artifact / Trace 저장

모든 실행은 독립 directory를 만든다.

```text
artifacts/runs/<run_id>/
├── run.json
├── events.jsonl
├── baseline/
│   ├── compile.log
│   ├── simulation.log
│   └── lint.log
├── attempts/
│   ├── 01/
│   │   ├── hypothesis.json
│   │   ├── patch.diff
│   │   └── validation.json
│   └── ...
├── final/
│   ├── patch.diff
│   ├── regression.json
│   └── metrics.json
└── report.md
```

## 16.1 events.jsonl

각 이벤트에 최소 다음을 남긴다.

```text
timestamp
run_id
case_id
iteration
event_type
tool/status
summary
```

민감한 prompt/API key는 기록하지 않는다.

---

# 17. Report 생성

최종 report는 읽는 사람이 1~2분 내 결과를 이해할 수 있어야 한다.

## 17.1 단일 case report

포함 내용:

```text
Case
Bug category
Baseline failure
Agent hypothesis
Patch summary
Patch diff
Attempt history
Validation matrix
Before/After
Final status
Token/cost/time
```

예시 validation matrix:

| Check | Before | Attempt 1 | Attempt 2 |
|---|---|---|---|
| Compile | PASS | PASS | PASS |
| Target simulation | FAIL | FAIL | PASS |
| Verilator lint | PASS | PASS | PASS |
| Yosys check | PASS | PASS | PASS |
| Full regression | - | - | PASS |

## 17.2 Benchmark report

자동 생성:

```text
artifacts/benchmark/<timestamp>/summary.md
artifacts/benchmark/<timestamp>/summary.json
artifacts/benchmark/<timestamp>/results.csv
```

포함:

- 총 case 수
- fixed 수
- first-shot fix
- category별 성공률
- retry 분포
- failure reason breakdown
- invalid patch count
- average/median execution time
- token/cost 가능 시

---

# 18. Phase 1 — Project Bootstrap

실제 수행한다.

## 작업

1. Git repository 초기화 또는 기존 repo 확인
2. Python project 생성
3. formatter/linter/test 환경 구성
4. dependency 관리
5. `.env.example`
6. CLI skeleton
7. logging
8. config
9. `semidebug doctor`
10. Dockerfile 초안

## 테스트

```bash
pytest
semidebug doctor
```

## 완료 조건

- clean install 가능
- `doctor`가 EDA tool 상태를 정확히 출력
- unit test 시작점 존재

---

# 19. Phase 2 — Deterministic Validation Pipeline

**LLM보다 먼저 구현한다.**

## 작업

1. subprocess runner
2. workspace copy
3. Icarus compile
4. vvp simulation
5. Verilator lint
6. Yosys sanity
7. ValidationBundle
8. timeout/error handling

## 첫 fixture

정상 counter + 의도적으로 실패하는 counter를 만든다.

## 완료 조건

정상 fixture:

```text
compile PASS
simulation PASS
lint PASS/acceptable
synthesis PASS
```

broken fixture:

```text
최소 하나 이상의 intended failure를 재현
```

---

# 20. Phase 3 — Patch System

## 작업

1. unified diff parser
2. allowed path validation
3. immutable file protection
4. max diff guard
5. temp workspace apply
6. rollback
7. file hash integrity

## 공격 테스트

다음 malicious patch를 만들어 모두 차단되는지 확인한다.

- testbench 수정
- expected output 수정
- 모든 test disable
- 허용 경로 밖 수정
- 대규모 unrelated rewrite

## 완료 조건

```text
legitimate RTL patch → allowed
forbidden test patch → blocked
immutable hash change → invalid run
```

---

# 21. Phase 4 — LLM Integration

## 작업

1. provider interface
2. live provider adapter
3. fake provider
4. structured Analyzer output
5. structured PatchProposal output
6. schema validation
7. timeout/retry
8. usage capture

## 테스트

Fake provider로 deterministic unit test를 먼저 만든다.

실제 API 테스트는 별도로 표시한다.

## 완료 조건

- malformed LLM output을 안전하게 처리
- schema에 맞지 않으면 patch 적용 금지
- API failure가 전체 process crash로 이어지지 않음

---

# 22. Phase 5 — Agent Loop

## 작업

1. state machine 구현
2. baseline evidence
3. analyze
4. patch
5. guard
6. apply
7. validate
8. retry
9. regression
10. terminate

## 핵심 테스트

### Scenario A
첫 patch 성공

### Scenario B
첫 patch 실패 → 두 번째 성공

### Scenario C
모든 patch 실패 → max retry 종료

### Scenario D
LLM이 testbench 변경 → guard 차단 → 재요청

### Scenario E
동일 patch 반복 → early stop

## 완료 조건

모든 state transition이 trace에 기록되고 재현 가능해야 한다.

---

# 23. Phase 6 — Benchmark Dataset 구축

## 순서

### 1. Gold RTL 작성

각 design마다 정상 version + regression test 작성.

### 2. Gold 검증

모든 EDA validation 통과.

### 3. Bug mutation 생성

가능하면 mutation script + manual curated bug를 혼합한다.

### 4. Broken 검증

실제로 원하는 failure가 나는지 검사.

### 5. Manifest 작성

### 6. Public/Hidden split

### 7. Integrity test

## 중요

단순 syntax bug만 30개 만드는 것은 금지한다.

functional bug가 충분히 포함되어야 한다.

---

# 24. Phase 7 — Benchmark Runner

## 작업

1. directory discovery
2. per-case isolated workspace
3. sequential execution 우선
4. result aggregation
5. resume 기능 고려
6. CSV/JSON export
7. metrics
8. failure taxonomy

병렬 실행은 안정성 확인 후 선택적으로 구현한다.

## Failure taxonomy 예

```text
FIXED
MAX_RETRY
PATCH_REJECTED
COMPILE_FAIL
SIMULATION_FAIL
REGRESSION_FAIL
LLM_ERROR
INFRA_ERROR
TIMEOUT
```

---

# 25. Phase 8 — Quality Improvement

첫 benchmark 결과를 얻은 뒤에만 개선한다.

## 분석할 것

- 어떤 category에서 실패하는가?
- context 부족인가?
- prompt가 원인인가?
- retry evidence가 부족한가?
- EDA warning noise 때문인가?
- patch guard가 과도한가?

## 개선 우선순위

1. context selection
2. evidence normalization
3. retry prompt
4. patch guard false positive
5. model config

모델을 더 비싼 것으로 바꾸는 것은 가장 마지막 선택이다.

## Regression requirement

개선 전/후 동일 benchmark를 실행한다.

결과를 다음처럼 저장한다.

```text
benchmark_v1.json
benchmark_v2.json
```

그리고 delta를 report한다.

---

# 26. Phase 9 — Test Suite

## Unit tests

- parser
- patch guard
- command builder
- log normalization
- metrics
- model validation

## Integration tests

- Icarus fixture
- Verilator fixture
- Yosys fixture
- patch → validation

## E2E tests

최소 3 case:

```text
first-shot fixed
retry fixed
unfixed safely
```

## 테스트 명령 통일

예:

```bash
make test
make test-integration
make e2e
```

Makefile 대신 task runner를 선택해도 되지만 README에서 하나로 통일한다.

---

# 27. Phase 10 — Reproducibility

최종 제출 전에 clean 환경에서 검증한다.

## 목표 명령

```bash
git clone ...
cd semidebug-agent
cp .env.example .env
./scripts/bootstrap.sh
semidebug doctor
./scripts/run_demo.sh
```

Docker가 canonical이면:

```bash
docker build -t semidebug .
docker run ...
```

## 확인

- fresh clone에서 동작
- absolute local path 없음
- username/home directory dependency 없음
- API secret 없음
- cache 없이 실행 가능

---

# 28. Phase 11 — Demo 시나리오

포트폴리오에서 가장 보여주기 쉬운 example 하나를 별도로 고정한다.

추천:

**Synchronous FIFO off-by-one / full boundary bug**

## Demo 흐름

```text
1. Original RTL
2. Test failure
3. Agent evidence
4. Root-cause hypothesis
5. Patch #1
6. Validation
7. 필요 시 Retry
8. Full regression
9. Final evidence report
```

## CLI

```bash
./scripts/run_demo.sh
```

출력이 너무 길지 않게 summary를 보여준다.

예시 형식:

```text
[SemiDebug]
Case       : fifo_off_by_one
Baseline   : FAIL
Reason     : FIFO accepted write while full

Attempt 1
Hypothesis : boundary condition is incorrect
Patch      : 1 file / 1 line changed
Simulation : PASS
Lint       : PASS
Synthesis  : PASS
Regression : PASS

FINAL      : FIXED
```

실제 결과만 출력한다.

---

# 29. Phase 12 — Portfolio Evidence 생성

코드를 만든 것만으로 끝내지 않는다.

다음을 자동 또는 반자동으로 생성한다.

## 29.1 `PORTFOLIO_EVIDENCE.md`

구조:

```text
Problem
Why LLM-only is unsafe
Architecture
Verification loop
Patch integrity
Benchmark design
Results
Failure cases
What I learned
Limitations
```

## 29.2 Architecture diagram

Mermaid source를 저장한다.

```text
docs/architecture.mmd
```

## 29.3 Evidence examples

최소 2개:

```text
successful_first_try.md
successful_after_retry.md
```

가능하면 실패 사례도 1개 포함한다.

```text
failed_case_analysis.md
```

성공만 골라 보여주기보다 limitation을 설명하면 신뢰도가 높다.

---

# 30. Phase 13 — README 완성

README 첫 화면에서 바로 이해돼야 한다.

권장 구성:

```text
# SemiDebug Agent

1 sentence

## Why
## How it works
## Demo
## Architecture
## Verification
## Benchmark
## Results
## Run locally
## Project structure
## Limitations
```

## README에서 반드시 명시할 한계

- production semiconductor EDA replacement가 아님
- 공개/자체 제작 소형 RTL benchmark를 대상으로 한 prototype
- LLM 결과는 verification을 통과해야만 accepted
- 실제 silicon/physical verification을 수행하지 않음

---

# 31. Phase 14 — 제출용 패키징

최종적으로 아래 ZIP을 생성한다.

```text
SemiDebug_Agent_SKHynix_Portfolio.zip
```

## 권장 내용

```text
SemiDebug_Agent_SKHynix_Portfolio/
├── README.md
├── PORTFOLIO_EVIDENCE.md
├── QUICKSTART.md
│
├── src/
├── examples/
├── benchmark/                   # 너무 크지 않은 범위
├── scripts/
│
├── results/
│   ├── benchmark_summary.md
│   ├── benchmark_results.csv
│   ├── benchmark_results.json
│   └── sample_run/
│
├── docs/
│   ├── ARCHITECTURE.md
│   └── architecture.mmd
│
├── pyproject.toml
├── Dockerfile
├── .env.example
└── run_demo.sh
```

## 제외할 것

- `.git/`
- `.env`
- API keys
- `.venv/`
- `node_modules/`
- Python cache
- 전체 LLM raw secret metadata
- 불필요한 model files
- 거대한 build artifact
- Docker image binary

## 50MB 제한

package script에서 생성 후 size를 검사한다.

```text
if zip > 50MB → packaging FAIL
```

실제로는 50MB보다 훨씬 작게 유지하는 것을 목표로 한다.

---

# 32. 자동 패키지 스크립트

`scripts/package_submission.py`를 만든다.

책임:

1. 제출 대상 파일 whitelist
2. secret scan
3. `.env` 제외
4. cache 제외
5. artifact 정리
6. ZIP 생성
7. SHA256 출력
8. ZIP size 출력
9. 50MB 초과 시 실패

가능하다면 다음도 검사한다.

- README 존재
- benchmark 결과 존재
- demo script 존재
- source 존재

---

# 33. CI

GitHub Actions 사용 가능하면 최소 CI를 추가한다.

```text
unit tests
format/lint
EDA integration smoke test
```

EDA tool 설치 방식은 Phase 0 조사 결과를 따른다.

Live LLM benchmark는 API secret을 요구하므로 public CI의 필수 test로 두지 않는다.

Fake provider 기반 E2E는 CI에서 실행한다.

---

# 34. Definition of Done

다음이 전부 충족되어야 프로젝트 완료다.

## 기능

- [ ] RTL project를 입력할 수 있다.
- [ ] baseline failure를 수집한다.
- [ ] AI가 hypothesis를 생성한다.
- [ ] AI가 unified diff patch를 생성한다.
- [ ] immutable test 보호가 동작한다.
- [ ] patch를 isolated workspace에 적용한다.
- [ ] Icarus compile/simulation을 실행한다.
- [ ] Verilator 검증을 실행한다.
- [ ] Yosys sanity check를 실행한다.
- [ ] 실패 후 retry할 수 있다.
- [ ] 성공 후 full regression을 실행한다.
- [ ] 모든 단계가 trace로 남는다.

## 테스트

- [ ] unit test PASS
- [ ] integration test PASS
- [ ] fake-provider E2E PASS
- [ ] live demo 최소 1개 PASS 또는 실패 원인 명확히 기록

## Benchmark

- [ ] 최소 20개 이상 case
- [ ] 가능하면 30개 case
- [ ] public/hidden split
- [ ] 실제 benchmark 실행
- [ ] raw result 보존
- [ ] metric 자동 계산
- [ ] 실패 case도 기록

## 문서

- [ ] RESEARCH.md
- [ ] DECISIONS.md
- [ ] ARCHITECTURE.md
- [ ] BENCHMARK.md
- [ ] SECURITY.md
- [ ] THIRD_PARTY.md
- [ ] README.md
- [ ] PORTFOLIO_EVIDENCE.md

## 제출

- [ ] `run_demo.sh`
- [ ] 결과 CSV/JSON
- [ ] sample evidence
- [ ] secret 없음
- [ ] ZIP 50MB 이하
- [ ] clean environment 재현 확인

---

# 35. 최종 Benchmark 결과 템플릿

실제 실행 후 아래를 채운다. **사전에 숫자를 채우지 않는다.**

```markdown
# Benchmark Result

Environment:
- Date:
- OS:
- Python:
- Icarus:
- Verilator:
- Yosys:
- LLM Provider:
- Model:

Cases:
- Public:
- Hidden:
- Total:

Results:
- Fixed:
- Repair Success Rate:
- First Attempt Fix Rate:
- Regression Integrity Rate:
- Invalid Patch Rate:
- Average Retry:
- Median Repair Time:
- Average LLM Calls:
- Total Input Tokens:
- Total Output Tokens:
- Estimated Cost:

Failure breakdown:
- MAX_RETRY:
- PATCH_REJECTED:
- COMPILE_FAIL:
- SIMULATION_FAIL:
- REGRESSION_FAIL:
- LLM_ERROR:
- INFRA_ERROR:
```

---

# 36. 포트폴리오에서 강조해야 할 기술적 메시지

최종 결과물이 완성되면 문서와 포트폴리오에서 다음 메시지가 자연스럽게 드러나게 한다.

## 36.1 AI에게 모든 것을 맡기지 않았다

```text
LLM = hypothesis / candidate patch
EDA tools = objective judge
```

## 36.2 AI 실패를 정상적인 시스템 상태로 설계했다

```text
Generate → Validate → Fail → Learn from evidence → Retry
```

## 36.3 검증 자체를 공격할 수 없게 만들었다

```text
Immutable tests
Patch guard
Hash verification
Independent validators
```

## 36.4 결과를 숫자로 측정했다

```text
Success rate
First-shot rate
Regression rate
Retry
Time
LLM calls
Cost
```

## 36.5 실패도 숨기지 않았다

실패 case 분석이 있는 것이 오히려 프로젝트 신뢰도를 높인다.

---

# 37. 추가 개선 후보 — MVP 완료 후에만 검토

MVP와 benchmark를 완성하기 전에 아래로 확장하지 않는다.

## 후보 A — Source dependency graph

module instantiation graph를 만들어 context selection 개선.

## 후보 B — Waveform/VCD evidence

실패 cycle 주변 signal delta를 분석해 prompt에 넣기.

## 후보 C — Formal verification

SymbiYosys 등 공식 도구 조사 후 작은 property 검증 추가.

## 후보 D — Multi-model comparison

동일 benchmark에 여러 LLM을 돌려 repair quality/cost 비교.

## 후보 E — Human-in-the-loop

confidence가 낮거나 patch가 큰 경우 apply 전에 review 요구.

## 후보 F — Git integration

최종 성공 patch를 branch/commit으로 생성.

---

# 38. Codex 최종 수행 순서 요약

Codex는 아래 순서를 그대로 실행한다.

```text
[0] Repository / Environment Inspect
 ↓
[1] Official Docs Research
 ↓
[2] RESEARCH.md + DECISIONS.md
 ↓
[3] Project Bootstrap
 ↓
[4] Deterministic EDA Validation
 ↓
[5] Patch Guard
 ↓
[6] LLM Provider
 ↓
[7] Agent Retry Loop
 ↓
[8] Small E2E Demo
 ↓
[9] Benchmark Dataset
 ↓
[10] Benchmark Runner
 ↓
[11] First Real Benchmark
 ↓
[12] Failure Analysis / Improvements
 ↓
[13] Same Benchmark Re-run
 ↓
[14] Unit + Integration + E2E Final
 ↓
[15] Evidence / README / Architecture
 ↓
[16] Clean Reproduction Test
 ↓
[17] Submission ZIP Generation
 ↓
[18] Final Checklist
```

**중요:** `[2]`에서 계획만 세우고 작업을 종료하지 않는다. 기술적으로 진행 불가능한 명백한 blocker가 없는 한 `[18]`까지 계속 수행한다.

---

# 39. Codex가 마지막에 사용자에게 보고할 내용

모든 작업을 마친 뒤 최종 응답에는 장황한 개발 일지 대신 아래를 요약한다.

1. 구현 완료 범위
2. 핵심 architecture
3. 실제 benchmark 결과
4. 가장 많이 실패한 bug category
5. 검증 도구 및 버전
6. 테스트 결과
7. demo 실행 명령
8. 제출 ZIP 경로와 크기
9. 알려진 한계
10. 포트폴리오에 사용할 수 있는 핵심 수치

실패하거나 미완성인 항목은 명확하게 표시한다.

---

# Appendix A — 조사 시 우선 확인할 공식 자료

Codex는 최신 정보를 실제로 다시 확인한다.

- Icarus Verilog official documentation
- Verilator User's Guide / Installation
- Yosys official documentation / Getting Started / Synthesis
- 선택한 Python dependency 공식 문서
- 선택한 LLM provider 공식 API 문서

버전 번호와 옵션은 이 문서 작성 시점의 기억이나 예시보다 **Codex가 실제 조사한 최신 공식 자료를 우선한다.**

---

# Appendix B — 프로젝트 성공 기준의 핵심

이 프로젝트에서 중요한 것은 “LLM이 Verilog를 생성할 수 있다”가 아니다.

최종적으로 다음 문장을 실제 evidence로 증명할 수 있어야 한다.

> **AI가 실패 원인을 추론하고 코드를 수정하도록 하되, AI의 판단 자체를 신뢰하지 않고 독립적인 compile·simulation·lint·synthesis 검증과 immutable regression test를 통해 결과를 통제했다. 실패 시 검증 결과를 다시 evidence로 사용해 재시도했으며, 그 성능을 반복 가능한 benchmark로 측정했다.**

이 문장을 실제 코드, 로그, diff, 테스트와 benchmark 숫자가 뒷받침하는 상태가 프로젝트의 최종 완료 상태다.

---

# 40. 최종 Git 커밋 및 GitHub 푸시

구현, 검증, 문서화, 제출 ZIP 생성을 마친 뒤 아래 절차를 끝까지 수행한다. GitHub 게시 결과와 실패한 시도도 `docs/PROGRESS.md` 및 해당 이슈 파일에 기록한다.

1. 저장소 루트에서 `git status`와 `git remote -v`를 확인한다. `.git`이 없으면 프로젝트 루트에서 Git 저장소를 초기화하고, 기존 브랜치/파일 상태가 있으면 보존한다.
2. `.gitignore`와 staged 변경사항을 검토한다. API 키·토큰·개인정보·임시 파일·대용량 생성물은 제외하고, 필요한 프로젝트 소스·문서·재현 가능한 설정만 커밋한다. 제출 ZIP은 프로젝트 정책상 저장소에 포함하는 것이 적절한지 확인한다.
3. 프로젝트 상태에 맞는 명확한 초기 커밋을 만든다. 커밋 전에 `git diff --cached`로 포함 내용을 확인하고, 커밋 후 `git status`로 작업 트리가 깨끗한지 확인한다.
4. `gh auth status`로 GitHub 인증을 확인한다. 인증이 가능하면 GitHub 사용자/조직의 기본 namespace 아래 `semidebug_agent`라는 이름의 원격 저장소가 이미 있는지 확인한다. 없으면 `gh repo create semidebug_agent`로 생성한다. 공개 여부는 사용자가 별도로 정한 설정이 있으면 이를 따르고, 별도 설정이 없으면 실수로 소스나 비밀정보를 공개하지 않도록 **private 저장소**로 생성한다.
5. 원격 저장소 생성 후 그 URL을 `origin`으로 설정한다(이미 올바른 `origin`이 있으면 중복 추가하지 않는다). 기본 브랜치를 원격에 push하고 upstream을 설정한다. 푸시 전에 비밀정보가 포함되지 않았는지 최종 확인한다.
6. push 성공 여부, 원격 URL, 브랜치명, 최종 커밋 hash를 `docs/PROGRESS.md`에 기록하고 `docs/ISSUES.md`의 상태를 갱신한다. GitHub 게시 후 기록 파일이 변경됐다면 해당 변경도 커밋·푸시해 원격과 로컬을 일치시킨다.
7. GitHub 인증 또는 네트워크 문제로 생성/푸시할 수 없는 경우, 오류와 수행한 조치를 이슈별 파일에 기록하고 `docs/ISSUES.md`에 `Blocked`로 등록한다. 가능한 범위에서 로컬 커밋까지 마친 뒤 사용자에게 필요한 후속 조치와 남은 명령을 보고한다. 실제로 성공하지 않은 원격 생성이나 push를 성공했다고 기록하지 않는다.

최종 완료 보고에는 GitHub 저장소 링크, 브랜치, 커밋 hash, push 여부를 포함한다. 저장소 링크를 확인할 수 없거나 push하지 못한 경우 그 사실과 이유를 분명히 알린다.


## 로컬 LLM 실행 방식 추가 지시 (2026-09-23)

- 로컬 데모와 성능 측정은 공식 Codex CLI의 ChatGPT 인증을 우선 사용한다. API 키를 요구하거나 로그인 토큰을 추출하여 API에 재사용하지 않는다.
- 실제 이용 가능한 모델을 확인하여 사용한다. 현재 확인 설정은 Codex CLI 0.156.1, gpt-6-sol, reasoning effort low이며 특정 모델을 필수 조건으로 삼지 않는다.
- 모델·CLI 버전·추론 강도·호출 수·입력/캐시/출력 토큰과 실제 EDA 검증 결과를 기록한다. 구독 사용량을 API 비용 0원으로 해석하지 않는다.
- 한 번의 추론에서 가설과 최소 패치를 받아 불필요한 호출을 줄인다. 정답 소스는 모델에 제공하지 않으며 검증 도구는 인증 정보 없이 격리 실행한다.
- 공개 24개와 holdout 6개는 고정 설정으로 실행하고 실패·재시도도 보존한다. 진행과 이슈는 기존 별도 파일 기록 규칙을 따른다. 완료 후 기존 semidebug_agent 원격 저장소에 커밋하고 푸시한다.
