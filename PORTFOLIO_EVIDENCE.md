# SemiDebug Agent — Portfolio Evidence

## Problem

LLM이 제안한 RTL 수정은 문법 오류, 기능 회귀, 테스트 우회를 일으킬 수 있습니다. 이 프로젝트는 수정 후보와 최종 승인 판단을 분리해 외부 검증 결과로 수리를 통제합니다.

## Architecture and verification loop

명시적 상태 머신이 baseline 수집 → 근거 기반 가설 → 최소 unified diff → 정책 검사 → 임시 복사본 적용 → 독립 EDA → 전체 회귀를 수행합니다. 실패한 패치는 버리고 원래 baseline에서 다시 시작합니다. 이전 가설·diff·명령·실패 로그는 다음 추론에 전달됩니다. API 오류·반복 패치·재시도 제한은 기록을 남기고 종료합니다.

## Patch integrity

RTL allowlist, 정확한 hunk 적용, 최대 2파일/40줄 제한, 테스트·manifest 변경 차단과 SHA256 검사를 구현했습니다. 잘못된 패치를 임시 복사본에만 적용하고 원본의 무결성도 확인합니다. 테스트 완료 표식 없이 종료 코드만 0인 실행은 성공으로 보지 않습니다. 네이티브 프로세스는 timeout과 출력 제한을 적용하고 자식 프로세스를 정리합니다.

## Dataset and measured results

- 자체 제작 6종 RTL, 오류 30개(공개 24 / holdout 6), 8종 오류 범주.
- 정상 6종의 compile/simulation/lint/synthesis/회귀 통과, 오류 30개의 실제 실패 확인.
- 초기 최종 통합 실행에서 테스트 86개 통과.
- 미리 정한 올바른 패치를 넣은 파이프라인 검증 30/30 승인, 첫 실행 median 360.5 ms.
- **API 키가 없어 live LLM을 실행하지 않았으므로 AI 수리 성공률은 제시하지 않습니다.** 위 30/30은 정답을 공급한 파이프라인 테스트입니다.

## Evidence examples

[첫 시도 성공](results/sample_run/report.md)은 FIFO full 경계 수정 후 독립 도구와 회귀가 통과한 기록입니다. [재시도 성공](results/retry_run/report.md)은 counter의 첫 잘못된 경계 수정이 실패하고 두 번째 후보가 통과한 기록입니다. [실패 사례](results/failed_run/report.md)는 동일한 실패 패치 반복을 감지하고 중단한 기록입니다. 모두 provider는 scripted test double이며 EDA는 실제 실행됐습니다.

## What was learned

시뮬레이터 종료 코드만으로는 완료 여부를 충분히 판단할 수 없어 immutable 테스트의 완료 표식을 추가했습니다. Verilator의 스타일 경고와 width/latch 같은 중요한 경고를 분리했습니다. macOS Bash 3.2의 빈 배열 처리 문제도 실제 데모 진입점 실행으로 발견하고 수정했습니다. 성공 숫자만 보고하지 않고 검증 대상(데이터셋, 파이프라인, 실제 AI)을 구분하는 것이 재현 가능성을 높입니다.

## Limitations and next measurement

소형 RTL 연구용 프로토타입이며 실제 반도체 생산환경·silicon·physical verification을 수행하지 않았습니다. 유한 테스트는 formal correctness 증명이 아닙니다. lexical patch guard는 모든 악성 HDL 우회를 증명 수준으로 차단하지 못합니다. live provider는 HTTP 모의 테스트를 통과했지만 실제 endpoint 호환성과 모델 성능은 아직 검증되지 않았습니다. 다음 단계는 API 설정 후 공개 벤치마크의 실제 실패를 분석하고 동일 조건 재실행 및 holdout 평가를 수행하는 것입니다.
