# 다른 컴퓨터에서 이어서 하기 (내부 · 팀 전용)

최신 PC 검증 결과와 이어갈 항목은 **[CONTINUE_HERE.md](CONTINUE_HERE.md)**부터 확인하세요. 아래는 최초 설정 안내이며, 기존 PC의 경로나 미검증 상태가 포함되어 있습니다.

## 저장소
- 앱 코드: https://github.com/Sweet-Butters/cutline (비공개)
- 내부 자료: https://github.com/Sweet-Butters/cutline-internal (비공개) — 이 문서, HANDOFF.md, 실측(measure/), 조사(research/, trinx/), 발표자료 소스(pitch/), 침착맨 시연 프로젝트 메타데이터(demo-chim/, 영상 제외)

## 필요한 프로그램
- Git, Node.js 20+ (원 PC는 24), ffmpeg/ffprobe (PATH), Python 3.10+ (yt-dlp·채점용, numpy)
- Codex CLI(`codex`) 설치와 본인 구독 로그인. `codex login status`로 확인하고 미로그인이면 `codex login`을 실행한다. 앱 대화창에서도 Codex를 선택한다. Claude Code CLI는 사용할 때만 별도로 로그인한다. 유료 API 키는 쓰지 않는다.
- Windows 권장(앱 패키징 스크립트가 PowerShell). macOS/Linux는 확장 개발 실행만 가능(미검증).
- GitHub CLI(`gh`): 비공개 Release의 영상·프록시를 자동 복원할 때 사용. `gh auth status`로 확인하고 미로그인이면 `gh auth login`으로 저장소 접근 가능한 계정에 로그인한다.

## 1. 앱 빌드
검증한 설치본을 바로 쓰려면 [비공개 GitHub Release](https://github.com/Sweet-Butters/cutline/releases/tag/v0.1.0-handoff-20261120)에서 `Cutline-win-x64.zip`과 해시를 받아 압축을 푼 뒤 `Cutline.exe`를 실행한다. 아래는 소스에서 직접 빌드하는 방법이다.

두 저장소를 담을 공통 상위 폴더에서 실행한다. 이미 clone했다면 해당 `git clone` 줄은 건너뛴다.

```powershell
git clone https://github.com/Sweet-Butters/cutline.git
git clone https://github.com/Sweet-Butters/cutline-internal.git
cd cutline
npm ci
npm test
npm run test:integration      # VS Code 테스트 인스턴스를 내려받아 실행
npm run package               # dist/cutline.vsix
powershell -ExecutionPolicy Bypass -File app/build.ps1   # VSCodium 받아 app/dist/Cutline-win-x64.zip 생성
cd ..                         # 두 저장소의 공통 상위 폴더로 돌아오기
```
- 개발 중엔 VS Code에서 이 폴더를 열고 F5(확장 개발 호스트)로도 실행 가능.

## 2. 침착맨 시연 프로젝트 복원 (GitHub Release에서 받기)

**기본 방법:** [비공개 영상 Release](https://github.com/Sweet-Butters/cutline-internal/releases/tag/demo-chim-media-20261120)에서 검증한 원본·사람 편집본·재생 프록시를 받는다. YouTube 재다운로드 없이 이전 PC와 동일한 파일로 복원한다. 영상은 `git clone`에 포함되지 않으므로 아래 단계가 필요하다.

```powershell
cd cutline-internal
gh auth status
# 아직 로그인하지 않았다면: gh auth login
powershell -NoProfile -ExecutionPolicy Bypass -File .\demo-chim\restore-github.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\demo-chim\restore-github.ps1
```

스크립트는 `demo-chim/media-manifest.json`에 따라 파일 크기·SHA-256을 검사하고 올바른 폴더에 둔다. 이미 같은 파일이 있으면 보존하며, 다른 기존 원본을 임의로 덮어쓰지 않는다. CLI 대신 직접 다운로드해 manifest의 `path`대로 배치할 수도 있다. 검증한 프록시까지 복원하면 패키지 Cutline에서 전체 영상 변환을 반복할 필요가 없다.

### 대체 방법: YouTube에서 다시 받기
영상 원본(권리 미확인 · 공개 금지 · 내부/심사용만):
- 원본(2:01:33, 침착맨 게임 풀버전): https://www.youtube.com/watch?v=wnXAkjgVELc
- 사람 편집본(23:18, 침착맨 플러스): https://www.youtube.com/watch?v=GVHagGsmLck

```
# 내부 자료 저장소 루트(cutline-internal)에서 실행
python -m venv .venv
.venv\Scripts\python -m pip install yt-dlp numpy
powershell -NoProfile -ExecutionPolicy Bypass -File .\demo-chim\download.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\demo-chim\download.ps1
```
- 다운로드 스크립트는 저장소 루트의 가상환경을 사용하고, 두 영상을 `demo-chim/sources/original.mp4`, `demo-chim/reference/human_edit.mp4`에 복원한다. 기존 파일은 보존한다. 다른 Python을 쓰려면 `-Python 'C:/경로/python.exe'`를 지정한다.
- 원 PC의 원본은 `original.mp4` 231MB, 길이 7293.06초. 다른 포맷으로 받히면 길이가 수십 ms 다를 수 있으나 타임라인(초 단위)은 그대로 쓸 수 있다.
- **CLI 경로:** 최신 wrapper는 `CUTLINE_CLI_PATH` 환경변수 → `demo-chim/.cutline/cli-path.txt` → 나란히 둔 `cutline/out/cli.js` 순으로 찾는다. 두 저장소를 나란히 clone하고 앱을 빌드했다면 수정할 필요가 없다. Release 앱에서는 압축을 푼 `Cutline/out/cli.js`의 절대경로를 `demo-chim/.cutline/cli-path.txt`에 UTF-8로 저장하면 재실행 뒤에도 사용한다. 환경변수를 사용한다면 `$env:CUTLINE_CLI_PATH='C:/실제/경로/Cutline/out/cli.js'`를 설정한 **같은 터미널에서 앱을 새로 실행**한다. 이미 열려 있던 앱에는 새 환경변수가 전달되지 않는다. 로컬 설정 파일은 Git에서 제외된다.
- 이미 들어 있는 것: `transcripts/original.mp4.json`(faster-whisper base), `reference/human_edit.timeline.json`(정답 99구간), `style.md`, `AGENTS.md`/`CLAUDE.md`, `tools/compare.js`.
- Cutline에서 처음 열면 재생용 변환(프록시)에 20~45분 걸린다.
- 후속 검증: 이번 PC에서 패키지 Cutline으로 2시간 원본의 `canplay`, 시작·중간·끝 탐색과 프레임·오디오 디코딩을 확인했다. 이번 720p 원본의 WebM 변환은 14분 46초였다. 2시간 연속 재생 검사는 아니다. 재현 명령과 숫자 결과는 `CONTINUE_HERE.md` 참고.

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
