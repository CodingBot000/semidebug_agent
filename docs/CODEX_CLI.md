# Codex CLI로 로컬 LLM 실행

## 설정

호스트에서 Node.js/npm, uv, Docker를 준비한 뒤 실행합니다.

```bash
npm install -g @openai/codex
codex login
codex login status
./scripts/bootstrap.sh
./scripts/doctor.sh
./scripts/run_demo.sh
./scripts/run_benchmark.sh benchmark/public
./scripts/run_benchmark.sh benchmark/hidden
```

2026-09-23 실제 실행 환경은 Codex CLI **0.156.1**, ChatGPT 로그인, **gpt-6-sol / low**입니다. 기존 0.147.0은 모델 요청을 거부하여 업데이트했습니다. 사용 가능한 다른 모델은 다음처럼 명시할 수 있습니다.

```bash
./scripts/run_demo.sh codex --model gpt-6-sol --reasoning-effort low
./scripts/run_benchmark.sh benchmark/public --model gpt-6-sol --reasoning-effort low
```

`SEMIDEBUG_CODEX_MODEL`, `SEMIDEBUG_REASONING_EFFORT`, `SEMIDEBUG_CODEX_TIMEOUT`으로도 설정할 수 있습니다. 실행별 모델과 추론 강도는 결과에 기록합니다. 실패 시 다른 모델로 자동 전환하지 않습니다.

## 인증 및 사용량

호스트의 공식 `codex exec`가 기존 ChatGPT 로그인을 사용합니다. 애플리케이션이 인증 토큰을 추출하거나 API 키로 바꾸지 않습니다. API 키 환경 변수는 CLI 추론 프로세스에 전달하지 않습니다. ChatGPT 플랜의 Codex 사용 한도를 소비하며 무제한 무료 실행을 의미하지 않습니다. 구독 실행의 API 환산 비용은 산정하지 않고 `estimated_cost: null`로 기록합니다.

CLI는 임시 디렉터리에서 읽기 전용, ephemeral, 사용자 설정 무시 모드로 실행합니다. 도구 사용은 비활성화하고 structured JSON 응답만 받습니다. 모델에는 오류 소스·테스트·검증 근거만 전달하며 정답과 evaluator는 제공하지 않습니다. 실제 EDA는 네트워크 없는 Docker에서 실행하며 Codex 인증 파일을 마운트하지 않습니다.

## 측정과 토큰 절감

한 번의 추론으로 가설과 패치를 함께 생성합니다. 짧은 전용 시스템 지시문과 성공 로그 요약을 사용하지만 원본 검증 로그는 보존합니다. 동일 FIFO 데모의 단일 파일럿에서 입력 토큰은 16,854 → 6,520개(61.3% 감소), 두 실행 모두 첫 시도에 통과했습니다. 이는 반복 실험으로 검증한 평균 절감률이나 수리 성능 개선 주장이 아닙니다. 이후 공개/holdout 벤치마크에는 같은 최적화 설정을 고정했습니다.

실행 결과에는 모델·CLI 버전·추론 강도·호출 수·입력/캐시/출력 토큰·시간·도구 사용 이벤트 수를 저장합니다. 시간은 로컬 Docker 검증까지 포함한 관측값이며 전용 성능 실험 환경의 수치는 아닙니다.

## 다른 실행 모드

- `./scripts/run_demo.sh --scripted`: 알려진 패치와 실제 EDA로 파이프라인 검증.
- `./scripts/run_demo.sh --replay`: 기존 기록 표시.
- `./scripts/run_demo.sh --api`: `.env`의 OPENAI_API_KEY / OPENAI_MODEL을 사용하는 별도 API 모드.

## 공식 자료

- [Codex 인증](https://learn.chatgpt.com/docs/auth)
- [비대화형 실행 및 structured output](https://learn.chatgpt.com/docs/non-interactive-mode)
- [설정 참조](https://learn.chatgpt.com/docs/config-file/config-reference)
