# Codex 지시문 — SK hynix AI Hackathon 제출용 문서/프로젝트 정리

아래 지시를 **현재 SemiDebug Agent 저장소의 실제 상태를 직접 확인한 후** 수행하라.

목표는 문서를 예쁘게 만드는 것이 아니라,
심사자가 짧은 시간 안에 다음을 검증할 수 있도록 만드는 것이다.

1. 어떤 문제를 풀었는가?
2. AI에게 무엇을 맡겼는가?
3. AI에게 무엇을 맡기지 않았는가?
4. 실패 결과를 어떻게 검증하고 다음 시도로 전달했는가?
5. 결과가 실제 실행을 통해 측정됐는가?
6. 내부 benchmark와 외부 unseen benchmark를 구분했는가?
7. 한계를 숨기지 않았는가?
8. ZIP을 받아 실제로 구조와 evidence를 확인할 수 있는가?

---

# 1. 작업 전 프로젝트 전체 조사

먼저 다음을 수행하라.

```bash
git status
git rev-parse HEAD
find . -maxdepth 3 -type f | sort
```

그 다음 모든 주요 Markdown 문서와 결과 요약 파일을 읽어라.

특히:

```text
README.md
PORTFOLIO_EVIDENCE.md
ARCHITECTURE.md
QUICKSTART.md

docs/**/*.md
results/**/summary.md
results/**/summary.json
results/**/results.csv
```

그리고 아래를 작성하라.

```text
docs/internal/DOCUMENT_AUDIT.md
```

포함:

- 문서 목록
- 각 문서 목적
- 중복 섹션
- 서로 다른 숫자
- 오래된 정보
- 실제 코드와 맞지 않는 설명
- 실행 불가능한 명령
- broken link
- private GitHub 때문에 외부에서 열리지 않는 링크
- 과장처럼 읽힐 수 있는 표현
- 제출자가 꼭 이해해야 하는 핵심 메시지
- 삭제/병합/이동 제안

**Audit 전에 문서를 대규모 수정하지 마라.**

---

# 2. Source of Truth 규칙

숫자는 반드시 실제 결과 파일에서 가져와라.

우선순위:

```text
raw run result
> aggregated JSON/CSV
> generated summary
> documentation prose
```

문서와 raw result가 다르면 문서를 raw result에 맞춰 고친다.

실행하지 않은 숫자를 만들지 마라.

다음 표현은 구분해서 사용하라.

```text
pipeline validation
live AI repair
internal benchmark
external benchmark
single-shot
full feedback loop
first-attempt
final success
scripted provider
real model
```

특히:

`known patch pipeline 30/30`을 `AI repair 30/30`처럼 표현하지 마라.

---

# 3. 경진대회용 Narrative

문서 전체가 다음 핵심 narrative를 유지해야 한다.

## Problem

LLM이 RTL patch를 생성할 수는 있지만,
문법 오류·기능 회귀·테스트 우회·허위 성공 판정이 발생할 수 있다.

## Design principle

LLM은:

```text
diagnosis
hypothesis
candidate patch
```

만 제안한다.

LLM은 성공 판정을 하지 않는다.

SemiDebug가:

```text
patch policy
compile
simulation
lint
synthesis
hidden regression
integrity check
```

를 실행하여 최종 승인 여부를 결정한다.

## Feedback loop

실패한 candidate는 원본에 누적 적용하지 않는다.

항상 baseline에서 새 candidate를 만들고,
이전 attempt의 diff·실패 로그·EDA evidence를 다음 reasoning에 전달한다.

## Evidence

결과는 다음처럼 구분한다.

```text
Internal benchmark
External unseen benchmark
Single-shot
Full feedback loop
Semantic retry
Format retry
Final failure
```

## Limitation

다음을 숨기지 않는다.

- research prototype
- 작은 RTL scope
- finite test != formal proof
- limited SystemVerilog coverage
- external benchmark sample size
- subscription-based Codex execution
- production silicon/physical verification 아님

---

# 4. README.md 편집 지침

README는 심사자가 첫 번째로 볼 가능성이 높다.

길더라도 첫 화면은 매우 압축적으로 구성하라.

권장 구조:

```text
# SemiDebug Agent

1문장 설명

[Architecture diagram]

## Why this exists

## Key results

Internal
External
Ablation

## How it works

## 60-second demo

## Evidence

## Limitations

## Reproduce
```

### Key results에서

표 하나로 끝내라.

예:

| Evaluation | Dataset | Result |
|---|---:|---:|
| Internal live AI | 30 | ... |
| First proposal | 30 | ... |
| Full loop | 30 | ... |
| External unseen | 12 | ... |

실제 V2 결과가 존재하는 경우에만 넣어라.

### README에서 줄여야 하는 것

- 긴 설치 배경
- 모든 내부 구현 세부
- 동일한 한계 반복
- 모든 결과 파일 링크 나열
- 개발 journal 내용

상세 내용은 docs로 이동한다.

---

# 5. PORTFOLIO_EVIDENCE.md 편집 지침

이 문서는 **심사 포트폴리오 핵심 문서**로 취급하라.

권장:

```text
# SemiDebug Agent — Portfolio Evidence

## 1. Problem
## 2. AI 활용 방식
## 3. Why deterministic verification matters
## 4. Architecture
## 5. Guardrails
## 6. Evaluation protocol
## 7. Internal results
## 8. External unseen results
## 9. Single-shot vs feedback loop
## 10. Representative retry trace
## 11. Failure case
## 12. What was learned
## 13. Limitations
```

중요:

`기술 스택을 사용했다`보다
`왜 이런 통제가 필요했고 어떤 failure를 잡았는지`가 더 중요하다.

---

# 6. ARCHITECTURE.md 편집 지침

Architecture는 구현 모듈 목록이 아니라
**control boundary**가 보이게 만들어라.

강조:

```text
LLM boundary
Evaluator boundary
Immutable files
Network boundary
Credential boundary
Patch boundary
```

다이어그램에서 다음을 시각적으로 구분할 수 있도록
Mermaid source를 정리하라.

```text
LLM
Orchestrator
Patch Guard
Isolated Workspace
EDA Validators
Hidden Evaluator
Evidence Store
```

---

# 7. BENCHMARK / V2_EVALUATION

`docs/BENCHMARK.md`는 dataset/methodology 중심으로 유지한다.

V2는 별도:

```text
docs/V2_EVALUATION.md
```

작성.

포함:

- exact model
- reasoning effort
- Codex CLI version
- runtime
- machine observation 주의
- benchmark selection
- split
- prompt-visible data
- evaluator-only data
- number of calls
- tokens
- first attempt
- final success
- retry reason
- external benchmark
- failure breakdown

모든 결과에는 날짜를 적어라.

---

# 8. 외부 benchmark Attribution

ChipBench/HWE-Bench 등을 사용하면:

```text
docs/THIRD_PARTY.md
```

를 검토·보완하라.

반드시 확인:

- license
- upstream repository
- 사용한 commit/release
- 어떤 파일을 재배포했는가
- 어떤 파일은 다운로드 스크립트만 제공하는가
- 원본 benchmark를 수정했는가
- reference solution을 package에 포함할 필요가 있는가

라이선스가 불명확하면 임의로 재배포하지 마라.

그 경우:

```text
download script
selection manifest
upstream hash
```

만 포함하는 방식을 사용하라.

---

# 9. 문서 중복 정리

동일 설명을 여러 문서에 복붙하지 마라.

권장 ownership:

```text
README
→ 빠른 이해

PORTFOLIO_EVIDENCE
→ 제출용 이야기 + 핵심 evidence

ARCHITECTURE
→ control flow / boundary

BENCHMARK
→ benchmark methodology

V2_EVALUATION
→ 최신 측정 결과

CODEX_CLI
→ 실행 provider 세부

SECURITY
→ sandbox/security

LIMITATIONS
→ 제약을 한 곳에 상세 정리
```

다른 문서는 링크를 사용한다.

---

# 10. Internal 문서 분리

심사자가 굳이 볼 필요 없는 개발 이력:

```text
PROGRESS.md
ISSUES.md
V2_AUDIT.md
DOCUMENT_AUDIT.md
debug notes
```

는 가능하면:

```text
docs/internal/
```

로 이동한다.

단, Git history와 link가 깨지지 않도록 수정한다.

---

# 11. 제출 Package 전용 SUBMISSION_GUIDE.md

새로 작성하라.

길이는 짧게.

포함:

```text
What this project demonstrates
Where to start
How to replay evidence
How to run scripted demo
How to run live demo
Which results are real model results
Which are scripted tests
External benchmark note
Known limitations
```

심사자는 이 파일만 읽고도 다음 파일로 이동할 수 있어야 한다.

---

# 12. Private GitHub 처리

현재 repository가 private인지 확인하라.

private이면 README의 clone URL을
경진대회 ZIP 안에서 반드시 필요한 기본 진입점처럼 쓰지 마라.

다음 중 하나로 문서를 구성한다.

```text
A. ZIP 자체가 self-contained
B. GitHub URL은 optional
```

Codex가 repository visibility를 변경하지 마라.

public 전환 여부는 사용자 결정이다.

---

# 13. 제출 ZIP 자동검사

package script를 검토하고 다음을 추가하라.

검사:

```text
size < 50MB
.env 없음
credentials 없음
auth 없음
.git 없음
absolute local path 없음
broken markdown relative links 없음
README 존재
PORTFOLIO_EVIDENCE 존재
results summary 존재
third-party attribution 존재
```

가능하면 package 후 자동으로 SHA256을 생성한다.

---

# 14. 최종 Review Checklist

문서 수정이 끝난 후 Codex 자신이 아래 질문에 답하라.

- "AI가 실제로 뭘 했나?"가 30초 안에 보이는가?
- "AI가 틀리면 어떻게 막나?"가 보이는가?
- "실제로 실행했나?"에 raw evidence가 있는가?
- "30/30이 너무 좋은데 benchmark가 쉬운 것 아닌가?"에 답할 외부 evidence가 있는가?
- "loop가 정말 필요한가?"에 ablation 결과가 있는가?
- "retry가 단순 diff format 복구인가, semantic retry인가?"가 구분되는가?
- "test를 모델이 봤나?"에 prompt visibility 설명이 있는가?
- "실패한 case도 보여주나?"가 충족되는가?
- "한계를 숨겼나?"가 충족되는가?
- "ZIP만 받아도 읽을 수 있나?"가 충족되는가?

하나라도 애매하면 문서를 수정하라.

---

# 15. 최종 산출물

최소:

```text
README.md
PORTFOLIO_EVIDENCE.md
ARCHITECTURE.md
SUBMISSION_GUIDE.md

docs/BENCHMARK.md
docs/V2_EVALUATION.md
docs/EXTERNAL_BENCHMARK_PROTOCOL.md
docs/LIMITATIONS.md
docs/THIRD_PARTY.md

docs/internal/DOCUMENT_AUDIT.md
docs/V2_COMPLETION_REPORT.md

submission/*.zip
```

마지막에는 사용자에게 다음을 보고할 수 있도록
`docs/V2_COMPLETION_REPORT.md`에 정리하라.

```text
1. 실제 변경 파일
2. benchmark protocol
3. 실행 결과
4. 실패 case
5. 문서 정리 내역
6. 제출 ZIP path / size / SHA256
7. 아직 남아 있는 리스크
```

---

# 16. 가장 중요한 금지사항

경진대회 제출물이라는 이유로 결과를 미화하지 마라.

- 실패 삭제 금지
- benchmark post-selection 금지
- 정답 prompt 노출 금지
- scripted 결과를 live AI 결과처럼 표현 금지
- external benchmark adapter 오류를 AI failure로 혼동 금지
- AI failure를 infrastructure failure로 숨기기 금지
- 실제 측정하지 않은 latency/cost/success 수치 작성 금지
- formal verification을 했다고 표현 금지
- silicon/production verification을 했다고 표현 금지

이 프로젝트의 강점은 100%라는 숫자가 아니라,
**확률적인 AI 후보를 deterministic validation과 immutable evidence로 통제하는 과정이 재현 가능하게 남는 것**이다.
