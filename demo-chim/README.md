# Cutline 실영상 데모 — chim_003

침착맨 게임 풀버전 원본과 침착맨 플러스의 사람 편집본 **「침마에의 놀라운 지휘」**를 비교하는 로컬 프로젝트입니다. 비공개 해커톤 심사용이며 영상·대본을 업로드하거나 git remote를 만들지 않습니다.

- `sources/original.mp4`: 제공된 원본의 독립 복사본. 7,293.063초(2:01:33.063), 426×240 영상입니다. 프록시 변환으로 원본 화질이 좋아지지는 않습니다.
- `reference/human_edit.mp4`: yt-dlp로 받은 720p 편집본, 약 23분 18초.
- `timeline.json`: 원본 전체를 담은 클립 1개. 에이전트 편집 전 시작 상태입니다.
- `transcripts/original.mp4.json`: 실제 한국어 ASR, Cutline의 `[{start,end,text}]` 형식. 침묵에는 대본이 없으며 게임 용어·고유명사는 오인식될 수 있습니다.
- `reference/human_edit.timeline.json`: 기존 음성 정렬로 복원한 99개 구간, 편집본 순서. 모든 reason은 `사람 편집자 원본 구간`입니다.
- `style.md`: 이 한 쌍에서 관찰한 편집 규칙과 원본 시각 예시.
- `tools/compare.js`: 의존성 없는 Node 비교 도구. `compare.json`에 점수를 씁니다.
- `reference/`: 정렬 원자료, 통계, ASR 보고서, 상관 검증, 시작 상태 및 검증 기록.
- `.cutline-cache/`: 실제 Cutline 코드가 만든 재생 프록시.

원본: https://www.youtube.com/watch?v=wnXAkjgVELc (침착맨 게임 풀버전)  
사람 편집: https://www.youtube.com/watch?v=GVHagGsmLck (침착맨 플러스)

## 점수의 의미

기존 정렬의 편집본 길이는 1,398.190초이며 그중 1,307.980초(93.548%)를 복원했습니다. 미정렬 90.210초는 임의로 채우지 않았습니다. 따라서 reference 타임라인은 21:47.980이며, 사람 편집본 전체의 자막·효과·편집 경계를 완벽히 복제한 것이 아닙니다. 특히 정렬 블록 중앙값 3.994초는 실제 샷 길이와 같다고 단정할 수 없습니다.

동일 원본 파일의 시간 구간을 합집합으로 합쳐 교집합을 계산합니다. 반복 삽입은 고유 시간에 한 번만 반영하고, 재생 길이는 반복도 포함해 별도로 보고합니다. 파일이 다른 구간은 겹치지 않습니다. 순서·이야기 전달·자막·효과는 채점하지 않습니다. 스타일을 이 정답에서 도출했으므로 독립적인 일반화 성능 평가도 아닙니다.

Precision은 `겹친 초 / AI가 남긴 고유 초`, recall은 `겹친 초 / 정답이 남긴 고유 초`, F1은 두 값의 조화평균입니다.

원본 고유 보존 시간은 1,289.009초입니다. 전체 원본 시작 상태는 precision 약 0.176745, recall 1, F1 약 0.300396입니다. 정답 자기 비교는 F1 1입니다. 점수만 올리려고 정답 JSON을 복사하면 편집 데모의 의미가 없습니다.

```powershell
cd D:\orca\projects\cutline-demo-chim\project
node tools/vidcli.js validate
node tools/compare.js --self-test
node tools/compare.js
# 선택한 후보와 reference 비교 (경로는 project 기준)
node tools/compare.js reference/starting.timeline.json
```

`tools/vidcli.js`는 현재 머신의 `D:/orca/projects/video-ide/out/cli.js`를 읽기 전용으로 로드합니다. 쓰기와 캐시는 이 project에만 발생합니다. 이 폴더를 다른 머신으로 옮길 때는 설치된 Cutline CLI 경로에 맞게 wrapper를 수정해야 합니다. 이 작업을 위해 video-ide에서 빌드나 테스트를 실행하지 마세요.

## Cutline에서 열기

설치된 Cutline에서 **File → Open Folder…**로 이 `project` 폴더를 엽니다. `timeline.json`을 열고 **Open Video Panel** 명령으로 오른쪽 영상 패널을 엽니다. 기존 확장의 자동 열기가 설정되어 있으면 패널이 자동으로 나타납니다. 처음에는 2:01:33짜리 원본 클립 하나가 표시되어야 합니다.

WebM 기본 프록시와 H.264/MP3 호환 프록시를 사용합니다. 영상 패널에서 Play, 대본 클릭, 음성 출력은 촬영 전에 직접 확인하세요. 프록시 캐시 검증과 실제 UI 재생 검증은 서로 다릅니다.

## 3분 시연 대본

긴 ASR과 프록시 변환은 시연 전에 완료합니다. 에이전트의 전체 편집 시간이 3분 안에 끝난다는 보장은 없으므로, 실제 편집 과정을 미리 녹화해 시간 경과를 표시하며 축약하거나 편집이 끝날 때까지 발표를 멈춥니다. 실행하지 않은 작업을 실시간 결과인 것처럼 소개하지 않습니다.

1. **0:00–0:30** — `timeline.json`의 클립 1개와 2시간 원본을 보여 줍니다. “에이전트가 영상 파일 대신 JSON을 편집하고, 옆 패널이 저장 즉시 바뀝니다.”
2. **0:30–1:05** — `style.md`의 원본 시각 예시와 한국어 대본을 보여 줍니다. 터미널에서 아래 프롬프트를 실행합니다.
3. **1:05–2:05** — 편집 수행 구간(필요하면 시간 경과를 명시한 녹화). 새 JSON이 저장되면 약 20–25분으로 줄어드는 패널과 reason을 보여 줍니다. 첫 장면 및 중간 장면을 재생합니다.
4. **2:05–2:40** — `node tools/vidcli.js validate`, `node tools/compare.js`를 실행합니다. 시작 F1 0.3004와 실제 편집 후 점수를 비교합니다. “93.55% 정렬된 사람 편집의 원본 선택과 얼마나 겹치는지 보는 보조 지표”라고 설명합니다.
5. **2:40–3:00** — 사람 편집 MP4와 선택된 원본 장면을 짧게 비교합니다. 이 결과는 이 한 쌍의 데모이며 사람의 모든 편집 판단을 채점하지 않는다고 마무리합니다.

Claude Code에 그대로 입력:

```text
AGENTS.md, CLAUDE.md, style.md와 transcripts/original.mp4.json을 읽고 이 침착맨 원본을 20–25분 하이라이트로 편집해 줘. style.md에 적힌 이 영상 쌍의 근거를 따르고, 질문·시도·반응이 이해되도록 문장 경계를 살려 줘. timeline.json만 직접 수정해. 기존 장면을 트림·이동할 때 id를 유지하고 새로운 선택에는 새 id를 사용해. 각 클립의 reason을 구체적인 한국어로 써 줘. 선택 중 reference 폴더의 정답 타임라인이나 human_edit 영상을 열거나 복사하지 마. 완성 JSON을 저장한 뒤 node tools/vidcli.js validate와 node tools/compare.js를 실행하고 길이와 precision/recall/F1을 보고해 줘. 점수 확인 뒤 정답에 맞춰 재편집하지 마. 원본·대본·style·reference·도구는 수정하지 말고 업로드·push·외부 검색·API 호출은 하지 마.
```

Codex에 그대로 입력:

```text
이 폴더는 Cutline 영상 프로젝트야. AGENTS.md와 style.md를 읽고 transcripts/original.mp4.json에 근거해서 원본 전체를 20–25분으로 줄인 timeline.json을 작성해 줘. 질문·시도·반응의 맥락을 보존하고 반복·대기 구간을 줄여 줘. 같은 장면을 트림·이동하면 id를 유지하고 새 장면에는 새 id를 써. 각 reason은 선택 이유가 드러나는 한국어로 작성해. 선택 단계에서는 reference 폴더의 정답 타임라인과 human_edit 영상을 열거나 복사하지 마. 저장 후 node tools/vidcli.js validate, node tools/compare.js를 실행하고 길이와 precision/recall/F1을 보고해 줘. 점수를 본 뒤 정답에 맞춰 재편집하지 마. timeline.json 외의 자료나 도구는 바꾸지 말고 업로드·push·외부 검색·API 호출을 하지 마.
```

Claude Code/Codex 자체가 클라우드 모델을 사용하는 설정이라면 프롬프트와 읽은 대본이 해당 서비스로 전달될 수 있습니다. 이 프로젝트 제작은 로컬 ASR로 수행했습니다. **“어디에도 업로드하지 않음”을 엄격하게 유지하는 시연은 로컬 모델로 설정된 에이전트에서만 실행하세요.** 클라우드 에이전트 실행은 이 제작 작업에 포함하지 않았습니다.

시작 상태로 돌아갈 때는 현재 편집을 별도 파일로 보관한 뒤 `reference/starting.timeline.json`을 `timeline.json`으로 복사합니다. 초기 상태에서는 git 저장소나 remote가 없습니다. Versions 기능이 필요하면 촬영 전에 이 폴더 안에 별도의 로컬 git 저장소와 커밋을 준비하세요.

## 실측 및 검증

최종 실측은 `reference/asr_report.json`, `reference/proxy_report.json`, `reference/spotchecks.json`, `reference/validation.json`과 아래 검증 기록을 확인하세요. 상위 폴더의 `scripts/`는 재현 스크립트, `logs/`는 실행 로그, `.venv/`는 이 작업 전용 yt-dlp·faster-whisper 환경입니다. 외부 모델은 제공된 MVP의 base 모델 경로에서 읽기만 합니다.

| 항목 | 결과 |
|---|---|
| 다운로드 | 전용 venv의 yt-dlp, 720p AV1/AAC MP4, 성공 실행 51.08초 |
| ASR | faster-whisper 1.2.1, multilingual base, CPU int8, CPU 4스레드, beam 1, batch 4, temperature 0, VAD, 단어 타임스탬프 |
| ASR 반복 억제 | no_repeat_ngram_size=3, repetition_penalty=1.1, 이전 문맥 전달 안 함 |
| ASR 최종 실행 | 모델 처리 195.04초, 프로세스 전체 196.13초 |
| ASR 모든 실제 인식 시도 합계 | 780.60초(13분 0.60초). 중단한 순차 처리 387.51초와 초기 배치 처리 196.96초 포함. 설치·프록시 시간 제외 |
| 처리 범위 | 0–7,293.063초 전체, 연속된 5분 처리 창 25개. 마지막 창은 짧음 |
| 출력 대본 | 215구간, 첫 인식 00:13.010 / 마지막 인식 2:01:27.150, 인식 구간 합계 519.93초 |
| 대본 구간 검사 | 모든 구간이 원본 범위 안, 인접 구간 중복 0개, 최대 길이 11.99초 |
| 저신뢰 | 76/215구간(35.35%), 인식 구간 시간의 30.23%. `[ASR 저신뢰]`로 표시 |
| 정렬 독립 확인 | 6개 표본의 스펙트럼 상관 0.662–0.942, 잔여 오프셋 0–16ms. 관계없는 +60초 구간의 상관은 −0.008–0.121 |
| 영상 디코딩 | 편집본의 0초·690초·1390초에서 각 1초, FFmpeg 정상 종료 |

저신뢰 판정은 `avg_logprob < -1`, `no_speech_prob > 0.6`, `compression_ratio > 2.4`, `mean_word_probability < 0.5` 중 하나입니다. **이는 오류율 측정치가 아닙니다.** 원본 전체를 처리했지만 VAD로 빠진 구간, 음악에 묻힌 말, 게임의 영어 음성을 모두 정확히 받아썼다는 뜻은 아닙니다. 말이 적은 공연 구간이 많고, 일부 한국어 전사도 틀립니다. 사람이 모든 문장을 교정한 대본이 아닙니다.

실행한 검증 명령:

```powershell
# project 폴더에서: 실제 Cutline CLI / 비교 도구
node tools/vidcli.js validate
node tools/compare.js --self-test
node tools/compare.js reference/human_edit.timeline.json
node tools/compare.js

# 상위 cutline-demo-chim 폴더에서: 실제 Cutline validator를 읽기 전용 로드
node scripts/validate.js
.\.venv\Scripts\python.exe scripts/finalize_asr.py
.\.venv\Scripts\python.exe scripts/spotcheck.py

ffprobe -v error -show_format -show_streams -of json project/sources/original.mp4
ffprobe -v error -show_format -show_streams -of json project/reference/human_edit.mp4
ffmpeg -v error -threads 1 -ss 1390 -i project/reference/human_edit.mp4 -t 1 -f null -
```

`scripts/validate.js`는 현재 타임라인과 reference 타임라인을 각각 Cutline의 `validate`·`validateMedia`로 검증하고, 실제 `transcripts` 로더로 대본을 읽습니다. `scripts/finalize_asr.py`는 전체 처리 창의 연속성, 대본 시간 범위, 저신뢰 표식 개수를 검사합니다. `reference/self.compare.json`과 `reference/starting.compare.json`에 두 점수를 보존했으며 `compare.json`은 시작 상태 점수입니다.

초기 시행착오도 남겼습니다. 설치 완료 전에 한 번 실행한 ASR은 모듈 미설치로 실패했고 설치 후 해결했습니다. 첫 다운로드 호출은 PowerShell의 stderr 경고 처리로 중단됐으며, 로컬 캐시와 명시적 JavaScript challenge 지원을 적용한 재실행은 성공했습니다. 순차 ASR은 느려 중단했고, 단어 정렬 없는 배치 결과는 긴 시간 범위와 반복 출력 때문에 폐기했습니다. 최종 대본에는 **단어 정렬과 반복 억제를 적용한 마지막 실행만** 사용했습니다.

실제 Cutline 창의 Play·음성 출력·대본 클릭·에이전트 편집·최종 영상 export는 이 작업에서 실행하지 않았습니다. 영상 파일 검사와 프록시/스키마 검증을 UI 검증으로 대신 주장하지 않습니다. 다른 작업이 진행 중인 `video-ide`에는 빌드·설치·테스트·소스 편집을 하지 않았습니다.

## 프록시 실측

실제 Cutline CLI `node tools/vidcli.js proxies webm` 및 `proxies mp4`로 생성했습니다. 원본 전체 SHA-256과 프로필 문자열을 결합한 키가 정확히 일치하며, 두 파일 모두 640×360 / 24fps / 원본 전체 길이를 ffprobe로 확인했습니다.

| 형식 | 실제 변환 시간 | 캐시 재사용 CLI 시간 |
|---|---:|---:|
| webm | 2613.63초 (43.56분) | 0.68초 |
| mp4 | 1431.63초 (23.86분) | 0.85초 |

WebM CLI의 전체 경과 시간에는 ASR 때문에 명시적으로 일시정지한 780.60초가 포함되어 있습니다. 위 변환 시간은 그 시간을 제외했습니다. 스레드 2개인 기존 Cutline 변환 설정을 그대로 사용했으며, 다른 작업의 시스템 부하 영향을 받는 실측값입니다. 기본 WebM은 VP8/Vorbis, 호환 MP4는 H.264/MP3입니다. 완성된 `.cutline-cache/`를 함께 유지하면 첫 열기 때 이 변환을 반복하지 않습니다. 실제 앱의 첫 프레임 표시 지연을 측정한 수치는 아닙니다.

최종 검증 명령: 상위 폴더에서 `.\.venv\Scripts\python.exe scripts/final_verify.py`. 결과는 `reference/final_verification.json`에 있습니다.
