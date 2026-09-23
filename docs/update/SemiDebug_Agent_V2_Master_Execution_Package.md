# SemiDebug Agent V2 — Master Execution Package

이 파일은 두 문서의 목적과 사용 순서를 설명한다.

1. `SemiDebug_Agent_V2_Enhancement_Plan.md`
   - V2 평가 설계와 개발 전 과정을 Codex가 실행하기 위한 계획서
   - hidden regression, single-shot ablation, external benchmark, retry taxonomy, packaging 포함

2. `CODEX_SKHynix_Submission_Doc_Review_Instructions.md`
   - 현재 repository의 Markdown/README/결과 문서를 경진대회 제출용으로 재검토·편집·정리하는 지시문
   - Codex가 먼저 repository audit을 하고 실제 결과를 source of truth로 삼도록 요구

## 권장 사용법

Codex 새 세션에서 먼저 다음과 같이 지시한다.

```text
현재 저장소를 먼저 전체 분석해라.
첨부한 SemiDebug_Agent_V2_Enhancement_Plan.md를 마스터 계획으로 사용하고,
CODEX_SKHynix_Submission_Doc_Review_Instructions.md의 문서 정리 규칙도 함께 적용해라.

중요:
- V1 결과는 동결하고 덮어쓰지 마라.
- 먼저 V2_AUDIT.md와 DOCUMENT_AUDIT.md를 작성하라.
- 추가 조사할 내용은 공식 upstream 문서/저장소를 직접 확인하라.
- 외부 benchmark case selection은 모델 실행 전에 고정하라.
- 모든 수치는 실제 실행 결과만 사용하라.
- 개발, 검증, benchmark, 문서 정리, 50MB 이하 제출 ZIP 생성까지 끝까지 수행하라.
- 중간에 선택지가 생기면 가장 보수적이고 재현 가능한 방향을 선택하고 결정 근거를 DECISIONS/V2 report에 기록하라.
```

Codex가 계획과 실제 repository 사이의 차이를 발견하면,
repository의 실제 코드와 현재 upstream 문서를 우선하여 계획을 수정하되,
왜 수정했는지 반드시 기록하게 한다.
