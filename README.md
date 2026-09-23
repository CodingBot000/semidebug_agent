# SemiDebug Agent

RTL 오류의 원인을 추론하고 최소 패치를 제안한 뒤, **실제 EDA 도구와 변경 불가능한 테스트를 통과한 수정만 승인하는** CLI 프로토타입입니다.

## 현재 결과

- 자체 제작 RTL 6종: counter, FIFO, round-robin arbiter, FSM controller, ALU, pulse detector.
- 오류 사례 **30개**: 공개 24개 / holdout 6개. 정상 버전은 모든 검증·회귀 테스트를 통과하고, 오류 버전 30개 모두 실제 실패를 재현했습니다.
- 단위·EDA 통합·스크립트 기반 E2E 테스트 **95개 통과**.
- 알려진 정답 패치를 공급한 **파이프라인 검증 30/30 통과**. 이는 AI 수리 성공률이 아닙니다.
- **실제 Codex CLI gpt-6-sol / low 평가: 공개 24/24 + holdout 6/6 수정 성공.** 첫 시도 23/30, 중앙 시간 14.68초. [실제 측정 결과](results/live_codex/summary.md) · [CLI 설정](docs/CODEX_CLI.md)

## 왜 필요한가

LLM이 제시한 코드가 컴파일되는 것과 원래 기능을 유지하며 오류를 고치는 것은 다릅니다. SemiDebug는 추론, 최소 변경, 외부 검증, 실패 피드백을 연결하고 원본·테스트 무결성을 확인합니다. 근거 로그와 diff가 함께 남으므로 수리가 실패한 이유도 확인할 수 있습니다.

## 동작 방식

```mermaid
flowchart LR
    A[오류 RTL] --> B[Baseline 검증]
    B --> C[근거 수집 + LLM 추론]
    C --> D[최소 diff]
    D --> E[패치 정책 검사]
    E --> F[격리된 복사본에 적용]
    F --> G[Compile + Simulation + Lint + Synthesis]
    G -->|실패| C
    G -->|통과| H[전체 회귀 + 테스트 해시]
    H -->|통과| I[수정 승인 + Evidence Report]
    H -->|실패| C
```

원본 소스는 직접 변경하지 않습니다. 승인된 RTL은 실행 결과의 `final/rtl/`에 저장합니다. 모든 재시도는 원래 baseline을 기준으로 하며, 최대 3회·동일 패치 반복·연속 금지 패치 등에서 안전하게 종료합니다.

## 빠른 실행

필요 도구: Git, [uv](https://docs.astral.sh/uv/getting-started/installation/), 실행 중인 Docker.

```bash
git clone https://github.com/CodingBot000/semidebug_agent.git
cd semidebug_agent
./scripts/bootstrap.sh
./scripts/run_demo.sh --scripted
```

`--scripted`는 미리 정한 패치를 사용하지만 Icarus·Verilator·Yosys와 회귀 테스트는 **매번 실제 실행**합니다. API 호출은 없습니다.

기록만 읽으려면:

```bash
./scripts/run_demo.sh --replay
```

화면에 `RECORDED RUN`이 표시되며 도구를 새로 실행하지 않습니다.

실제 AI 실행:

```bash
npm install -g @openai/codex
codex login
./scripts/doctor.sh
./scripts/run_demo.sh
./scripts/run_benchmark.sh benchmark/public
./scripts/run_benchmark.sh benchmark/hidden
```

기본 실행은 Codex CLI의 ChatGPT 인증을 사용하며 구독 사용 한도를 소비합니다. API 키는 필요하지 않습니다. 실제 확인 모델은 `gpt-6-sol`, 추론 강도는 `low`입니다. [모델 변경·인증·사용량 안내](docs/CODEX_CLI.md). 별도 API 모드는 `.env` 설정 후 `./scripts/run_demo.sh --api`로 실행합니다.

## 검증 정책

| 단계 | 도구 | 승인 조건 |
|---|---|---|
| Compile | Icarus 11.0, `-g2012` | 종료 코드 0 |
| Simulation | VVP `-N` | 종료 코드 0 + immutable testbench 완료 표식 |
| Lint | Verilator 5.006 | 오류 및 중요 warning 없음 |
| Synthesis sanity | Yosys 0.23 | hierarchy/proc/opt/check -assert 통과 |
| Regression | 별도 seed 17, 103 | 더 긴 시나리오 모두 통과 |
| Integrity | SHA256 | 원본 및 immutable 파일 보존 |

최신 upstream 대신 고정된 Debian 도구 버전을 사용합니다. Python 3.12.14와 기반 이미지 digest, 잠긴 Python 의존성으로 재현 환경을 제공합니다. [조사](docs/RESEARCH.md) · [결정 근거](docs/DECISIONS.md)

## CLI 및 테스트

```bash
uv run semidebug --help
./scripts/doctor.sh
make test             # 호스트 단위 테스트
make test-integration # Docker에서 정상/오류 RTL 검증
make e2e              # 실제 EDA + scripted provider
make test-all
make lint
make package
```

네이티브 EDA 도구가 있으면 `uv run semidebug fix <case-directory>`를 직접 실행할 수 있습니다. 입력 형식은 [예제 manifest](examples/fifo_off_by_one/case.json)와 같습니다. 임의의 shell build 명령은 지원하지 않습니다. 각 명령은 `--help`를 제공합니다.

## 근거와 벤치마크

- [실제 LLM 데모](results/live_demo/report.md) / [실제 AI 벤치마크](results/live_codex/summary.md)
- [측정 범위와 결과](docs/BENCHMARK.md)
- [첫 시도 성공](results/sample_run/report.md) / [재시도 성공](results/retry_run/report.md) / [실패 사례](results/failed_run/report.md)
- [파이프라인 결과 JSON](results/benchmark_results.json) / [CSV](results/benchmark_results.csv)
- [정상·오류 데이터셋 검증 로그](results/dataset_audit.json)
- [포트폴리오 설명](PORTFOLIO_EVIDENCE.md)

## 저장소 구조와 문서 안내

```text
src/semidebug/       CLI, 오케스트레이터, LLM provider, diff 검사, EDA 실행, 리포트
benchmark/           모델 평가용 공개 사례와 holdout 사례, manifest 및 immutable 테스트
examples/            FIFO 데모 입력과 scripted 응답
evaluator/           정상 RTL 정답과 mutation 정의; 런타임 모델 입력에서 격리
tests/               unit, integration, end-to-end 테스트
results/             검증 결과, 실행 추적, 데모 및 실제 모델 벤치마크
scripts/             설치, 진단, 데모, 벤치마크, 제출물 패키징 명령
docs/                아키텍처, 설정, 보안, 결정, 진행 및 이슈 기록
```

정상 정답과 mutation 정의는 모델 입력에 전달하지 않습니다.

처음 보는 개발자는 **이 README → [빠른 시작](QUICKSTART.md) → [아키텍처](docs/ARCHITECTURE.md) → [실제 벤치마크와 방법](docs/BENCHMARK.md)** 순서로 읽으면 됩니다. 로컬 AI 실행은 [Codex CLI 설정](docs/CODEX_CLI.md), OpenAI API 설정은 `.env.example` 및 `--api` 실행 경로를 참고하세요. 주요 결정·보안 경계·외부 의존성은 각각 [DECISIONS](docs/DECISIONS.md), [SECURITY](docs/SECURITY.md), [THIRD_PARTY](docs/THIRD_PARTY.md)에 있습니다. 개발 진행과 해결된 이슈는 [PROGRESS](docs/PROGRESS.md), [ISSUES](docs/ISSUES.md)에 기록합니다.

## 한계

소형 자체 제작 RTL을 대상으로 한 연구·포트폴리오 프로토타입입니다. 상용 반도체 EDA, silicon 검증, physical verification, formal equivalence를 대체하지 않습니다. Yosys의 기본 SystemVerilog 지원 범위는 제한적입니다. 테스트 통과가 모든 입력에 대한 정확성 증명은 아닙니다.

Codex CLI 경로에서 실제 AI 수리를 측정했으며 별도 API 경로는 모의 HTTP 테스트만 수행했습니다. Holdout은 다른 mutation을 사용하지만 같은 설계 계열이므로 독립 설계에 대한 일반화 결과가 아닙니다. 임의의 악성 HDL을 안전하게 실행하는 제품이 아니며, native/live 모드는 신뢰하는 입력만 사용합니다. [실행 경계와 보안](docs/SECURITY.md)

MIT 라이선스. 외부 도구 라이선스는 [THIRD_PARTY.md](docs/THIRD_PARTY.md)를 확인하세요.
