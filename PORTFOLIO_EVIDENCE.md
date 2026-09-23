# SemiDebug Agent — Portfolio Evidence

## 1. Problem

LLM은 RTL 수정안을 빠르게 만들 수 있지만, 컴파일 성공만으로 기능 보존을 보장할 수 없습니다. 테스트 우회, 회귀, 잘못된 성공 판정도 생길 수 있습니다. SemiDebug는 **AI의 후보 생성과 수정 승인 판단을 분리**해 이 문제를 다룹니다.

## 2. AI 활용 방식

호스트의 Codex CLI `gpt-6-sol / low`가 실패 로그와 보이는 소스를 바탕으로 원인 가설과 unified diff를 제안합니다. 모델은 EDA 명령을 실행하거나 성공을 선언하지 않습니다. 실패 후에는 이전 가설·diff와 검증 상태를 받아 다음 후보를 만듭니다. 상세한 평가 전용 정답과 회귀 출력은 모델 요청에 들어가지 않습니다.

## 3. 왜 결정적 검증이 필요한가

SemiDebug는 패치를 격리된 복사본에 적용한 뒤 Icarus/VVP, Verilator, Yosys, 평가 전용 회귀와 SHA256 무결성을 확인합니다. V2 내부 사례는 target과 회귀 테스트가 별도 소스입니다. 외부 ChipBench 사례는 원본 공식 테스트의 mismatch 결과까지 통과해야 합니다. 테스트 실행이 0으로 종료돼도 신뢰할 완료 표식이나 공식 결과가 없으면 성공으로 처리하지 않습니다.

## 4. 구조와 통제 경계

[아키텍처](docs/ARCHITECTURE.md)는 모델 입력, 정확한 패치 정책, 네트워크 없는 EDA 실행, 평가 전용 테스트, 근거 저장의 경계를 보여줍니다. 패치는 명시된 RTL 파일 최대 2개와 변경 줄 40개로 제한됩니다. 실패한 후보는 버리고 모든 시도는 원래 baseline에서 시작합니다. 입력 파일은 덮어쓰지 않습니다.

## 5. 평가 프로토콜

V1 결과는 `semidebug-v1-baseline` 태그와 원본 결과 파일로 보존했습니다. V2에서는 먼저 정상 설계 6종이 target·별도 hidden 회귀를 통과하고 오류 30종이 실패하는 것을 실제 EDA로 확인했습니다. 알려진 정답 패치를 준 파이프라인 점검도 30/30을 통과했지만 **AI 수리 성능으로 계산하지 않았습니다**. 외부 12건은 [선정 목록](external/chipbench/selection_manifest.json)을 모델 실행 전에 커밋하고 파일 해시를 고정했습니다. [전체 프로토콜과 결과](docs/V2_EVALUATION.md).

## 6. 내부 결과

V2 내부 최대 3회 실행은 **30/30** 수정했고 첫 시도는 **23/30**이었습니다. 별도의 1회 실행은 **24/30**이었습니다. 두 조건 모두 Codex CLI 0.156.1, 동일 모델·노력도·Docker EDA·데이터셋을 사용했습니다. 다만 별도 실행은 확률적인 새 제안을 생성하므로, 같은 실행의 첫 제안과 최종 결과를 짝지어 본 23/30 → 30/30이 더 직접적인 관찰입니다. 내부에서 되살린 7건은 모두 diff 파싱 오류였고 semantic retry 성공은 없었습니다. [사례별 비교](results/v2/internal/comparison.md).

## 7. 외부 선정 사례 결과

ChipBench zero-shot 디버깅에서 네 오류 유형별 3건씩 12건을 사전 선정했습니다. 정상 reference와 공식 테스트의 호환성은 **12/12**, 오류 baseline의 실패 재현도 **12/12**이었습니다. 실제 모델 실행에서는 **5/12** 수정, 첫 시도 **2/12**, semantic retry로 추가 통과 **3건**이었습니다. 최종 실패 **7건**은 제외하지 않았습니다. 범주별 결과는 산술 1/3, 할당 2/3, 상태기계 2/3, 타이밍 0/3입니다. [선정·실패 포함 전체 결과](results/v2/external/chipbench/evaluation.md).

## 8. 대표적인 피드백과 실패

[외부 arithmetic Prob001](results/v2/evidence/semantic_retry/report.md)의 첫 후보는 compile·target·lint·synthesis를 통과했지만 공식 회귀에서 실패했습니다. 두 번째 후보가 같은 검사와 공식 회귀를 모두 통과했습니다. 이 사례는 형식 오류 수정과 구별되는 실제 의미상의 재시도입니다.

[외부 arithmetic Prob002](results/v2/evidence/final_failure/report.md)는 첫 번째와 세 번째 후보가 공식 회귀에서 실패했고 중간 후보는 diff 파싱에 실패했습니다. 세 번의 제한이 끝나자 `MAX_RETRY`로 중단하고 모든 근거를 저장했습니다. 내부의 [형식 오류 복구](results/v2/evidence/format_retry/report.md)와 [1회 시도 실패](results/v2/evidence/one_shot_failure/report.md)도 별도로 제시합니다.

## 9. 배운 점과 한계

V1의 100% 내부 결과만으로 일반화를 주장할 수 없었습니다. 별도 평가용 테스트, 외부 사전 선정, 재시도 사유 분류를 도입하자 통과 5건과 실패 7건을 구분해 설명할 수 있게 됐습니다. 높은 최종 성공률보다 **어떤 근거가 승인으로 이어졌고 어디서 중단됐는지 재현 가능하게 남기는 것**이 이 프로젝트의 핵심입니다.

이 결과는 소형 RTL과 작은 외부 표본에 한정됩니다. 내부 holdout은 같은 여섯 설계의 다른 mutation이고, 외부 사례가 모델 사전학습에 없었다는 증거는 없습니다. 시뮬레이션 통과는 formal equivalence나 실리콘 검증이 아닙니다. HWE-bench는 구조와 리소스를 조사했지만 실행하지 않았습니다. [상세 한계](docs/LIMITATIONS.md) · [원시 결과](results/v2/README.md).
