# 다른 컴퓨터에서 이어서 하기 (내부 · 팀 전용)

최신 PC 검증 결과와 이어갈 항목은 **[CONTINUE_HERE.md](CONTINUE_HERE.md)**부터 확인하세요. 아래는 최초 설정 안내이며, 기존 PC의 경로나 미검증 상태가 포함되어 있습니다.

## 저장소
- 앱 코드: https://github.com/Sweet-Butters/cutline (비공개)
- 내부 자료: https://github.com/Sweet-Butters/cutline-internal (비공개) — 이 문서, HANDOFF.md, 실측(measure/), 조사(research/, trinx/), 발표자료 소스(pitch/), 침착맨 시연 프로젝트 메타데이터(demo-chim/, 영상 제외)

## 필요한 프로그램
- Git, Node.js 20+ (원 PC는 24), ffmpeg/ffprobe (PATH), Python 3.10+ (yt-dlp·채점용, numpy)
- Claude Code CLI(`claude`)·Codex CLI(`codex`) 구독 로그인. 유료 API 키는 쓰지 않는다.
- Windows 권장(앱 패키징 스크립트가 PowerShell). macOS/Linux는 확장 개발 실행만 가능(미검증).

## 1. 앱 빌드
```
git clone https://github.com/Sweet-Butters/cutline.git
cd cutline
npm ci
npm test
npm run test:integration      # VS Code 테스트 인스턴스를 내려받아 실행
npm run package               # dist/cutline.vsix
powershell -ExecutionPolicy Bypass -File app/build.ps1   # VSCodium 받아 app/dist/Cutline-win-x64.zip 생성
```
- 개발 중엔 VS Code에서 이 폴더를 열고 F5(확장 개발 호스트)로도 실행 가능.

## 2. 침착맨 시연 프로젝트 복원 (영상은 다시 받기)
영상 원본(권리 미확인 · 공개 금지 · 내부/심사용만):
- 원본(2:01:33, 침착맨 게임 풀버전): https://www.youtube.com/watch?v=wnXAkjgVELc
- 사람 편집본(23:18, 침착맨 플러스): https://www.youtube.com/watch?v=GVHagGsmLck

```
git clone https://github.com/Sweet-Butters/cutline-internal.git
cd cutline-internal/demo-chim
python -m venv .venv && .venv\Scripts\pip install yt-dlp
mkdir sources
.venv\Scripts\python -m yt_dlp -f "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720]" --merge-output-format mp4 -o "sources/original.%(ext)s" https://www.youtube.com/watch?v=wnXAkjgVELc
.venv\Scripts\python -m yt_dlp -f "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720]" --merge-output-format mp4 -o "reference/human_edit.%(ext)s" https://www.youtube.com/watch?v=GVHagGsmLck
```
- 원 PC의 원본은 `original.mp4` 231MB, 길이 7293.06초. 다른 포맷으로 받히면 길이가 수십 ms 다를 수 있으나 타임라인(초 단위)은 그대로 쓸 수 있다.
- **수정 필요:** `demo-chim/tools/vidcli.js` 3번째 줄의 `D:/orca/projects/video-ide/out/cli.js`를 새 PC의 `cutline/out/cli.js` 경로로 바꾼다.
- 이미 들어 있는 것: `transcripts/original.mp4.json`(faster-whisper base), `reference/human_edit.timeline.json`(정답 99구간), `style.md`, `AGENTS.md`/`CLAUDE.md`, `tools/compare.js`.
- Cutline에서 처음 열면 재생용 변환(프록시)에 20~45분 걸린다.
- ⚠️ 원 PC에서 2시간 원본이 Cutline 패널에서 실제 재생(canplay)되는지 아직 확인 안 됨(07:25 기준 조사 중). 안 되면 원본에서 30분만 잘라 쓰는 것을 고려.

## 3. 실측(채점) 다시 돌리기
`measure/` 참고. 요약:
- 조건별 폴더(sources/ 원본 하드링크, transcripts/, timeline.json(원본 전체 1클립), tools/vidcli.js, 필요하면 style.md/signals)를 만들고 `run.sh <폴더> "<프롬프트>"` → `claude -p` 실행(약 2~3분).
- `eval.py`가 F1·±3초 F1·핵심 장면·무작위·음량 기준선을 계산. 경로는 원 PC 기준이라 맞게 수정. 음량 기준선은 원본 오디오를 8kHz mono raw로 뽑아 사용(`ffmpeg -i original.mp4 -ac 1 -ar 8000 -f s16le audio8k.raw`).
- 목표: 음량 기준선 F1 0.35 / 핵심 장면 15개를 에이전트 구성으로 넘기기.

## 4. 발표자료
`pitch/`에서 `deck.json`, `facts.json` 수정 → `python build.py` → `out/Cutline_pitch.pdf`/`.pptx`. PowerPoint COM으로 PDF를 뽑으므로 PowerPoint가 켜져 있지 않을 때 실행. 대본 `script.md`, Q&A `QA.md`.

## 5. 주의
- 공개 저장소는 이 두 저장소를 그대로 공개하지 말고, 코드·README·샘플만 담은 정리본으로 따로 만든다.
- 원 PC(회광)에서도 07:30 이후 Claude가 작업 중일 수 있음(침착맨 재생 문제, 발표자료 검수). 같은 파일을 동시에 고치지 않게, 작업 전 `git pull`.
