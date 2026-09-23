# Codex 지시문 — SemiDebug Agent V2 제출 직전 보강

## 목적

현재 SemiDebug Agent V2의 benchmark 결과와 raw evidence는 그대로 보존한 채, 제출 전 아래 세 가지 문제만 보강한다.

1. `./scripts/run_demo.sh`의 기본 데모를 **V2 hidden-regression 구조를 실제로 사용하는 데모**로 교체
2. Git 이력을 근거로 `PROVENANCE.json` 생성
3. `106 tests`, lint, packaging 검사 결과를 실제 실행 로그/JSON으로 보존

마지막에는 제출 ZIP을 다시 만들고 clean extraction 검증까지 수행한다.

이 작업은 **기존 V1/V2 benchmark 결과를 다시 튜닝하거나 성공률을 바꾸는 작업이 아니다.**

---

# 0. 절대 규칙

먼저 repository 전체를 직접 확인하고 실제 현재 구조에 맞춰 작업하라.

금지:

- 기존 `results/live_codex/` 수정 또는 삭제
- 기존 `results/v2/internal/` raw result 수정
- 기존 `results/v2/external/` raw result 수정
- benchmark 성공/실패 case 변경
- V1/V2 headline 숫자 재작성 또는 미화
- benchmark를 다시 실행한 뒤 더 좋은 결과로 기존 측정값 교체
- ChipBench selection manifest 수정
- GitHub visibility 변경
- remote push / release 수행
- 실행하지 않은 테스트를 `PASS`로 기록
- Docker가 없거나 명령이 실패했는데 성공 로그 생성
- API key, Codex auth, `.env`, credential을 ZIP에 포함

새로 얻은 검증 결과는 반드시 별도 verification artifact로 저장한다.

---

# 1. 작업 시작 전 상태 확인

먼저 아래를 실행하고 상태를 기록한다.

```bash
git status --short
git rev-parse HEAD
git branch --show-current
git tag --list
git log --oneline --decorate -20
```

현재 dirty working tree가 있다면 사용자 작업을 임의로 덮어쓰지 마라.

가능하면 이번 보강 작업은 별도 branch에서 진행한다.

예:

```bash
git switch -c submission-hardening
```

단, branch가 이미 존재하거나 현재 환경에서 적절하지 않으면 실제 repository 상태에 맞춰 판단하고 이유를 기록한다.

작업 전 상태를:

```text
docs/internal/SUBMISSION_HARDENING_AUDIT.md
```

에 기록한다.

---

# 2. Task A — 기본 Demo를 V2 hidden-regression fixture로 교체

## 2.1 먼저 현재 데모 경로 확인

반드시 다음을 읽는다.

```text
scripts/run_demo.sh
run_demo.sh
examples/
benchmark_v2/
src/semidebug/context/selector.py
src/semidebug/agent/orchestrator.py
src/semidebug/benchmark/loader.py
tests/
README.md
QUICKSTART.md
SUBMISSION_GUIDE.md
```

현재 기본 live demo가 `examples/fifo_off_by_one`처럼
target과 regression이 같은 TB source를 공유한다면 V2 핵심 메시지와 불일치한다.

---

## 2.2 V2 전용 Demo fixture 생성

가장 안전한 방법은 `benchmark_v2/`의 실제 V2 case 구조를 참고하여
작고 독립적인 demo fixture를 새로 만드는 것이다.

권장 예:

```text
examples/fifo_off_by_one_v2/
  case.json
  rtl/
    fifo.v
  tb/
    fifo_target_tb.v
    fifo_hidden_regression_17_tb.v
    fifo_hidden_regression_103_tb.v
  expected/
    ...
```

실제 repository schema가 다르면 현재 V2 case schema를 그대로 따른다.

### 필수 조건

1. `target.sources`와 모든 `regression.sources`가 서로 다른 source file이어야 한다.
2. model-visible source와 evaluator-only regression source가 물리적으로 구분되어야 한다.
3. `prompt_visible` 같은 현재 V2 visibility field가 존재한다면 명시적으로 설정한다.
4. hidden regression source/path/detail은 provider context에 들어가면 안 된다.
5. regression은 target보다 더 긴 시나리오 또는 다른 directed vectors를 가져야 한다.
6. testbench와 manifest는 immutable이어야 한다.
7. 기존 V2 validation gates를 그대로 사용해야 한다.
8. demo를 위해 validation을 약화시키지 마라.

가능하면 기존 V2 FIFO case를 기반으로 복사하되,
benchmark 원본을 직접 수정하지 말고 `examples/` 아래에 독립 fixture를 만든다.

---

## 2.3 Scripted demo response도 새 fixture에 맞춘다

현재 `--scripted` mode가 어떤 response JSON / fake provider를 사용하는지 확인한다.

새 V2 demo fixture에 맞는 **known correct patch**를 scripted response로 제공한다.

주의:

- scripted demo는 AI 성능 평가가 아니다.
- 그러나 Icarus/VVP, Verilator, Yosys, hidden regression, integrity 검증은 실제로 실행되어야 한다.
- README에서도 계속 이 차이를 명확히 표시한다.

---

## 2.4 `scripts/run_demo.sh` 수정

최종적으로:

```bash
./scripts/run_demo.sh
```

은 새 V2 hidden-regression demo fixture를 대상으로 live Codex 경로를 사용해야 한다.

```bash
./scripts/run_demo.sh --scripted
```

도 동일 V2 fixture를 사용해야 한다.

`--replay`가 여전히 V1 `results/sample_run`을 보여준다면,
가능하면 V2 representative evidence로 변경한다.

우선순위:

1. V2 semantic retry evidence
2. V2 first-shot evidence
3. 기존 V1 replay는 별도 옵션으로 남겨도 됨

단, raw V2 result를 수정하지 않는다.

---

## 2.5 Demo visibility 자동 테스트 추가

최소 하나의 자동 테스트를 추가한다.

예:

```text
tests/unit/test_default_demo_visibility.py
```

검증할 것:

- default demo case를 loader로 읽을 수 있음
- `target.sources`와 regression sources가 disjoint
- regression source가 `prompt_visible`에 없음
- `select_context()` 결과 serialized string에 hidden regression path/content marker가 없음
- target source는 context에 있음

추가로 가능하면:

```text
tests/e2e/test_default_demo.py
```

에서 scripted demo가 실제 EDA + hidden regression을 통과하는지 확인한다.

---

# 3. Task B — `PROVENANCE.json` 추가

## 3.1 목적

ZIP에 `.git/`을 넣지 않아도 다음 provenance를 확인할 수 있게 한다.

- V1 baseline commit
- V1 baseline tag
- ChipBench selection freeze commit
- V2 internal evaluation source commit
- V2 external evaluation source commit
- final submission commit
- commit ancestry 관계
- 핵심 파일 SHA256

---

## 3.2 값은 문서에서 복사하지 말고 Git에서 직접 읽는다

현재 문서에서 후보 commit을 참고할 수는 있지만,
최종 JSON 값은 반드시 실제 Git 명령으로 검증한다.

최소 확인:

```bash
git rev-parse semidebug-v1-baseline
git rev-parse HEAD
git show --no-patch --format='%H %cI %s' <commit>
```

ChipBench selection commit은 현재 repository history에서
`external/chipbench/selection_manifest.json`이 고정된 commit을 직접 확인한다.

예:

```bash
git log --follow --oneline -- external/chipbench/selection_manifest.json
```

필요하면:

```bash
git blame
git show <commit>:external/chipbench/selection_manifest.json
```

으로 검증한다.

---

## 3.3 ancestry 검증

다음을 실제로 실행한다.

```bash
git merge-base --is-ancestor <v1_baseline> <final_head>
git merge-base --is-ancestor <selection_commit> <external_eval_commit>
git merge-base --is-ancestor <internal_eval_commit> <final_head>
git merge-base --is-ancestor <external_eval_commit> <final_head>
```

exit code 0/1을 기록한다.

문서의 기대값과 다르면 문서를 억지로 맞추지 말고 실제 Git history를 보고한다.

---

## 3.4 핵심 artifact SHA256

최소:

```text
external/chipbench/selection_manifest.json
results/v2/internal/comparison.json
results/v2/external/chipbench/evaluation.json
docs/V2_EVALUATION.md
PORTFOLIO_EVIDENCE.md
README.md
```

의 SHA256을 계산한다.

또한 가능하면 V1 핵심:

```text
results/live_codex/summary.md
```

도 포함한다.

---

## 3.5 권장 파일

```text
results/v2/PROVENANCE.json
```

예시 schema:

```json
{
  "generated_at_utc": "...",
  "repository": "SemiDebug Agent",
  "v1": {
    "tag": "semidebug-v1-baseline",
    "commit": "...",
    "tag_resolves_to_expected_commit": true
  },
  "chipbench_selection": {
    "commit": "...",
    "manifest_sha256_at_commit": "...",
    "working_tree_manifest_sha256": "...",
    "manifest_unchanged_since_selection": true
  },
  "evaluations": {
    "internal_source_commit": "...",
    "external_source_commit": "..."
  },
  "submission": {
    "source_commit": "..."
  },
  "ancestry": {
    "v1_is_ancestor_of_submission": true,
    "selection_is_ancestor_of_external_evaluation": true,
    "internal_evaluation_is_ancestor_of_submission": true,
    "external_evaluation_is_ancestor_of_submission": true
  },
  "artifacts": {
    "README.md": "sha256:...",
    "PORTFOLIO_EVIDENCE.md": "sha256:...",
    "results/v2/internal/comparison.json": "sha256:...",
    "results/v2/external/chipbench/evaluation.json": "sha256:..."
  }
}
```

필요하면 schema를 실제 history에 맞게 조정한다.

### 중요

`final submission commit`은 circular dependency가 생길 수 있다.

`PROVENANCE.json` 자체를 commit하면 HEAD가 바뀌기 때문이다.

따라서 다음 중 한 가지를 명시적으로 선택한다.

### 방법 A — source commit + package commit 분리

- provenance 생성 전 source commit을 `evaluated_source_commit`으로 기록
- provenance/package 변경을 별도 commit으로 생성
- 마지막에는 `packaging_commit`을 별도 metadata 파일 또는 completion report에서 기록

### 방법 B — package-time metadata

`PROVENANCE.json`을 packaging 시 생성하여 Git tracked file로 commit하지 않고 ZIP에만 넣는다.

둘 중 repository에 더 적합한 방식을 선택하고 문서에 설명한다.

**존재하지 않는 self-hash/final commit을 억지로 만들지 마라.**

---

# 4. Task C — Verification logs 보존

## 4.1 새 verification 디렉터리

권장:

```text
results/v2/verification/
```

최소:

```text
environment.json
lint.log
test_all.log
scripted_demo.log
package_scan.json
clean_extract.log
verification_summary.json
```

기존에 유사 파일이 있다면 중복을 만들지 말고 V2 경로에 정리한다.

---

## 4.2 Environment 기록

실제 실행 전에 기록:

```text
UTC timestamp
OS
architecture
Python version
uv version
Docker version
Codex CLI version
Git commit
```

Codex auth token, username, credential path는 저장하지 않는다.

---

## 4.3 Lint 실제 실행

repository에서 공식 lint command를 확인한 뒤 실행한다.

예:

```bash
make lint > results/v2/verification/lint.log 2>&1
```

exit code를 별도로 기록한다.

명령이 다르면 실제 Makefile 기준으로 사용한다.

---

## 4.4 전체 106 tests 실제 실행

Docker가 필요한 현재 공식 command를 사용한다.

예:

```bash
make test-all > results/v2/verification/test_all.log 2>&1
```

반드시 log에서 실제:

```text
106 passed
```

또는 이에 상응하는 현재 결과를 확인한다.

### 만약 test 개수가 변경되었다면

문서의 `106`을 억지로 유지하지 말고,
왜 변경되었는지 확인한다.

이번 보강에서 test를 추가하면 예를 들어:

```text
108 passed
```

가 될 수 있다.

그 경우 문서도 **최신 실제 test count**로 바꾼다.

`106 passed`는 역사적 완료보고서 기록으로 남길 수 있으나,
최종 README/Completion Report의 현재 검증 수치는 새 값을 사용한다.

### Docker 사용 불가 시

절대 PASS로 기록하지 말 것.

```json
{
  "status": "NOT_RUN",
  "reason": "Docker unavailable"
}
```

처럼 기록한다.

---

## 4.5 Scripted demo 실행

새 V2 demo fixture를 대상으로:

```bash
./scripts/run_demo.sh --scripted \
  > results/v2/verification/scripted_demo.log 2>&1
```

다음을 확인한다.

- baseline failure
- patch accepted
- compile pass
- simulation pass
- lint pass
- synthesis pass
- hidden regression pass
- integrity pass
- final FIXED

실행 결과가 실패하면 package를 만들기 전에 원인을 수정한다.

---

# 5. Task D — 문서 최소 보완

대규모 문서 재작성은 하지 않는다.

다음만 필요한 만큼 갱신한다.

## README.md

- 60초 demo가 이제 V2 hidden regression demo라는 것을 정확하게 기술
- scripted demo는 AI benchmark가 아니라는 기존 표현 유지
- provenance / verification evidence 링크를 근거 섹션에 짧게 추가

## QUICKSTART.md

실제 최신 demo command가 맞는지 검토.

## SUBMISSION_GUIDE.md

다음을 추가:

```text
Provenance:
results/v2/PROVENANCE.json

Latest local verification:
results/v2/verification/verification_summary.json
```

## V2_COMPLETION_REPORT / submission completion report

이번 보강 후 새 ZIP:

- 파일 수
- byte size
- SHA256
- 실제 test count
- demo fixture 변경

을 최신 값으로 갱신한다.

과거 ZIP hash를 최신 ZIP hash처럼 남겨두지 않는다.

---

# 6. Task E — Submission package 재생성

현재 package script를 먼저 읽는다.

```text
scripts/package_submission.py
```

다음 파일이 최종 ZIP에 포함되도록 한다.

```text
results/v2/PROVENANCE.json
results/v2/verification/verification_summary.json
results/v2/verification/lint.log
results/v2/verification/test_all.log
results/v2/verification/scripted_demo.log
```

단, 크기가 과도한 raw log는 필요하면 tail/summary 형태로 curated한다.

50MB 제한을 유지한다.

---

# 7. Package scanner

기존 package scanner가 있으면 확장하고,
없으면 package 검증 함수를 만든다.

최소 검사:

```text
ZIP < 50MB
.env 없음
credential/auth 없음
.git 없음
absolute local path 없음
broken relative Markdown link 없음
README 존재
PORTFOLIO_EVIDENCE 존재
PROVENANCE.json 존재
verification_summary.json 존재
external reference solution 없음
ChipBench test/ref source 원본 불필요하게 포함하지 않음
```

결과:

```text
results/v2/verification/package_scan.json
```

예:

```json
{
  "status": "PASS",
  "zip_bytes": 0,
  "file_count": 0,
  "under_50mb": true,
  "secret_scan": "PASS",
  "markdown_links": "PASS",
  "absolute_paths": "PASS",
  "git_metadata_absent": true
}
```

---

# 8. Clean extraction verification

최종 ZIP을 임시 디렉터리에 새로 푼다.

예:

```bash
tmp=$(mktemp -d)
unzip dist/SemiDebug_Agent_V2_Submission.zip -d "$tmp"
cd "$tmp/<submission-root>"
```

최소:

```bash
./scripts/bootstrap.sh
./scripts/run_demo.sh --replay
./scripts/run_demo.sh --scripted
```

가능하면:

```bash
make lint
make test-all
```

까지 다시 수행한다.

결과를:

```text
results/v2/verification/clean_extract.log
```

에 보존한다.

주의: clean extraction 후 log를 최종 ZIP 안에 다시 넣으려 하면 ZIP hash가 바뀌는 순환이 발생한다.

따라서:

1. package 생성
2. package 자체 검증
3. clean extraction 실행
4. 외부 completion report에 clean extraction 결과 기록

방식으로 처리하거나,
package 내부 log와 package 후 log를 명확하게 분리한다.

---

# 9. Final ZIP hash

최종 파일 생성 후 실제 값을 계산한다.

```bash
shasum -a 256 dist/SemiDebug_Agent_V2_Submission.zip
wc -c dist/SemiDebug_Agent_V2_Submission.zip
unzip -Z1 dist/SemiDebug_Agent_V2_Submission.zip | wc -l
```

이 세 값을 Completion Report의:

```text
Path
Size
File count
SHA256
```

과 일치시키고 다시 확인한다.

---

# 10. 최종 자동 검증

Codex는 완료라고 선언하기 전에 아래를 프로그램적으로 검사한다.

## Demo

```text
default demo case target source ∩ regression sources == ∅
hidden regression path ∉ provider serialized request
hidden marker ∉ provider serialized request
scripted demo == FIXED
```

## Provenance

```text
V1 tag resolves
selection manifest working hash == frozen selection hash
selection commit ancestor of external evaluation commit
evaluation commits ancestor of submission source
```

## Raw benchmark protection

작업 전후 아래 raw result의 SHA256이 동일한지 확인한다.

최소:

```text
results/live_codex/summary.md
results/v2/internal/comparison.json
results/v2/external/chipbench/evaluation.json
results/v2/internal/full_loop_public/results.json
results/v2/internal/full_loop_hidden/results.json
results/v2/external/chipbench/live/results.json
```

하나라도 달라졌으면 즉시 조사하고,
이번 보강 때문에 raw benchmark result가 변경됐다면 원복한다.

---

# 11. Codex 최종 보고 형식

작업 종료 시 다음 순서로 사용자에게 보고한다.

## 1. 변경 사항

```text
Default demo
Provenance
Verification evidence
Packaging
Docs
```

## 2. 실제 실행 결과

반드시 실행한 것만:

```text
lint: PASS/FAIL/NOT_RUN
tests: N passed / FAIL / NOT_RUN
scripted V2 demo: PASS/FAIL
package scan: PASS/FAIL
clean extraction: PASS/FAIL
```

## 3. Benchmark preservation

```text
V1 raw result unchanged: yes/no
V2 internal raw result unchanged: yes/no
V2 external raw result unchanged: yes/no
```

## 4. 최종 ZIP

```text
path:
bytes:
file count:
SHA256:
```

## 5. 남은 리스크

없으면 `No new blocking issue found`라고 쓰고,
있으면 숨기지 말고 적는다.

---

# 12. Definition of Done

- [ ] 기존 benchmark raw result 불변 확인
- [ ] default live demo가 V2 hidden regression fixture 사용
- [ ] scripted demo도 동일 V2 fixture 사용
- [ ] target/regression source가 서로 분리됨
- [ ] provider context에 hidden regression source/path/content가 없음
- [ ] demo visibility 자동 테스트 추가
- [ ] `PROVENANCE.json` 생성
- [ ] Git ancestry 실제 검증
- [ ] selection manifest freeze hash 실제 검증
- [ ] lint 실제 실행 기록
- [ ] 전체 test suite 실제 실행 기록
- [ ] V2 scripted demo 실제 EDA 실행 기록
- [ ] package scan JSON 생성
- [ ] README/QUICKSTART/SUBMISSION_GUIDE 최소 업데이트
- [ ] 제출 ZIP 재생성
- [ ] 50MB 미만 확인
- [ ] ZIP SHA256 계산
- [ ] clean extraction 검증
- [ ] Completion Report 최신화
- [ ] 실패나 미실행 항목을 PASS로 표현하지 않음

---

# 핵심 의도

이번 작업의 목적은 benchmark 점수를 올리는 것이 아니다.

기존 결과:

```text
Internal full loop: 30/30
Independent one-shot: 24/30
External ChipBench: 5/12
Semantic retry rescue: 3
```

는 그대로 보존한다.

보강하는 것은 오직:

```text
실행 데모가 실제 V2 설계를 대표하도록 만들기
+
Git provenance를 ZIP에서도 검증 가능하게 만들기
+
테스트/패키징 성공 주장을 실제 로그로 증명하기
```

이다.

이 세 작업이 끝나면 새로운 ZIP을 제출 후보로 사용한다.
