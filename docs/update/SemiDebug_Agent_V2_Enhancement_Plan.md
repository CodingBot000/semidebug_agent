# SemiDebug Agent V2 보강 개발계획서
## SK hynix AI Hackathon 2026 제출용 — Codex End-to-End Execution Plan

> 목적: 현재 SemiDebug Agent V1을 **경진대회 제출용 증거 중심 프로젝트**로 보강한다.<br>
> 핵심은 기능을 늘리는 것이 아니라, **평가 신뢰성·외부 일반화·Agent feedback loop의 효과·재현성·문서 전달력**을 강화하는 것이다.<br>
> Codex는 이 문서를 읽고 현재 저장소를 직접 조사한 뒤, 필요한 변경을 설계·구현·검증·문서화·패키징까지 끝까지 수행한다.

---

# 0. 최우선 운영 원칙

## 0.1 V1 결과를 절대 덮어쓰지 않는다

현재 확인된 V1의 대표 결과는 다음과 같다.

- 자체 RTL 설계 6종
- 오류 30개
- Public 24 / Holdout 6
- 단위·통합·E2E 테스트 95개 통과
- Known-fix pipeline validation 30/30
- 실제 Codex CLI benchmark 30/30
- First attempt 23/30
- Overall median 14.68s
- 실제 모델: `gpt-6-sol`
- reasoning effort: `low`

위 값은 **V1 측정 결과**로 보존한다.

Codex는 작업 시작 직후 현재 commit SHA, branch, 주요 결과 파일의 SHA256을 기록하고,
가능하면 로컬 Git tag 또는 별도 V1 baseline branch를 만든다.

권장:

```bash
git status
git rev-parse HEAD
git tag -a semidebug-v1-baseline -m "Frozen baseline before V2 evaluation hardening"
```

단, 기존 tag 충돌이나 원격 push는 자동 수행하지 않는다.

### 금지

- V1 raw result 파일 덮어쓰기
- V1 숫자를 V2 결과로 재사용
- 실행하지 않은 결과를 문서에 추가
- 실패 case 삭제 후 성공률 재계산
- benchmark를 실행한 뒤 유리한 case만 선택
- 기존 benchmark testbench를 결과에 맞춰 수정
- 외부 benchmark 정답/patch를 모델 prompt에 포함
- 사용자 승인 없이 repository visibility 변경
- 사용자 승인 없이 원격 release/publish 수행

---

# 1. Codex가 작업 시작 시 반드시 수행할 Repository Audit

개발에 바로 들어가지 말고 먼저 프로젝트 전체를 다시 읽는다.

최소 조사 대상:

```text
README.md
PORTFOLIO_EVIDENCE.md
ARCHITECTURE.md
QUICKSTART.md

docs/
  BENCHMARK.md
  CODEX_CLI.md
  DECISIONS.md
  RESEARCH.md
  SECURITY.md
  PROGRESS.md
  ISSUES.md
  THIRD_PARTY.md
  기타 존재하는 문서

src/semidebug/
  agent/
  benchmark/
  context/
  llm/
  patch/
  report/
  tools/
  cli.py
  config.py
  models.py

benchmark/
evaluator/
results/
scripts/
tests/
Dockerfile
Makefile
pyproject.toml
uv.lock
.github/workflows/
```

Codex는 다음 질문에 답한 `docs/V2_AUDIT.md`를 먼저 작성한다.

1. 현재 V1의 실제 실행 경로는 무엇인가?
2. 모델이 prompt에서 볼 수 있는 파일은 정확히 무엇인가?
3. regression test source가 현재 모델 context에 포함되는가?
4. gold/reference/mutation 정의가 runtime workspace와 prompt에서 격리되어 있는가?
5. single-shot 실험을 현재 코드만으로 실행할 수 있는가?
6. retry 발생 원인을 현재 결과 schema에서 얼마나 세분화할 수 있는가?
7. 외부 benchmark adapter를 어느 레이어에 추가하는 것이 가장 덜 침습적인가?
8. 현재 README/PORTFOLIO/BENCHMARK 문서 사이에 중복·모순·과장 가능성이 있는가?
9. 제출 ZIP에 포함하면 안 되는 파일은 무엇인가?
10. third-party benchmark의 라이선스/재배포 조건은 무엇인가?

이 Audit을 끝내기 전에는 대규모 수정에 들어가지 않는다.

---

# 2. V2 목표

V2는 다음 네 가지 질문에 답할 수 있어야 한다.

## Q1. AI가 보지 못한 검증에서도 수정이 통과하는가?

현재 target/regression separation을 다시 검토하고,
**최종 regression source를 LLM context에서 실제로 제외**한다.

## Q2. Feedback loop는 single-shot 대비 실제로 가치가 있는가?

동일 모델·동일 설정·동일 case에서

- first proposal
- full bounded retry loop

를 비교한다.

단순 성공률뿐 아니라 **왜 재시도가 발생했는지** 분류한다.

## Q3. 자체 제작 benchmark 밖에서도 동작하는가?

사전에 selection rule을 고정한 외부 benchmark를 사용한다.

우선순위:

1. ChipBench Verilog Debugging
2. 호환되면 HWE-Bench 소량 real bug
3. 추가 benchmark는 시간과 라이선스가 허용할 때만

## Q4. 경진대회 심사자가 3~5분 안에 핵심을 이해할 수 있는가?

최종 README, Portfolio Evidence, Architecture, Benchmark 문서를
**제출용 evidence package** 관점에서 다시 편집한다.

---

# 3. Phase A — Evaluation Leakage 제거

## 3.1 현재 Context Selector 재검토

현재 코드에서 다음과 유사한 구조가 존재하는지 확인한다.

```python
files = list(case.mutable) + list(
    dict.fromkeys(s for t in [case.target, *case.regression] for s in t.sources)
)
```

이 경우 regression test source까지 LLM context에 포함될 수 있다.

V2에서는 모델에게 보여주는 test source와 evaluator-only test source를 분리한다.

### 목표 구조 예시

```text
case/
  rtl/
    fifo.v

  visible/
    fifo_target_tb.v

  hidden/
    fifo_regression_17_tb.v
    fifo_regression_103_tb.v

  case.json
```

또는 현재 구조를 유지하되 schema에서 구분한다.

예:

```json
{
  "prompt_visible": [
    "rtl/fifo.v",
    "tb/fifo_target_tb.v"
  ],
  "evaluator_only": [
    "tb/fifo_regression_17_tb.v",
    "tb/fifo_regression_103_tb.v"
  ]
}
```

## 3.2 설계 원칙

LLM이 볼 수 있는 것:

- mutable RTL
- baseline compile/simulation error
- visible target testbench
- 이전 attempt의 실패 로그
- 이전 diff 및 guard/EDA 결과

LLM이 볼 수 없어야 하는 것:

- evaluator gold RTL
- exact mutation definition
- reference patch
- hidden regression source
- hidden expected values
- benchmark split label
- external benchmark reference solution

## 3.3 Context Leak 자동 테스트 추가

새 테스트를 반드시 만든다.

예:

```text
tests/unit/test_context_visibility.py
tests/integration/test_evaluator_isolation.py
```

검증:

- context serialization에 hidden path가 없어야 함
- hidden file content의 marker 문자열이 prompt에 없어야 함
- evaluator directory가 workspace에 복사되지 않아야 함
- final regression은 실행되지만 provider invocation에는 포함되지 않아야 함

## 3.4 기존 30개 benchmark 재구축 여부

현재 target/regression이 동일 TB + 다른 plusarg/seed를 사용하는 경우,
단순 context filtering만으로 충분한지 검토한다.

가능하면 V2에서는 적어도 주요 design에 대해
**별도 evaluator-only regression TB**를 둔다.

권장 최소:

- counter
- FIFO
- arbiter
- controller
- ALU
- pulse detector

각 family에서 hidden regression이 visible target보다 더 긴 시퀀스 또는
다른 boundary sequence를 사용하도록 구성한다.

단, gold logic을 그대로 testbench에 노출하는 방식은 피한다.

---

# 4. Phase B — Single-shot vs Feedback Loop Ablation

## 4.1 실험 목적

다음 두 조건을 비교한다.

### Condition A — Single-shot

```text
max_iterations = 1
```

### Condition B — Full loop

```text
max_iterations = 3
```

고정 조건:

- 동일 benchmark
- 동일 model
- 동일 reasoning effort
- 동일 prompt template
- 동일 EDA
- 동일 machine/runtime
- 동일 validation gates

기본 비교 모델:

```text
gpt-6-sol / low
```

기존 V1과 직접 비교하려면 반드시 이 설정을 우선 사용한다.

## 4.2 Paired metric 우선

LLM은 비결정성이 있으므로,
가능하면 기존 full-loop 실행 안에서 다음을 먼저 계산한다.

```text
First proposal accepted
Final success after retry
Cases rescued after attempt #1
```

V1에서는 이미:

```text
First attempt: 23/30
Final:         30/30
```

이 존재한다.

하지만 V2에서는 retry 이유를 세분화한다.

## 4.3 Retry Taxonomy

최소 다음 타입으로 분류한다.

```text
PATCH_PARSE_RETRY
PATCH_GUARD_RETRY
COMPILE_RETRY
SIMULATION_RETRY
LINT_RETRY
SYNTHESIS_RETRY
REGRESSION_RETRY
REPEATED_PATCH_STOP
REPEATED_FAILURE_STOP
LLM_ERROR
INFRA_ERROR
```

각 attempt에 다음을 기록한다.

```json
{
  "attempt": 1,
  "retry_reason": "SIMULATION_RETRY",
  "guard_pass": true,
  "compile_pass": true,
  "simulation_pass": false,
  "lint_pass": null,
  "synthesis_pass": null,
  "regression_pass": null
}
```

## 4.4 반드시 별도로 측정할 지표

```text
first_attempt_success_rate
final_success_rate
retry_rescue_count
semantic_retry_rescue_count
format_retry_rescue_count
average_attempts
median_attempts
median_latency
input_tokens
output_tokens
invalid_patch_rate
regression_rejection_count
```

### Semantic retry 정의

다음 중 하나를 만족하고 이후 attempt가 성공한 경우:

- patch guard를 통과했지만 compile fail
- compile pass + simulation fail
- target pass + lint/synthesis fail
- target validation pass + hidden regression fail

단순 malformed diff 복구는 semantic retry에 포함하지 않는다.

## 4.5 Single-shot 별도 실행

기존 CLI를 활용:

```bash
./scripts/run_benchmark.sh benchmark/public \
  --max-iterations 1 \
  --model gpt-6-sol \
  --reasoning-effort low

./scripts/run_benchmark.sh benchmark/hidden \
  --max-iterations 1 \
  --model gpt-6-sol \
  --reasoning-effort low
```

결과는 별도 디렉터리에 저장한다.

권장:

```text
results/v2_ablation/
  single_shot/
  full_loop/
  comparison.json
  comparison.csv
  comparison.md
```

---

# 5. Phase C — External Unseen Benchmark

# 5.1 Selection Principle

외부 benchmark case selection은 **모델 실행 전에 고정**해야 한다.

절대 금지:

- 결과가 좋은 case만 추리기
- 여러 번 실행 후 최고값만 보고하기
- 실패 case를 "호환성 문제"로 임의 제거
- gold/reference patch를 prompt에 노출

선택 기준과 제외 기준을 문서화한다.

파일:

```text
docs/EXTERNAL_BENCHMARK_PROTOCOL.md
```

---

# 5.2 1차 외부 benchmark — ChipBench Verilog Debugging

Codex는 먼저 최신 upstream 구조와 라이선스를 직접 확인한다.

조사 항목:

- repository URL
- license
- Verilog Debugging dataset 구조
- `prompt.txt`
- buggy RTL
- `ref.sv`
- `test.sv`
- simulator dependency
- redistribution 가능 여부
- testbench 실행 방식
- SystemVerilog feature 요구사항

## 사전 고정 selection

가능하다면 다음 네 유형에서 정렬순으로 3개씩 선택한다.

```text
Timing Bug       3
Assignment Bug   3
Arithmetic Bug   3
State Machine    3

Total = 12
```

실제 directory 명칭이 다르면 upstream을 따라 수정하되,
selection rule은 실행 전에 기록한다.

예:

```text
sort(path) 후 각 category 첫 3개
```

selection 결과:

```text
external/chipbench/selection_manifest.json
```

에 저장하고 commit한다.

## Prompt visibility

Agent 입력 가능:

- buggy RTL
- problem statement
- baseline failure log
- 필요 최소 visible context

Evaluator only:

- `ref.sv`
- hidden testbench / expected result
- upstream solution
- patch

## Adapter 방식

외부 benchmark를 내부 benchmark format으로 변환하는
독립 importer/adapter를 만든다.

예:

```text
tools/external/
  chipbench_import.py
  chipbench_validate.py
```

가능하면 원본 파일을 직접 수정하지 말고,
upstream source hash + local normalized case를 생성한다.

## 결과

```text
results/v2_external/chipbench/
  selection_manifest.json
  environment.json
  runs/
  summary.json
  summary.csv
  summary.md
```

보고:

```text
selected
compatible
attempted
fixed
first_attempt_fixed
semantic_retry_rescued
unsupported
infra_error
```

`unsupported`와 `failed`는 구분한다.

---

# 5.3 2차 외부 benchmark — HWE-Bench

ChipBench adapter와 평가 경로가 정상화된 뒤에만 진행한다.

Codex는 HWE-Bench 최신 구조와 resource requirement를 다시 조사한다.

목표는 전체 benchmark가 아니다.

우선:

```text
Ibex subset 3~5 real historical bug cases
```

정도로 시작한다.

선택 규칙 역시 사전 고정한다.

예:

```text
Ibex에서 공식 metadata 정렬순 첫 5개 중
현재 환경에서 reproducible하게 baseline fail이 확인된 case 전부
```

단, baseline fail을 확인하기 전에 model을 실행하지 않는다.

## HWE-Bench는 기존 case.json 구조에 억지로 맞추지 않는다

repository-scale benchmark일 수 있으므로
필요하면 별도 external runner를 만든다.

```text
external_runner/
  hwe_adapter.py
  hwe_provider_bridge.py
  hwe_result_normalizer.py
```

중요한 것은:

```text
Problem statement
        ↓
Model
        ↓
candidate patch
        ↓
official/native benchmark validation
```

구조를 유지하는 것이다.

## Resource가 과도하면

시간·disk·Docker resource가 제출 일정에 비해 과도하면
HWE-Bench를 강제로 완료하지 않는다.

대신 다음을 기록한다.

```text
docs/HWE_BENCH_FEASIBILITY.md
```

- 조사 내용
- 실제 필요한 image/disk
- 어떤 부분까지 확인했는지
- 왜 ChipBench 12 cases를 최종 external evidence로 사용했는지

이는 실패가 아니라 합리적인 scope control이다.

---

# 6. Phase D — Benchmark Integrity / Anti-Gaming 강화

## 6.1 Patch Integrity

기존 정책 유지 및 재검증:

- mutable RTL allowlist
- max file count
- max changed lines
- exact unified diff
- no fuzzy apply
- testbench modification 차단
- manifest modification 차단
- hash check
- fresh baseline per attempt

## 6.2 External dataset에서는 추가 차단

- reference solution path 접근 차단
- `.git` history 접근 금지
- network-disabled validator
- model tool use 비활성화
- external evaluator answer file prompt 노출 금지

## 6.3 Success Definition

`FIXED` 조건:

```text
Patch Guard PASS
Compile PASS
Visible Target Simulation PASS
Critical Lint PASS
Synthesis Sanity PASS
Hidden Regression PASS
Integrity PASS
```

외부 benchmark가 자체 official validation을 제공하면
그 official validation을 최우선 success criterion으로 추가한다.

---

# 7. Phase E — V2 결과 분석

다음 파일을 생성한다.

```text
results/v2/
  internal/
  ablation/
  external/
  evidence/
  V2_SUMMARY.json
  V2_SUMMARY.csv
  V2_SUMMARY.md
```

## 최소 결과표

```text
Internal V2
- total
- fixed
- first attempt
- final
- semantic retry rescue
- format retry rescue
- hidden regression rejection
- median time
- token usage

External
- selected
- attempted
- fixed
- first attempt
- semantic retry rescue
- unsupported
- infra failure

Ablation
- single-shot success
- full-loop success
- absolute delta
- retry-rescued count
```

## 보고 원칙

예:

```text
Internal: 30/30
External: 9/12
```

이면 그대로 보고한다.

외부 9/12을 75%가 낮아 보인다는 이유로 숨기지 않는다.

오히려 실패 3건을 분석한다.

```text
Failure #1: unsupported SV construct
Failure #2: model generated semantically wrong FSM patch
Failure #3: regression rejected target-pass candidate
```

이런 결과가 좋은 evidence다.

---

# 8. Phase F — Failure Case Analysis

최소 다음 세 종류의 대표 trace를 만든다.

## Case A — First-shot success

```text
baseline FAIL
→ hypothesis
→ patch
→ all validation PASS
```

## Case B — Semantic retry success

```text
baseline FAIL
→ patch #1
→ guard PASS
→ EDA FAIL
→ failure feedback
→ different hypothesis/patch #2
→ hidden regression PASS
```

## Case C — Final failure

```text
baseline FAIL
→ attempts exhausted / repeated failure / unsupported
→ safe stop
```

각 case는:

```text
results/v2/evidence/
  first_shot/
  semantic_retry/
  final_failure/
```

에 저장한다.

---

# 9. Phase G — Tests / CI

V2 변경 후 전체 테스트를 재정비한다.

최소 추가 테스트:

```text
test_context_visibility.py
test_hidden_regression_isolation.py
test_retry_reason.py
test_single_shot_mode.py
test_external_manifest.py
test_external_gold_isolation.py
test_external_adapter.py
test_v2_metrics.py
test_submission_packaging.py
```

최종:

```bash
make lint
make test
make test-integration
make e2e
make test-all
```

CI에서도 가능한 범위까지 실행한다.

외부 benchmark처럼 heavy한 작업은 CI mandatory로 만들지 않아도 된다.

---

# 10. Phase H — 경진대회 제출용 문서 재구성

이 프로젝트는 일반 오픈소스 프로젝트가 아니라
**AI 활용 경험 증거 제출물**로 읽혀야 한다.

따라서 Codex는 기존 Markdown 전체를 다시 검토하여
중복·과장·불필요한 구현 세부를 정리한다.

별도 지시문은 `CODEX_SUBMISSION_DOC_REVIEW.md`를 따른다.

---

# 11. 최종 문서 구조 권장

## Root

```text
README.md
PORTFOLIO_EVIDENCE.md
ARCHITECTURE.md
SUBMISSION_GUIDE.md
QUICKSTART.md
LICENSE
```

## docs/

```text
docs/
  BENCHMARK.md
  V2_EVALUATION.md
  EXTERNAL_BENCHMARK_PROTOCOL.md
  CODEX_CLI.md
  SECURITY.md
  DECISIONS.md
  RESEARCH.md
  THIRD_PARTY.md
  LIMITATIONS.md
```

개발 중 상세 journal:

```text
docs/internal/
  PROGRESS.md
  ISSUES.md
  V2_AUDIT.md
  ...
```

제출 ZIP에서는 `docs/internal/`은 제외 가능하다.

---

# 12. README 최종 목적

README 첫 화면에서 반드시 30초 내 이해 가능해야 한다.

권장 순서:

1. One-line problem
2. 핵심 diagram
3. Why this is not "LLM generated code"
4. 핵심 결과 4~6개
5. Internal vs External 구분
6. Quick demo
7. Evidence links
8. Limitations

### 가장 중요한 메시지

> The LLM proposes a repair. It never decides that the repair is correct.<br>
> Independent EDA tools and immutable evaluator tests decide whether a patch is accepted.

한국어 제출물에서는 자연스럽게 번역한다.

---

# 13. PORTFOLIO_EVIDENCE.md 최종 목적

경진대회 심사자가 보는 핵심 evidence 문서다.

권장 섹션:

```text
1. Problem
2. Why naive LLM repair is unsafe
3. Architecture
4. Control / Verification loop
5. Benchmark protocol
6. Internal V2 results
7. External unseen results
8. Single-shot vs feedback loop
9. Representative retry trace
10. Failure analysis
11. What I learned
12. Limitations
```

기술 스택 목록은 부차적이다.

---

# 14. 제출 ZIP

Codex는 최종적으로 50MB 이하 제출물을 생성하도록 한다.

권장:

```text
semidebug_submission/
  00_README.md
  01_PORTFOLIO_EVIDENCE.md
  02_ARCHITECTURE.md
  03_SUBMISSION_GUIDE.md

  src/
  scripts/
  benchmark/
  external_manifest/

  results/
    v2_summary/
    selected_evidence/

  docs/
    BENCHMARK.md
    V2_EVALUATION.md
    EXTERNAL_BENCHMARK_PROTOCOL.md
    LIMITATIONS.md

  Dockerfile
  Makefile
  pyproject.toml
  uv.lock
  LICENSE
  THIRD_PARTY.md
```

제외:

```text
.venv/
node_modules/
.cache/
.git/
full external dataset
large docker images
credentials
.env
API keys
Codex auth
raw duplicated logs
intermediate temporary workspaces
```

## ZIP sanity check

자동 검사:

- size < 50MB
- no secret
- no absolute local path
- README links resolve
- quickstart syntax correct
- results referenced by docs actually included
- third-party notices included
- hidden evaluator answer/reference solution은 필요 이상 포함하지 않음

---

# 15. 제출 직전 Final Verification

Codex는 다음 순서로 수행한다.

```bash
git status
make lint
make test-all

./scripts/run_demo.sh --replay
# live 실행은 필요 시 별도 수행

python scripts/package_submission.py
unzip -l <submission.zip>
```

그리고 새로운 clean temporary directory에서:

```bash
unzip <submission.zip>
cd <submission>
./scripts/bootstrap.sh
./scripts/run_demo.sh --replay
```

가능하면 scripted demo도 실행한다.

실제 live AI benchmark 전체 재실행은 사용량 때문에
최종 package validation 단계에서 강제하지 않는다.

---

# 16. Codex 최종 보고서

작업 종료 시 Codex는 `docs/V2_COMPLETION_REPORT.md`를 만든다.

반드시 포함:

## 구현 변경

- 무엇을 변경했는가
- 어떤 이유인가
- 주요 파일

## 평가 설계 변경

- hidden regression
- context isolation
- retry taxonomy
- single-shot ablation
- external benchmark

## 실제 결과

실행한 결과만 작성.

## 실패/미완료

숨기지 않는다.

## 문서 변경

- 어떤 문서를 병합/정리/삭제/이동했는가
- 이유

## 제출 package

- ZIP 파일명
- 크기
- SHA256
- included evidence

---

# 17. Definition of Done

다음을 모두 만족하면 V2 완료로 본다.

- [ ] V1 결과 frozen
- [ ] V2 Audit 작성
- [ ] hidden evaluator source가 LLM context에서 분리됨
- [ ] leak 방지 자동 테스트 존재
- [ ] retry reason taxonomy 구현
- [ ] single-shot vs full-loop 결과 생성
- [ ] internal benchmark 재측정
- [ ] 외부 benchmark selection protocol 사전 고정
- [ ] ChipBench external cases 실제 실행
- [ ] external success/failure 모두 raw evidence 보존
- [ ] 가능하면 semantic retry 실제 사례 확보
- [ ] HWE-Bench feasibility 조사
- [ ] 가능하면 HWE-Bench real bug 3~5개 실행
- [ ] README 제출형으로 재편집
- [ ] PORTFOLIO_EVIDENCE 업데이트
- [ ] BENCHMARK/V2_EVALUATION 업데이트
- [ ] limitations 명시
- [ ] third-party attribution 확인
- [ ] 50MB 이하 ZIP 생성
- [ ] clean extraction sanity check
- [ ] V2 completion report 작성

---

# 18. 중요한 판단 기준

이 프로젝트의 목표는 성공률을 최대한 높이는 것이 아니다.

더 중요한 것은:

```text
문제 정의
→ AI가 후보를 만든다
→ 시스템이 AI를 제한한다
→ deterministic tool이 검증한다
→ 실패 evidence가 다음 reasoning으로 돌아간다
→ 수정이 실제로 검증된다
→ 성공/실패 모두 재현 가능한 evidence로 남는다
```

이 과정을 경진대회 심사자가 명확하게 볼 수 있도록 만드는 것이다.

성공률이 낮아지더라도 외부 unseen benchmark와 hidden regression을 도입한 결과가
더 신뢰할 수 있다면 V2의 가치가 높아진 것이다.
